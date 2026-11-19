#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Four-year Chicago theft audit/backtest (2021-2024)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "d1_denominator"
AUDIT = OUT / "audit_chicago"


def top(idx, rate, k):
    k = min(k, len(idx))
    return set(idx[np.lexsort((idx, -rate[idx]))[:k]]) if k > 0 else set()


def met(S, y, pop, pov, total):
    S = list(S)
    return float(np.average(pov[S], weights=pop[S] + 1e-9)), float(y[S].sum() / total)


def main():
    socio = pd.read_csv(ROOT / "data/processed/grid_socio.csv").set_index("grid_id").reindex(range(1246))
    pop, pov = socio["pop"].values, socio["poverty"].values
    crime = pd.read_csv(OUT / "crime_2021_2024_grid.csv").set_index("grid_id").reindex(range(1246)).fillna(0)
    th = pd.read_csv(OUT / "theft_by_year.csv").set_index("grid_id").reindex(range(1246)).fillna(0)
    crime["THEFT_2022"] = th["theft_2022"].values
    crime["THEFT_2023"] = th["theft_2023"].values
    div = pd.read_csv(ROOT / "data/processed/od_corrected/divvy_2022_2023_grid_year_daypart.csv")
    act_year = div.groupby(["grid_id", "year"])["total"].sum().unstack(fill_value=0).reindex(range(1246), fill_value=0)
    activity = {}
    for y in [2021, 2024]:
        activity[y] = pd.read_csv(OUT / f"divvy_activity_{y}.csv", index_col=0)["activity"].reindex(range(1246), fill_value=0).values
    for y in [2022, 2023]:
        activity[y] = act_year[y].values
    elig = pop >= 100
    ai = np.where(elig)[0]
    T, K = None, 100
    dec_rows, bt_rows = [], []
    for y in [2021, 2022, 2023, 2024]:
        ytr = crime[f"THEFT_{y}"].values.astype(float)
        act = activity[y].astype(float)
        T = float(np.quantile(act[elig], 0.90))
        cov = elig & (act >= T)
        ci, ui = np.where(cov)[0], np.where(elig & ~cov)[0]
        total = ytr[ai].sum()
        ra = ytr / (act + T); rr = ytr / (pop + 1e-9)
        cs = ytr[ci].sum() / total
        kc = min(int(round(K * cs)), len(ci), K); ku = min(K - kc, len(ui))
        H = top(ci, ra, kc) | top(ui, rr, ku)
        M = top(ci, rr, kc) | top(ui, rr, ku)
        R = top(ai, rr, K)
        A = top(ci, ra, min(K, len(ci)))
        Mn = top(ci, rr, min(K, len(ci)))
        h, m, r = met(H, ytr, pop, pov, total), met(M, ytr, pop, pov, total), met(R, ytr, pop, pov, total)
        a, mn = met(A, ytr, pop, pov, total), met(Mn, ytr, pop, pov, total)
        dec_rows.append(dict(year=y, covered=int(cov.sum()), theft=int(total),
                             pov_den=h[0] - m[0], pov_cov=m[0] - r[0],
                             cap_den=(h[1] - m[1]) * 100, cap_cov=(m[1] - r[1]) * 100,
                             naive_pov_den=a[0] - mn[0], naive_pov_cov=mn[0] - r[0],
                             naive_cap_den=(a[1] - mn[1]) * 100, naive_cap_cov=(mn[1] - r[1]) * 100))
        # backtest to next year
        if y < 2024:
            yte = crime[f"THEFT_{y+1}"].values.astype(float)
            total_te = yte[ai].sum()
            rte, ate, hte = met(R, yte, pop, pov, total_te), met(A, yte, pop, pov, total_te), met(H, yte, pop, pov, total_te)
            best = None
            for k in range(0, K + 1):
                if k > len(ci) or (K - k) > len(ui):
                    continue
                S = top(ci, ra, k) | top(ui, rr, K - k)
                pr, cr = met(S, ytr, pop, pov, total)
                pte, cte = met(S, yte, pop, pov, total_te)
                if best is None or cr > best[1]:
                    best = (k, cr, pte, cte)
            bt_rows.append(dict(train=y, test=y + 1, strategy="residential", kc=0,
                                pov_test=rte[0], cap_test=rte[1] * 100))
            bt_rows.append(dict(train=y, test=y + 1, strategy="ambient_only", kc=min(K, len(ci)),
                                pov_test=ate[0], cap_test=ate[1] * 100))
            bt_rows.append(dict(train=y, test=y + 1, strategy="fixed_hybrid", kc=kc,
                                pov_test=hte[0], cap_test=hte[1] * 100))
            S = top(ci, ra, best[0]) | top(ui, rr, K - best[0])
            # re-evaluate test for best (already in best)
            bt_rows.append(dict(train=y, test=y + 1, strategy="optimized", kc=best[0],
                                pov_test=best[2], cap_test=best[3] * 100))

            # Simple baselines: prior-year crime count; matched coverage with optimized quota only.
            S_hist = top(ai, ytr + 1e-9 * rr, K)
            h_te = met(S_hist, yte, pop, pov, total_te)
            bt_rows.append(dict(train=y, test=y + 1, strategy="historical_count", kc=0,
                                pov_test=h_te[0], cap_test=h_te[1] * 100))

            best_m = None
            for k in range(0, K + 1):
                if k > len(ci) or (K - k) > len(ui):
                    continue
                S = top(ci, rr, k) | top(ui, rr, K - k)
                pr, cr = met(S, ytr, pop, pov, total)
                pte, cte = met(S, yte, pop, pov, total_te)
                if best_m is None or cr > best_m[1]:
                    best_m = (k, cr, pte, cte)
            bt_rows.append(dict(train=y, test=y + 1, strategy="matched_optimized", kc=best_m[0],
                                pov_test=best_m[2], cap_test=best_m[3] * 100))

            # Fixed-quota H/M comparison: 50 covered slots, same total budget.
            kfix = 50
            Hf = top(ci, ra, kfix) | top(ui, rr, K - kfix)
            Mf = top(ci, rr, kfix) | top(ui, rr, K - kfix)
            hf, mf = met(Hf, yte, pop, pov, total_te), met(Mf, yte, pop, pov, total_te)
            bt_rows.append(dict(train=y, test=y + 1, strategy="hybrid_fixed50", kc=kfix,
                                pov_test=hf[0], cap_test=hf[1] * 100))
            bt_rows.append(dict(train=y, test=y + 1, strategy="matched_fixed50", kc=kfix,
                                pov_test=mf[0], cap_test=mf[1] * 100))
    pd.DataFrame(dec_rows).to_csv(AUDIT / "four_year_quantile_decomposition.csv", index=False)
    pd.DataFrame(bt_rows).to_csv(AUDIT / "four_year_quantile_backtest.csv", index=False)
    print("decomposition"); print(pd.DataFrame(dec_rows).round(2).to_string(index=False))
    print("backtest"); print(pd.DataFrame(bt_rows).round(2).to_string(index=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Leakage-free half-year folds using activity measured only up to the training cutoff."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/processed/d1_denominator"
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
    hy = pd.read_csv(OUT / "theft_halfyear.csv").set_index("grid_id").reindex(range(1246)).fillna(0)
    a = pd.read_csv(OUT / "divvy_halfyear_activity.csv")
    act = a.pivot_table(index="grid_id", columns="fold", values="activity", aggfunc="sum").reindex(range(1246), fill_value=0)
    elig = pop >= 100; ai = np.where(elig)[0]
    rows = []
    for tr, te in [("2022H1", "2022H2"), ("2022H2", "2023H1"), ("2023H1", "2023H2")]:
        ytr = hy[tr].values.astype(float); yte = hy[te].values.astype(float)
        atr = act[tr].values.astype(float)
        T = float(np.quantile(atr[elig], 0.90))
        cov = elig & (atr >= T)
        ci, ui = np.where(cov)[0], np.where(elig & ~cov)[0]
        total_tr, total_te = ytr[ai].sum(), yte[ai].sum()
        ra = ytr / (atr + T); rr = ytr / (pop + 1e-9)
        K = 100
        cs = ytr[ci].sum() / total_tr
        kc = min(int(round(K * cs)), len(ci), K); ku = min(K - kc, len(ui))
        R = top(ai, rr, K); A = top(ci, ra, min(K, len(ci)))
        H = top(ci, ra, kc) | top(ui, rr, ku)
        best = None
        for k in range(0, K + 1):
            if k > len(ci) or (K - k) > len(ui): continue
            S = top(ci, ra, k) | top(ui, rr, K - k)
            _, cr = met(S, ytr, pop, pov, total_tr)
            if best is None or cr > best[1]: best = (k, cr)
        Sopt = top(ci, ra, best[0]) | top(ui, rr, K - best[0])
        for name, S, kk in [("residential", R, 0), ("ambient_only", A, min(K, len(ci))), ("fixed_hybrid", H, kc), ("optimized", Sopt, best[0])]:
            p, c = met(S, yte, pop, pov, total_te)
            rows.append(dict(train=tr, test=te, strategy=name, kc=kk, covered=len(ci), T=T, pov_test=p, cap_test=c * 100))
    res = pd.DataFrame(rows); res.to_csv(AUDIT / "backtest_folds_fixed.csv", index=False)
    print(res.round(3).to_string(index=False))

if __name__ == "__main__":
    main()

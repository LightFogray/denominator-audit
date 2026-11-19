#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reporting-bias bounds for the Denominator Audit (Chicago theft).

Simulates reporting rates correlated with income or activity, adjusts counts,
and recomputes the H/M/R decomposition. This is a bounds/sensitivity exercise,
not a correction.
"""
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
    return dict(poverty=float(np.average(pov[S], weights=pop[S] + 1e-9)),
                captured=float(y[S].sum() / total))


def decompose(y, pop, pov, act, ci, ui, ai, K, kc, ku, kc_n):
    total = y[ai].sum()
    rate_amb = y / (act + 25000)
    rate_res = y / (pop + 1e-9)
    H = top(ci, rate_amb, kc) | top(ui, rate_res, ku)
    M = top(ci, rate_res, kc) | top(ui, rate_res, ku)
    R = top(ai, rate_res, K)
    A = top(ci, rate_amb, kc_n)
    Mn = top(ci, rate_res, kc_n)
    h, m, r = met(H, y, pop, pov, total), met(M, y, pop, pov, total), met(R, y, pop, pov, total)
    a, mn = met(A, y, pop, pov, total), met(Mn, y, pop, pov, total)
    return dict(
        pov_den=h["poverty"] - m["poverty"], pov_cov=m["poverty"] - r["poverty"],
        cap_den=h["captured"] - m["captured"], cap_cov=m["captured"] - r["captured"],
        naive_pov_den=a["poverty"] - mn["poverty"], naive_pov_cov=mn["poverty"] - r["poverty"],
        naive_cap_den=a["captured"] - mn["captured"], naive_cap_cov=mn["captured"] - r["captured"],
        pov_h=h["poverty"], pov_r=r["poverty"], cap_h=h["captured"], cap_r=r["captured"],
    )


def main():
    socio = pd.read_csv(ROOT / "data/processed/grid_socio.csv").set_index("grid_id").reindex(range(1246))
    sub = pd.read_csv(OUT / "property_subtypes_grid.csv").set_index("grid_id").reindex(range(1246))
    z = np.load(ROOT / "data/processed/od_corrected/divvy_2022_2023_activity.npz")
    act = (z["inflow"] + z["outflow"]).sum(axis=(0, 1))
    pop, pov, inc = socio["pop"].values, socio["poverty"].values, socio["income"].values
    y = sub["THEFT"].values.astype(float)
    elig = pop >= 100
    ai = np.where(elig)[0]
    T = 25000
    ci, ui = np.where(elig & (act >= T))[0], np.where(elig & (act < T))[0]
    K = 119
    crime_share = y[ci].sum() / y[ai].sum()
    kc = min(int(round(K * crime_share)), len(ci), K)
    ku = min(K - kc, len(ui))
    kc_n = min(K, len(ci))

    def zs(x):
        x = np.asarray(x, float)
        return (x - x.mean()) / (x.std() + 1e-9)

    zi, za = zs(np.log1p(np.maximum(inc, 0))), zs(np.log1p(act))
    scenarios = [("uniform", np.full(1246, 0.5))]
    for b in [0.3, 0.5, 0.8]:
        r = 1 / (1 + np.exp(-(b * zi))); scenarios.append((f"income_pos_{b}", np.clip(r, 0.15, 0.85)))
        r = 1 / (1 + np.exp(-(-b * zi))); scenarios.append((f"income_neg_{b}", np.clip(r, 0.15, 0.85)))
        r = 1 / (1 + np.exp(-(b * za))); scenarios.append((f"activity_pos_{b}", np.clip(r, 0.15, 0.85)))
        r = 1 / (1 + np.exp(-(-b * za))); scenarios.append((f"activity_neg_{b}", np.clip(r, 0.15, 0.85)))

    rows = []
    for name, r in scenarios:
        y_adj = y / r
        d = decompose(y_adj, pop, pov, act, ci, ui, ai, K, kc, ku, kc_n)
        rows.append(dict(scenario=name, r_mean=float(r[elig].mean()),
                         pov_den=d["pov_den"], pov_cov=d["pov_cov"],
                         cap_den=d["cap_den"] * 100, cap_cov=d["cap_cov"] * 100,
                         naive_pov_den=d["naive_pov_den"], naive_pov_cov=d["naive_pov_cov"],
                         naive_cap_den=d["naive_cap_den"] * 100, naive_cap_cov=d["naive_cap_cov"] * 100))
    res = pd.DataFrame(rows)
    res.to_csv(AUDIT / "reporting_bounds.csv", index=False)
    print(res.round(2).to_string(index=False))


if __name__ == "__main__":
    main()

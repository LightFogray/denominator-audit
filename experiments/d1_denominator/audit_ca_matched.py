#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matched coverage/selection sensitivity: grid vs community area, 2022->2023."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/processed/d1_denominator"
AUDIT = OUT / "audit_ca_matched"
AUDIT.mkdir(parents=True, exist_ok=True)

def top(idx, rate, k):
    k = min(k, len(idx))
    return set(idx[np.lexsort((idx, -rate[idx]))[:k]]) if k > 0 else set()

def met(S, y, pop, pov, total):
    S = list(S)
    return float(np.average(pov[S], weights=pop[S] + 1e-9)), float(y[S].sum() / total)

def run(df, label, K):
    elig = df["pop"].values >= 100
    ai = np.where(elig)[0]
    y = df["th22"].values.astype(float); yte = df["th23"].values.astype(float)
    act = df["act22"].values.astype(float); pop = df["pop"].values; pov = df["pov"].values
    T = float(np.quantile(act[elig], 0.662))
    cov = elig & (act >= T)
    ci, ui = np.where(cov)[0], np.where(elig & ~cov)[0]
    total, total_te = y[ai].sum(), yte[ai].sum()
    ra = y / (act + T); rr = y / (pop + 1e-9)
    R = top(ai, rr, K); A = top(ci, ra, min(K, len(ci)))
    best = None
    for k in range(0, K + 1):
        if k > len(ci) or (K - k) > len(ui):
            continue
        S = top(ci, ra, k) | top(ui, rr, K - k)
        _, cr = met(S, y, pop, pov, total)
        if best is None or cr > best[1]:
            best = (k, cr)
    Sopt = top(ci, ra, best[0]) | top(ui, rr, K - best[0])
    rows = []
    for name, S in [("residential", R), ("ambient_only", A), ("optimized", Sopt)]:
        p, c = met(S, yte, pop, pov, total_te)
        rows.append(dict(unit=label, strategy=name, K=K, covered=len(ci), eligible=len(ai),
                         coverage_share=len(ci)/len(ai), kc=best[0] if name=="optimized" else (min(K,len(ci)) if name=="ambient_only" else 0),
                         pov_test=p, cap_test=c*100))
    return rows

socio = pd.read_csv(ROOT / "data/processed/grid_socio.csv").set_index("grid_id").reindex(range(1246))
theft = pd.read_csv(OUT / "theft_by_year.csv").set_index("grid_id").reindex(range(1246)).fillna(0)
div = pd.read_csv(ROOT / "data/processed/od_corrected/divvy_2022_2023_grid_year_daypart.csv")
act = div[div.year == 2022].groupby("grid_id")["total"].sum().reindex(range(1246), fill_value=0)
ctx = pd.read_csv(ROOT / "data/processed/grid_context.csv").set_index("grid_id").reindex(range(1246))
grid = pd.DataFrame({"pop": socio["pop"].values, "pov": socio["poverty"].values,
                     "th22": theft["theft_2022"].values, "th23": theft["theft_2023"].values,
                     "act22": act.values, "ca": ctx.community_area.fillna(-1).astype(int).values})
grid = grid[grid["pop"] >= 100]
ca = grid[grid.ca > 0].groupby("ca").agg(pop=("pop","sum"), th22=("th22","sum"), th23=("th23","sum"), act22=("act22","sum"))
ca["pov"] = grid[grid.ca > 0].groupby("ca").apply(lambda d: np.average(d.pov, weights=d["pop"]+1e-9))
rows = run(grid, "grid", 100) + run(ca.reset_index(), "community_area", 7)
out = pd.DataFrame(rows); out.to_csv(AUDIT / "compare.csv", index=False)
print(out.round(3).to_string(index=False))

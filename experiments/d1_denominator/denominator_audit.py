#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Denominator Audit (Route A prototype).

Chicago grid input → coverage, reliability, H/M/R decomposition with
leave-one-community-out min-max, priority maps, frontier, one-page report.

Usage:
  python denominator_audit.py --crime THEFT --k 119 --threshold 25000
"""
from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "d1_denominator"
AUDIT = OUT / "audit_chicago"


def load_data():
    socio = pd.read_csv(ROOT / "data/processed/grid_socio.csv").set_index("grid_id").reindex(range(1246))
    sub = pd.read_csv(OUT / "property_subtypes_grid.csv").set_index("grid_id").reindex(range(1246))
    z = np.load(ROOT / "data/processed/od_corrected/divvy_2022_2023_activity.npz")
    act = (z["inflow"] + z["outflow"]).sum(axis=(0, 1))
    ctx = pd.read_csv(ROOT / "data/processed/grid_context.csv").set_index("grid_id").reindex(range(1246))
    ca = ctx["community_area"].fillna(-1).astype(int).values
    return socio, sub, act, ca


def top(idx, rate, k):
    k = min(k, len(idx))
    return set(idx[np.lexsort((idx, -rate[idx]))[:k]]) if k > 0 else set()


def met(S, y, pop, pov, total):
    S = list(S)
    return dict(n=len(S),
                poverty=float(np.average(pov[S], weights=pop[S] + 1e-9)),
                captured=float(y[S].sum() / total))


def sets_and_terms(ci, ui, ai, y, pop, pov, rate_amb, rate_res, K, kc, ku, kc_n):
    total = y[ai].sum()
    H = top(ci, rate_amb, kc) | top(ui, rate_res, ku)
    M = top(ci, rate_res, kc) | top(ui, rate_res, ku)
    R = top(ai, rate_res, K)
    A = top(ci, rate_amb, kc_n)
    Mn = top(ci, rate_res, kc_n)
    h, m, r = met(H, y, pop, pov, total), met(M, y, pop, pov, total), met(R, y, pop, pov, total)
    a, mn = met(A, y, pop, pov, total), met(Mn, y, pop, pov, total)
    return dict(
        H=h, M=m, R=r, A=a, Mn=mn, H_set=H, M_set=M, R_set=R, A_set=A, Mn_set=Mn,
        hybrid_pov_total=h["poverty"] - r["poverty"],
        hybrid_pov_den=h["poverty"] - m["poverty"],
        hybrid_pov_cov=m["poverty"] - r["poverty"],
        hybrid_cap_total=h["captured"] - r["captured"],
        hybrid_cap_den=h["captured"] - m["captured"],
        hybrid_cap_cov=m["captured"] - r["captured"],
        naive_pov_total=a["poverty"] - r["poverty"],
        naive_pov_den=a["poverty"] - mn["poverty"],
        naive_pov_cov=mn["poverty"] - r["poverty"],
        naive_cap_total=a["captured"] - r["captured"],
        naive_cap_den=a["captured"] - mn["captured"],
        naive_cap_cov=mn["captured"] - r["captured"],
    )


def jackknife(ci, ui, ai, y, pop, pov, rate_amb, rate_res, K, kc, ku, kc_n, ca):
    terms = []
    for a in [x for x in np.unique(ca) if x > 0]:
        ci_s = ci[ca[ci] != a]
        ui_s = ui[ca[ui] != a]
        ai_s = ai[ca[ai] != a]
        if len(ci_s) < 20 or len(ui_s) < 5:
            continue
        kc_s = min(kc, len(ci_s), K)
        ku_s = min(K - kc_s, len(ui_s))
        kc_n_s = min(kc_n, len(ci_s))
        d = sets_and_terms(ci_s, ui_s, ai_s, y, pop, pov, rate_amb, rate_res, K, kc_s, ku_s, kc_n_s)
        terms.append([d[k] for k in [
            "hybrid_pov_den", "hybrid_pov_cov", "hybrid_cap_den", "hybrid_cap_cov",
            "naive_pov_den", "naive_pov_cov", "naive_cap_den", "naive_cap_cov"]])
    arr = np.array(terms)
    n = len(arr)
    means = arr.mean(0)
    se = np.sqrt((n - 1) / n * ((arr - means) ** 2).sum(0))
    return {name: (float(means[i]), float(arr[:, i].min()), float(arr[:, i].max()))
            for i, name in enumerate([
                "hybrid_pov_den", "hybrid_pov_cov", "hybrid_cap_den", "hybrid_cap_cov",
                "naive_pov_den", "naive_pov_cov", "naive_cap_den", "naive_cap_cov"])}, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crime", default="THEFT")
    ap.add_argument("--k", type=int, default=119)
    ap.add_argument("--threshold", type=int, default=25000)
    ap.add_argument("--stabilize", type=int, default=25000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    global AUDIT
    AUDIT = OUT / (args.out or "audit_chicago")
    AUDIT.mkdir(parents=True, exist_ok=True)

    socio, sub, act, ca = load_data()
    pop = socio["pop"].values
    pov = socio["poverty"].values
    if args.crime not in sub.columns:
        raise SystemExit(f"crime column {args.crime} not found; choose from {list(sub.columns)}")
    y = sub[args.crime].values.astype(float)
    elig = pop >= 100
    ai = np.where(elig)[0]
    total = y[ai].sum()

    # 1. coverage
    cov = pd.DataFrame([
        dict(threshold=T, grids=int((elig & (act >= T)).sum()),
             grid_share=float((elig & (act >= T)).sum() / elig.sum()),
             population_share=float(pop[elig & (act >= T)].sum() / pop[ai].sum()),
             crime_share=float(y[elig & (act >= T)].sum() / total))
        for T in [1000, 5000, 10000, 25000, 50000, 100000]
    ])
    cov.to_csv(AUDIT / "coverage.csv", index=False)

    # 2. reliability
    bins = [0, 1000, 5000, 10000, 25000, 50000, 100000, np.inf]
    labels = ["<1k", "1k-5k", "5k-10k", "10k-25k", "25k-50k", "50k-100k", ">100k"]
    rel = pd.DataFrame({"bin": pd.cut(act, bins=bins, labels=labels, right=False), "y": y, "act": act, "pop": pop})
    rel = rel[elig].groupby("bin", observed=False).agg(grids=("y", "size"), crime=("y", "sum"), activity=("act", "sum"))
    rel["rate_per_100k_trips"] = rel["crime"] / (rel["activity"] + 1e-9) * 100000
    rel.to_csv(AUDIT / "reliability.csv")

    # 3. decomposition
    T = args.threshold
    c = args.stabilize
    ci, ui = np.where(elig & (act >= T))[0], np.where(elig & (act < T))[0]
    rate_amb = y / (act + c)
    rate_res = y / (pop + 1e-9)
    crime_share = y[ci].sum() / total
    kc = min(int(round(args.k * crime_share)), len(ci), args.k)
    ku = args.k - kc
    if ku > len(ui):
        ku = len(ui); kc = args.k - ku
    kc_n = min(args.k, len(ci))
    d = sets_and_terms(ci, ui, ai, y, pop, pov, rate_amb, rate_res, args.k, kc, ku, kc_n)
    jk, n_jk = jackknife(ci, ui, ai, y, pop, pov, rate_amb, rate_res, args.k, kc, ku, kc_n, ca)

    rows = []
    for prefix, label in [("hybrid", "hybrid_vs_residential"), ("naive", "naive_ambient_only_vs_residential")]:
        for metric, key in [("poverty", "pov"), ("captured", "cap")]:
            rows.append(dict(comparison=label, metric=metric,
                             total=d[f"{prefix}_{key}_total"],
                             denominator=d[f"{prefix}_{key}_den"],
                             coverage=d[f"{prefix}_{key}_cov"],
                             den_lo=jk[f"{prefix}_{key}_den"][1], den_hi=jk[f"{prefix}_{key}_den"][2],
                             cov_lo=jk[f"{prefix}_{key}_cov"][1], cov_hi=jk[f"{prefix}_{key}_cov"][2]))
    dec = pd.DataFrame(rows)
    # capture terms are proportions; convert to percentage points for consistency
    cap = dec.metric == "captured"
    for col in ["total", "denominator", "coverage", "den_lo", "den_hi", "cov_lo", "cov_hi"]:
        dec.loc[cap, col] = dec.loc[cap, col] * 100
    dec.to_csv(AUDIT / "decomposition.csv", index=False)

    # 4. maps
    grid = gpd.read_file(ROOT / "data/processed/chicago_grid.geojson")
    grid["cat"] = "other"
    grid.loc[list(d["R_set"]), "cat"] = "residential"
    grid.loc[list(d["H_set"]), "cat"] = "hybrid"
    grid.loc[list(d["A_set"]), "cat"] = "ambient_only"
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
    for ax, cat, title, col in zip(axes, ["residential", "hybrid", "ambient_only"],
                                   ["Residential top-K", "Coverage-aware hybrid", "Ambient-only top-K"],
                                   ["#4c72b0", "#55a868", "#c44e52"]):
        grid.plot(ax=ax, color="#eeeeee", edgecolor="white", linewidth=0.15)
        s = grid[grid.cat == cat]
        if len(s):
            s.plot(ax=ax, color=col, edgecolor="white", linewidth=0.15)
        ax.set_title(title, fontsize=9, fontweight="bold"); ax.set_axis_off()
    plt.suptitle(f"{args.crime} priority maps (K={args.k}, T={T})", fontweight="bold")
    plt.tight_layout()
    plt.savefig(AUDIT / "priority_maps.png", dpi=200, bbox_inches="tight")

    # 5. frontier
    fr = []
    for f in np.linspace(0, 1, 21):
        kc_f = int(round(args.k * f)); ku_f = args.k - kc_f
        S = top(ci, rate_amb, kc_f) | top(ui, rate_res, ku_f)
        mm = met(S, y, pop, pov, total)
        fr.append(dict(covered_share=f, captured=mm["captured"], poverty=mm["poverty"]))
    fr = pd.DataFrame(fr); fr.to_csv(AUDIT / "frontier.csv", index=False)
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.plot(fr["captured"] * 100, fr["poverty"], "o-", color="#4c72b0")
    ax.set_xlabel("Crime captured (%)"); ax.set_ylabel("Poverty in selected grids (%)")
    ax.set_title("Efficiency–equity frontier of coverage allocation", loc="left", fontweight="bold")
    plt.tight_layout(); plt.savefig(AUDIT / "frontier.png", dpi=200, bbox_inches="tight")

    # 6. report
    cov_fmt = cov.copy()
    cov_fmt["threshold"] = cov_fmt["threshold"].astype(int).astype(str)
    cov_fmt["grids"] = cov_fmt["grids"].astype(int).astype(str)
    lines = [f"# Denominator Audit — Chicago {args.crime}\n",
             f"**K** = {args.k}; **activity threshold T** = {T:,}; **stabilization c** = {c:,}; **jackknife n** = {n_jk}.\n",
             "## 1. Coverage\n",
             cov_fmt.to_markdown(index=False, floatfmt=".3f"),
             "\n## 2. Reliability (aggregate rate by activity bin)\n",
             rel.reset_index().assign(grids=lambda x: x.grids.astype(int), crime=lambda x: x.crime.astype(int),
                                      activity=lambda x: x.activity.astype(int), rate_per_100k_trips=lambda x: x.rate_per_100k_trips.round(1)).to_markdown(index=False),
             "\n## 3. Decomposition (percentage points; leave-one-community-out min-max)\n",
             dec.assign(total=lambda x: x.total.round(2), denominator=lambda x: x.denominator.round(2),
                        coverage=lambda x: x.coverage.round(2), den_lo=lambda x: x.den_lo.round(2),
                        den_hi=lambda x: x.den_hi.round(2), cov_lo=lambda x: x.cov_lo.round(2),
                        cov_hi=lambda x: x.cov_hi.round(2)).to_markdown(index=False),
             "\n## 4. Headline\n",
             f"- residential: capture {d['R']['captured']:.1%}, poverty {d['R']['poverty']:.1f}%",
             f"- hybrid: capture {d['H']['captured']:.1%}, poverty {d['H']['poverty']:.1f}%",
             f"- ambient-only (covered): capture {d['A']['captured']:.1%}, poverty {d['A']['poverty']:.1f}%",
             "\n## 5. Recommendation\n",
             "- Use ambient only where activity is above the reliability threshold; use residential outside.",
             "- Report coverage, selection rate/K, denominator, and crime type.",
             "- Do not interpret naive ambient-vs-residential differences as denominator effects without the decomposition.",
             "\n## 6. Robustness (separate files)\n",
             "- `reporting_bounds.csv`: decomposition under reporting-rate scenarios.",
             "- `sensitivity.csv`: K × threshold sensitivity.",
             "- `../audit_chicago_burglary/` and `../audit_chicago_vehicle/`: crime-type controls.",
             "- `backtest_report.md` and `backtest_folds.csv`: out-of-time allocation test (year and half-year folds).",
             "- K must not exceed the covered stratum for the ambient-only comparison; otherwise the capacity constraint dominates.",
             "\n## 7. Caveats\n",
             "- Activity proxy is not a general ambient population.",
             "- Recorded crime; reporting bias not adjusted.",
             "- Decomposition is descriptive, not causal.",
             "- Deletion ranges describe single-community influence, not confidence intervals."]
    (AUDIT / "audit_report.md").write_text("\n".join(lines), encoding="utf-8")
    print("saved", AUDIT)
    print(dec.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

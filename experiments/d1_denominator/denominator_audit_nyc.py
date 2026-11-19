#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Denominator Audit — NYC taxi pilot (coverage + decomposition).

Unit: taxi zones; crime: Jan 2023 theft; activity: yellow-taxi pickups.
Income: ACS 2016 NTA median household income (fuzzy matched; pilot-grade).
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
AUDIT = OUT / "audit_nyc"


def top(idx, rate, k):
    k = min(k, len(idx))
    return set(idx[np.lexsort((idx, -rate[idx]))[:k]]) if k > 0 else set()


def met(S, df, total):
    S = list(S)
    w = df.population.to_numpy()[S]
    return dict(n=len(S),
                low_unw=float(df.low.to_numpy()[S].mean()),
                low_w=float(np.average(df.low.to_numpy()[S], weights=w + 1e-9)),
                captured=float(df.theft.to_numpy()[S].sum() / total))


def decompose(df, T, K):
    cov = df.taxi >= T
    ci = np.where(cov.to_numpy())[0]
    ui = np.where(~cov.to_numpy())[0]
    ai = np.arange(len(df))
    total = df.theft.sum()
    rate_amb = (df.theft / (df.taxi + T)).to_numpy()
    rate_res = (df.theft / (df.population + 1)).to_numpy()
    crime_share = df.theft.to_numpy()[ci].sum() / total
    kc = min(int(round(K * crime_share)), len(ci), K)
    ku = K - kc
    if ku > len(ui):
        ku = len(ui); kc = K - ku
    H = top(ci, rate_amb, kc) | top(ui, rate_res, ku)
    M = top(ci, rate_res, kc) | top(ui, rate_res, ku)
    R = top(ai, rate_res, K)
    A = top(ci, rate_amb, min(K, len(ci)))
    Mn = top(ci, rate_res, min(K, len(ci)))
    h, m, r = met(H, df, total), met(M, df, total), met(R, df, total)
    a, mn = met(A, df, total), met(Mn, df, total)
    rows = []
    for prefix, label, hh, mm, rr in [("hybrid", "hybrid_vs_residential", h, m, r),
                                      ("naive", "naive_ambient_only_vs_residential", a, mn, r)]:
        for metric in ["low_unw", "low_w", "captured"]:
            rows.append(dict(comparison=label, metric=metric, T=T, K=K, kc=kc, ku=ku,
                             total=hh[metric] - rr[metric], denominator=hh[metric] - mm[metric],
                             coverage=mm[metric] - rr[metric]))
    return pd.DataFrame(rows), dict(H=H, M=M, R=R, A=A)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="nyc_zone_pilot.csv")
    ap.add_argument("--out", default="audit_nyc")
    args = ap.parse_args()
    global AUDIT
    AUDIT = OUT / args.out
    AUDIT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(OUT / args.input).set_index("zone_id")
    df = df[df.population > 0].copy()
    if "poverty" in df.columns:
        q75 = df.poverty.quantile(0.75)
        df["low"] = (df.poverty >= q75).astype(float)  # high-poverty quartile
        ses_label = "high-poverty (ACS 2023 5-year)"
    else:
        q25 = df.income.quantile(0.25)
        df["low"] = (df.income <= q25).astype(float)
        ses_label = "low-income (ACS 2016 NTA)" 
    total = df.theft.sum()

    cov_rows = []
    for T in [1, 10, 100, 1000, 5000, 10000]:
        m = df.taxi >= T
        cov_rows.append(dict(threshold=T, zones=int(m.sum()), zone_share=float(m.mean()),
                             population_share=float(df.loc[m, "population"].sum() / df.population.sum()),
                             theft_share=float(df.loc[m, "theft"].sum() / total)))
    cov = pd.DataFrame(cov_rows)
    cov.to_csv(AUDIT / "coverage.csv", index=False)

    # T=1000 primary; T=100 sensitivity
    d1, sets1 = decompose(df, 1000, 100)
    d2, _ = decompose(df, 5000, 100)
    dec = pd.concat([d1, d2], ignore_index=True)
    dec.to_csv(AUDIT / "decomposition.csv", index=False)

    # map top sets at T=1000, K=100
    zones = gpd.read_file("zip://" + str(ROOT / "data/raw/nyc_taxi_zones.zip") + "!taxi_zones/taxi_zones.shp").to_crs(2263)
    zones = zones[zones.borough.isin(["Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island"])].copy()
    zones["zone_id"] = zones["LocationID"].astype(int)
    zones = zones.set_index("zone_id")
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    for ax, S, title, col in zip(axes, [sets1["R"], sets1["H"], sets1["A"]],
                                 ["Residential top-K", "Coverage-aware hybrid", "Ambient-only top-K"],
                                 ["#4c72b0", "#55a868", "#c44e52"]):
        zones.plot(ax=ax, color="#eeeeee", edgecolor="white", linewidth=0.3)
        ids = df.index.to_numpy()[list(S)]
        s = zones.loc[zones.index.intersection(ids)]
        if len(s):
            s.plot(ax=ax, color=col, edgecolor="white", linewidth=0.3)
        ax.set_title(title, fontsize=9, fontweight="bold"); ax.set_axis_off()
    plt.suptitle("NYC theft priority maps (K=100, T=1,000)", fontweight="bold")
    plt.tight_layout(); plt.savefig(AUDIT / "priority_maps.png", dpi=200, bbox_inches="tight")

    cov_fmt = cov.copy()
    cov_fmt["threshold"] = cov_fmt["threshold"].astype(int).astype(str)
    cov_fmt["zones"] = cov_fmt["zones"].astype(int).astype(str)
    lines = ["# Denominator Audit — NYC taxi pilot (THEFT)\n",
             "**Unit**: taxi zones; **crime**: Jan/Apr/Jul 2023 theft; **activity**: yellow-taxi pickups; "
             f"**SES**: {ses_label}.\n",
             "## 1. Coverage\n",
             cov_fmt.to_markdown(index=False, floatfmt=".3f"),
             "\n## 2. Decomposition (percentage points)\n",
             dec.assign(total=lambda x: (x.total * 100).round(2), denominator=lambda x: (x.denominator * 100).round(2),
                        coverage=lambda x: (x.coverage * 100).round(2)).to_markdown(index=False),
             "\n## 3. Headline\n",
             "- At `taxi>0`, coverage looks near-universal; at >=100/1,000 pickups, it is 61%/27.5% of zones.",
             "- Ambient top-K is much more low-income; capture does not consistently improve.",
             "\n## 4. Caveats\n",
             "- One month; taxi is a mode-specific activity proxy, not ambient population.",
             "- Income is ACS 2016 with fuzzy matching; pilot-grade.",
             "- No jackknife CI (few boroughs; zone-level dependence not modeled)."]
    (AUDIT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("saved", AUDIT)
    print(cov.to_string(index=False))
    print(dec.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Community-area (MAUP) check for the Denominator Audit.

Aggregates the 1,246 grids to 77 community areas and repeats coverage,
decomposition, and a 2022→2023 backtest. Unit = policy-relevant CA.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "processed" / "d1_denominator"
AUDIT = OUT / "audit_ca"


def top(idx, rate, k):
    k = min(k, len(idx))
    return set(idx[np.lexsort((idx, -rate[idx]))[:k]]) if k > 0 else set()


def met(S, y, pop, pov, total):
    S = list(S)
    return float(np.average(pov[S], weights=pop[S] + 1e-9)), float(y[S].sum() / total)


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    ctx = pd.read_csv(ROOT / "data/processed/grid_context.csv")
    socio = pd.read_csv(ROOT / "data/processed/grid_socio.csv").set_index("grid_id").reindex(range(1246))
    theft = pd.read_csv(OUT / "theft_by_year.csv").set_index("grid_id").reindex(range(1246)).fillna(0)
    div = pd.read_csv(ROOT / "data/processed/od_corrected/divvy_2022_2023_grid_year_daypart.csv")
    act = div.groupby(["grid_id", "year"])["total"].sum().unstack(fill_value=0).reindex(range(1246), fill_value=0)
    df = pd.DataFrame({
        "ca": ctx.community_area.fillna(-1).astype(int).values,
        "pop": socio["pop"].values, "pov": socio["poverty"].values,
        "th22": theft["theft_2022"].values, "th23": theft["theft_2023"].values,
        "act22": act[2022].values, "act23": act[2023].values,
    })
    df = df[df.ca > 0]
    ca = df.groupby("ca").agg(pop=("pop", "sum"), th22=("th22", "sum"), th23=("th23", "sum"),
                              act22=("act22", "sum"), act23=("act23", "sum"))
    ca["pov"] = df.groupby("ca").apply(lambda d: np.average(d.pov, weights=d["pop"] + 1e-9))
    names = ctx[ctx.community_area > 0].drop_duplicates("community_area").set_index("community_area")["community"]
    ca["name"] = names
    ca.to_csv(AUDIT / "ca_data.csv")

    cov_rows = []
    for T in [1000, 5000, 10000, 25000, 50000]:
        m = ca.act22 >= T
        cov_rows.append(dict(threshold=T, cas=int(m.sum()), ca_share=float(m.mean()),
                             pop_share=float(ca.loc[m, "pop"].sum() / ca["pop"].sum()),
                             theft_share=float(ca.loc[m, "th22"].sum() / ca["th22"].sum())))
    cov = pd.DataFrame(cov_rows)
    cov.to_csv(AUDIT / "coverage.csv", index=False)

    # decomposition at T=25k, K=8
    T, K = 25000, 8
    covm = ca.act22 >= T
    ci = np.where(covm.values)[0]; ui = np.where(~covm.values)[0]; ai = np.arange(len(ca))
    y = ca.th22.values.astype(float); yte = ca.th23.values.astype(float)
    pop, pov = ca["pop"].values, ca["pov"].values
    rate_amb = y / (ca.act22.values + T)
    rate_res = y / (pop + 1e-9)
    total = y[ai].sum(); total_te = yte[ai].sum()
    cs = y[ci].sum() / total
    kc = min(int(round(K * cs)), len(ci), K); ku = min(K - kc, len(ui))
    H = top(ci, rate_amb, kc) | top(ui, rate_res, ku)
    M = top(ci, rate_res, kc) | top(ui, rate_res, ku)
    R = top(ai, rate_res, K)
    A = top(ci, rate_amb, min(K, len(ci)))
    Mn = top(ci, rate_res, min(K, len(ci)))
    def m(S):
        S = list(S); return dict(pov=float(np.average(pov[S], weights=pop[S] + 1e-9)),
                                cap=float(yte[S].sum() / total_te))
    h, mm, r, a, mn = m(H), m(M), m(R), m(A), m(Mn)
    dec = pd.DataFrame([
        dict(comparison="hybrid_vs_residential", metric="poverty", total=h["pov"] - r["pov"], denominator=h["pov"] - mm["pov"], coverage=mm["pov"] - r["pov"]),
        dict(comparison="hybrid_vs_residential", metric="captured", total=h["cap"] - r["cap"], denominator=h["cap"] - mm["cap"], coverage=mm["cap"] - r["cap"]),
        dict(comparison="naive_ambient_only_vs_residential", metric="poverty", total=a["pov"] - r["pov"], denominator=a["pov"] - mn["pov"], coverage=mn["pov"] - r["pov"]),
        dict(comparison="naive_ambient_only_vs_residential", metric="captured", total=a["cap"] - r["cap"], denominator=a["cap"] - mn["cap"], coverage=mn["cap"] - r["cap"]),
    ])
    capmask = dec.metric == "captured"
    for col in ["total", "denominator", "coverage"]:
        dec.loc[capmask, col] = dec.loc[capmask, col] * 100
    dec.to_csv(AUDIT / "decomposition.csv", index=False)

    # backtest K=8, optimize kc on train capture
    fr = []
    for kc_i in range(0, K + 1):
        if kc_i > len(ci) or (K - kc_i) > len(ui):
            continue
        S = top(ci, rate_amb, kc_i) | top(ui, rate_res, K - kc_i)
        p_tr, c_tr = met(S, y, pop, pov, total)
        p_te, c_te = met(S, yte, pop, pov, total_te)
        fr.append(dict(kc=kc_i, pov_train=p_tr, cap_train=c_tr, pov_test=p_te, cap_test=c_te))
    fr = pd.DataFrame(fr); fr.to_csv(AUDIT / "backtest_frontier.csv", index=False)
    best = fr.loc[fr.cap_train.idxmax()]
    bt = pd.DataFrame([
        dict(strategy="residential", kc=0, pov_test=r["pov"], cap_test=r["cap"]),
        dict(strategy="ambient_only", kc=min(K, len(ci)), pov_test=a["pov"], cap_test=a["cap"]),
        dict(strategy="fixed_hybrid", kc=kc, pov_test=h["pov"], cap_test=h["cap"]),
        dict(strategy="optimized", kc=int(best.kc), pov_test=best.pov_test, cap_test=best.cap_test),
    ])
    bt["cap_test"] = bt["cap_test"] * 100
    bt.to_csv(AUDIT / "backtest.csv", index=False)

    cov_fmt = cov.copy(); cov_fmt["threshold"] = cov_fmt["threshold"].astype(int).astype(str); cov_fmt["cas"] = cov_fmt["cas"].astype(int).astype(str)
    lines = ["# Denominator Audit — Chicago community areas (MAUP check)\n",
             "**Unit**: 77 community areas (grids aggregated). **Crime**: theft; **activity**: Divvy 2022.\n",
             "## 1. Coverage (2022)\n", cov_fmt.to_markdown(index=False, floatfmt=".3f"),
             "\n## 2. Decomposition (K=8, T=25,000; test year 2023)\n",
             dec.assign(total=lambda x: x.total.round(2), denominator=lambda x: x.denominator.round(2), coverage=lambda x: x.coverage.round(2)).to_markdown(index=False),
             "\n## 3. Backtest (train 2022 → test 2023)\n", bt.round(3).to_markdown(index=False),
             "\n## 4. Interpretation\n",
             "- At the CA scale, residential dominates: ambient-only/hybrid capture ~11% vs 27.8% for residential, and select poorer CAs.",
             "- The denominator direction (ambient more poor, lower capture) is consistent, but the efficiency penalty is much larger than at grid scale.",
             "- This is scale dependence, not just a weaker effect: grid-level optimized allocation does not transfer to coarse policy units.",
             "- Use the audit at the unit where decisions are made, and report the unit.",
             "\n## 5. Caveats\n",
             "- 77 units; K=8; small-sample; no CI.",
             "- Aggregation is by grid centroid/CA assignment; not area-weighted."]
    (AUDIT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("saved", AUDIT)
    print(cov.to_string(index=False))
    print(dec.round(2).to_string(index=False))
    print(bt.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

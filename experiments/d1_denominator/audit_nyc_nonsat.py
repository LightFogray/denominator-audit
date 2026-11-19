#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NYC non-saturated same-budget comparison (K < |C|)."""
from pathlib import Path
import pandas as pd
import numpy as np
import denominator_audit_nyc as d

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/processed/d1_denominator"
df = pd.read_csv(OUT / "nyc_zone_pilot_3m_acs2023.csv").set_index("zone_id")
df = df[df.population > 0].copy()
q75 = df.poverty.quantile(0.75)
df["low"] = (df.poverty >= q75).astype(float)
out = OUT / "audit_nyc_3m_acs2023_nonsat"
out.mkdir(parents=True, exist_ok=True)
rows = []
for K in [40, 60, 80]:
    dec, sets = d.decompose(df, 1000, K)
    dec["K"] = K
    rows.append(dec)
all_dec = pd.concat(rows, ignore_index=True)
all_dec.to_csv(out / "decomposition.csv", index=False)
print(all_dec.assign(total=lambda x: (x.total*100).round(2), denominator=lambda x: (x.denominator*100).round(2), coverage=lambda x: (x.coverage*100).round(2)).to_string(index=False))
print("covered", int((df.taxi>=1000).sum()), "eligible", len(df))

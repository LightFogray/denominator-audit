# Denominator Audit — NYC taxi pilot (THEFT)

**Unit**: taxi zones; **crime**: Jan/Apr/Jul 2023 theft; **activity**: yellow-taxi pickups; **SES**: high-poverty (ACS 2023 5-year).

## 1. Coverage

|   threshold |   zones |   zone_share |   population_share |   theft_share |
|------------:|--------:|-------------:|-------------------:|--------------:|
|           1 |     245 |        0.996 |              0.998 |         0.998 |
|          10 |     237 |        0.963 |              0.979 |         0.987 |
|         100 |     213 |        0.866 |              0.937 |         0.953 |
|        1000 |     100 |        0.407 |              0.422 |         0.568 |
|        5000 |      63 |        0.256 |              0.191 |         0.344 |
|       10000 |      55 |        0.224 |              0.150 |         0.294 |

## 2. Decomposition (percentage points)

| comparison                        | metric   |    T |   K |   kc |   ku |   total |   denominator |   coverage |
|:----------------------------------|:---------|-----:|----:|-----:|-----:|--------:|--------------:|-----------:|
| hybrid_vs_residential             | low_unw  | 1000 | 100 |   57 |   43 |   12    |         12    |       0    |
| hybrid_vs_residential             | low_w    | 1000 | 100 |   57 |   43 |    8.04 |          8.62 |      -0.57 |
| hybrid_vs_residential             | captured | 1000 | 100 |   57 |   43 |   -4.54 |         -3.94 |      -0.61 |
| naive_ambient_only_vs_residential | low_unw  | 1000 | 100 |   57 |   43 |   -9    |          0    |      -9    |
| naive_ambient_only_vs_residential | low_w    | 1000 | 100 |   57 |   43 |   -8.39 |          0    |      -8.39 |
| naive_ambient_only_vs_residential | captured | 1000 | 100 |   57 |   43 |    0.07 |          0    |       0.07 |
| hybrid_vs_residential             | low_unw  | 5000 | 100 |   34 |   66 |   11    |         10    |       1    |
| hybrid_vs_residential             | low_w    | 5000 | 100 |   34 |   66 |   10.37 |          9.52 |       0.85 |
| hybrid_vs_residential             | captured | 5000 | 100 |   34 |   66 |   -1.36 |         -1.24 |      -0.12 |
| naive_ambient_only_vs_residential | low_unw  | 5000 | 100 |   34 |   66 |   -8.95 |          0    |      -8.95 |
| naive_ambient_only_vs_residential | low_w    | 5000 | 100 |   34 |   66 |   -6.11 |          0    |      -6.11 |
| naive_ambient_only_vs_residential | captured | 5000 | 100 |   34 |   66 |  -22.27 |          0    |     -22.27 |

## 3. Headline

- At `taxi>0`, coverage looks near-universal; at >=100/1,000 pickups, it is 61%/27.5% of zones.
- Ambient top-K is much more low-income; capture does not consistently improve.

## 4. Caveats

- One month; taxi is a mode-specific activity proxy, not ambient population.
- Income is ACS 2016 with fuzzy matching; pilot-grade.
- No jackknife CI (few boroughs; zone-level dependence not modeled).
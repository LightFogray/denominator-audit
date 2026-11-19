# Denominator Audit — NYC taxi pilot (THEFT)

**Unit**: taxi zones; **crime**: Jan 2023 theft; **activity**: yellow-taxi pickups; **income**: ACS 2016 NTA median (fuzzy matched; pilot-grade).

## 1. Coverage

|   threshold |   zones |   zone_share |   population_share |   theft_share |
|------------:|--------:|-------------:|-------------------:|--------------:|
|       1.000 | 243.000 |        0.988 |              0.994 |         0.996 |
|      10.000 | 227.000 |        0.923 |              0.964 |         0.977 |
|     100.000 | 155.000 |        0.630 |              0.715 |         0.798 |
|    1000.000 |  69.000 |        0.280 |              0.214 |         0.357 |
|    5000.000 |  50.000 |        0.203 |              0.136 |         0.274 |

## 2. Decomposition (percentage points)

| comparison                        | metric   |    T |   K |   kc |   ku |   total |   denominator |   coverage |
|:----------------------------------|:---------|-----:|----:|-----:|-----:|--------:|--------------:|-----------:|
| hybrid_vs_residential             | low_unw  | 1000 | 100 |   36 |   64 |    5    |          5    |       0    |
| hybrid_vs_residential             | low_w    | 1000 | 100 |   36 |   64 |    4.09 |          5.31 |      -1.22 |
| hybrid_vs_residential             | captured | 1000 | 100 |   36 |   64 |   -4.35 |         -4.71 |       0.36 |
| naive_ambient_only_vs_residential | low_unw  | 1000 | 100 |   36 |   64 |  -13.96 |          0    |     -13.96 |
| naive_ambient_only_vs_residential | low_w    | 1000 | 100 |   36 |   64 |  -13.23 |          0    |     -13.23 |
| naive_ambient_only_vs_residential | captured | 1000 | 100 |   36 |   64 |  -22.81 |          0    |     -22.81 |
| hybrid_vs_residential             | low_unw  |  100 | 150 |  120 |   30 |    4.67 |          5.33 |      -0.67 |
| hybrid_vs_residential             | low_w    |  100 | 150 |  120 |   30 |    4.42 |          3.06 |       1.36 |
| hybrid_vs_residential             | captured |  100 | 150 |  120 |   30 |   -8.65 |         -8.34 |      -0.31 |
| naive_ambient_only_vs_residential | low_unw  |  100 | 150 |  120 |   30 |   -1.33 |          0.67 |      -2    |
| naive_ambient_only_vs_residential | low_w    |  100 | 150 |  120 |   30 |   -0.41 |          0.71 |      -1.12 |
| naive_ambient_only_vs_residential | captured |  100 | 150 |  120 |   30 |   -0.36 |         -0.44 |       0.08 |

## 3. Headline

- At `taxi>0`, coverage looks near-universal; at >=100/1,000 pickups, it is 61%/27.5% of zones.
- Ambient top-K is much more low-income; capture does not consistently improve.

## 4. Caveats

- One month; taxi is a mode-specific activity proxy, not ambient population.
- Income is ACS 2016 with fuzzy matching; pilot-grade.
- No jackknife CI (few boroughs; zone-level dependence not modeled).
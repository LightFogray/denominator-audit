# Denominator Audit — Chicago BURGLARY

**K** = 119; **activity threshold T** = 25,000; **stabilization c** = 25,000; **jackknife n** = 77.

## 1. Coverage

|   threshold |   grids |   grid_share |   population_share |   crime_share |
|------------:|--------:|-------------:|-------------------:|--------------:|
|    1000.000 | 459.000 |        0.420 |              0.610 |         0.591 |
|    5000.000 | 275.000 |        0.251 |              0.432 |         0.400 |
|   10000.000 | 214.000 |        0.196 |              0.357 |         0.329 |
|   25000.000 | 152.000 |        0.139 |              0.275 |         0.257 |
|   50000.000 | 109.000 |        0.100 |              0.208 |         0.194 |
|  100000.000 |  64.000 |        0.059 |              0.138 |         0.121 |

## 2. Reliability (aggregate rate by activity bin)

| bin      |   grids |    crime |     activity |   rate_per_100k_trips |
|:---------|--------:|---------:|-------------:|----------------------:|
| <1k      |     635 | 6114.000 |   131251.000 |              4658.250 |
| 1k-5k    |     184 | 2855.000 |   428812.000 |               665.793 |
| 5k-10k   |      61 | 1061.000 |   433204.000 |               244.919 |
| 10k-25k  |      62 | 1065.000 |   999488.000 |               106.555 |
| 25k-50k  |      43 |  945.000 |  1670921.000 |                56.556 |
| 50k-100k |      45 | 1085.000 |  3246083.000 |                33.425 |
| >100k    |      64 | 1812.000 | 15485065.000 |                11.702 |

## 3. Decomposition (percentage points; jackknife 95% CI)

| comparison                        | metric   |   total |   denominator |   coverage |   den_lo |   den_hi |   cov_lo |   cov_hi |
|:----------------------------------|:---------|--------:|--------------:|-----------:|---------:|---------:|---------:|---------:|
| hybrid_vs_residential             | poverty  |   -5.94 |          0.18 |      -6.12 |    -2.25 |     2.58 |    -9.31 |    -3.05 |
| hybrid_vs_residential             | captured |    1.97 |         -0.39 |       2.36 |    -2.06 |     1.19 |    -0.26 |     5    |
| naive_ambient_only_vs_residential | poverty  |  -15.38 |          0.31 |     -15.69 |    -1.94 |     2.41 |   -19.6  |   -11.63 |
| naive_ambient_only_vs_residential | captured |    0.46 |         -0.25 |       0.71 |    -2.64 |     2.28 |    -7.42 |     8.6  |

## 4. Headline

- residential: capture 22.8%, poverty 27.5%
- hybrid: capture 24.8%, poverty 21.5%
- ambient-only (covered): capture 23.3%, poverty 12.1%

## 5. Recommendation

- Use ambient only where activity is above the reliability threshold; use residential outside.
- Report coverage, selection rate/K, denominator, and crime type.
- Do not interpret naive ambient-vs-residential differences as denominator effects without the decomposition.

## 6. Caveats

- Activity proxy is not a general ambient population.
- Recorded crime; reporting bias not adjusted.
- Decomposition is descriptive, not causal.
- Jackknife CI is cluster-robust by community area but does not capture data uncertainty.
# Denominator Audit — Chicago MOTOR VEHICLE THEFT

**K** = 119; **activity threshold T** = 25,000; **stabilization c** = 25,000; **jackknife n** = 77.

## 1. Coverage

|   threshold |   grids |   grid_share |   population_share |   crime_share |
|------------:|--------:|-------------:|-------------------:|--------------:|
|    1000.000 | 459.000 |        0.420 |              0.610 |         0.583 |
|    5000.000 | 275.000 |        0.251 |              0.432 |         0.366 |
|   10000.000 | 214.000 |        0.196 |              0.357 |         0.292 |
|   25000.000 | 152.000 |        0.139 |              0.275 |         0.223 |
|   50000.000 | 109.000 |        0.100 |              0.208 |         0.174 |
|  100000.000 |  64.000 |        0.059 |              0.138 |         0.106 |

## 2. Reliability (aggregate rate by activity bin)

| bin      |   grids |     crime |     activity |   rate_per_100k_trips |
|:---------|--------:|----------:|-------------:|----------------------:|
| <1k      |     635 | 20919.000 |   131251.000 |             15938.164 |
| 1k-5k    |     184 | 10896.000 |   428812.000 |              2540.974 |
| 5k-10k   |      61 |  3708.000 |   433204.000 |               855.948 |
| 10k-25k  |      62 |  3478.000 |   999488.000 |               347.978 |
| 25k-50k  |      43 |  2445.000 |  1670921.000 |               146.326 |
| 50k-100k |      45 |  3442.000 |  3246083.000 |               106.035 |
| >100k    |      64 |  5305.000 | 15485065.000 |                34.259 |

## 3. Decomposition (percentage points; jackknife 95% CI)

| comparison                        | metric   |   total |   denominator |   coverage |   den_lo |   den_hi |   cov_lo |   cov_hi |
|:----------------------------------|:---------|--------:|--------------:|-----------:|---------:|---------:|---------:|---------:|
| hybrid_vs_residential             | poverty  |   -4.54 |         -0.69 |      -3.85 |    -2.53 |     1.2  |    -7.05 |    -0.71 |
| hybrid_vs_residential             | captured |    1    |         -0.74 |       1.74 |    -3.04 |     1.49 |    -1.36 |     4.78 |
| naive_ambient_only_vs_residential | poverty  |  -15.4  |          0.53 |     -15.93 |    -2.57 |     3.45 |   -19.46 |   -12.28 |
| naive_ambient_only_vs_residential | captured |   -4.16 |         -0.2  |      -3.96 |    -1.56 |     1.25 |   -11.02 |     2.86 |

## 4. Headline

- residential: capture 24.1%, poverty 27.9%
- hybrid: capture 25.1%, poverty 23.4%
- ambient-only (covered): capture 19.9%, poverty 12.5%

## 5. Recommendation

- Use ambient only where activity is above the reliability threshold; use residential outside.
- Report coverage, selection rate/K, denominator, and crime type.
- Do not interpret naive ambient-vs-residential differences as denominator effects without the decomposition.

## 6. Caveats

- Activity proxy is not a general ambient population.
- Recorded crime; reporting bias not adjusted.
- Decomposition is descriptive, not causal.
- Jackknife CI is cluster-robust by community area but does not capture data uncertainty.
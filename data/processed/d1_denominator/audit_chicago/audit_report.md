# Denominator Audit — Chicago THEFT

**K** = 119; **activity threshold T** = 25,000; **stabilization c** = 25,000; **jackknife n** = 77.

## 1. Coverage

|   threshold |   grids |   grid_share |   population_share |   crime_share |
|------------:|--------:|-------------:|-------------------:|--------------:|
|        1000 |     459 |        0.420 |              0.610 |         0.712 |
|        5000 |     275 |        0.251 |              0.432 |         0.554 |
|       10000 |     214 |        0.196 |              0.357 |         0.494 |
|       25000 |     152 |        0.139 |              0.275 |         0.421 |
|       50000 |     109 |        0.100 |              0.208 |         0.356 |
|      100000 |      64 |        0.059 |              0.138 |         0.269 |

## 2. Reliability (aggregate rate by activity bin)

| bin      |   grids |   crime |   activity |   rate_per_100k_trips |
|:---------|--------:|--------:|-----------:|----------------------:|
| <1k      |     635 |   31484 |     131251 |               23987.6 |
| 1k-5k    |     184 |   17359 |     428812 |                4048.2 |
| 5k-10k   |      61 |    6520 |     433204 |                1505.1 |
| 10k-25k  |      62 |    7972 |     999488 |                 797.6 |
| 25k-50k  |      43 |    7157 |    1670921 |                 428.3 |
| 50k-100k |      45 |    9493 |    3246083 |                 292.4 |
| >100k    |      64 |   29470 |   15485065 |                 190.3 |

## 3. Decomposition (percentage points; leave-one-community-out min-max)

| comparison                        | metric   |   total |   denominator |   coverage |   den_lo |   den_hi |   cov_lo |   cov_hi |
|:----------------------------------|:---------|--------:|--------------:|-----------:|---------:|---------:|---------:|---------:|
| hybrid_vs_residential             | poverty  |    1.03 |          1.76 |      -0.74 |     0.65 |     1.78 |    -0.74 |    -0.29 |
| hybrid_vs_residential             | captured |   -2.6  |         -3.89 |       1.29 |    -4.02 |    -0.96 |     1.19 |     2.85 |
| naive_ambient_only_vs_residential | poverty  |   -4.2  |         -0.3  |      -3.9  |    -0.4  |    -0.14 |    -5.14 |    -3.52 |
| naive_ambient_only_vs_residential | captured |    5.43 |         -0.5  |       5.93 |    -0.53 |     0.16 |     5.16 |     6.67 |

## 4. Headline

- residential: capture 33.4%, poverty 16.3%
- hybrid: capture 30.8%, poverty 17.3%
- ambient-only (covered): capture 38.8%, poverty 12.1%

## 5. Recommendation

- Use ambient only where activity is above the reliability threshold; use residential outside.
- Report coverage, selection rate/K, denominator, and crime type.
- Do not interpret naive ambient-vs-residential differences as denominator effects without the decomposition.

## 6. Robustness (separate files)

- `reporting_bounds.csv`: decomposition under reporting-rate scenarios.
- `sensitivity.csv`: K × threshold sensitivity.
- `../audit_chicago_burglary/` and `../audit_chicago_vehicle/`: crime-type controls.
- `backtest_report.md` and `backtest_folds.csv`: out-of-time allocation test (year and half-year folds).
- K must not exceed the covered stratum for the ambient-only comparison; otherwise the capacity constraint dominates.

## 7. Caveats

- Activity proxy is not a general ambient population.
- Recorded crime; reporting bias not adjusted.
- Decomposition is descriptive, not causal.
- Deletion ranges describe single-community influence, not confidence intervals.
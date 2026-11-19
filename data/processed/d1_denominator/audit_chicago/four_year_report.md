# Four-year Chicago theft audit (2021–2024)

**Data**: Chicago crime 2021/2024 downloaded from Socrata; Divvy 2021/2024 monthly zips downloaded from S3; 2022/2023 crime/activity from the existing project data.

## Coverage (T=25,000, theft)

| Year | Covered grids | Theft |
|---|---:|---:|
| 2021 | 109 | 38,810 |
| 2022 | 110 | 52,968 |
| 2023 | 108 | 56,487 |
| 2024 | 110 | 59,653 |

## Decomposition (percentage points)

| Year | Denominator: poverty | Coverage: poverty | Denominator: capture | Coverage: capture |
|---|---:|---:|---:|---:|
| 2021 | +0.09 | −2.93 | −0.05 | +1.76 |
| 2022 | +0.44 | −1.07 | −0.17 | +1.59 |
| 2023 | +1.03 | −0.62 | −1.22 | +1.96 |
| 2024 | +0.26 | −0.28 | −0.79 | +0.58 |

Naive coverage effects remain large: poverty −8.31/−5.90/−4.82/−4.53pp; capture +1.70/+1.51/+3.61/−1.63pp. The denominator point estimates are smaller than in the 2-year (22M endpoint) activity build because year-specific activity yields ~109 covered grids (vs 152 for the pooled 2022–2023 build); direction is consistent but magnitude depends on the activity build.

## Out-of-time backtest (K=119)

| Train → test | residential | ambient-only | fixed hybrid | optimized |
|---|---:|---:|---:|---:|
| 2021 → 2022 | 29.7% / 19.4% | 35.4% / 11.1% | 32.2% / 16.5% | **37.8% / 13.0%** (kc=81) |
| 2022 → 2023 | 32.1% / 16.9% | 35.2% / 11.0% | 33.8% / 16.3% | **37.2% / 11.5%** (kc=97) |
| 2023 → 2024 | 33.3% / 16.0% | 36.7% / 11.2% | 34.4% / 16.4% | **39.7% / 12.2%** (kc=82) |

(Values: test-year capture / test-year poverty.) The optimized allocation beats residential in all three year transitions and lowers poverty; fixed hybrid is only marginally better.

## Interpretation

1. The **coverage/decomposition direction is stable across 2021–2024**: naive comparisons are coverage-dominated; controlled denominator effects are small but consistently pro-poor / lower-capture.
2. The **optimized allocation is robust out of time**: 2021→2022, 2022→2023, 2023→2024 all improve capture and reduce poverty vs residential.
3. The **fixed crime-share hybrid remains weak**; the policy rule should be "train kc on the prior year, choose on the frontier," not a hard-coded quota.
4. 2021 is a COVID-affected year; it still follows the same pattern.

## Caveats

- 2021/2024 activity is built from endpoint counts (start+end) in the monthly zips; 2022/2023 uses the existing year totals. Totals are comparable (~11M endpoints/year), but the build differs.
- 2021 crime is lower (COVID); 2024 higher.
- Theft only; recorded crime.
- K=119, T=25,000; sensitivity to T/K remains.

## Files

- `four_year_decomposition.csv`
- `four_year_backtest.csv`
- `chicago_crime_2021_2024.csv` (raw download)
- `crime_2021_2024_grid.csv`
- `divvy_activity_2021.csv`, `divvy_activity_2024.csv`

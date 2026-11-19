# Denominator Audit — Chicago (Route A prototype)

A pre-flight check for crime priority maps: **who is visible** in the activity data, **is the denominator stable**, and **how much of the ambient-vs-residential difference is coverage rather than denominator**.

## Files

| File | Content |
|---|---|
| `audit_report.md` / `audit_report.pdf` | one-page audit: coverage, reliability, decomposition, recommendation |
| `coverage.csv` | grids / population / crime covered at each activity threshold |
| `reliability.csv` | aggregate theft rate by activity bin |
| `decomposition.csv` | H/M/R total, denominator, coverage; community-area jackknife CI |
| `priority_maps.png` | residential / coverage-aware hybrid / ambient-only top-K |
| `frontier.png` | crime captured vs poverty in selected grids |
| `reporting_bounds.csv` | decomposition under reporting-rate scenarios |
| `sensitivity.csv` | K × threshold sensitivity |
| `backtest_report.md` | out-of-time validation, 2022→2023 / 2023→2022 |
| `backtest.csv` / `backtest_optimized.csv` | fixed vs optimized allocation, test-year capture/poverty |
| `backtest_folds.csv` | half-year temporal folds (2022H1→2022H2, 2022H2→2023H1, 2023H1→2023H2) |
| `four_year_report.md` | 2021–2024 four-year audit + backtest |
| `four_year_decomposition.csv` / `four_year_backtest.csv` | four-year decomposition and year-to-year backtest |
| `backtest_frontier.png` | out-of-time allocation frontier |
| `../audit_ca/` | MAUP check at 77 community areas; residential dominates at coarse scale |
| `../audit_chicago_robbery/` | robbery control; denominator effect near zero |
| `../audit_london_imd/` | London 1 km grid + LSOA IMD: ambient selects more deprived cells, capture not consistently higher |
| `../audit_nyc_3m_acs2023/` | NYC 3-month taxi + ACS 2023 5-year poverty: ambient +12pp high-poverty, capture −4.5pp |

## Run

```bash
python experiments/d1_denominator/denominator_audit.py --crime THEFT --k 119 --threshold 25000
python experiments/d1_denominator/audit_pdf.py
python experiments/d1_denominator/audit_reporting_bounds.py
python experiments/d1_denominator/audit_sensitivity.py
```

## Key numbers (THEFT, K=119, T=25,000)

- Coverage: 152/1,094 eligible grids (13.9%); 27.5% population; 42.1% theft.
- Naive ambient-only vs residential: poverty −4.2pp, capture +5.4pp.
- Decomposition: denominator −0.3pp poverty / −0.5pp capture; coverage −3.9pp / +5.9pp.
- Controlled hybrid: poverty +1.0pp total (denominator +1.8pp, coverage −0.7pp); capture −2.6pp (denominator −3.9pp, coverage +1.3pp).
- Jackknife 95% CI is wide; only the naive coverage effect on capture is clearly positive.

## Caveats

- Activity proxy (Divvy) is not a general ambient population.
- Recorded crime; reporting bias is bounded, not corrected.
- Decomposition is descriptive, not causal.
- K must not exceed the covered stratum for the "ambient-only" comparison; otherwise the capacity constraint dominates.

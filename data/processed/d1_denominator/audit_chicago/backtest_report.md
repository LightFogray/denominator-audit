# Out-of-time backtest — Chicago theft

**Question**: does the coverage-aware allocation actually improve prioritization out of time, or is it only an in-sample artifact?

**Design**: train on year *t* (theft + Divvy activity), select top-K grids, evaluate captured theft in year *t+1*. Strategies: residential, ambient-only, fixed-hybrid (crime-share kc), matched-coverage, oracle. K=45/119; T=25,000.

## Results (K=119)

| Train → test | Strategy | Capture | Poverty |
|---|---|---:|---:|
| 2022 → 2023 | residential | 32.1% | 16.9% |
| 2022 → 2023 | ambient-only (110 grids) | 35.2% | 11.0% |
| 2022 → 2023 | fixed hybrid (kc=43) | 33.8% | 16.3% |
| 2022 → 2023 | **optimized kc=97** | **37.2%** | **11.5%** |
| 2023 → 2022 | residential | 31.7% | 16.0% |
| 2023 → 2022 | ambient-only (108 grids) | 36.2% | 11.2% |
| 2023 → 2022 | fixed hybrid (kc=43) | 32.1% | 16.4% |
| 2023 → 2022 | **optimized kc=82** | **38.0%** | **12.2%** |

At K=45, the fixed hybrid is **worse** than residential (15.1%/16.7% vs 17.1%/12.6%), while optimized kc=45 (ambient-only) is 24.0%/12.1%.

## Temporal folds (half-year, K=119)

| Train → test | residential | ambient-only | fixed hybrid | optimized |
|---|---:|---:|---:|---:|
| 2022H1 → 2022H2 | 32.6% / 17.4% | 36.6% / 11.0% | 33.3% / 16.5% | **38.6% / 11.7%** (kc=94) |
| 2022H2 → 2023H1 | 32.9% / 16.7% | 34.3% / 11.0% | 33.8% / 15.8% | **36.5% / 13.2%** (kc=77) |
| 2023H1 → 2023H2 | 31.0% / 15.8% | 36.8% / 11.2% | 32.2% / 15.8% | **38.9% / 11.6%** (kc=96) |

(Values: test-year capture / test-year poverty.) The optimized allocation beats residential in all three folds and reduces poverty; fixed hybrid is only marginally better.

## Interpretation

1. **Fixed crime-share hybrid is not automatically better.** At K=45 it is dominated; at K=119 it is only marginally better than residential.
2. **Training-optimized allocation improves out-of-time capture and lowers poverty** relative to residential: +5.1pp capture / −5.4pp poverty (2022→2023), +6.3pp / −3.8pp (2023→2022).
3. The allocation frontier shows the policy tradeoff: residential is dominated; moving toward ambient-heavy allocation raises capture and lowers poverty in this sample, but it also reduces the share of peripheral grids.
4. **Policy rule**: use prior-year data to choose kc on the efficiency–equity frontier; do not hard-code a fixed quota. Report coverage, K, and kc.

## Caveats

- Two years only; one city; theft only.
- Optimized kc may overfit; the two year-pairs give kc=97/82 (70–90% of covered), so the result is "mostly ambient in the covered core, keep some residential outside."
- Poverty is population-weighted ACS 2022; activity is Divvy, not a general ambient population.
- Oracle (test-year top-K) captures 43%, so there is still room.

## Files

- `backtest.csv`: fixed strategies.
- `backtest_optimized.csv`: rules (max capture, equity-constrained, utility).
- `backtest_frontier_2022_2023.csv` / `backtest_frontier_2023_2022.csv`: kc frontier.
- `backtest_frontier.png`: out-of-time frontier.

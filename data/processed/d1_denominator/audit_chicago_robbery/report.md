# Denominator Audit — Chicago ROBBERY (control)

**Unit**: 1,246 grids; **crime**: robbery 2022–2023; **activity**: Divvy.

## 1. Decomposition (K=119, T=25,000)

| comparison                        | metric   |   total |   denominator |   coverage |
|:----------------------------------|:---------|--------:|--------------:|-----------:|
| hybrid_vs_residential             | poverty  |  -4.521 |         0.799 |     -5.32  |
| hybrid_vs_residential             | captured |  -0.181 |        -2.256 |      2.075 |
| naive_ambient_only_vs_residential | poverty  | -15.225 |        -0.309 |    -14.917 |
| naive_ambient_only_vs_residential | captured |  -7.035 |        -0.477 |     -6.558 |

## 2. Backtest (train 2022 → test 2023, K=119)

| strategy     |   kc |   pov_test |   cap_test |
|:-------------|-----:|-----------:|-----------:|
| residential  |    0 |     26.775 |     26.825 |
| ambient_only |  110 |     10.982 |     19.534 |
| fixed_hybrid |   25 |     22.108 |     28.245 |
| optimized    |   44 |     18.14  |     29.346 |

## 3. Interpretation

- Robbery is a violent, activity-dependent control. Compare its denominator/coverage terms with theft.
- If the denominator effect is weaker/absent, the theft-specific claim is supported; if present, the story should be "activity-dependent" rather than "theft-only".

## 4. Caveats

- 2022–2023 only; recorded crime.

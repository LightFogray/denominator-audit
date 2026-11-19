# Denominator Audit — Chicago community areas (MAUP check)

**Unit**: 77 community areas (grids aggregated). **Crime**: theft; **activity**: Divvy 2022.

## 1. Coverage (2022)

|   threshold |   cas |   ca_share |   pop_share |   theft_share |
|------------:|------:|-----------:|------------:|--------------:|
|        1000 |    70 |      0.909 |       0.955 |         0.974 |
|        5000 |    51 |      0.662 |       0.814 |         0.865 |
|       10000 |    41 |      0.532 |       0.713 |         0.757 |
|       25000 |    26 |      0.338 |       0.492 |         0.586 |
|       50000 |    21 |      0.273 |       0.402 |         0.526 |

## 2. Decomposition (K=8, T=25,000; test year 2023)

| comparison                        | metric   |   total |   denominator |   coverage |
|:----------------------------------|:---------|--------:|--------------:|-----------:|
| hybrid_vs_residential             | poverty  |    4.76 |          4.76 |       0    |
| hybrid_vs_residential             | captured |  -16.94 |        -16.94 |       0    |
| naive_ambient_only_vs_residential | poverty  |    5.26 |          4.89 |       0.37 |
| naive_ambient_only_vs_residential | captured |  -16.62 |        -21.15 |       4.54 |

## 3. Backtest (train 2022 → test 2023)

| strategy     |   kc |   pov_test |   cap_test |
|:-------------|-----:|-----------:|-----------:|
| residential  |    0 |     12.894 |     27.815 |
| ambient_only |    8 |     18.152 |     11.197 |
| fixed_hybrid |    5 |     17.657 |     10.879 |
| optimized    |    6 |     17.483 |     11.19  |

## 4. Interpretation

- At the CA scale, residential dominates: ambient-only/hybrid capture ~11% vs 27.8% for residential, and select poorer CAs.
- The denominator direction (ambient more poor, lower capture) is consistent, but the efficiency penalty is much larger than at grid scale.
- This is scale dependence, not just a weaker effect: grid-level optimized allocation does not transfer to coarse policy units.
- Use the audit at the unit where decisions are made, and report the unit.

## 5. Caveats

- 77 units; K=8; small-sample; no CI.
- Aggregation is by grid centroid/CA assignment; not area-weighted.
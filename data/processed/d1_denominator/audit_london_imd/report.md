# London IMD audit (1km grid, theft)

**Unit**: 1 km grid; **SES**: LSOA IMD score (higher = more deprived); **activity**: Santander Cycles 4 periods.

## 1. Coverage (theft, 4 months)

|    T |   cells |   pop_share |   theft_share |
|-----:|--------:|------------:|--------------:|
|    1 |     118 |       0.170 |         0.476 |
|   10 |     118 |       0.170 |         0.476 |
|  100 |     118 |       0.170 |         0.476 |
| 1000 |     116 |       0.168 |         0.475 |

## 2. Decomposition / strategy comparison

|    T |   K |   kc |   ku | strategy     |   deprived |   captured |
|-----:|----:|-----:|-----:|:-------------|-----------:|-----------:|
| 1000 |  12 |    6 |    6 | hybrid       |      0.485 |      0.16  |
| 1000 |  12 |    6 |    6 | matched      |      0.272 |      0.159 |
| 1000 |  12 |    6 |    6 | residential  |      0.204 |      0.183 |
| 1000 |  12 |    6 |    6 | ambient_only |      0.399 |      0.178 |
| 1000 |  20 |    9 |   11 | hybrid       |      0.265 |      0.177 |
| 1000 |  20 |    9 |   11 | matched      |      0.184 |      0.201 |
| 1000 |  20 |    9 |   11 | residential  |      0.299 |      0.207 |
| 1000 |  20 |    9 |   11 | ambient_only |      0.374 |      0.233 |

## 3. Interpretation

- K=12: hybrid deprived 48.5%, capture 16.0%; ambient-only 39.9%/17.8%; residential 20.4%/18.3%.
- K=20: ambient-only deprived 37.4%, capture 23.3%; residential 29.9%/20.7%; hybrid 26.5%/17.7%.
- London cycle coverage is 118/1,577 eligible cells (17% population, ~48% theft); central/peripheral structure remains.

## 4. Caveats

- IMD is LSOA-level assigned by grid centroid; 1km aggregation; 4 months; no backtest.

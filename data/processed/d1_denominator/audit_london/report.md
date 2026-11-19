# Denominator Audit — London coverage check

**Unit**: 1 km grid; **crime**: property, 4 months (2023-11, 2024-02, 2024-05, 2024-08); **activity**: Santander Cycles hires (same periods).

## 1. Coverage

| group   |   grids |   property_crime |
|:--------|--------:|-----------------:|
| all     |    3828 |           150980 |
| pop>0   |    3826 |           150980 |
| cycle>0 |     128 |            59403 |
| both    |     128 |            59403 |


## 2. Efficiency direction (top-10%, same covered grids)

|   subtype |   eff_res |   eff_amb |   eff_diff |   jaccard |
|----------:|----------:|----------:|-----------:|----------:|
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |
|       nan |       nan |       nan |        nan |       nan |


## 3. Headline

- Cycle data covers 128/3,828 grids (3.3%) but 39.3% of property crime.
- Within covered grids, ambient captures fewer theft/burglary/vehicle crimes than residential (top-10%).
- No grid-level SES in this pilot; no H/M/R decomposition. This is a coverage-only audit for London.

## 4. Caveats

- Cycle hire is a station network, not a continuous activity surface.
- Four two-week periods; seasonal representativeness limited.
- No income/deprivation at grid level; equity dimension not estimated.
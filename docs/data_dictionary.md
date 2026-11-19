# Data dictionary

All tables are CSV unless noted. Grid identifiers refer to the 1,246-cell Chicago grid used in the audit.

## Core Chicago inputs

| File | Rows | Columns | Meaning |
|---|---:|---|---|
| `data/processed/grid_socio.csv` | 1,246 | `grid_id, pop, poverty, bachelor, unemployment, income` | Grid population and 2022 ACS socioeconomic attributes |
| `data/processed/chicago_grid.geojson` | 1,246 | geometry + grid attributes | Chicago grid geometry (EPSG used by the scripts) |
| `data/processed/grid_context.csv` | 1,246 | `grid_id, community_area, community, restaurant, bar, school, hospital, police, nightclub, landuse_entropy, road_density, poi_total` | Grid-to-community-area lookup and place covariates used by the CA checks |
| `data/processed/d1_denominator/chicago_crime_2021_2024.csv` | 165,855 | `year, primary_type, latitude, longitude` | Geocoded theft incidents, 2021–2024 |
| `data/processed/d1_denominator/crime_2021_2024_grid.csv` | 1,246 | `grid_id` and yearly theft/burglary/vehicle/robbery counts | Grid-level crime counts |
| `data/processed/d1_denominator/theft_by_year.csv` | 1,246 | `grid_id, theft_2022, theft_2023` | Theft counts used in the pooled and annual checks |
| `data/processed/d1_denominator/theft_halfyear.csv` | 1,246 | `grid_id, 2022H1, 2022H2, 2023H1, 2023H2` | Half-year theft counts |
| `data/processed/d1_denominator/divvy_activity_2021.csv` | 1,246 | `grid_id, activity` | Divvy activity, 2021 |
| `data/processed/d1_denominator/divvy_activity_2024.csv` | 1,246 | `grid_id, activity` | Divvy activity, 2024 |
| `data/processed/od_corrected/divvy_2022_2023_grid_year_daypart.csv` | — | `grid_id, year, total` | Divvy activity for 2022–2023 |
| `data/processed/d1_denominator/divvy_halfyear_activity.csv` | 4,984 | `grid_id, fold, activity` | Activity measured only up to each half-year training cutoff |

## Multi-city inputs

| File | Rows | Columns | Meaning |
|---|---:|---|---|
| `data/processed/d1_denominator/nyc_acs2023_tract.csv` | 2,327 | `NAME, pop, poor, median_income, pop2, state, county, tract, GEOID` | 2023 ACS tract attributes for NYC |
| `data/processed/d1_denominator/london_grid_imd.csv` | 3,339 | `grid_id, population, activity, imd, theft, burglary, vehicle` | London 1-km grid population, cycle activity, IMD and crime counts |
| `data/raw/nyc_taxi_zones.zip` | — | shapefile | Public NYC taxi-zone boundaries |

## Audit outputs

| File | Meaning |
|---|---|
| `audit_chicago/four_year_quantile_backtest.csv` | Primary out-of-time allocation test by strategy and year |
| `audit_chicago/four_year_quantile_decomposition.csv` | H/M/R decomposition by year |
| `audit_chicago/backtest_folds_fixed.csv` | Leakage-free half-year folds |
| `audit_chicago/independent_T_c.csv` | Coverage-by-smoothing sensitivity |
| `audit_chicago/reporting_bounds.csv` | Reporting-rate scenarios |
| `audit_ca_matched/compare.csv` | Grid vs community-area matched-coverage comparison |
| `audit_nyc_3m_acs2023_nonsat/decomposition.csv` | NYC non-saturated budget comparison |
| `audit_london_imd/decomposition.csv` | London strategy comparison |

The table CSVs used in the manuscript are in `docs/ASAP_manuscript/tables/`. `poverty` and `capture` are percentages or percentage-point differences as indicated by each table's caption.

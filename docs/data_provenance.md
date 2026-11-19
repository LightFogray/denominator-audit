# Data provenance and preprocessing

The audit combines public crime, trip, population and boundary data. Raw files
are not redistributed; this note records the sources and the processing logic so
that the analysis can be reconstructed.

## Chicago

- **Crime**: City of Chicago, Crimes 2001–Present, Chicago Data Portal,
  <https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2>.
  The extract contains theft and comparison property-crime categories for
  2021–2024 with latitude/longitude. Records are assigned to the 1-km grid by
  point-in-polygon; non-geocoded records are excluded.
- **Population and socioeconomics**: 2022 American Community Survey (ACS)
  5-year tract estimates, allocated to grid cells by area-weighted overlay.
  `pop` is residential population; `poverty` is the tract poverty rate.
- **Activity**: Divvy bike-share trip data,
  <https://divvy-tripdata.s3.amazonaws.com/index.html>. Trip endpoints are
  assigned to grid cells. For 2022–2023, activity is built from the processed
  `divvy_2022_2023_grid_year_daypart.csv`; for 2021 and 2024 it comes from the
  yearly activity files. Half-year activity uses only trips before each
  training cutoff.

## New York City

- **Crime**: NYPD complaint data via NYC Open Data; larceny excluding motor
  vehicle theft is the theft outcome. The three-month extract covers January,
  April and July 2023.
- **Taxi activity**: NYC TLC yellow-taxi trip records,
  <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>. Pickups are
  aggregated to taxi zones.
- **Zones and population**: NYC taxi-zone boundaries (the small public
  `nyc_taxi_zones.zip` is included) and 2023 ACS 5-year tract estimates,
  area-weighted to zones. The residential score uses `y/(p+1)` to handle zero
  population.
- **Coverage**: a zone is covered at the 1,000-pickup threshold. The primary
  non-saturated comparison uses K=60; K=100 is reported only as a saturation
  check.

## London

- **Crime**: property-crime records for November 2023, February 2024, May 2024
  and August 2024, from the police.uk data portal,
  <https://data.police.uk/data/>. Theft, burglary and vehicle crime are
  aggregated to 1-km cells.
- **Activity**: Santander Cycles hire data from Transport for London,
  <https://cycling.data.tfl.gov.uk/>. Hires for the first two weeks of each
  month are mapped from station names to coordinates.
- **Population and deprivation**: WorldPop 2020 1-km population,
  <https://www.worldpop.org/>, and the English Index of Multiple Deprivation
  (IMD), <https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019>.
  LSOA IMD scores are assigned to grid cells by centroid.
- **Known limitation**: the WorldPop build undercounts London's population
  (4.84 million in eligible cells); London results are used for structural
  comparison, not city-level population claims.

## Coverage and audit definitions

- Chicago: eligible grids have population >= 100. The primary coverage rule is
  the top activity decile; the absolute 25,000-endpoint threshold is a
  sensitivity check. The smoothing constant is set to the coverage threshold
  (`c=T`) in the primary specification.
- NYC: positive population; threshold 1,000 pickups; `c=1,000`.
- London: positive population and an IMD assignment; threshold 1,000 hires;
  `c=1,000`.
- Selection: scores are ranked in descending order; ties are broken by
  ascending unit identifier. Historical-count rankings break count ties by
  residential rate. Coverage is fixed at the training period.

## Licence and attribution

The processed data are released under CC BY 4.0 to the extent permitted by the
providers' terms. Original data remain under the providers' terms. Users should
cite the manuscript and the relevant providers when reusing the data.

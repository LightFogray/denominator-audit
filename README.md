# Denominator audit for crime prioritization

Reproduction package for the manuscript:

> **Scale-aware denominator audit for crime prioritization: coverage, decomposition, and an out-of-time allocation test**

This repository contains the processed analysis data, audit code, and audit outputs. It is prepared for anonymous peer review: no title page, author names, affiliations, e-mail addresses, or ORCID identifiers are included.

**The manuscript PDF and LaTeX source are deliberately not stored here.** They are submitted separately. Keeping the manuscript out of this repository avoids a circular update chain in which every paper revision requires a repository update, which in turn requires a new anonymous-link snapshot.

## What is included

```text
data/processed/                     processed analysis data used by the audit
  d1_denominator/                   Chicago, NYC and London audit outputs
  grid_socio.csv                    Chicago grid population and poverty
  grid_context.csv                  grid-to-community lookup and place covariates
  chicago_grid.geojson              Chicago grid geometry
  od_corrected/                     processed Divvy grid-year activity
data/raw/nyc_taxi_zones.zip         small public NYC boundary file
experiments/d1_denominator/         audit code
docs/data_dictionary.md             variable definitions
docs/data_provenance.md             sources, licences and preprocessing notes
```

Raw crime, trip, population and boundary extracts are **not** redistributed. They are large (the raw working directory is about 14 GB) and remain subject to their providers' terms. `docs/data_provenance.md` records the sources and the variables used.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Re-run the main Chicago four-year audit
python experiments/d1_denominator/audit_4year_quantile.py

# Re-run the leakage-free half-year folds
python experiments/d1_denominator/audit_backtest_folds_fixed.py

# Re-run the matched-scale and NYC checks
python experiments/d1_denominator/audit_ca_matched.py
python experiments/d1_denominator/audit_nyc_nonsat.py
```

The scripts use paths relative to the repository root and write their outputs back into `data/processed/d1_denominator/`.

## Manuscript

The manuscript is not hosted in this repository. It is submitted through the journal system and points here for code and processed data. This separation keeps the review snapshot stable.

## Reproducibility notes

- The processed data are sufficient to re-run the audit tables and the main quantitative checks.
- Raw inputs are needed only to rebuild the processed data from source; they are documented in `docs/data_provenance.md`.
- Audit outputs, including the CSV tables and diagnostic figures used in the paper, are under `data/processed/d1_denominator/`.
- Figure and manuscript build scripts are intentionally not included; they belong with the manuscript package, not the public data repository.

## Data and code licences

- Code: MIT (`LICENSE`).
- Processed data: CC BY 4.0 (`DATA_LICENSE.md`), subject to the original providers' terms.
- Original data: retain their providers' licences; see `docs/data_provenance.md`.

## Anonymous review link

https://anonymous.4open.science/r/denominator-audit-057E/

## Anonymity

This repository is intended to be shared through an anonymous link during double-blind review. Please do not add author-identifying information, the title page, grant numbers, or acknowledgements to this repository before the review is complete.

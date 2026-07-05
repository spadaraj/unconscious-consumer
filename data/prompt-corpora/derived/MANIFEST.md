# Manifest — prompt corpora build

Reproducibility record. Populated stage-by-stage.

## Environment

- **Python:** 3.11.15 (Homebrew, `/usr/local/bin/python3.11`)
- **Venv:** `data/prompt-corpora/.venv`
- **Package versions:** _recorded after Stage 0 install_ (see `pip freeze` output committed alongside)

## Random seeds

- **Global seed:** `20260704` (set on every script)

## Stage 1 — Ingest

- **Corpus snapshot / commit hashes:** _pending_
- **Row counts written to `corpus.db`:**
  - `conversations`: _pending_
  - `turns`: _pending_
  - `queries`: _pending_
- **Months where the 100k-per-corpus stratum was undersized:** _pending_
- **ORCAS included?** _pending — depends on URL check_

## Stage 2 — Features

- **`features` rows:** _pending_
- **`conv_features` rows:** _pending_

## Stage 3 — Aggregates

- **Countries suppressed (under 500 conversations):** _pending_

## Stage 4 — Validation sample

- **Rows:** 500 (stratified)
- **Strata:** _pending_

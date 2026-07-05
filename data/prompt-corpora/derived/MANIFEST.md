# Manifest — prompt corpora build

Reproducibility record. Populated stage-by-stage.

## Environment

- **Python:** 3.11.15 (Homebrew, `/usr/local/bin/python3.11`)
- **Venv:** `data/prompt-corpora/.venv`
- **Package pins:** `data/prompt-corpora/requirements-lock.txt` (`pip freeze` at time of install)

## Random seeds

- **Global seed:** `20260704` (WildChat), `20260705` (LMSYS), `20260706` (MS MARCO), `20260707` (ORCAS). Set in `scripts/01_ingest.py`.

## Stage 1 — Ingest

Full run details in `derived/stage1_stats.json`.

### Corpus snapshots (HF commit shas at ingest time)

- **WildChat-1M:** `7d6490e462285cf85d91eabea0f9a954fbddcd1f` (last modified 2024-10-17)
- **LMSYS-Chat-1M:** `200748d9d3cddcc9d782887541057aca0b18c5da` (last modified 2024-07-27)
- **MS MARCO v2.1:** `a47ee7aae8d7d466ba15f9f0bfac3b3681087b3a` (last modified 2024-01-04)
- **ORCAS:** downloaded from `https://msmarco.z22.web.core.windows.net/msmarcoranking/orcas.tsv.gz` (the URL in the brief returned 409; this is the current URL from the official ORCAS landing page). File `Last-Modified: 2023-11-09`.

### Row counts written to `corpus.db`

| Table | Rows |
|---|---:|
| `conversations` | 199,397 |
| `turns` (user turns only) | 405,483 |
| `queries` | 400,000 |

By source:

| Source | Rows | Notes |
|---|---:|---|
| `conversations` — wildchat | 99,397 | Per-month reservoir target 8,000 × 13 months; some months undersized after English filter |
| `conversations` — lmsys | 100,000 | Uniform reservoir; **no per-row timestamps** — see caveat below |
| `queries` — msmarco | 200,000 | Reservoir from 808,731 streamed MS MARCO v2.1 rows |
| `queries` — orcas | 200,000 | Reservoir from 10,405,309 unique ORCAS queries |

### Undersized months / gaps

- WildChat English coverage runs `2023-04 … 2024-04` (13 months). All months hit ≥ 7,478 rows in the sample (all months were oversubscribed against the 8,000 target, so the reservoir replaced-in randomly rather than took-all).
- **LMSYS has no per-conversation timestamp field** in the streaming schema. Trend-line analyses for angles 1 (scaffolding) and 6 (politeness) must rest on WildChat only; LMSYS contributes only to point-in-time / cross-corpus comparisons.
- ORCAS query list has ~10.4M distinct queries (down from 18M raw click rows via dedup); reservoir of 200k gives parity with MS MARCO for the length-comparison chart.

### DB size

- `corpus.db`: 544 MB — over the brief's 200 MB threshold. Gitignored per the brief rule; Stage 3 CSVs will be committed instead.

## Stage 2 — Features

Full run details in `derived/stage2_stats.json`.

- **`features` rows:** 405,483 (one per user turn)
- **`conv_features` rows:** 199,397 (one per conversation)
- **Elapsed:** ~4 minutes

### Sanity spot checks

- Politeness marker rates (all conversations): please 10.99%, thanks 2.09%, apology 1.11%, hedge 1.15%. All in the single-digit to low-double-digit range the plan predicted.
- Top imperative verbs: write, give, make, create, name, tell, generate, explain, rewrite, describe, translate, list. Matches the plan's expectation that write/make/create/explain dominate.
- Question-vs-imperative split: 22% imperative, 28% question, 50% other (large "other" bucket is declarative statements, code pastes, and mid-conversation follow-ups).

## Stage 3 — Aggregates

Full run details in `derived/stage3_stats.json`.

### Outputs

Ten CSVs in `derived/`:
- `length_comparison.csv` (deciles: prompts vs MS MARCO vs ORCAS)
- `scaffolding_trend.csv` (monthly WildChat)
- `politeness_by_month.csv`
- `politeness_by_country.csv` (top 20 by volume, min 500 conv)
- `politeness_by_country_suppressed.csv` (137 countries below the 500 threshold — kept for transparency)
- `delegation_split_overall.csv` + `delegation_split.csv` (monthly)
- `purchase_prompts.csv` (monthly WildChat)
- `iteration.csv` (distribution of user turns/conv) + `iteration_summary.csv`

Seven PNG charts in `derived/charts/`.

`derived/topline.md` — the ten most striking numbers with caveats.

### Countries suppressed

137 countries fell below the 500-conversation threshold and are excluded from the country cut. Full list in `politeness_by_country_suppressed.csv`.

## Stage 4 — Validation sample

Full run details in `derived/stage4_stats.json`.

- **Total rows:** 500
- **Strata:** 250 stratified (25 rows × 10 feature-positive strata) + 250 uniform random. Every feature column populated for all 500 rows.
- **File:** `derived/validation_sample.csv` — **not committed** (contains raw user text; excluded via `.gitignore` per the brief's privacy rule). Regenerate deterministically with `.venv/bin/python scripts/04_validation_sample.py`.
- **Design purpose:** the feature-positive strata oversample the rare heuristics (is_purchase, is_reassurance) so precision is estimable at all. The uniform 250 gives recall-side coverage — the labeller can spot heuristic misses on turns the regex didn't fire on.

Adam / chat editor take it from here for the model-assisted labelling pass.

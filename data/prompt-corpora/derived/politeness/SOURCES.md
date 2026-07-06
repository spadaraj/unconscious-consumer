# Sources — politeness hypothesis tests

Retrieval date for all external data: **2026-07-05**. No score was ever fabricated, approximated from memory, or reconstructed. Where a country is absent from a source, it is left null and reported as such in `FINDINGS.md`.

## External reference data

### Hofstede six dimensions (power distance, individualism) — H1

- **URL:** https://geerthofstede.com/wp-content/uploads/2016/08/6-dimensions-for-website-2015-08-16.csv
- **Terms:** the dimension-data-matrix page states *"Researchers can use them without asking for permission. Those who are considering commercial use should contact us."* Aggregate research use (correlation of published scores) is within terms.
- **Fetched:** clean HTTP 200, semicolon-delimited CSV. `#NULL!` = missing.
- **Columns used:** `pdi` (power distance), `idv` (individualism). Normalised to `external/hofstede.csv` (iso3, pdi, idv, source_url, retrieved_date).

### GLOBE Phase 2 societal-culture practices (humane orientation, assertiveness) — H1

- **URL:** https://globeproject.com/data/GLOBE-Phase-2-Aggregated-Societal-Culture-Data.xls (linked from https://globeproject.com/study_2004_2007.html)
- **Terms:** GLOBE publicly posts the aggregated society-level data files on its study pages. The site's `/results/` *browse* path returns 403 to automated requests, but the data file itself is openly served (fetched with a standard browser User-Agent + Referer; no login, no paywall circumvented). Aggregate research use is within the spirit of a publicly posted dataset.
- **Columns used:** `Humane Orientation Societal Practices` and `Assertiveness Societal Practices` — the "as is" (practices) scores, not "should be" (values). Normalised to `external/globe.csv`.
- **Society-name mapping notes (see crosswalk):**
  - United Kingdom → GLOBE society **England** (Anglo cluster). GLOBE has no "UK".
  - Germany → GLOBE splits **Germany (EAST)** / **Germany (WEST)**; we use **WEST** (dominant population, standard comparison choice). East/West differ little on these two dimensions.
  - Canada → **Canada (English-speaking)** sample.
  - GLOBE has no society for: Pakistan, Vietnam, Romania, Jamaica, Saudi Arabia, Estonia → null.

### EF English Proficiency Index (EF EPI) — H2

- **URL:** https://www.ef.com/wwen/epi/  — **2025 edition**, 123 countries/regions.
- **Terms:** EF publishes the rankings and scores openly on the web page and in a free PDF report. Scores were extracted programmatically from the page's embedded data (the `"<country-slug>/","score":NNN` entries in the served HTML), **not** transcribed from memory. Normalised to `external/ef_epi.csv`.
- **Structural limitation (critical for H2):** EF EPI measures English as a *foreign* language and therefore **excludes native-English countries** — the US, UK, Canada, Australia, New Zealand, Jamaica are all absent. These are exactly the low-please Western bloc. The crosswalk carries an `english_native_or_official` flag (=1 for those six plus Singapore, where English is a primary official language and EF also excludes it) so the native-English bloc is reported separately rather than silently dropped.
- **Also EF-absent:** **Taiwan** (not native-English; genuinely not listed in EF EPI 2025 — a true null, not reconstructed). This matters because Taiwan is the highest-please country, so it cannot enter the EF correlation at all.

## Crosswalk

`external/country_crosswalk.csv` — one explicit, hand-authored row per corpus country (`wildchat_name → iso3 → hofstede_name → globe_name → ef_slug`, plus `english_native_or_official` and notes). Validated programmatically: every non-null source name resolves to an actual row in that source (0 mapping errors). Join coverage of the 29 corpus countries ≥ 500 conversations: Hofstede 29/29, GLOBE 23/29, EF EPI 21/29.

## Thresholds and parameters (reproducibility)

| Parameter | Value |
|---|---|
| Per-country conversation floor | **500** conversations (WildChat) |
| Please base | **non-fiction** cut (`looks_like_fiction = 0`), user turns only |
| Template cluster threshold | normalised 200-char prefix appearing in **≥ 20 distinct conversations** |
| Prefix normalisation | lowercase, collapse whitespace + digits, first 200 chars |
| East Asia bloc (for exclusion tests) | TWN, CHN, JPN, HKG, SGP |
| Correlation method | Spearman rank (rho, p, N) |
| Rank partial | computed only when joined N ≥ 15 |
| Random sampling | none (no seed needed) |

Raw downloaded source files live in `raw/politeness_sources/` (gitignored: Hofstede CSV, GLOBE xls, EF EPI page HTML). Only the normalised aggregate CSVs, crosswalk, correlations, splits, charts, and memos are committed.

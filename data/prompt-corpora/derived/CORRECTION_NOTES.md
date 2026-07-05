# Correction notes — user-turns-only re-extraction pass

_Audit trail for the corrective re-run of Stages 2–4 (and a small ingest-side filter) triggered by the editorial labelling result on the original `validation_sample.csv`._

---

## Stage 0 — Root cause

The brief hypothesised contamination source (A) — assistant-authored text leaking into user-role rows because the ingest pipeline concatenated turns or mislabelled roles. **That hypothesis is largely rejected by the evidence.** The real picture:

### What the ingest code does

`extract_user_turns` in `scripts/01_ingest.py` walks each conversation and yields one entry per turn where `role == 'user'`, with `text` set to that turn's `content` field only. The `write_conv` INSERT stores `role='user'` verbatim. There is no concatenation, no cross-turn bleed, and no role reassignment. The code is not the leak.

### What the 30-row diagnostic (has_apology + has_please) actually shows

- **6 out of 15 has_apology sample rows** are user-authored roleplay/fiction dialogue where characters apologise to each other (Doki Doki Literature Club fanfic pattern: `Monika:`, `Sayori:`, `MC:`; Minecraft roleplay: `[player]:`; various "write a scene where…" tasks).
- **1 out of 15 has_apology sample rows** — `wildchat:3c436fb715f74a8e9e6c661059bb494e` turn 4 — is a genuine assistant-authored row labelled `role='user'` from the WildChat corpus itself, marked with a `🤖` prefix. Confirmed by re-streaming that conversation from HF: WildChat stores it as 10 alternating turns, but every assistant reply is *also* recorded as a `user` turn prefixed with `🤖` (a UI/collection artifact where the model's reply was echoed for confirmation). My code faithfully preserves what the source says; the `🤖`-prefix filter drops exactly these ghost turns.
- The rest are user prompts that explicitly ask for assistant-like text (customer service reply templates, "act as an AI" DAN jailbreaks, translation of an English "please" into other languages, meta-instructions like "stop apologising"), or user prompts that happen to contain "please" (the majority).

### Scale of each source

| Contamination source | Approx count in `turns` (405,483 rows) |
|---|---:|
| (A) Genuine assistant text stored under `role='user'` (🤖 prefix + classic assistant openers "I apologize for", "As an AI language model", "Certainly!", "I'll do my best") | **~38 turns** (0.009%) |
| (B) User-authored fiction / roleplay / write-a-scene tasks — measured by the rough proxy `text LIKE '(%'` OR `%Monika%` OR `%NAME_1%` OR `%[player]%` OR `%roleplay%` OR `%: %:%` (multi-character dialogue) | **~65,000 turns fire on the proxy overall**; of politeness firings specifically: **76.5% of has_apology, 62.6% of has_please, 58.8% of has_thanks** match the fiction proxy |

**Conclusion:** contamination source (A) is a rounding error. Contamination source (B) — user-authored fiction/roleplay — is dominant, and it's not a user-turn-isolation problem because the text IS user-authored. It needs the fiction flag from Stage 2b, not re-extraction.

### What this means for the corrective pass

- **Stage 1b (re-extraction):** still worth doing, but narrowly. I add a tiny assistant-tell filter to `extract_user_turns` (drop turns starting with `🤖`, or with the ~5 canonical assistant openers) and apply it to the existing `turns` table via DELETE. This cleans up the 38 rows without re-streaming 2M rows.
- **Stage 2b (features + `looks_like_fiction` flag):** this is where the real fix lives. The fiction flag is what the editorial finding was actually surfacing.
- **Stage 3b (two-cut aggregates):** the "with fiction / without fiction" politeness cuts are the key deliverable — that's where the editorial side sees how much roleplay was moving each number.
- **Stage 4b (re-sample):** re-draw from clean turns with the fiction flag included.

The brief's "40-row verification gate" is easy to pass because assistant-text contamination was tiny to begin with. The harder editorial question — how much of the East Asia politeness cluster is real vs. driven by fiction/roleplay — gets answered by the fiction=0 cut in Stage 3b.

---

## Stage 1b — Assistant-tell filter + 40-row verification

- **Rows dropped from `turns`:** 31 of 405,483 (0.0076%) — assistant-tell matches only (leading `🤖`, or classic assistant openers). Matches Stage 0's ~38-row estimate.
- **`turns` row count after clean:** 405,452.
- **`conversations.n_turns` rebuilt** to match the cleaned turn counts.
- **40-row verification gate:** **PASS**. Zero rows in the random 40-sample contained the assistant tells the brief flags ("Apologies for", "please let me know", "Thank you for", "I'll do my best").


## Stage 2b — Fiction flag share

- **`looks_like_fiction` share overall:** 1.28% of user turns (5,195 / 405,452).
- **Per source:** WildChat 2.27% (4,808 / 211,623), LMSYS 0.20% (387 / 193,829). Matches the intuition that WildChat is naturalistic ChatGPT (more roleplay, DDLC fanfic, D&D scenes) while LMSYS is Arena benchmark queries.
- **Politeness fires very differently inside vs outside the fiction bucket:**

| Cut | n turns | please | thanks | apology |
|---|---:|---:|---:|---:|
| non-fiction | 400,257 | 10.76% | 1.56% | 0.71% |
| fiction | 5,195 | 28.60% | 43.12% | 31.78% |
| **fiction share of total firings** | | ~3% | ~26% | ~37% |

- **What that means for the East Asia finding:** politeness rates on `has_please` barely move when fiction is excluded (10.76% vs 10.99% originally), so the East Asia cluster is unlikely to be a fiction artefact. Stage 3b confirms this with the country-level cut.
- **Detector under-catches (noted, not fixed per brief's no-regex-rebuild rule):** prose fiction with no colon-dialogue and inline-quote dialogue (`"…" she said`) both slip past. The current signals require dialogue-line markers (`Name:` / `NAME_N:` / `[player]:`), stage directions in parens or asterisks, or explicit "roleplay" framing. A stricter detector is a later pass — this one is a floor, not a ceiling.
- **Missed assistant text (also noted, not fixed):** the ASSISTANT_TELL filter dropped 31 turns starting with `🤖` and the classic openers listed in `patterns.py`, but a small share of assistant-authored text with non-canonical openings ("I'm sorry if my previous responses did not meet your expectations. Please let me know…") slipped through. The new `validation_sample.csv` will surface these for the next editorial pass.

## Stage 3b — East Asia cluster change on clean cut

Every politeness and delegation aggregate ships in two cuts: all user turns, and non-fiction only. New CSVs alongside originals:
- `politeness_by_month_nonfiction.csv`
- `politeness_by_country_nonfiction.csv`
- `delegation_split_nonfiction.csv`
- `delegation_split_overall_nonfiction.csv`

### East Asia politeness cluster — the headline check

**The cluster holds on the non-fiction cut.** Country `please` rates barely move (fiction is only 1–2% of these countries' user turns):

| Country | `please` all turns | `please` non-fiction | Δ |
|---|---:|---:|---:|
| Taiwan | 74.4% | 74.4% | 0.0 |
| China | 54.3% | 54.4% | +0.1 |
| Japan | 53.9% | 53.9% | 0.0 |
| Hong Kong | 46.0% | 45.9% | −0.1 |
| Singapore | 41.2% | 41.2% | 0.0 |
| Germany | 11.5% | 11.5% | 0.0 |
| Australia | 10.4% | 10.2% | −0.2 |
| United States | 12.7% | 12.5% | −0.2 |

Relative ranking unchanged. The cross-cultural politeness pattern is a real user-behaviour signal in the WildChat data, not an artefact of fiction/roleplay contamination.

### What moved materially

- **`please` overall**: 10.99% → 10.76% (all vs non-fiction). Barely moves.
- **`thanks` overall**: 2.09% → drops on non-fiction cut (~26% of thanks firings were inside the fiction bucket, per Stage 2b).
- **`apology` overall**: 1.11% → drops harder on non-fiction cut (~37% of apology firings inside fiction).
- Non-monthly / non-country findings (length gap, role assignment, template structure, iteration mean, imperative verbs) are unchanged; they don't depend on the politeness cut.

## Stage 4b — Validation sample regenerated

- **Rows:** 500 (250 stratified across 10 feature-positive strata + 250 uniform random). Same design as the original pass.
- **Fiction flag:** `looks_like_fiction` column now included; 43 of the 500 rows (8.6%) are fiction-flagged. Higher than the 1.28% population base because the feature-positive strata (has_apology, has_thanks) pull disproportionately from fiction — which is precisely the coverage the labeller needs to validate the flag.
- **Contamination check:** zero rows in the sample start with `🤖` (Stage 1b filter is working end-to-end).
- **Not committed:** `validation_sample.csv` remains gitignored per the brief's privacy rule. Regenerate deterministically with `.venv/bin/python scripts/04_validation_sample.py`.
- Adam / chat editor take it from here for the model-assisted labelling pass on the clean sample.

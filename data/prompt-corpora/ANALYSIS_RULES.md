# Analysis rules — prompt-corpora mining

Standing rules for **every** analysis pass over these corpora. Written after a
per-country "please" finding (Taiwan 74%) turned out to be one copied Midjourney
prompt template — 73% of the "Taiwan" sample — not a cultural signal. These rules
exist to stop a laundered number from reaching an article again.

## The gate — run before any number becomes a claim

1. **Decontaminate first.** Before computing any rate or comparison, remove
   circulating templates and near-duplicates (prefix-cluster detector in
   `scripts/05_politeness_tests.py`). One copied prompt is ~4% of this corpus and
   >70% of some country cells; leaving it in manufactures effects.
2. **Recut and require survival.** Recompute the finding on the decontaminated
   (freehand) subset. If it moves materially, the raw number was an artifact —
   **kill it, don't caveat it.** (Length gap moved 17→16 words and survived;
   the please cluster moved 74→6% and did not.)
3. **Second adversarial cut.** Ask what else could produce this number besides the
   story you like — one template, one community, one bot, or geography that is
   really IP address, not nationality. A finding that survives only one cut is not
   robust, however good it looks.
4. **Confirm against Tier 1 before print.** The corpus generates hypotheses; it
   does not prove them. No corpus number becomes an article claim until an
   independent Tier 1 source supports it (CLAUDE.md Phase 2).

## What the data can support — claim-class hardness (robust → fragile)

- **Structural / linguistic** (length, keyword-vs-sentence, imperative grammar) —
  safe; survives sample skew.
- **Existence** ("this happens") — safe for *that it occurs*; never for *how often*.
- **Prevalence** ("X% do Y") — fragile; the denominator is a self-selected population.
- **Cross-group / geography / trend** — most fragile; selection bias differs by
  group. Do not publish these off a convenience corpus.

Rule of thumb: **a prevalence-by-group claim is guilty until proven innocent.**

## Dataset trust tiers

- **MS MARCO, ORCAS** — real Bing query logs. Representative of search. Usable for
  structure and, cautiously, for the prevalence of query *forms*.
- **WildChat, LMSYS** — convenience samples (a free-GPT-4 proxy; a model-testing
  arena). "Country" is hashed IP, not nationality. Use for structure and existence
  only. Never for population rates, geography, or demographic comparison.

## One line to remember

The corpus is a hypothesis generator, not an evidence source. **Comfort is a
warning sign** — the finding that flatters a prior is the one to cut hardest, not
the one to wave through.

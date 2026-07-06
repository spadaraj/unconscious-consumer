# Evidence pack — the translation tax (returns)

_Pre-draft evidence map, produced by the data workstream (Claude Code) for the
chat assistant to build the article from. This is not a draft. It is the Phase 2
"pre-draft evidence map" CLAUDE.md asks for: each candidate claim paired with the
number that supports it, the caveats, and what still needs a Tier 1 source._

**The gate is baked in.** Every number below is on the **freehand cut** —
non-fiction, circulating templates removed (prefix appearing in ≥ 20 conversations).
The raw-vs-freehand recut is shown so robustness is visible, not asserted.

---

## Candidate thesis (Phase 1 — for the chat assistant to sharpen)

> I am arguing that the move from search box to chat box is not a new tool but the
> **refund of a hidden tax** — for a generation we compressed our intentions into
> keywordese so a search engine could parse them, and people now simply *state* what
> they want; which means anyone designing a query interface should stop optimising
> for keyword input and design for stated intent, because users have stopped
> translating.

Passes the falsifiable-claim test (it predicts a measurable structural difference,
found below) and carries a concrete decision consequence (interface designers:
build for intent, not keywords). "Only Adam can write this": the history of learned
keywordese as a UX behaviour, and the design consequence, is his professional
ground — this is not a Wikipedia-summary piece.

---

## The evidence (freehand cut; both corpora, n = 356,930 prompts)

Prompts to a conversational agent vs real search queries, as text forms:

| Structural measure | Prompts (freehand) | MS MARCO | ORCAS |
|---|---:|---:|---:|
| Median length (words) | **16** | 6 | 3 |
| Ends in sentence punctuation (. ? !) | **41.7%** | 6.9% | 0.3% |
| Contains first person (I / my / me) | **31.8%** | 3.2% | 2.3% |
| Contains second person (you / your) | **26.6%** | 4.7% | 0.8% |
| Question-formed | 37.3% | 73.3%* | 9.6% |
| Function-word ratio (grammar density) | **0.383** | 0.332 | **0.101** |

Chart artefacts for the **Data** image slot: `charts/length_distribution.png`,
`charts/structural_fingerprint.png`.

### The three claims the data can carry (structural class — safe per ANALYSIS_RULES)

1. **People write to a chatbot in sentences, to a search engine in fragments.**
   Median prompt is 16 words; a general search query (ORCAS) is 3. Prompts end in
   sentence punctuation 41.7% of the time; ORCAS queries, 0.3%. That is a ~130×
   gap on the most basic marker of "is this a sentence."
2. **People address the machine as an interlocutor.** Second-person ("can *you*",
   "*you* are") appears in 26.6% of prompts vs 0.8% of ORCAS queries — roughly 30×.
   First-person is ~14× (31.8% vs 2.3%). Nobody says "I" or "you" to a search box;
   they say it constantly to a chat box.
3. **Prompts carry grammar; queries strip it out.** Function-word density — the
   share of words that are articles, pronouns, prepositions, auxiliaries — is 0.10
   for ORCAS queries (a near-pure keyword bag) vs 0.38 for prompts (ordinary
   natural-language grammar). Keywordese is visible in the search data as the
   *absence* of grammar; prompts put the grammar back.

\* **MS MARCO caveat — do not lean on it.** MS MARCO's 73% question rate is an
artefact: it is a curated *question-answering* benchmark, so its queries are
questions by construction. It is **not** a general sample of search behaviour. Use
**ORCAS** (18M real Bing click queries) as the honest keywordese baseline; cite
MS MARCO only as "even Bing's question-queries are shorter and barer than prompts,"
never as the primary contrast.

---

## The recut (gate step 2 — proof the finding is not a template artifact)

Templates were ~13% of non-fiction prompt turns. Removing them barely moves any
measure, and *strengthens* the sentence-shape signal (templates were keyword-ish
scaffolds, so stripping them raises punctuation and question rates):

| Measure | Raw (non-fiction) | Freehand | Δ |
|---|---:|---:|---:|
| Median words | 17 | 16 | −1 |
| Terminal punctuation | 38.8% | 41.7% | +2.9 |
| First person | 33.9% | 31.8% | −2.1 |
| Second person | 31.0% | 26.6% | −4.4 |
| Question form | 34.8% | 37.3% | +2.5 |
| Function-word ratio | 0.376 | 0.383 | +0.007 |

Contrast with the politeness finding, which moved 74% → 6% on the same recut. This
one survives. It is a structural fact about the language, not a paste-count.

---

## What still needs a Tier 1 source (Phase 2 — before any of this is a claim)

The **numbers above establish the present-day structural gap.** The *narrative*
(that people once learned to strip their intent for search, and have now stopped)
needs external evidence — the corpus cannot prove a historical behaviour it never
observed. Specifically:

- **The "keywordese was learned" premise.** Needs HCI/IR literature on web-query
  formulation and length (the long-standing finding that web queries average ~2–3
  terms, and that users deliberately shorten and de-grammaticise for search). Assign
  a Tier 1 source; do not assert the history from these data.
- **The "tax" and "refund" framing** is interpretation, not measurement. It is the
  article's argument, to be earned in prose and defended in the adversarial pass —
  not a data finding. Label it as such.
- **The design consequence** (build for intent, not keywords) is Adam's Tier-4 UX
  observation territory; per CLAUDE.md it may appear once and must extend, not
  replace, the Tier 1 point.

## Counter-evidence to address (CLAUDE.md Phase 2 requires this before drafting)

- **Affordance, not refund.** Prompts may be long and grammatical because the chat
  UI *invites* prose (a big text box, a conversational partner), not because users
  have "stopped translating." The article must engage this — the data cannot
  distinguish "users changed" from "the interface changed what users do."
- **Novelty / politeness decay.** Verbose, polite prompting could be an early-adopter
  or novelty behaviour that regresses toward keywordese as chat becomes routine.
  These are 2023–2024 snapshots; no claim about the trajectory is supported.
- **Sample skew.** WildChat/LMSYS are convenience samples (ANALYSIS_RULES tiers).
  The *structural* claim is robust to this (a skewed sample of prompts is still made
  of prompts), but any "how common" framing is not. Keep the piece structural.

## What this data does NOT support (guardrails)

- No prevalence-by-group, geography, demographic, or trend claims.
- No "X% of people" population statement — n is a corpus, not a public.
- The claim is strictly: *as text forms, prompts and queries differ structurally in
  these specific, large, decontamination-robust ways.*

---

_Handoff: this pack is the input to the chat assistant's Phase 1 angle-sharpening
and Phase 2 evidence mapping. Drafting is editorial (chat assistant) per the
division of labour; the data workstream stops here._

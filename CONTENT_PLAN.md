# Content Plan

A living strategy doc for new writing on **The Unconscious Consumer** (site + Substack).
Drafting happens in a Claude Project; this file plans *what* to write and tracks the health
of the existing catalogue. For *how* to publish a finished piece, see `PUBLISHING.md`.

*Snapshot generated from `articles.json` on 2026-06-11. Regenerate when it drifts.*

## Model: Substack-first

New essays publish on **Substack first**; the site links out via `hosting: "substack"`
entries (no `bodyHtml`). The site is the portfolio/landing layer. Three active categories:
`consumer-psychology`, `behavioural-economics`, `user-experience`.
**Undercurrents is retired** — no new pieces; existing 10 stay live but are no longer
promoted in the nav (see `PUBLISHING.md`).

## Audit snapshot

| Signal | Finding | Implication |
|---|---|---|
| Cadence | 2023: 43 · 2024: 1 · 2025: 0 · 2026: 2 | Restart a steady cadence |
| Category balance (active) | user-experience 19 · consumer-psychology 17 · **behavioural-economics 11** | Feed behavioural-economics first |
| Substack coverage | 6 of 57 are `hosting: substack` | New Substack-first pieces grow this |
| Internal linking | All 50 full-content articles have `related`, but **22 are never linked *to*** (orphans) | Thread orphans into new pieces as `related` targets |
| Covers | 14 articles have no `coverImage` (procedural SVG fallback) | Optional art-sourcing backlog |

## Backlog (prioritized)

Method, highest leverage first. Each idea names a target category and 1–2 `related` slugs
to thread (prefer orphans). These are starting points — drafting/refining happens in the
Claude Project.

### 1. Feed behavioural-economics (thinnest active category, 0 on Substack)
- **Extend the *From Page to Practice* franchise** — existing entries:
  `thinking-fast-and-slow-consumer-behaviour`, `predictably-irrational-in-an-unpredictable-economy`,
  `nudge-theory-for-climate-action`, `wearing-our-genes-on-our-sleeves-spent`.
  Next books: *Scarcity* (Mullainathan & Shafir), *Influence* (Cialdini), *Misbehaving* (Thaler).
- **Present bias / hyperbolic discounting** applied to subscription & BNPL spending →
  thread `paradox-of-choice-streaming-wars` (orphan).
- **Default effects in 2026** (pensions, AI opt-outs) → thread `anchoring-effect-housing-market` (orphan).

### 2. Extend the *Digital Nudge Series* (user-experience)
Existing: `digital-nudge-paradox-of-choice`, `digital-nudge-desirable-difficulty`,
`digital-nudge-returning-customers`. New entries: friction-as-feature, progress indicators,
social proof in UI → thread `slacking-off-or-on` / `grammarly-writing-habits` (orphans).

### 3. Fresh 2026-vantage angles in consumer-psychology / user-experience
- AI shopping assistants and the erosion of deliberate choice → thread
  `rise-of-the-skeptical-shopper`, `endowment-effect`.
- Re-examine a stale 2023 take with a 2026 lens (the catalogue's AI pieces are dated).

### Threading backlog — 22 orphan articles (never linked *to*)
These articles render fine on their own, but nothing links *to* them, so readers rarely
discover them. The lever: when writing or editing a piece, add an orphan slug to the
*linking* article's `related` array. (Related cards only render on articles that have
`bodyHtml` — all 50 of those already have `related` set, so the work is adding orphans as
*targets*, not filling empty arrays. `hosting: substack` and stub articles never render
related cards, so don't bother threading *from* them.)

- **behavioural-economics:** `peak-end-rule`, `paradox-of-choice-streaming-wars`,
  `behavioural-economics-distracted-driving`, `vegan-food-market-consumer-decisions`,
  `anchoring-effect-housing-market`, `voice-pitch-bias-elections`
- **consumer-psychology:** `endowment-effect`, `mistaken-celebrity`, `post-hoc-rationalization`,
  `hidden-influences-scents-retail`, `influencer-tipping-point`,
  `februarys-over-the-gym-is-empty-again`*
- **user-experience:** `typography-ux-design`, `slacking-off-or-on`, `grammarly-writing-habits`,
  `revolution-not-streamed`, `why-product-teams-misunderstand-their-customers`*
- **undercurrents (retired — link only if useful):** `ai-web-accessibility`,
  `quiet-return-of-analog`*, `tesla-range-controversy-brand-trust`*,
  `chatgpt-hypergrowth-consumer-expectations`*, `ai-personalization-uncanny-valley`*

*\* = also `hosting: substack` (its own related cards never render).*

### Art-sourcing backlog — 14 articles with no `coverImage`
These fall back to a procedural SVG cover. Add a `coverImage` when art is available:
`chatgpt-hypergrowth-consumer-expectations`, `tesla-range-controversy-brand-trust`,
`ai-personalization-uncanny-valley`, `quiet-return-of-analog`,
`why-product-teams-misunderstand-their-customers`, `februarys-over-the-gym-is-empty-again`,
`tesla-range-controversy`, `brand-trust-ai-experiences`, `ai-web-accessibility`,
`chatgpt-threads-hypergrowth`, `twitter-tightrope-walk`, `riding-the-ai-wave`,
`endowment-effect`, `paradox-of-choice-streaming-wars`.

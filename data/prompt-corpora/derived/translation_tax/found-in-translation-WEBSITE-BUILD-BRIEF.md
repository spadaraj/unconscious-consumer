# Claude Code brief — website build: "Found in translation"

**Handoff from Chat.** Editorial is complete. This brief covers the mechanical website channel only: `articles.json` entry, `bodyHtml` generation, internal-link resolution, and the interactive-widget embed. Substack is handled separately by Chat and is not your concern.

**Source of truth:** `found-in-translation-FINAL.md` (the article body above the `## HANDOFF METADATA` divider). Everything below the divider is instructions for you.

---

## 1. articles.json entry

Use the block in the handoff metadata. Fill the three fields Chat does not own:
- `id` — read `articles.json`, use `max(id) + 1`. Do not guess.
- `date` — publish date, `YYYY-MM-DD`.
- `related` — `repriced-overnight` is confirmed (this is its measurement sequel); propose two more thematic neighbours from `articles.json` and have Adam confirm.

**Website `subtitle`:** use the discovery-reader variant — "What 357,000 prompts reveal about the language we only ever spoke for the machine." Not the Substack line.

## 2. bodyHtml

Convert the `.md` body (hook through "The last word", ending before the handoff divider) to HTML per the standard pipeline. Internal links are already resolved to the `article.html?slug=` pattern — verify, don't re-resolve.

## 3. Interactive widgets — the part that needs care

Two interactives exist: `grammar-lights-up.html` (the grammar highlight) and the barcode/dots showcase (`showcase.html`, or its components). **Do not paste their `<script>` blocks into `bodyHtml`.** Markup injected into a page via `innerHTML` does not execute embedded JavaScript, so an inlined widget will render as dead HTML.

**Before building, verify how `article.html` injects the body.** Check whether it uses `innerHTML`, `insertAdjacentHTML`, a framework render, or something else. Then pick the embed mechanism accordingly:

- **Preferred:** host each interactive as its own file in the repo (e.g. `/interactives/found-in-translation/grammar.html`, `/interactives/found-in-translation/barcode.html`) and embed via `<iframe>` in `bodyHtml` at the two marked positions. Iframes execute their own scripts and isolate styling.
- Confirm the iframe approach works with how the site serves static files, and set a sensible default height with the widget being internally responsive (both widgets already have mobile breakpoints).

**Embed positions in the body:**
- Grammar / barcode widget → after the structural-fingerprint section (the paragraph ending "...simply ordinary written English"), before "A note on rigour."
- Lights/dots widget → inside "The person was always there," before "Read against that background."

If the two showcase visuals are bundled in one `showcase.html`, either embed it once at the fingerprint section or split it; Adam to confirm which visuals go where. Match the placements Chat used in the Substack static frames for consistency across channels.

## 4. Data integrity note (already checked by Chat, stated for your build)

The widgets' embedded numbers were verified against the published figures: dot panels show measured "I"/"you" rates within sampling noise of 31.8% / 26.6% (prompts) and 2.3% / 0.8% (queries); the barcode per-message function-word shares match 38% / 10%. Do not regenerate or resample the widget data during the build — ship the verified files as-is.

## 5. Pre-publish checklist (CLAUDE.md)

- [ ] `id` / `date` / `related` filled; `related` slugs exist
- [ ] All citation URLs open and support their claims — the Jansen/Spink 2000 ScienceDirect DOI was verified live by Chat; re-confirm the rest at publish
- [ ] Body matches across channels except the deliberate Substack additions (hero + 2 data images, subscribe button, forward-looking close, further-reading footer, Substack subtitle/links)
- [ ] `readTime` = 11 min, identical both channels
- [ ] Interactive widgets execute in the live page (not dead HTML) — test in browser before publish
- [ ] Adversarial pass + counter-evidence: complete (task-mix, affordance, novelty all addressed in-body)

## Definition of done

- [ ] `articles.json` entry added with real id/date/related
- [ ] `bodyHtml` generated, internal links verified
- [ ] Both interactives embedded and confirmed executing in the live article
- [ ] Committed and pushed

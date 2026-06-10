# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**The Unconscious Consumer** — a static website and content portfolio for Dr. Adam
Spadaro's UX-research / behavioural-economics writing. It is the home base for Substack
readers and a portfolio of thought-leadership articles.

**Hard constraints (from `TUC_DESIGN_BRIEF.md` — "What never changes"):**
- Plain HTML, CSS, and vanilla JS only — **no frameworks, no npm, no build step, no compilation**
- Must stay readable and editable by a non-developer
- Deployed to Vercel via GitHub (push to deploy)

There is no package.json, test suite, or linter. "Building" means editing files directly.

## Running locally

Pages use `fetch('articles.json')`, so opening `index.html` via `file://` will fail (CORS) —
you must serve over HTTP. The configured dev server (`.claude/launch.json`) runs:

```bash
python3 -m http.server 8787   # then open http://localhost:8787
```

Any static file server works. There is nothing to compile or watch.

## Architecture

Three HTML entry points share `styles.css`, and JS reads from a single JSON data file.

- **`index.html`** — homepage. Loads `covers.js` then `app.js`. Sections: hero (featured
  article), featured, subscribe, articles grid, about, reading list.
- **`article.html`** — the template for *every* article. It reads `?slug=` from the URL,
  fetches `articles.json`, finds the matching article, and renders it. All rendering logic
  lives inline in a `<script>` in this file (no separate JS file).
- **`cv.html`** — standalone CV page (served at `/cv` via a `vercel.json` rewrite).

**`articles.json` is the single source of truth** for all article content and metadata
(57 articles). Each entry has: `slug`, `title`, `excerpt`, `category`, `date`, `readTime`,
`coverImage`/`coverObject`, `related`, `featured`, and crucially `hosting` + `bodyHtml` +
`substackUrl`. To add/edit an article, edit this JSON file — nothing else.

**Article hosting model** — every article is one of two kinds:
- `hosting: "local"` — has `bodyHtml`; rendered in-page by `article.html`.
- `hosting: "substack"` — `bodyHtml` is null; `article.html` redirects to its `substackUrl`.
  On cards, a `substackUrl` makes the "Read →" link open Substack in a new tab.

**`app.js`** drives the homepage: category filtering, real-time search, infinite scroll
(IntersectionObserver, `BATCH_SIZE = 6`), dark mode (persisted in `localStorage`, respects
`prefers-color-scheme`), the two-layer nav, and the animated featured hero. State is held in
module-level variables (`currentFilter`, `searchQuery`, `displayedCount`).

**`covers.js`** generates procedural SVG cover art via `generateCover(category, animated,
seed, coverObject)`, one visual style per category. Used as a fallback only when an article
has no `coverImage`. Consumer-psychology covers composite a PNG from `images/Covers/`
(`coverObject` names the stem, e.g. `cart` → `cp-cart.png`; valid values in `CP_KNOWN_OBJECTS`).

**`vercel.json`** preserves SEO from the previous Squarespace site: it maps dozens of old
URLs (e.g. `/user-experience/behind-dark-patterns...`) to `/article.html?slug=...` as
permanent redirects, and maps old category paths to `/?filter=<category>`. When you rename a
slug or move an article, update the matching redirect here.

## Key conventions

- **The four categories are a fixed enum:** `consumer-psychology`, `behavioural-economics`,
  `user-experience`, `undercurrents`. They appear as the keys/keyspace in `app.js`
  (`HERO_LABELS`, `getCategoryTag`), `article.html` (`CAT_LABELS`, `CAT_CLASSES`), `covers.js`,
  CSS tag classes (`tag-cp`/`tag-be`/`tag-ux`/`tag-uc`), and `vercel.json`. Adding a category
  means touching all of these.
- **`?filter=<category>` URL param** deep-links the homepage to a filtered view; the discovery
  pills and article-page category links rely on it.
- **Article titles may contain emoji in the data, but they are stripped at render time**
  (`stripEmoji` in `article.html`) — the design brief forbids emoji in titles. Body images
  from scraped content are also stripped (`stripImages`) except `class="book-cover"`/`"data-viz"`.
- **Design system** (colors, typography, nav behaviour, layout rules) is specified in
  `TUC_DESIGN_BRIEF.md` — consult it before any visual change. Single accent color is
  terracotta `#C4531A`; never use orange (it was the old Substack brand color).
- **Third-party embeds:** Plausible (analytics) and HubSpot (forms) are loaded via script tags
  in the HTML; there is no backend.

## Legacy / one-off files (do not treat as live code)

- **`articles-data.js`** (`const ARTICLES_DATA = [...]`) is the *old* data format. It is **not
  loaded at runtime** — `articles.json` superseded it. Kept for reference only.
- **`build-articles-json.py`** was a one-time migration that generated `articles.json` from
  `articles-data.js` plus scraped content. It is not part of any workflow; edit `articles.json`
  directly instead of rerunning it.

## Git workflow

Develop on the branch assigned for the session, commit with descriptive messages, and push
with `git push -u origin <branch>`. Pushing to the connected GitHub repo triggers a Vercel
deploy — do not create pull requests unless explicitly asked.

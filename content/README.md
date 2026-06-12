# Content archive

Working copies of articles, organized by stage. The site is **Substack-first**, so the
*live* copy of every published piece lives on Substack — these files are the editorial
archive: drafts while writing, and a saved copy of the final text after it goes live.

## Folders

- **`drafts/`** — work in progress, before publishing. One markdown file per article, named
  by its eventual slug (e.g. `repriced-overnight-ai-benchmark.md`).
- **`published/`** — the final version after it's live on Substack and carded on the site.

## Workflow (pairs with `../PUBLISHING.md`)

1. New draft lands in **`drafts/<slug>.md`**.
2. Publish the piece on Substack; add the `hosting: "substack"` entry to `../articles.json`.
3. **Move** the file from `drafts/` to **`published/<slug>.md`** and add the Substack URL +
   publish date to the top, so the archive mirrors what's live.

These markdown files are not part of the website itself — they're excluded from the Vercel
deploy via `../.vercelignore`, so unpublished drafts never become public URLs.

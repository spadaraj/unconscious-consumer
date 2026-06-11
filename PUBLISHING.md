# Publishing a new article (Substack-first)

How to put a new piece on the site once it's written. The site is **Substack-first**: the
essay lives on Substack, and the site shows a card that links out to it. You only edit one
file — `articles.json`. No build step, no tooling.

For *what* to write next, see `CONTENT_PLAN.md`.

## Steps

1. **Publish the essay on Substack.** (Draft it in the Claude Project, then publish on
   Substack and copy the post URL — it looks like
   `https://theunconsciousconsumer.substack.com/p/your-post`.)

2. **Add one entry to `articles.json`** (append to the array). Copy this template:

   ```json
   {
     "id": 67,
     "slug": "kebab-case-unique-slug",
     "title": "Your Title (emoji allowed — they're stripped when rendered)",
     "excerpt": "One or two sentences. Shows on the card and in search/social previews.",
     "category": "consumer-psychology | behavioural-economics | user-experience",
     "date": "Jun 11, 2026",
     "readTime": "7 min read",
     "hosting": "substack",
     "substackUrl": "https://theunconsciousconsumer.substack.com/p/your-post",
     "bodyHtml": null,
     "related": ["slug-a", "slug-b"],
     "coverImage": "images/Article Images/Your Image.png",
     "coverObject": null,
     "featured": false
   }
   ```

3. **Fill in the fields:**
   - `id` — next integer (one higher than the current max).
   - `slug` — unique, lowercase, hyphenated. Becomes `/article.html?slug=...`.
   - `category` — one of the **three active** categories. Do **not** use `undercurrents`
     (retired). Pick `consumer-psychology`, `behavioural-economics`, or `user-experience`.
   - `hosting` — `"substack"`, with `bodyHtml: null` and `substackUrl` set. (A card's
     "Read →" then opens Substack in a new tab, and the article page redirects to it.)
   - `related` — 1–2 existing slugs to thread. Prefer "orphan" articles from
     `CONTENT_PLAN.md` so they get more internal links.
   - `coverImage` — optional. Put the file under `images/` and reference its path. Omit it
     to use the auto-generated procedural cover.
   - `coverObject` — leave `null` unless the category is `consumer-psychology`, where it can
     name a PNG stem from `CP_KNOWN_OBJECTS` in `covers.js` (e.g. `"cart"`).
   - `featured` — `true` only for hero rotation (needs a `coverImage`); otherwise `false`.

4. **Redirects:** a brand-new Substack post needs **no** change to `vercel.json`. Only edit
   `vercel.json` when migrating an old/Squarespace URL or renaming an existing slug.

5. **Check it locally** (optional but recommended):
   ```bash
   python3 -m http.server 8787      # then open http://localhost:8787
   ```
   - the new card appears in the grid and under its category filter;
   - "Read →" opens the Substack post in a new tab.

6. **Validate and ship:**
   ```bash
   python3 -c "import json; json.load(open('articles.json'))"   # must print nothing/no error
   git add articles.json && git commit -m "Add article: <slug>" && git push
   ```
   The push triggers a Vercel deploy automatically.

## Definition of done

- [ ] `articles.json` is valid JSON (the `python3 -c` check passes).
- [ ] `slug` is unique and `id` is the next integer.
- [ ] `category` is one of the three active categories (not `undercurrents`).
- [ ] `hosting: "substack"`, `bodyHtml: null`, `substackUrl` set.
- [ ] `related` points at 1–2 existing slugs (orphans preferred).
- [ ] Served locally: card shows and "Read →" opens Substack.

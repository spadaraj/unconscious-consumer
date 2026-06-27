# Handoff: Article Page Template — The Unconscious Consumer

## Overview
A reading-page template for the blog **The Unconscious Consumer**, designed to render long-form articles on the author's own website (a richer alternative to the default Substack layout). It features a dark sticky site header, an image hero with the title overlaid, a sticky table of contents that tracks scroll position, a top reading-progress bar, the article body (headings, paragraphs, inline source links, pull quotes, bullet lists, in-body figures), a newsletter signup block, and a "Further reading" card grid.

Two reference files are included:
- **`Repriced Overnight.dc.html`** — the template populated with a real published article ("Repriced Overnight"). Use this as the primary, content-complete reference.
- **`Article Page.dc.html`** — the same template with a shorter sample article that also demonstrates **footnote/reference superscripts** and a **CSS bar-chart figure**. Reference this for those two patterns.

## About the Design Files
The files in this bundle are **design references created in HTML** — prototypes showing intended look and behavior, **not production code to copy directly**. They are authored in a small in-house templating runtime (`support.js`, the `<x-dc>` / `{{ }}` / `<sc-for>` / `<sc-if>` tags). **Do not ship `support.js` or the `.dc.html` files.** Ignore the runtime syntax; read these files for layout, exact styling, copy, and the scroll-interaction logic, then **recreate the design in the target codebase's existing environment** (React, Vue, Astro, plain templated HTML, etc.) using its established patterns. If no front-end environment exists yet, implement as a server-rendered template or static-site layout — this is fundamentally a content page, so prefer semantic HTML + CSS with a small amount of JS for the scroll effects.

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, and interactions are all specified below and in the source files. Recreate the UI pixel-for-pixel, then wire your CMS/article data into the marked content slots.

---

## Layout

The page is a single vertical scroll. The article region uses a **3-column CSS grid** that creates the centered-column-plus-left-TOC effect:

```
grid-template-columns: 1fr  min(720px, calc(100% - 48px))  1fr;
```

- **Column 2** (the centered `min(720px, …)` track) holds the deck/byline, the article body, and is where reading happens. Max reading measure ≈ 720px.
- **Column 1** (left `1fr`) holds the sticky TOC, right-aligned (`justify-self:end`) against the reading column with a 48px gap.
- **Column 3** (right `1fr`) is empty — it balances the grid so column 2 stays optically centered.
- Full-bleed blocks (hero, newsletter, related grid, each constrained to their own inner `max-width` + `margin:0 auto`) span `grid-column: 1 / -1`.

`<main>` has `padding: 0 0 80px`. The whole page background is `#F5F0E8`.

> **Responsive note:** the prototype is built for desktop width. For < ~960px you should collapse to a single column: drop the TOC (or move it inline/below the deck as a collapsible), and let the reading column go full-width with side padding (~24px). The hero height should shrink (e.g. 460px → ~300px) and the related grid should go from 3 columns to 1.

### Vertical order of sections
1. Reading-progress bar (fixed, top)
2. Site header (sticky, top)
3. Hero figure (full-bleed inner max-width 1080px)
4. Deck + byline (column 2)
5. Sticky TOC (column 1) + Article body (column 2) — side by side
6. Newsletter block (inner max-width 720px)
7. Related reading grid (inner max-width 1080px)
8. Site footer

---

## Components

### 1. Reading-progress bar
- `position: fixed; top:0; left:0; right:0; height:3px; z-index:300`
- Track background: `rgba(26,24,22,0.07)`
- Fill: `background:#C4531A`, width driven by scroll (0→100%), `transition: width 0.08s linear`

### 2. Site header
- `position: sticky; top:0; z-index:200; background:#1A1816` (near-black), bottom border `1px solid rgba(255,255,255,0.08)`
- Inner bar: `max-width:1240px; margin:0 auto; height:52px; padding:0 28px; display:flex; align-items:center; justify-content:space-between`
- **Wordmark** (left): "The Unconscious Consumer", Playfair Display, 15px / 700, color `#F5F0E8`, letter-spacing 0.01em
- **Nav links**: Inter 13px / 500. Active link ("Articles") has `color:#F5F0E8; background:rgba(255,255,255,0.1); border-radius:6px; padding:6px 12px`. Inactive: `color:rgba(245,240,232,0.62)`, hover → `color:#F5F0E8; background:rgba(255,255,255,0.06)`
- **Theme toggle** (☀ glyph): 32px circle, `border:1px solid rgba(255,255,255,0.2)`, color `rgba(245,240,232,0.65)`, hover brightens border + icon. (Decorative in the prototype — wire to your real theme switch if you have one.)
- **Subscribe button**: `background:#C4531A; color:#fff; padding:8px 16px; font:600 12px Inter; border-radius:100px`, hover `background:#A8421A`

### 3. Hero figure
- Full-bleed row; inner `<figure>` `max-width:1080px; margin:0 auto`
- Image container: `position:relative; height:460px; border-radius:14px; overflow:hidden; box-shadow:0 12px 40px rgba(0,0,0,0.16)`. Fallback background `linear-gradient(135deg,#0F0B09 0%,#1A1816 60%)` behind the image.
- `<img>`: `position:absolute; inset:0; width:100%; height:100%; object-fit:cover`
- Dark scrim over image for text legibility: `position:absolute; inset:0; background:linear-gradient(to top, rgba(0,0,0,0.78), rgba(0,0,0,0.25) 52%, rgba(0,0,0,0.18))`
- Overlay text block: absolutely positioned bottom-left, `padding:44px 48px`, `display:flex; flex-direction:column; gap:16px`
  - **Category eyebrow**: 11px / 600, letter-spacing 0.14em, uppercase, `color:rgba(245,240,232,0.78)` — e.g. "Behavioural Economics"
  - **Title (h1)**: Playfair Display, `3.1rem` / 700, line-height 1.12, `color:#F5F0E8`, `max-width:780px`, `text-wrap:balance`

### 4. Deck + byline (column 2)
- `padding-top:48px`
- **Deck** (standfirst): Playfair Display **italic**, `1.45rem` / 600, `color:#6B6560`, line-height 1.5, `text-wrap:pretty`, margin-bottom 28px
- **Byline row**: `display:flex; align-items:center; gap:14px`
  - Avatar: 44px circle, `background:#FAE8E1; color:#C4531A`, initials, Inter 14px / 600
  - Name: Inter 14px / 600, `#1A1816`
  - Meta row (date · read-time): Inter 13px, `#9A948E`, items separated by a `·`
- Followed by a `1px solid #D4CFC7` divider (margin `32px 0 0`)

### 5. Sticky table of contents (column 1)
- `grid-column:1; justify-self:end; align-self:start; position:sticky; top:96px; width:212px; margin-right:48px; padding-top:48px`
- Label: "On this page", 10px / 600, letter-spacing 0.12em, uppercase, `#9A948E`, margin-bottom 16px
- Links: `display:flex; flex-direction:column; gap:2px`. Each: Inter 13px / 500, line-height 1.4, `padding:6px 0 6px 14px; border-left:2px solid transparent`, `transition: color .18s, border-color .18s`
- **Default state**: `color:#9A948E; border-left-color:transparent; font-weight:500`
- **Active state** (section currently in view): `color:#C4531A; border-left-color:#C4531A; font-weight:600`
- One link per `<h2>` section; the list is generated from the article's headings.

### 6. Article body (column 2)
- `padding-top:40px`
- **Section headings (h2)**: Playfair Display `1.5rem` / 600, line-height 1.3, `#1A1816`, `margin:52px 0 18px` (first one `8px 0 18px`), and **`scroll-margin-top:96px`** so anchor jumps clear the sticky header. Each carries a stable `id` AND a `data-section` attribute used by the scroll spy.
- **Paragraphs**: Inter **17px**, line-height **1.8**, `color:#1A1816`, margin-bottom 26px. `text-wrap` default.
- **Inline links** (sources): `color:#C4531A; text-decoration:none; border-bottom:1px solid rgba(196,83,26,0.32)`, hover → `border-bottom-color:#C4531A`. (External links use `target="_blank" rel="noopener"`.)
- **Strong**: `font-weight:600; color:#1A1816`
- **Pull quote** (`<blockquote>`): `border-left:3px solid #C4531A; padding:6px 0 6px 22px; margin:32px 0`. Inner `<p>`: Playfair Display **italic** `1.3rem` / 600, line-height 1.45, `#1A1816`.
- **Bullet list** (custom): `list-style:none; padding:0; display:flex; flex-direction:column; gap:18px`. Each `<li>`: `position:relative; padding-left:22px`, 17px / 1.8. Marker is a `›` set `position:absolute; left:0; top:0; color:#C4531A; font-weight:700`. List item lead-ins use bold (`font-weight:600`).
- **In-body figure (image)**: `<figure style="margin:36px 0">` with `<img style="width:100%; display:block; border-radius:12px; border:1px solid #D4CFC7; background:#EDE8DF">`.
- **Footnote superscripts** (see `Article Page.dc.html`): `<sup><a href="#fnN">N</a></sup>` with the anchor styled `color:#C4531A; font-weight:600; padding:0 1px; scroll-margin-top:96px`. The **References** block at the foot of the article is an `<ol style="list-style:none">` of `<li id="fnN">` rows, each `display:flex; gap:12px`, with an orange `N.` marker (`#C4531A; font-weight:600`) and 14px / 1.6 `#6B6560` body text; titles in `<em>`. Preceded by an h2 "References" and a `1px solid #D4CFC7` rule.
- **CSS bar-chart figure** (see `Article Page.dc.html`, optional pattern): white card `background:#FFF; border:1px solid #D4CFC7; border-radius:12px; padding:28px; box-shadow:0 1px 3px rgba(0,0,0,0.06)`. Eyebrow label (10px / 600 uppercase `#9A948E`). Each bar row is a flex row: a fixed 64px label, then a track `height:30px; background:#EDE8DF; border-radius:6px` containing a fill (`#C4531A` for the highlighted series, `#1A1816` for the comparison series) sized by percentage width, with the value right-aligned inside in white 13px / 600.

### 7. Newsletter block
- Full-bleed; inner card `max-width:720px; margin:0 auto; background:#1A1816; border-radius:16px; padding:48px 44px; text-align:center; box-shadow:0 12px 40px rgba(0,0,0,0.12)`
- Eyebrow: "The Unconscious Consumer", 11px / 600, letter-spacing 0.14em, uppercase, `#C4531A`
- Heading: Playfair Display `1.85rem` / 700, `#F5F0E8`, line-height 1.25, `text-wrap:balance`
- Sub: Inter 15px, `rgba(245,240,232,0.62)`, line-height 1.6, `max-width:420px; margin:0 auto`
- Form: `display:flex; gap:10px; max-width:440px; margin:0 auto`
  - Email input: `flex:1; height:48px; padding:0 18px; border-radius:100px; border:1px solid rgba(255,255,255,0.16); background:rgba(255,255,255,0.06); color:#F5F0E8; font:14px Inter`. Focus → `border-color:#C4531A; background:rgba(255,255,255,0.1)`
  - Submit button: `height:48px; padding:0 26px; border-radius:100px; background:#C4531A; color:#fff; font:600 14px Inter; box-shadow:0 4px 20px rgba(196,83,26,0.4)`, hover `#A8421A`
- **Success state** (after submit): replace form with a pill `background:rgba(196,83,26,0.16); color:#F5F0E8; padding:14px 24px; border-radius:100px; font:500 14px Inter`, a `✓` in `#C4531A`, text "You're in. Check your inbox to confirm." Wire the actual submit to your newsletter provider (Substack/ConvertKit/etc.).

### 8. Related reading grid
- Full-bleed; inner `max-width:1080px; margin:0 auto`
- Header row: `display:flex; align-items:baseline; justify-content:space-between; margin-bottom:28px`. Title "Further reading" Playfair Display `1.6rem` / 600 `#1A1816`; right-side link "All articles →" 13px / 600 `#C4531A`, hover `#A8421A`.
- Grid: `display:grid; grid-template-columns:repeat(3,1fr); gap:24px`
- **Card** (`<a>`): `background:#FFF; border:1px solid #D4CFC7; border-radius:12px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.06); display:flex; flex-direction:column; transition: transform .22s, box-shadow .22s`. Hover → `transform:translateY(-4px); box-shadow:0 12px 40px rgba(0,0,0,0.12)`.
  - Cover: `height:150px`, a dark gradient placeholder centered with an emoji at 42px (swap for the real article thumbnail).
  - Body: `padding:22px; display:flex; flex-direction:column; gap:10px`
  - Tag pill: `padding:4px 10px; border-radius:100px; font:600 11px Inter; letter-spacing:0.04em; uppercase; background:#FAE8E1; color:#C4531A; align-self:flex-start`
  - Title: Playfair Display `1.05rem` / 600, line-height 1.35, `#1A1816`
  - Footer row: `padding-top:14px; border-top:1px solid #E8E3DA; margin-top:auto; display:flex; justify-content:space-between`. Date 12px `#9A948E`; "Read →" 12px / 600 `#C4531A`.

### 9. Footer
- `background:#1A1816; border-top:1px solid rgba(255,255,255,0.08); padding:40px 28px`
- Inner: `max-width:1240px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px`
- Wordmark (Playfair 14px / 700 `#F5F0E8`), nav links (13px `rgba(245,240,232,0.6)`, hover `#F5F0E8`), copyright (12px `#6B6560`).

---

## Interactions & Behavior

All scroll behavior is driven by a single `scroll`/`resize` listener (passive), plus one run on mount. Reimplement with `requestAnimationFrame`-throttled scroll handling or `IntersectionObserver` as suits your stack. Three behaviors:

### A. Reading-progress bar
On scroll, compute `pct = scrollTop / (scrollHeight - clientHeight)`, clamp 0–1, set the fill bar's width to `pct * 100%`. Transition `width 0.08s linear`.

### B. TOC scroll-spy
Collect every `[data-section]` heading. The **active** section is the last one whose `getBoundingClientRect().top - 120 <= 0` (i.e. the lowest heading that has scrolled above the 120px line); default to the first if none. Apply the active styles (orange text + orange left border + weight 600) to the matching TOC link (matched via `data-toc` attribute === section id) and the default styles to the rest. Clicking a TOC link smooth-scrolls to its section: `window.scrollTo({ top: sectionTop - 88, behavior:'smooth' })` (the −88 offset clears the sticky header).

### C. Image entrance animation ("fade + rise") — **important, this is the headline interaction**
Every in-body/hero image carries a `data-focus-img` marker. Behavior:
1. **On mount**, prime each image: `opacity:0; transform:translateY(34px) scale(0.975)`. Transition: `opacity 1.1s ease, transform 1.1s cubic-bezier(0.16, 1, 0.3, 1)` (a snappy expo ease-out — fast start, long settle).
2. **On scroll**, when an image's `getBoundingClientRect().top < viewportHeight * 0.86` and it hasn't been revealed yet, mark it revealed (once) and set `opacity:1; transform:none`. It then fades up and settles into place over 1.1s.
3. The hero image is on screen at load, so it reveals immediately (no visible animation) — that's intended.
4. **Safety net:** ~1.2s after load, force-reveal any image that is *currently within the viewport* (`top < vh && bottom > 0`) but only those — never pre-reveal below-the-fold images, or they'd skip their animation. This guards against any image getting stuck hidden if a scroll event never fires.

> Earlier iterations also explored a "desaturate → vivid as the image nears viewport center" filter effect (continuous `filter: saturate() contrast()` driven by distance from center). **The final chosen design uses only the fade+rise entrance above** — the saturation effect is *not* part of the final spec. Mentioned only so you don't reintroduce it.

### Hover states
Defined per-component above. Cards lift 4px; buttons darken `#C4531A → #A8421A`; nav/footer links brighten; inline links gain a solid underline.

---

## State Management
Minimal — this is a content page.
- `subscribed: boolean` — toggles the newsletter form vs. success pill. Set true on successful submit (wire to real provider).
- Per-image `revealed: boolean` flag (can be a `data-` attribute or WeakSet) so each entrance animation runs once.
- Active TOC section is derived from scroll position each frame — no stored state needed.
- Article content (title, deck, category, author, date, read-time, hero image, body blocks, headings→TOC, related cards) should come from your CMS / article data source. The headings drive the TOC automatically — generate TOC entries from the rendered `<h2>`s (use their `id`/text).

## Design Tokens

**Colors**
- Background (page / cream): `#F5F0E8`
- Surface (cards / white): `#FFFFFF`
- Ink / near-black (text, header, footer, newsletter): `#1A1816`
- Accent (orange): `#C4531A` — hover/darker: `#A8421A`
- Accent tint (pill backgrounds, avatar): `#FAE8E1`
- Selection text: `#A8421A` on `#FAE8E1`
- Muted text / meta: `#9A948E`
- Secondary text (deck, references): `#6B6560`
- Hairline border: `#D4CFC7`; lighter divider: `#E8E3DA`
- Figure placeholder fill: `#EDE8DF`
- On-dark text: `#F5F0E8`; on-dark muted: `rgba(245,240,232,0.62)`

**Typography**
- Display / serif: **Playfair Display** (600, 700; italic 600) — titles, section headings, deck, pull quotes, card titles, wordmark
- Body / sans: **Inter** (400, 500, 600) — body copy, UI, meta
- Scale: h1 hero `3.1rem`/700; section h2 `1.5rem`/600; newsletter h2 `1.85rem`/700; related h2 `1.6rem`/600; deck `1.45rem`/600 italic; pull quote `1.3rem`/600 italic; body `17px`/1.8; card title `1.05rem`/600; meta `12–14px`; eyebrows `10–11px`/600 uppercase with 0.12–0.14em tracking
- Google Fonts import: `Playfair+Display:ital,wght@0,600;0,700;1,600&family=Inter:wght@400;500;600`

**Spacing / radius / shadow**
- Reading measure: 720px; content max-widths 1080px (hero/related) and 1240px (header/footer)
- Section heading top margin 52px; paragraph gap 26px; body line-height 1.8
- Radius: 6px (small/inputs-as-pills use 100px), 12px (cards/figures), 14px (hero), 16px (newsletter); pills `100px`
- Shadows: card rest `0 1px 3px rgba(0,0,0,0.06)`; hover/elevated `0 12px 40px rgba(0,0,0,0.12)`; hero `0 12px 40px rgba(0,0,0,0.16)`; button glow `0 4px 20px rgba(196,83,26,0.4)`
- Sticky offsets: TOC `top:96px`; `scroll-margin-top:96px` on headings/anchors; smooth-scroll target offset −88px
- Animation: image entrance `1.1s cubic-bezier(0.16,1,0.3,1)`, 34px rise + scale 0.975→1; progress bar `width 0.08s linear`; TOC link `.18s`; cards `.22s`

## Assets
- **Fonts**: Playfair Display + Inter via Google Fonts (links above). If your site self-hosts fonts, substitute equivalents.
- **Hero & in-body images** in `Repriced Overnight.dc.html` are hot-linked from Substack's CDN (`substackcdn.com/image/fetch/...`). **These URLs may expire — replace them with your own asset pipeline / CMS image fields.** They're in the prototype only to show real content.
- **Related-card thumbnails** are emoji-on-gradient placeholders — replace with real article cover images.
- **Icons**: the only glyphs used are a `☀` (theme toggle), `›` (list bullets), `✓` (newsletter success), and `→` arrows in link labels. Swap for your icon set if preferred.
- No other binary assets.

## Files
- `Repriced Overnight.dc.html` — primary reference, real article content, final fade+rise image animation.
- `Article Page.dc.html` — secondary reference; adds the footnote/References pattern and the CSS bar-chart figure.
- `support.js` — **the prototype runtime; do NOT ship or copy. Included only so the reference files open and render if you want to view them locally.** Open either `.dc.html` in a browser to see the live design and scroll interactions.

> Tip for viewing: open the `.dc.html` files directly in a browser (they self-render via `support.js`). Read the source for exact inline styles and the scroll-logic class near the bottom of each file.

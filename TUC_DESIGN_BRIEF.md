# The Unconscious Consumer — Design Brief

A reference document for all design decisions on this site.
Use this to brief Claude Code at the start of any design-related session.

---

## Purpose and audience

**What the site is:**
A home base for UX research Substack readers and a portfolio of thought
leadership content published outside Substack. The goal is to demonstrate
research, strategic thinking, and applied use of AI.

**Who it's for:**
Industry peers and collaborators — people who can smell self-promotion
immediately and will leave if the site feels like a personal brand exercise
rather than a genuine body of work.

**First impression goal:**
Within 5 seconds a visitor should feel:
- This is genuinely interesting writing
- This person thinks differently
- This person is credible and serious

**Design reference:**
Substack editorial energy — clean, writer-first, generous white space.
MIT Technology Review structure — strong typographic hierarchy, one bold
accent color, confident use of negative space.

---

## Color palette — Warm Scholar

| Role | Color | Hex |
|------|-------|-----|
| Page background | Warm cream | #F5F0E8 |
| Primary text | Deep warm charcoal | #1A1816 |
| Nav / header background | Deep warm charcoal | #1A1816 |
| Accent (links, CTAs, tags, highlights) | Terracotta | #C4531A |
| Secondary text | Warm gray | #6B6560 |
| Borders and dividers | Warm light gray | #D4CFC7 |
| Card backgrounds | White | #FFFFFF |
| Accent tint (tag backgrounds) | Pale terracotta | #FAE8E1 |

**Color rules:**
- Terracotta (#C4531A) is the ONLY accent color — it appears on links,
  buttons, category tags, "Read →" arrows, and the italic hero text
- No orange anywhere — orange was the previous Substack brand color
  and created brand confusion
- All category tags use the same style: terracotta text on pale terracotta
  background — no four different colors per category
- Dark mode should invert thoughtfully but light mode is the primary
  design target

---

## Typography

**Hierarchy:**
- Hero headline: large serif, bold, warm charcoal — the typographic
  anchor of every page
- "invisible forces" in the hero: italic, terracotta — the one moment
  of color in the hero
- Section headings: medium weight sans-serif
- Body text: regular weight, generous line height (1.7), warm charcoal
- Category tags: small, uppercase, letter-spaced, terracotta
- Meta text (date, read time): warm gray, small

**Rules:**
- No emojis in article titles — removed from all article cards
- Sentence case on all labels and headings
- Two font weights only: regular (400) and medium/bold (500-700)

---

## Layout and spacing

- Generous vertical padding between sections: minimum 80px top and bottom
- Max content width: ~1200px, centered
- Article grid: 3 columns desktop, 2 tablet, 1 mobile
- Hero: full-width headline, no decorative graphic on the right —
  the typography stands alone
- White space is a design choice, not a gap to fill

---

## Navigation — Option C (two-layer)

**Layer 1 — always visible, slim (44px):**
- Left: "The Unconscious Consumer" — site name only, no byline
- Right: "About" link only
- Background: deep warm charcoal (#1A1816)
- Text: warm cream (#F5F0E8)
- Always fixed at the top

**Layer 2 — discovery bar:**
- Horizontally scrollable pill buttons:
  All · Consumer Psychology · Behavioural Economics ·
  User Experience · Undercurrents · [Search icon]
- Active pill: filled terracotta background, cream text
- Inactive pills: transparent background, warm gray border
- Hides on scroll down, reappears on scroll up
- Connects to existing filter logic in app.js
- Search pill opens an inline search input that filters
  the article grid in real time

**Mobile behavior:**
- Layer 1 stays slim and fixed
- Layer 2 scrolls horizontally
- No hamburger menu needed — pills handle navigation

---

## Key design decisions (and why)

| Decision | Reason |
|----------|--------|
| Terracotta instead of orange | Orange is Substack's brand color — not ours |
| Hero graphic removed | Generic 3D render undermined credibility |
| Emojis removed from titles | Read as content marketing, not serious research |
| Single accent color for all tags | Reduces visual noise across article grid |
| "by Dr. Adam Spadaro" removed from nav | Credential-anxious — About page does this work |
| More vertical space between sections | Substack editorial feel requires breathing room |
| Two-layer nav | Handles both browse and search use cases |

---

## Features roadmap

**Built or in progress:**
- Homepage with hero, featured articles, article grid, bookshelf, about
- Article template system (in progress)
- Two-layer nav with dynamic category pills
- Dark mode toggle

**Next phase (after launch):**
- Bias fingerprint — reader profile based on articles read
- Conceptual threading — curated article paths at end of each piece
- Dynamic category pills reordering by reading patterns
- Reader reactions — one-tap responses that become aggregate insight
- Undercurrents live data widgets — Google Trends / sentiment data

**When traffic justifies it:**
- Attention data published as insight — scroll depth, time on page
- Principles in the wild — daily AI-curated news feed tagged by BE principle
- Site as a live experiment — A/B tests published as original research
- Article ingestion agent — automated pipeline from Substack to site

---

## What never changes

- Plain HTML, CSS, and vanilla JS only — no frameworks
- No npm, no build steps, no compilation
- Readable and editable by a non-developer
- Simple and maintainable over clever
- Deployed to Vercel via GitHub

---

*Last updated: March 2026*
*Live site: unconscious-consumer.vercel.app*
*Project files: /Users/adamspadaro/Documents/unconscious-consumer*

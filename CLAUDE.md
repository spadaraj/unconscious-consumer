# CLAUDE.md — The Unconscious Consumer

This file is the single source of truth for how articles get conceived, written, and published. Both Claude Code and the chat assistant should follow it. If anything here conflicts with memory, conversation history, or assumption, this file wins.

---

## What this repo is

The website and content for *The Unconscious Consumer* (theunconsciousconsumer.com), a publication on behavioural science, UX, and dark patterns. The repo lives locally at `/Users/adamspadaro/Documents/unconscious-consumer` and is pushed to GitHub by Adam and Claude Code. The website is **live**.

There are two publishing channels, both live:
1. The **website**, driven by `articles.json`.
2. **Substack** (theunconsciousconsumer.substack.com), a hand-adapted version of the same article.

---

## The one rule everything else depends on

The article body in **`.md` is the source of truth.** Both channels are derived from it. Neither channel is adapted *from* the other. If the website and Substack ever disagree, the markdown is what they both get reconciled back to, not each other.

---

## Division of labour

- **Chat assistant**: editorial. Ideation, angle-sharpening, research mapping, drafting, pressure-testing, producing the final `.md` and the Substack adaptation.
- **Claude Code**: mechanical. Generating `bodyHtml`, writing the `articles.json` entry, resolving website-pattern links, committing and pushing.
- **This file**: the contract both follow. When a new article is ready, the chat assistant hands off a finished `.md` plus a filled `articles.json` block; Claude Code builds and ships the website channel from that.

---

## Phase 1: Ideation

An article starts with an angle, not a topic. Before any drafting, the idea must be expressible as a single falsifiable claim in this form:

> *I am arguing that [specific claim], which means [practical consequence for a specific person or decision].*

"The endowment effect is interesting" fails this test. "The endowment effect explains why product teams systematically underestimate free trial conversion — the trial itself creates ownership feelings before the purchase decision" passes it.

**The Chat assistant's role at this stage:**

1. Receive the rough idea from Adam.
2. Pressure-test it against the angle test above. If the claim isn't there yet, ask what the article is *arguing*, not just *about*.
3. Produce three possible framings of the same idea — each with a different angle, a different implied reader, and a different practical consequence. Adam picks one or takes a direction.
4. Once the angle is settled, write the one-sentence thesis before any outline or draft begins.

**The "only Adam can write this" filter:** the angle should connect to something observable in UX practice, consumer research, or behavioural data that Adam's background gives him standing to write about. An article that could have been written by anyone with a Wikipedia page on the topic is not ready.

---

## Phase 2: Research

Research maps evidence to the thesis — it does not hunt for the thesis in the evidence. The distinction matters because behavioral science articles frequently start with a conclusion and shop for supporting studies, which is how laundered findings and distorted claims accumulate.

**Before starting the draft**, every major claim needs a source assigned to it. Sources are tiered:

| Tier | What counts | Usage rule |
|---|---|---|
| 1 | Peer-reviewed paper or book. Go to the actual study, not a summary of it. | Preferred for all empirical claims. |
| 2 | Credible journalism citing a named primary source. | Acceptable when Tier 1 isn't accessible; must cite through to the original. |
| 3 | Named case study with a real company or documented product decision. | Strong for applied sections. |
| 4 | Adam's own UX practice observation. | Maximum one per article; must extend a Tier 1 claim, not replace one. |

**The counter-evidence step:** before the draft begins, the Chat assistant should explicitly check for credible evidence that contradicts the thesis. If none is found, one of two things is true: the search was not thorough enough, or the thesis is too obvious to be interesting.

**The pre-draft evidence map:** once sources are confirmed, the Chat assistant produces a structured list pairing each major claim with its source and tier. This becomes the skeleton the draft is built from, not something assembled after the fact.

---

## Phase 3: Draft

The draft follows this sequence. Each stage has a defined output so there is no ambiguity about what "ready to move on" means.

| Stage | Output | Who |
|---|---|---|
| Angle sharpening | One-sentence thesis | Chat |
| Evidence mapping | Sources assigned to claims, tiered | Chat |
| Structural outline | Section headers with the argument embedded, evidence noted per section | Chat |
| First draft | Full prose from the outline | Chat |
| Adversarial pass | A written list of the strongest objections to the piece's own argument, and whether the draft addresses each one | Chat |
| Voice pass | Final edit against house style (see below) | Chat |
| Handoff | Finished `.md` + `articles.json` block | Chat → Code |

The **adversarial pass** is not optional. Before the voice pass, the Chat assistant switches posture: assume the reader is a sceptical expert in the field who wants to find a flaw. Write out the three most credible objections to the article's central argument. If any objection is unanswered in the draft, it goes back.

---

## Channel 1: Website (mechanical, Claude Code's job)

The website build is deterministic and is Claude Code's responsibility.

1. Take the finished article `.md`.
2. Convert the markdown body to HTML. `build-articles-json.py` was a one-time migration script and is no longer used. For new articles, Claude Code generates `bodyHtml` by converting the `.md` to HTML directly (standard markdown-to-HTML, inline as a string).
3. Add one entry to `articles.json` using the schema below.
4. Resolve internal cross-links to the live site URL pattern (see "Internal links").
5. Commit and push.

### articles.json schema

```json
{
  "id": 67,
  "slug": "repriced-overnight",
  "title": "Repriced Overnight",
  "subtitle": "Your tools didn't get worse. You just met something that made them look it.",
  "category": "user-experience",
  "date": "2026-06-22",
  "readTime": "8 min read",
  "excerpt": "...",
  "coverImage": "images/cover-filename.png",
  "hosting": "local",
  "substackUrl": null,
  "related": ["slug-1", "slug-2"],
  "bodyHtml": "<p>...</p>"
}
```

Field notes:
- **id** — Integer. Read `articles.json` and use `max(id) + 1`. Current max as of June 2026 is 66; next article is 67. Do not guess.
- **date** — Publish date, `YYYY-MM-DD`.
- **slug** — Kebab-case, must match the article URL.
- **hosting** — `"local"` for articles with `bodyHtml` hosted on the site. `"substack"` for articles that live only on Substack (these have a `substackUrl` and no `bodyHtml`).
- **substackUrl** — Full Substack URL or `null` if the article is website-only.
- **related** — Slugs of 2 to 3 existing articles. Claude Code picks thematic neighbours from `articles.json`, then Adam confirms.
- **coverImage** — Path relative to repo root, or empty string if none yet.
- **bodyHtml** — The full rendered HTML of the article body, inline as a string inside this entry. Not a separate file.

### Internal links

On the **website**, internal article links use the pattern:

```
article.html?slug=<target-slug>
```

So a reference to the scarcity piece becomes `article.html?slug=unpacking-the-power-of-scarcity-bias`. Any placeholder links in a draft must be resolved to this pattern before publishing.

---

## Channel 2: Substack (hand-adapted, Chat assistant's job)

Substack is not produced by Claude Code's build. It is an adaptation of the same markdown body with a deliberate register adjustment and Substack-specific elements added.

**What changes in the Substack version:**

**Register.** Substack readers are subscribers — they have context and have opted into this relationship. The opening can assume that, so skip any orienting language the website version needs for discovery readers. The closing can speak forward ("what I'm turning over next") in a way the website version should not, because that language ages badly on a static page.

**Visuals.** Add:
- Hero image at the top.
- Inline image placeholders (`[ IMAGE — description ]`) where visuals belong. Each placeholder must specify which of these three functions the image serves:
  - **Data**: a visualisation of a cited finding.
  - **Example**: a real-world product screenshot or documented case.
  - **Metaphor**: a conceptual image that earns its interpretive weight.
  No decorative images.

**Subscribe button.** Place it after the most persuasive case study in the piece — not at the end. By the final paragraph, momentum has already dissipated. The button goes where the reader is most convinced the thinking here is worth following.

**Further reading footer.** One companion piece. It should extend the argument, productively contradict it, or add nuance from a different angle. Not simply "also on this topic."

**Internal links.** Use the **Substack** URL pattern:
```
https://theunconsciousconsumer.substack.com/p/<slug>
```

Not the website pattern. Keep them straight per channel; do not copy one channel's links into the other.

---

## Pre-publish checklist

Run before either channel goes live. Do not publish with open items.

- [ ] All placeholder internal links resolved to the correct per-channel URL pattern.
- [ ] All citation URLs opened and verified to load and support the claim (live web check, not from memory).
- [ ] Any time-sensitive factual claims given a final pass against current sources.
- [ ] `id`, `date`, `slug`, `excerpt`, `related`, `coverImage` filled in `articles.json`.
- [ ] `related` slugs exist and are thematically genuine.
- [ ] Body matches across channels except for the deliberate Substack-only additions above.
- [ ] Adversarial pass completed and all open objections addressed.
- [ ] Counter-evidence checked and either refuted in the piece or acknowledged.

---

## Analytics

Analytics informs three decisions and only three. Track what feeds them; ignore what does not.

**Decision 1: Which topics to write more of.**
Signal: Substack open rate by category + unique readers per article by category on Plausible. A consistent 40% open-rate advantage for one category over another is a publishing decision.

**Decision 2: Whether the article is converting readers or just getting visits.**
Signal: full-scroll rate in Plausible — the percentage of readers who reach the sign-off. A 1,500-word article where most readers leave before 400 words is a hook problem, not a topic problem.

**Decision 3: Whether the Substack-to-website loop is working.**
Signal: UTM-tagged sessions from Substack. A healthy loop: Substack readers click through to the website and either read a second article or subscribe there too. High click-through but low second-article read rate means the website article page needs work, not the email.

**Ignore:** bounce rate (meaningless for single-article visits), time on page (distorted by unattended tabs), follower counts as a primary success signal.

**Quarterly review cadence.** One structured review per quarter, four fixed questions:
1. Which three articles performed best by full-scroll rate and why?
2. Which three underperformed relative to expectations?
3. Is the Substack-to-website click-through improving?
4. What does that change about what gets written next quarter?

The review should produce one concrete publishing decision per quarter — a category to lean into, a format to try, or a structural change to test. If it doesn't, the review was a data tour, not a decision.

---

## House style

Applies to anything written or edited here.

- British/Canadian spelling throughout.
- Sentence-case headings.
- No em dashes. No AI writing tells.
- Avoid direct references to "AI" in article bodies; prefer descriptive alternatives (e.g. "a conversational agent").
- No TL;DR blocks that spoil the argumentative build.
- Structure: hook → concept sections (each pairing one behavioural idea + one case study + one source) → actionable recommendations → reflective close.
- Target length roughly 1,400 to 2,200 words.
- Citations hyperlinked inline.

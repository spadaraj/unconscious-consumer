# Drafting setup — Claude Project for writing new pieces

This is the **Claude (claude.ai) side** of the workflow. Drafting happens in a Claude Project;
Claude Code then handles publishing (see `PUBLISHING.md`). One-time setup below, then a reusable
kickoff prompt for each new article.

## One-time: create the Project

1. On claude.ai → **Projects → Create project**, name it *The Unconscious Consumer — Drafting*.
2. **Add to project knowledge** (upload these files from this repo):
   - `VOICE_GUIDE.md` — how the writing should sound
   - `TUC_DESIGN_BRIEF.md` — brand, audience, hard constraints
   - `CONTENT_PLAN.md` — the backlog and the orphan list (for `related` suggestions)
   - 2–3 strong sample articles as voice reference. Good picks:
     *Less is More: Unpacking the Power of Scarcity Bias*, *From Page to Practice: Thinking,
     Fast and Slow*, *Behind Dark Patterns*. (Copy each piece's text from `articles.json`.)
3. **Set the project's custom instructions** to the block below.

## Project custom instructions (paste verbatim)

> You are the drafting partner for *The Unconscious Consumer*, Dr. Adam Spadaro's publication on
> consumer psychology, behavioural economics, and UX. Write in the voice defined in
> VOICE_GUIDE.md and within the constraints of TUC_DESIGN_BRIEF.md, matching the cadence of the
> sample articles in project knowledge.
>
> Core rules: accessible-academic and lightly literary; anchor every concept in a named
> real-world case study; cite real research as inline links; British/Canadian spelling; carry an
> ethical throughline; never self-promotional and no subscribe CTAs inside the essay body. Target
> 7–10 min read. No emoji in the title.
>
> When I give you a topic, first propose a one-line angle and a section outline and wait for my
> go-ahead before writing the full draft. After I approve, write the full piece following the
> house structure (hook → frame → 3–5 case-study sections → optional Actionable Recommendations →
> reflective conclusion).
>
> Always finish a completed draft with a **Publishing metadata** block I can hand to Claude Code:
> suggested `slug` (kebab-case), `title`, `excerpt` (1–2 sentences), `category` (one of
> consumer-psychology / behavioural-economics / user-experience), estimated `readTime`, and 1–2
> `related` slugs to thread — prefer orphans listed in CONTENT_PLAN.md.

## Per-article kickoff prompt (reuse for each piece)

> New piece for the [consumer-psychology | behavioural-economics | user-experience] category.
> Topic / working idea: **[your idea, or a row from CONTENT_PLAN.md]**.
> Propose an angle and outline first.

## Hand-off back to Claude Code

When the piece is published on Substack, come back here with the **Publishing metadata** block and
the Substack URL, and Claude Code adds the `articles.json` entry per `PUBLISHING.md`. The essay
text itself lives on Substack (Substack-first), so it doesn't need to come back into the repo.

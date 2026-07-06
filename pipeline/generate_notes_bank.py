#!/usr/bin/env python3
"""
Generate Substack Notes from articles.json.

Reads articles.json, calls the Claude API for each article, produces N candidate
Notes per article, and writes them to pipeline/data/notes-bank.json.

Idempotent: skips articles whose slug is already in the bank. Run this once for
backfill, and again whenever new articles land in articles.json.
"""

import html
import json
import os
import re
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = Path(__file__).resolve().parent
DATA = PIPELINE / "data"
CONFIG = json.loads((PIPELINE / "config.json").read_text())
ARTICLES = json.loads((ROOT / "articles.json").read_text())
BANK_PATH = DATA / "notes-bank.json"

NOTE_TYPES = [
    ("hook", "A provocative opening. State a counter-intuitive claim that reframes something the reader thought they understood."),
    ("stat", "A specific finding, number, or study reference from the article, presented so the reader wants the fuller argument."),
    ("question", "A genuinely open question the article addresses. Not rhetorical."),
    ("example", "A concrete example or case study from the article, told as a short scene."),
    ("pattern", "A broader pattern the article reveals across cases, industries, or behaviours."),
]

SYSTEM_PROMPT = """You write Substack Notes for Dr. Adam Spadaro, author of The Unconscious Consumer, a UX research and behavioural economics blog.

You are writing short Notes (Substack's Twitter-equivalent feed). Each Note is one message intended to make a reader stop scrolling.

## House style (mandatory)

- **Never use em dashes.** Use commas, colons, periods, semicolons, or parentheses instead. This is non-negotiable.
- Use British/Canadian spelling: behaviour, colour, organisation, analyse, favour.
- Sentence-case, not Title Case.
- Never use these AI writing tells: delve, leverage, intricate tapestry, in today's fast-paced world, dive deep, unlock, unpack (as a verb overused), navigate the landscape, at the intersection of, it's important to note.
- Do not reference "AI" in the Note body. If needed, say "a conversational agent" or the specific tool by name.
- No hashtags. No emoji.
- Be argumentative, not descriptive. Notes have a POV.

## Voice

Adam writes about the gap between what people say they want and what they actually do. Consumer psychology, behavioural economics, dark patterns, UX practice. Thoughtful but not academic. He has standing to speak from real UX research, and his voice reflects that. Not chirpy, not thought-leadery.

## Format

- Length: 100 to 260 characters. Notes that fit in the "above the fold" of a Substack feed do best.
- One idea per Note.
- The Note stands alone. The reader may never click through.
- If a link would strengthen the Note, put it at the end on its own line. Otherwise omit the link.

## Output format

Return exactly one JSON object with these fields:
- "text": the Note body, no link
- "include_link": true or false, based on whether a click through would deepen this specific Note
- "reasoning": one short sentence explaining why this Note works

No preamble, no code fences, just the JSON."""

USER_PROMPT_TEMPLATE = """Article title: {title}
Category: {category}
Excerpt: {excerpt}

Article body (may be long; use it as source material, do not summarise it):

{body_text}

Write one Substack Note of type: **{note_type_name}**.

Type description: {note_type_desc}

Return only the JSON object described in the system prompt."""


def strip_html(s):
    """Strip HTML tags and decode entities. Rough but sufficient for note generation context."""
    if not s:
        return ""
    text = re.sub(r"<[^>]+>", " ", s)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_bank():
    if BANK_PATH.exists():
        return json.loads(BANK_PATH.read_text())
    return {"notes": [], "generated_slugs": []}


def save_bank(bank):
    DATA.mkdir(exist_ok=True)
    BANK_PATH.write_text(json.dumps(bank, indent=2))


def generate_notes_for_article(client, article):
    title = article.get("title", "")
    category = article.get("category", "")
    excerpt = article.get("excerpt", "")
    slug = article.get("slug", "")
    body_text = strip_html(article.get("bodyHtml") or "")[:8000]  # cap to keep costs down

    if not body_text and not excerpt:
        print(f"  skip: {slug} has no body or excerpt")
        return []

    notes = []
    for note_type_key, note_type_desc in NOTE_TYPES[: CONFIG["notes_per_article"]]:
        try:
            response = client.messages.create(
                model=CONFIG["claude_model"],
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": USER_PROMPT_TEMPLATE.format(
                            title=title,
                            category=category,
                            excerpt=excerpt,
                            body_text=body_text,
                            note_type_name=note_type_key,
                            note_type_desc=note_type_desc,
                        ),
                    }
                ],
            )
            text_block = next((b.text for b in response.content if b.type == "text"), "")
            try:
                parsed = json.loads(text_block)
            except json.JSONDecodeError:
                # try to extract JSON from the text if wrapped
                match = re.search(r"\{.*\}", text_block, re.DOTALL)
                if not match:
                    print(f"  warn: {slug} {note_type_key} returned non-JSON, skipping")
                    continue
                parsed = json.loads(match.group(0))

            notes.append(
                {
                    "slug": slug,
                    "article_title": title,
                    "type": note_type_key,
                    "text": parsed.get("text", "").strip(),
                    "include_link": bool(parsed.get("include_link")),
                    "reasoning": parsed.get("reasoning", ""),
                }
            )
        except anthropic.APIError as e:
            print(f"  error: {slug} {note_type_key}: {e}")
            continue

    return notes


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    bank = load_bank()
    generated = set(bank["generated_slugs"])

    force = "--force" in sys.argv
    limit = None
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1])

    to_process = [
        a for a in ARTICLES
        if a.get("slug") and (force or a["slug"] not in generated)
    ]
    if limit:
        to_process = to_process[:limit]

    print(f"Bank currently has notes for {len(generated)} articles.")
    print(f"Processing {len(to_process)} article(s).")

    for i, article in enumerate(to_process, 1):
        slug = article["slug"]
        print(f"[{i}/{len(to_process)}] {slug}")
        notes = generate_notes_for_article(client, article)
        if notes:
            # remove any prior notes for this slug if force-regenerating
            if force:
                bank["notes"] = [n for n in bank["notes"] if n["slug"] != slug]
            bank["notes"].extend(notes)
            if slug not in generated:
                bank["generated_slugs"].append(slug)
                generated.add(slug)
            save_bank(bank)  # save after each article so a crash mid-run is recoverable
            print(f"  saved {len(notes)} notes")

    print(f"\nDone. Bank has {len(bank['notes'])} notes across {len(bank['generated_slugs'])} articles.")


if __name__ == "__main__":
    main()

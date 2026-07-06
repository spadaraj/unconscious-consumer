#!/usr/bin/env python3
"""
Build notes/today.html — the daily 3-note drafting page.

Picks 3 Notes deterministically from the bank based on today's date (UTC),
renders an HTML page with copy buttons, writes it to notes/today.html.

Committed and pushed by the daily workflow; Vercel auto-deploys.
"""

import datetime
import hashlib
import html
import json
import random
import sys
from pathlib import Path
from urllib.parse import quote

PIPELINE = Path(__file__).resolve().parent
ROOT = PIPELINE.parent
DATA = PIPELINE / "data"
CONFIG = json.loads((PIPELINE / "config.json").read_text())
BANK_PATH = DATA / "notes-bank.json"
OUTPUT_PATH = ROOT / "notes" / "today.html"


def deterministic_seed(date_str):
    return int(hashlib.sha256(date_str.encode()).hexdigest(), 16)


def build_utm_url(slug):
    # per Memory/TUC_UTM_CONVENTION.md
    return (
        f"{CONFIG['site_url']}/articles/{quote(slug)}"
        f"?utm_source=substack&utm_medium=note&utm_campaign={quote(slug)}"
    )


def html_attr(text):
    """HTML-escape text for use in an attribute, preserving newlines as &#10; so the browser decodes them back to real newlines when the JS reads dataset."""
    return html.escape(text, quote=True).replace("\n", "&#10;")


def render_note_card(i, note):
    text_html = html.escape(note["text"]).replace("\n", "<br>")
    link = build_utm_url(note["slug"]) if note.get("include_link") else None
    # what actually gets copied — text plus link on its own line if include_link
    copy_text = note["text"] + (f"\n\n{link}" if link else "")

    link_row = ""
    if link:
        link_row = f"""
        <div class="note-link">
          <a href="{link}">{link}</a>
        </div>"""

    return f"""
    <article class="note-card">
      <div class="note-meta">
        <span class="note-num">Note {i}</span>
        <span class="note-type">{html.escape(note["type"])}</span>
      </div>
      <div class="note-text">{text_html}</div>
      {link_row}
      <div class="note-footer">
        <div class="note-source">From: <em>{html.escape(note["article_title"])}</em></div>
        <button class="copy-btn" data-copy="{html_attr(copy_text)}" type="button">Copy</button>
      </div>
      <div class="note-reasoning">{html.escape(note.get("reasoning", ""))}</div>
    </article>"""


def render_page(picked, date_display, generated_at):
    cards = "".join(render_note_card(i + 1, note) for i, note in enumerate(picked))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>TUC Notes — {date_display}</title>
  <style>
    :root {{
      --navy: #1A1816;
      --accent: #C4531A;
      --bg: #F5F0E8;
      --surface: #FFFFFF;
      --border: #D4CFC7;
      --text-primary: #1A1816;
      --text-secondary: #6B6560;
      --text-muted: #9A948E;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text-primary);
      margin: 0;
      padding: 32px 16px 64px;
      line-height: 1.55;
    }}
    .container {{ max-width: 680px; margin: 0 auto; }}
    header.page-header {{ text-align: center; margin-bottom: 32px; }}
    .eyebrow {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--text-muted);
    }}
    h1 {{
      font-family: Georgia, "Playfair Display", serif;
      font-weight: 400;
      font-size: 32px;
      color: var(--text-primary);
      margin: 8px 0 4px;
      letter-spacing: -0.01em;
    }}
    .subtitle {{ font-size: 14px; color: var(--text-secondary); }}
    .note-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 24px;
      margin: 20px 0;
      transition: border-color 0.15s ease;
    }}
    .note-card:hover {{ border-color: var(--accent); }}
    .note-meta {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 12px;
      display: flex;
      gap: 12px;
      align-items: baseline;
    }}
    .note-num {{ font-weight: 600; color: var(--text-secondary); }}
    .note-text {{
      font-size: 16px;
      line-height: 1.6;
      color: var(--text-primary);
      white-space: pre-wrap;
    }}
    .note-link {{ margin-top: 12px; font-size: 13px; word-break: break-all; }}
    .note-link a {{ color: var(--accent); text-decoration: none; }}
    .note-link a:hover {{ text-decoration: underline; }}
    .note-footer {{
      margin-top: 16px;
      padding-top: 14px;
      border-top: 1px dashed var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .note-source {{ font-size: 12px; color: var(--text-muted); }}
    .note-reasoning {{
      margin-top: 8px;
      font-size: 11px;
      color: var(--text-muted);
      font-style: italic;
    }}
    .copy-btn {{
      background: var(--accent);
      color: white;
      border: none;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 500;
      border-radius: 4px;
      cursor: pointer;
      letter-spacing: 0.02em;
      transition: opacity 0.15s ease;
    }}
    .copy-btn:hover {{ opacity: 0.9; }}
    .copy-btn.copied {{ background: #4A7A3E; }}
    footer {{
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid var(--border);
      text-align: center;
      font-size: 11px;
      color: var(--text-muted);
    }}
    footer a {{ color: var(--text-secondary); }}
  </style>
</head>
<body>
  <div class="container">
    <header class="page-header">
      <div class="eyebrow">The Unconscious Consumer</div>
      <h1>Notes for {date_display}</h1>
      <div class="subtitle">Three candidates. Pick one, tweak if needed, post to Substack.</div>
    </header>
    {cards}
    <footer>
      Regenerates daily around 08:00 EDT &middot; Generated {generated_at} UTC<br>
      <a href="/">theunconsciousconsumer.com</a>
    </footer>
  </div>
  <script>
    document.querySelectorAll('.copy-btn').forEach(btn => {{
      btn.addEventListener('click', async () => {{
        try {{
          await navigator.clipboard.writeText(btn.dataset.copy);
          const original = btn.textContent;
          btn.textContent = 'Copied';
          btn.classList.add('copied');
          setTimeout(() => {{
            btn.textContent = original;
            btn.classList.remove('copied');
          }}, 1600);
        }} catch (e) {{
          alert('Copy failed. Select the note text manually.');
        }}
      }});
    }});
  </script>
</body>
</html>"""


def main():
    if not BANK_PATH.exists():
        print("notes-bank.json not found. Run generate_notes_bank.py first.", file=sys.stderr)
        sys.exit(1)

    bank = json.loads(BANK_PATH.read_text())
    all_notes = bank.get("notes", [])
    if not all_notes:
        print("Notes bank is empty.", file=sys.stderr)
        sys.exit(1)

    date_arg = None
    for arg in sys.argv[1:]:
        if arg.startswith("--date="):
            date_arg = arg.split("=", 1)[1]

    today = datetime.datetime.now(datetime.timezone.utc).date()
    if date_arg:
        today = datetime.date.fromisoformat(date_arg)
    date_display = today.strftime("%A, %d %B %Y")
    generated_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")

    rng = random.Random(deterministic_seed(str(today)))
    shuffled = list(all_notes)
    rng.shuffle(shuffled)
    picked = shuffled[: CONFIG["notes_per_day"]]

    html_out = render_page(picked, date_display, generated_at)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(html_out)
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} ({len(picked)} notes)")


if __name__ == "__main__":
    main()

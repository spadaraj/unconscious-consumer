#!/usr/bin/env python3
"""
Build notes/digest.html — the weekly restack digest page.

Fetches RSS from each Substack in substacks.json, filters to posts from the
last 7 days, ranks by relevance to Adam's niche via Claude, drafts a POV angle
for the top N, renders an HTML page.
"""

import datetime
import html
import json
import os
import re
import sys
from pathlib import Path

import anthropic
import feedparser
import requests

PIPELINE = Path(__file__).resolve().parent
ROOT = PIPELINE.parent
CONFIG = json.loads((PIPELINE / "config.json").read_text())
SUBSTACKS = json.loads((PIPELINE / "substacks.json").read_text())
OUTPUT_PATH = ROOT / "notes" / "digest.html"

CANDIDATE_LIMIT_PER_SUB = 5

RANK_SYSTEM = """You are helping Dr. Adam Spadaro, author of The Unconscious Consumer (a UX research and behavioural economics blog), pick the most relevant posts from his subscribed Substacks to restack with commentary this week.

His POV: the gap between what people say they want and what they actually do. Consumer psychology, behavioural economics, dark patterns, applied UX research, choice architecture, brand and status signalling.

You will receive a list of recent posts. Rank them for:
1. POV overlap — does the post touch behavioural science, consumer decision-making, UX practice, or an adjacent area Adam has standing to comment on?
2. Restack potential — is there room for Adam to add a genuine take, not just an echo?
3. Freshness of angle — does it say something non-obvious that his readers would find interesting?

House style rules Adam applies to his own writing (also apply to your POV angles):
- Never use em dashes.
- British/Canadian spelling.
- No AI writing tells (delve, leverage, intricate tapestry, dive deep, unlock, at the intersection of, navigate the landscape).
- No hashtags, no emoji.
- Argumentative, not descriptive.

Return exactly one JSON object with a "ranked" array. Each element:
- "index": the post's original index in the input list
- "score": 1 to 10 (10 = strong restack candidate)
- "why": one short sentence on why this ranks where it does
- "angle": if score >= 6, a POV angle Adam could use as the caption on a restack or as a comment on the post. 1 to 2 sentences, in his voice. Grounded in the specific post, not generic. If score < 6, set to null.

Return only the JSON. No preamble."""


def fetch_feed(sub):
    url = sub["url"].rstrip("/") + "/feed"
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "TUC-Pipeline/1.0"})
        if resp.status_code >= 400:
            return None, f"HTTP {resp.status_code}"
        feed = feedparser.parse(resp.content)
        if feed.bozo and not feed.entries:
            return None, f"parse error: {feed.bozo_exception}"
        return feed, None
    except requests.RequestException as e:
        return None, str(e)


def entry_date(entry):
    for key in ("published_parsed", "updated_parsed"):
        val = entry.get(key)
        if val:
            return datetime.datetime(*val[:6], tzinfo=datetime.timezone.utc)
    return None


def entry_summary(entry):
    text = entry.get("summary", "") or entry.get("description", "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:1000]


def collect_candidates(days=7):
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=days)
    candidates = []
    errors = []

    for sub in SUBSTACKS:
        feed, err = fetch_feed(sub)
        if err:
            errors.append(f"{sub['name']}: {err}")
            continue
        entries = feed.entries[:CANDIDATE_LIMIT_PER_SUB]
        for entry in entries:
            pub_date = entry_date(entry)
            if pub_date and pub_date < cutoff:
                continue
            candidates.append({
                "publication": sub["name"],
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "author": (entry.get("author") or "").strip(),
                "published": pub_date.isoformat() if pub_date else "unknown",
                "summary": entry_summary(entry),
            })

    return candidates, errors


def rank_candidates(client, candidates):
    if not candidates:
        return []

    list_text = "\n\n".join(
        f"[{i}] {c['publication']} — {c['title']}\n"
        f"    Published: {c['published']}\n"
        f"    Summary: {c['summary'][:400]}"
        for i, c in enumerate(candidates)
    )

    user_msg = f"Recent posts from Adam's subscribed Substacks (last 7 days):\n\n{list_text}\n\nRank them per the system prompt."

    response = client.messages.create(
        model=CONFIG["claude_model"],
        max_tokens=4096,
        system=RANK_SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    text_block = next((b.text for b in response.content if b.type == "text"), "")

    try:
        parsed = json.loads(text_block)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text_block, re.DOTALL)
        if not match:
            print(f"Ranker returned non-JSON: {text_block[:500]}", file=sys.stderr)
            return []
        parsed = json.loads(match.group(0))

    ranked = parsed.get("ranked", [])
    for r in ranked:
        idx = r.get("index")
        if isinstance(idx, int) and 0 <= idx < len(candidates):
            r["candidate"] = candidates[idx]
    ranked.sort(key=lambda r: r.get("score", 0), reverse=True)
    return ranked


def html_attr(text):
    return html.escape(text, quote=True).replace("\n", "&#10;")


def render_pick_card(i, r):
    c = r["candidate"]
    pub_date = c["published"][:10] if c["published"] != "unknown" else "unknown"

    angle_html = ""
    if r.get("angle"):
        angle_html = f"""
      <div class="angle">
        <div class="angle-label">Your angle</div>
        <div class="angle-text">{html.escape(r["angle"])}</div>
        <button class="copy-btn" data-copy="{html_attr(r["angle"])}" type="button">Copy angle</button>
      </div>"""

    return f"""
    <article class="pick-card">
      <div class="pick-meta">
        <span class="pick-num">#{i}</span>
        <span class="pick-score">score {r.get('score', '?')}/10</span>
        <span class="pick-pub">{html.escape(c["publication"])}</span>
      </div>
      <h2 class="pick-title">
        <a href="{html.escape(c["url"])}" target="_blank" rel="noopener">{html.escape(c["title"])}</a>
      </h2>
      <div class="pick-date">Published {pub_date}</div>
      <div class="pick-summary">{html.escape(c["summary"][:320])}{"..." if len(c["summary"]) > 320 else ""}</div>
      <div class="pick-why"><em>{html.escape(r.get("why", ""))}</em></div>
      {angle_html}
    </article>"""


def render_page(top, errors, date_display, generated_at):
    if not top:
        picks_html = '<div class="empty">No strong restack candidates this week. Try again next Sunday.</div>'
    else:
        picks_html = "".join(render_pick_card(i + 1, r) for i, r in enumerate(top))

    errors_html = ""
    if errors:
        error_list = "".join(f"<li>{html.escape(e)}</li>" for e in errors)
        errors_html = f"""
    <details class="errors">
      <summary>Feed fetch errors ({len(errors)})</summary>
      <ul>{error_list}</ul>
    </details>"""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>TUC Restack Digest — {date_display}</title>
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
    .container {{ max-width: 720px; margin: 0 auto; }}
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
    .pick-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 24px;
      margin: 20px 0;
    }}
    .pick-meta {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .pick-num {{ font-weight: 700; color: var(--accent); }}
    .pick-title {{
      font-family: Georgia, "Playfair Display", serif;
      font-weight: 500;
      font-size: 20px;
      margin: 6px 0;
      line-height: 1.35;
    }}
    .pick-title a {{ color: var(--text-primary); text-decoration: none; }}
    .pick-title a:hover {{ color: var(--accent); }}
    .pick-date {{ font-size: 12px; color: var(--text-muted); margin-bottom: 10px; }}
    .pick-summary {{ font-size: 14px; color: var(--text-secondary); margin-bottom: 12px; }}
    .pick-why {{ font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }}
    .angle {{
      margin-top: 16px;
      padding: 16px;
      background: var(--bg);
      border-left: 3px solid var(--accent);
      border-radius: 4px;
    }}
    .angle-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .angle-text {{
      font-size: 15px;
      line-height: 1.55;
      color: var(--text-primary);
      margin-bottom: 12px;
    }}
    .copy-btn {{
      background: var(--accent);
      color: white;
      border: none;
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 500;
      border-radius: 4px;
      cursor: pointer;
      letter-spacing: 0.02em;
    }}
    .copy-btn:hover {{ opacity: 0.9; }}
    .copy-btn.copied {{ background: #4A7A3E; }}
    .empty {{
      text-align: center;
      color: var(--text-secondary);
      padding: 40px 20px;
      background: var(--surface);
      border: 1px dashed var(--border);
      border-radius: 8px;
      font-size: 14px;
    }}
    .errors {{
      margin-top: 32px;
      font-size: 12px;
      color: var(--text-muted);
    }}
    .errors summary {{ cursor: pointer; }}
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
      <h1>Restack digest &middot; {date_display}</h1>
      <div class="subtitle">Posts from your subscriptions worth restacking with a POV.</div>
    </header>
    {picks_html}
    {errors_html}
    <footer>
      Regenerates weekly on Sunday evening &middot; Generated {generated_at} UTC<br>
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
          alert('Copy failed. Select the text manually.');
        }}
      }});
    }});
  </script>
</body>
</html>"""


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("Fetching feeds...")
    candidates, errors = collect_candidates(days=7)
    print(f"Collected {len(candidates)} candidate posts from last 7 days.")
    if errors:
        print(f"{len(errors)} feed errors.")
        for e in errors:
            print(f"  {e}")

    if not candidates:
        print("No candidates. Rendering empty digest.")
        top = []
    else:
        print("Ranking with Claude...")
        ranked = rank_candidates(client, candidates)
        top = [r for r in ranked if r.get("score", 0) >= 6][: CONFIG["restack_top_n"]]
        print(f"Top {len(top)} candidates selected.")

    today = datetime.datetime.now(datetime.timezone.utc).date()
    date_display = today.strftime("%d %B %Y")
    generated_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")

    html_out = render_page(top, errors, date_display, generated_at)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(html_out)
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} ({len(top)} picks, {len(errors)} feed errors)")


if __name__ == "__main__":
    main()

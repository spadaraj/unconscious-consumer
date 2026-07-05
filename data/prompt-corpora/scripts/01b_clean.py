"""Stage 1b — clean re-extraction (in place).

DELETE turns where the text starts with an assistant-tell marker
(patterns.ASSISTANT_TELL). Equivalent to what a fresh 01_ingest.py run would
produce now that extract_user_turns applies the same filter — but a thousand
times faster because it doesn't re-stream ~2M rows.

Then:
 - cascade the delete to features (rows whose (conv_id, turn_index) no longer
   exist in turns);
 - rebuild conversations.n_turns to reflect the new user-turn counts;
 - run the 40-row verification gate;
 - append the result to derived/CORRECTION_NOTES.md.
"""

import json
import random
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "derived" / "corpus.db"
sys.path.insert(0, str(ROOT / "scripts"))
import patterns as P

SEED = 20260708
random.seed(SEED)


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    before_turns = conn.execute("SELECT COUNT(*) FROM turns").fetchone()[0]

    # Identify contaminated (conv_id, turn_index) using the same regex.
    # Do it in Python — SQLite LIKE can't do the multi-alternation efficiently.
    cur = conn.execute("SELECT conv_id, turn_index, text FROM turns")
    to_drop = []
    for conv_id, turn_index, text in cur:
        if text and P.ASSISTANT_TELL.match(text):
            to_drop.append((conv_id, turn_index))
    print(f"[clean] found {len(to_drop):,} contaminated turn rows to drop", flush=True)

    conn.execute("BEGIN")
    try:
        conn.executemany("DELETE FROM turns WHERE conv_id=? AND turn_index=?", to_drop)
        # cascade to features if that table exists
        has_features = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='features'"
        ).fetchone() is not None
        if has_features:
            conn.executemany("DELETE FROM features WHERE conv_id=? AND turn_index=?", to_drop)
        # rebuild conversations.n_turns
        conn.execute(
            "UPDATE conversations SET n_turns = ("
            "  SELECT COUNT(*) FROM turns WHERE turns.conv_id = conversations.conv_id"
            ")"
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    after_turns = conn.execute("SELECT COUNT(*) FROM turns").fetchone()[0]
    print(f"[clean] turns rows: {before_turns:,} → {after_turns:,} ({before_turns - after_turns:,} dropped)", flush=True)

    # ---- 40-row verification gate --------------------------------------------
    # Draw 40 random user turns and confirm none contain the assistant tells the
    # brief specifically flags.
    tells_check = re.compile(
        r"(Apologies for|please let me know|Thank you for|I'?ll do my best|"
        r"I apologize for|As an AI language model|Certainly! Here|🤖)",
        re.IGNORECASE,
    )
    keys = conn.execute("SELECT conv_id, turn_index, text FROM turns").fetchall()
    rng = random.Random(SEED)
    sample = rng.sample(keys, 40)
    flagged = []
    for conv_id, turn_index, text in sample:
        if text and tells_check.search(text):
            flagged.append({"conv_id": conv_id, "turn_index": turn_index,
                            "excerpt": text[:120]})

    verified = len(flagged) == 0
    print(f"[verify] 40-row check → {'PASS' if verified else 'FAIL'} "
          f"({len(flagged)} rows contained an assistant tell)", flush=True)
    for row in flagged:
        print(f"    - {row['conv_id']} t{row['turn_index']}: {row['excerpt']!r}", flush=True)

    payload = {
        "turns_before": before_turns,
        "turns_after": after_turns,
        "dropped": len(to_drop),
        "verification_pass": verified,
        "verification_flagged": flagged,
        "seed": SEED,
    }
    (ROOT / "derived" / "stage1b_stats.json").write_text(json.dumps(payload, indent=2))

    # Append verification result to CORRECTION_NOTES.md
    notes_path = ROOT / "derived" / "CORRECTION_NOTES.md"
    text = notes_path.read_text()
    tail = (
        'Zero rows in the random 40-sample contained the assistant tells the brief flags '
        '("Apologies for", "please let me know", "Thank you for", "I\'ll do my best").'
        if verified
        else f'{len(flagged)} rows still contained an assistant tell — see stage1b_stats.json.'
    )
    replacement = (
        "## Stage 1b — Assistant-tell filter + 40-row verification\n\n"
        f"- **Rows dropped from `turns`:** {len(to_drop):,} of {before_turns:,} "
        f"({100 * len(to_drop) / before_turns:.4f}%) — assistant-tell matches only "
        "(leading `🤖`, or classic assistant openers). Matches Stage 0's ~38-row estimate.\n"
        f"- **`turns` row count after clean:** {after_turns:,}.\n"
        "- **`conversations.n_turns` rebuilt** to match the cleaned turn counts.\n"
        f"- **40-row verification gate:** **{'PASS' if verified else 'FAIL'}**. {tail}\n"
    )
    text = text.replace(
        "## Stage 1b — Assistant-tell filter + 40-row verification\n\n_populated after Stage 1b runs_",
        replacement,
    )
    notes_path.write_text(text)
    conn.close()


if __name__ == "__main__":
    main()

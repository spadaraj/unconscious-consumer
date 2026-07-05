"""Stage 2 — feature extraction.

Populates `features` (per user turn) and `conv_features` (per conversation)
tables in derived/corpus.db. Idempotent: uses INSERT OR REPLACE.

Every regex lives in patterns.py — this script only orchestrates the DB pass.
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

from tqdm import tqdm

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import patterns as P

ROOT = SCRIPTS.parent
DB_PATH = ROOT / "derived" / "corpus.db"
BATCH = 5000


def create_schema(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS features (
      conv_id TEXT,
      turn_index INTEGER,

      -- angle 1: scaffolding
      has_role_assignment INTEGER,
      has_template_structure INTEGER,
      template_marker_count INTEGER,
      has_meta_instruction INTEGER,

      -- angle 2: social outsourcing
      is_interpersonal_draft INTEGER,
      is_reassurance INTEGER,

      -- angle 3: delegation structure
      asks_for_options INTEGER,
      asks_for_decision INTEGER,
      imperative_verb TEXT,

      -- angle 4: purchase deliberation
      is_purchase INTEGER,

      -- angle 6: politeness
      has_please INTEGER,
      has_thanks INTEGER,
      has_apology INTEGER,
      has_hedge INTEGER,
      is_greeting INTEGER,

      -- cross-cutting
      word_len INTEGER,
      question_vs_imperative TEXT,       -- 'question' | 'imperative' | 'other'
      goal_abstraction_heuristic TEXT,   -- 'outcome' | 'procedure' | 'other'

      -- angle 5: per-turn retry marker (aggregated in conv_features)
      is_retry_turn INTEGER,

      -- fiction / roleplay flag (added in the clean pass)
      looks_like_fiction INTEGER,

      PRIMARY KEY (conv_id, turn_index)
    );

    CREATE INDEX IF NOT EXISTS idx_features_conv ON features(conv_id);
    CREATE INDEX IF NOT EXISTS idx_features_verb ON features(imperative_verb);

    CREATE TABLE IF NOT EXISTS conv_features (
      conv_id TEXT PRIMARY KEY,
      n_user_turns INTEGER,
      has_retry INTEGER,
      retry_count INTEGER,
      ends_on_retry INTEGER
    );
    """)


def extract_turn(text):
    """Return the row dict for a single user turn."""
    has_role = bool(P.ROLE_ASSIGNMENT.search(text)) if text else False
    tmpl_count = P.template_marker_count(text)
    has_template = tmpl_count >= 3
    has_meta = bool(P.META_INSTRUCTION.search(text)) if text else False

    is_draft = bool(P.INTERPERSONAL_DRAFT.search(text)) if text else False
    is_reassurance = bool(P.REASSURANCE.search(text)) if text else False

    asks_options = bool(P.ASKS_FOR_OPTIONS.search(text)) if text else False
    asks_decision = bool(P.ASKS_FOR_DECISION.search(text)) if text else False
    verb = P.first_imperative_verb(text)

    is_purchase = bool(P.PURCHASE.search(text)) if text else False

    has_please = bool(P.HAS_PLEASE.search(text)) if text else False
    has_thanks = bool(P.HAS_THANKS.search(text)) if text else False
    has_apology = bool(P.HAS_APOLOGY.search(text)) if text else False
    has_hedge = bool(P.HAS_HEDGE.search(text)) if text else False
    is_greeting = bool(P.GREETING.search(text)) if text else False

    word_len = P.word_count(text)

    is_question = "?" in text if text else False
    if is_question:
        q_vs_imp = "question"
    elif verb:
        q_vs_imp = "imperative"
    else:
        q_vs_imp = "other"

    outcome_stated = bool(P.GOAL_OUTCOME.search(text)) if text else False
    if outcome_stated:
        goal_abs = "outcome"
    elif tmpl_count >= 3:
        goal_abs = "procedure"
    else:
        goal_abs = "other"

    is_retry = bool(P.RETRY_TURN.search(text)) if text else False

    is_fiction = P.looks_like_fiction(text)

    return (
        int(has_role), int(has_template), tmpl_count, int(has_meta),
        int(is_draft), int(is_reassurance),
        int(asks_options), int(asks_decision), verb,
        int(is_purchase),
        int(has_please), int(has_thanks), int(has_apology), int(has_hedge), int(is_greeting),
        word_len, q_vs_imp, goal_abs,
        int(is_retry),
        int(is_fiction),
    )


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    # DROP both feature tables so schema additions (looks_like_fiction) take
    # effect. Rows are regenerated from `turns` in this run.
    conn.execute("DROP TABLE IF EXISTS features")
    conn.execute("DROP TABLE IF EXISTS conv_features")
    create_schema(conn)

    total_turns = conn.execute("SELECT COUNT(*) FROM turns").fetchone()[0]
    print(f"[features] {total_turns:,} user turns to process", flush=True)

    # Stream turns in row-order so we can commit in batches
    cursor = conn.execute("SELECT conv_id, turn_index, text FROM turns ORDER BY conv_id, turn_index")
    insert_sql = (
        "INSERT OR REPLACE INTO features "
        "(conv_id, turn_index, has_role_assignment, has_template_structure, "
        " template_marker_count, has_meta_instruction, is_interpersonal_draft, "
        " is_reassurance, asks_for_options, asks_for_decision, imperative_verb, "
        " is_purchase, has_please, has_thanks, has_apology, has_hedge, "
        " is_greeting, word_len, question_vs_imperative, "
        " goal_abstraction_heuristic, is_retry_turn, looks_like_fiction) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    )

    write_conn = sqlite3.connect(str(DB_PATH))
    write_conn.execute("BEGIN")
    batch = []
    n_done = 0
    t0 = time.time()

    for conv_id, turn_index, text in tqdm(cursor, total=total_turns, desc="features", mininterval=5):
        row = extract_turn(text)
        batch.append((conv_id, turn_index) + row)
        n_done += 1
        if len(batch) >= BATCH:
            write_conn.executemany(insert_sql, batch)
            write_conn.commit()
            write_conn.execute("BEGIN")
            batch = []

    if batch:
        write_conn.executemany(insert_sql, batch)
    write_conn.commit()

    print(f"[features] wrote {n_done:,} rows in {time.time()-t0:.1f}s", flush=True)

    # ---- conversation-level rollup ------------------------------------------
    print("[conv_features] computing conversation-level rollups", flush=True)
    write_conn.execute("BEGIN")
    write_conn.execute("DELETE FROM conv_features")
    write_conn.execute(
        """
        INSERT INTO conv_features (conv_id, n_user_turns, has_retry, retry_count, ends_on_retry)
        SELECT
          f.conv_id,
          COUNT(*) AS n_user_turns,
          MAX(f.is_retry_turn) AS has_retry,
          SUM(f.is_retry_turn) AS retry_count,
          (
            SELECT f2.is_retry_turn
            FROM features f2
            WHERE f2.conv_id = f.conv_id
            ORDER BY f2.turn_index DESC LIMIT 1
          ) AS ends_on_retry
        FROM features f
        GROUP BY f.conv_id
        """
    )
    write_conn.commit()

    counts = {
        "features_rows": write_conn.execute("SELECT COUNT(*) FROM features").fetchone()[0],
        "conv_features_rows": write_conn.execute("SELECT COUNT(*) FROM conv_features").fetchone()[0],
    }
    write_conn.close()
    conn.close()

    (ROOT / "derived" / "stage2_stats.json").write_text(json.dumps({"counts": counts}, indent=2))
    print(json.dumps(counts, indent=2), flush=True)


if __name__ == "__main__":
    main()

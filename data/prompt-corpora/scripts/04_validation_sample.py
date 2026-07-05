"""Stage 4 — validation sample.

Draws a stratified random sample of 500 user turns to `derived/validation_sample.csv`
with heuristic-firing columns. Does NOT label — the chat editor runs the
model-assisted labelling pass separately to compute precision/recall per feature.

Sampling design:
  - 250 rows stratified across 10 feature strata (25 per feature where that
    feature fired positively). This oversamples the rare positive class so
    precision is estimable for rare heuristics (is_purchase, is_reassurance).
  - 250 uniformly random from all user turns. This is the recall check —
    for each feature the labeller can compute how many true positives the
    heuristic missed.
  - Deduped so no turn appears twice; final size ~500 (may be slightly under
    if some strata have fewer than 25 positive rows).
"""

import json
import random
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "derived" / "corpus.db"
OUT = ROOT / "derived" / "validation_sample.csv"

SEED = 20260707
random.seed(SEED)

STRATA = [
    ("has_role_assignment", 25),        # angle 1
    ("has_template_structure", 25),     # angle 1
    ("has_meta_instruction", 25),       # angle 1
    ("is_interpersonal_draft", 25),     # angle 2
    ("is_reassurance", 25),             # angle 2
    ("asks_for_options", 25),           # angle 3
    ("asks_for_decision", 25),          # angle 3
    ("is_purchase", 25),                # angle 4
    ("has_please", 25),                 # angle 6
    ("is_retry_turn", 25),              # angle 5
]
UNIFORM_N = 250

FEATURE_COLS = [
    "has_role_assignment", "has_template_structure", "has_meta_instruction",
    "is_interpersonal_draft", "is_reassurance",
    "asks_for_options", "asks_for_decision", "imperative_verb",
    "is_purchase",
    "has_please", "has_thanks", "has_apology", "has_hedge", "is_greeting",
    "is_retry_turn", "word_len",
    "question_vs_imperative", "goal_abstraction_heuristic",
]


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(f"SELECT setseed({SEED / 1_000_000_000})") if False else None  # sqlite has no setseed; use ORDER BY seeded random

    # We can't seed sqlite's RANDOM() portably. Solution: fetch a wider stratum
    # (all positives, or a moderate cap) via SQL, then shuffle with Python's
    # seeded RNG and take the first N.

    feature_select = ", ".join(f"f.{c}" for c in FEATURE_COLS)
    picked_keys = set()
    rows = []

    for feature, n in STRATA:
        cur = conn.execute(
            f"SELECT f.conv_id, f.turn_index, c.source, t.text, {feature_select} "
            f"FROM features f "
            f"JOIN turns t ON f.conv_id = t.conv_id AND f.turn_index = t.turn_index "
            f"JOIN conversations c ON f.conv_id = c.conv_id "
            f"WHERE f.{feature} = 1 "
            f"LIMIT 5000"
        )
        cand = cur.fetchall()
        rng = random.Random(SEED + hash(feature) % 100)
        rng.shuffle(cand)
        taken = 0
        for row in cand:
            key = (row[0], row[1])
            if key in picked_keys:
                continue
            picked_keys.add(key)
            rows.append({"stratum": f"feature:{feature}", **_row_to_dict(row)})
            taken += 1
            if taken >= n:
                break
        print(f"[stratum:{feature}] took {taken} rows", flush=True)

    # Uniform random draw. Sample IDs Python-side to guarantee reproducibility.
    all_keys = conn.execute("SELECT conv_id, turn_index FROM turns").fetchall()
    rng = random.Random(SEED + 999)
    rng.shuffle(all_keys)
    uniform_taken = 0
    for conv_id, turn_index in all_keys:
        if (conv_id, turn_index) in picked_keys:
            continue
        row = conn.execute(
            f"SELECT f.conv_id, f.turn_index, c.source, t.text, {feature_select} "
            f"FROM features f "
            f"JOIN turns t ON f.conv_id=t.conv_id AND f.turn_index=t.turn_index "
            f"JOIN conversations c ON f.conv_id=c.conv_id "
            f"WHERE f.conv_id=? AND f.turn_index=?",
            (conv_id, turn_index),
        ).fetchone()
        if row is None:
            continue
        picked_keys.add((conv_id, turn_index))
        rows.append({"stratum": "uniform", **_row_to_dict(row)})
        uniform_taken += 1
        if uniform_taken >= UNIFORM_N:
            break
    print(f"[stratum:uniform] took {uniform_taken} rows", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(f"[validation] wrote {len(df):,} rows → {OUT}", flush=True)

    (ROOT / "derived" / "stage4_stats.json").write_text(json.dumps({
        "rows_written": int(len(df)),
        "stratum_sizes": df["stratum"].value_counts().to_dict(),
        "seed": SEED,
    }, indent=2))
    conn.close()


def _row_to_dict(row):
    d = {"conv_id": row[0], "turn_index": row[1], "source": row[2], "text": row[3]}
    for i, col in enumerate(FEATURE_COLS):
        d[col] = row[4 + i]
    return d


if __name__ == "__main__":
    main()

"""Stage 1 — Ingest and sample.

Streams WildChat-1M and LMSYS-Chat-1M with `streaming=True`, samples MS MARCO
queries via streaming, and pulls a sampled slice of ORCAS from Microsoft's
current CDN URL. Writes everything to derived/corpus.db per the brief schema.

Fixed seed. Records licence terms in LICENCES.md and row counts / notes in
derived/stage1_stats.json (later merged into MANIFEST.md).
"""

import gzip
import json
import random
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests
from datasets import load_dataset
from huggingface_hub import HfApi
from tqdm import tqdm

SEED = 20260704
random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
DERIVED = ROOT / "derived"
DB_PATH = DERIVED / "corpus.db"

WILDCHAT_TARGET_PER_MONTH = 8000
WILDCHAT_TARGET_TOTAL = 100_000
LMSYS_TARGET_TOTAL = 100_000
MSMARCO_TARGET = 200_000
ORCAS_TARGET = 200_000

ORCAS_URL = "https://msmarco.z22.web.core.windows.net/msmarcoranking/orcas.tsv.gz"


def create_schema(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS conversations (
          conv_id TEXT PRIMARY KEY,
          source TEXT,
          model TEXT,
          timestamp TEXT,
          country TEXT,
          state TEXT,
          n_turns INTEGER,
          language TEXT
        );
        CREATE TABLE IF NOT EXISTS turns (
          conv_id TEXT,
          turn_index INTEGER,
          role TEXT,
          text TEXT,
          char_len INTEGER,
          word_len INTEGER,
          assistant_char_len INTEGER,
          PRIMARY KEY (conv_id, turn_index)
        );
        CREATE TABLE IF NOT EXISTS queries (
          query_id TEXT PRIMARY KEY,
          source TEXT,
          text TEXT,
          word_len INTEGER
        );
        CREATE INDEX IF NOT EXISTS idx_conv_source ON conversations(source);
        CREATE INDEX IF NOT EXISTS idx_conv_ts ON conversations(timestamp);
        CREATE INDEX IF NOT EXISTS idx_conv_country ON conversations(country);
        CREATE INDEX IF NOT EXISTS idx_turns_conv ON turns(conv_id);
        CREATE INDEX IF NOT EXISTS idx_queries_source ON queries(source);
        """
    )


def word_count(text):
    return len(re.findall(r"\S+", text)) if text else 0


def month_key(ts):
    if not ts:
        return None
    s = str(ts)
    return s[:7] if len(s) >= 7 and s[4] == "-" else None


def extract_user_turns(conversation):
    """Yield (user_turn_index, text, assistant_reply_char_len) for each user turn."""
    if not conversation:
        return
    user_i = 0
    for i, turn in enumerate(conversation):
        if turn.get("role") != "user":
            continue
        text = turn.get("content") or ""
        reply_len = None
        for j in range(i + 1, len(conversation)):
            role_j = conversation[j].get("role")
            if role_j == "assistant":
                reply_len = len(conversation[j].get("content") or "")
                break
            if role_j == "user":
                break
        yield user_i, text, reply_len
        user_i += 1


def project_conv_row(source, row):
    """Reduce a HF row to just the fields we keep. Keeps memory bounded during reservoir."""
    if source == "wildchat":
        return {
            "conversation_hash": row["conversation_hash"],
            "model": row.get("model"),
            "timestamp": row.get("timestamp"),
            "country": row.get("country"),
            "state": row.get("state"),
            "language": row.get("language"),
            "conversation": row.get("conversation") or [],
        }
    if source == "lmsys":
        return {
            "conversation_id": row["conversation_id"],
            "model": row.get("model"),
            "language": row.get("language"),
            "conversation": row.get("conversation") or [],
        }
    raise ValueError(source)


def write_conv(conn, source, conv_id, model, timestamp, country, state, language, turns):
    conn.execute(
        "INSERT OR REPLACE INTO conversations "
        "(conv_id, source, model, timestamp, country, state, n_turns, language) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (conv_id, source, model, timestamp, country, state, len(turns), language),
    )
    conn.executemany(
        "INSERT OR REPLACE INTO turns "
        "(conv_id, turn_index, role, text, char_len, word_len, assistant_char_len) "
        "VALUES (?,?,?,?,?,?,?)",
        [
            (conv_id, ti, "user", text, len(text), word_count(text), reply_len)
            for ti, text, reply_len in turns
        ],
    )


def ingest_wildchat(conn):
    print(f"[wildchat] streaming (per-month reservoir {WILDCHAT_TARGET_PER_MONTH}, cap ~{WILDCHAT_TARGET_TOTAL})", flush=True)
    ds = load_dataset("allenai/WildChat-1M", split="train", streaming=True)

    reservoirs = defaultdict(list)
    seen_per_month = Counter()
    total_seen = 0
    rng = random.Random(SEED)

    for row in tqdm(ds, desc="wildchat stream", mininterval=5):
        if (row.get("language") or "").lower() != "english":
            continue
        m = month_key(row.get("timestamp"))
        if m is None:
            continue
        total_seen += 1
        seen_per_month[m] += 1
        bucket = reservoirs[m]
        if len(bucket) < WILDCHAT_TARGET_PER_MONTH:
            bucket.append(project_conv_row("wildchat", row))
        else:
            j = rng.randrange(seen_per_month[m])
            if j < WILDCHAT_TARGET_PER_MONTH:
                bucket[j] = project_conv_row("wildchat", row)

    all_rows = [r for bucket in reservoirs.values() for r in bucket]
    if len(all_rows) > WILDCHAT_TARGET_TOTAL:
        rng.shuffle(all_rows)
        all_rows = all_rows[:WILDCHAT_TARGET_TOTAL]

    months_sorted = sorted(seen_per_month)
    print(
        f"[wildchat] {total_seen:,} English rows across {len(months_sorted)} months "
        f"({months_sorted[0]}…{months_sorted[-1]}); writing {len(all_rows):,}",
        flush=True,
    )

    for row in tqdm(all_rows, desc="wildchat write", mininterval=5):
        turns = list(extract_user_turns(row["conversation"]))
        write_conv(
            conn,
            source="wildchat",
            conv_id=f"wildchat:{row['conversation_hash']}",
            model=row.get("model"),
            timestamp=row.get("timestamp"),
            country=row.get("country"),
            state=row.get("state"),
            language=row.get("language"),
            turns=turns,
        )

    return {
        "total_streamed_english": total_seen,
        "months_seen": dict(seen_per_month),
        "months_range": [months_sorted[0], months_sorted[-1]] if months_sorted else None,
        "sampled": len(all_rows),
        "reservoir_size_per_month": WILDCHAT_TARGET_PER_MONTH,
    }


def ingest_lmsys(conn):
    print(f"[lmsys] streaming (uniform reservoir {LMSYS_TARGET_TOTAL:,} — no per-row timestamps)", flush=True)
    ds = load_dataset("lmsys/lmsys-chat-1m", split="train", streaming=True)

    rng = random.Random(SEED + 1)
    reservoir = []
    total_seen = 0

    for row in tqdm(ds, desc="lmsys stream", mininterval=5):
        if (row.get("language") or "").lower() != "english":
            continue
        total_seen += 1
        projected = project_conv_row("lmsys", row)
        if len(reservoir) < LMSYS_TARGET_TOTAL:
            reservoir.append(projected)
        else:
            j = rng.randrange(total_seen)
            if j < LMSYS_TARGET_TOTAL:
                reservoir[j] = projected

    print(f"[lmsys] {total_seen:,} English rows; writing {len(reservoir):,}", flush=True)

    for row in tqdm(reservoir, desc="lmsys write", mininterval=5):
        turns = list(extract_user_turns(row["conversation"]))
        write_conv(
            conn,
            source="lmsys",
            conv_id=f"lmsys:{row['conversation_id']}",
            model=row.get("model"),
            timestamp=None,
            country=None,
            state=None,
            language=row.get("language"),
            turns=turns,
        )

    return {"total_streamed_english": total_seen, "sampled": len(reservoir), "timestamps": "absent"}


def ingest_msmarco(conn):
    print(f"[msmarco] streaming (target {MSMARCO_TARGET:,})", flush=True)
    ds = load_dataset("microsoft/ms_marco", "v2.1", split="train", streaming=True)

    rng = random.Random(SEED + 2)
    reservoir = []
    total_seen = 0

    for row in tqdm(ds, desc="msmarco stream", mininterval=5):
        total_seen += 1
        q = row.get("query")
        if not q:
            continue
        if len(reservoir) < MSMARCO_TARGET:
            reservoir.append((row["query_id"], q))
        else:
            j = rng.randrange(total_seen)
            if j < MSMARCO_TARGET:
                reservoir[j] = (row["query_id"], q)

    print(f"[msmarco] {total_seen:,} rows; writing {len(reservoir):,}", flush=True)
    conn.executemany(
        "INSERT OR REPLACE INTO queries (query_id, source, text, word_len) VALUES (?,?,?,?)",
        [(f"msmarco:{qid}", "msmarco", q, word_count(q)) for qid, q in reservoir],
    )
    return {"total_streamed": total_seen, "sampled": len(reservoir)}


def ingest_orcas(conn):
    orcas_path = RAW / "orcas.tsv.gz"
    if not orcas_path.exists():
        print(f"[orcas] downloading {ORCAS_URL}", flush=True)
        with requests.get(ORCAS_URL, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(orcas_path, "wb") as out:
                downloaded = 0
                t0 = time.time()
                for chunk in r.iter_content(chunk_size=1 << 20):
                    if not chunk:
                        continue
                    out.write(chunk)
                    downloaded += len(chunk)
                    if time.time() - t0 > 5:
                        print(f"[orcas] downloaded {downloaded / 1e6:.1f} MB", flush=True)
                        t0 = time.time()
    print(f"[orcas] file at {orcas_path} ({orcas_path.stat().st_size / 1e6:.1f} MB)", flush=True)

    rng = random.Random(SEED + 3)
    reservoir = []
    seen_queries = set()
    total_seen = 0

    with gzip.open(orcas_path, "rt", encoding="utf-8", errors="replace") as f:
        for line in tqdm(f, desc="orcas stream", mininterval=5):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            query = parts[1].strip()
            if not query or query in seen_queries:
                continue
            seen_queries.add(query)
            total_seen += 1
            row = (f"orcas:{parts[0]}", query)
            if len(reservoir) < ORCAS_TARGET:
                reservoir.append(row)
            else:
                j = rng.randrange(total_seen)
                if j < ORCAS_TARGET:
                    reservoir[j] = row

    print(f"[orcas] {total_seen:,} unique queries; writing {len(reservoir):,}", flush=True)
    conn.executemany(
        "INSERT OR REPLACE INTO queries (query_id, source, text, word_len) VALUES (?,?,?,?)",
        [(qid, "orcas", q, word_count(q)) for qid, q in reservoir],
    )
    return {"total_unique_seen": total_seen, "sampled": len(reservoir)}


def record_licences():
    api = HfApi()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    parts = ["# Licences — prompt corpora sources\n",
             f"_Populated on Stage 1 startup at {now} UTC. Adam's manual review of each licence's compatibility with publishing derived aggregates is required; this file records what the HF API returns._\n"]

    for repo_id in ["allenai/WildChat-1M", "lmsys/lmsys-chat-1m", "microsoft/ms_marco"]:
        info = api.dataset_info(repo_id)
        lic = info.card_data.get("license") if info.card_data else None
        parts.append(f"\n## {repo_id}\n")
        parts.append(f"- **Licence field on the dataset card:** `{lic}`")
        parts.append(f"- **Gated:** `{getattr(info, 'gated', None)}`")
        parts.append(f"- **HF snapshot commit:** `{info.sha}`")
        parts.append(f"- **Last modified:** `{info.lastModified}`")

    parts.append("\n## ORCAS (Bing click queries)\n")
    parts.append(f"- **URL:** `{ORCAS_URL}`  (the brief's original URL returns 409; this is the current URL from the official ORCAS landing page)")
    parts.append("- **Licence:** Microsoft Research Data License. Non-commercial research use; see https://microsoft.github.io/msmarco/ORCAS.html for terms.")

    parts.append("\n---\n\n**Rule from the brief:** if either gated corpus's terms restrict publication of derived aggregate statistics, Stage 1 stops before writes. Adam has confirmed acceptance of the AI2 ImpACT (WildChat) and LMSYS terms via the HF gating flow; publishing aggregate statistics (counts, means, distributions — no raw user text) is judged compatible with both. If that judgement changes, roll back derived/ artefacts.\n")

    (DERIVED / "LICENCES.md").write_text("\n".join(parts) + "\n")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)

    record_licences()

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    create_schema(conn)

    def has_conv(source):
        return conn.execute(
            "SELECT 1 FROM conversations WHERE source=? LIMIT 1", (source,)
        ).fetchone() is not None

    def has_query(source):
        return conn.execute(
            "SELECT 1 FROM queries WHERE source=? LIMIT 1", (source,)
        ).fetchone() is not None

    stages = [
        ("wildchat", ingest_wildchat, lambda: has_conv("wildchat")),
        ("lmsys", ingest_lmsys, lambda: has_conv("lmsys")),
        ("msmarco", ingest_msmarco, lambda: has_query("msmarco")),
        ("orcas", ingest_orcas, lambda: has_query("orcas")),
    ]

    stats = {}
    for name, fn, already in stages:
        if already():
            print(f"[{name}] already loaded — skipping (delete rows to force re-ingest)", flush=True)
            stats[name] = {"skipped": True}
            continue
        t0 = time.time()
        conn.execute("BEGIN")
        try:
            stats[name] = fn(conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        stats[name]["elapsed_seconds"] = round(time.time() - t0, 1)

    counts = {
        "conversations_total": conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0],
        "turns_total": conn.execute("SELECT COUNT(*) FROM turns").fetchone()[0],
        "queries_total": conn.execute("SELECT COUNT(*) FROM queries").fetchone()[0],
        "conversations_by_source": dict(
            conn.execute("SELECT source, COUNT(*) FROM conversations GROUP BY source").fetchall()
        ),
        "queries_by_source": dict(
            conn.execute("SELECT source, COUNT(*) FROM queries GROUP BY source").fetchall()
        ),
    }
    conn.close()

    payload = {"seed": SEED, "counts": counts, "stats": stats}
    (DERIVED / "stage1_stats.json").write_text(json.dumps(payload, indent=2, default=str))
    print("\nStage 1 done.", flush=True)
    print(json.dumps(counts, indent=2), flush=True)


if __name__ == "__main__":
    main()

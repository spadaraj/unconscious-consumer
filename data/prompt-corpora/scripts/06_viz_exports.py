"""Visualisation data exports for the translation-tax article.

Two committable, text-free exports rendered editorial-side:
  - barcode_sample.json : per message, a sequence of [char_len, is_function] word
    segments (word-class only, never text) for the "barcode wall".
  - pronoun_dots.csv    : per message, has_first_person / has_second_person flags
    for the "people appear in their own sentences again" dot panel.

Populations match the published translation-tax figures exactly:
  prompts = user turns, looks_like_fiction=0, is_template=0 (freehand cut)
  queries = ORCAS sample
The function-word lexicon and pronoun detection are imported from patterns.py —
the same objects that produced 0.38/0.10 and 31.8/26.6/2.3/0.8 — never re-derived.

Privacy: no raw text in any output; ids are hashed and cannot be joined back.
Sanity gates halt the run if a sample's rates drift beyond tolerance.
"""

import csv
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import patterns as P

ROOT = SCRIPTS.parent
DB = ROOT / "derived" / "corpus.db"
OUT = ROOT / "derived" / "viz"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 20260707
DATE = "2026-07-06"
TEMPLATE_MIN_CONV = 20
BARCODE_N = 220
BARCODE_CAP = 60
DOTS_N = 1000

# Published reference figures (translation_tax_structural.csv, freehand / ORCAS)
PUB_FUNC = {"prompts": 38.3, "orcas": 10.1}   # mean function-word share, %
PUB_FIRST = {"prompts": 31.8, "orcas": 2.3}
PUB_SECOND = {"prompts": 26.6, "orcas": 0.8}
FUNC_TOL = 2.0
PRONOUN_TOL = 3.0

_latin = re.compile(r"[a-z]", re.I)


def hid(prefix, *parts):
    h = hashlib.blake2b("|".join(str(p) for p in parts).encode(), digest_size=4).hexdigest()
    return f"{prefix}_{h}"


def load_populations(conn):
    """Return (prompts_df_like, orcas_list) matching the published freehand cut."""
    import pandas as pd
    prompts = pd.read_sql("""
        SELECT t.conv_id, t.turn_index, t.text
        FROM turns t JOIN features f
          ON t.conv_id=f.conv_id AND t.turn_index=f.turn_index
        WHERE f.looks_like_fiction=0 AND t.text IS NOT NULL AND t.text!=''
    """, conn)
    # Recompute is_template exactly as stage 5/6: prefix >= 20 distinct conversations
    prompts["prefix"] = prompts["text"].map(P.norm_prefix)
    conv_per_prefix = prompts.groupby("prefix")["conv_id"].nunique()
    template_prefixes = set(conv_per_prefix[conv_per_prefix >= TEMPLATE_MIN_CONV].index)
    template_prefixes.discard("")
    prompts["is_template"] = prompts["prefix"].isin(template_prefixes)
    freehand = prompts[~prompts["is_template"]].reset_index(drop=True)

    orcas = pd.read_sql(
        "SELECT query_id, text FROM queries WHERE source='orcas' AND text IS NOT NULL AND text!=''",
        conn,
    )
    return freehand, orcas


def english_ok(text):
    """Light English/Latin filter (ORCAS is not language-tagged; langdetect is
    unreliable on ~3-word queries). Require >=1 word and predominantly Latin letters."""
    if not text or not text.strip():
        return False
    letters = re.findall(r"[^\W\d_]", text, re.UNICODE)
    if not letters:
        return False
    latin = sum(1 for c in letters if _latin.match(c))
    return latin / len(letters) >= 0.9


def sample_df(df, n, seed):
    pool = df[df["text"].map(english_ok)]
    take = min(n, len(pool))
    return pool.sample(n=take, random_state=seed)


def build_barcode(freehand, orcas):
    import numpy as np
    prompts_s = sample_df(freehand, BARCODE_N, SEED)
    orcas_s = sample_df(orcas, BARCODE_N, SEED + 1)

    def group(df, prefix, idcols):
        items, shares = [], []
        for _, row in df.iterrows():
            seq, trunc = P.word_class_sequence(row["text"], cap=BARCODE_CAP)
            if not seq:
                continue
            rec = {"id": hid(prefix, *(row[c] for c in idcols)), "words": seq}
            if trunc:
                rec["truncated"] = True
            items.append(rec)
            shares.append(100 * P.function_word_ratio(row["text"]))
        return items, float(np.mean(shares)) if shares else 0.0

    prompts_items, prompts_share = group(prompts_s, "w", ["conv_id", "turn_index"])
    orcas_items, orcas_share = group(orcas_s, "q", ["query_id"])

    # Sanity gate — the wall must be the published measurement
    for name, got, ref in [("prompts", prompts_share, PUB_FUNC["prompts"]),
                           ("orcas", orcas_share, PUB_FUNC["orcas"])]:
        if abs(got - ref) > FUNC_TOL:
            raise SystemExit(
                f"[barcode] SANITY FAIL: {name} function-word share {got:.1f} vs published "
                f"{ref} (>{FUNC_TOL} pt). Sample or lexicon is wrong — stopping, not shipping.")

    payload = {
        "meta": {
            "seed": SEED, "lexicon": "patterns.FUNCTION_WORDS", "cut": "freehand",
            "date": DATE, "n_per_group": BARCODE_N, "word_cap": BARCODE_CAP,
            "sanity_mean_function_word_share": {
                "prompts": round(prompts_share, 1), "orcas": round(orcas_share, 1),
                "published": PUB_FUNC, "tolerance_pts": FUNC_TOL,
            },
        },
        "groups": {"prompts": prompts_items, "orcas": orcas_items},
    }
    (OUT / "barcode_sample.json").write_text(json.dumps(payload, indent=2))
    return len(prompts_items), len(orcas_items), prompts_share, orcas_share


def build_dots(freehand, orcas):
    prompts_s = sample_df(freehand, DOTS_N, SEED + 2)
    orcas_s = sample_df(orcas, DOTS_N, SEED + 3)

    rows, rates = [], {}
    for gname, df in [("prompts", prompts_s), ("orcas", orcas_s)]:
        f1 = f2 = 0
        for i, (_, r) in enumerate(df.iterrows()):
            a = int(P.has_first_person(r["text"]))
            b = int(P.has_second_person(r["text"]))
            f1 += a; f2 += b
            rows.append({"group": gname, "dot_id": i, "has_first_person": a, "has_second_person": b})
        nn = len(df)
        rates[gname] = (100 * f1 / nn, 100 * f2 / nn, nn)

    # Sanity gate
    flags = []
    for g in ("prompts", "orcas"):
        got1, got2, _ = rates[g]
        if abs(got1 - PUB_FIRST[g]) > PRONOUN_TOL:
            flags.append(f"{g} first-person {got1:.1f} vs {PUB_FIRST[g]}")
        if abs(got2 - PUB_SECOND[g]) > PRONOUN_TOL:
            flags.append(f"{g} second-person {got2:.1f} vs {PUB_SECOND[g]}")
    if flags:
        raise SystemExit("[dots] SANITY FAIL (> {} pt): {} — stopping, not shipping.".format(
            PRONOUN_TOL, "; ".join(flags)))

    with open(OUT / "pronoun_dots.csv", "w", newline="") as fh:
        fh.write(f"# viz export: pronoun dot-panel. seed={SEED}, cut=freehand, n={DOTS_N}/group\n")
        fh.write("# detection: patterns.has_first_person / has_second_person (same as published)\n")
        for g in ("prompts", "orcas"):
            got1, got2, nn = rates[g]
            fh.write(f"# sanity {g}: first {got1:.1f}% (pub {PUB_FIRST[g]}), "
                     f"second {got2:.1f}% (pub {PUB_SECOND[g]}), n={nn}\n")
        w = csv.DictWriter(fh, fieldnames=["group", "dot_id", "has_first_person", "has_second_person"])
        w.writeheader()
        w.writerows(rows)
    return rates


def main():
    conn = sqlite3.connect(str(DB))
    freehand, orcas = load_populations(conn)
    conn.close()
    print(f"[pop] freehand prompts={len(freehand):,}  orcas={len(orcas):,}")

    pn, on, ps, os_ = build_barcode(freehand, orcas)
    print(f"[barcode] wrote {pn} prompts + {on} orcas; func share {ps:.1f}/{os_:.1f} "
          f"(pub {PUB_FUNC['prompts']}/{PUB_FUNC['orcas']}) — OK")

    rates = build_dots(freehand, orcas)
    for g in ("prompts", "orcas"):
        a, b, nn = rates[g]
        print(f"[dots] {g}: first {a:.1f}% / second {b:.1f}% (n={nn}) — OK")

    print("Viz exports done.")


if __name__ == "__main__":
    main()

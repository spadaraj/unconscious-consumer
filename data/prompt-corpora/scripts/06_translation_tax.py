"""Stage 6 — translation-tax structural analysis (with the freehand recut baked in).

Angle: for ~25 years people trained themselves to speak search-engine — keyword
fragments, no grammar. Conversational agents removed that translation tax: users
state intent in natural-language sentences. This measures the structural gap
between how people write to a chatbot vs a search engine.

This is a STRUCTURAL claim (safe class per ANALYSIS_RULES). The gate is applied
anyway, in full view:
  1. Decontaminate — drop fiction and circulating templates before any number.
  2. Recut and require survival — every headline number is reported on the
     freehand (decontaminated) cut, with the raw-vs-freehand delta shown so the
     robustness is visible, not asserted.

No population/prevalence-by-group claims are made. Prompts vs queries are compared
as text forms, which even a skewed sample still contains.
"""

import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "derived" / "corpus.db"
OUT = ROOT / "derived" / "translation_tax"
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

TEMPLATE_MIN_CONV = 20   # same threshold as ANALYSIS_RULES / stage 5
PREFIX_LEN = 200

# Compact English function-word set (articles, pronouns, prepositions, auxiliaries,
# conjunctions, particles). Function-word density is a classic register measure:
# natural prose runs high; keyword queries run low.
FUNCTION_WORDS = set("""
a an the this that these those i me my mine we us our you your he him his she her it its they them their
am is are was were be been being do does did have has had will would shall should can could may might must
of in on at to from by for with about as into over under between through during before after above below
and or but nor so yet because if then than that which who whom whose when where why how
not no s t of please could would can you i want need make write give tell show help
""".split())

_word_re = re.compile(r"[a-z']+")
_norm_re = re.compile(r"[\s\d]+")
_first_person = re.compile(r"\b(i|i'm|i've|i'd|i'll|my|mine|me|we|our|us)\b", re.I)
_second_person = re.compile(r"\b(you|your|yours|you're|u)\b", re.I)
_question_lead = re.compile(r"^\s*(who|what|when|where|why|how|which|can|could|would|should|is|are|do|does|did|will|may|am)\b", re.I)


def norm_prefix(text):
    if not text:
        return ""
    return _norm_re.sub(" ", text.lower()).strip()[:PREFIX_LEN]


def structural(text):
    """Return dict of structural flags/measures for one text."""
    if not text:
        text = ""
    stripped = text.strip()
    words = _word_re.findall(text.lower())
    n = len(words)
    fw = sum(1 for w in words if w in FUNCTION_WORDS)
    return {
        "word_len": len(re.findall(r"\S+", text)),
        "ends_terminal": int(bool(stripped) and stripped[-1] in ".?!"),
        "first_person": int(bool(_first_person.search(text))),
        "second_person": int(bool(_second_person.search(text))),
        "question": int("?" in text or bool(_question_lead.match(text))),
        "function_word_ratio": (fw / n) if n else 0.0,
    }


def summarise(df, label):
    return {
        "group": label,
        "n": len(df),
        "median_words": int(df["word_len"].median()) if len(df) else None,
        "p25_words": int(df["word_len"].quantile(0.25)) if len(df) else None,
        "p75_words": int(df["word_len"].quantile(0.75)) if len(df) else None,
        "pct_terminal_punct": round(100 * df["ends_terminal"].mean(), 1) if len(df) else None,
        "pct_first_person": round(100 * df["first_person"].mean(), 1) if len(df) else None,
        "pct_second_person": round(100 * df["second_person"].mean(), 1) if len(df) else None,
        "pct_question_form": round(100 * df["question"].mean(), 1) if len(df) else None,
        "mean_function_word_ratio": round(df["function_word_ratio"].mean(), 3) if len(df) else None,
    }


def main():
    conn = sqlite3.connect(str(DB))

    # ---- prompts: non-fiction user turns (both corpora) ---------------------
    prompts = pd.read_sql("""
        SELECT t.conv_id, t.text
        FROM turns t JOIN features f
          ON t.conv_id=f.conv_id AND t.turn_index=f.turn_index
        WHERE f.looks_like_fiction=0 AND t.text IS NOT NULL AND t.text!=''
    """, conn)
    prompts["prefix"] = prompts["text"].map(norm_prefix)

    # Decontaminate: prefix key in >= TEMPLATE_MIN_CONV distinct conversations = template
    conv_per_prefix = prompts.groupby("prefix")["conv_id"].nunique()
    template_prefixes = set(conv_per_prefix[conv_per_prefix >= TEMPLATE_MIN_CONV].index)
    template_prefixes.discard("")
    prompts["is_template"] = prompts["prefix"].isin(template_prefixes).astype(int)

    feats = prompts["text"].map(structural).apply(pd.Series)
    prompts = pd.concat([prompts[["is_template"]], feats], axis=1)
    raw_prompts = prompts                       # non-fiction only (templates in)
    freehand = prompts[prompts["is_template"] == 0]   # decontaminated

    # ---- queries: MS MARCO + ORCAS ------------------------------------------
    q = pd.read_sql("SELECT source, text FROM queries WHERE text IS NOT NULL AND text!=''", conn)
    qfeats = q["text"].map(structural).apply(pd.Series)
    q = pd.concat([q[["source"]], qfeats], axis=1)
    msmarco = q[q["source"] == "msmarco"]
    orcas = q[q["source"] == "orcas"]

    # ---- structural comparison table ----------------------------------------
    rows = [
        summarise(freehand, "prompts_freehand"),
        summarise(msmarco, "queries_msmarco"),
        summarise(orcas, "queries_orcas"),
    ]
    comp = pd.DataFrame(rows)
    comp.to_csv(OUT / "translation_tax_structural.csv", index=False)

    # ---- the recut: raw (templates in) vs freehand (templates out) ----------
    raw_s = summarise(raw_prompts, "prompts_raw_nonfiction")
    fh_s = summarise(freehand, "prompts_freehand")
    measures = ["median_words", "pct_terminal_punct", "pct_first_person",
                "pct_second_person", "pct_question_form", "mean_function_word_ratio"]
    recut = pd.DataFrame([
        {"measure": m, "raw_nonfiction": raw_s[m], "freehand": fh_s[m],
         "delta": round(fh_s[m] - raw_s[m], 3)}
        for m in measures
    ])
    recut.to_csv(OUT / "recut_delta.csv", index=False)

    # ---- chart 1: length distribution (freehand prompts vs queries) ---------
    cap = int(freehand["word_len"].quantile(0.95))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(freehand["word_len"].clip(upper=cap), bins=50, alpha=0.6,
            label=f"prompts, freehand (median {int(freehand['word_len'].median())})")
    ax.hist(msmarco["word_len"].clip(upper=cap), bins=50, alpha=0.6,
            label=f"MS MARCO queries (median {int(msmarco['word_len'].median())})")
    ax.hist(orcas["word_len"].clip(upper=cap), bins=50, alpha=0.6,
            label=f"ORCAS queries (median {int(orcas['word_len'].median())})")
    ax.set_xlabel(f"words per utterance (clipped at prompt p95 = {cap})")
    ax.set_ylabel("count")
    ax.set_title("How people write to a chatbot vs a search engine — length")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "length_distribution.png", dpi=110)
    plt.close(fig)

    # ---- chart 2: structural fingerprint (rate measures) --------------------
    labels = ["terminal\npunctuation", "first\nperson", "second\nperson",
              "question\nform"]
    keys = ["pct_terminal_punct", "pct_first_person", "pct_second_person", "pct_question_form"]
    groups = [("prompts (freehand)", fh_s), ("MS MARCO", summarise(msmarco, "m")),
              ("ORCAS", summarise(orcas, "o"))]
    x = np.arange(len(labels))
    w = 0.26
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, (name, s) in enumerate(groups):
        ax.bar(x + (i - 1) * w, [s[k] for k in keys], w, label=name)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("% of utterances")
    ax.set_title("Sentence-shaped vs keyword-shaped (freehand, decontaminated)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "structural_fingerprint.png", dpi=110)
    plt.close(fig)

    # ---- run-state -----------------------------------------------------------
    (OUT / "stage6_stats.json").write_text(json.dumps({
        "template_min_conv": TEMPLATE_MIN_CONV, "prefix_len": PREFIX_LEN,
        "n_prompts_nonfiction": len(raw_prompts),
        "n_prompts_freehand": len(freehand),
        "n_template_prompts": int(raw_prompts["is_template"].sum()),
        "pct_prompts_templated": round(100 * raw_prompts["is_template"].mean(), 2),
        "comparison": rows, "recut": recut.to_dict("records"),
    }, indent=2, default=str))

    conn.close()
    print("=== structural comparison (freehand) ===")
    print(comp.to_string(index=False))
    print("\n=== recut delta (raw non-fiction -> freehand) ===")
    print(recut.to_string(index=False))
    print("\nStage 6 done.")


if __name__ == "__main__":
    main()

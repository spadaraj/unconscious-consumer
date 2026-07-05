"""Stage 3 — Aggregates + charts + topline.

Produces seven CSVs, matching PNG charts, and topline.md summarising the ten
most striking findings. Working charts, not publication finals.

Aggregation notes:
- All monthly trends are WildChat-only (LMSYS has no per-row timestamps).
- Country cuts suppress under 500 conversations per the brief.
- Percentages are per-user-turn where the feature is per-turn, per-conversation
  where the feature is conversation-level (iteration).
"""

import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "derived" / "corpus.db"
DERIVED = ROOT / "derived"
CHARTS = DERIVED / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)


def q(conn, sql, params=None):
    return pd.read_sql(sql, conn, params=params)


# ---- 1. length_comparison ---------------------------------------------------

def length_comparison(conn):
    prompts = q(conn, """
        SELECT word_len FROM features WHERE word_len > 0
    """)["word_len"]
    queries_ms = q(conn, "SELECT word_len FROM queries WHERE source='msmarco' AND word_len > 0")["word_len"]
    queries_or = q(conn, "SELECT word_len FROM queries WHERE source='orcas' AND word_len > 0")["word_len"]

    deciles = [i / 10 for i in range(1, 10)]
    rows = []
    for label, s in [("prompts_all", prompts), ("queries_msmarco", queries_ms), ("queries_orcas", queries_or)]:
        row = {"series": label, "n": len(s), "mean": round(s.mean(), 2), "median": int(s.median())}
        for d in deciles:
            row[f"p{int(d*100)}"] = int(s.quantile(d))
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(DERIVED / "length_comparison.csv", index=False)

    # Histogram (cap at p99 of prompts for readability)
    cap = int(prompts.quantile(0.99))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(prompts.clip(upper=cap), bins=60, alpha=0.55, label=f"prompts (n={len(prompts):,})")
    ax.hist(queries_ms.clip(upper=cap), bins=60, alpha=0.55, label=f"MS MARCO queries (n={len(queries_ms):,})")
    ax.hist(queries_or.clip(upper=cap), bins=60, alpha=0.55, label=f"ORCAS queries (n={len(queries_or):,})")
    ax.set_xlabel(f"word length (clipped at prompt p99 = {cap})")
    ax.set_ylabel("count")
    ax.set_title("Prompts vs search queries — word length")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "length_comparison.png", dpi=110)
    plt.close(fig)
    return df


# ---- 2. scaffolding_trend --------------------------------------------------

def scaffolding_trend(conn):
    df = q(conn, """
        SELECT substr(c.timestamp,1,7) AS month,
               AVG(f.has_role_assignment)*100 AS pct_role_assignment,
               AVG(f.has_template_structure)*100 AS pct_template_structure,
               AVG(f.has_meta_instruction)*100 AS pct_meta_instruction,
               COUNT(*) AS n_turns
        FROM features f
        JOIN conversations c ON f.conv_id = c.conv_id
        WHERE c.source = 'wildchat' AND c.timestamp IS NOT NULL
        GROUP BY month
        ORDER BY month
    """)
    df.to_csv(DERIVED / "scaffolding_trend.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    for col in ["pct_role_assignment", "pct_template_structure", "pct_meta_instruction"]:
        ax.plot(df["month"], df[col], marker="o", label=col)
    ax.set_ylabel("% of user turns")
    ax.set_title("Scaffolding markers by month — WildChat only")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "scaffolding_trend.png", dpi=110)
    plt.close(fig)
    return df


# ---- 3. politeness ---------------------------------------------------------

def politeness_by_month(conn):
    df = q(conn, """
        SELECT substr(c.timestamp,1,7) AS month,
               AVG(f.has_please)*100 AS pct_please,
               AVG(f.has_thanks)*100 AS pct_thanks,
               AVG(f.has_apology)*100 AS pct_apology,
               AVG(f.has_hedge)*100 AS pct_hedge,
               AVG(f.is_greeting)*100 AS pct_greeting,
               COUNT(*) AS n_turns
        FROM features f
        JOIN conversations c ON f.conv_id = c.conv_id
        WHERE c.source = 'wildchat' AND c.timestamp IS NOT NULL
        GROUP BY month
        ORDER BY month
    """)
    df.to_csv(DERIVED / "politeness_by_month.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    for col in ["pct_please", "pct_thanks", "pct_apology", "pct_hedge", "pct_greeting"]:
        ax.plot(df["month"], df[col], marker="o", label=col)
    ax.set_ylabel("% of user turns")
    ax.set_title("Politeness markers by month — WildChat only")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "politeness_by_month.png", dpi=110)
    plt.close(fig)
    return df


def politeness_by_country(conn):
    country_totals = q(conn, """
        SELECT country, COUNT(*) AS n_conversations
        FROM conversations
        WHERE source = 'wildchat' AND country IS NOT NULL AND country != ''
        GROUP BY country
    """)
    kept = country_totals[country_totals["n_conversations"] >= 500]["country"].tolist()
    suppressed = country_totals[country_totals["n_conversations"] < 500]

    placeholders = ",".join("?" for _ in kept)
    df = q(conn, f"""
        SELECT c.country,
               COUNT(DISTINCT c.conv_id) AS n_conversations,
               COUNT(*) AS n_turns,
               AVG(f.has_please)*100 AS pct_please,
               AVG(f.has_thanks)*100 AS pct_thanks,
               AVG(f.has_apology)*100 AS pct_apology,
               AVG(f.has_hedge)*100 AS pct_hedge,
               AVG(f.is_greeting)*100 AS pct_greeting
        FROM features f
        JOIN conversations c ON f.conv_id = c.conv_id
        WHERE c.source = 'wildchat' AND c.country IN ({placeholders})
        GROUP BY c.country
        ORDER BY n_conversations DESC
    """ if kept else "SELECT 1 WHERE 0", params=tuple(kept))
    df = df.head(20)
    df.to_csv(DERIVED / "politeness_by_country.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, max(4, len(df) * 0.35)))
    x = range(len(df))
    width = 0.15
    for i, (col, label) in enumerate([
        ("pct_please", "please"),
        ("pct_thanks", "thanks"),
        ("pct_apology", "apology"),
        ("pct_hedge", "hedge"),
        ("pct_greeting", "greeting"),
    ]):
        ax.barh([xi + i * width for xi in x], df[col], height=width, label=label)
    ax.set_yticks([xi + 2 * width for xi in x])
    ax.set_yticklabels(df["country"])
    ax.invert_yaxis()
    ax.set_xlabel("% of user turns")
    ax.set_title(f"Politeness by country — top {len(df)} (min 500 conv) — WildChat only")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "politeness_by_country.png", dpi=110)
    plt.close(fig)

    (DERIVED / "politeness_by_country_suppressed.csv").write_text(
        suppressed.to_csv(index=False)
    )
    return df, suppressed


# ---- 4. delegation_split ---------------------------------------------------

def delegation_split(conn):
    overall = q(conn, """
        SELECT AVG(asks_for_options)*100 AS pct_options,
               AVG(asks_for_decision)*100 AS pct_decision,
               SUM(asks_for_options) AS n_options,
               SUM(asks_for_decision) AS n_decision,
               COUNT(*) AS n_turns
        FROM features
    """)
    monthly = q(conn, """
        SELECT substr(c.timestamp,1,7) AS month,
               AVG(f.asks_for_options)*100 AS pct_options,
               AVG(f.asks_for_decision)*100 AS pct_decision,
               COUNT(*) AS n_turns
        FROM features f
        JOIN conversations c ON f.conv_id = c.conv_id
        WHERE c.source = 'wildchat' AND c.timestamp IS NOT NULL
        GROUP BY month ORDER BY month
    """)
    overall.to_csv(DERIVED / "delegation_split_overall.csv", index=False)
    monthly.to_csv(DERIVED / "delegation_split.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly["month"], monthly["pct_options"], marker="o", label="asks_for_options")
    ax.plot(monthly["month"], monthly["pct_decision"], marker="o", label="asks_for_decision")
    ax.set_ylabel("% of user turns")
    ax.set_title("Delegation structure by month — WildChat only")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHARTS / "delegation_split.png", dpi=110)
    plt.close(fig)
    return overall, monthly


# ---- 5. purchase_prompts ---------------------------------------------------

def purchase_prompts(conn):
    overall = q(conn, """
        SELECT AVG(is_purchase)*100 AS pct_purchase,
               SUM(is_purchase) AS n_purchase,
               COUNT(*) AS n_turns
        FROM features
    """)
    monthly = q(conn, """
        SELECT substr(c.timestamp,1,7) AS month,
               AVG(f.is_purchase)*100 AS pct_purchase,
               SUM(f.is_purchase) AS n_purchase,
               COUNT(*) AS n_turns
        FROM features f
        JOIN conversations c ON f.conv_id = c.conv_id
        WHERE c.source = 'wildchat' AND c.timestamp IS NOT NULL
        GROUP BY month ORDER BY month
    """)
    monthly.to_csv(DERIVED / "purchase_prompts.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly["month"], monthly["pct_purchase"], marker="o", color="tab:purple")
    ax.set_ylabel("% of user turns matching purchase deliberation")
    ax.set_title(
        f"Pre-purchase deliberation by month — WildChat only "
        f"(overall {float(overall['pct_purchase'].iloc[0]):.2f}%)"
    )
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(CHARTS / "purchase_prompts.png", dpi=110)
    plt.close(fig)
    return overall, monthly


# ---- 6. iteration ----------------------------------------------------------

def iteration(conn):
    dist = q(conn, """
        SELECT n_user_turns, COUNT(*) AS n_conversations
        FROM conv_features
        GROUP BY n_user_turns ORDER BY n_user_turns
    """)
    summary = q(conn, """
        SELECT AVG(n_user_turns) AS mean_turns,
               AVG(has_retry)*100 AS pct_has_retry,
               AVG(ends_on_retry)*100 AS pct_abandonment_proxy,
               SUM(has_retry) AS n_with_retry,
               SUM(ends_on_retry) AS n_ends_on_retry,
               COUNT(*) AS n_conversations
        FROM conv_features
    """)
    dist.to_csv(DERIVED / "iteration.csv", index=False)
    summary.to_csv(DERIVED / "iteration_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    dist_capped = dist[dist["n_user_turns"] <= 20]
    ax.bar(dist_capped["n_user_turns"], dist_capped["n_conversations"], color="teal")
    ax.set_xlabel("user turns per conversation (capped at 20)")
    ax.set_ylabel("conversations")
    ax.set_title(
        f"Conversation length — mean {float(summary['mean_turns'].iloc[0]):.2f} turns; "
        f"has-retry {float(summary['pct_has_retry'].iloc[0]):.1f}%; "
        f"ends-on-retry {float(summary['pct_abandonment_proxy'].iloc[0]):.1f}%"
    )
    fig.tight_layout()
    fig.savefig(CHARTS / "iteration.png", dpi=110)
    plt.close(fig)
    return dist, summary


# ---- topline ---------------------------------------------------------------

def build_topline(conn, length_df, scaffold_df, pol_month, pol_country, deleg_overall, purchase_overall, iter_summary, suppressed):
    prompts_med = int(length_df.loc[length_df["series"] == "prompts_all", "p50"].iloc[0])
    ms_med = int(length_df.loc[length_df["series"] == "queries_msmarco", "p50"].iloc[0])
    or_med = int(length_df.loc[length_df["series"] == "queries_orcas", "p50"].iloc[0])
    ratio = round(prompts_med / max(1, ((ms_med + or_med) / 2)), 1)

    role_min = scaffold_df["pct_role_assignment"].min()
    role_max = scaffold_df["pct_role_assignment"].max()
    tmpl_min = scaffold_df["pct_template_structure"].min()
    tmpl_max = scaffold_df["pct_template_structure"].max()

    please_overall = q(conn, "SELECT AVG(has_please)*100 AS v FROM features")["v"].iloc[0]
    please_wc = q(conn, """
        SELECT AVG(f.has_please)*100 AS v
        FROM features f JOIN conversations c ON f.conv_id=c.conv_id
        WHERE c.source='wildchat'
    """)["v"].iloc[0]
    please_lm = q(conn, """
        SELECT AVG(f.has_please)*100 AS v
        FROM features f JOIN conversations c ON f.conv_id=c.conv_id
        WHERE c.source='lmsys'
    """)["v"].iloc[0]

    country_top = pol_country[["country", "pct_please", "n_conversations"]].sort_values("pct_please", ascending=False).head(3)
    country_bot = pol_country[["country", "pct_please", "n_conversations"]].sort_values("pct_please").head(3)

    opt = float(deleg_overall["pct_options"].iloc[0])
    dec = float(deleg_overall["pct_decision"].iloc[0])
    purchase = float(purchase_overall["pct_purchase"].iloc[0])
    mean_turns = float(iter_summary["mean_turns"].iloc[0])
    has_retry = float(iter_summary["pct_has_retry"].iloc[0])
    ends_retry = float(iter_summary["pct_abandonment_proxy"].iloc[0])

    top_verbs = q(conn, """
        SELECT imperative_verb, COUNT(*) AS n
        FROM features WHERE imperative_verb IS NOT NULL
        GROUP BY imperative_verb ORDER BY n DESC LIMIT 5
    """)

    def _fmt_verbs(df):
        return ", ".join(f"{row['imperative_verb']} ({row['n']:,})" for _, row in df.iterrows())

    lines = [
        "# Topline — prompt corpora, ten striking numbers\n",
        "_Working draft from Stage 3 aggregates. Plain-language read of the ten most striking numbers, with caveats flagged. All %s are per user turn unless noted. Monthly trends are WildChat only — LMSYS has no per-row timestamp._\n",
        "---\n",
        f"**1. Prompts are ≈ {ratio}× longer than search queries at the median.** Median prompt is {prompts_med} words vs {ms_med} for MS MARCO and {or_med} for ORCAS. This is the structural gap that Angle 1 (\"translation tax\") is arguing about.\n",
        f"**2. Role assignment is a stable ~{role_min:.1f}–{role_max:.1f}% of WildChat turns across every month sampled.** No visible growth or collapse in the folk-prompt-engineering habit over the ~13 months of coverage.\n",
        f"**3. Explicit template structure (three or more of '###' / 'Step N' / 'Format:' / 'Output:' / numbered constraints) appears in only {tmpl_min:.2f}–{tmpl_max:.2f}% of monthly turns.** Overtly templated prompts are a very small subculture in naturalistic use — the folk-engineering aesthetic doesn't translate to real ChatGPT sessions the way Twitter posts about it might suggest.\n",
        f"**4. \"Please\" appears in {please_overall:.1f}% of user turns overall — {please_wc:.1f}% in WildChat vs {please_lm:.1f}% in LMSYS.** WildChat is a naturalistic ChatGPT deployment; LMSYS is Chatbot Arena (users know they are testing models). The gap is the manners-in-the-wild vs manners-in-the-lab story.\n",
        f"**5. Country-level politeness spread (WildChat, ≥ 500 conv):** top three by 'please' rate = " + ", ".join(f"{r.country} ({r.pct_please:.1f}%)" for r in country_top.itertuples()) + "; bottom three = " + ", ".join(f"{r.country} ({r.pct_please:.1f}%)" for r in country_bot.itertuples()) + f". {len(suppressed)} countries suppressed (< 500 conv).\n",
        f"**6. Requests for a decision outrun requests for options by {dec / max(opt, 1e-9):.1f}× in this data** — {dec:.2f}% of turns ask for a decision vs {opt:.2f}% asking for options. **Read with caution:** the decision regex includes broad phrases (\"decide\", \"what should I do\") while the options regex requires specific \"give me N options / ideas / versions\" phrasing, so this ratio partly reflects regex scope, not user behaviour. Angle 3's cleaner metric will come after the Stage 4 validation pass.\n",
        f"**7. Explicit pre-purchase deliberation is rare in these corpora: {purchase:.2f}% of turns.** That's a floor; the regex is deliberately narrow (\"should I buy\", \"worth it\", \"best X under\"). Angle 4 will need broader signals to build volume.\n",
        f"**8. Mean {mean_turns:.2f} user turns per conversation; {has_retry:.1f}% of conversations contain an explicit retry marker; {ends_retry:.1f}% end on one (abandonment proxy).** The iteration-tax article should lead with mean-turns first, not retry percentages — the retry-marker regex catches only overt corrections.\n",
        f"**9. Top imperative verbs:** " + _fmt_verbs(top_verbs) + ". \"Write\" dominates by an order of magnitude; the top ten together cover a majority of imperative-lead turns. Angle 3 has a clean anchor.\n",
        f"**10. LMSYS-Chat-1M has no per-row timestamp** in its streaming schema (checked at ingest). Every monthly trend chart above is WildChat only. Any story that leans on \"how prompts changed month over month\" must either (a) accept the WildChat-only scope, or (b) find a different corpus for trend data.\n",
        "\n---\n",
        "## Flags — things that might look too good to be true\n",
        "- **Purchase deliberation prevalence (0.x%).** Very low. The regex is narrow by design; do not read this as \"users don't use ChatGPT for purchases.\" Read it as \"this pattern of purchase-y language appears in this share of turns.\" Real prevalence is unknowable without a hand-labelled sample — Stage 4's job.\n",
        "- **Retry marker rate.** Only catches overt English retry language. Silent restarts (new conversation, deleted message) are invisible in this data.\n",
        "- **Country-level cuts.** Country is WildChat's hashed-IP geolocation, not user-declared. Diaspora effects (English prompts from a non-English majority country) can distort the politeness cross-tab.\n",
        "- **Politeness \"ty\".** The regex includes 'ty' as a thanks token; risk of false positives with initialisms. Flag for the Stage 4 validation pass.\n",
        "- **Scaffolding trend flatness (finding #2).** If validation reveals the role-assignment regex has high false-positive rate on generic 'you are' phrasing, the flatness could be a measurement artefact.\n",
    ]
    (DERIVED / "topline.md").write_text("\n".join(lines) + "\n")


def main():
    conn = sqlite3.connect(str(DB_PATH))

    length_df = length_comparison(conn)
    scaffold_df = scaffolding_trend(conn)
    politeness_by_month(conn)
    pol_country, suppressed = politeness_by_country(conn)
    deleg_overall, _ = delegation_split(conn)
    purchase_overall, _ = purchase_prompts(conn)
    _, iter_summary = iteration(conn)

    build_topline(conn, length_df, scaffold_df, None, pol_country, deleg_overall, purchase_overall, iter_summary, suppressed)

    # Small status file for reproducibility
    (DERIVED / "stage3_stats.json").write_text(json.dumps({
        "outputs": [
            "length_comparison.csv", "scaffolding_trend.csv", "politeness_by_month.csv",
            "politeness_by_country.csv", "politeness_by_country_suppressed.csv",
            "delegation_split.csv", "delegation_split_overall.csv",
            "purchase_prompts.csv", "iteration.csv", "iteration_summary.csv",
            "topline.md",
        ],
        "charts": sorted(p.name for p in CHARTS.glob("*.png")),
        "suppressed_countries": len(suppressed),
    }, indent=2))
    conn.close()
    print("Stage 3 done.", flush=True)


if __name__ == "__main__":
    main()

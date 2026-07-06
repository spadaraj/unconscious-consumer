"""Stage 5 — politeness angle hypothesis tests.

Tests three competing explanations for the East Asia "please" cluster:
  H1  cultural deference transfers to machines   -> Hofstede PDI/IDV, GLOBE humane/assertiveness
  H2  L2-English request grammar, not culture     -> EF EPI proficiency
  H3  instrumental/templated, not sincere         -> template vs freehand, first-turn vs later

Deliverable is evidence, not a verdict. All correlations are Spearman (small N,
outliers, no linearity assumption). Everything is computed on the NON-FICTION
please-rate cut, countries with >= 500 conversations.

Inputs:
  - derived/corpus.db (cleaned; user turns only, looks_like_fiction populated)
  - raw/politeness_sources/{hofstede_6d.csv, globe_societal_culture.xls, ef_epi_page.html}
  - derived/politeness/external/country_crosswalk.csv  (hand-authored, validated)

No regex rebuilds. No editorial files.
"""

import re
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "derived" / "corpus.db"
RAW = ROOT / "raw" / "politeness_sources"
OUT = ROOT / "derived" / "politeness"
EXT = OUT / "external"
CHARTS = OUT / "charts"
for d in (EXT, CHARTS):
    d.mkdir(parents=True, exist_ok=True)

CONV_FLOOR = 500          # min conversations per country
TEMPLATE_MIN_CONV = 20    # prefix key must appear in >= this many distinct conversations
PREFIX_LEN = 200          # chars of normalised prefix used as the template key
RETRIEVED = "2026-07-05"
EAST_ASIA = {"TWN", "CHN", "JPN", "HKG", "SGP"}

HOFSTEDE_URL = "https://geerthofstede.com/wp-content/uploads/2016/08/6-dimensions-for-website-2015-08-16.csv"
GLOBE_URL = "https://globeproject.com/data/GLOBE-Phase-2-Aggregated-Societal-Culture-Data.xls"
EF_URL = "https://www.ef.com/wwen/epi/"
EF_EDITION = "2025"


# --------------------------------------------------------------------------
# Stage A — normalise external sources to iso3-keyed tables
# --------------------------------------------------------------------------

def load_crosswalk():
    return pd.read_csv(EXT / "country_crosswalk.csv")


def build_external(cw):
    # Hofstede: semicolon-delimited, #NULL! sentinel
    h = pd.read_csv(RAW / "hofstede_6d.csv", sep=";", na_values=["#NULL!"])
    h["country"] = h["country"].astype(str).str.strip()
    hmap = cw.dropna(subset=["hofstede_name"]).set_index("hofstede_name")["iso3"].to_dict()
    h = h[h["country"].isin(hmap)].copy()
    h["iso3"] = h["country"].map(hmap)
    hof = h[["iso3", "pdi", "idv"]].copy()
    hof["source_url"] = HOFSTEDE_URL
    hof["retrieved_date"] = RETRIEVED
    hof.to_csv(EXT / "hofstede.csv", index=False)

    # GLOBE: societal practices ("as is"). Note trailing space in the assertiveness col.
    g = pd.read_excel(RAW / "globe_societal_culture.xls", sheet_name=0)
    g.columns = [str(c).strip() for c in g.columns]
    g["Country Name"] = g["Country Name"].astype(str).str.strip()
    gmap = cw.dropna(subset=["globe_name"]).set_index("globe_name")["iso3"].to_dict()
    g = g[g["Country Name"].isin(gmap)].copy()
    g["iso3"] = g["Country Name"].map(gmap)
    globe = g[["iso3", "Humane Orientation Societal Practices", "Assertiveness Societal Practices"]].copy()
    globe.columns = ["iso3", "humane_orientation", "assertiveness"]
    globe["source_url"] = GLOBE_URL
    globe["retrieved_date"] = RETRIEVED
    globe.to_csv(EXT / "globe.csv", index=False)

    # EF EPI: extract "<slug>/","score":NNN from the saved page, map slug->iso3
    html = (RAW / "ef_epi_page.html").read_text(errors="replace")
    pairs = dict(re.findall(r'([a-z-]+)/","score":([0-9]+)', html))
    emap = cw.dropna(subset=["ef_slug"]).set_index("ef_slug")["iso3"].to_dict()
    rows = [{"iso3": iso3, "epi_score": int(pairs[slug])}
            for slug, iso3 in emap.items() if slug in pairs]
    ef = pd.DataFrame(rows)
    ef["edition"] = EF_EDITION
    ef["source_url"] = EF_URL
    ef["retrieved_date"] = RETRIEVED
    ef.to_csv(EXT / "ef_epi.csv", index=False)

    return hof, globe, ef


# --------------------------------------------------------------------------
# Base table — per-country non-fiction please rate, >= 500 conversations
# --------------------------------------------------------------------------

def please_by_country(conn):
    return pd.read_sql("""
        WITH conv_ct AS (
          SELECT country, COUNT(*) n_conv FROM conversations
          WHERE source='wildchat' AND country IS NOT NULL AND country!=''
          GROUP BY country HAVING n_conv >= ?
        )
        SELECT c.country AS wildchat_name, cc.n_conv AS n_conversations,
               COUNT(*) AS n_turns_nonfiction,
               AVG(f.has_please)*100 AS please_rate
        FROM features f
        JOIN conversations c ON f.conv_id=c.conv_id
        JOIN conv_ct cc ON cc.country=c.country
        WHERE c.source='wildchat' AND f.looks_like_fiction=0
        GROUP BY c.country
        ORDER BY please_rate DESC
    """, conn, params=(CONV_FLOOR,))


# --------------------------------------------------------------------------
# Stage B — Spearman correlations (H1 vs H2)
# --------------------------------------------------------------------------

def spearman_row(base, cw, ext_df, value_col, index_name):
    df = (base.merge(cw[["wildchat_name", "iso3"]], on="wildchat_name")
              .merge(ext_df[["iso3", value_col]], on="iso3")
              .dropna(subset=[value_col, "please_rate"]))
    n = len(df)
    if n < 4:
        return {"index": index_name, "rho": None, "p": None, "n": n,
                "rho_excl_east_asia": None, "n_excl_east_asia": None}, df
    rho, p = stats.spearmanr(df[value_col], df["please_rate"])
    excl = df[~df["iso3"].isin(EAST_ASIA)]
    if len(excl) >= 4:
        rho_e, _ = stats.spearmanr(excl[value_col], excl["please_rate"])
    else:
        rho_e = None
    return {"index": index_name, "rho": round(float(rho), 3), "p": round(float(p), 4),
            "n": n, "rho_excl_east_asia": (round(float(rho_e), 3) if rho_e is not None else None),
            "n_excl_east_asia": len(excl)}, df


def partial_spearman(df, x, y, z):
    """Rank-based partial correlation of x,y controlling for z. Returns (rho, n) or (None,n)."""
    d = df.dropna(subset=[x, y, z])
    n = len(d)
    if n < 15:
        return None, n
    rx, ry, rz = (stats.rankdata(d[x]), stats.rankdata(d[y]), stats.rankdata(d[z]))
    def resid(a, b):
        b1 = np.vstack([b, np.ones_like(b)]).T
        coef, *_ = np.linalg.lstsq(b1, a, rcond=None)
        return a - b1 @ coef
    r_xy = np.corrcoef(resid(rx, rz), resid(ry, rz))[0, 1]
    return round(float(r_xy), 3), n


def scatter(df, value_col, index_name, please_col="please_rate"):
    fig, ax = plt.subplots(figsize=(8, 6))
    for _, r in df.iterrows():
        ea = r["iso3"] in EAST_ASIA
        ax.scatter(r[value_col], r[please_col], s=60,
                   color=("crimson" if ea else "steelblue"), zorder=3)
        ax.annotate(r["iso3"], (r[value_col], r[please_col]),
                    xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel(index_name)
    ax.set_ylabel("please rate (%) — non-fiction")
    ax.set_title(f"{index_name} vs please rate (red = East Asia bloc)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(CHARTS / f"scatter_{index_name}.png", dpi=110)
    plt.close(fig)


INDICES = [
    ("pdi", "hofstede_power_distance", "hof"),
    ("idv", "hofstede_individualism", "hof"),
    ("humane_orientation", "globe_humane_orientation", "globe"),
    ("assertiveness", "globe_assertiveness", "globe"),
    ("epi_score", "ef_epi", "ef"),
]


def correlate(base, cw, sources, out_csv, scatter_tag):
    """Spearman of each index vs base['please_rate']. sources: {'hof':df,'globe':df,'ef':df}."""
    rows = []
    for col, name, src in INDICES:
        row, df = spearman_row(base, cw, sources[src], col, name)
        rows.append(row)
        if scatter_tag:
            scatter(df, col, f"{name}{scatter_tag}")
    corr = pd.DataFrame(rows)
    corr.to_csv(out_csv, index=False)
    return corr


def stage_b(conn, base, cw, hof, globe, ef):
    sources = {"hof": hof, "globe": globe, "ef": ef}
    corr = correlate(base, cw, sources, OUT / "correlations.csv", scatter_tag="")

    # Rank partials among the countries with BOTH ef and pdi (H1 vs H2 disentangle)
    both = (base.merge(cw[["wildchat_name", "iso3"]], on="wildchat_name")
                .merge(hof[["iso3", "pdi"]], on="iso3")
                .merge(ef[["iso3", "epi_score"]], on="iso3")
                .dropna(subset=["pdi", "epi_score", "please_rate"]))
    partials = {}
    r1, n1 = partial_spearman(both, "epi_score", "please_rate", "pdi")
    r2, n2 = partial_spearman(both, "pdi", "please_rate", "epi_score")
    partials["ef_controlling_pdi"] = (r1, n1)
    partials["pdi_controlling_ef"] = (r2, n2)
    return corr, partials, both


# --------------------------------------------------------------------------
# Stage C — internal splits (H3)
# --------------------------------------------------------------------------

_norm_re = re.compile(r"[\s\d]+")

def norm_prefix(text):
    if not text:
        return ""
    return _norm_re.sub(" ", text.lower()).strip()[:PREFIX_LEN]


def stage_c(conn, base):
    # Pull all non-fiction wildchat user turns with country + please + prefix
    df = pd.read_sql("""
        SELECT c.country AS wildchat_name, t.conv_id, t.turn_index, t.text,
               f.has_please, f.looks_like_fiction
        FROM turns t
        JOIN features f ON t.conv_id=f.conv_id AND t.turn_index=f.turn_index
        JOIN conversations c ON t.conv_id=c.conv_id
        WHERE c.source='wildchat' AND f.looks_like_fiction=0
    """, conn)
    keep = set(base["wildchat_name"])
    df = df[df["wildchat_name"].isin(keep)].copy()
    df["prefix"] = df["text"].map(norm_prefix)

    # Template cluster = prefix key appearing in >= TEMPLATE_MIN_CONV distinct conversations
    conv_per_prefix = df.groupby("prefix")["conv_id"].nunique()
    template_prefixes = set(conv_per_prefix[conv_per_prefix >= TEMPLATE_MIN_CONV].index)
    template_prefixes.discard("")
    df["is_template"] = df["prefix"].isin(template_prefixes).astype(int)

    # Top-20 clusters with a 100-char preview
    top = (conv_per_prefix[conv_per_prefix.index.isin(template_prefixes)]
           .sort_values(ascending=False).head(20))
    preview_rows = []
    for pref, n_conv in top.items():
        example = df[df["prefix"] == pref]["text"].iloc[0]
        preview_rows.append({"n_conversations": int(n_conv),
                             "preview_100char": example[:100].replace("\n", " ")})
    clusters = pd.DataFrame(preview_rows)
    clusters.to_csv(OUT / "template_clusters_top20.csv", index=False)

    # Midjourney sanity check
    midjourney_caught = df[df["text"].str.contains("adhere to the structure", case=False, na=False)]
    mj_templated = int(midjourney_caught["is_template"].sum()) if len(midjourney_caught) else 0

    # C1: please by template vs freehand, per country + overall
    def rate_split(g):
        tmpl = g[g["is_template"] == 1]
        free = g[g["is_template"] == 0]
        return pd.Series({
            "n_turns": len(g),
            "share_template": round(100 * len(tmpl) / len(g), 2) if len(g) else 0,
            "please_template": round(100 * tmpl["has_please"].mean(), 2) if len(tmpl) else None,
            "please_freehand": round(100 * free["has_please"].mean(), 2) if len(free) else None,
        })
    by_country = df.groupby("wildchat_name").apply(rate_split, include_groups=False).reset_index()
    overall = rate_split(df).to_frame().T
    overall.insert(0, "wildchat_name", "OVERALL")
    c1 = pd.concat([overall, by_country.sort_values("please_freehand", ascending=False)], ignore_index=True)
    c1.to_csv(OUT / "please_by_template_by_country.csv", index=False)

    # C2: please by turn position (first vs later), per country + overall
    df["position"] = np.where(df["turn_index"] == 0, "first", "later")
    def pos_split(g):
        first = g[g["position"] == "first"]
        later = g[g["position"] == "later"]
        return pd.Series({
            "n_first": len(first), "n_later": len(later),
            "please_first": round(100 * first["has_please"].mean(), 2) if len(first) else None,
            "please_later": round(100 * later["has_please"].mean(), 2) if len(later) else None,
        })
    by_country_pos = df.groupby("wildchat_name").apply(pos_split, include_groups=False).reset_index()
    overall_pos = pos_split(df).to_frame().T
    overall_pos.insert(0, "wildchat_name", "OVERALL")
    c2 = pd.concat([overall_pos, by_country_pos], ignore_index=True)
    c2.to_csv(OUT / "please_by_position_by_country.csv", index=False)

    return clusters, c1, c2, mj_templated, len(template_prefixes)


def main():
    conn = sqlite3.connect(str(DB))
    cw = load_crosswalk()
    hof, globe, ef = build_external(cw)
    base = please_by_country(conn)
    print(f"[base] {len(base)} countries >= {CONV_FLOOR} conv")

    corr, partials, both = stage_b(conn, base, cw, hof, globe, ef)
    print("[stage B] correlations (all non-fiction please):\n", corr.to_string(index=False))
    print("[stage B] partials:", partials, f"(joined N={len(both)})")

    clusters, c1, c2, mj, n_templates = stage_c(conn, base)
    print(f"[stage C] {n_templates} template clusters; Midjourney templated turns caught: {mj}")

    # Robustness: re-run the H1/H2 correlations on FREEHAND please rate (templates
    # removed), since Stage C shows templates drive the cross-country pattern.
    freehand_base = (c1[c1["wildchat_name"] != "OVERALL"][["wildchat_name", "please_freehand"]]
                     .rename(columns={"please_freehand": "please_rate"}).dropna())
    corr_fh = correlate(freehand_base, cw, {"hof": hof, "globe": globe, "ef": ef},
                        OUT / "correlations_freehand.csv", scatter_tag="_freehand")
    print("[stage B] correlations (FREEHAND please):\n", corr_fh.to_string(index=False))

    # Persist a small run-state for the memo
    import json
    (OUT / "stage5_stats.json").write_text(json.dumps({
        "conv_floor": CONV_FLOOR, "template_min_conv": TEMPLATE_MIN_CONV,
        "prefix_len": PREFIX_LEN, "n_countries": len(base),
        "n_template_clusters": int(n_templates),
        "midjourney_templated_turns": int(mj),
        "partials": {k: {"rho": v[0], "n": v[1]} for k, v in partials.items()},
    }, indent=2))
    conn.close()
    print("Stage 5 done.")


if __name__ == "__main__":
    main()

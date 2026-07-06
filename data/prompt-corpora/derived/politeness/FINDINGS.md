# Findings — politeness angle hypothesis tests

_Evidence, not a verdict. Numbers only; the editorial side interprets. All rates are per user turn on the non-fiction cut, WildChat, countries with ≥ 500 conversations (N = 29). Thresholds and sources in `SOURCES.md`._

---

## Headline: the East Asia "please" cluster is mostly one circulated template

The single most important result. On **freehand turns only** (template pastes removed), the East Asia cluster collapses toward Western levels:

| Country | please, all turns | please, **freehand only** | share of turns that are template |
|---|---:|---:|---:|
| Taiwan | 74.4% | **6.4%** | 76.8% |
| China | 54.3% | **8.3%** | 51.3% |
| Hong Kong | 46.0% | **11.6%** | 40.0% |
| Singapore | 41.2% | **9.7%** | 35.7% |
| Japan | 53.9% | **15.9%** | 47.2% |
| United States | 12.7% | 6.0% | 9.0% |
| United Kingdom | 7.6% | 6.4% | 4.6% |

**Answer to the brief's key question — does the cluster survive on freehand turns? No.** Taiwan's 74% falls to 6.4%, statistically indistinguishable from the US (6.0%) and UK (6.4%). The cluster is **template circulation, not manners.** The driver is a single mass-reused prompt — the Midjourney prompt-generator template ("As a prompt generator for a generative AI called Midjourney… **Please** adhere to the structure and formatting below"), which contains one "please", was pasted as an opening turn in tens of thousands of conversations, and is heavily concentrated in Taiwan, China, Hong Kong and Singapore. It accounts for 16,775 turns — the largest template cluster by an order of magnitude.

Japan is the partial exception: it retains the highest freehand please rate (15.9%), roughly 2–3× Western levels, so a smaller genuine-politeness residual there is not ruled out.

**Turn-position corroborates.** Please in the *first* user turn vs *later* turns: Taiwan 84.5% → 7.4%, China 77.8% → 6.2%, Singapore 64.5% → 6.0%. The politeness is front-loaded onto the opening turn (where the template is pasted) and vanishes in working turns. US: 18.2% → 5.0%.

---

## H1 (culture) and H2 (English proficiency): no index predicts please-rate

Spearman correlations of each external index against per-country please-rate. Two panels: all non-fiction turns, and freehand only (the honest test, since templates drive the all-turns number).

**All non-fiction turns:**

| Index | rho | p | N | rho excl. East Asia |
|---|---:|---:|---:|---:|
| Hofstede power distance | 0.06 | 0.77 | 27 | −0.12 |
| Hofstede individualism | −0.36 | 0.065 | 27 | −0.02 |
| GLOBE humane orientation | −0.07 | 0.76 | 23 | −0.04 |
| GLOBE assertiveness | 0.22 | 0.31 | 23 | 0.55 |
| EF English proficiency | −0.03 | 0.90 | 21 | 0.23 |

**Freehand only:**

| Index | rho | p | N | rho excl. East Asia |
|---|---:|---:|---:|---:|
| Hofstede power distance | −0.15 | 0.46 | 27 | −0.27 |
| Hofstede individualism | −0.20 | 0.33 | 27 | 0.03 |
| GLOBE humane orientation | −0.11 | 0.62 | 23 | −0.03 |
| GLOBE assertiveness | 0.30 | 0.16 | 23 | 0.45 |
| EF English proficiency | −0.07 | 0.77 | 21 | 0.10 |

One sentence per index:

- **Power distance (H1):** no relationship in either panel (p ≥ 0.46). Cultural deference, as Hofstede measures it, does not track please-rate.
- **Individualism (H1):** the only index reaching marginal significance (rho −0.36, p 0.065) on all turns — but it drops to −0.02 once the five East Asia countries are removed, and to −0.20 (n.s.) on the freehand cut. Whatever signal exists is entirely the East Asia bloc, and that bloc is the template artifact above.
- **GLOBE humane orientation (H1):** no relationship (p ≥ 0.62).
- **GLOBE assertiveness (H1):** positive but not significant (p 0.16–0.31); the excl-East-Asia rho (0.45–0.55) is larger but rests on 18 countries and is not significance-tested — noted, not claimed.
- **EF English proficiency (H2):** no relationship (rho −0.03 to −0.07, p ≥ 0.77). English proficiency does not predict please-rate. Note H2 is structurally hobbled: EF excludes native-English countries and Taiwan, so the test runs over 21 non-native countries only.

**Rank partials** (disentangling H1 from H2 among the 19 countries with both power-distance and EF scores): EF controlling for power distance rho = −0.19; power distance controlling for EF rho = −0.15. Neither survives as a driver. (N = 19 met the ≥ 15 threshold.)

---

## Template clusters (top of the list)

98 template clusters detected (normalised 200-char prefix in ≥ 20 distinct conversations). The largest by conversation count:

| conversations | preview (100 char) |
|---:|---|
| 16,775 | `As a prompt generator for a generative AI called "Midjourne…` |
| 713 | `Hi` |
| 329 | `Hello` |
| 171 | `CONSTRAINTS: 1. ~100k word limit for short term memory…` (Auto-GPT scaffold) |
| 155 | `CONSTRAINTS: 1. ~4000 word limit…` (Auto-GPT scaffold) |
| 127 | `continue` |

Full top-20 in `template_clusters_top20.csv`. The Midjourney template dwarfs everything and is the please-bearing one; the rest are short recurrent messages (Hi, continue, More, Thanks) or agent scaffolds that mostly carry no "please".

---

## Caveats and things to flag

- **The 74% was too good to be true — and now we know why.** It was a template-paste rate wearing the costume of a manners statistic. Any article built on "East Asians are polite to machines" would be building on a Midjourney prompt's single "please".
- **Template bucket is broad by the brief's definition.** "≥ 20 distinct conversations" catches both the circulated Midjourney prompt *and* trivial recurrent messages ("Hi", "continue"). The trivial ones carry no "please", so if anything the freehand please rates are slightly *over*-stated (removing zero-please short messages from the freehand denominator raises it) — the East Asia collapse is a conservative floor.
- **Small-N power.** 21–27 countries. Only large effects are detectable; the many non-significant results are weak evidence of absence, not proof of no effect. Do not language-inflate the marginal individualism or excl-East-Asia assertiveness numbers.
- **Unjoinable countries.** GLOBE-null: Pakistan, Vietnam, Romania, Jamaica, Saudi Arabia, Estonia. EF-null: Taiwan + the seven native/official-English countries (US, UK, Canada, Australia, NZ, Jamaica, Singapore). Hofstede covers all 29.
- **Japan residual.** Japan's freehand please (15.9%) and Hong Kong's (11.6%) stay above Western levels; a smaller genuine effect there is not excluded and is the only part of the original cluster that survives scrutiny.
- **Country = hashed-IP geolocation**, not user nationality; diaspora and VPN effects unquantified.

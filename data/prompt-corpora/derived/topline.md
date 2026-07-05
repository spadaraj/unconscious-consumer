# Topline — prompt corpora, ten striking numbers

> **Correction pass (2026-07-05).** This is the cleaned re-run. Two changes vs the original pass:
> 1. **31 assistant-mislabelled turns removed** at ingest (WildChat's `🤖`-prefix ghost turns + five canonical assistant openers). Total user turns: 405,483 → 405,452.
> 2. **`looks_like_fiction` flag added** — 1.28% of turns flag as fiction/roleplay overall; 2.27% in WildChat, 0.20% in LMSYS. Every politeness and delegation aggregate now ships in two cuts: all turns, and non-fiction only.
>
> **What moved materially:** thanks and apology rates dropped on the non-fiction cut (fiction was overweighting them); please barely moved; the East Asia politeness cluster **holds strongly on the non-fiction cut**. Details in the findings below.


_Working draft. Plain-language read of the ten most striking numbers, with caveats flagged. All %s are per user turn unless noted. Monthly trends are WildChat only — LMSYS has no per-row timestamp._

---

**1. Prompts are ≈ 3.8× longer than search queries at the median.** Median prompt is 17 words vs 6 for MS MARCO and 3 for ORCAS. Unchanged from the original pass. This is the structural gap that Angle 1 ("translation tax") is arguing about.

**2. Role assignment is a stable ~1.1–2.6% of WildChat turns across every month sampled.** Unchanged from the original pass. No visible growth or collapse in the folk-prompt-engineering habit over the ~13 months of coverage.

**3. Explicit template structure (three or more of '###' / 'Step N' / 'Format:' / 'Output:' / numbered constraints) appears in only 0.00–0.04% of monthly turns.** Overtly templated prompts are a very small subculture in naturalistic use — the folk-engineering aesthetic doesn't translate to real ChatGPT sessions the way Twitter posts about it might suggest.

**4. "Please" barely moves after the fiction cut.** All turns: 10.99% overall, 14.67% WildChat vs 6.98% LMSYS. **Non-fiction only:** 10.76% overall, 14.34% WildChat vs 6.94% LMSYS. The WildChat-vs-LMSYS gap survives — this is the manners-in-the-wild vs manners-in-the-lab story, unchanged from the original pass. **Thanks and apology drop harder** on the non-fiction cut (fiction was overweighting them — see CORRECTION_NOTES).

**5. East Asia politeness cluster holds on the clean cut.** All turns, top three by 'please' rate = Taiwan (74.4%), China (54.3%), Japan (53.9%); bottom three = New Zealand (2.5%), Russia (4.1%), India (4.3%). **Non-fiction only** top three = Taiwan (74.4%), China (54.4%), Japan (53.9%). The absolute rates barely move because fiction is only ~1% of these countries' turns; the cluster is a real user-behaviour signal, not a fiction artefact. 137 countries suppressed (< 500 conv).

**6. Requests for a decision outrun requests for options by 4.2× in this data** — 0.53% of turns ask for a decision vs 0.13% asking for options. **Read with caution:** the decision regex includes broad phrases ("decide", "what should I do") while the options regex requires specific "give me N options / ideas / versions" phrasing, so this ratio partly reflects regex scope, not user behaviour. Regex rebuild is a later pass; keep this metric caveated.

**7. Explicit pre-purchase deliberation is rare in these corpora: 0.14% of turns.** That's a floor; the regex is deliberately narrow ("should I buy", "worth it", "best X under"). Angle 4 will need broader signals to build volume.

**8. Mean 2.03 user turns per conversation; 2.7% of conversations contain an explicit retry marker; 2.1% end on one (abandonment proxy).** The iteration-tax article should lead with mean-turns first, not retry percentages — the retry-marker regex catches only overt corrections.

**9. Top imperative verbs:** write (31,003), give (10,407), make (5,465), create (5,103), name (4,565). "Write" dominates by an order of magnitude; the top ten together cover a majority of imperative-lead turns. Angle 3 has a clean anchor.

**10. LMSYS-Chat-1M has no per-row timestamp** in its streaming schema (checked at ingest). Every monthly trend chart above is WildChat only. Any story that leans on "how prompts changed month over month" must either (a) accept the WildChat-only scope, or (b) find a different corpus for trend data.


---

## Flags — things that might look too good to be true

- **Fiction flag under-catches.** `looks_like_fiction` fires at 1.28% overall, but a coarser proxy (any Name-colon dialogue, DDLC character names, parentheticals) suggests real user-authored roleplay is closer to ~5-10% of user turns in WildChat. The flag is a floor, not a ceiling — a stricter detector is a later pass. See CORRECTION_NOTES.

- **Purchase deliberation prevalence.** Very low. The regex is narrow by design; do not read this as "users don't use ChatGPT for purchases." Real prevalence is unknowable without a hand-labelled sample.

- **Retry marker rate.** Only catches overt English retry language. Silent restarts (new conversation, deleted message) are invisible in this data.

- **Country-level cuts.** Country is WildChat's hashed-IP geolocation, not user-declared. Diaspora effects can distort the politeness cross-tab.

- **Politeness "ty".** The regex includes 'ty' as a thanks token; risk of false positives with initialisms. Flagged for the next validation pass.


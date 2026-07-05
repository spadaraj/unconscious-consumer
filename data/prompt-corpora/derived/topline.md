# Topline — prompt corpora, ten striking numbers

_Working draft from Stage 3 aggregates. Plain-language read of the ten most striking numbers, with caveats flagged. All %s are per user turn unless noted. Monthly trends are WildChat only — LMSYS has no per-row timestamp._

---

**1. Prompts are ≈ 3.8× longer than search queries at the median.** Median prompt is 17 words vs 6 for MS MARCO and 3 for ORCAS. This is the structural gap that Angle 1 ("translation tax") is arguing about.

**2. Role assignment is a stable ~1.1–2.6% of WildChat turns across every month sampled.** No visible growth or collapse in the folk-prompt-engineering habit over the ~13 months of coverage.

**3. Explicit template structure (three or more of '###' / 'Step N' / 'Format:' / 'Output:' / numbered constraints) appears in only 0.00–0.04% of monthly turns.** Overtly templated prompts are a very small subculture in naturalistic use — the folk-engineering aesthetic doesn't translate to real ChatGPT sessions the way Twitter posts about it might suggest.

**4. "Please" appears in 11.0% of user turns overall — 14.7% in WildChat vs 7.0% in LMSYS.** WildChat is a naturalistic ChatGPT deployment; LMSYS is Chatbot Arena (users know they are testing models). The gap is the manners-in-the-wild vs manners-in-the-lab story.

**5. Country-level politeness spread (WildChat, ≥ 500 conv):** top three by 'please' rate = Taiwan (74.4%), China (54.3%), Japan (53.9%); bottom three = New Zealand (2.5%), Russia (4.1%), India (4.3%). 137 countries suppressed (< 500 conv).

**6. Requests for a decision outrun requests for options by 4.2× in this data** — 0.53% of turns ask for a decision vs 0.13% asking for options. **Read with caution:** the decision regex includes broad phrases ("decide", "what should I do") while the options regex requires specific "give me N options / ideas / versions" phrasing, so this ratio partly reflects regex scope, not user behaviour. Angle 3's cleaner metric will come after the Stage 4 validation pass.

**7. Explicit pre-purchase deliberation is rare in these corpora: 0.14% of turns.** That's a floor; the regex is deliberately narrow ("should I buy", "worth it", "best X under"). Angle 4 will need broader signals to build volume.

**8. Mean 2.03 user turns per conversation; 2.7% of conversations contain an explicit retry marker; 2.1% end on one (abandonment proxy).** The iteration-tax article should lead with mean-turns first, not retry percentages — the retry-marker regex catches only overt corrections.

**9. Top imperative verbs:** write (31,003), give (10,407), make (5,465), create (5,103), name (4,565). "Write" dominates by an order of magnitude; the top ten together cover a majority of imperative-lead turns. Angle 3 has a clean anchor.

**10. LMSYS-Chat-1M has no per-row timestamp** in its streaming schema (checked at ingest). Every monthly trend chart above is WildChat only. Any story that leans on "how prompts changed month over month" must either (a) accept the WildChat-only scope, or (b) find a different corpus for trend data.


---

## Flags — things that might look too good to be true

- **Purchase deliberation prevalence (0.x%).** Very low. The regex is narrow by design; do not read this as "users don't use ChatGPT for purchases." Read it as "this pattern of purchase-y language appears in this share of turns." Real prevalence is unknowable without a hand-labelled sample — Stage 4's job.

- **Retry marker rate.** Only catches overt English retry language. Silent restarts (new conversation, deleted message) are invisible in this data.

- **Country-level cuts.** Country is WildChat's hashed-IP geolocation, not user-declared. Diaspora effects (English prompts from a non-English majority country) can distort the politeness cross-tab.

- **Politeness "ty".** The regex includes 'ty' as a thanks token; risk of false positives with initialisms. Flag for the Stage 4 validation pass.

- **Scaffolding trend flatness (finding #2).** If validation reveals the role-assignment regex has high false-positive rate on generic 'you are' phrasing, the flatness could be a measurement artefact.


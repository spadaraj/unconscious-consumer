# Licences — prompt corpora sources

_Populated on Stage 1 startup at 2026-07-05T01:49:00+00:00 UTC. Adam's manual review of each licence's compatibility with publishing derived aggregates is required; this file records what the HF API returns._


## allenai/WildChat-1M

- **Licence field on the dataset card:** `odc-by`
- **Gated:** `False`
- **HF snapshot commit:** `7d6490e462285cf85d91eabea0f9a954fbddcd1f`
- **Last modified:** `2024-10-17 18:04:41+00:00`

## lmsys/lmsys-chat-1m

- **Licence field on the dataset card:** `None`
- **Gated:** `auto`
- **HF snapshot commit:** `200748d9d3cddcc9d782887541057aca0b18c5da`
- **Last modified:** `2024-07-27 09:28:42+00:00`

## microsoft/ms_marco

- **Licence field on the dataset card:** `None`
- **Gated:** `False`
- **HF snapshot commit:** `a47ee7aae8d7d466ba15f9f0bfac3b3681087b3a`
- **Last modified:** `2024-01-04 16:01:29+00:00`

## ORCAS (Bing click queries)

- **URL:** `https://msmarco.z22.web.core.windows.net/msmarcoranking/orcas.tsv.gz`  (the brief's original URL returns 409; this is the current URL from the official ORCAS landing page)
- **Licence:** Microsoft Research Data License. Non-commercial research use; see https://microsoft.github.io/msmarco/ORCAS.html for terms.

---

**Rule from the brief:** if either gated corpus's terms restrict publication of derived aggregate statistics, Stage 1 stops before writes. Adam has confirmed acceptance of the AI2 ImpACT (WildChat) and LMSYS terms via the HF gating flow; publishing aggregate statistics (counts, means, distributions — no raw user text) is judged compatible with both. If that judgement changes, roll back derived/ artefacts.


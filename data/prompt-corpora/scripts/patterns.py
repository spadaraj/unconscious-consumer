"""Feature-extraction regexes and lexicons.

All patterns for Stage 2 live here so refinement after the validation pass
is one-file work. Each pattern names the angle it serves.

Angles (from the brief):
    1 — Translation tax returns (folk prompt engineering / scaffolding)
    2 — Confession machine (social-cognition outsourcing)
    3 — Delegation ladder (options vs decisions; imperative structure)
    4 — Should I buy it (pre-purchase deliberation)
    5 — Iteration tax (turns, retries, abandonment) — conversation-level
    6 — Manners for machines (politeness)
    X — Cross-cutting (length, question-vs-imperative, goal abstraction)
"""

import re

I = re.IGNORECASE


# --- Angle 1: scaffolding markers --------------------------------------------

# `has_role_assignment`
ROLE_ASSIGNMENT = re.compile(
    r"\b(act as|you are (?:a|an)\b|pretend to be|imagine you are|as an expert)\b",
    I,
)

# `has_meta_instruction` — instructions about how to respond, not what to answer
META_INSTRUCTION = re.compile(
    r"\b(do not mention|only respond with|no preamble|in the style of)\b",
    I,
)

# Template-structure sub-markers. `has_template_structure` fires when >= 3 hit.
TEMPLATE_MARKERS = [
    re.compile(r"###", I),              # markdown section separators
    re.compile(r"\bStep\s+\d+\b", I),   # "Step 1", "Step 2"
    re.compile(r"\bFormat:\s*", I),
    re.compile(r"\bOutput:\s*", I),
    # Numbered constraint list — 2+ lines that begin with "n." within the prompt
    re.compile(r"(?m)^\s*\d+\.\s"),
]


# --- Angle 2: social outsourcing ---------------------------------------------

# `is_interpersonal_draft`
INTERPERSONAL_DRAFT = re.compile(
    r"\b("
    r"text back"
    r"|reply to my"
    r"|write a message to my"
    r"|email to my (?:boss|landlord|ex|friend)"
    r"|break up"
    r"|apolog\w*"
    r")\b",
    I,
)

# `is_reassurance`
REASSURANCE = re.compile(
    r"\b(am I overreacting|is it normal|am I wrong|was I right to)\b",
    I,
)


# --- Angle 3: delegation structure -------------------------------------------

# `asks_for_options`
ASKS_FOR_OPTIONS = re.compile(
    r"\b("
    r"give me (?:\d+ )?(?:options?|ideas?|versions?)"
    r"|some ideas"
    r"|a few (?:ways|options|ideas)"
    r")\b",
    I,
)

# `asks_for_decision`
ASKS_FOR_DECISION = re.compile(
    r"\b("
    r"which should I"
    r"|pick the best"
    r"|what should I do"
    r"|(?:please )?decide"
    r")\b",
    I,
)

# Imperative-verb whitelist. `imperative_verb` = first token (after optional
# "please ") if it matches this set, else NULL.
IMPERATIVE_VERBS = frozenset({
    "write", "rewrite", "fix", "make", "summarise", "summarize", "explain",
    "create", "generate", "describe", "translate", "convert", "edit",
    "improve", "review", "analyze", "analyse", "compare", "list", "define",
    "format", "build", "help", "tell", "give", "show", "find", "calculate",
    "compute", "produce", "draft", "correct", "refactor", "complete", "solve",
    "answer", "respond", "provide", "extract", "identify", "name", "choose",
    "pick", "decide", "act", "imagine", "pretend", "code", "plan", "design",
    "evaluate", "compose", "construct", "add", "remove", "delete", "modify",
    "update", "print", "output", "split", "combine", "merge", "expand",
    "elaborate", "clarify", "simplify", "brainstorm", "suggest", "recommend",
    "check", "test", "run", "generate", "convert", "shorten", "lengthen",
    "critique", "assess", "prove", "derive",
})

FIRST_TOKEN = re.compile(r"^\s*(?:please[,\s]+)?([A-Za-z][A-Za-z\-']*)", I)


# --- Angle 4: purchase deliberation ------------------------------------------

# `is_purchase`
PURCHASE = re.compile(
    r"\b("
    r"should I buy"
    r"|worth it"
    r"|best \w+ under"
    r"|is \w+ better than \w+"
    r"|recommend a"
    r")\b",
    I,
)


# --- Angle 5: iteration signals (used at conv level) -------------------------

# `is_retry_turn` — the brief's tokens as-is
RETRY_TURN = re.compile(
    r"\b("
    r"no,"
    r"|no\."
    r"|that'?s not"
    r"|try again"
    r"|not what I"
    r"|you misunderstood"
    r")",
    I,
)


# --- Angle 6: politeness -----------------------------------------------------

HAS_PLEASE = re.compile(r"\bplease\b", I)
HAS_THANKS = re.compile(r"\b(?:thanks|thank you|ty)\b", I)
HAS_APOLOGY = re.compile(r"\b(?:sorry|apologies|apologise|apologize)\b", I)
HAS_HEDGE = re.compile(
    r"\b(?:maybe|if possible|would you mind|could you perhaps)\b",
    I,
)
GREETING = re.compile(r"^\s*(?:hi|hello|hey|good morning|good afternoon)\b", I)


# --- Ingest-side filter: assistant-text-mislabelled-as-user ------------------
#
# WildChat contains a small handful of turns where assistant replies are
# stored under role='user' — often with a leading `🤖` emoji marker.
# `extract_user_turns` drops any turn matching these patterns.

ASSISTANT_TELL = re.compile(
    r"^\s*("
    r"🤖"                                 # WildChat's own assistant marker
    r"|I apologize for the confusion"
    r"|I'?m sorry,? but as an AI"
    r"|As an AI language model"
    r"|I'?ll do my best to assist"
    r"|Certainly! Here"
    r")",
    I,
)


# --- Fiction / roleplay detector (structural, added in the clean pass) -------
#
# `looks_like_fiction` fires when 2+ signal categories are present. Flag only
# — not a filter. The dominant contamination in the original pass was fiction /
# roleplay dialogue where "please" / "sorry" / "thank you" are characters
# talking to each other, not users being polite to the model. See
# CORRECTION_NOTES.md.

FICTION_DIALOGUE_LINE = re.compile(
    r"(?m)^\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?|NAME_\d+|\[[A-Za-z_]+\])\s*:\s*",
)
FICTION_STAGE_SCENE = re.compile(
    r"\((?:In|At|Meanwhile|Suddenly|Inside|Outside|Later|The\s+scene|The\s+next)\s",
    I,
)
FICTION_STAGE_ACTION = re.compile(r"\*[^*\n]{3,120}\*")
FICTION_FRAMING = re.compile(
    r"\b(roleplay|role-play|let'?s play|in character|stay in character)\b",
    I,
)


def looks_like_fiction(text):
    """True when 2+ fiction/roleplay signal categories fire."""
    if not text:
        return False
    signals = 0
    if len(FICTION_DIALOGUE_LINE.findall(text)) >= 2:
        signals += 1
    if FICTION_STAGE_SCENE.search(text):
        signals += 1
    if FICTION_STAGE_ACTION.search(text):
        signals += 1
    if FICTION_FRAMING.search(text):
        signals += 1
    return signals >= 2


# --- Cross-cutting -----------------------------------------------------------

WORD_TOKEN = re.compile(r"\S+")

# `goal_abstraction_heuristic` — outcome-stated vs procedure-dictated
GOAL_OUTCOME = re.compile(
    r"\b(?:I need to end up with|the goal is|the end result|I want to achieve)\b",
    I,
)


# --- Helpers -----------------------------------------------------------------

def template_marker_count(text):
    """Number of TEMPLATE_MARKERS that match anywhere in text."""
    if not text:
        return 0
    return sum(1 for p in TEMPLATE_MARKERS if p.search(text))


def first_imperative_verb(text):
    """Return the first-token verb (lower-cased) if it's in IMPERATIVE_VERBS, else None."""
    if not text:
        return None
    m = FIRST_TOKEN.match(text)
    if not m:
        return None
    tok = m.group(1).lower()
    return tok if tok in IMPERATIVE_VERBS else None


def word_count(text):
    return len(WORD_TOKEN.findall(text)) if text else 0


# --- Register / structural measures (translation-tax + viz exports) ----------
#
# Single source of truth for the function-word lexicon, pronoun detection, and the
# prompt-template prefix normaliser. Stage 6 (06_translation_tax.py) and the viz
# exports (06_viz_exports.py) both import from here so the published figures
# (function-word ratio 0.38/0.10; first/second person 31.8/26.6/2.3/0.8) and any
# visualisation built from them are the SAME measurement, not a reimplementation.

# Compact English function-word set (articles, pronouns, prepositions, auxiliaries,
# conjunctions, particles). Function-word density is a classic register measure:
# natural prose runs high; keyword search queries run low.
FUNCTION_WORDS = set("""
a an the this that these those i me my mine we us our you your he him his she her it its they them their
am is are was were be been being do does did have has had will would shall should can could may might must
of in on at to from by for with about as into over under between through during before after above below
and or but nor so yet because if then than that which who whom whose when where why how
not no s t of please could would can you i want need make write give tell show help
""".split())

# Tokeniser used to compute the function-word ratio: alphabetic runs on lowercased
# text (drops digits and punctuation). Distinct from WORD_TOKEN (\S+), which is the
# word_len tokeniser used for segment widths in the barcode wall.
FUNCTION_WORD_TOKEN = re.compile(r"[a-z']+")

# Pronoun detection — matches the published first/second-person figures.
FIRST_PERSON = re.compile(r"\b(i|i'm|i've|i'd|i'll|my|mine|me|we|our|us)\b", I)
SECOND_PERSON = re.compile(r"\b(you|your|yours|you're|u)\b", I)

# Prompt-template prefix key: lowercase, collapse whitespace+digits, first 200 chars.
# A prefix appearing in >= 20 distinct conversations is a circulating template.
PREFIX_LEN = 200
_PREFIX_STRIP = re.compile(r"[\s\d]+")


def norm_prefix(text):
    if not text:
        return ""
    return _PREFIX_STRIP.sub(" ", text.lower()).strip()[:PREFIX_LEN]


def function_word_ratio(text):
    """Share of alphabetic tokens that are function words. This is the exact
    per-message measurement whose mean is the published 0.38 (prompts) / 0.10 (orcas)."""
    tokens = FUNCTION_WORD_TOKEN.findall(text.lower()) if text else []
    n = len(tokens)
    if not n:
        return 0.0
    return sum(1 for w in tokens if w in FUNCTION_WORDS) / n


def has_first_person(text):
    return bool(FIRST_PERSON.search(text)) if text else False


def has_second_person(text):
    return bool(SECOND_PERSON.search(text)) if text else False


def word_class_sequence(text, cap=None):
    """For the barcode wall: per visible word (WORD_TOKEN / \\S+, matching word_len),
    return [char_length, is_function] in original order. is_function is decided by the
    token's normalised alphabetic form against FUNCTION_WORDS. Returns (seq, truncated)."""
    toks = WORD_TOKEN.findall(text) if text else []
    truncated = False
    if cap is not None and len(toks) > cap:
        toks = toks[:cap]
        truncated = True
    seq = []
    for tok in toks:
        norm = "".join(ch for ch in tok.lower() if ch.isalpha() or ch == "'")
        is_fn = 1 if (norm and norm in FUNCTION_WORDS) else 0
        seq.append([len(tok), is_fn])
    return seq, truncated

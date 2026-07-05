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

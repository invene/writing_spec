"""Closed vocabularies for ITWS rule metadata and profile identity.

Every value below is closed. The parser rejects an unknown value, so a
misspelled facet fails the build instead of silently disappearing from a
search result.

Two groups of fields exist:

``NORMATIVE_FIELDS``
    Fields that record a condition the rule's own normative statement already
    states. ``constructs`` is the only such field: §1.4 item 3 makes construct
    presence part of applicability.

``NAVIGATION_FIELDS``
    Fields that help an agent find a rule. They never narrow the profile
    envelope. §1.6 states this separation normatively.
"""

from __future__ import annotations

PROFILE_IDS: tuple[str, ...] = (
    "design-rfc",
    "decision-record",
    "procedure",
    "explanation",
    "incident",
    "technical-report",
    "research-paper",
    "investigation-log",
    "epic",
    "task",
    "subtask",
    "maintenance-comment",
)

PROFILE_LABELS: dict[str, str] = {
    "design-rfc": "Design / RFC",
    "decision-record": "Architecture decision record",
    "procedure": "Runbook / how-to",
    "explanation": "Concept / explanation",
    "incident": "Incident report / postmortem",
    "technical-report": "Technical report",
    "research-paper": "Research paper",
    "investigation-log": "Investigation log",
    "epic": "Epic",
    "task": "Task",
    "subtask": "Subtask",
    "maintenance-comment": "Maintenance comment set",
}

#: §0.2.1 governed surfaces. A profile governs exactly one surface form.
SURFACES: tuple[str, ...] = ("markdown-document", "hosted-comment-set")

PROFILE_SURFACES: dict[str, str] = {
    "design-rfc": "markdown-document",
    "decision-record": "markdown-document",
    "procedure": "markdown-document",
    "explanation": "markdown-document",
    "incident": "markdown-document",
    "technical-report": "markdown-document",
    "research-paper": "markdown-document",
    "investigation-log": "markdown-document",
    "epic": "markdown-document",
    "task": "markdown-document",
    "subtask": "markdown-document",
    "maintenance-comment": "hosted-comment-set",
}

#: Host languages with a registered §4.13 adapter. The list is closed: a
#: change set naming an unregistered adapter is `blocked`, never guessed at.
HOST_ADAPTERS: tuple[str, ...] = ("python",)

#: Closed §4.13 comment purposes. A governed comment record declares one.
COMMENT_PURPOSES: tuple[str, ...] = (
    "rationale",
    "invariant",
    "caution",
    "history",
    "reference",
    "marker",
)

#: Closed §4.13 comment lifecycles.
COMMENT_LIFECYCLES: tuple[str, ...] = ("durable", "temporary")

#: Closed §8.7 comment provenance values. Tooling never infers these from
#: prose style; a record states them or the comment is not governed.
COMMENT_PROVENANCES: tuple[str, ...] = ("human-authored", "ai-proposed")

#: Closed §8.7 human dispositions for one comment proposal record.
PROPOSAL_DISPOSITIONS: tuple[str, ...] = (
    "pending",
    "accepted",
    "revised",
    "rejected",
)

#: Change classifications the extractor assigns to one governed comment.
COMMENT_CHANGES: tuple[str, ...] = ("added", "modified", "removed")

# Profile families back the shared overlay modules in spec/overlays/shared/.
# §1.5.2 assigns a multi-profile rule to the module of its family.
PROFILE_FAMILIES: dict[str, tuple[str, ...]] = {
    "work-item": ("epic", "task", "subtask"),
    "report": ("technical-report", "research-paper"),
}

TIERS: tuple[str, ...] = ("core", "reviewed", "publication")

MINIMUM_TIER: dict[str, str] = {
    "design-rfc": "reviewed",
    "decision-record": "core",
    "procedure": "reviewed",
    "explanation": "core",
    "incident": "reviewed",
    "technical-report": "reviewed",
    "research-paper": "publication",
    "investigation-log": "core",
    "epic": "reviewed",
    "task": "core",
    "subtask": "core",
    "maintenance-comment": "core",
}

RULE_CLASSES: tuple[str, ...] = ("mandatory", "recommended", "permitted")

MACHINE_CHECKABILITY: tuple[str, ...] = ("yes", "partial", "no")

RULE_STATUSES: tuple[str, ...] = ("active", "deprecated")

#: §4.1 chunk purposes. ``any`` means the rule does not depend on the purpose.
CHUNK_TYPES: tuple[str, ...] = (
    "any",
    "context",
    "definition",
    "requirement",
    "claim",
    "decision",
    "mechanism",
    "procedure",
    "evidence",
    "interpretation",
    "risk",
    "limitation",
)

#: The unit a rule judges. A rule names exactly one target.
TARGETS: tuple[str, ...] = (
    "document",
    "collection",
    "section",
    "heading",
    "chunk",
    "sentence",
    "list",
    "word",
    "term",
    "symbol",
    "equation",
    "citation",
    "figure",
    "table",
    "bounded-block",
    "procedure-step",
    "declaration",
    "conformance-record",
    "comment",
    "comment-set",
)

#: Which of §1.2's two layers the rule governs.
LAYERS: tuple[str, ...] = ("exact", "plain", "both")

#: How much of the document a reviewer must hold to decide the rule.
CONTEXT_SCOPES: tuple[str, ...] = (
    "local",
    "neighboring",
    "section",
    "document",
    "collection",
)

#: What a repair may attempt. ``prohibited`` marks content an agent may not
#: mutate on its own authority.
REWRITE_GUIDANCE: tuple[str, ...] = (
    "mechanical",
    "candidate",
    "review",
    "prohibited",
)

#: Construct conditions. ``any`` means the rule has no construct gate beyond
#: the presence of governed prose.
CONSTRUCTS: tuple[str, ...] = (
    "any",
    "acronym",
    "admitted-term",
    "analogy",
    "bounded-block",
    "caveat",
    "citation",
    "claim",
    "comment",
    "comparison",
    "connective",
    "cross-reference",
    "declaration",
    "definition",
    "diagram",
    "domain-term",
    "equation",
    "figure",
    "generalization",
    "heading",
    "hedge",
    "host-anchor",
    "interface",
    "invariant",
    "limitation",
    "list",
    "marker",
    "measurement",
    "name",
    "noun-cluster",
    "number",
    "observation",
    "parent-link",
    "procedure-step",
    "prohibited-phrase",
    "pronoun",
    "proposal-record",
    "quantity",
    "removal-condition",
    "requirement",
    "risk",
    "section",
    "speculation",
    "statistic",
    "symbol",
    "table",
    "title",
    "tool-artifact",
    "user-journey",
    "verb",
    "waiver",
    "warning",
    "word",
    "worked-example",
)

#: Ledgers and text surfaces a rule reads or writes. An agent uses these to
#: detect two work slices that would collide.
RESOURCES: tuple[str, ...] = (
    "none",
    "chunk-text",
    "heading",
    "declaration-block",
    "term-ledger",
    "symbol-ledger",
    "exact-item-ledger",
    "claim-ledger",
    "evidence-ledger",
    "cross-reference-ledger",
    "skeleton-order",
    "figure-ledger",
    "citation-ledger",
    "conformance-record",
    "waiver-record",
    "comment-text",
    "host-anchor-ledger",
    "proposal-record",
)

#: Typed edges between rules. ``exemplified-by`` is generated from Annex D and
#: never authored on a rule.
RELATION_TYPES: tuple[str, ...] = (
    "requires",
    "constrains",
    "overrides",
    "pairs-with",
    "validates",
    "exemplified-by",
)

AUTHORED_RELATION_TYPES: tuple[str, ...] = (
    "requires",
    "constrains",
    "overrides",
    "pairs-with",
    "validates",
)

#: §1.4 precedence layers, most decisive first. The compiler emits this order
#: as a machine relation so a tool never re-derives it from prose.
PRECEDENCE_LAYERS: tuple[tuple[int, str, str], ...] = (
    (1, "exactness-and-safety", "Exactness and safety over style."),
    (2, "profile-exception", "Explicit profile exception over its named general rule."),
    (3, "structure-over-sentence", "Structure over sentence."),
    (4, "mandatory-over-recommended", "Mandatory over recommended."),
    (5, "normative-over-notes", "Normative text over notes."),
    (6, "specific-over-general", "Specific over general."),
)

#: Self-check passes of §8.1, keyed by the part that owns the rule.
CHECKLIST_PASSES: dict[str, str] = {
    "2": "Vocabulary",
    "3": "Sentences",
    "4": "Structure and explanation",
    "5": "Technical exactness and evidence",
    "6": "Structure and explanation",
    "7": "Technical exactness and evidence",
}

CHECKLIST_PASS_ORDER: tuple[str, ...] = (
    "Vocabulary",
    "Sentences",
    "Structure and explanation",
    "Technical exactness and evidence",
)

#: Severity that §8.2's map assigns to each rule class.
SEVERITY_BY_CLASS: dict[str, str] = {
    "mandatory": "error",
    "recommended": "warning",
    "permitted": "suggestion",
}

#: States that a record uses instead of inventing an absent value.
UNRESOLVED_STATES: tuple[str, ...] = ("unknown", "not_applicable", "blocked")

#: Confidence an agent may attach to its own semantic judgment.
JUDGMENT_STATES: tuple[str, ...] = (
    "proposed",
    "accepted_for_run",
    "disputed",
    "unresolved",
)

#: Four-state validation outcome of §8.6.
VALIDATION_STATES: tuple[str, ...] = ("pass", "fail", "needs_review", "blocked")

NORMATIVE_FIELDS: tuple[str, ...] = ("profiles", "constructs")

NAVIGATION_FIELDS: tuple[str, ...] = (
    "target",
    "chunk_types",
    "slots",
    "layers",
    "context_scope",
    "rewrite_guidance",
    "reads",
    "writes",
    "relations",
)


def profile_surface(profile: str) -> str:
    """Return the §0.2.1 governed surface that ``profile`` declares."""
    return PROFILE_SURFACES[profile]


def profile_families(profile: str) -> tuple[str, ...]:
    """Return the shared overlay modules that ``profile`` loads."""
    return tuple(
        family
        for family, members in sorted(PROFILE_FAMILIES.items())
        if profile in members
    )


def tier_at_least(tier: str, minimum: str) -> bool:
    """Return whether ``tier`` satisfies ``minimum`` under §0.4.3."""
    return TIERS.index(tier) >= TIERS.index(minimum)


def rule_sort_key(number: str) -> tuple[int, int, int]:
    """Sort permanent rule IDs numerically, not lexically."""
    part, section, index = number.split(".")
    return int(part), int(section), int(index)

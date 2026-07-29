"""Optional record types for agent-authored semantic analysis.

Nothing here is required. An agent may use every record, some records, or
none, and may build its own structures instead. What the module does supply
is a shape that satisfies Rule 8.6.4: a recorded judgment names its source
spans, cites the rule or section that supports it, and carries a judgment
state.

The validators in this module check identifiers, spans, hashes, and
citations. They never check whether a semantic judgment is correct.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from itws.document import StructuralManifest
from itws.vocab import (
    CHUNK_TYPES,
    CONSTRUCTS,
    JUDGMENT_STATES,
    LAYERS,
    UNRESOLVED_STATES,
)

SECTION_CITATION_PREFIXES = ("§", "Annex ", "Rule ", "P")


@dataclass
class Judgment:
    """One semantic claim an agent makes about one or more source spans."""

    kind: str
    value: str
    span_ids: tuple[str, ...]
    support: tuple[str, ...]
    state: str = "proposed"
    note: str = ""

    def to_json(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "value": self.value,
            "span_ids": list(self.span_ids),
            "support": list(self.support),
            "state": self.state,
            "note": self.note,
        }


@dataclass
class LedgerEntry:
    """One entry in a document-wide ledger an agent maintains.

    The ledger kinds mirror the §1.6.2 resources: a term, a symbol, a name,
    an exact item, a claim, evidence, a caveat, or a cross-reference.
    """

    ledger: str
    key: str
    span_ids: tuple[str, ...]
    support: tuple[str, ...]
    state: str = "proposed"
    detail: str = ""

    def to_json(self) -> dict[str, object]:
        return {
            "ledger": self.ledger,
            "key": self.key,
            "span_ids": list(self.span_ids),
            "support": list(self.support),
            "state": self.state,
            "detail": self.detail,
        }


@dataclass
class OpenQuestion:
    """An unresolved point the agent refuses to guess at.

    Rule 8.6.3 gives an absent fact its own state. Recording the question is
    how a pipeline reports a gap instead of inventing content.
    """

    question: str
    span_ids: tuple[str, ...]
    state: str = "unknown"
    blocks: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "question": self.question,
            "span_ids": list(self.span_ids),
            "state": self.state,
            "blocks": list(self.blocks),
        }


@dataclass
class AgentAnalysis:
    """One agent's reading of one document, held apart from the structure."""

    document_path: str
    document_hash: str
    profile: str
    judgments: list[Judgment] = field(default_factory=list)
    ledger: list[LedgerEntry] = field(default_factory=list)
    open_questions: list[OpenQuestion] = field(default_factory=list)
    notes: str = ""

    def classify(
        self,
        span_ids: Sequence[str],
        chunk_type: str,
        support: Sequence[str],
        *,
        state: str = "proposed",
        note: str = "",
    ) -> Judgment:
        """Record a §4.1 chunk-type judgment with its supporting citation."""
        judgment = Judgment(
            kind="chunk_type",
            value=chunk_type,
            span_ids=tuple(span_ids),
            support=tuple(support),
            state=state,
            note=note,
        )
        self.judgments.append(judgment)
        return judgment

    def assign_layer(
        self,
        span_ids: Sequence[str],
        layer: str,
        support: Sequence[str],
        *,
        state: str = "proposed",
    ) -> Judgment:
        """Record whether a span belongs to the exact or the plain layer."""
        judgment = Judgment(
            kind="layer",
            value=layer,
            span_ids=tuple(span_ids),
            support=tuple(support),
            state=state,
        )
        self.judgments.append(judgment)
        return judgment

    def note_construct(
        self,
        span_ids: Sequence[str],
        construct: str,
        support: Sequence[str],
        *,
        state: str = "proposed",
    ) -> Judgment:
        """Record that a span contains one §1.6.2 construct."""
        judgment = Judgment(
            kind="construct",
            value=construct,
            span_ids=tuple(span_ids),
            support=tuple(support),
            state=state,
        )
        self.judgments.append(judgment)
        return judgment

    def revise(self, judgment: Judgment, value: str, support: Sequence[str]) -> Judgment:
        """Replace one judgment, keeping the earlier reading as disputed.

        An agent that changes its mind after further search leaves both
        readings on the record, which is what §1.6.1 and Rule 8.6.4 intend.
        """
        judgment.state = "disputed"
        return self.classify(
            judgment.span_ids, value, support, state="proposed",
            note=f"revises the {judgment.value!r} reading",
        ) if judgment.kind == "chunk_type" else self.note_construct(
            judgment.span_ids, value, support
        )

    def to_json(self) -> dict[str, object]:
        return {
            "document_path": self.document_path,
            "document_hash": self.document_hash,
            "profile": self.profile,
            "notes": self.notes,
            "judgments": [item.to_json() for item in self.judgments],
            "ledger": [item.to_json() for item in self.ledger],
            "open_questions": [item.to_json() for item in self.open_questions],
        }


def validate_analysis(
    analysis: AgentAnalysis,
    manifest: StructuralManifest,
    *,
    known_rules: Iterable[str] = (),
) -> list[str]:
    """Check a record's identifiers, spans, hashes, and citations.

    The function reports mechanical problems only. It never reports that a
    classification is wrong: no deterministic code can decide that.
    """
    problems: list[str] = []
    rules = set(known_rules)
    span_ids = {unit.id for unit in manifest.units}

    if analysis.document_hash != manifest.document_hash:
        problems.append(
            "the analysis was written against a different document version "
            f"({analysis.document_hash} != {manifest.document_hash})"
        )
    if manifest.declarations and analysis.profile != manifest.declarations.profile:
        problems.append(
            f"the analysis names profile {analysis.profile!r} but the document "
            f"declares {manifest.declarations.profile!r}"
        )

    for judgment in analysis.judgments:
        label = f"judgment {judgment.kind}={judgment.value!r}"
        if judgment.state not in JUDGMENT_STATES:
            problems.append(f"{label}: unknown state {judgment.state!r}")
        if not judgment.span_ids:
            problems.append(f"{label}: names no source span (Rule 8.6.4)")
        for span_id in judgment.span_ids:
            if span_id not in span_ids:
                problems.append(f"{label}: unknown span ID {span_id!r}")
        if not judgment.support:
            problems.append(f"{label}: cites no rule or section (Rule 8.6.4)")
        problems.extend(
            f"{label}: {problem}"
            for problem in _citation_problems(judgment.support, rules)
        )
        if judgment.kind == "chunk_type" and judgment.value not in CHUNK_TYPES:
            problems.append(f"{label}: unknown §4.1 chunk type")
        if judgment.kind == "layer" and judgment.value not in LAYERS:
            problems.append(f"{label}: unknown prose layer")
        if judgment.kind == "construct" and judgment.value not in CONSTRUCTS:
            problems.append(f"{label}: unknown §1.6.2 construct")

    for entry in analysis.ledger:
        label = f"ledger {entry.ledger}:{entry.key!r}"
        if entry.state not in JUDGMENT_STATES:
            problems.append(f"{label}: unknown state {entry.state!r}")
        for span_id in entry.span_ids:
            if span_id not in span_ids:
                problems.append(f"{label}: unknown span ID {span_id!r}")
        problems.extend(
            f"{label}: {problem}"
            for problem in _citation_problems(entry.support, rules)
        )

    for question in analysis.open_questions:
        if question.state not in UNRESOLVED_STATES:
            problems.append(
                f"open question {question.question!r}: state must be one of "
                + ", ".join(UNRESOLVED_STATES)
            )
        for span_id in question.span_ids:
            if span_id not in span_ids:
                problems.append(
                    f"open question {question.question!r}: unknown span ID "
                    f"{span_id!r}"
                )

    return problems


def _citation_problems(support: Sequence[str], rules: set[str]) -> list[str]:
    problems: list[str] = []
    for citation in support:
        stripped = citation.strip()
        if stripped in rules:
            continue
        if any(stripped.startswith(prefix) for prefix in SECTION_CITATION_PREFIXES):
            continue
        problems.append(
            f"citation {citation!r} is neither a known rule ID nor a section "
            "reference"
        )
    return problems


def contradictions(analysis: AgentAnalysis) -> list[str]:
    """Report spans that carry two accepted judgments of one kind.

    Two `proposed` readings are a legitimate open question. Two
    `accepted_for_run` readings of one kind are a defect in the record.
    """
    accepted: dict[tuple[str, str], list[str]] = {}
    for judgment in analysis.judgments:
        if judgment.state != "accepted_for_run":
            continue
        for span_id in judgment.span_ids:
            accepted.setdefault((span_id, judgment.kind), []).append(judgment.value)
    return [
        f"span {span_id} has {len(values)} accepted {kind} judgments: "
        + ", ".join(sorted(values))
        for (span_id, kind), values in sorted(accepted.items())
        if len(set(values)) > 1
    ]

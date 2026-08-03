"""Optional records for agent-authored semantic analysis.

These records support a rewrite but never form a conformance gate. An agent
may use them, use another shape, or use none. Missing facts remain local open
questions so work can continue on independent spans.
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
        judgment = Judgment(
            kind="construct",
            value=construct,
            span_ids=tuple(span_ids),
            support=tuple(support),
            state=state,
        )
        self.judgments.append(judgment)
        return judgment

    def revise(
        self,
        judgment: Judgment,
        value: str,
        support: Sequence[str],
    ) -> Judgment:
        judgment.state = "disputed"
        if judgment.kind == "chunk_type":
            return self.classify(
                judgment.span_ids,
                value,
                support,
                note=f"revises the {judgment.value!r} reading",
            )
        return self.note_construct(judgment.span_ids, value, support)

    def to_json(self) -> dict[str, object]:
        return {
            "document_path": self.document_path,
            "document_hash": self.document_hash,
            "profile": self.profile,
            "notes": self.notes,
            "judgments": [item.to_json() for item in self.judgments],
            "ledger": [item.to_json() for item in self.ledger],
            "open_questions": [
                item.to_json() for item in self.open_questions
            ],
        }


def validate_analysis(
    analysis: AgentAnalysis,
    manifest: StructuralManifest,
    *,
    known_rules: Iterable[str] = (),
) -> list[str]:
    """Check identifiers and record shape without judging meaning."""
    problems: list[str] = []
    rules = set(known_rules)
    span_ids = {unit.id for unit in manifest.units}
    if analysis.document_hash != manifest.document_hash:
        problems.append("the analysis names a different document version")
    if manifest.declarations and analysis.profile != manifest.declarations.profile:
        problems.append(
            f"the analysis names profile {analysis.profile!r}, but the "
            f"document declares {manifest.declarations.profile!r}"
        )
    for judgment in analysis.judgments:
        label = f"judgment {judgment.kind}={judgment.value!r}"
        if judgment.state not in JUDGMENT_STATES:
            problems.append(f"{label}: unknown state {judgment.state!r}")
        if not judgment.span_ids:
            problems.append(f"{label}: names no source span")
        for span_id in judgment.span_ids:
            if span_id not in span_ids:
                problems.append(f"{label}: unknown span ID {span_id!r}")
        problems.extend(
            f"{label}: {problem}"
            for problem in _citation_problems(judgment.support, rules)
        )
        if judgment.kind == "chunk_type" and judgment.value not in CHUNK_TYPES:
            problems.append(f"{label}: unknown §4.1 chunk type")
        if judgment.kind == "layer" and judgment.value not in LAYERS:
            problems.append(f"{label}: unknown prose layer")
        if judgment.kind == "construct" and judgment.value not in CONSTRUCTS:
            problems.append(f"{label}: unknown §1.6 construct")
    for entry in analysis.ledger:
        label = f"ledger {entry.ledger}:{entry.key!r}"
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


def validate_comment_judgments(
    comment_set, *, known_rules: Iterable[str] = ()
) -> list[str]:
    """Check optional comment judgments and questions mechanically."""
    problems: list[str] = []
    rules = set(known_rules)
    comment_ids = {record.comment_id for record in comment_set.records}
    for index, judgment in enumerate(comment_set.judgments, start=1):
        label = f"carrier judgment {index}"
        if not isinstance(judgment, dict):
            problems.append(f"{label}: must be an object")
            continue
        state = judgment.get("state", "proposed")
        if state not in JUDGMENT_STATES:
            problems.append(f"{label}: unknown state {state!r}")
        for span_id in judgment.get("span_ids", []):
            if span_id not in comment_ids:
                problems.append(f"{label}: unknown comment ID {span_id!r}")
        problems.extend(
            f"{label}: {problem}"
            for problem in _citation_problems(
                tuple(judgment.get("support", [])), rules
            )
        )
    for index, question in enumerate(comment_set.open_questions, start=1):
        label = f"carrier open question {index}"
        if not isinstance(question, dict):
            problems.append(f"{label}: must be an object")
            continue
        state = question.get("state", "unknown")
        if state not in UNRESOLVED_STATES:
            problems.append(
                f"{label}: state must be one of "
                + ", ".join(UNRESOLVED_STATES)
            )
        for span_id in question.get("span_ids", []):
            if span_id not in comment_ids:
                problems.append(f"{label}: unknown comment ID {span_id!r}")
    return problems


def _citation_problems(
    support: Sequence[str], rules: set[str]
) -> list[str]:
    problems: list[str] = []
    for citation in support:
        stripped = citation.strip()
        if stripped in rules:
            continue
        if any(
            stripped.startswith(prefix)
            for prefix in SECTION_CITATION_PREFIXES
        ):
            continue
        problems.append(
            f"citation {citation!r} is neither a known rule ID nor a "
            "section reference"
        )
    return problems


def contradictions(analysis: AgentAnalysis) -> list[str]:
    accepted: dict[tuple[str, str], list[str]] = {}
    for judgment in analysis.judgments:
        if judgment.state != "accepted_for_run":
            continue
        for span_id in judgment.span_ids:
            accepted.setdefault(
                (span_id, judgment.kind), []
            ).append(judgment.value)
    return [
        f"span {span_id} has {len(values)} accepted {kind} judgments: "
        + ", ".join(sorted(values))
        for (span_id, kind), values in sorted(accepted.items())
        if len(set(values)) > 1
    ]

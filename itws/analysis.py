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

import json
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from itws.document import ScanPath, StructuralManifest
from itws.model import content_hash
from itws.vocab import (
    CHUNK_TYPES,
    CONSTRUCTS,
    JUDGMENT_STATES,
    LAYERS,
    UNRESOLVED_STATES,
)

SECTION_CITATION_PREFIXES = ("§", "Annex ", "Rule ", "P")
SCAN_KEY_FIELDS = (
    "purpose",
    "main_point",
    "status_or_strength",
    "material_boundaries",
)
SCAN_TEST_ROLES = ("author", "reader_proxy", "publication_participant")
SCAN_TEST_RESULTS = ("pass", "fail", "blocked")


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


@dataclass(frozen=True)
class ScanKeyField:
    """One expected part of a document-specific scan response."""

    name: str
    expected: str
    span_ids: tuple[str, ...]
    support: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "expected": self.expected,
            "span_ids": list(self.span_ids),
            "support": list(self.support),
        }


@dataclass(frozen=True)
class StrengthenedFoil:
    """One plausible but wider or stronger paraphrase."""

    id: str
    protected_field: str
    text: str
    span_ids: tuple[str, ...]
    support: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "protected_field": self.protected_field,
            "text": self.text,
            "span_ids": list(self.span_ids),
            "support": list(self.support),
        }


@dataclass(frozen=True)
class ScanTestKey:
    """The exact-layer answer key and strengthened foils for one document."""

    document_path: str
    document_hash: str
    profile: str
    scan_path_hash: str
    fields: tuple[ScanKeyField, ...]
    foils: tuple[StrengthenedFoil, ...]

    def _content_json(self) -> dict[str, object]:
        return {
            "document_path": self.document_path,
            "document_hash": self.document_hash,
            "profile": self.profile,
            "scan_path_hash": self.scan_path_hash,
            "fields": [item.to_json() for item in self.fields],
            "foils": [item.to_json() for item in self.foils],
        }

    @property
    def key_hash(self) -> str:
        rendered = json.dumps(
            self._content_json(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return content_hash(rendered)

    def to_json(self) -> dict[str, object]:
        return {**self._content_json(), "key_hash": self.key_hash}


@dataclass(frozen=True)
class FoilResponse:
    """One reader decision on one strengthened foil."""

    foil_id: str
    accepted: bool

    def to_json(self) -> dict[str, object]:
        return {"foil_id": self.foil_id, "accepted": self.accepted}


@dataclass(frozen=True)
class ScanTestRecord:
    """One delayed scan response and its mechanical provenance."""

    role: str
    profile: str
    document_hash: str
    scan_path_hash: str
    key_hash: str
    linked_source_hashes: tuple[tuple[str, str], ...]
    intervening_task: str
    elapsed_seconds: float
    response_fields: tuple[tuple[str, str], ...]
    foil_responses: tuple[FoilResponse, ...]
    result: str
    findings: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "role": self.role,
            "profile": self.profile,
            "document_hash": self.document_hash,
            "scan_path_hash": self.scan_path_hash,
            "key_hash": self.key_hash,
            "linked_source_hashes": [
                {"span_id": span_id, "source_hash": source_hash}
                for span_id, source_hash in self.linked_source_hashes
            ],
            "intervening_task": self.intervening_task,
            "elapsed_seconds": self.elapsed_seconds,
            "response_fields": dict(self.response_fields),
            "foil_responses": [item.to_json() for item in self.foil_responses],
            "result": self.result,
            "findings": list(self.findings),
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


def validate_scan_test(
    key: ScanTestKey,
    record: ScanTestRecord,
    manifest: StructuralManifest,
    path: ScanPath,
    *,
    known_rules: Iterable[str] = (),
) -> list[str]:
    """Check scan-test structure, citations, hashes, and foil coverage.

    This function never decides whether a response matches an expected
    meaning. A reader or agent performs that comparison under Rule 8.1.4.
    """
    problems: list[str] = []
    rules = set(known_rules)
    units = {unit.id: unit for unit in manifest.units}

    if key.document_path != manifest.path:
        problems.append(
            f"the scan key names {key.document_path!r}, not {manifest.path!r}"
        )
    if key.document_hash != manifest.document_hash:
        problems.append("the scan key was prepared against a different document hash")
    if key.scan_path_hash != path.scan_path_hash:
        problems.append("the scan key was prepared against a different scan path")
    if manifest.declarations and key.profile != manifest.declarations.profile:
        problems.append(
            f"the scan key names profile {key.profile!r} but the document declares "
            f"{manifest.declarations.profile!r}"
        )

    field_names = [item.name for item in key.fields]
    if len(field_names) != len(set(field_names)):
        problems.append("the scan key repeats a field")
    for required in SCAN_KEY_FIELDS:
        if required not in field_names:
            problems.append(f"the scan key omits required field {required!r}")
    for item in key.fields:
        label = f"scan-key field {item.name!r}"
        if item.name not in SCAN_KEY_FIELDS:
            problems.append(f"{label}: unknown field")
        if not item.expected.strip():
            problems.append(f"{label}: expected response is empty")
        if not item.span_ids:
            problems.append(f"{label}: names no linked source span")
        for span_id in item.span_ids:
            if span_id not in units:
                problems.append(f"{label}: unknown span ID {span_id!r}")
        problems.extend(
            f"{label}: {problem}"
            for problem in _citation_problems(item.support, rules)
        )

    foil_ids = [foil.id for foil in key.foils]
    if len(foil_ids) != len(set(foil_ids)):
        problems.append("the scan key repeats a strengthened-foil ID")
    for foil in key.foils:
        label = f"foil {foil.id!r}"
        if foil.protected_field not in field_names:
            problems.append(
                f"{label}: unknown protected field {foil.protected_field!r}"
            )
        if not foil.text.strip():
            problems.append(f"{label}: text is empty")
        if not foil.span_ids:
            problems.append(f"{label}: names no linked source span")
        for span_id in foil.span_ids:
            if span_id not in units:
                problems.append(f"{label}: unknown span ID {span_id!r}")
        problems.extend(
            f"{label}: {problem}"
            for problem in _citation_problems(foil.support, rules)
        )

    if record.role not in SCAN_TEST_ROLES:
        problems.append(f"unknown scan-test role {record.role!r}")
    if record.profile != key.profile:
        problems.append("the scan record and key name different profiles")
    if record.document_hash != manifest.document_hash:
        problems.append("the scan record was written against a different document")
    if record.scan_path_hash != path.scan_path_hash:
        problems.append("the scan record was written against a different scan path")
    if record.key_hash != key.key_hash:
        problems.append("the scan record was scored against a different key")
    if not record.intervening_task.strip():
        problems.append("the scan record names no source-independent task")
    if record.elapsed_seconds < 0:
        problems.append("the scan record has a negative elapsed interval")
    if record.result not in SCAN_TEST_RESULTS:
        problems.append(f"unknown scan-test result {record.result!r}")

    linked_hashes = dict(record.linked_source_hashes)
    if len(linked_hashes) != len(record.linked_source_hashes):
        problems.append("the scan record repeats a linked source span")
    required_span_ids = {
        span_id
        for item in key.fields
        for span_id in item.span_ids
    } | {
        span_id
        for foil in key.foils
        for span_id in foil.span_ids
    }
    for span_id in sorted(required_span_ids):
        if span_id not in linked_hashes:
            problems.append(f"the scan record omits source hash for {span_id!r}")
        elif span_id in units and linked_hashes[span_id] != units[span_id].source_hash:
            problems.append(f"the scan record has a stale source hash for {span_id!r}")

    response_fields = dict(record.response_fields)
    if len(response_fields) != len(record.response_fields):
        problems.append("the scan response repeats a field")
    for required in SCAN_KEY_FIELDS:
        if required not in response_fields:
            problems.append(f"the scan response omits field {required!r}")

    foil_responses = {item.foil_id: item for item in record.foil_responses}
    if len(foil_responses) != len(record.foil_responses):
        problems.append("the scan response repeats a foil decision")
    for foil_id in foil_ids:
        response = foil_responses.get(foil_id)
        if response is None:
            problems.append(f"the scan response omits foil {foil_id!r}")
        elif response.accepted:
            problems.append(f"the scan response accepts strengthened foil {foil_id!r}")
    for foil_id in foil_responses:
        if foil_id not in foil_ids:
            problems.append(f"the scan response names unknown foil {foil_id!r}")

    return problems


def validate_comment_judgments(
    comment_set, *, known_rules: Iterable[str] = ()
) -> list[str]:
    """Check the judgments a carrier records against its comment records.

    A carrier may record the same Rule 8.6.4 judgments as a document
    analysis: each names its comment IDs, cites its support, and carries a
    judgment state. The function checks identifiers and citations only; it
    never checks that a judgment, such as an information-delta or a
    code-comment-conflict reading, is correct.
    """
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
        span_ids = judgment.get("span_ids", [])
        if not span_ids:
            problems.append(f"{label}: names no comment ID (Rule 8.6.4)")
        for span_id in span_ids:
            if span_id not in comment_ids:
                problems.append(f"{label}: unknown comment ID {span_id!r}")
        support = judgment.get("support", [])
        if not support:
            problems.append(f"{label}: cites no rule or section (Rule 8.6.4)")
        problems.extend(
            f"{label}: {problem}"
            for problem in _citation_problems(tuple(support), rules)
        )
    for index, question in enumerate(comment_set.open_questions, start=1):
        label = f"carrier open question {index}"
        if not isinstance(question, dict):
            problems.append(f"{label}: must be an object")
            continue
        state = question.get("state", "unknown")
        if state not in UNRESOLVED_STATES:
            problems.append(
                f"{label}: state must be one of " + ", ".join(UNRESOLVED_STATES)
            )
        for span_id in question.get("span_ids", []):
            if span_id not in comment_ids:
                problems.append(f"{label}: unknown comment ID {span_id!r}")
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

"""Optional planning scaffolds for agent-coordinated rewrites.

An agent may use every record here, some of them, or none. The module
supplies shapes and mechanical checks; it prescribes no orchestration
protocol and imposes no repository-wide job format.

The checks reject a cycle, an unknown identifier, and a resource collision.
They never choose between two dependency readings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from itws.catalog import Catalog
from itws.document import StructuralManifest
from itws.model import MutationPolicy
from itws.vocab import JUDGMENT_STATES, RESOURCES

#: Relationships a coordinator commonly declares between work slices. The
#: list is a prompt, not a closed vocabulary: an agent may add its own.
COMMON_DEPENDENCIES = (
    "definition-before-use",
    "prior-before-dependent-detail",
    "exact-before-plain-rendering",
    "evidence-before-interpretation",
    "claim-with-local-caveat",
    "heading-with-section-opening",
    "skeleton-slot-order",
    "parent-condition-before-subtask-verification",
    "procedure-prerequisite-before-step",
)


@dataclass
class PreservationNote:
    """Content a rewrite must carry through unchanged."""

    span_ids: tuple[str, ...]
    what: str
    support: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "span_ids": list(self.span_ids),
            "what": self.what,
            "support": list(self.support),
        }


@dataclass
class ResourceClaim:
    """A declared read or write of one §1.6.2 resource."""

    resource: str
    mode: str
    detail: str = ""

    def to_json(self) -> dict[str, object]:
        return {"resource": self.resource, "mode": self.mode, "detail": self.detail}


@dataclass
class DependencyNote:
    """One ordering an agent asserts between two work slices."""

    before: str
    after: str
    kind: str
    support: tuple[str, ...]
    state: str = "proposed"

    def to_json(self) -> dict[str, object]:
        return {
            "before": self.before,
            "after": self.after,
            "kind": self.kind,
            "support": list(self.support),
            "state": self.state,
        }


@dataclass
class WorkSlice:
    """One rewrite task: writable spans, read-only context, and its rules."""

    id: str
    writable_span_ids: tuple[str, ...]
    context_span_ids: tuple[str, ...] = ()
    rules: tuple[str, ...] = ()
    sections: tuple[str, ...] = ()
    terms: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()
    intent: str = ""
    preservation: tuple[PreservationNote, ...] = ()
    claims: tuple[ResourceClaim, ...] = ()
    prohibited: tuple[str, ...] = ()
    blocker_policy: str = "report and stop"

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "writable_span_ids": list(self.writable_span_ids),
            "context_span_ids": list(self.context_span_ids),
            "rules": list(self.rules),
            "sections": list(self.sections),
            "terms": list(self.terms),
            "examples": list(self.examples),
            "intent": self.intent,
            "preservation": [note.to_json() for note in self.preservation],
            "resource_claims": [claim.to_json() for claim in self.claims],
            "prohibited": list(self.prohibited),
            "blocker_policy": self.blocker_policy,
        }

    @property
    def writes(self) -> set[str]:
        return {claim.resource for claim in self.claims if claim.mode == "write"}

    @property
    def reads(self) -> set[str]:
        return {claim.resource for claim in self.claims if claim.mode == "read"}


@dataclass
class ExecutionWave:
    """A set of work slices a coordinator proposes to run together."""

    index: int
    slice_ids: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {"index": self.index, "slice_ids": list(self.slice_ids)}


@dataclass
class WorkPlan:
    """A coordinator's slices, dependencies, and proposed waves."""

    document_path: str
    document_hash: str
    profile: str
    slices: list[WorkSlice] = field(default_factory=list)
    dependencies: list[DependencyNote] = field(default_factory=list)
    waves: list[ExecutionWave] = field(default_factory=list)

    def slice(self, slice_id: str) -> WorkSlice | None:
        for candidate in self.slices:
            if candidate.id == slice_id:
                return candidate
        return None

    def to_json(self) -> dict[str, object]:
        return {
            "document_path": self.document_path,
            "document_hash": self.document_hash,
            "profile": self.profile,
            "slices": [item.to_json() for item in self.slices],
            "dependencies": [item.to_json() for item in self.dependencies],
            "waves": [item.to_json() for item in self.waves],
        }


def validate_plan(
    plan: WorkPlan,
    manifest: StructuralManifest,
    catalog: Catalog | None = None,
) -> list[str]:
    """Check identifiers, spans, hashes, resources, and dependency endpoints."""
    problems: list[str] = []
    span_ids = {unit.id for unit in manifest.units}
    slice_ids = [item.id for item in plan.slices]

    if plan.document_hash != manifest.document_hash:
        problems.append(
            "the plan was written against a different document version "
            f"({plan.document_hash} != {manifest.document_hash})"
        )
    duplicates = {value for value in slice_ids if slice_ids.count(value) > 1}
    for value in sorted(duplicates):
        problems.append(f"duplicate work-slice ID {value!r}")

    for work_slice in plan.slices:
        label = f"slice {work_slice.id!r}"
        if not work_slice.writable_span_ids:
            problems.append(f"{label}: declares no writable span")
        for span_id in work_slice.writable_span_ids + work_slice.context_span_ids:
            if span_id not in span_ids:
                problems.append(f"{label}: unknown span ID {span_id!r}")
        overlap = set(work_slice.writable_span_ids) & set(work_slice.context_span_ids)
        if overlap:
            problems.append(
                f"{label}: span(s) {', '.join(sorted(overlap))} are both writable "
                "and read-only context"
            )
        for claim in work_slice.claims:
            if claim.resource not in RESOURCES:
                problems.append(f"{label}: unknown resource {claim.resource!r}")
            if claim.mode not in {"read", "write"}:
                problems.append(f"{label}: unknown resource mode {claim.mode!r}")
        if catalog is not None:
            for rule_id in work_slice.rules:
                if rule_id not in catalog.rules:
                    problems.append(f"{label}: unknown rule ID {rule_id!r}")
            for term in work_slice.terms:
                try:
                    catalog.get_glossary_entry(term)
                except Exception:  # noqa: BLE001 - reported, not raised
                    problems.append(f"{label}: unknown glossary term {term!r}")
        for note in work_slice.preservation:
            for span_id in note.span_ids:
                if span_id not in span_ids:
                    problems.append(
                        f"{label}: preservation note names unknown span {span_id!r}"
                    )
            if not note.support:
                problems.append(
                    f"{label}: preservation note {note.what!r} cites no rule"
                )

    for dependency in plan.dependencies:
        if dependency.before not in slice_ids:
            problems.append(
                f"dependency names unknown slice {dependency.before!r} as `before`"
            )
        if dependency.after not in slice_ids:
            problems.append(
                f"dependency names unknown slice {dependency.after!r} as `after`"
            )
        if dependency.before == dependency.after:
            problems.append(f"slice {dependency.before!r} depends on itself")
        if dependency.state not in JUDGMENT_STATES:
            problems.append(f"dependency has unknown state {dependency.state!r}")
        if not dependency.support:
            problems.append(
                f"dependency {dependency.before} -> {dependency.after} cites no rule"
            )

    problems.extend(_wave_problems(plan))
    problems.extend(
        f"{left} and {right} both write {resource}"
        for left, right, resource in detect_write_conflicts(plan)
    )
    return problems


def _wave_problems(plan: WorkPlan) -> list[str]:
    if not plan.waves:
        return []
    problems: list[str] = []
    slice_ids = {item.id for item in plan.slices}
    placement: dict[str, int] = {}
    for wave in plan.waves:
        for slice_id in wave.slice_ids:
            if slice_id not in slice_ids:
                problems.append(f"wave {wave.index} names unknown slice {slice_id!r}")
            if slice_id in placement:
                problems.append(
                    f"slice {slice_id!r} appears in waves {placement[slice_id]} "
                    f"and {wave.index}"
                )
            placement[slice_id] = wave.index
    missing = sorted(slice_ids - set(placement))
    for slice_id in missing:
        problems.append(f"slice {slice_id!r} is in no wave")

    for dependency in plan.dependencies:
        before = placement.get(dependency.before)
        after = placement.get(dependency.after)
        if before is None or after is None:
            continue
        if before >= after:
            problems.append(
                f"wave order violates dependency {dependency.before} -> "
                f"{dependency.after} ({dependency.kind})"
            )

    for wave in plan.waves:
        members = [plan.slice(slice_id) for slice_id in wave.slice_ids]
        for index, left in enumerate(members):
            for right in members[index + 1 :]:
                if left is None or right is None:
                    continue
                shared_write = left.writes & right.writes
                if shared_write:
                    problems.append(
                        f"wave {wave.index}: {left.id} and {right.id} both write "
                        + ", ".join(sorted(shared_write))
                    )
                write_read = (left.writes & right.reads) | (right.writes & left.reads)
                if write_read:
                    problems.append(
                        f"wave {wave.index}: {left.id} and {right.id} have a "
                        "write-to-read conflict on " + ", ".join(sorted(write_read))
                    )
    return problems


def detect_cycles(plan: WorkPlan) -> list[list[str]]:
    """Return every dependency cycle, as its ordered edges.

    A cycle is reported, never broken: choosing which edge to drop is a
    reading of the document, not a mechanical step.
    """
    edges: dict[str, list[str]] = {}
    for dependency in plan.dependencies:
        edges.setdefault(dependency.before, []).append(dependency.after)

    cycles: list[list[str]] = []
    state: dict[str, int] = {}

    def visit(node: str, trail: list[str]) -> None:
        mark = state.get(node, 0)
        if mark == 1:
            start = trail.index(node)
            cycles.append(trail[start:] + [node])
            return
        if mark == 2:
            return
        state[node] = 1
        for successor in sorted(edges.get(node, [])):
            visit(successor, trail + [node])
        state[node] = 2

    for node in sorted(edges):
        visit(node, [])
    return cycles


def detect_write_conflicts(plan: WorkPlan) -> list[tuple[str, str, str]]:
    """Return unordered slice pairs that write one resource.

    A declared serial dependency between the two removes the conflict.
    """
    ordered: set[tuple[str, str]] = set()
    for dependency in plan.dependencies:
        ordered.add((dependency.before, dependency.after))
        ordered.add((dependency.after, dependency.before))

    conflicts: list[tuple[str, str, str]] = []
    for index, left in enumerate(plan.slices):
        for right in plan.slices[index + 1 :]:
            if (left.id, right.id) in ordered:
                continue
            for resource in sorted(left.writes & right.writes):
                if resource == "none":
                    continue
                conflicts.append((left.id, right.id, resource))
    return conflicts


def check_mutation_policies(
    plan: WorkPlan,
    manifest: StructuralManifest,
    policies: Iterable[MutationPolicy],
) -> list[str]:
    """Report a writable span that a skeleton's mutation policy forbids."""
    problems: list[str] = []
    policy_list = list(policies)
    if not policy_list:
        return problems
    by_id = {unit.id: unit for unit in manifest.units}
    for work_slice in plan.slices:
        for span_id in work_slice.writable_span_ids:
            unit = by_id.get(span_id)
            if unit is None:
                continue
            for policy in policy_list:
                if policy.policy != "append-only":
                    continue
                if not _under_slot(unit, policy.scope, manifest):
                    continue
                problems.append(
                    f"slice {work_slice.id!r} declares span {span_id} writable, but "
                    f"the {policy.scope!r} slot is append-only "
                    f"(rule {policy.rule}): {policy.note}"
                )
    return problems


def _under_slot(unit, slot: str, manifest: StructuralManifest) -> bool:
    if unit.canonical_slot == slot:
        return True
    for heading in manifest.units:
        if heading.node_type != "heading" or heading.canonical_slot != slot:
            continue
        if heading.heading_path and set(heading.heading_path) <= set(unit.heading_path):
            return True
    return False


def context_packet(
    plan: WorkPlan,
    work_slice: WorkSlice,
    manifest: StructuralManifest,
    catalog: Catalog,
    *,
    analysis_json: dict | None = None,
) -> dict:
    """Render one work slice as a compact, self-contained context packet."""
    by_id = {unit.id: unit for unit in manifest.units}
    writable = [by_id[span] for span in work_slice.writable_span_ids if span in by_id]
    context = [by_id[span] for span in work_slice.context_span_ids if span in by_id]
    beam = catalog.assemble_context(
        profile=plan.profile,
        rules=work_slice.rules,
        sections=work_slice.sections,
        terms=work_slice.terms,
        examples=work_slice.examples,
        note=work_slice.intent,
    )
    dependencies = [
        dependency.to_json()
        for dependency in plan.dependencies
        if work_slice.id in {dependency.before, dependency.after}
    ]
    return {
        "itws_version": catalog.version,
        "artifact_manifest_hash": catalog.manifest["artifact_hashes"].get(
            "rules.jsonl", ""
        ),
        "document": {
            "path": manifest.path,
            "document_hash": manifest.document_hash,
            "declarations": (
                manifest.declarations.to_json() if manifest.declarations else None
            ),
        },
        "slice": work_slice.to_json(),
        "writable_spans": [
            {
                "id": unit.id,
                "source_span": unit.span.to_json(),
                "source_hash": unit.source_hash,
                "heading_path": list(unit.heading_path),
                "canonical_slot": unit.canonical_slot,
                "text": unit.text,
            }
            for unit in writable
        ],
        "read_only_context": [
            {
                "id": unit.id,
                "source_span": unit.span.to_json(),
                "heading_path": list(unit.heading_path),
                "text": unit.text,
            }
            for unit in context
        ],
        "dependencies": dependencies,
        "agent_analysis": analysis_json,
        "navigation_beam": beam,
    }

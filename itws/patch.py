"""Mechanical guards for proposed rewrites.

Every function here inspects. None applies a patch, chooses between two
patches, or judges whether a rewrite preserves meaning. Rule 8.6.5 requires
a collision to be reported rather than resolved, and Rule 5.1.1 reserves the
meaning question for a reader.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from itws.document import StructuralManifest, parse_document
from itws.model import content_hash
from itws.work import WorkSlice


@dataclass(frozen=True)
class ChangedRange:
    """One contiguous change between a base document and a proposal."""

    base_start: int
    base_end: int
    proposed_start: int
    proposed_end: int
    operation: str
    base_text: str
    proposed_text: str

    def to_json(self) -> dict[str, object]:
        return {
            "operation": self.operation,
            "base_start_line": self.base_start,
            "base_end_line": self.base_end,
            "proposed_start_line": self.proposed_start,
            "proposed_end_line": self.proposed_end,
            "base_text": self.base_text,
            "proposed_text": self.proposed_text,
        }


@dataclass
class PatchReport:
    """What deterministic code can establish about one proposed rewrite."""

    base_path: str
    base_hash: str
    proposed_hash: str
    changes: tuple[ChangedRange, ...]
    affected_span_ids: tuple[str, ...]
    outside_slice: tuple[str, ...] = ()
    stale_spans: tuple[str, ...] = ()
    problems: tuple[str, ...] = ()

    @property
    def safe_to_apply(self) -> bool:
        """No stale source, no edit outside the declared spans, no problem.

        A safe patch is still an unreviewed patch: this property says nothing
        about meaning.
        """
        return not (self.outside_slice or self.stale_spans or self.problems)

    def to_json(self) -> dict[str, object]:
        return {
            "base_path": self.base_path,
            "base_hash": self.base_hash,
            "proposed_hash": self.proposed_hash,
            "change_count": len(self.changes),
            "changes": [change.to_json() for change in self.changes],
            "affected_span_ids": list(self.affected_span_ids),
            "edits_outside_slice": list(self.outside_slice),
            "stale_spans": list(self.stale_spans),
            "problems": list(self.problems),
            "safe_to_apply": self.safe_to_apply,
        }


def changed_ranges(base: str, proposed: str) -> list[ChangedRange]:
    """Return every changed line range between two documents."""
    base_lines = base.splitlines()
    proposed_lines = proposed.splitlines()
    matcher = difflib.SequenceMatcher(None, base_lines, proposed_lines, autojunk=False)
    changes: list[ChangedRange] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        changes.append(
            ChangedRange(
                base_start=i1 + 1,
                base_end=max(i2, i1 + 1),
                proposed_start=j1 + 1,
                proposed_end=max(j2, j1 + 1),
                operation=tag,
                base_text="\n".join(base_lines[i1:i2]),
                proposed_text="\n".join(proposed_lines[j1:j2]),
            )
        )
    return changes


def inspect(
    base_path: Path,
    proposed_path: Path,
    *,
    manifest: StructuralManifest | None = None,
    work_slice: WorkSlice | None = None,
    expected_hashes: dict[str, str] | None = None,
) -> PatchReport:
    """Compare a base document with a proposal and report the mechanics."""
    base = base_path.read_text(encoding="utf-8")
    proposed = proposed_path.read_text(encoding="utf-8")
    manifest = manifest or parse_document(base_path)
    changes = changed_ranges(base, proposed)

    affected: list[str] = []
    for change in changes:
        for unit in manifest.units_in_range(change.base_start, change.base_end):
            if unit.id not in affected:
                affected.append(unit.id)

    problems: list[str] = []
    if manifest.document_hash != content_hash(base):
        problems.append(
            "the structural manifest does not match the base document; reparse "
            "before inspecting the patch"
        )

    stale = list(check_stale(manifest, expected_hashes or {}))
    outside: list[str] = []
    if work_slice is not None:
        writable = set(work_slice.writable_span_ids)
        unknown = writable - {unit.id for unit in manifest.units}
        problems.extend(
            f"work slice names unknown span {span_id}" for span_id in sorted(unknown)
        )
        outside = [span_id for span_id in affected if span_id not in writable]
        for change in changes:
            if not manifest.units_in_range(change.base_start, change.base_end):
                problems.append(
                    f"the patch changes lines {change.base_start}-{change.base_end}, "
                    "which lie outside every indexed source unit"
                )

    return PatchReport(
        base_path=base_path.as_posix(),
        base_hash=content_hash(base),
        proposed_hash=content_hash(proposed),
        changes=tuple(changes),
        affected_span_ids=tuple(affected),
        outside_slice=tuple(outside),
        stale_spans=tuple(stale),
        problems=tuple(problems),
    )


def check_stale(
    manifest: StructuralManifest, expected_hashes: dict[str, str]
) -> list[str]:
    """Return the span IDs whose source changed since the hash was taken."""
    current = {unit.id: unit.source_hash for unit in manifest.units}
    stale: list[str] = []
    for span_id, expected in sorted(expected_hashes.items()):
        if span_id not in current:
            stale.append(span_id)
        elif current[span_id] != expected:
            stale.append(span_id)
    return stale


@dataclass(frozen=True)
class Collision:
    """Two proposals that cannot be combined without a decision."""

    left: str
    right: str
    kind: str
    detail: str

    def to_json(self) -> dict[str, object]:
        return {
            "left": self.left,
            "right": self.right,
            "kind": self.kind,
            "detail": self.detail,
        }


def detect_collisions(
    proposals: Sequence[tuple[str, PatchReport]],
    *,
    slices: dict[str, WorkSlice] | None = None,
) -> list[Collision]:
    """Report every write collision among proposed rewrites (Rule 8.6.5).

    Detection is order independent: the same set of proposals produces the
    same collisions regardless of the order they arrive in.
    """
    slices = slices or {}
    collisions: list[Collision] = []
    ordered = sorted(proposals, key=lambda item: item[0])
    for index, (left_name, left) in enumerate(ordered):
        for right_name, right in ordered[index + 1 :]:
            shared_spans = sorted(
                set(left.affected_span_ids) & set(right.affected_span_ids)
            )
            for span_id in shared_spans:
                collisions.append(
                    Collision(
                        left=left_name,
                        right=right_name,
                        kind="span",
                        detail=f"both proposals change span {span_id}",
                    )
                )
            for left_change in left.changes:
                for right_change in right.changes:
                    if _ranges_overlap(left_change, right_change) and not shared_spans:
                        collisions.append(
                            Collision(
                                left=left_name,
                                right=right_name,
                                kind="line-range",
                                detail=(
                                    f"lines {left_change.base_start}-"
                                    f"{left_change.base_end} overlap lines "
                                    f"{right_change.base_start}-"
                                    f"{right_change.base_end}"
                                ),
                            )
                        )
            left_slice = slices.get(left_name)
            right_slice = slices.get(right_name)
            if left_slice and right_slice:
                for resource in sorted(left_slice.writes & right_slice.writes):
                    if resource == "none":
                        continue
                    collisions.append(
                        Collision(
                            left=left_name,
                            right=right_name,
                            kind="resource",
                            detail=f"both proposals write {resource}",
                        )
                    )
    return collisions


def _ranges_overlap(left: ChangedRange, right: ChangedRange) -> bool:
    return not (
        left.base_end < right.base_start or right.base_end < left.base_start
    )


def detect_comment_collisions(
    proposals: Sequence[tuple[str, object]]
) -> list[Collision]:
    """Report comment change sets that write one host anchor (Rule 8.6.5).

    ``proposals`` pairs a name with a :class:`itws.comments.CommentSetManifest`.
    Two change sets that record a comment on one construct span of one host
    file cannot be combined without a decision, exactly as two document
    rewrites of one source span cannot.
    """
    collisions: list[Collision] = []
    ordered = sorted(proposals, key=lambda item: item[0])
    for index, (left_name, left) in enumerate(ordered):
        for right_name, right in ordered[index + 1 :]:
            left_anchors = {
                (record.anchor.path, record.anchor.start_line, record.anchor.end_line)
                for record in left.records
            }
            right_anchors = {
                (record.anchor.path, record.anchor.start_line, record.anchor.end_line)
                for record in right.records
            }
            for path, start, end in sorted(left_anchors & right_anchors):
                collisions.append(
                    Collision(
                        left=left_name,
                        right=right_name,
                        kind="host-anchor",
                        detail=(
                            f"both change sets write a comment anchored to "
                            f"{path}:{start}-{end}"
                        ),
                    )
                )
    return collisions


@dataclass
class AuditRecord:
    """An optional record of one applied or rejected rewrite."""

    document_path: str
    base_hash: str
    proposed_hash: str
    slice_id: str
    rule_trail: list[dict] = field(default_factory=list)
    findings: list[dict] = field(default_factory=list)
    notes: str = ""
    outcome: str = "proposed"

    def to_json(self) -> dict[str, object]:
        return {
            "document_path": self.document_path,
            "base_hash": self.base_hash,
            "proposed_hash": self.proposed_hash,
            "slice_id": self.slice_id,
            "outcome": self.outcome,
            "notes": self.notes,
            "rule_trail": self.rule_trail,
            "findings": self.findings,
        }


def unified_diff(base_path: Path, proposed_path: Path) -> str:
    """Render the change as a unified diff for a reader."""
    base = base_path.read_text(encoding="utf-8").splitlines(keepends=True)
    proposed = proposed_path.read_text(encoding="utf-8").splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            base,
            proposed,
            fromfile=base_path.as_posix(),
            tofile=proposed_path.as_posix(),
        )
    )

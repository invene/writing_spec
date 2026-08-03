"""Load one comment change set and report its mechanical facts.

The manifest built here is the hosted-surface counterpart of
:class:`itws.document.StructuralManifest`. It records extraction results,
carrier matching, coverage, marker grammar, anchors, and source staleness.
Semantic questions stay with a reader or agent (§1.6.1).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from itws.comments.adapter import get_adapter
from itws.comments.records import (
    MARKER_GRAMMAR_RE,
    MARKER_PREFIX_RE,
    MARKER_REFERENCE_RE,
    CommentRecord,
    CommentSetDeclarations,
    CommentUnit,
    parse_comment_records,
    parse_declarations,
)
from itws.document import Declarations, SourceUnit, StructuralManifest
from itws.model import SourceSpan, content_hash
from itws.vocab import COMMENT_PURPOSES


@dataclass(frozen=True)
class _UnitDelta:
    """One occurrence-aware comparison of base and proposed comments."""

    added: tuple[CommentUnit, ...]
    moved: tuple[tuple[CommentUnit, CommentUnit], ...]
    removed: tuple[CommentUnit, ...]
    unchanged: tuple[CommentUnit, ...]


@dataclass
class CommentSetManifest:
    """One parsed comment change set with its extraction results.

    ``problems`` holds carrier and extraction defects that block any check:
    an unreadable file, an unknown adapter, or malformed JSON. Rule-specific
    facts are separate fields so each checker reports under its own rule.
    """

    carrier_path: str
    declarations: CommentSetDeclarations | None
    declaration_problems: tuple[str, ...]
    records: tuple[CommentRecord, ...]
    base_source: str = ""
    proposed_source: str = ""
    base_units: tuple[CommentUnit, ...] = ()
    proposed_units: tuple[CommentUnit, ...] = ()
    problems: tuple[str, ...] = ()
    judgments: tuple[dict, ...] = ()
    open_questions: tuple[dict, ...] = ()

    # ---- derived facts ----------------------------------------------------

    def governed_records(self) -> tuple[CommentRecord, ...]:
        return self.records

    def _pair_units(self) -> "_UnitDelta":
        """Pair base against proposed comments by text, then by position.

        Membership alone loses two real changes. A comment whose text is
        unchanged but whose host lines moved is attached to different code,
        which Rule 4.13.3 governs. A second copy of an existing comment is a
        new governed comment even though its text already occurs. Pairing
        occurrences, rather than comparing sets, keeps both visible.
        """
        available: dict[str, list[CommentUnit]] = {}
        for unit in self.base_units:
            if not unit.excluded:
                available.setdefault(unit.text, []).append(unit)

        added: list[CommentUnit] = []
        moved: list[tuple[CommentUnit, CommentUnit]] = []
        unchanged: list[CommentUnit] = []
        for unit in self.proposed_units:
            if unit.excluded:
                continue
            pool = available.get(unit.text)
            if not pool:
                added.append(unit)
                continue
            # The nearest remaining occurrence keeps the pairing stable when
            # one text repeats, so a move is reported once rather than twice.
            partner = min(
                pool,
                key=lambda candidate: (
                    abs(candidate.span.start_line - unit.span.start_line),
                    candidate.span.start_line,
                ),
            )
            pool.remove(partner)
            if not pool:
                available.pop(unit.text, None)
            if partner.span.start_line == unit.span.start_line:
                unchanged.append(unit)
            else:
                moved.append((partner, unit))

        removed = [unit for pool in available.values() for unit in pool]
        return _UnitDelta(
            added=tuple(added),
            moved=tuple(moved),
            removed=tuple(sorted(removed, key=lambda unit: unit.span.start_line)),
            unchanged=tuple(unchanged),
        )

    def changed_units(self) -> tuple[CommentUnit, ...]:
        """Comment units the proposal adds or attaches to different lines."""
        delta = self._pair_units()
        units = [*delta.added, *(proposed for _, proposed in delta.moved)]
        return tuple(sorted(units, key=lambda unit: unit.span.start_line))

    def moved_units(self) -> tuple[tuple[CommentUnit, CommentUnit], ...]:
        """Base and proposed positions of each comment that kept its text."""
        return self._pair_units().moved

    def removed_units(self) -> tuple[CommentUnit, ...]:
        """Comment units the proposal drops, counting repeated text once each."""
        return self._pair_units().removed

    def uncovered_markers(self) -> tuple[CommentUnit, ...]:
        """Changed markers with no carrier record (§4.3.3 coverage)."""
        recorded = {record.text for record in self.records}
        return tuple(
            unit
            for unit in (*self.changed_units(), *self.removed_units())
            if unit.is_marker and unit.text not in recorded
        )

    def unmatched_records(self) -> tuple[tuple[CommentRecord, str], ...]:
        """Records whose recorded comment no longer matches the sources."""
        problems: list[tuple[CommentRecord, str]] = []
        changed = {unit.span.start_line: unit for unit in self.changed_units()}
        removed = {unit.span.start_line: unit for unit in self.removed_units()}
        for record in self.records:
            pool = removed if record.change == "removed" else changed
            unit = pool.get(record.span.start_line)
            if unit is None:
                problems.append(
                    (record, "no changed comment starts at the recorded line")
                )
            elif unit.text != record.text:
                problems.append(
                    (record, "the recorded text differs from the source comment")
                )
        return tuple(problems)

    def anchor_problems(self) -> tuple[tuple[CommentRecord, str], ...]:
        """Records whose anchor does not resolve or does not match.

        Rule 4.13.3 resolves each anchor against the source its change kind
        names. A removed comment is absent from the proposed source, so its
        anchor resolves against the base source, where it still stood.
        """
        if self.declarations is None:
            return ()
        adapter = get_adapter(self.declarations.host_adapter)
        if adapter is None:
            return ()
        problems: list[tuple[CommentRecord, str]] = []
        for record in self.records:
            if record.change == "removed":
                source = self.base_source
                source_path = self.declarations.base_path
            else:
                source = self.proposed_source
                source_path = self.declarations.proposed_path
            if not source:
                continue
            resolved = adapter.resolve_anchor(source, source_path, record.span)
            anchor = record.anchor
            if not anchor.construct:
                problems.append((record, "the record names no anchor construct"))
            elif anchor.construct != resolved.construct or (
                anchor.start_line,
                anchor.end_line,
            ) != (resolved.start_line, resolved.end_line):
                problems.append(
                    (
                        record,
                        f"the recorded anchor {anchor.construct!r} "
                        f"({anchor.start_line}-{anchor.end_line}) does not match "
                        f"the resolved anchor {resolved.construct!r} "
                        f"({resolved.start_line}-{resolved.end_line})",
                    )
                )
            elif anchor.anchor_hash and anchor.anchor_hash != resolved.anchor_hash:
                problems.append((record, "the recorded anchor hash is stale"))
        return tuple(problems)

    def purpose_problems(self) -> tuple[tuple[CommentRecord, str], ...]:
        problems: list[tuple[CommentRecord, str]] = []
        for record in self.records:
            if record.purpose not in COMMENT_PURPOSES:
                problems.append(
                    (
                        record,
                        f"purpose {record.purpose!r} is not one closed value; "
                        "permitted: " + ", ".join(COMMENT_PURPOSES),
                    )
                )
        return tuple(problems)

    def lifecycle_problems(self) -> tuple[tuple[CommentRecord, str], ...]:
        problems: list[tuple[CommentRecord, str]] = []
        for record in self.records:
            if record.lifecycle == "temporary" and not record.removal_condition:
                problems.append(
                    (record, "lifecycle is temporary with no removal condition")
                )
        return tuple(problems)

    def basis_gaps(self) -> tuple[tuple[CommentRecord, str], ...]:
        """Records owing a basis that name none and give no reason."""
        problems: list[tuple[CommentRecord, str]] = []
        for record in self.records:
            if record.purpose not in {"rationale", "invariant", "history"}:
                continue
            if not record.basis and not record.basis_none_reason:
                problems.append(
                    (record, "no basis and no recorded reason none exists")
                )
        return tuple(problems)

    def marker_problems(self) -> tuple[tuple[str, SourceSpan, str], ...]:
        """Retained markers that violate the Rule 4.13.8 grammar.

        A removed marker is not checked. It is absent from the proposed
        source, so requiring it to be complete would make deleting a bare
        `TODO` a violation and leave keeping it as the conforming option.
        """
        problems: list[tuple[str, SourceSpan, str]] = []
        for unit in self.changed_units():
            if not unit.is_marker or not unit.text:
                continue
            match = MARKER_GRAMMAR_RE.match(unit.text)
            if not match:
                problems.append(
                    (
                        unit.text,
                        unit.span,
                        "does not match TODO(<reference>): <removal condition>",
                    )
                )
                continue
            reference = match.group("reference")
            if not MARKER_REFERENCE_RE.match(reference):
                problems.append(
                    (
                        unit.text,
                        unit.span,
                        f"reference {reference!r} is not a work-item ID or URL",
                    )
                )
        return tuple(problems)

    def to_json(self) -> dict[str, object]:
        delta = self._pair_units()
        return {
            "carrier_path": self.carrier_path,
            "declarations": (
                self.declarations.to_json() if self.declarations else None
            ),
            "declaration_problems": list(self.declaration_problems),
            "problems": list(self.problems),
            "records": [record.to_json() for record in self.records],
            "changed_units": [unit.to_json() for unit in self.changed_units()],
            "added_units": [unit.to_json() for unit in delta.added],
            "moved_units": [
                {"base": base.to_json(), "proposed": proposed.to_json()}
                for base, proposed in delta.moved
            ],
            "removed_units": [unit.to_json() for unit in delta.removed],
            "uncovered_markers": [
                unit.to_json() for unit in self.uncovered_markers()
            ],
        }


def load_comment_set(carrier_path: Path) -> CommentSetManifest:
    """Load a declaration carrier and extract both source versions."""
    location = carrier_path.as_posix()
    try:
        payload = json.loads(carrier_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return CommentSetManifest(
            carrier_path=location,
            declarations=None,
            declaration_problems=(f"unreadable carrier: {error}",),
            records=(),
            problems=(f"unreadable carrier: {error}",),
        )
    if not isinstance(payload, dict):
        return CommentSetManifest(
            carrier_path=location,
            declarations=None,
            declaration_problems=("the carrier must be one JSON object",),
            records=(),
            problems=("the carrier must be one JSON object",),
        )

    declaration_problems: list[str] = []
    declarations = parse_declarations(payload, declaration_problems)
    record_problems: list[str] = []
    records = parse_comment_records(
        payload, declarations.proposed_path, record_problems
    )

    problems: list[str] = []
    base_source = ""
    proposed_source = ""
    base_units: tuple[CommentUnit, ...] = ()
    proposed_units: tuple[CommentUnit, ...] = ()
    adapter = get_adapter(declarations.host_adapter)
    if declarations.host_adapter and adapter is None:
        problems.append(
            f"no registered host adapter for {declarations.host_adapter!r}"
        )
    for attribute, relative in (
        ("base", declarations.base_path),
        ("proposed", declarations.proposed_path),
    ):
        if not relative:
            continue
        path = (carrier_path.parent / relative).resolve()
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as error:
            problems.append(f"unreadable {attribute} source: {error}")
            continue
        recorded = getattr(declarations, f"{attribute}_hash")
        if recorded and recorded != content_hash(source):
            problems.append(
                f"the recorded {attribute}_hash does not match "
                f"{relative}; re-extract before checking (Rule 8.6.2)"
            )
        if attribute == "base":
            base_source = source
        else:
            proposed_source = source
    if adapter is not None:
        if base_source:
            base_units = tuple(
                adapter.extract_comments(base_source, declarations.base_path)
            )
        if proposed_source:
            proposed_units = tuple(
                adapter.extract_comments(proposed_source, declarations.proposed_path)
            )

    return CommentSetManifest(
        carrier_path=location,
        declarations=declarations,
        declaration_problems=tuple(declaration_problems + record_problems),
        records=records,
        base_source=base_source,
        proposed_source=proposed_source,
        base_units=base_units,
        proposed_units=proposed_units,
        problems=tuple(problems),
        judgments=tuple(payload.get("judgments", ()) or ()),
        open_questions=tuple(payload.get("open_questions", ()) or ()),
    )


def comment_scan_path(manifest: CommentSetManifest) -> dict[str, object]:
    """Extract the Rule 4.13.9 scan path with no semantic verdict."""
    problems: list[str] = []
    segments: list[dict[str, object]] = []
    declarations = manifest.declarations
    if declarations is None or not declarations.change_set_id:
        problems.append("the scan path has no change-set ID (Rule 4.13.9)")
    else:
        segments.append(
            {"kind": "change-set-id", "text": declarations.change_set_id}
        )
    ordered = sorted(
        manifest.records, key=lambda record: (record.span.start_line, record.comment_id)
    )
    for record in ordered:
        anchor = record.anchor
        if anchor.construct:
            segments.append(
                {
                    "kind": "anchor",
                    "text": (
                        f"{anchor.construct}, lines "
                        f"{anchor.start_line}-{anchor.end_line}"
                    ),
                    "comment_id": record.comment_id,
                }
            )
        else:
            problems.append(
                f"comment {record.comment_id or '(unnamed)'} contributes no "
                "anchor to the scan path (Rule 4.13.9)"
            )
        if record.text:
            segments.append(
                {
                    "kind": "comment",
                    "text": record.text,
                    "comment_id": record.comment_id,
                }
            )
        else:
            problems.append(
                f"comment {record.comment_id or '(unnamed)'} contributes no "
                "text to the scan path (Rule 4.13.9)"
            )
    scan_text = "\n".join(
        "\x1f".join((str(segment["kind"]), str(segment["text"])))
        for segment in segments
    )
    return {
        "carrier_path": manifest.carrier_path,
        "scan_path_hash": content_hash(scan_text),
        "problems": problems,
        "segments": segments,
    }


def structural_manifest(manifest: CommentSetManifest) -> StructuralManifest:
    """Build a text-lint view of the governed comments.

    Each governed comment becomes one paragraph unit at its host span, so
    the shared phrase, sentence, and vocabulary checks read stripped comment
    text and report host line numbers. The view adds no headings and no
    semantic labels.
    """
    declarations = manifest.declarations
    path = declarations.proposed_path if declarations else manifest.carrier_path
    units: list[SourceUnit] = []
    for record in sorted(
        manifest.records, key=lambda item: (item.span.start_line, item.comment_id)
    ):
        if record.change == "removed" or not record.text:
            continue
        text = record.text
        if record.purpose == "marker":
            text = MARKER_PREFIX_RE.sub("", text)
        units.append(
            SourceUnit(
                id=f"c{record.span.start_line:05d}-{record.comment_id or 'unnamed'}",
                node_type="paragraph",
                span=record.span,
                text=text,
                source_hash=record.text_hash,
                heading_path=(),
                heading_level=0,
                parent_id="",
                previous_id="",
                next_id="",
                canonical_slot="",
                slot_evidence="",
                links=(),
                identifiers=(),
                fence_info="",
            )
        )
    document_declarations = None
    if declarations is not None:
        document_declarations = Declarations(
            itws_version=declarations.itws_version,
            profile=declarations.profile,
            span=SourceSpan(manifest.carrier_path, 0, 0),
        )
    line_count = len(manifest.proposed_source.splitlines())
    return StructuralManifest(
        path=path,
        document_hash=content_hash(manifest.proposed_source),
        declarations=document_declarations,
        declaration_problems=(),
        units=tuple(units),
        section_map=(),
        section_map_problems=(),
        line_count=max(line_count, 1),
    )

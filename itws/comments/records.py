"""Typed records for one comment change set and its declaration carrier.

The carrier is the §0.2.1 declaration surface of the `maintenance-comment`
profile. Every record converts to JSON only at the serialization edge, in a
fixed field order, so two runs over one carrier produce identical bytes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from itws.model import SourceSpan, content_hash
from itws.vocab import (
    COMMENT_CHANGES,
    COMMENT_LIFECYCLES,
    COMMENT_PURPOSES,
    HOST_ADAPTERS,
)

#: A durable work-item or issue reference inside a marker, such as
#: ``TASK-142`` or ``INC-31``, or an absolute URL.
MARKER_REFERENCE_RE = re.compile(r"^(?:[A-Z][A-Z0-9]*-\d+|https?://\S+)$")

#: The Rule 4.13.8 marker grammar: keyword, one reference, removal condition.
MARKER_GRAMMAR_RE = re.compile(
    r"^(?P<keyword>TODO|FIXME)\((?P<reference>[^()\s]+)\):\s*(?P<condition>\S)"
)

#: Detects that a comment is a marker at all, grammatical or not.
MARKER_RE = re.compile(r"\b(?:TODO|FIXME)\b")

#: The marker syntax that precedes a marker's prose. The shared text checks
#: strip it: the keyword and reference are comment syntax, not sentences.
MARKER_PREFIX_RE = re.compile(r"^(?:TODO|FIXME)(?:\([^)]*\))?:?\s*")


@dataclass(frozen=True)
class HostAnchor:
    """The host construct span one governed comment attaches to."""

    path: str
    start_line: int
    end_line: int
    construct: str
    anchor_hash: str

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "construct": self.construct,
            "anchor_hash": self.anchor_hash,
        }


@dataclass(frozen=True)
class CommentUnit:
    """One extracted comment span, before any carrier matching.

    ``text`` is the comment content with its markers stripped. ``excluded``
    records the adapter's conservative exclusion policy; an excluded unit is
    never governed.
    """

    span: SourceSpan
    text: str
    raw_text: str
    trailing: bool
    excluded: bool = False
    exclusion_reason: str = ""

    @property
    def text_hash(self) -> str:
        return content_hash(self.text)

    @property
    def is_marker(self) -> bool:
        return bool(MARKER_RE.search(self.text))

    def to_json(self) -> dict[str, object]:
        return {
            "span": self.span.to_json(),
            "text": self.text,
            "text_hash": self.text_hash,
            "trailing": self.trailing,
            "is_marker": self.is_marker,
            "excluded": self.excluded,
            "exclusion_reason": self.exclusion_reason,
        }


@dataclass(frozen=True)
class CommentRecord:
    """One governed comment's complete carrier record (Annex E §E.12)."""

    comment_id: str
    change: str
    anchor: HostAnchor
    span: SourceSpan
    text: str
    purpose: str
    information_delta: str
    basis: tuple[str, ...]
    basis_none_reason: str
    lifecycle: str
    removal_condition: str

    @property
    def text_hash(self) -> str:
        return content_hash(self.text)

    def to_json(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "comment_id": self.comment_id,
            "change": self.change,
            "anchor": self.anchor.to_json(),
            "span": self.span.to_json(),
            "text": self.text,
            "text_hash": self.text_hash,
            "purpose": self.purpose,
            "information_delta": self.information_delta,
            "basis": list(self.basis),
            "basis_none_reason": self.basis_none_reason,
            "lifecycle": self.lifecycle,
            "removal_condition": self.removal_condition,
        }
        return payload


@dataclass(frozen=True)
class CommentSetDeclarations:
    """The §0.4.3 declarations plus the change-set identity fields."""

    itws_version: str
    profile: str
    change_set_id: str
    host_adapter: str
    base_path: str
    base_hash: str
    proposed_path: str
    proposed_hash: str
    change_scope: str
    boundaries: str

    def to_json(self) -> dict[str, object]:
        return {
            "itws_version": self.itws_version,
            "profile": self.profile,
            "change_set_id": self.change_set_id,
            "host_adapter": self.host_adapter,
            "base_path": self.base_path,
            "base_hash": self.base_hash,
            "proposed_path": self.proposed_path,
            "proposed_hash": self.proposed_hash,
            "change_scope": self.change_scope,
            "boundaries": self.boundaries,
        }


def _string(payload: dict, key: str, problems: list[str], *, required: bool = True) -> str:
    value = payload.get(key, "")
    if not isinstance(value, str):
        problems.append(f"carrier field {key!r} must be a string")
        return ""
    if required and not value.strip():
        problems.append(f"missing carrier field: {key}")
    return value.strip()


def _string_list(payload: dict, key: str, problems: list[str]) -> tuple[str, ...]:
    value = payload.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        problems.append(f"carrier field {key!r} must be a list of strings")
        return ()
    return tuple(item.strip() for item in value if item.strip())


def _closed(
    value: str, allowed: tuple[str, ...], key: str, problems: list[str]
) -> str:
    if value and value not in allowed:
        problems.append(
            f"carrier field {key!r} has unknown value {value!r}; permitted: "
            + ", ".join(allowed)
        )
    return value


def parse_declarations(
    payload: dict, problems: list[str]
) -> CommentSetDeclarations:
    """Read the declaration fields, recording every defect found."""
    declarations = CommentSetDeclarations(
        itws_version=_string(payload, "itws_version", problems),
        profile=_string(payload, "profile", problems),
        change_set_id=_string(payload, "change_set_id", problems),
        host_adapter=_closed(
            _string(payload, "host_adapter", problems), HOST_ADAPTERS,
            "host_adapter", problems,
        ),
        base_path=_string(payload, "base_path", problems),
        base_hash=_string(payload, "base_hash", problems),
        proposed_path=_string(payload, "proposed_path", problems),
        proposed_hash=_string(payload, "proposed_hash", problems),
        change_scope=_string(payload, "change_scope", problems),
        boundaries=_string(payload, "boundaries", problems),
    )
    return declarations


def _parse_span(payload: dict, path: str, problems: list[str], label: str) -> SourceSpan:
    span = payload.get("span", {})
    if not isinstance(span, dict):
        problems.append(f"{label}: span must be an object")
        return SourceSpan(path, 0, 0)
    try:
        start = int(span.get("start_line", 0))
        end = int(span.get("end_line", 0))
    except (TypeError, ValueError):
        problems.append(f"{label}: span lines must be integers")
        return SourceSpan(path, 0, 0)
    if start <= 0 or end < start:
        problems.append(f"{label}: span {start}-{end} is not a valid line range")
    return SourceSpan(path, start, end)


def _parse_anchor(payload: dict, problems: list[str], label: str) -> HostAnchor:
    anchor = payload.get("anchor")
    if not isinstance(anchor, dict):
        problems.append(f"{label}: missing anchor object (Rule 4.13.3)")
        return HostAnchor("", 0, 0, "", "")
    local: list[str] = []
    record = HostAnchor(
        path=_string(anchor, "path", local),
        start_line=int(anchor.get("start_line", 0) or 0),
        end_line=int(anchor.get("end_line", 0) or 0),
        construct=_string(anchor, "construct", local),
        anchor_hash=_string(anchor, "anchor_hash", local),
    )
    problems.extend(f"{label}: {problem}" for problem in local)
    return record


def parse_comment_records(
    payload: dict, proposed_path: str, problems: list[str]
) -> tuple[CommentRecord, ...]:
    """Read the repeated comment records, recording every defect found."""
    raw_records = payload.get("comments", [])
    if not isinstance(raw_records, list):
        problems.append("carrier field 'comments' must be a list")
        return ()
    records: list[CommentRecord] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(raw_records):
        label = f"comment record {index + 1}"
        if not isinstance(raw, dict):
            problems.append(f"{label}: must be an object")
            continue
        local: list[str] = []
        comment_id = _string(raw, "comment_id", local)
        if comment_id:
            label = f"comment record {comment_id}"
            if comment_id in seen_ids:
                local.append("duplicate comment_id")
            seen_ids.add(comment_id)
        change = _closed(
            _string(raw, "change", local), COMMENT_CHANGES, "change", local
        )
        span_path = proposed_path if change != "removed" else _string(
            {"base_path": payload.get("base_path", "")}, "base_path", []
        )
        record = CommentRecord(
            comment_id=comment_id,
            change=change,
            anchor=_parse_anchor(raw, local, label),
            span=_parse_span(raw, span_path or proposed_path, local, label),
            text=_string(raw, "text", local),
            purpose=_string(raw, "purpose", local),
            information_delta=_string(raw, "information_delta", local),
            basis=_string_list(raw, "basis", local),
            basis_none_reason=_string(raw, "basis_none_reason", local, required=False),
            lifecycle=_closed(
                _string(raw, "lifecycle", local), COMMENT_LIFECYCLES,
                "lifecycle", local,
            ),
            removal_condition=_string(raw, "removal_condition", local, required=False),
        )
        problems.extend(f"{label}: {problem}" for problem in local)
        records.append(record)
    return tuple(records)

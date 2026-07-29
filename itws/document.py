"""Structural indexing of a governed Markdown document.

This module records syntax, never meaning. It may say that a span is a
heading, a paragraph, a list, a quotation, a code fence, a table, or a link.
It never says that the span is a claim, a requirement, a caveat, an exact
item, a plain rendering, a definition, an observation, or an interpretation.
Section 1.6.1 reserves those judgments for a reader or an agent, which
records them through :mod:`itws.analysis`.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from itws.model import Skeleton, SourceSpan, content_hash
from itws.vocab import PROFILE_IDS, TIERS

DECLARATION_VERSION_RE = re.compile(r"^ITWS version:\s*(?P<value>\S+)\s*$")
DECLARATION_PROFILE_RE = re.compile(r"^Profile:\s*(?P<value>[A-Za-z-]+)\s*$")
DECLARATION_TIER_RE = re.compile(r"^Conformance tier:\s*(?P<value>[a-z]+)\s*$")

HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.+?)\s*$")
SETEXT_H1_RE = re.compile(r"^=+\s*$")
SETEXT_H2_RE = re.compile(r"^-{2,}\s*$")
FENCE_RE = re.compile(r"^(?P<indent> *)(?P<fence>```+|~~~+)(?P<info>.*)$")
LIST_ITEM_RE = re.compile(r"^ *(?:[-*+]|\d+[.)])\s+")
TABLE_ROW_RE = re.compile(r"^ *\|.*\|\s*$")
QUOTE_RE = re.compile(r"^ *> ?")
LINK_RE = re.compile(r"\[(?P<label>[^\]]*)\]\((?P<target>[^)]*)\)")
BARE_URL_RE = re.compile(r"(?<![(\w])(?P<url>https?://[^\s)\]]+)")
IDENTIFIER_RE = re.compile(r"\b(?:[A-Z]{1,4}-\d+|CC-\d+|INV-\d+|SP-\d+)\b")
SECTION_MAP_FENCE = "itws-section-map"
SECTION_MAP_LINE_RE = re.compile(
    r'^(?:"(?P<quoted>[^"]+)"|(?P<plain>[^"][^-]*?))\s*->\s*(?P<slot>.+?)\s*$'
)

NODE_TYPES = (
    "heading",
    "paragraph",
    "list",
    "table",
    "code_fence",
    "block_quote",
    "declaration",
    "section_map",
    "thematic_break",
)


@dataclass(frozen=True)
class Declarations:
    """The three §0.4.3 declaration fields, as the document states them."""

    itws_version: str
    profile: str
    tier: str
    span: SourceSpan

    def to_json(self) -> dict[str, object]:
        return {
            "itws_version": self.itws_version,
            "profile": self.profile,
            "conformance_tier": self.tier,
            "source_span": self.span.to_json(),
        }


@dataclass(frozen=True)
class SourceUnit:
    """One structural span of the document, with no semantic label."""

    id: str
    node_type: str
    span: SourceSpan
    text: str
    source_hash: str
    heading_path: tuple[str, ...]
    heading_level: int
    parent_id: str
    previous_id: str
    next_id: str
    canonical_slot: str
    slot_evidence: str
    links: tuple[tuple[str, str], ...]
    identifiers: tuple[str, ...]
    fence_info: str

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "node_type": self.node_type,
            "source_span": self.span.to_json(),
            "text": self.text,
            "source_hash": self.source_hash,
            "heading_path": list(self.heading_path),
            "heading_level": self.heading_level,
            "parent_id": self.parent_id,
            "previous_id": self.previous_id,
            "next_id": self.next_id,
            "canonical_slot": self.canonical_slot,
            "slot_evidence": self.slot_evidence,
            "links": [{"label": label, "target": target} for label, target in self.links],
            "identifiers": list(self.identifiers),
            "fence_info": self.fence_info,
        }


@dataclass(frozen=True)
class SectionMapEntry:
    heading: str
    slot: str
    span: SourceSpan

    def to_json(self) -> dict[str, object]:
        return {
            "heading": self.heading,
            "slot": self.slot,
            "source_span": self.span.to_json(),
        }


@dataclass
class StructuralManifest:
    """The generated description of one document's structure."""

    path: str
    document_hash: str
    declarations: Declarations | None
    declaration_problems: tuple[str, ...]
    units: tuple[SourceUnit, ...]
    section_map: tuple[SectionMapEntry, ...]
    section_map_problems: tuple[str, ...]
    line_count: int
    artifact_manifest_hash: str = ""
    profile_envelope: tuple[str, ...] = ()

    def unit(self, unit_id: str) -> SourceUnit | None:
        for candidate in self.units:
            if candidate.id == unit_id:
                return candidate
        return None

    def units_in_range(self, start: int, end: int) -> tuple[SourceUnit, ...]:
        return tuple(
            unit
            for unit in self.units
            if not (unit.span.end_line < start or unit.span.start_line > end)
        )

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "document_hash": self.document_hash,
            "line_count": self.line_count,
            "declarations": (
                self.declarations.to_json() if self.declarations else None
            ),
            "declaration_problems": list(self.declaration_problems),
            "section_map": [entry.to_json() for entry in self.section_map],
            "section_map_problems": list(self.section_map_problems),
            "artifact_manifest_hash": self.artifact_manifest_hash,
            "profile_envelope": list(self.profile_envelope),
            "units": [unit.to_json() for unit in self.units],
        }


def _span_id(path: str, start: int, end: int, heading_path: tuple[str, ...], text: str) -> str:
    """Build a run-stable identifier for one source unit.

    The identifier covers the document identity, the source range, the
    heading path, and the original content. It identifies a source unit
    during one rewrite run. It does not claim that the unit is one §4.1
    chunk.
    """
    digest = hashlib.sha256()
    digest.update(path.encode("utf-8"))
    digest.update(f"{start}:{end}".encode("utf-8"))
    digest.update("".join(heading_path).encode("utf-8"))
    digest.update(text.encode("utf-8"))
    return f"u{start:05d}-{digest.hexdigest()[:10]}"


def _parse_declarations(
    lines: list[str], path: str
) -> tuple[Declarations | None, list[str]]:
    """Read the three declaration lines, rejecting repeats and conflicts."""
    found: dict[str, list[tuple[int, str]]] = {
        "itws_version": [],
        "profile": [],
        "tier": [],
    }
    for index, line in enumerate(lines):
        stripped = line.strip()
        for key, matcher in (
            ("itws_version", DECLARATION_VERSION_RE),
            ("profile", DECLARATION_PROFILE_RE),
            ("tier", DECLARATION_TIER_RE),
        ):
            match = matcher.match(stripped)
            if match:
                found[key].append((index + 1, match.group("value")))

    problems: list[str] = []
    for key, hits in found.items():
        if not hits:
            problems.append(f"missing declaration: {key}")
        elif len({value for _, value in hits}) > 1:
            lines_seen = ", ".join(str(number) for number, _ in hits)
            problems.append(
                f"conflicting {key} declarations on lines {lines_seen}"
            )
        elif len(hits) > 1:
            lines_seen = ", ".join(str(number) for number, _ in hits)
            problems.append(f"repeated {key} declaration on lines {lines_seen}")

    conflicted = any(
        len({value for _, value in hits}) > 1 for hits in found.values()
    )
    if conflicted or any(not hits for hits in found.values()):
        # A conflicting or absent declaration leaves no single declared value.
        # §0.4.4 checks a document against the version it declares, so an
        # ambiguous declaration resolves to none at all.
        return None, problems

    profile = found["profile"][0][1]
    tier = found["tier"][0][1]
    if profile not in PROFILE_IDS:
        problems.append(f"unknown profile ID: {profile}")
    if tier not in TIERS:
        problems.append(f"unknown conformance tier: {tier}")

    start = min(hits[0][0] for hits in found.values())
    end = max(hits[-1][0] for hits in found.values())
    return (
        Declarations(
            itws_version=found["itws_version"][0][1],
            profile=profile,
            tier=tier,
            span=SourceSpan(path, start, end),
        ),
        problems,
    )


def _parse_section_map(
    lines: list[str], path: str, skeleton: Skeleton | None
) -> tuple[list[SectionMapEntry], list[str]]:
    """Parse the optional ``itws-section-map`` block of §E.0.2."""
    entries: list[SectionMapEntry] = []
    problems: list[str] = []
    blocks = 0
    index = 0
    while index < len(lines):
        fence = FENCE_RE.match(lines[index])
        if not fence or fence.group("info").strip() != SECTION_MAP_FENCE:
            index += 1
            continue
        blocks += 1
        marker = fence.group("fence")
        index += 1
        while index < len(lines) and not lines[index].strip().startswith(marker):
            raw = lines[index].strip()
            index += 1
            if not raw or raw.startswith("#"):
                continue
            match = SECTION_MAP_LINE_RE.match(raw)
            if not match:
                problems.append(f"line {index}: malformed section-map entry {raw!r}")
                continue
            heading = (match.group("quoted") or match.group("plain") or "").strip()
            entries.append(
                SectionMapEntry(
                    heading=heading,
                    slot=match.group("slot").strip(),
                    span=SourceSpan(path, index, index),
                )
            )
        index += 1

    if blocks > 1:
        problems.append("a document declares at most one section map")

    seen_headings: set[str] = set()
    seen_slots: set[str] = set()
    for entry in entries:
        key = entry.heading.casefold()
        if key in seen_headings:
            problems.append(f"section map repeats heading {entry.heading!r}")
        seen_headings.add(key)
        if entry.slot in seen_slots:
            problems.append(f"section map repeats slot {entry.slot!r}")
        seen_slots.add(entry.slot)
        if skeleton is not None and skeleton.slot(entry.slot) is None:
            merged = {merge.combined for merge in skeleton.merges}
            if entry.slot not in merged:
                problems.append(
                    f"section map names slot {entry.slot!r}, which is absent "
                    f"from the {skeleton.profile} skeleton"
                )
    return entries, problems


def _flush(
    buffer: list[str],
    start: int,
    node_type: str,
    fence_info: str,
) -> tuple[str, int, int, str] | None:
    while buffer and not buffer[-1].strip():
        buffer.pop()
    if not buffer:
        return None
    return "\n".join(buffer), start, start + len(buffer) - 1, node_type


def parse_document(
    path: Path, *, skeleton: Skeleton | None = None
) -> StructuralManifest:
    """Parse a governed Markdown document into a structural manifest."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    location = path.as_posix()

    declarations, declaration_problems = _parse_declarations(lines, location)
    section_map, section_map_problems = _parse_section_map(lines, location, skeleton)
    explicit_slots = {
        entry.heading.casefold(): entry.slot for entry in section_map
    }

    raw_units: list[tuple[str, int, int, str, tuple[str, ...], int, str]] = []
    heading_stack: list[tuple[int, str]] = []
    buffer: list[str] = []
    buffer_start = 0
    buffer_type = "paragraph"
    fence_marker = ""
    fence_info = ""

    def current_path() -> tuple[str, ...]:
        return tuple(title for _, title in heading_stack)

    def flush() -> None:
        nonlocal buffer, buffer_start, buffer_type, fence_info
        result = _flush(buffer, buffer_start, buffer_type, fence_info)
        if result:
            body, start, end, node_type = result
            raw_units.append(
                (body, start, end, node_type, current_path(), 0, fence_info)
            )
        buffer = []
        buffer_type = "paragraph"
        fence_info = ""

    index = 0
    while index < len(lines):
        line = lines[index]
        line_number = index + 1

        if fence_marker:
            buffer.append(line)
            if line.strip().startswith(fence_marker):
                flush()
                fence_marker = ""
            index += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            flush()
            fence_marker = fence.group("fence")
            fence_info = fence.group("info").strip()
            buffer = [line]
            buffer_start = line_number
            buffer_type = "code_fence"
            index += 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            flush()
            level = len(heading.group("hashes"))
            title = heading.group("text").rstrip("#").strip()
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            raw_units.append(
                (
                    line,
                    line_number,
                    line_number,
                    "heading",
                    current_path() + (title,),
                    level,
                    "",
                )
            )
            heading_stack.append((level, title))
            index += 1
            continue

        if not line.strip():
            flush()
            index += 1
            continue

        if re.fullmatch(r" *([-*_]) *(\1 *){2,}", line):
            flush()
            raw_units.append(
                (line, line_number, line_number, "thematic_break", current_path(), 0, "")
            )
            index += 1
            continue

        if QUOTE_RE.match(line):
            node_type = "block_quote"
        elif LIST_ITEM_RE.match(line):
            node_type = "list"
        elif TABLE_ROW_RE.match(line):
            node_type = "table"
        else:
            node_type = "paragraph"

        if not buffer:
            buffer_start = line_number
            buffer_type = node_type
        elif node_type != buffer_type and node_type in {"list", "table", "block_quote"}:
            flush()
            buffer_start = line_number
            buffer_type = node_type
        buffer.append(line)
        index += 1

    flush()

    units: list[SourceUnit] = []
    heading_ids: dict[tuple[str, ...], str] = {}
    for position, (body, start, end, node_type, path_tuple, level, info) in enumerate(
        raw_units
    ):
        unit_id = _span_id(location, start, end, path_tuple, body)
        parent_key = path_tuple[:-1] if node_type == "heading" else path_tuple
        parent_id = heading_ids.get(parent_key, "")
        canonical_slot = ""
        slot_evidence = ""
        if node_type == "heading":
            heading_ids[path_tuple] = unit_id
            title = path_tuple[-1]
            mapped = explicit_slots.get(title.casefold())
            if mapped:
                canonical_slot = mapped
                slot_evidence = "section-map"
            elif skeleton is not None:
                resolved = skeleton.canonical_for_heading(title)
                if resolved:
                    canonical_slot = resolved
                    slot_evidence = (
                        "exact-name"
                        if skeleton.slot(resolved)
                        and skeleton.slot(resolved).name.casefold()
                        == title.strip().rstrip(".").casefold()
                        else "permitted-rename"
                    )
        units.append(
            SourceUnit(
                id=unit_id,
                node_type=node_type,
                span=SourceSpan(location, start, end),
                text=body,
                source_hash=content_hash(body),
                heading_path=path_tuple,
                heading_level=level,
                parent_id=parent_id,
                previous_id="",
                next_id="",
                canonical_slot=canonical_slot,
                slot_evidence=slot_evidence,
                links=tuple(
                    (match.group("label"), match.group("target"))
                    for match in LINK_RE.finditer(body)
                )
                + tuple(("", match.group("url")) for match in BARE_URL_RE.finditer(body)),
                identifiers=tuple(dict.fromkeys(IDENTIFIER_RE.findall(body))),
                fence_info=info,
            )
        )

    linked: list[SourceUnit] = []
    for position, unit in enumerate(units):
        previous_id = units[position - 1].id if position else ""
        next_id = units[position + 1].id if position + 1 < len(units) else ""
        linked.append(
            SourceUnit(
                **{
                    **unit.__dict__,
                    "previous_id": previous_id,
                    "next_id": next_id,
                }
            )
        )

    return StructuralManifest(
        path=location,
        document_hash=content_hash(text),
        declarations=declarations,
        declaration_problems=tuple(declaration_problems),
        units=tuple(linked),
        section_map=tuple(section_map),
        section_map_problems=tuple(section_map_problems),
        line_count=len(lines),
    )


def outline(manifest: StructuralManifest) -> list[dict[str, object]]:
    """Return the heading outline with source spans and no semantic labels."""
    return [
        {
            "id": unit.id,
            "level": unit.heading_level,
            "heading": unit.heading_path[-1] if unit.heading_path else "",
            "canonical_slot": unit.canonical_slot,
            "slot_evidence": unit.slot_evidence,
            "start_line": unit.span.start_line,
            "end_line": unit.span.end_line,
        }
        for unit in manifest.units
        if unit.node_type == "heading"
    ]

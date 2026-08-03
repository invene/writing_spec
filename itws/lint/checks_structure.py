"""Part 4 and Part 6 checks: declarations, skeleton, navigation, formatting."""

from __future__ import annotations

import re
from typing import Iterable

from itws.document import scan_path
from itws.lint.model import Finding, LintContext
from itws.lint.registry import register
from itws.lint.text import (
    BOUNDED_BLOCK_RE,
    CROSS_REFERENCE_RE,
    POSITIONAL_REFERENCE_RE,
    admissions,
    body_units,
    counted_word_length,
    document_words,
    prose_units,
    split_sentences,
    strip_inline_markup,
)

PERMITTED_BLOCK_LABELS = ("Detail", "Intuition", "Speculation")
RECALL_OPENER_RE = re.compile(r"^\s*(?:\*\*)?Recall:", re.IGNORECASE)
ALT_TEXT_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\([^)]*\)")
MERMAID_INFO = {"mermaid"}


def _headings(context: LintContext):
    return [unit for unit in context.manifest.units if unit.node_type == "heading"]


def _hosted_surface(context: LintContext) -> bool:
    """Whether the declared profile governs a hosted comment set.

    A hosted surface has no headings and keeps its skeleton in the
    declaration carrier, so the heading-driven checks below do not apply;
    `itws.lint.checks_comments` covers the carrier instead (§0.2.1).
    """
    profile = context.spec.profile(context.profile)
    return profile is not None and profile.surface == "hosted-comment-set"


@register("4.3.1", name="profile-declaration")
def profile_declaration(context: LintContext) -> Iterable[Finding]:
    """The document declares exactly one canonical profile ID."""
    manifest = context.manifest
    findings: list[Finding] = []
    for problem in manifest.declaration_problems:
        findings.append(
            Finding(
                rule="4.3.1",
                severity=context.severity_for("4.3.1"),
                kind="violation",
                message=f"{problem} (§4.3.1, §0.4.3)",
                path=manifest.path,
                start_line=1,
                end_line=min(manifest.line_count, 20),
                checker="profile-declaration",
            )
        )
    return findings


@register("4.3.3", name="required-slots")
def required_slots(context: LintContext) -> Iterable[Finding]:
    """Every required Annex E slot is present, in the skeleton's order."""
    if _hosted_surface(context):
        return []
    skeleton = context.spec.skeleton(context.profile)
    if skeleton is None:
        return []
    present: dict[str, int] = {}
    for unit in _headings(context):
        if unit.canonical_slot:
            present.setdefault(unit.canonical_slot, unit.span.start_line)
    merged = {
        part: merge.combined
        for merge in skeleton.merges
        for part in merge.parts
        if merge.combined in present
    }
    findings: list[Finding] = []
    for slot in skeleton.slots:
        if not slot.required:
            continue
        if slot.name in present or slot.name in merged:
            continue
        if slot.parent and slot.parent not in present and slot.parent not in merged:
            continue
        findings.append(
            Finding(
                rule="4.3.3",
                severity=context.severity_for("4.3.3"),
                kind="violation",
                message=(
                    f"required Annex E slot {slot.name!r} has no heading, permitted "
                    "rename, or section-map entry (§4.3.3)"
                ),
                path=context.manifest.path,
                start_line=1,
                end_line=1,
                checker="required-slots",
                excerpt=slot.name,
            )
        )
    return findings


@register("4.4.1", name="skeleton-order")
def skeleton_order(context: LintContext) -> Iterable[Finding]:
    """Resolved slots appear in the order the skeleton fixes."""
    if _hosted_surface(context):
        return []
    skeleton = context.spec.skeleton(context.profile)
    if skeleton is None:
        return []
    order = {slot.name: slot.order for slot in skeleton.slots}
    repeating = {slot.name for slot in skeleton.slots if slot.repeats}
    seen: list[tuple[int, str, int]] = []
    for unit in _headings(context):
        if unit.canonical_slot not in order:
            continue
        if unit.canonical_slot in repeating:
            # A repeating slot restarts the sequence: an investigation log's
            # second entry legitimately returns to the entry's first job.
            seen = []
        seen.append(
            (order[unit.canonical_slot], unit.canonical_slot, unit.span.start_line)
        )
    findings: list[Finding] = []
    for previous, current in zip(seen, seen[1:]):
        if current[0] < previous[0]:
            findings.append(
                Finding(
                    rule="4.4.1",
                    severity=context.severity_for("4.4.1"),
                    kind="violation",
                    message=(
                        f"slot {current[1]!r} appears after {previous[1]!r}; the "
                        f"{context.profile} skeleton fixes the reverse order (§4.4.1)"
                    ),
                    path=context.manifest.path,
                    start_line=previous[2],
                    end_line=current[2],
                    checker="skeleton-order",
                    excerpt=current[1],
                )
            )
    return findings


@register("4.6.2", name="bounded-block-markup")
def bounded_block_markup(context: LintContext) -> Iterable[Finding]:
    """A bounded block carries exactly one permitted label."""
    findings: list[Finding] = []
    for unit in context.manifest.units:
        if unit.node_type != "block_quote":
            continue
        matches = BOUNDED_BLOCK_RE.findall(unit.text)
        if not matches:
            continue
        if len(matches) > 1:
            findings.append(
                Finding(
                    rule="4.6.2",
                    severity=context.severity_for("4.6.2"),
                    kind="violation",
                    message="a bounded block carries more than one label (§4.6.2)",
                    path=unit.span.path,
                    start_line=unit.span.start_line,
                    end_line=unit.span.end_line,
                    checker="bounded-block-markup",
                )
            )
        for label, topic in matches:
            if label not in PERMITTED_BLOCK_LABELS:
                findings.append(
                    Finding(
                        rule="4.6.2",
                        severity=context.severity_for("4.6.2"),
                        kind="violation",
                        message=(
                            f"bounded-block label {label!r} is not Detail, "
                            "Intuition, or Speculation (§4.6.2)"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line,
                        end_line=unit.span.end_line,
                        checker="bounded-block-markup",
                        excerpt=label,
                    )
                )
            elif not topic:
                findings.append(
                    Finding(
                        rule="4.6.2",
                        severity=context.severity_for("4.6.2"),
                        kind="violation",
                        message=(
                            f"the {label} block names no topic; §4.6.2 requires "
                            f"**[{label} — <topic>]**"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line,
                        end_line=unit.span.end_line,
                        checker="bounded-block-markup",
                        excerpt=label,
                    )
                )
    return findings


@register("4.7.3", name="positional-cross-reference")
def positional_cross_reference(context: LintContext) -> Iterable[Finding]:
    """A cross-reference cites a number, not a position."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            plain = strip_inline_markup(line)
            for match in POSITIONAL_REFERENCE_RE.finditer(plain):
                findings.append(
                    Finding(
                        rule="4.7.3",
                        severity=context.severity_for("4.7.3"),
                        kind="violation",
                        message=(
                            f"{match.group(0)!r} locates content by position; "
                            "§4.7.3 requires a numbered section, figure, or table"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line + line_offset,
                        end_line=unit.span.start_line + line_offset,
                        checker="positional-cross-reference",
                        excerpt=match.group(0),
                    )
                )
    return findings


@register("4.8.1", name="admission-density")
def admission_density(context: LintContext) -> Iterable[Finding]:
    """At most three admissions per 500-word page."""
    words = document_words(context.manifest)
    if not words:
        return []
    page_of_line: dict[int, int] = {}
    for position, (_, line) in enumerate(words):
        page_of_line.setdefault(line, position // 500 + 1)

    pages: dict[int, list[tuple[str, int]]] = {}
    for term, line, _ in admissions(context.manifest):
        page = page_of_line.get(line)
        if page is None:
            continue
        pages.setdefault(page, []).append((term, line))

    findings: list[Finding] = []
    for page, entries in sorted(pages.items()):
        if len(entries) <= 3:
            continue
        findings.append(
            Finding(
                rule="4.8.1",
                severity=context.severity_for("4.8.1"),
                kind="violation",
                message=(
                    f"page {page} admits {len(entries)} terms "
                    f"({', '.join(term for term, _ in entries)}); §4.8.1 caps a "
                    "500-word page at three"
                ),
                path=context.manifest.path,
                start_line=entries[0][1],
                end_line=entries[-1][1],
                checker="admission-density",
            )
        )
    return findings


def _section_word_counts(context: LintContext, level: int) -> list[tuple[str, int, int, int]]:
    """Word counts per section at ``level``.

    A section ends at the next heading of the same level or shallower, so a
    subsection never absorbs the sections that follow its parent.
    """
    sections: list[tuple[str, int, int, int]] = []
    all_headings = [
        unit for unit in context.manifest.units if unit.node_type == "heading"
    ]
    headings = [unit for unit in all_headings if unit.heading_level == level]
    for heading in headings:
        following = [
            unit
            for unit in all_headings
            if unit.span.start_line > heading.span.start_line
            and unit.heading_level <= level
        ]
        end = (
            following[0].span.start_line - 1
            if following
            else context.manifest.line_count
        )
        total = sum(
            counted_word_length(unit.text)
            for unit in context.manifest.units_in_range(heading.span.start_line, end)
            if unit.node_type in {"paragraph", "list", "block_quote"}
        )
        sections.append(
            (heading.heading_path[-1], heading.span.start_line, end, total)
        )
    return sections


@register("4.8.2", name="section-length")
def section_length(context: LintContext) -> Iterable[Finding]:
    """A section stays under 1,500 words."""
    return [
        Finding(
            rule="4.8.2",
            severity=context.severity_for("4.8.2"),
            kind="violation",
            message=f"section {name!r} holds {total} words; §4.8.2 caps it at 1,500",
            path=context.manifest.path,
            start_line=start,
            end_line=end,
            checker="section-length",
            excerpt=name,
        )
        for name, start, end, total in _section_word_counts(context, 2)
        if total > 1500
    ]


@register("4.8.3", name="subsection-length")
def subsection_length(context: LintContext) -> Iterable[Finding]:
    """A subsection stays under 600 words."""
    return [
        Finding(
            rule="4.8.3",
            severity=context.severity_for("4.8.3"),
            kind="violation",
            message=f"subsection {name!r} holds {total} words; §4.8.3 caps it at 600",
            path=context.manifest.path,
            start_line=start,
            end_line=end,
            checker="subsection-length",
            excerpt=name,
        )
        for name, start, end, total in _section_word_counts(context, 3)
        if total > 600
    ]


@register("4.10.1", name="heading-case")
def heading_case(context: LintContext) -> Iterable[Finding]:
    """A heading uses sentence case."""
    findings: list[Finding] = []
    for unit in _headings(context):
        title = unit.heading_path[-1] if unit.heading_path else ""
        words = [word for word in strip_inline_markup(title).split() if word]
        if len(words) < 3:
            continue
        capitalized = [
            word
            for word in words[1:]
            if word[:1].isupper() and not word.isupper() and word.isalpha()
        ]
        if len(capitalized) >= max(2, (len(words) - 1) // 2):
            findings.append(
                Finding(
                    rule="4.10.1",
                    severity=context.severity_for("4.10.1"),
                    kind="violation",
                    message=(
                        f"heading {title!r} looks like title case; §4.10.1 requires "
                        "sentence case"
                    ),
                    path=unit.span.path,
                    start_line=unit.span.start_line,
                    end_line=unit.span.end_line,
                    checker="heading-case",
                    excerpt=title,
                )
            )
    return findings


@register("4.12.1", name="scan-path-structure")
def scan_path_structure(context: LintContext) -> Iterable[Finding]:
    """Report syntax that prevents a complete Rule 4.12.1 extraction."""
    if _hosted_surface(context):
        # Rule 4.13.9 replaces the Rule 4.12.1 path on a hosted comment
        # set; the comment-scan-path checker covers it.
        return []
    result = scan_path(context.manifest)
    findings: list[Finding] = []
    for problem in result.problems:
        line_match = re.search(r"\bline (\d+)\b", problem)
        line = int(line_match.group(1)) if line_match else 1
        findings.append(
            Finding(
                rule="4.12.1",
                severity=context.severity_for("4.12.1"),
                kind="candidate",
                message=problem,
                path=context.manifest.path,
                start_line=line,
                end_line=line,
                checker="scan-path-structure",
            )
        )
    return findings


@register("4.12.3", name="scan-qualification-candidate")
def scan_qualification_candidate(context: LintContext) -> Iterable[Finding]:
    """Flag scan sentences whose qualification may disappear while skimming."""
    entries = [
        entry
        for entry in context.spec.phrase_lists
        if entry.rule == "4.12.3"
    ]
    matchers = [
        (
            entry,
            re.compile(
                entry.pattern,
                re.IGNORECASE if entry.ignore_case else 0,
            ),
        )
        for entry in entries
    ]
    findings: list[Finding] = []
    for segment in scan_path(context.manifest).segments:
        if not segment.opening_sentence:
            continue
        for entry, matcher in matchers:
            match = matcher.search(segment.opening_sentence)
            if not match:
                continue
            findings.append(
                Finding(
                    rule="4.12.3",
                    severity=context.severity_for("4.12.3"),
                    kind="candidate",
                    message=(
                        f"{match.group(0)!r} may carry a scan-path qualification; "
                        "confirm that affirmative content words preserve the "
                        "assertion's status, strength, and boundary (§4.12.3)"
                    ),
                    path=context.manifest.path,
                    start_line=segment.opening_line,
                    end_line=segment.opening_line,
                    checker=f"phrase-list:{entry.id}",
                    excerpt=segment.opening_sentence,
                )
            )
    return findings


@register("6.3.1", name="intuition-block-form")
def intuition_block_form(context: LintContext) -> Iterable[Finding]:
    """An Intuition label appears only inside a blockquote."""
    findings: list[Finding] = []
    for unit in context.manifest.units:
        if unit.node_type == "block_quote":
            continue
        for match in BOUNDED_BLOCK_RE.finditer(unit.text):
            if match.group("label") != "Intuition":
                continue
            findings.append(
                Finding(
                    rule="6.3.1",
                    severity=context.severity_for("6.3.1"),
                    kind="violation",
                    message=(
                        "an Intuition label appears outside a blockquote; §6.3.1 "
                        "requires the bounded intuition-block form"
                    ),
                    path=unit.span.path,
                    start_line=unit.span.start_line,
                    end_line=unit.span.end_line,
                    checker="intuition-block-form",
                    excerpt=match.group(0),
                )
            )
    return findings


def _figures(context: LintContext):
    """Return every figure: an image, a mermaid fence, or a numbered caption."""
    found = []
    for unit in context.manifest.units:
        if unit.node_type == "code_fence" and unit.fence_info in MERMAID_INFO:
            found.append((unit, ""))
        for match in ALT_TEXT_RE.finditer(unit.text):
            found.append((unit, match.group("alt")))
    return found


@register("6.4.2", name="diagram-referenced")
def diagram_referenced(context: LintContext) -> Iterable[Finding]:
    """Every diagram is referenced from the main text by its number."""
    figures = _figures(context)
    if not figures:
        return []
    references = set()
    for unit in body_units(context.manifest):
        for match in re.finditer(r"\b(?:Figure|Diagram) (\d+)", unit.text):
            references.add(match.group(1))
    findings: list[Finding] = []
    numbered = 0
    for unit, _alt in figures:
        caption = re.search(r"\b(?:Figure|Diagram) (\d+)", unit.text)
        if caption:
            numbered += 1
            if caption.group(1) not in references:
                findings.append(
                    Finding(
                        rule="6.4.2",
                        severity=context.severity_for("6.4.2"),
                        kind="violation",
                        message=(
                            f"Figure {caption.group(1)} is never referenced from "
                            "the main text (§6.4.2)"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line,
                        end_line=unit.span.end_line,
                        checker="diagram-referenced",
                    )
                )
        else:
            findings.append(
                Finding(
                    rule="6.4.2",
                    severity=context.severity_for("6.4.2"),
                    kind="violation",
                    message=(
                        "a diagram carries no number, so the main text cannot "
                        "reference it by number (§6.4.2)"
                    ),
                    path=unit.span.path,
                    start_line=unit.span.start_line,
                    end_line=unit.span.end_line,
                    checker="diagram-referenced",
                )
            )
    return findings


@register("6.4.3", name="diagram-terms")
def diagram_terms(context: LintContext) -> Iterable[Finding]:
    """Diagram text uses assumed or previously admitted terms only."""
    admitted = {term.casefold() for term, _, _ in admissions(context.manifest)}
    glossary = {entry.term.casefold() for entry in context.spec.glossary}
    findings: list[Finding] = []
    for unit in context.manifest.units:
        if unit.node_type != "code_fence" or unit.fence_info not in MERMAID_INFO:
            continue
        for label in re.findall(r'"([^"]{2,60})"|\[([^\]\n]{2,60})\]', unit.text):
            text = (label[0] or label[1]).strip()
            for word in re.findall(r"[A-Za-z][A-Za-z\-]{2,}", text):
                key = word.casefold()
                if key in glossary and key not in admitted:
                    findings.append(
                        Finding(
                            rule="6.4.3",
                            severity=context.severity_for("6.4.3"),
                            kind="violation",
                            message=(
                                f"diagram label uses {word!r}, an Annex A term this "
                                "document has not admitted (§6.4.3)"
                            ),
                            path=unit.span.path,
                            start_line=unit.span.start_line,
                            end_line=unit.span.end_line,
                            checker="diagram-terms",
                            excerpt=text,
                        )
                    )
    return findings


#: Alt text that names the artifact instead of stating what it shows. Rule
#: 6.4.4's own non-compliant example, `alt="diagram"`, is one of these.
PLACEHOLDER_ALT = frozenset(
    {
        "diagram",
        "image",
        "figure",
        "picture",
        "photo",
        "screenshot",
        "chart",
        "graph",
        "illustration",
        "alt text",
        "todo",
    }
)


@register("6.4.4", name="diagram-alt-text")
def diagram_alt_text(context: LintContext) -> Iterable[Finding]:
    """Every diagram carries alt text that says what it shows.

    Absence, emptiness, and a bare placeholder are decided here. Whether
    real alt text states the diagram's point in its labels' admitted terms
    is a reader's judgment, which is why Rule 6.4.4 is `partial`.
    """
    findings: list[Finding] = []
    for unit in context.manifest.units:
        for match in ALT_TEXT_RE.finditer(unit.text):
            alt = match.group("alt").strip()
            if not alt:
                message = "the image carries no alt text (§6.4.4)"
            elif alt.strip(".!\"' ").casefold() in PLACEHOLDER_ALT:
                message = (
                    f"the alt text {alt!r} names the artifact instead of "
                    "stating what it shows (§6.4.4)"
                )
            else:
                continue
            findings.append(
                Finding(
                    rule="6.4.4",
                    severity=context.severity_for("6.4.4"),
                    kind="violation",
                    message=message,
                    path=unit.span.path,
                    start_line=unit.span.start_line,
                    end_line=unit.span.end_line,
                    checker="diagram-alt-text",
                    excerpt=alt,
                )
            )
    return findings


@register("6.5.2", name="distant-reuse")
def distant_reuse(context: LintContext) -> Iterable[Finding]:
    """An admitted term reused after 2,500 words carries a recall or reference."""
    words = document_words(context.manifest)
    position_of_line: dict[int, int] = {}
    for position, (_, line) in enumerate(words):
        position_of_line.setdefault(line, position)

    findings: list[Finding] = []
    for term, admitted_line, _ in admissions(context.manifest):
        pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
        admitted_position = position_of_line.get(admitted_line, 0)
        last_position = admitted_position
        for unit in body_units(context.manifest):
            for line_offset, line in enumerate(unit.text.splitlines()):
                line_number = unit.span.start_line + line_offset
                if line_number <= admitted_line:
                    continue
                if not pattern.search(strip_inline_markup(line)):
                    continue
                position = position_of_line.get(line_number, last_position)
                if position - last_position > 2500:
                    supported = bool(
                        CROSS_REFERENCE_RE.search(line)
                        or RECALL_OPENER_RE.match(line)
                    )
                    if not supported:
                        findings.append(
                            Finding(
                                rule="6.5.2",
                                severity=context.severity_for("6.5.2"),
                                kind="violation",
                                message=(
                                    f"{term!r} reappears after more than 2,500 "
                                    "intervening words without a verbatim recall or "
                                    "section reference (§6.5.2)"
                                ),
                                path=unit.span.path,
                                start_line=line_number,
                                end_line=line_number,
                                checker="distant-reuse",
                                excerpt=term,
                            )
                        )
                last_position = position
    return findings


@register("6.5.3", name="boundary-recap")
def boundary_recap(context: LintContext) -> Iterable[Finding]:
    """Report where §6.5.3's permitted boundary recap would help."""
    admitted = admissions(context.manifest)
    if len(admitted) < 4:
        return []
    findings: list[Finding] = []
    headings = [
        unit
        for unit in context.manifest.units
        if unit.node_type == "heading" and unit.heading_level == 2
    ]
    for heading in headings[1:]:
        opening = next(
            (
                unit
                for unit in context.manifest.units
                if unit.span.start_line > heading.span.start_line
                and unit.node_type in {"paragraph", "list"}
            ),
            None,
        )
        if opening is None or RECALL_OPENER_RE.match(opening.text):
            continue
        earlier = [term for term, line, _ in admitted if line < heading.span.start_line]
        if len(earlier) < 4:
            continue
        findings.append(
            Finding(
                rule="6.5.3",
                severity=context.severity_for("6.5.3"),
                kind="candidate",
                message=(
                    f"section {heading.heading_path[-1]!r} follows "
                    f"{len(earlier)} term admissions and opens without the "
                    "boundary recap that §6.5.3 permits"
                ),
                path=heading.span.path,
                start_line=heading.span.start_line,
                end_line=heading.span.start_line,
                checker="boundary-recap",
            )
        )
    return findings

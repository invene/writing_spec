"""Part 5 and Part 7 checks: symbols, citations, work items, speculation."""

from __future__ import annotations

import re
from typing import Iterable

from itws.lint.model import Finding, LintContext
from itws.lint.registry import register
from itws.lint.text import (
    BOUNDED_BLOCK_RE,
    body_units,
    prose_units,
    split_sentences,
    strip_inline_markup,
)

SYMBOL_BINDING_RE = re.compile(
    r"(?:^|[\s(])(?:let|where)\s+\$?(?P<symbol>[A-Za-z]|\\[A-Za-z]+)\$?\s+"
    r"(?:be|denotes?|is|=)\s+(?P<meaning>[^.,;]{3,80})",
    re.IGNORECASE,
)
NOTATION_TABLE_RE = re.compile(r"\|\s*Symbol\s*\|", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b")
ACCESS_DATE_RE = re.compile(r"accessed (?P<date>[^.,;)]+)", re.IGNORECASE)
PLACEHOLDER_DATE_RE = re.compile(r"\b(?:XXXX|20XX|\d{4}-XX-XX|n\.d\.)\b")
IDENTIFIER_DEFINITION_RE = re.compile(
    r"^\s*(?:[-*+]\s+|\d+[.)]\s+)?(?:\*\*)?(?P<id>[A-Z]{2,4}-\d+)(?:\*\*)?\s*[:.]"
)
CLASSIFICATION_RE = re.compile(
    r"^\s*(?:[-*+]\s+)?(?:\*\*)?(?P<field>Outcome class|Change reason)(?:\*\*)?\s*[:.]"
    r"\s*(?P<value>.+?)\s*$",
    re.IGNORECASE,
)
PARENT_RE = re.compile(
    r"^\s*(?:\*\*)?Parent(?: task)?(?:\*\*)?\s*[:.]\s*(?P<value>.+?)\s*$",
    re.IGNORECASE,
)
PARENT_CONDITION_RE = re.compile(
    r"^\s*(?:\*\*)?Named completion condition(?:\*\*)?\s*[:.]\s*(?P<value>.+?)\s*$",
    re.IGNORECASE,
)
WORK_ITEM_ID_RE = re.compile(r"\b[A-Z]{1,3}-\d+\b")
CONDITION_ID_RE = re.compile(r"\bCC-\d+\b")
SPECULATIVE_MARKER_RE = re.compile(
    r"\b(?:might|could|perhaps|possibly|conceivably|we speculate|it is plausible)\b",
    re.IGNORECASE,
)


def _slot_units(context: LintContext, slot_name: str):
    """Return the units under one resolved skeleton slot."""
    headings = [
        unit for unit in context.manifest.units if unit.node_type == "heading"
    ]
    for position, heading in enumerate(headings):
        if heading.canonical_slot != slot_name:
            continue
        end = (
            headings[position + 1].span.start_line - 1
            if position + 1 < len(headings)
            else context.manifest.line_count
        )
        return context.manifest.units_in_range(heading.span.start_line, end)
    return ()


@register("5.2.2", name="symbol-binding")
def symbol_binding(context: LintContext) -> Iterable[Finding]:
    """One symbol carries one meaning, and one meaning uses one symbol."""
    bindings: dict[str, list[tuple[str, int]]] = {}
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            for match in SYMBOL_BINDING_RE.finditer(strip_inline_markup(line)):
                symbol = match.group("symbol")
                meaning = " ".join(match.group("meaning").split()).casefold()
                bindings.setdefault(symbol, []).append(
                    (meaning, unit.span.start_line + line_offset)
                )

    findings: list[Finding] = []
    for symbol, uses in sorted(bindings.items()):
        meanings = {meaning for meaning, _ in uses}
        if len(meanings) > 1:
            findings.append(
                Finding(
                    rule="5.2.2",
                    severity=context.severity_for("5.2.2"),
                    kind="violation",
                    message=(
                        f"symbol {symbol!r} is bound to {len(meanings)} meanings; "
                        "§5.2.2 permits one"
                    ),
                    path=context.manifest.path,
                    start_line=uses[0][1],
                    end_line=uses[-1][1],
                    checker="symbol-binding",
                    excerpt=symbol,
                )
            )

    by_meaning: dict[str, set[str]] = {}
    for symbol, uses in bindings.items():
        for meaning, _ in uses:
            by_meaning.setdefault(meaning, set()).add(symbol)
    for meaning, symbols in sorted(by_meaning.items()):
        if len(symbols) > 1:
            findings.append(
                Finding(
                    rule="5.2.2",
                    severity=context.severity_for("5.2.2"),
                    kind="violation",
                    message=(
                        f"meaning {meaning!r} is written with "
                        f"{len(symbols)} symbols ({', '.join(sorted(symbols))}); "
                        "§5.2.2 permits one"
                    ),
                    path=context.manifest.path,
                    start_line=1,
                    end_line=context.manifest.line_count,
                    checker="symbol-binding",
                )
            )
    return findings


@register("5.2.3", name="notation-table")
def notation_table(context: LintContext) -> Iterable[Finding]:
    """More than six defined symbols require a notation table."""
    symbols: set[str] = set()
    for unit in body_units(context.manifest):
        for match in SYMBOL_BINDING_RE.finditer(strip_inline_markup(unit.text)):
            symbols.add(match.group("symbol"))
    if len(symbols) <= 6:
        return []
    has_table = any(
        NOTATION_TABLE_RE.search(unit.text)
        for unit in context.manifest.units
        if unit.node_type == "table"
    )
    if has_table:
        return []
    return [
        Finding(
            rule="5.2.3",
            severity=context.severity_for("5.2.3"),
            kind="violation",
            message=(
                f"the document defines {len(symbols)} non-baseline symbols and has "
                "no notation table (§5.2.3)"
            ),
            path=context.manifest.path,
            start_line=1,
            end_line=context.manifest.line_count,
            checker="notation-table",
        )
    ]


@register("5.4.3", name="citation-resolution", network=False)
def citation_resolution(context: LintContext) -> Iterable[Finding]:
    """Offline part of §5.4.3: form, placeholders, and archive coverage."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            line_number = unit.span.start_line + line_offset
            for match in PLACEHOLDER_DATE_RE.finditer(line):
                findings.append(
                    Finding(
                        rule="5.4.3",
                        severity=context.severity_for("5.4.3"),
                        kind="violation",
                        message=(
                            f"citation carries the placeholder access date "
                            f"{match.group(0)!r} (§5.4.3)"
                        ),
                        path=unit.span.path,
                        start_line=line_number,
                        end_line=line_number,
                        checker="citation-resolution",
                        excerpt=match.group(0),
                    )
                )
            for match in DOI_RE.finditer(line):
                if not re.fullmatch(r"10\.\d{4,9}/\S+", match.group(0)):
                    findings.append(
                        Finding(
                            rule="5.4.3",
                            severity=context.severity_for("5.4.3"),
                            kind="violation",
                            message=f"malformed DOI {match.group(0)!r} (§5.4.3)",
                            path=unit.span.path,
                            start_line=line_number,
                            end_line=line_number,
                            checker="citation-resolution",
                            excerpt=match.group(0),
                        )
                    )
    if not context.evidence.network_checks_enabled:
        has_links = any(unit.links for unit in context.manifest.units)
        if has_links:
            findings.append(
                Finding(
                    rule="5.4.3",
                    severity=context.severity_for("5.4.3"),
                    kind="skipped",
                    message=(
                        "link and DOI resolution needs network access; run with "
                        "--network to complete §5.4.3"
                    ),
                    path=context.manifest.path,
                    start_line=1,
                    end_line=1,
                    checker="citation-resolution",
                )
            )
    return findings


@register("5.8.1", name="checkability-statement")
def checkability_statement(context: LintContext) -> Iterable[Finding]:
    """A report includes its reproducibility or verification statement."""
    slot_name = {
        "technical-report": "Reproducibility or verification",
        "research-paper": "Reproducibility statement",
    }.get(context.profile)
    if slot_name is None:
        return []
    units = _slot_units(context, slot_name)
    if not units:
        return [
            Finding(
                rule="5.8.1",
                severity=context.severity_for("5.8.1"),
                kind="violation",
                message=(
                    f"the report has no resolved {slot_name!r} section, so it "
                    "carries no checkability statement (§5.8.1)"
                ),
                path=context.manifest.path,
                start_line=1,
                end_line=1,
                checker="checkability-statement",
            )
        ]
    body = " ".join(unit.text for unit in units if unit.node_type != "heading")
    if len(body.split()) < 20:
        return [
            Finding(
                rule="5.8.1",
                severity=context.severity_for("5.8.1"),
                kind="candidate",
                message=(
                    "the checkability section holds fewer than 20 words; confirm "
                    "that it states every applicable statement element (§5.8.1)"
                ),
                path=units[0].span.path,
                start_line=units[0].span.start_line,
                end_line=units[-1].span.end_line,
                checker="checkability-statement",
            )
        ]
    return []


@register("5.9.1", name="one-definition-of-done")
def one_definition_of_done(context: LintContext) -> Iterable[Finding]:
    """A work item carries exactly one Definition of done slot."""
    if context.profile not in {"epic", "task", "subtask"}:
        return []
    matches = [
        unit
        for unit in context.manifest.units
        if unit.node_type == "heading"
        and unit.canonical_slot == "Definition of done"
    ]
    inline = [
        unit
        for unit in context.manifest.units
        if unit.node_type != "heading"
        and re.search(r"\*\*Definition of done\.?\*\*", unit.text)
    ]
    total = len(matches) + len(inline)
    if total == 1:
        return []
    if total == 0:
        return [
            Finding(
                rule="5.9.1",
                severity=context.severity_for("5.9.1"),
                kind="violation",
                message="the work item has no `Definition of done` slot (§5.9.1)",
                path=context.manifest.path,
                start_line=1,
                end_line=1,
                checker="one-definition-of-done",
            )
        ]
    spans = matches + inline
    return [
        Finding(
            rule="5.9.1",
            severity=context.severity_for("5.9.1"),
            kind="violation",
            message=(
                f"the work item carries {total} `Definition of done` slots; §5.9.1 "
                "permits exactly one"
            ),
            path=context.manifest.path,
            start_line=min(unit.span.start_line for unit in spans),
            end_line=max(unit.span.end_line for unit in spans),
            checker="one-definition-of-done",
        )
    ]


def _declared_identifiers(context: LintContext, prefix: str) -> list[tuple[str, int]]:
    found: list[tuple[str, int]] = []
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            match = IDENTIFIER_DEFINITION_RE.match(line)
            if match and match.group("id").startswith(prefix):
                found.append((match.group("id"), unit.span.start_line + line_offset))
    return found


@register("4.11.8", name="epic-invariant-ids")
def epic_invariant_ids(context: LintContext) -> Iterable[Finding]:
    """Each epic invariant carries a unique stable identifier."""
    if context.profile != "epic":
        return []
    units = _slot_units(context, "Technical invariants")
    findings: list[Finding] = []
    declared = _declared_identifiers(context, "INV")
    seen: dict[str, int] = {}
    for identifier, line in declared:
        if identifier in seen:
            findings.append(
                Finding(
                    rule="4.11.8",
                    severity=context.severity_for("4.11.8"),
                    kind="violation",
                    message=(
                        f"invariant identifier {identifier!r} is reused on lines "
                        f"{seen[identifier]} and {line} (§4.11.8)"
                    ),
                    path=context.manifest.path,
                    start_line=seen[identifier],
                    end_line=line,
                    checker="epic-invariant-ids",
                    excerpt=identifier,
                )
            )
        seen[identifier] = line

    for unit in units:
        if unit.node_type != "list":
            continue
        for line_offset, line in enumerate(unit.text.splitlines()):
            if not line.strip():
                continue
            if not IDENTIFIER_DEFINITION_RE.match(line):
                findings.append(
                    Finding(
                        rule="4.11.8",
                        severity=context.severity_for("4.11.8"),
                        kind="violation",
                        message=(
                            "the invariant carries no stable identifier of the form "
                            "`INV-<n>:` (§4.11.8)"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line + line_offset,
                        end_line=unit.span.start_line + line_offset,
                        checker="epic-invariant-ids",
                        excerpt=line.strip()[:80],
                    )
                )
    return findings


@register("5.9.3", name="task-condition-ids")
def task_condition_ids(context: LintContext) -> Iterable[Finding]:
    """Each task completion condition carries a unique stable identifier."""
    if context.profile != "task":
        return []
    findings: list[Finding] = []
    seen: dict[str, int] = {}
    for identifier, line in _declared_identifiers(context, "CC"):
        if identifier in seen:
            findings.append(
                Finding(
                    rule="5.9.3",
                    severity=context.severity_for("5.9.3"),
                    kind="violation",
                    message=(
                        f"completion-condition identifier {identifier!r} is reused "
                        f"on lines {seen[identifier]} and {line} (§5.9.3)"
                    ),
                    path=context.manifest.path,
                    start_line=seen[identifier],
                    end_line=line,
                    checker="task-condition-ids",
                    excerpt=identifier,
                )
            )
        seen[identifier] = line
    units = _slot_units(context, "Definition of done")
    if units and not seen:
        findings.append(
            Finding(
                rule="5.9.3",
                severity=context.severity_for("5.9.3"),
                kind="violation",
                message=(
                    "the definition of done declares no `CC-<n>` completion-condition "
                    "identifier (§5.9.3)"
                ),
                path=units[0].span.path,
                start_line=units[0].span.start_line,
                end_line=units[-1].span.end_line,
                checker="task-condition-ids",
            )
        )
    return findings


@register("4.11.5", name="task-classification")
def task_classification(context: LintContext) -> Iterable[Finding]:
    """A task declares one Outcome class and one Change reason."""
    if context.profile != "task":
        return []
    declared: dict[str, list[tuple[str, int]]] = {
        "outcome class": [],
        "change reason": [],
    }
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            match = CLASSIFICATION_RE.match(line)
            if match:
                declared[match.group("field").casefold()].append(
                    (match.group("value").strip(), unit.span.start_line + line_offset)
                )
    findings: list[Finding] = []
    for field, values in declared.items():
        if len(values) != 1:
            findings.append(
                Finding(
                    rule="4.11.5",
                    severity=context.severity_for("4.11.5"),
                    kind="violation",
                    message=(
                        f"the task declares {len(values)} `{field}` values; §4.11.5 "
                        "requires exactly one"
                    ),
                    path=context.manifest.path,
                    start_line=values[0][1] if values else 1,
                    end_line=values[-1][1] if values else 1,
                    checker="task-classification",
                )
            )
    return findings


def _slot_or_field(
    context: LintContext, slot_name: str, field_re: re.Pattern[str]
) -> list[tuple[str, int]]:
    """Collect a work-item field from its slot body or its inline label.

    Annex E permits either a heading or an inline bold label, so the checker
    reads both forms rather than requiring one house style.
    """
    found: list[tuple[str, int]] = []
    for unit in _slot_units(context, slot_name):
        if unit.node_type == "heading":
            continue
        for line_offset, line in enumerate(unit.text.splitlines()):
            if line.strip():
                found.append((line.strip(), unit.span.start_line + line_offset))
    if found:
        return found
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            match = field_re.match(line)
            if match:
                found.append(
                    (match.group("value"), unit.span.start_line + line_offset)
                )
    return found


@register("4.11.12", name="subtask-one-parent")
def subtask_one_parent(context: LintContext) -> Iterable[Finding]:
    """A subtask names exactly one parent task."""
    if context.profile != "subtask":
        return []
    parents = _slot_or_field(context, "Parent task", PARENT_RE)
    if not parents:
        return [
            Finding(
                rule="4.11.12",
                severity=context.severity_for("4.11.12"),
                kind="violation",
                message="the subtask names no parent task (§4.11.12)",
                path=context.manifest.path,
                start_line=1,
                end_line=1,
                checker="subtask-one-parent",
            )
        ]
    findings: list[Finding] = []
    if not any(WORK_ITEM_ID_RE.search(value) for value, _ in parents):
        findings.append(
            Finding(
                rule="4.11.12",
                severity=context.severity_for("4.11.12"),
                kind="violation",
                message=(
                    "the parent-task field names no work-item identifier "
                    "(§4.11.12)"
                ),
                path=context.manifest.path,
                start_line=parents[0][1],
                end_line=parents[-1][1],
                checker="subtask-one-parent",
                excerpt=parents[0][0][:80],
            )
        )
    named = {
        identifier
        for value, _ in parents
        for identifier in WORK_ITEM_ID_RE.findall(value)
    }
    if len(named) > 1:
        findings.append(
            Finding(
                rule="4.11.12",
                severity=context.severity_for("4.11.12"),
                kind="violation",
                message=(
                    f"the subtask names {len(named)} parent tasks "
                    f"({', '.join(sorted(named))}); §4.11.12 requires one"
                ),
                path=context.manifest.path,
                start_line=parents[0][1],
                end_line=parents[-1][1],
                checker="subtask-one-parent",
            )
        )
    return findings


@register("4.11.13", name="subtask-one-condition")
def subtask_one_condition(context: LintContext) -> Iterable[Finding]:
    """A subtask names exactly one parent completion-condition ID."""
    if context.profile != "subtask":
        return []
    declared = _slot_or_field(
        context, "Named completion condition", PARENT_CONDITION_RE
    )
    if not declared:
        return [
            Finding(
                rule="4.11.13",
                severity=context.severity_for("4.11.13"),
                kind="violation",
                message=(
                    "the subtask names no parent completion condition (§4.11.13)"
                ),
                path=context.manifest.path,
                start_line=1,
                end_line=1,
                checker="subtask-one-condition",
            )
        ]
    conditions = {
        identifier
        for value, _ in declared
        for identifier in CONDITION_ID_RE.findall(value)
    }
    if len(conditions) == 1:
        return []
    return [
        Finding(
            rule="4.11.13",
            severity=context.severity_for("4.11.13"),
            kind="violation",
            message=(
                f"the named completion condition resolves to {len(conditions)} "
                "`CC-<n>` identifiers; §4.11.13 requires exactly one"
            ),
            path=context.manifest.path,
            start_line=declared[0][1],
            end_line=declared[-1][1],
            checker="subtask-one-condition",
            excerpt=declared[0][0][:80],
        )
    ]


@register("7.3.2", name="speculation-block")
def speculation_block(context: LintContext) -> Iterable[Finding]:
    """A speculative statement appears only in a marked speculation block."""
    if not context.rule_applies("7.3.2"):
        return []
    block_lines: set[int] = set()
    for unit in context.manifest.units:
        if unit.node_type != "block_quote":
            continue
        if any(label == "Speculation" for label, _ in BOUNDED_BLOCK_RE.findall(unit.text)):
            block_lines.update(range(unit.span.start_line, unit.span.end_line + 1))

    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            if sentence.line in block_lines:
                continue
            match = SPECULATIVE_MARKER_RE.search(strip_inline_markup(sentence.text))
            if not match:
                continue
            findings.append(
                Finding(
                    rule="7.3.2",
                    severity=context.severity_for("7.3.2"),
                    kind="violation",
                    message=(
                        f"the speculative marker {match.group(0)!r} appears outside a "
                        "**[Speculation — <topic>]** block (§7.3.2)"
                    ),
                    path=unit.span.path,
                    start_line=sentence.line,
                    end_line=sentence.line,
                    checker="speculation-block",
                    excerpt=sentence.text[:120],
                )
            )
    return findings

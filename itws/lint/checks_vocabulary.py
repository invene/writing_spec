"""Part 2 checks: acronyms, the term ladder, and definition form."""

from __future__ import annotations

import re
from typing import Iterable

from itws.lint.model import Finding, LintContext
from itws.lint.registry import register
from itws.lint.text import (
    ACRONYM_RE,
    EXPANSION_RE,
    admissions,
    body_units,
    counted_word_length,
    document_words,
    prose_units,
    split_sentences,
    strip_inline_markup,
)

#: Acronyms that Annex B assumes, so they need no expansion.
def _assumed_acronyms(context: LintContext) -> set[str]:
    assumed: set[str] = set()
    for item in context.spec.baseline:
        for match in re.finditer(r"\(([A-Z][A-Z0-9]{1,7})s?\)", item.text):
            assumed.add(match.group(1))
        for match in re.finditer(r"\b([A-Z][A-Z0-9]{1,7})\b", item.text):
            assumed.add(match.group(1))
    return assumed


@register("2.1.4", name="acronym-expansion")
def acronym_expansion(context: LintContext) -> Iterable[Finding]:
    """Every non-baseline acronym carries its expansion at first use."""
    assumed = _assumed_acronyms(context)
    expanded: set[str] = set()
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            plain = strip_inline_markup(line)
            for match in EXPANSION_RE.finditer(plain):
                expanded.add(match.group("short"))
            for match in ACRONYM_RE.finditer(plain):
                short = match.group("short")
                if short in assumed or short in expanded:
                    continue
                if EXPANSION_RE.search(plain[: match.end() + 1]):
                    continue
                expanded.add(short)
                findings.append(
                    Finding(
                        rule="2.1.4",
                        severity=context.severity_for("2.1.4"),
                        kind="violation",
                        message=(
                            f"acronym {short!r} appears without the expansion and "
                            "parenthesized short form that §2.1.4 requires at "
                            "first use"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line + line_offset,
                        end_line=unit.span.start_line + line_offset,
                        checker="acronym-expansion",
                        excerpt=short,
                    )
                )
    return findings


@register("2.1.5", name="acronym-consistency")
def acronym_consistency(context: LintContext) -> Iterable[Finding]:
    """After introduction, one form is used, not both interchangeably."""
    findings: list[Finding] = []
    introduced: dict[str, tuple[str, int]] = {}
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            plain = strip_inline_markup(line)
            for match in EXPANSION_RE.finditer(plain):
                introduced.setdefault(
                    match.group("short"),
                    (match.group("expansion"), unit.span.start_line + line_offset),
                )

    for short, (expansion, introduced_line) in sorted(introduced.items()):
        short_uses: list[int] = []
        long_uses: list[int] = []
        for unit in body_units(context.manifest):
            for line_offset, line in enumerate(unit.text.splitlines()):
                line_number = unit.span.start_line + line_offset
                if line_number <= introduced_line:
                    continue
                plain = strip_inline_markup(line)
                if re.search(rf"\b{re.escape(short)}s?\b", plain):
                    short_uses.append(line_number)
                if re.search(rf"\b{re.escape(expansion)}\b", plain, re.IGNORECASE):
                    long_uses.append(line_number)
        if short_uses and long_uses:
            findings.append(
                Finding(
                    rule="2.1.5",
                    severity=context.severity_for("2.1.5"),
                    kind="violation",
                    message=(
                        f"{short!r} and {expansion!r} both appear after "
                        f"introduction on line {introduced_line}; §2.1.5 requires "
                        "one form"
                    ),
                    path=context.manifest.path,
                    start_line=min(short_uses[0], long_uses[0]),
                    end_line=max(short_uses[-1], long_uses[-1]),
                    checker="acronym-consistency",
                    excerpt=short,
                )
            )
    return findings


@register("2.3.1", name="define-before-use")
def define_before_use(context: LintContext) -> Iterable[Finding]:
    """A term used before its admission breaks the ladder.

    The check covers two cases: an Annex A term the document never admits or
    admits late, and a term the document admits itself but uses earlier.
    """
    admitted = {term.casefold(): line for term, line, _ in admissions(context.manifest)}
    findings: list[Finding] = []
    words = document_words(context.manifest)
    joined = " ".join(word for word, _ in words).casefold()

    for term, admitted_line, _ in admissions(context.manifest):
        first_use = _first_use_line(context, term, before=admitted_line)
        if first_use is not None and first_use < admitted_line:
            findings.append(
                Finding(
                    rule="2.3.1",
                    severity=context.severity_for("2.3.1"),
                    kind="violation",
                    message=(
                        f"{term!r} is used on line {first_use} but this document "
                        f"admits it on line {admitted_line} (§2.3.1)"
                    ),
                    path=context.manifest.path,
                    start_line=first_use,
                    end_line=admitted_line,
                    checker="define-before-use",
                    excerpt=term,
                )
            )

    for entry in context.spec.glossary:
        if entry.status != "admitted":
            continue
        needle = entry.term.casefold()
        if needle not in joined:
            continue
        first_use = _first_use_line(context, entry.term)
        if first_use is None:
            continue
        admitted_line = admitted.get(needle)
        if admitted_line is None:
            findings.append(
                Finding(
                    rule="2.3.1",
                    severity=context.severity_for("2.3.1"),
                    kind="violation",
                    message=(
                        f"Annex A term {entry.term!r} is used without an admission "
                        "in this document (§2.3.1)"
                    ),
                    path=context.manifest.path,
                    start_line=first_use,
                    end_line=first_use,
                    checker="define-before-use",
                    excerpt=entry.term,
                )
            )
        elif admitted_line > first_use:
            findings.append(
                Finding(
                    rule="2.3.1",
                    severity=context.severity_for("2.3.1"),
                    kind="violation",
                    message=(
                        f"{entry.term!r} is used on line {first_use} but admitted "
                        f"on line {admitted_line} (§2.3.1)"
                    ),
                    path=context.manifest.path,
                    start_line=first_use,
                    end_line=admitted_line,
                    checker="define-before-use",
                    excerpt=entry.term,
                )
            )
    return findings


def _first_use_line(
    context: LintContext, term: str, *, before: int | None = None
) -> int | None:
    """Return the first body line that uses ``term``.

    ``before`` restricts the search to lines above an admission, so an
    admission line never counts as a use of the term it admits.
    """
    pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            line_number = unit.span.start_line + line_offset
            if before is not None and line_number >= before:
                return None
            if pattern.search(strip_inline_markup(line)):
                return line_number
    return None


@register("2.3.2", name="ladder-prerequisites")
def ladder_prerequisites(context: LintContext) -> Iterable[Finding]:
    """A definition may stand only on terms already assumed or admitted."""
    order = {
        term.casefold(): line for term, line, _ in admissions(context.manifest)
    }
    findings: list[Finding] = []
    for entry in context.spec.glossary:
        needle = entry.term.casefold()
        if needle not in order:
            continue
        admitted_line = order[needle]
        for prerequisite in entry.prerequisites:
            key = prerequisite.casefold()
            if key not in order:
                findings.append(
                    Finding(
                        rule="2.3.2",
                        severity=context.severity_for("2.3.2"),
                        kind="violation",
                        message=(
                            f"{entry.term!r} is admitted on line {admitted_line}, but "
                            f"its Annex A prerequisite {prerequisite!r} is never "
                            "admitted (§2.3.2)"
                        ),
                        path=context.manifest.path,
                        start_line=admitted_line,
                        end_line=admitted_line,
                        checker="ladder-prerequisites",
                        excerpt=prerequisite,
                    )
                )
            elif order[key] > admitted_line:
                findings.append(
                    Finding(
                        rule="2.3.2",
                        severity=context.severity_for("2.3.2"),
                        kind="violation",
                        message=(
                            f"{entry.term!r} is admitted on line {admitted_line} "
                            f"before its prerequisite {prerequisite!r} on line "
                            f"{order[key]} (§2.3.2)"
                        ),
                        path=context.manifest.path,
                        start_line=admitted_line,
                        end_line=order[key],
                        checker="ladder-prerequisites",
                        excerpt=prerequisite,
                    )
                )
    return findings


@register("2.4.4", name="definition-length")
def definition_length(context: LintContext) -> Iterable[Finding]:
    """A definition stays within two sentences and 40 words."""
    findings: list[Finding] = []
    admitted_lines = {line for _, line, _ in admissions(context.manifest)}
    for unit in body_units(context.manifest):
        sentences = split_sentences(unit)
        opening = [
            sentence
            for sentence in sentences
            if sentence.line in admitted_lines
        ]
        if not opening:
            continue
        start = sentences.index(opening[0])
        window = sentences[start : start + 3]
        words = sum(counted_word_length(sentence.text) for sentence in window[:2])
        if words > 40:
            findings.append(
                Finding(
                    rule="2.4.4",
                    severity=context.severity_for("2.4.4"),
                    kind="violation",
                    message=(
                        f"the definition runs {words} words; §2.4.4 caps a "
                        "definition at two sentences and 40 words"
                    ),
                    path=unit.span.path,
                    start_line=window[0].line,
                    end_line=window[-1].line,
                    checker="definition-length",
                )
            )
    return findings

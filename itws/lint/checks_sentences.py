"""Part 3 checks: length caps, noun clusters, and punctuation."""

from __future__ import annotations

import re
from typing import Iterable

from itws.lint.model import Finding, LintContext
from itws.lint.registry import register
from itws.lint.text import (
    OPENER_FOLLOWERS,
    admissions,
    body_units,
    counted_word_length,
    noun_clusters,
    split_sentences,
    strip_inline_markup,
    unbalanced_math,
)

LOAD_BEARING_RE = re.compile(
    r"\*\*shall(?: not)?\*\*|\*\*should(?: not)?\*\*|\*\*may\*\*", re.IGNORECASE
)
SEMICOLON_CLAUSE_RE = re.compile(r";\s+(?P<tail>[A-Za-z][^;]*)")
INDEPENDENT_CLAUSE_RE = re.compile(
    r"^(?:the|a|an|this|that|these|those|it|we|they|he|she|there|"
    r"[A-Z][A-Za-z0-9_-]*)\s+\w+", re.IGNORECASE
)
SERIAL_LIST_RE = re.compile(
    r"(?P<head>[^,;:.]{1,60}(?:,[^,;:.]{1,60})+)\s+(?P<conjunction>and|or)\s+"
    r"(?P<tail>[^,.;:]{1,60})"
)
#: A list item is short. A long segment before the conjunction is a clause,
#: not a list item, and Rule 3.8.2 does not reach it.
MAX_LIST_ITEM_WORDS = 6


@register("3.1.1", name="descriptive-sentence-cap")
def descriptive_sentence_cap(context: LintContext) -> Iterable[Finding]:
    """A descriptive sentence stays within 25 words (Rule 3.1.3 counting)."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            if LOAD_BEARING_RE.search(sentence.text):
                continue
            length = counted_word_length(sentence.text)
            if length > 25:
                findings.append(
                    Finding(
                        rule="3.1.1",
                        severity=context.severity_for("3.1.1"),
                        kind="violation",
                        message=(
                            f"the sentence counts {length} words; §3.1.1 caps a "
                            "descriptive sentence at 25"
                        ),
                        path=unit.span.path,
                        start_line=sentence.line,
                        end_line=sentence.line,
                        checker="descriptive-sentence-cap",
                        excerpt=sentence.text[:120],
                    )
                )
    return findings


@register("3.1.2", name="load-bearing-sentence-cap")
def load_bearing_sentence_cap(context: LintContext) -> Iterable[Finding]:
    """A sentence carrying a §0.4 keyword stays within 20 words."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            if not LOAD_BEARING_RE.search(sentence.text):
                continue
            length = counted_word_length(sentence.text)
            if length > 20:
                findings.append(
                    Finding(
                        rule="3.1.2",
                        severity=context.severity_for("3.1.2"),
                        kind="candidate",
                        message=(
                            f"the sentence counts {length} words and carries a "
                            "conformance keyword; §3.1.2 caps a load-bearing "
                            "sentence at 20. Rule 3.1.4 requires a split, not a "
                            "loss of precision"
                        ),
                        path=unit.span.path,
                        start_line=sentence.line,
                        end_line=sentence.line,
                        checker="load-bearing-sentence-cap",
                        excerpt=sentence.text[:120],
                    )
                )
    return findings


@register("3.1.3", name="inline-math-counting")
def inline_math_counting(context: LintContext) -> Iterable[Finding]:
    """An unbalanced inline delimiter makes the §3.1.3 count undecidable."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            if unbalanced_math(line):
                findings.append(
                    Finding(
                        rule="3.1.3",
                        severity=context.severity_for("3.1.3"),
                        kind="violation",
                        message=(
                            "the line has an unbalanced inline-math or inline-code "
                            "delimiter, so the §3.1.3 word count cannot be applied"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line + line_offset,
                        end_line=unit.span.start_line + line_offset,
                        checker="inline-math-counting",
                        excerpt=line[:120],
                    )
                )
    return findings


@register("3.5.1", name="noun-cluster-cap")
def noun_cluster_cap(context: LintContext) -> Iterable[Finding]:
    """A noun cluster holds at most three nouns."""
    admitted = {term.casefold() for term, _, _ in admissions(context.manifest)}
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            for cluster in noun_clusters(sentence):
                if _collapses_to_three(cluster, admitted):
                    continue
                findings.append(
                    Finding(
                        rule="3.5.1",
                        severity=context.severity_for("3.5.1"),
                        kind="candidate",
                        message=(
                            f"{' '.join(cluster)!r} reads as a stack of "
                            f"{len(cluster)} nouns; §3.5.1 caps a cluster at three. "
                            "Confirm the reading before repairing"
                        ),
                        path=unit.span.path,
                        start_line=sentence.line,
                        end_line=sentence.line,
                        checker="noun-cluster-cap",
                        excerpt=" ".join(cluster),
                    )
                )
    return findings


def _collapses_to_three(cluster: tuple[str, ...], admitted: set[str]) -> bool:
    """Apply Rule 3.5.2: an admitted multiword term counts as one noun."""
    remaining = list(cluster)
    count = 0
    while remaining:
        matched = 0
        for width in range(min(4, len(remaining)), 1, -1):
            candidate = " ".join(remaining[:width]).casefold()
            if candidate in admitted:
                matched = width
                break
        count += 1
        remaining = remaining[matched or 1 :]
    return count <= 3


@register("3.5.2", name="admitted-term-collapse")
def admitted_term_collapse(context: LintContext) -> Iterable[Finding]:
    """Report where Rule 3.5.2's permitted counting resolves a long cluster."""
    admitted = {term.casefold() for term, _, _ in admissions(context.manifest)}
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            for cluster in noun_clusters(sentence):
                if not _collapses_to_three(cluster, admitted):
                    continue
                findings.append(
                    Finding(
                        rule="3.5.2",
                        severity=context.severity_for("3.5.2"),
                        kind="candidate",
                        message=(
                            f"{' '.join(cluster)!r} exceeds three words but counts "
                            "as three or fewer nouns under §3.5.2 because it "
                            "contains an admitted multiword term"
                        ),
                        path=unit.span.path,
                        start_line=sentence.line,
                        end_line=sentence.line,
                        checker="admitted-term-collapse",
                        excerpt=" ".join(cluster),
                    )
                )
    return findings


@register("3.6.2", name="bare-opener")
def bare_opener(context: LintContext) -> Iterable[Finding]:
    """A sentence does not open with a bare demonstrative or "it".

    The covered openers come from the §3.6.2 phrase list. An opener is
    compliant when a noun follows it, so the check fires only when the next
    word is an auxiliary or a finite verb.
    """
    openers = {
        entry.pattern.casefold(): entry
        for entry in context.spec.phrase_lists
        if entry.rule == "3.6.2"
    }
    if not openers:
        return []
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            words = strip_inline_markup(sentence.text).split()
            if len(words) < 2:
                continue
            first = words[0].strip("*_(\"'").casefold()
            entry = openers.get(first)
            if entry is None:
                continue
            follower = words[1].strip(".,;:*_)\"'").casefold()
            if follower not in OPENER_FOLLOWERS:
                continue
            findings.append(
                Finding(
                    rule="3.6.2",
                    severity=context.severity_for("3.6.2"),
                    kind="violation",
                    message=(
                        f"the sentence opens with a bare {first!r} followed by "
                        f"{follower!r}; §3.6.2 requires the opener to name its "
                        "referent through a following noun"
                    ),
                    path=unit.span.path,
                    start_line=sentence.line,
                    end_line=sentence.line,
                    checker=f"phrase-list:{entry.id}",
                    excerpt=" ".join(words[:4]),
                )
            )
    return findings


@register("3.7.2", name="respectively-pairing")
def respectively_pairing(context: LintContext) -> Iterable[Finding]:
    """"Respectively" pairs at most two items."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            if not re.search(r"\brespectively\b", sentence.text, re.IGNORECASE):
                continue
            plain = strip_inline_markup(sentence.text)
            items = max(
                (len(re.findall(r",", segment)) for segment in plain.split(" and ")),
                default=0,
            )
            if items >= 2:
                findings.append(
                    Finding(
                        rule="3.7.2",
                        severity=context.severity_for("3.7.2"),
                        kind="violation",
                        message=(
                            "\"respectively\" pairs three or more items; §3.7.2 "
                            "requires a direct or tabular pairing"
                        ),
                        path=unit.span.path,
                        start_line=sentence.line,
                        end_line=sentence.line,
                        checker="respectively-pairing",
                        excerpt=sentence.text[:120],
                    )
                )
    return findings


@register("3.8.1", name="semicolon-clauses")
def semicolon_clauses(context: LintContext) -> Iterable[Finding]:
    """A semicolon does not join independent clauses."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        if unit.node_type == "list":
            continue
        for sentence in split_sentences(unit):
            plain = strip_inline_markup(sentence.text)
            for match in SEMICOLON_CLAUSE_RE.finditer(plain):
                tail = match.group("tail").strip()
                if INDEPENDENT_CLAUSE_RE.match(tail):
                    findings.append(
                        Finding(
                            rule="3.8.1",
                            severity=context.severity_for("3.8.1"),
                            kind="violation",
                            message=(
                                "a semicolon joins independent clauses; §3.8.1 "
                                "requires two sentences"
                            ),
                            path=unit.span.path,
                            start_line=sentence.line,
                            end_line=sentence.line,
                            checker="semicolon-clauses",
                            excerpt=f"; {tail[:80]}",
                            repair=". ",
                        )
                    )
    return findings


@register("3.8.2", name="serial-comma")
def serial_comma(context: LintContext) -> Iterable[Finding]:
    """A list of three or more items uses the serial comma."""
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for sentence in split_sentences(unit):
            # A thousands separator is not a list comma.
            plain = re.sub(
                r"(?<=\d),(?=\d)", "", strip_inline_markup(sentence.text)
            )
            for match in SERIAL_LIST_RE.finditer(plain):
                head = match.group("head")
                if head.rstrip().endswith(","):
                    continue
                items = [segment.strip() for segment in head.split(",")]
                items.append(match.group("tail").strip())
                if len(items) < 3:
                    continue
                if any(len(item.split()) > MAX_LIST_ITEM_WORDS for item in items):
                    continue
                findings.append(
                    Finding(
                        rule="3.8.2",
                        severity=context.severity_for("3.8.2"),
                        kind="violation",
                        message=(
                            "a list of three or more items omits the comma before "
                            f"{match.group('conjunction')!r} (§3.8.2)"
                        ),
                        path=unit.span.path,
                        start_line=sentence.line,
                        end_line=sentence.line,
                        checker="serial-comma",
                        excerpt=match.group(0)[:120],
                    )
                )
    return findings

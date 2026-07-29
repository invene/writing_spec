"""Phrase-list checks, driven entirely by the generated lists.

No literal string in this module names a prohibited word. Every pattern comes
from a phrase-list paragraph in the authoritative Markdown (§8.2.1), so the
living lists have exactly one home.
"""

from __future__ import annotations

import re
from typing import Iterable

from itws.lint.model import Finding, LintContext
from itws.lint.registry import register
from itws.lint.text import body_units, prose_units, split_sentences

#: Rules whose findings come only from their phrase list.
PHRASE_DRIVEN_RULES = (
    "2.1.3",
    "2.3.3",
    "2.6.3",
    "2.6.4",
    "2.6.6",
    "2.6.7",
    "2.6.9",
    "2.6.11",
    "3.9.1",
    "3.10.2",
    "3.10.4",
    "3.10.6",
    "4.10.5",
    "6.5.4",
)

#: A `partial` rule reports a candidate; a `yes` rule reports a violation.
CANDIDATE_RULES = frozenset({"2.6.9", "3.10.6", "6.5.4"})


def _compile(pattern: str, kind: str, ignore_case: bool) -> re.Pattern[str]:
    flags = re.IGNORECASE if ignore_case else 0
    if kind == "word":
        return re.compile(rf"\b{re.escape(pattern)}\b", flags)
    if kind == "phrase":
        return re.compile(re.escape(pattern), flags)
    if kind == "opener":
        return re.compile(rf"^\W*{re.escape(pattern)}\b", flags)
    return re.compile(pattern, flags)


def _scan(context: LintContext, rule_id: str) -> Iterable[Finding]:
    entries = [entry for entry in context.spec.phrase_lists if entry.rule == rule_id]
    if not entries:
        return
    kind = "candidate" if rule_id in CANDIDATE_RULES else "violation"
    severity = context.severity_for(rule_id)
    openers = [entry for entry in entries if entry.kind == "opener"]
    others = [entry for entry in entries if entry.kind != "opener"]

    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            line_number = unit.span.start_line + line_offset
            for entry in others:
                matcher = _compile(entry.pattern, entry.kind, entry.ignore_case)
                for match in matcher.finditer(line):
                    yield Finding(
                        rule=rule_id,
                        severity=severity,
                        kind=kind,
                        message=entry.message,
                        path=unit.span.path,
                        start_line=line_number,
                        end_line=line_number,
                        checker=f"phrase-list:{entry.id}",
                        excerpt=match.group(0),
                        repair=entry.replacement,
                    )
        if openers:
            for sentence in split_sentences(unit):
                for entry in openers:
                    matcher = _compile(entry.pattern, entry.kind, entry.ignore_case)
                    match = matcher.search(sentence.text)
                    if match:
                        yield Finding(
                            rule=rule_id,
                            severity=severity,
                            kind=kind,
                            message=entry.message,
                            path=unit.span.path,
                            start_line=sentence.line,
                            end_line=sentence.line,
                            checker=f"phrase-list:{entry.id}",
                            excerpt=match.group(0),
                            repair=entry.replacement,
                        )


def _make(rule_id: str):
    def checker(context: LintContext) -> Iterable[Finding]:
        return list(_scan(context, rule_id))

    checker.__name__ = f"phrase_list_{rule_id.replace('.', '_')}"
    return checker


for _rule in PHRASE_DRIVEN_RULES:
    register(_rule, name=f"phrase-list:{_rule}")(_make(_rule))


@register("2.6.10", name="stacked-connectives")
def stacked_connectives(context: LintContext) -> Iterable[Finding]:
    """Rule 2.6.10 prohibits stacking, so one covered opener is compliant."""
    entries = [entry for entry in context.spec.phrase_lists if entry.rule == "2.6.10"]
    if not entries:
        return []
    matchers = [
        (entry, _compile(entry.pattern, entry.kind, entry.ignore_case))
        for entry in entries
    ]
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        run: list[tuple[int, str, str]] = []
        for sentence in split_sentences(unit):
            hit = next(
                (
                    (entry, matcher.search(sentence.text))
                    for entry, matcher in matchers
                    if matcher.search(sentence.text)
                ),
                None,
            )
            if hit:
                entry, match = hit
                run.append((sentence.line, match.group(0), entry.id))
            else:
                run = []
            if len(run) >= 2:
                findings.append(
                    Finding(
                        rule="2.6.10",
                        severity=context.severity_for("2.6.10"),
                        kind="violation",
                        message=(
                            "consecutive sentences open with a covered connective "
                            f"({run[-2][1]!r}, then {run[-1][1]!r}); §2.6.10 "
                            "prohibits stacking"
                        ),
                        path=unit.span.path,
                        start_line=run[-2][0],
                        end_line=sentence.line,
                        checker=f"phrase-list:{run[-1][2]}",
                        excerpt=run[-1][1],
                    )
                )
                run = []
    return findings


@register("2.6.5", name="agency-verbs")
def agency_verbs(context: LintContext) -> Iterable[Finding]:
    """A covered agency verb is a candidate until its definition is found."""
    entries = [entry for entry in context.spec.phrase_lists if entry.rule == "2.6.5"]
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            for entry in entries:
                matcher = _compile(entry.pattern, entry.kind, entry.ignore_case)
                match = matcher.search(line)
                if not match:
                    continue
                findings.append(
                    Finding(
                        rule="2.6.5",
                        severity=context.severity_for("2.6.5"),
                        kind="candidate",
                        message=(
                            f"{entry.message}; confirm that the subject is human "
                            "or that §2.6.5 defines the verb operationally"
                        ),
                        path=unit.span.path,
                        start_line=unit.span.start_line + line_offset,
                        end_line=unit.span.start_line + line_offset,
                        checker=f"phrase-list:{entry.id}",
                        excerpt=match.group(0),
                    )
                )
    return findings


@register("2.6.8", name="vague-authority")
def vague_authority(context: LintContext) -> Iterable[Finding]:
    """Vague attribution is a candidate: a nearby citation may resolve it."""
    entries = [entry for entry in context.spec.phrase_lists if entry.rule == "2.6.8"]
    findings: list[Finding] = []
    for unit in body_units(context.manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            for entry in entries:
                matcher = _compile(entry.pattern, entry.kind, entry.ignore_case)
                match = matcher.search(line)
                if not match:
                    continue
                findings.append(
                    Finding(
                        rule="2.6.8",
                        severity=context.severity_for("2.6.8"),
                        kind="candidate",
                        message=f"{entry.message}; name and cite the source",
                        path=unit.span.path,
                        start_line=unit.span.start_line + line_offset,
                        end_line=unit.span.start_line + line_offset,
                        checker=f"phrase-list:{entry.id}",
                        excerpt=match.group(0),
                    )
                )
    return findings

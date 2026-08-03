"""Checks for the hosted comment-set surface (§4.13).

Every checker here reads the :class:`itws.comments.CommentSetManifest` that
the runner supplies for a `maintenance-comment` unit. Each checker reports
mechanical facts under its own rule. Information delta, inferred intent,
basis sufficiency, and code-comment conflict remain reader judgments and
have no checker (Rules 4.13.1, 4.13.5, 4.13.6).
"""

from __future__ import annotations

from typing import Iterable

from itws.comments.changeset import CommentSetManifest, comment_scan_path
from itws.comments.records import CommentRecord
from itws.lint.model import Finding, LintContext
from itws.lint.registry import register
from itws.model import SourceSpan


def _comment_set(context: LintContext) -> CommentSetManifest | None:
    return getattr(context, "comment_set", None)


def _finding(
    context: LintContext,
    rule: str,
    kind: str,
    message: str,
    span: SourceSpan,
    checker: str,
    excerpt: str = "",
) -> Finding:
    return Finding(
        rule=rule,
        severity=context.severity_for(rule),
        kind=kind,
        message=message,
        path=span.path or context.manifest.path,
        start_line=max(span.start_line, 1),
        end_line=max(span.end_line, 1),
        checker=checker,
        excerpt=excerpt,
    )


def _record_findings(
    context: LintContext,
    rule: str,
    kind: str,
    checker: str,
    pairs: Iterable[tuple[CommentRecord, str]],
    citation: str,
) -> list[Finding]:
    return [
        _finding(
            context,
            rule,
            kind,
            f"comment {record.comment_id or '(unnamed)'}: {message} ({citation})",
            record.span,
            checker,
            excerpt=record.text[:80],
        )
        for record, message in pairs
    ]


@register("4.3.1", name="carrier-declarations")
def carrier_declarations(context: LintContext) -> Iterable[Finding]:
    """The declaration carrier states every required declaration."""
    comment_set = _comment_set(context)
    if comment_set is None:
        if context.spec.profile(context.profile) is not None and (
            context.spec.profile(context.profile).surface == "hosted-comment-set"
        ):
            return [
                Finding(
                    rule="4.3.1",
                    severity=context.severity_for("4.3.1"),
                    kind="violation",
                    message=(
                        "a maintenance-comment unit is a hosted comment set; "
                        "supply its declaration carrier (§0.2.1, §4.3.1)"
                    ),
                    path=context.manifest.path,
                    start_line=1,
                    end_line=1,
                    checker="carrier-declarations",
                )
            ]
        return []
    span = SourceSpan(comment_set.carrier_path, 1, 1)
    return [
        _finding(
            context, "4.3.1", "violation", f"{problem} (§4.3.1, §0.4.3)",
            span, "carrier-declarations",
        )
        for problem in comment_set.declaration_problems
    ]


@register("4.3.3", name="carrier-slots")
def carrier_slots(context: LintContext) -> Iterable[Finding]:
    """Every governed comment has one complete carrier record."""
    comment_set = _comment_set(context)
    if comment_set is None:
        return []
    findings: list[Finding] = []
    for unit in comment_set.uncovered_markers():
        findings.append(
            _finding(
                context,
                "4.3.3",
                "violation",
                (
                    "a changed marker has no comment record in the carrier; "
                    "Annex E §E.12 requires one per governed comment (§4.3.3)"
                ),
                unit.span,
                "carrier-slots",
                excerpt=unit.text[:80],
            )
        )
    findings.extend(
        _record_findings(
            context,
            "4.3.3",
            "violation",
            "carrier-slots",
            comment_set.unmatched_records(),
            "§4.3.3",
        )
    )
    return findings


@register("4.13.2", name="comment-purpose")
def comment_purpose(context: LintContext) -> Iterable[Finding]:
    """Each record declares exactly one closed purpose."""
    comment_set = _comment_set(context)
    if comment_set is None:
        return []
    return _record_findings(
        context, "4.13.2", "violation", "comment-purpose",
        comment_set.purpose_problems(), "Rule 4.13.2",
    )


@register("4.13.3", name="comment-anchor")
def comment_anchor(context: LintContext) -> Iterable[Finding]:
    """Each anchor resolves to one construct span in the proposed source."""
    comment_set = _comment_set(context)
    if comment_set is None:
        return []
    return _record_findings(
        context, "4.13.3", "violation", "comment-anchor",
        comment_set.anchor_problems(), "Rule 4.13.3",
    )


@register("4.13.4", name="comment-basis")
def comment_basis(context: LintContext) -> Iterable[Finding]:
    """A rationale, invariant, or history comment names a basis.

    The rule is `partial`: presence is mechanical, durability is a reader
    judgment, so every finding is a candidate.
    """
    comment_set = _comment_set(context)
    if comment_set is None:
        return []
    return _record_findings(
        context, "4.13.4", "candidate", "comment-basis",
        comment_set.basis_gaps(), "Rule 4.13.4",
    )


@register("4.13.7", name="removal-condition")
def removal_condition(context: LintContext) -> Iterable[Finding]:
    """A temporary comment records an observable removal condition."""
    comment_set = _comment_set(context)
    if comment_set is None:
        return []
    return _record_findings(
        context, "4.13.7", "violation", "removal-condition",
        comment_set.lifecycle_problems(), "Rule 4.13.7",
    )


@register("4.13.8", name="marker-grammar")
def marker_grammar(context: LintContext) -> Iterable[Finding]:
    """A changed marker follows TODO(<reference>): <removal condition>."""
    comment_set = _comment_set(context)
    if comment_set is None:
        return []
    return [
        _finding(
            context,
            "4.13.8",
            "violation",
            f"marker {text!r} {message} (Rule 4.13.8)",
            span,
            "marker-grammar",
            excerpt=text[:80],
        )
        for text, span, message in comment_set.marker_problems()
    ]


@register("4.13.9", name="comment-scan-path")
def scan_path_check(context: LintContext) -> Iterable[Finding]:
    """The scan path has its change-set ID, anchors, and comments.

    The rule is `partial`: extraction is mechanical, and whether the path
    preserves each comment's knowledge is a reader judgment.
    """
    comment_set = _comment_set(context)
    if comment_set is None:
        return []
    path = comment_scan_path(comment_set)
    span = SourceSpan(comment_set.carrier_path, 1, 1)
    return [
        _finding(
            context, "4.13.9", "candidate", str(problem), span,
            "comment-scan-path",
        )
        for problem in path["problems"]
    ]


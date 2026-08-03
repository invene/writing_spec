"""Checks for the binary machine-report contract in Part 8."""

from __future__ import annotations

from typing import Iterable

from itws.lint.model import Finding, LintContext
from itws.lint.registry import register, registrations
from itws.vocab import SEVERITY_BY_CLASS


def _finding(
    context: LintContext,
    rule: str,
    kind: str,
    message: str,
    checker: str,
) -> Finding:
    return Finding(
        rule=rule,
        severity=context.severity_for(rule),
        kind=kind,
        message=message,
        path=context.manifest.path,
        start_line=1,
        end_line=1,
        checker=checker,
    )


@register("8.2.1", scope="tooling", name="binary-result")
def binary_result(context: LintContext) -> Iterable[Finding]:
    """The report model derives fail only from error violations."""
    return ()


@register("8.2.2", scope="tooling", name="severity-map")
def severity_map(context: LintContext) -> Iterable[Finding]:
    """Every registered rule resolves to its declared class severity."""
    findings: list[Finding] = []
    for rule_id in registrations():
        rule = context.spec.rule(rule_id)
        if rule is None:
            findings.append(
                _finding(
                    context,
                    "8.2.2",
                    "violation",
                    f"a checker is registered for unknown rule {rule_id}",
                    "severity-map",
                )
            )
            continue
        expected = SEVERITY_BY_CLASS[rule.rule_class]
        if context.severity_for(rule_id) != expected:
            findings.append(
                _finding(
                    context,
                    "8.2.2",
                    "violation",
                    f"rule {rule_id} maps to {context.severity_for(rule_id)}; "
                    f"its {rule.rule_class} class requires {expected}",
                    "severity-map",
                )
            )
    return findings


@register("8.2.3", scope="tooling", name="version-profile-pin")
def version_profile_pin(context: LintContext) -> Iterable[Finding]:
    """The run uses the governed unit's declared version and profile."""
    declarations = context.manifest.declarations
    if declarations is None:
        return (
            _finding(
                context,
                "8.2.3",
                "violation",
                "the required version and profile declarations are missing or "
                "ambiguous (§0.4.3, Rule 8.2.3)",
                "version-profile-pin",
            ),
        )
    findings: list[Finding] = []
    if declarations.itws_version != context.spec.version:
        findings.append(
            Finding(
                rule="8.2.3",
                severity=context.severity_for("8.2.3"),
                kind="violation",
                message=(
                    f"the governed unit declares ITWS "
                    f"{declarations.itws_version}, but the run loaded "
                    f"{context.spec.version} (Rule 8.2.3)"
                ),
                path=context.manifest.path,
                start_line=declarations.span.start_line,
                end_line=declarations.span.end_line,
                checker="version-profile-pin",
            )
        )
    if declarations.profile != context.profile:
        findings.append(
            Finding(
                rule="8.2.3",
                severity=context.severity_for("8.2.3"),
                kind="violation",
                message=(
                    f"the governed unit declares profile "
                    f"{declarations.profile!r}, but the run used "
                    f"{context.profile!r} (Rule 8.2.3)"
                ),
                path=context.manifest.path,
                start_line=declarations.span.start_line,
                end_line=declarations.span.end_line,
                checker="version-profile-pin",
            )
        )
    return findings


@register("8.6.1", scope="tooling", name="generation-contract")
def generation_contract(context: LintContext) -> Iterable[Finding]:
    """Report generated-artifact defects when the caller checked them."""
    if context.artifact_problems is None:
        return (
            _finding(
                context,
                "8.6.1",
                "skipped",
                "generated artifacts were not checked in this lint run",
                "generation-contract",
            ),
        )
    return tuple(
        _finding(
            context,
            "8.6.1",
            "violation",
            problem,
            "generation-contract",
        )
        for problem in context.artifact_problems
    )


@register("8.6.2", scope="tooling", name="stale-artifacts")
def stale_artifacts(context: LintContext) -> Iterable[Finding]:
    """A stale generated artifact is a decidable machine failure."""
    if context.artifact_problems is None:
        return (
            _finding(
                context,
                "8.6.2",
                "skipped",
                "artifact freshness was not checked in this lint run",
                "stale-artifacts",
            ),
        )
    return tuple(
        _finding(
            context,
            "8.6.2",
            "violation",
            problem,
            "stale-artifacts",
        )
        for problem in context.artifact_problems
        if "stale generated artifact" in problem
        or "missing generated artifact" in problem
    )


@register("8.6.6", scope="tooling", name="coverage-aware-report")
def coverage_aware_report(context: LintContext) -> Iterable[Finding]:
    """The :class:`LintReport` serializer supplies the required fields."""
    return ()

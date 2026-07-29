"""The lint runner.

The runner resolves the version and profile, selects the applicable rules
from the profile envelope, runs every registered checker, and combines the
findings under one schema.
"""

from __future__ import annotations

from pathlib import Path

from itws.document import StructuralManifest, parse_document
from itws.lint.model import Evidence, Finding, LintContext, LintReport
from itws.lint.registry import registrations
from itws.lint.text import body_units, flesch_kincaid, split_sentences
from itws.model import Specification


def run_lint(
    spec: Specification,
    manifest: StructuralManifest,
    *,
    profile: str,
    tier: str,
    evidence: Evidence | None = None,
    network: bool = False,
    comment_set=None,
) -> LintReport:
    """Run every applicable check and return one combined report."""
    evidence = evidence or Evidence()
    evidence.network_checks_enabled = network
    context = LintContext(
        spec=spec,
        manifest=manifest,
        profile=profile,
        tier=tier,
        evidence=evidence,
        comment_set=comment_set,
    )

    findings: list[Finding] = []
    checked: list[str] = []
    skipped: list[str] = []

    for rule_id, entries in registrations().items():
        if not context.rule_applies(rule_id):
            skipped.append(rule_id)
            continue
        checked.append(rule_id)
        for entry in entries:
            findings.extend(entry.checker(context))

    # Rule 8.2.1 is evaluated last: it depends on every other finding.
    outstanding = [
        finding
        for finding in findings
        if finding.severity == "error" and finding.kind == "violation"
    ]
    if context.rule_applies("8.2.1") and outstanding:
        waived = {waiver.get("rule", "") for waiver in evidence.waivers}
        unwaived = sorted({finding.rule for finding in outstanding} - waived)
        if unwaived:
            findings.append(
                Finding(
                    rule="8.2.1",
                    severity=context.severity_for("8.2.1"),
                    kind="violation",
                    message=(
                        f"{len(outstanding)} error-severity finding(s) remain "
                        f"without a waiver, from rule(s) {', '.join(unwaived)}; "
                        "§8.2.1 requires a lint-gate outcome"
                    ),
                    path=manifest.path,
                    start_line=1,
                    end_line=1,
                    checker="lint-gate",
                )
            )

    sentences = [
        sentence
        for unit in body_units(manifest)
        for sentence in split_sentences(unit)
    ]

    return LintReport(
        path=manifest.path,
        itws_version=spec.version,
        profile=profile,
        tier=tier,
        findings=tuple(sorted(findings, key=lambda finding: finding.sort_key)),
        checked_rules=tuple(sorted(checked)),
        skipped_rules=tuple(sorted(skipped)),
        readability=flesch_kincaid(sentences),
    )


def lint_path(
    spec: Specification,
    path: Path,
    *,
    profile: str | None = None,
    tier: str | None = None,
    evidence: Evidence | None = None,
    network: bool = False,
) -> LintReport:
    """Parse a document and lint it against its own declarations."""
    provisional = parse_document(path)
    declared = provisional.declarations
    resolved_profile = profile or (declared.profile if declared else "")
    if not resolved_profile:
        raise ValueError(
            f"{path}: the document declares no profile and none was supplied"
        )
    skeleton = spec.skeleton(resolved_profile)
    manifest = parse_document(path, skeleton=skeleton)
    manifest.profile_envelope = tuple(
        rule.number for rule in spec.envelope(resolved_profile)
    )
    resolved_tier = tier or (declared.tier if declared else "core")
    return run_lint(
        spec,
        manifest,
        profile=resolved_profile,
        tier=resolved_tier,
        evidence=evidence,
        network=network,
    )

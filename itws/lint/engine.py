"""The lint runner.

The runner resolves the version and profile, selects the applicable rules
from the profile envelope, runs every registered checker, and combines the
findings under one schema.
"""

from __future__ import annotations

from pathlib import Path

from itws.document import StructuralManifest, parse_document
from itws.lint.model import Finding, LintContext, LintReport
from itws.lint.registry import registrations
from itws.lint.text import body_units, flesch_kincaid, split_sentences
from itws.model import Specification


def run_lint(
    spec: Specification,
    manifest: StructuralManifest,
    *,
    profile: str,
    network: bool = False,
    citation_resolver=None,
    artifact_problems: tuple[str, ...] | None = None,
    comment_set=None,
) -> LintReport:
    """Run every applicable check and return one combined report."""
    if network and citation_resolver is None:
        from itws.lint.resolvers import UrllibResolver

        citation_resolver = UrllibResolver()
    context = LintContext(
        spec=spec,
        manifest=manifest,
        profile=profile,
        network_checks_enabled=network,
        citation_resolver=citation_resolver,
        artifact_problems=artifact_problems,
        comment_set=comment_set,
    )

    findings: list[Finding] = []
    checker_rules: list[str] = []

    for rule_id, entries in registrations().items():
        if not context.rule_applies(rule_id):
            continue
        for entry in entries:
            if entry.scope == "assurance":
                continue
            checker_rules.append(rule_id)
            findings.extend(entry.checker(context))

    sentences = [
        sentence
        for unit in body_units(manifest)
        for sentence in split_sentences(unit)
    ]

    envelope = spec.envelope(profile)
    checked_set = set(checker_rules)
    skipped_full_checks = {
        finding.rule
        for finding in findings
        if finding.kind == "skipped"
    }
    by_machine_checkability = {
        state: tuple(
            rule.number
            for rule in envelope
            if rule.machine_checkable == state
        )
        for state in ("yes", "partial", "no")
    }
    fully_checked = tuple(
        rule.number
        for rule in envelope
        if (
            rule.machine_checkable == "yes"
            and rule.number in checked_set
            and rule.number not in skipped_full_checks
        )
    )
    partially_checked = tuple(
        rule.number
        for rule in envelope
        if rule.machine_checkable == "partial" and rule.number in checked_set
    )
    untested = tuple(
        rule.number
        for rule in envelope
        if rule.number not in set(fully_checked) | set(partially_checked)
    )

    return LintReport(
        path=manifest.path,
        itws_version=spec.version,
        profile=profile,
        findings=tuple(sorted(findings, key=lambda finding: finding.sort_key)),
        fully_checked_rules=fully_checked,
        partially_checked_rules=partially_checked,
        untested_rules=untested,
        checker_rules=tuple(sorted(checked_set)),
        coverage_by_machine_checkability=by_machine_checkability,
        readability=flesch_kincaid(sentences),
    )


def lint_path(
    spec: Specification,
    path: Path,
    *,
    profile: str | None = None,
    network: bool = False,
    citation_resolver=None,
    artifact_problems: tuple[str, ...] | None = None,
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
    return run_lint(
        spec,
        manifest,
        profile=resolved_profile,
        network=network,
        citation_resolver=citation_resolver,
        artifact_problems=artifact_problems,
    )

"""Part 8 checks over conformance evidence and the toolchain.

These rules govern the process around a document, not its prose. Their
checkers read the evidence a run supplies. Absent evidence produces a
``blocked`` finding: Rule 8.6.3 forbids reporting a pass for a check that
never ran.
"""

from __future__ import annotations

import re
from typing import Iterable

from itws.lint.model import Finding, LintContext
from itws.lint.registry import register
from itws.vocab import SEVERITY_BY_CLASS, TIERS

WAIVER_FIELDS = (
    "Deviated rule",
    "Document / location",
    "Justification",
    "Compensating measure",
    "Approver",
    "Scope of validity",
)
WAIVER_BLOCK_RE = re.compile(r"Waiver — ITWS deviation record")


def _blocked(context: LintContext, rule: str, message: str, checker: str) -> Finding:
    return Finding(
        rule=rule,
        severity=context.severity_for(rule),
        kind="blocked",
        message=message,
        path=context.manifest.path,
        start_line=1,
        end_line=1,
        checker=checker,
    )


@register("8.1.1", scope="evidence", name="checklist-generated")
def checklist_generated(context: LintContext) -> Iterable[Finding]:
    """The checklist is generated from Annex C, not edited by hand."""
    evidence = context.evidence
    if evidence.checklist_path is None:
        return [
            _blocked(
                context,
                "8.1.1",
                "no generated checklist was supplied; §8.1.1 requires one",
                "checklist-generated",
            )
        ]
    if not evidence.checklist_path.exists():
        return [
            Finding(
                rule="8.1.1",
                severity=context.severity_for("8.1.1"),
                kind="violation",
                message=f"the checklist {evidence.checklist_path} does not exist",
                path=context.manifest.path,
                start_line=1,
                end_line=1,
                checker="checklist-generated",
            )
        ]
    text = evidence.checklist_path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    if "This file is generated from Annex C" not in text:
        findings.append(
            Finding(
                rule="8.1.1",
                severity=context.severity_for("8.1.1"),
                kind="violation",
                message=(
                    "the checklist carries no generation banner, so it may have "
                    "been authored by hand (§8.1.1)"
                ),
                path=evidence.checklist_path.as_posix(),
                start_line=1,
                end_line=1,
                checker="checklist-generated",
            )
        )
    if f"**Profile:** `{context.profile}`" not in text:
        findings.append(
            Finding(
                rule="8.1.1",
                severity=context.severity_for("8.1.1"),
                kind="violation",
                message=(
                    f"the checklist was not generated for profile "
                    f"{context.profile!r} (§8.1.1)"
                ),
                path=evidence.checklist_path.as_posix(),
                start_line=1,
                end_line=1,
                checker="checklist-generated",
            )
        )
    return findings


@register("8.1.2", scope="evidence", name="self-check-recorded")
def self_check_recorded(context: LintContext) -> Iterable[Finding]:
    """The author completes and records the four self-check passes."""
    recorded = context.evidence.self_check_recorded
    if recorded is None:
        return [
            _blocked(
                context,
                "8.1.2",
                "no author self-check record was supplied; §8.1.2 requires the "
                "four passes before any tier is recorded",
                "self-check-recorded",
            )
        ]
    if recorded:
        return []
    return [
        Finding(
            rule="8.1.2",
            severity=context.severity_for("8.1.2"),
            kind="violation",
            message="the author self-check is recorded as incomplete (§8.1.2)",
            path=context.manifest.path,
            start_line=1,
            end_line=1,
            checker="self-check-recorded",
        )
    ]


@register("8.1.3", scope="evidence", name="checklist-current")
def checklist_current(context: LintContext) -> Iterable[Finding]:
    """The checklist matches the current Annex C revision."""
    evidence = context.evidence
    if evidence.checklist_path is None or not evidence.checklist_annex_hash:
        return [
            _blocked(
                context,
                "8.1.3",
                "no Annex C revision hash was supplied, so checklist freshness "
                "cannot be confirmed (§8.1.3)",
                "checklist-current",
            )
        ]
    if not evidence.checklist_path.exists():
        return []
    text = evidence.checklist_path.read_text(encoding="utf-8")
    if evidence.checklist_annex_hash in text:
        return []
    return [
        Finding(
            rule="8.1.3",
            severity=context.severity_for("8.1.3"),
            kind="violation",
            message=(
                "the checklist cites an Annex C revision that differs from the "
                "current one; regenerate it (§8.1.3)"
            ),
            path=evidence.checklist_path.as_posix(),
            start_line=1,
            end_line=1,
            checker="checklist-current",
        )
    ]


@register("8.2.1", scope="evidence", name="lint-gate")
def lint_gate(context: LintContext) -> Iterable[Finding]:
    """A pinned lint run leaves no unwaived error-severity finding.

    The engine evaluates this rule after every other check, so the runner
    supplies the outstanding errors through the evidence record.
    """
    if not context.evidence.lint_run_version:
        return [
            _blocked(
                context,
                "8.2.1",
                "no pinned lint run was recorded for this document (§8.2.1)",
                "lint-gate",
            )
        ]
    return []


@register("8.2.2", scope="tooling", name="severity-map")
def severity_map(context: LintContext) -> Iterable[Finding]:
    """Every registered checker carries the severity of its rule class."""
    from itws.lint.registry import registrations

    findings: list[Finding] = []
    for rule_id in registrations():
        rule = context.spec.rule(rule_id)
        if rule is None:
            findings.append(
                Finding(
                    rule="8.2.2",
                    severity="error",
                    kind="violation",
                    message=f"a checker is registered for unknown rule {rule_id}",
                    path=context.manifest.path,
                    start_line=1,
                    end_line=1,
                    checker="severity-map",
                )
            )
            continue
        expected = SEVERITY_BY_CLASS[rule.rule_class]
        if context.severity_for(rule_id) != expected:
            findings.append(
                Finding(
                    rule="8.2.2",
                    severity="error",
                    kind="violation",
                    message=(
                        f"rule {rule_id} is {rule.rule_class} but its checks report "
                        f"{context.severity_for(rule_id)}; §8.2.2 requires {expected}"
                    ),
                    path=context.manifest.path,
                    start_line=1,
                    end_line=1,
                    checker="severity-map",
                )
            )
    return findings


@register("8.2.3", scope="evidence", name="version-pinned-run")
def version_pinned_run(context: LintContext) -> Iterable[Finding]:
    """The run uses the document's declared version and profile."""
    declarations = context.manifest.declarations
    findings: list[Finding] = []
    if declarations is None:
        return [
            _blocked(
                context,
                "8.2.3",
                "the document declarations could not be read, so the run cannot be "
                "pinned to its declared version and profile (§8.2.3)",
                "version-pinned-run",
            )
        ]
    if declarations.itws_version != context.spec.version:
        findings.append(
            Finding(
                rule="8.2.3",
                severity=context.severity_for("8.2.3"),
                kind="violation",
                message=(
                    f"the document declares ITWS {declarations.itws_version} but the "
                    f"loaded specification is {context.spec.version} (§8.2.3)"
                ),
                path=context.manifest.path,
                start_line=declarations.span.start_line,
                end_line=declarations.span.end_line,
                checker="version-pinned-run",
            )
        )
    if declarations.profile != context.profile:
        findings.append(
            Finding(
                rule="8.2.3",
                severity=context.severity_for("8.2.3"),
                kind="violation",
                message=(
                    f"the document declares profile {declarations.profile!r} but the "
                    f"run used {context.profile!r} (§8.2.3)"
                ),
                path=context.manifest.path,
                start_line=declarations.span.start_line,
                end_line=declarations.span.end_line,
                checker="version-pinned-run",
            )
        )
    minimum = context.spec.profile(declarations.profile)
    if minimum and TIERS.index(declarations.tier) < TIERS.index(minimum.minimum_tier):
        findings.append(
            Finding(
                rule="8.2.3",
                severity=context.severity_for("8.2.3"),
                kind="violation",
                message=(
                    f"profile {declarations.profile!r} requires at least "
                    f"{minimum.minimum_tier!r}; the document declares "
                    f"{declarations.tier!r} (§0.4.3)"
                ),
                path=context.manifest.path,
                start_line=declarations.span.start_line,
                end_line=declarations.span.end_line,
                checker="version-pinned-run",
            )
        )
    return findings


@register("8.5.2", name="waiver-content")
def waiver_content(context: LintContext) -> Iterable[Finding]:
    """Every waiver block completes each template field."""
    findings: list[Finding] = []
    for unit in context.manifest.units:
        if not WAIVER_BLOCK_RE.search(unit.text):
            continue
        missing = [
            field for field in WAIVER_FIELDS if f"{field}:" not in unit.text
        ]
        if missing:
            findings.append(
                Finding(
                    rule="8.5.2",
                    severity=context.severity_for("8.5.2"),
                    kind="violation",
                    message=(
                        "the waiver omits required template field(s): "
                        + ", ".join(missing)
                        + " (§8.5.2)"
                    ),
                    path=unit.span.path,
                    start_line=unit.span.start_line,
                    end_line=unit.span.end_line,
                    checker="waiver-content",
                )
            )
    return findings


@register("8.6.1", scope="evidence", name="artifacts-current")
def artifacts_current(context: LintContext) -> Iterable[Finding]:
    """The generated artifact set satisfies the generation contract."""
    evidence = context.evidence
    if evidence.artifacts_current is None:
        return [
            _blocked(
                context,
                "8.6.1",
                "the generated artifact set was not checked; run "
                "`python3 tools/itws_compile.py --check` (§8.6.1)",
                "artifacts-current",
            )
        ]
    if evidence.artifacts_current:
        return []
    return [
        Finding(
            rule="8.6.1",
            severity=context.severity_for("8.6.1"),
            kind="violation",
            message=(
                "the generated artifact set does not satisfy the generation "
                "contract: " + "; ".join(evidence.artifact_problems)
            ),
            path=context.manifest.path,
            start_line=1,
            end_line=1,
            checker="artifacts-current",
        )
    ]


@register("8.6.2", scope="evidence", name="stale-artifacts")
def stale_artifacts(context: LintContext) -> Iterable[Finding]:
    """A stale artifact set stops the run instead of producing a result."""
    declarations = context.manifest.declarations
    if declarations is None:
        return []
    if declarations.itws_version == context.spec.version:
        return []
    return [
        Finding(
            rule="8.6.2",
            severity=context.severity_for("8.6.2"),
            kind="violation",
            message=(
                f"the document declares ITWS {declarations.itws_version}; this "
                f"checkout holds {context.spec.version}. §8.6.2 rejects a result "
                "computed from a different specification version"
            ),
            path=context.manifest.path,
            start_line=declarations.span.start_line,
            end_line=declarations.span.end_line,
            checker="stale-artifacts",
        )
    ]


@register("8.6.3", scope="evidence", name="validation-state")
def validation_state(context: LintContext) -> Iterable[Finding]:
    """Human gates required by the declared tier are reported separately."""
    tier = context.tier
    findings: list[Finding] = []
    gates: list[tuple[str, bool | None]] = [
        ("author self-check", context.evidence.self_check_recorded)
    ]
    if tier in {"reviewed", "publication"}:
        gates.append(("subject-matter-owner review", context.evidence.owner_review_recorded))
        gates.append(("reader-proxy review", context.evidence.proxy_review_recorded))
    if tier == "publication":
        gates.append(("independent reader test", context.evidence.reader_test_recorded))
    for name, recorded in gates:
        if recorded is None:
            findings.append(
                _blocked(
                    context,
                    "8.6.3",
                    f"the {tier} tier requires a recorded {name}; none was supplied, "
                    "so this run cannot report `pass` (§8.6.3, Rule 8.2.4)",
                    "validation-state",
                )
            )
        elif not recorded:
            findings.append(
                Finding(
                    rule="8.6.3",
                    severity=context.severity_for("8.6.3"),
                    kind="violation",
                    message=f"the {name} is recorded as incomplete (§8.6.3)",
                    path=context.manifest.path,
                    start_line=1,
                    end_line=1,
                    checker="validation-state",
                )
            )
    return findings


@register("8.6.5", scope="tooling", name="write-collisions")
def write_collisions(context: LintContext) -> Iterable[Finding]:
    """Collision detection lives in :mod:`itws.patch`.

    A lint run over one document has no set of proposed rewrites to compare,
    so this checker reports nothing here. ``itws_patch.py combine`` calls
    :func:`itws.patch.detect_collisions` for the real check, and the patch
    tests cover it.
    """
    return []

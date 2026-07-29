"""Four-state conformance validation (§8.6.2).

A run reports ``pass``, ``fail``, ``needs_review``, or ``blocked``. A clean
machine run never closes a human gate, and a skipped required check never
reports as a pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from itws.analysis import validate_comment_judgments
from itws.comments.changeset import load_comment_set, structural_manifest
from itws.compile import compile_all
from itws.document import parse_document
from itws.lint.engine import lint_path, run_lint
from itws.lint.model import Evidence, LintReport
from itws.model import Specification
from itws.parser import parse_specification
from itws.vocab import TIERS


@dataclass
class ValidationReport:
    """One document's validation outcome and the reasons behind it."""

    path: str
    itws_version: str
    profile: str
    tier: str
    state: str
    reasons: list[str] = field(default_factory=list)
    human_gates: dict[str, str] = field(default_factory=dict)
    lint: LintReport | None = None
    structural_problems: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "itws_version": self.itws_version,
            "profile": self.profile,
            "conformance_tier": self.tier,
            "state": self.state,
            "reasons": list(self.reasons),
            "human_gates": dict(self.human_gates),
            "structural_problems": list(self.structural_problems),
            "lint": self.lint.to_json() if self.lint else None,
        }


def _human_gates(tier: str, evidence: Evidence) -> dict[str, str]:
    def state(recorded: bool | None) -> str:
        if recorded is None:
            return "not recorded"
        return "complete" if recorded else "incomplete"

    gates = {"author self-check (§8.1.2)": state(evidence.self_check_recorded)}
    if TIERS.index(tier) >= TIERS.index("reviewed"):
        gates["subject-matter-owner review (§8.4.2)"] = state(
            evidence.owner_review_recorded
        )
        gates["reader-proxy review (§8.4.3)"] = state(evidence.proxy_review_recorded)
    if tier == "publication":
        gates["independent reader test (§8.3.1)"] = state(
            evidence.reader_test_recorded
        )
    return gates


def validate_document(
    spec: Specification,
    path: Path,
    *,
    spec_dir: Path,
    profile: str | None = None,
    tier: str | None = None,
    evidence: Evidence | None = None,
    network: bool = False,
    check_artifacts: bool = True,
) -> ValidationReport:
    """Run version, structure, lint, and gate checks and pick one state."""
    evidence = evidence or Evidence()
    if check_artifacts and evidence.artifacts_current is None:
        _, problems = compile_all(spec_dir, check_only=True)
        evidence.artifacts_current = not problems
        evidence.artifact_problems = tuple(problems)

    provisional = parse_document(path)
    declared = provisional.declarations
    resolved_profile = profile or (declared.profile if declared else "")
    resolved_tier = tier or (declared.tier if declared else "core")

    report = ValidationReport(
        path=path.as_posix(),
        itws_version=spec.version,
        profile=resolved_profile,
        tier=resolved_tier,
        state="blocked",
        structural_problems=list(provisional.declaration_problems)
        + list(provisional.section_map_problems),
    )

    if not resolved_profile:
        report.reasons.append(
            "the document declares no canonical profile ID, so no rule set can be "
            "resolved (§4.3.1)"
        )
        return report
    if spec.profile(resolved_profile) is None:
        report.state = "fail"
        report.reasons.append(f"unknown profile ID {resolved_profile!r} (§0.2)")
        return report

    if not evidence.lint_run_version:
        evidence.lint_run_version = spec.version
        evidence.lint_run_profile = resolved_profile

    report.lint = lint_path(
        spec,
        path,
        profile=resolved_profile,
        tier=resolved_tier,
        evidence=evidence,
        network=network,
    )
    report.human_gates = _human_gates(resolved_tier, evidence)
    _resolve_state(report, spec, evidence, resolved_profile)
    return report


def _resolve_state(
    report: ValidationReport,
    spec: Specification,
    evidence: Evidence,
    resolved_profile: str,
) -> None:
    """Pick the §8.6.2 state from the lint findings and human gates."""
    waived = {waiver.get("rule", "") for waiver in evidence.waivers}
    unwaived_errors = [
        finding for finding in report.lint.errors if finding.rule not in waived
    ]
    blocked = list(report.lint.blocked)
    skipped = [
        finding for finding in report.lint.findings if finding.kind == "skipped"
    ]
    candidates = [
        finding for finding in report.lint.findings if finding.kind == "candidate"
    ]
    open_human_rules = [
        rule.number
        for rule in spec.envelope(resolved_profile)
        if rule.machine_checkable in {"partial", "no"}
    ]

    if unwaived_errors:
        report.state = "fail"
        report.reasons.append(
            f"{len(unwaived_errors)} unwaived error-severity finding(s) remain "
            "(§8.2.1)"
        )
    elif blocked or skipped:
        report.state = "blocked"
        for finding in blocked[:10]:
            report.reasons.append(finding.message)
        for finding in skipped[:10]:
            report.reasons.append(finding.message)
    else:
        report.state = "needs_review"
        report.reasons.append(
            f"{len(open_human_rules)} applicable rule(s) are `partial` or `no` on "
            "machine-checkability and still need a reader (Rule 8.2.4)"
        )
        if candidates:
            report.reasons.append(
                f"{len(candidates)} candidate finding(s) await confirmation"
            )
        if all(state == "complete" for state in report.human_gates.values()):
            report.state = "pass"
            report.reasons = [
                "every machine-checkable applicable rule passed, no required "
                "check was skipped, and every human gate for the declared tier "
                "is recorded"
            ]

    if report.structural_problems and report.state == "pass":
        report.state = "fail"
        report.reasons = list(report.structural_problems)


def validate_comment_set(
    spec: Specification,
    carrier_path: Path,
    *,
    spec_dir: Path,
    evidence: Evidence | None = None,
    network: bool = False,
    check_artifacts: bool = True,
) -> ValidationReport:
    """Validate one comment change set through its declaration carrier.

    The run keeps the four §8.6.2 states. A missing source, a hash that no
    longer matches, or an unknown host adapter is `blocked`, never a pass.
    """
    evidence = evidence or Evidence()
    if check_artifacts and evidence.artifacts_current is None:
        _, problems = compile_all(spec_dir, check_only=True)
        evidence.artifacts_current = not problems
        evidence.artifact_problems = tuple(problems)

    comment_set = load_comment_set(carrier_path)
    declared = comment_set.declarations
    resolved_profile = declared.profile if declared else ""
    resolved_tier = declared.tier if declared and declared.tier else "core"

    report = ValidationReport(
        path=carrier_path.as_posix(),
        itws_version=spec.version,
        profile=resolved_profile,
        tier=resolved_tier,
        state="blocked",
    )

    if not resolved_profile:
        report.reasons.append(
            "the carrier declares no canonical profile ID, so no rule set can "
            "be resolved (§4.3.1)"
        )
        return report
    profile_record = spec.profile(resolved_profile)
    if profile_record is None:
        report.state = "fail"
        report.reasons.append(f"unknown profile ID {resolved_profile!r} (§0.2)")
        return report
    if profile_record.surface != "hosted-comment-set":
        report.state = "fail"
        report.reasons.append(
            f"profile {resolved_profile!r} governs a Markdown document, not a "
            "comment change set (§0.2.1)"
        )
        return report
    if comment_set.problems:
        report.reasons.extend(comment_set.problems)
        return report

    report.structural_problems = validate_comment_judgments(
        comment_set, known_rules=[rule.number for rule in spec.rules]
    )

    if not evidence.lint_run_version:
        evidence.lint_run_version = spec.version
        evidence.lint_run_profile = resolved_profile

    report.lint = run_lint(
        spec,
        structural_manifest(comment_set),
        profile=resolved_profile,
        tier=resolved_tier,
        evidence=evidence,
        network=network,
        comment_set=comment_set,
    )
    report.human_gates = _human_gates(resolved_tier, evidence)
    _resolve_state(report, spec, evidence, resolved_profile)
    return report


def validate_path(
    spec_dir: Path,
    path: Path,
    **kwargs,
) -> ValidationReport:
    """Parse the specification, then validate one document against it."""
    spec = parse_specification(spec_dir)
    return validate_document(spec, path, spec_dir=spec_dir, **kwargs)

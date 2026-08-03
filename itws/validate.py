"""Binary machine validation with explicit rule coverage.

The result is ``pass`` or ``fail``. It describes only the checks represented
in the attached lint report. Semantic candidates, skipped checks, and missing
source facts remain visible without becoming workflow states.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from itws.analysis import validate_comment_judgments
from itws.comments.changeset import load_comment_set, structural_manifest
from itws.compile import compile_all
from itws.document import parse_document
from itws.lint.engine import lint_path, run_lint
from itws.lint.model import LintReport
from itws.model import Specification
from itws.parser import parse_specification


@dataclass
class ValidationReport:
    """One governed unit's binary machine result."""

    path: str
    itws_version: str
    profile: str
    result: str = "fail"
    reasons: list[str] = field(default_factory=list)
    lint: LintReport | None = None
    structural_problems: list[str] = field(default_factory=list)
    artifact_problems: list[str] = field(default_factory=list)
    unresolved_facts: list[str] = field(default_factory=list)

    @property
    def candidates(self):
        return self.lint.candidates if self.lint else ()

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "itws_version": self.itws_version,
            "profile": self.profile,
            "result": self.result,
            "reasons": list(self.reasons),
            "structural_problems": list(self.structural_problems),
            "artifact_problems": list(self.artifact_problems),
            "candidates": [
                finding.to_json() for finding in self.candidates
            ],
            "unresolved_facts": list(self.unresolved_facts),
            "lint": self.lint.to_json() if self.lint else None,
        }


def _artifact_check(
    spec_dir: Path, check_artifacts: bool
) -> tuple[str, ...] | None:
    if not check_artifacts:
        return None
    _, problems = compile_all(spec_dir, check_only=True)
    return tuple(problems)


def _finish(report: ValidationReport) -> None:
    lint_errors = len(report.lint.errors) if report.lint else 0
    if report.structural_problems or report.artifact_problems or lint_errors:
        report.result = "fail"
        if report.structural_problems:
            report.reasons.append(
                f"{len(report.structural_problems)} structural problem(s)"
            )
        if report.artifact_problems:
            report.reasons.append(
                f"{len(report.artifact_problems)} generated-artifact problem(s)"
            )
        if lint_errors:
            report.reasons.append(
                f"{lint_errors} error-severity machine finding(s)"
            )
        return
    report.result = "pass"
    report.reasons.append(
        "no error-severity violation was found in the disclosed machine "
        "coverage; this is not full semantic conformance certification"
    )


def validate_document(
    spec: Specification,
    path: Path,
    *,
    spec_dir: Path,
    profile: str | None = None,
    network: bool = False,
    check_artifacts: bool = True,
) -> ValidationReport:
    """Validate one Markdown document without assurance inputs."""
    provisional = parse_document(path)
    declared = provisional.declarations
    resolved_profile = profile or (declared.profile if declared else "")
    report = ValidationReport(
        path=path.as_posix(),
        itws_version=spec.version,
        profile=resolved_profile,
        structural_problems=list(provisional.declaration_problems)
        + list(provisional.section_map_problems),
    )

    if not resolved_profile:
        if not report.structural_problems:
            report.structural_problems.append(
                "the governed unit declares no canonical profile ID"
            )
        _finish(report)
        return report
    profile_record = spec.profile(resolved_profile)
    if profile_record is None:
        report.structural_problems.append(
            f"unknown profile ID {resolved_profile!r} (§0.2)"
        )
        _finish(report)
        return report
    if profile_record.surface != "markdown-document":
        report.structural_problems.append(
            f"profile {resolved_profile!r} governs a hosted comment set, not "
            "a Markdown document (§0.2.1)"
        )
        _finish(report)
        return report

    artifact_problems = _artifact_check(spec_dir, check_artifacts)
    if artifact_problems is not None:
        report.artifact_problems.extend(artifact_problems)
    report.lint = lint_path(
        spec,
        path,
        profile=resolved_profile,
        network=network,
        artifact_problems=artifact_problems,
    )
    report.unresolved_facts.extend(
        finding.message for finding in report.lint.unresolved_facts
    )
    _finish(report)
    return report


def _question_text(question: object) -> str:
    if isinstance(question, dict):
        return str(
            question.get("question")
            or question.get("value")
            or question
        )
    return str(question)


def validate_comment_set(
    spec: Specification,
    carrier_path: Path,
    *,
    spec_dir: Path,
    network: bool = False,
    check_artifacts: bool = True,
) -> ValidationReport:
    """Validate one hosted comment set without provenance or approval gates."""
    comment_set = load_comment_set(carrier_path)
    declared = comment_set.declarations
    resolved_profile = declared.profile if declared else ""
    report = ValidationReport(
        path=carrier_path.as_posix(),
        itws_version=spec.version,
        profile=resolved_profile,
        structural_problems=list(comment_set.declaration_problems)
        + list(comment_set.problems),
        unresolved_facts=[
            _question_text(question)
            for question in comment_set.open_questions
        ],
    )

    if not resolved_profile:
        if not report.structural_problems:
            report.structural_problems.append(
                "the declaration carrier names no canonical profile ID"
            )
        _finish(report)
        return report
    profile_record = spec.profile(resolved_profile)
    if profile_record is None:
        report.structural_problems.append(
            f"unknown profile ID {resolved_profile!r} (§0.2)"
        )
        _finish(report)
        return report
    if profile_record.surface != "hosted-comment-set":
        report.structural_problems.append(
            f"profile {resolved_profile!r} governs a Markdown document, not "
            "a hosted comment set (§0.2.1)"
        )
        _finish(report)
        return report

    report.unresolved_facts.extend(
        validate_comment_judgments(
            comment_set, known_rules=[rule.number for rule in spec.rules]
        )
    )
    artifact_problems = _artifact_check(spec_dir, check_artifacts)
    if artifact_problems is not None:
        report.artifact_problems.extend(artifact_problems)
    report.lint = run_lint(
        spec,
        structural_manifest(comment_set),
        profile=resolved_profile,
        network=network,
        artifact_problems=artifact_problems,
        comment_set=comment_set,
    )
    report.unresolved_facts.extend(
        finding.message for finding in report.lint.unresolved_facts
    )
    _finish(report)
    return report


def validate_path(
    spec_dir: Path,
    path: Path,
    **kwargs,
) -> ValidationReport:
    """Parse the specification, then validate one Markdown document."""
    spec = parse_specification(spec_dir)
    return validate_document(spec, path, spec_dir=spec_dir, **kwargs)

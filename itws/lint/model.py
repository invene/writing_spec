"""Records the lint engine produces and consumes."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from itws.document import StructuralManifest
from itws.model import Specification
from itws.vocab import SEVERITY_BY_CLASS

#: What a finding asserts.
FINDING_KINDS = ("violation", "candidate", "review", "skipped", "blocked")


@dataclass(frozen=True)
class Finding:
    """One lint result, always attributable to a rule and a source span."""

    rule: str
    severity: str
    kind: str
    message: str
    path: str
    start_line: int
    end_line: int
    checker: str
    excerpt: str = ""
    repair: str = ""

    @property
    def sort_key(self) -> tuple[int, int, str, str]:
        return (self.start_line, self.end_line, self.rule, self.checker)

    def to_json(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "rule": self.rule,
            "severity": self.severity,
            "kind": self.kind,
            "message": self.message,
            "path": self.path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "checker": self.checker,
        }
        if self.excerpt:
            payload["excerpt"] = self.excerpt
        if self.repair:
            payload["repair"] = self.repair
        return payload


@dataclass
class Evidence:
    """Conformance evidence a run may supply for the Part 8 process rules.

    Every field defaults to absent. An absent field produces a `blocked`
    finding rather than a pass, which is what Rule 8.6.3 requires.
    """

    checklist_path: Path | None = None
    checklist_annex_hash: str = ""
    self_check_recorded: bool | None = None
    lint_run_version: str = ""
    lint_run_profile: str = ""
    waivers: tuple[dict[str, str], ...] = ()
    owner_review_recorded: bool | None = None
    proxy_review_recorded: bool | None = None
    reader_test_recorded: bool | None = None
    artifacts_current: bool | None = None
    artifact_problems: tuple[str, ...] = ()
    network_checks_enabled: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "checklist_path": (
                self.checklist_path.as_posix() if self.checklist_path else None
            ),
            "checklist_annex_hash": self.checklist_annex_hash,
            "self_check_recorded": self.self_check_recorded,
            "lint_run_version": self.lint_run_version,
            "lint_run_profile": self.lint_run_profile,
            "waiver_count": len(self.waivers),
            "owner_review_recorded": self.owner_review_recorded,
            "proxy_review_recorded": self.proxy_review_recorded,
            "reader_test_recorded": self.reader_test_recorded,
            "artifacts_current": self.artifacts_current,
            "artifact_problems": list(self.artifact_problems),
            "network_checks_enabled": self.network_checks_enabled,
        }


@dataclass
class LintContext:
    """Everything a checker may read."""

    spec: Specification
    manifest: StructuralManifest
    profile: str
    tier: str
    evidence: Evidence = field(default_factory=Evidence)

    def severity_for(self, rule_id: str) -> str:
        rule = self.spec.rule(rule_id)
        return SEVERITY_BY_CLASS[rule.rule_class] if rule else "error"

    def rule_applies(self, rule_id: str) -> bool:
        rule = self.spec.rule(rule_id)
        return bool(rule and rule.is_active and rule.applies_to_profile(self.profile))


@dataclass
class LintReport:
    """The complete result of one lint run."""

    path: str
    itws_version: str
    profile: str
    tier: str
    findings: tuple[Finding, ...]
    checked_rules: tuple[str, ...]
    skipped_rules: tuple[str, ...]
    readability: dict[str, float]

    @property
    def errors(self) -> tuple[Finding, ...]:
        return tuple(
            finding
            for finding in self.findings
            if finding.severity == "error" and finding.kind == "violation"
        )

    @property
    def blocked(self) -> tuple[Finding, ...]:
        return tuple(
            finding for finding in self.findings if finding.kind == "blocked"
        )

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "itws_version": self.itws_version,
            "profile": self.profile,
            "conformance_tier": self.tier,
            "counts": {
                "findings": len(self.findings),
                "errors": len(self.errors),
                "blocked": len(self.blocked),
                "checked_rules": len(self.checked_rules),
                "skipped_rules": len(self.skipped_rules),
            },
            "readability": self.readability,
            "checked_rules": list(self.checked_rules),
            "skipped_rules": list(self.skipped_rules),
            "findings": [finding.to_json() for finding in self.findings],
        }

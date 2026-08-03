"""Records the lint engine produces and consumes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from itws.document import Declarations, StructuralManifest
from itws.model import Specification
from itws.vocab import SEVERITY_BY_CLASS

if TYPE_CHECKING:
    from itws.comments.changeset import CommentSetManifest


class GovernedManifest(Protocol):
    """What the shared text checks require of any governed surface.

    :class:`itws.document.StructuralManifest` satisfies the protocol for a
    Markdown document, and :func:`itws.comments.structural_manifest` builds
    a satisfying view of a hosted comment set from stripped comment units.
    The protocol keeps one text-check implementation for both surfaces.
    """

    path: str
    document_hash: str
    declarations: Declarations | None
    line_count: int

    @property
    def units(self): ...

#: What a finding asserts.
FINDING_KINDS = ("violation", "candidate", "unresolved", "skipped")


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
class LintContext:
    """Everything a checker may read.

    ``comment_set`` is present only when the governed unit is a hosted
    comment set; the §4.13 and §8.7 checkers read it, and every other
    checker ignores it.
    """

    spec: Specification
    manifest: StructuralManifest
    profile: str
    network_checks_enabled: bool = False
    citation_resolver: object | None = None
    artifact_problems: tuple[str, ...] | None = None
    comment_set: "CommentSetManifest | None" = None

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
    findings: tuple[Finding, ...]
    fully_checked_rules: tuple[str, ...]
    partially_checked_rules: tuple[str, ...]
    untested_rules: tuple[str, ...]
    checker_rules: tuple[str, ...]
    coverage_by_machine_checkability: dict[str, tuple[str, ...]]
    readability: dict[str, float]

    @property
    def errors(self) -> tuple[Finding, ...]:
        return tuple(
            finding
            for finding in self.findings
            if finding.severity == "error" and finding.kind == "violation"
        )

    @property
    def candidates(self) -> tuple[Finding, ...]:
        return tuple(
            finding for finding in self.findings if finding.kind == "candidate"
        )

    @property
    def unresolved_facts(self) -> tuple[Finding, ...]:
        return tuple(
            finding
            for finding in self.findings
            if finding.kind in {"unresolved", "skipped"}
        )

    @property
    def result(self) -> str:
        return "fail" if self.errors else "pass"

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "itws_version": self.itws_version,
            "profile": self.profile,
            "result": self.result,
            "counts": {
                "findings": len(self.findings),
                "errors": len(self.errors),
                "candidates": len(self.candidates),
                "unresolved_facts": len(self.unresolved_facts),
                "fully_checked_rules": len(self.fully_checked_rules),
                "partially_checked_rules": len(self.partially_checked_rules),
                "untested_rules": len(self.untested_rules),
            },
            "readability": self.readability,
            "coverage": {
                "fully_checked_rules": list(self.fully_checked_rules),
                "partially_checked_rules": list(self.partially_checked_rules),
                "untested_rules": list(self.untested_rules),
                "checker_rules": list(self.checker_rules),
                "by_machine_checkability": {
                    state: list(rule_ids)
                    for state, rule_ids in sorted(
                        self.coverage_by_machine_checkability.items()
                    )
                },
            },
            "candidates": [
                finding.to_json() for finding in self.candidates
            ],
            "unresolved_facts": [
                finding.to_json() for finding in self.unresolved_facts
            ],
            "findings": [finding.to_json() for finding in self.findings],
        }

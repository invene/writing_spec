"""Lint coverage, severity, candidate handling, and the risk fixtures."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.support import (
    BLOCKED,
    CONFORMING,
    VIOLATIONS,
    conforming_documents,
    spec,
)

from itws.document import parse_document
from itws.lint.engine import lint_path, run_lint
from itws.lint.registry import registrations
from itws.lint.text import (
    counted_word_length,
    noun_clusters,
    split_sentences,
    unbalanced_math,
)
from itws.vocab import SEVERITY_BY_CLASS


def violations(report) -> list:
    return [f for f in report.findings if f.kind == "violation"]


class TestConformingFixtures(unittest.TestCase):
    def test_no_conforming_fixture_has_a_content_violation(self) -> None:
        for path in conforming_documents():
            report = lint_path(spec(), path)
            content = [
                finding
                for finding in violations(report)
                if not finding.rule.startswith("8.")
            ]
            with self.subTest(document=path.name):
                self.assertEqual(
                    content,
                    [],
                    "\n".join(
                        f"{f.rule} line {f.start_line}: {f.message}" for f in content
                    ),
                )

    def test_every_conforming_fixture_reaches_its_profile_checks(self) -> None:
        for path in conforming_documents():
            report = lint_path(spec(), path)
            with self.subTest(document=path.name):
                checked = len(report.fully_checked_rules) + len(
                    report.partially_checked_rules
                )
                self.assertGreater(checked, 40)
                self.assertTrue(report.readability["words"] > 0)


class TestSeverityMap(unittest.TestCase):
    def test_severity_always_follows_rule_class(self) -> None:
        report = lint_path(spec(), CONFORMING / "task.md")
        for finding in report.findings:
            rule = spec().rule(finding.rule)
            if rule is None:
                continue
            self.assertEqual(
                finding.severity, SEVERITY_BY_CLASS[rule.rule_class], finding.rule
            )

    def test_every_registered_checker_names_a_known_rule(self) -> None:
        for rule_id in registrations():
            self.assertIsNotNone(spec().rule(rule_id), rule_id)


class TestRiskFixtures(unittest.TestCase):
    def test_a_term_used_before_its_definition_is_flagged(self) -> None:
        report = lint_path(spec(), VIOLATIONS / "term-before-definition.md")
        rules = {finding.rule for finding in violations(report)}
        self.assertIn("2.3.1", rules)

    def test_a_reordered_safety_dependency_is_flagged(self) -> None:
        report = lint_path(spec(), VIOLATIONS / "procedure-reordered.md")
        found = [f for f in violations(report) if f.rule == "4.4.1"]
        self.assertTrue(found)
        self.assertIn("Steps", found[0].message)

    def test_a_missing_scan_opening_is_a_candidate(self) -> None:
        report = lint_path(spec(), VIOLATIONS / "scan-missing-opening.md")
        found = [
            finding
            for finding in report.findings
            if finding.rule == "4.12.1" and finding.kind == "candidate"
        ]
        self.assertTrue(found)
        self.assertIn("Risks", found[0].message)

    def test_a_trailing_scan_qualification_is_a_candidate(self) -> None:
        report = lint_path(spec(), VIOLATIONS / "scan-trailing-qualification.md")
        found = [
            finding
            for finding in report.findings
            if finding.rule == "4.12.3" and finding.kind == "candidate"
        ]
        self.assertTrue(found)
        self.assertIn("though", found[0].excerpt.casefold())

    def test_a_negated_scan_qualification_is_a_candidate(self) -> None:
        report = lint_path(spec(), VIOLATIONS / "scan-negation-qualification.md")
        found = [
            finding
            for finding in report.findings
            if finding.rule == "4.12.3" and finding.kind == "candidate"
        ]
        self.assertTrue(found)
        self.assertIn("not approved", found[0].excerpt.casefold())

    def test_a_stale_version_declaration_fails_pinning(self) -> None:
        report = lint_path(spec(), BLOCKED / "stale-version.md")
        rules = {finding.rule for finding in violations(report)}
        self.assertIn("8.2.3", rules)

    def test_missing_evidence_fixture_has_no_retired_process_rules(self) -> None:
        """Absent measurements stay in prose; process rules no longer block."""
        report = lint_path(spec(), BLOCKED / "missing-evidence.md")
        rules = {finding.rule for finding in violations(report)}
        retired_prefixes = ("8.1.", "8.3.", "8.4.", "8.5.", "8.7.")
        self.assertFalse(
            any(
                any(rule.startswith(prefix) for prefix in retired_prefixes)
                for rule in rules
            ),
            sorted(rules),
        )

    def test_a_partial_rule_reports_a_candidate_not_a_violation(self) -> None:
        report = lint_path(spec(), CONFORMING / "technical-report.md")
        for finding in report.findings:
            rule = spec().rule(finding.rule)
            if rule and rule.machine_checkable == "partial":
                self.assertIn(
                    finding.kind, {"candidate", "unresolved", "skipped"}
                )


class _StubResolver:
    """Resolve from a fixed table, so the check runs without a network."""

    def __init__(self, resolvable: set[str]) -> None:
        self.resolvable = resolvable
        self.asked: list[str] = []

    def resolve(self, target: str):
        from itws.lint.resolvers import Resolution

        self.asked.append(target)
        return Resolution(
            target, target in self.resolvable, "" if target in self.resolvable else "404"
        )


def _citation_findings(*, citation_resolver=None, network: bool = False):
    report = lint_path(
        spec(),
        CONFORMING / "research-paper.md",
        network=network,
        citation_resolver=citation_resolver,
    )
    return [finding for finding in report.findings if finding.rule == "5.4.3"]


class TestCitationResolution(unittest.TestCase):
    """Rule 5.4.3: the run never records a resolution it did not perform."""

    def test_without_a_resolver_each_target_is_skipped(self) -> None:
        findings = _citation_findings()
        self.assertTrue(findings)
        for finding in findings:
            self.assertEqual(finding.kind, "skipped")
        self.assertTrue(
            any("example.invalid" in finding.excerpt for finding in findings)
        )

    def test_an_unreachable_target_is_a_violation_when_resolved(self) -> None:
        resolver = _StubResolver(set())
        findings = _citation_findings(citation_resolver=resolver)
        self.assertTrue(resolver.asked)
        self.assertTrue(findings)
        for finding in findings:
            self.assertEqual(finding.kind, "violation")

    def test_a_reachable_target_produces_no_finding(self) -> None:
        resolver = _StubResolver(
            {"https://example.invalid/itws-fixture/checker"}
        )
        self.assertEqual(
            _citation_findings(citation_resolver=resolver), []
        )

    def test_the_default_run_asks_no_resolver(self) -> None:
        """§8.2: the default lint gate makes no network request."""
        resolver = _StubResolver(set())
        lint_path(spec(), CONFORMING / "decision-record.md")
        self.assertEqual(resolver.asked, [])


class TestTextHelpers(unittest.TestCase):
    def test_inline_math_counting_follows_rule_three_one_three(self) -> None:
        self.assertEqual(counted_word_length("The loss $L$ decreases fast."), 5)
        self.assertEqual(counted_word_length("We report $L(x) - L(y)$ here."), 6)

    def test_unbalanced_math_is_detected(self) -> None:
        self.assertFalse(unbalanced_math("balanced $x$ here"))
        self.assertTrue(unbalanced_math("unbalanced $x here"))

    def test_noun_clusters_need_a_determiner_anchor(self) -> None:
        from itws.lint.text import Sentence

        stacked = Sentence(
            text="the account service request timeout setting fails",
            unit_id="u",
            line=1,
            offset=0,
        )
        self.assertTrue(noun_clusters(stacked))
        plain = Sentence(
            text="Submit one test job and confirm the result.",
            unit_id="u",
            line=1,
            offset=0,
        )
        self.assertEqual(noun_clusters(plain), [])

    def test_sentences_keep_their_line_numbers(self) -> None:
        manifest = parse_document(CONFORMING / "explanation.md")
        for unit in manifest.units:
            for sentence in split_sentences(unit):
                self.assertGreaterEqual(sentence.line, unit.span.start_line)
                self.assertLessEqual(sentence.line, unit.span.end_line)


class TestPhraseDrivenChecks(unittest.TestCase):
    def test_a_prohibited_word_is_reported_with_its_generated_entry(self) -> None:
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        )
        handle.write(
            "# T\n\nITWS version: 0.10.0-draft\nProfile: explanation\n\n"
            "## Summary\n\n"
            "The cache is a pivotal part of the tapestry.\n"
        )
        handle.close()
        path = Path(handle.name)
        report = lint_path(spec(), path)
        hits = [f for f in report.findings if f.rule == "2.6.4"]
        self.assertGreaterEqual(len(hits), 2)
        for hit in hits:
            self.assertTrue(hit.checker.startswith("phrase-list:2.6.4/"))
        path.unlink()

    def test_stacked_connectives_need_two_consecutive_sentences(self) -> None:
        def lint(body: str):
            handle = tempfile.NamedTemporaryFile(
                "w", suffix=".md", delete=False, encoding="utf-8"
            )
            handle.write(
                "# T\n\nITWS version: 0.10.0-draft\nProfile: explanation\n\n"
                f"## Summary\n\n{body}\n"
            )
            handle.close()
            path = Path(handle.name)
            report = lint_path(spec(), path)
            path.unlink()
            return [f for f in report.findings if f.rule == "2.6.10"]

        self.assertEqual(lint("Moreover, the cache helps. The load falls."), [])
        self.assertTrue(lint("Moreover, the cache helps. Furthermore, load falls."))


if __name__ == "__main__":
    unittest.main()

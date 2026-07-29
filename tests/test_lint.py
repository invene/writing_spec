"""Lint coverage, severity, candidate handling, and the risk fixtures."""

from __future__ import annotations

import unittest

from tests.support import (
    BLOCKED,
    CONFORMING,
    VIOLATIONS,
    conforming_documents,
    spec,
)

from itws.document import parse_document
from itws.lint.engine import lint_path, run_lint
from itws.lint.model import Evidence
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
                self.assertGreater(len(report.checked_rules), 40)
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

    def test_a_stale_version_declaration_blocks_the_run(self) -> None:
        report = lint_path(spec(), BLOCKED / "stale-version.md")
        rules = {finding.rule for finding in violations(report)}
        self.assertIn("8.6.2", rules)
        self.assertIn("8.2.3", rules)

    def test_absent_evidence_reports_blocked_and_never_passes(self) -> None:
        report = lint_path(spec(), BLOCKED / "missing-evidence.md")
        self.assertTrue(report.blocked)
        for finding in report.blocked:
            self.assertEqual(finding.kind, "blocked")

    def test_a_partial_rule_reports_a_candidate_not_a_violation(self) -> None:
        report = lint_path(spec(), CONFORMING / "technical-report.md")
        for finding in report.findings:
            rule = spec().rule(finding.rule)
            if rule and rule.machine_checkable == "partial":
                self.assertIn(finding.kind, {"candidate", "blocked", "skipped"})


class TestNetworkSeparation(unittest.TestCase):
    def test_citation_checks_are_skipped_without_network(self) -> None:
        report = lint_path(spec(), CONFORMING / "research-paper.md", network=False)
        skipped = [f for f in report.findings if f.kind == "skipped"]
        self.assertTrue(any(f.rule == "5.4.3" for f in skipped))

    def test_a_skipped_check_is_not_a_pass(self) -> None:
        report = lint_path(spec(), CONFORMING / "research-paper.md", network=False)
        self.assertTrue(
            any(f.kind in {"skipped", "blocked"} for f in report.findings)
        )


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
        import tempfile
        from pathlib import Path

        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        )
        handle.write(
            "# T\n\nITWS version: 0.8.0-draft\nProfile: explanation\n"
            "Conformance tier: core\n\n## Summary\n\n"
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
        import tempfile
        from pathlib import Path

        def lint(body: str):
            handle = tempfile.NamedTemporaryFile(
                "w", suffix=".md", delete=False, encoding="utf-8"
            )
            handle.write(
                "# T\n\nITWS version: 0.8.0-draft\nProfile: explanation\n"
                f"Conformance tier: core\n\n## Summary\n\n{body}\n"
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

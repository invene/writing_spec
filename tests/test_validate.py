"""Binary machine validation with explicit lint coverage."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.support import BLOCKED, CONFORMING, SPEC_DIR, VIOLATIONS, conforming_documents, spec

from itws.validate import validate_document


class TestBinaryValidation(unittest.TestCase):
    def test_a_conforming_document_passes_without_assurance_inputs(self) -> None:
        report = validate_document(
            spec(),
            CONFORMING / "decision-record.md",
            spec_dir=SPEC_DIR,
            check_artifacts=False,
        )
        self.assertEqual(report.result, "pass", report.reasons)
        self.assertIsNotNone(report.lint)
        self.assertGreater(len(report.lint.fully_checked_rules), 0)

    def test_a_content_violation_fails(self) -> None:
        report = validate_document(
            spec(),
            VIOLATIONS / "term-before-definition.md",
            spec_dir=SPEC_DIR,
            check_artifacts=False,
        )
        self.assertEqual(report.result, "fail", report.reasons)
        rules = {finding.rule for finding in report.lint.errors}
        self.assertIn("2.3.1", rules)

    def test_a_stale_declared_version_fails(self) -> None:
        report = validate_document(
            spec(),
            BLOCKED / "stale-version.md",
            spec_dir=SPEC_DIR,
            check_artifacts=False,
        )
        self.assertEqual(report.result, "fail", report.reasons)
        rules = {finding.rule for finding in report.lint.errors}
        self.assertIn("8.2.3", rules)

    def test_an_obsolete_tier_line_is_a_structural_problem(self) -> None:
        source = (CONFORMING / "decision-record.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "with-tier.md"
            lines = source.splitlines()
            insert_at = next(
                i for i, line in enumerate(lines) if line.startswith("Profile:")
            )
            lines.insert(insert_at + 1, "Conformance tier: core")
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            report = validate_document(
                spec(), path, spec_dir=SPEC_DIR, check_artifacts=False
            )
        self.assertEqual(report.result, "fail", report.reasons)
        self.assertTrue(
            any("obsolete conformance-tier" in p for p in report.structural_problems),
            report.structural_problems,
        )

    def test_report_names_version_and_profile(self) -> None:
        report = validate_document(
            spec(),
            CONFORMING / "epic.md",
            spec_dir=SPEC_DIR,
            check_artifacts=False,
        )
        self.assertEqual(report.profile, "epic")
        self.assertEqual(report.itws_version, spec().version)

    def test_every_conforming_fixture_passes(self) -> None:
        for path in conforming_documents():
            report = validate_document(
                spec(),
                path,
                spec_dir=SPEC_DIR,
                check_artifacts=False,
            )
            with self.subTest(document=path.name):
                self.assertEqual(report.result, "pass", report.reasons)

    def test_candidates_surface_without_changing_pass_or_fail(self) -> None:
        """Partial rules may emit candidates; only error violations fail."""
        report = validate_document(
            spec(),
            CONFORMING / "technical-report.md",
            spec_dir=SPEC_DIR,
            check_artifacts=False,
        )
        partial_rules = {
            rule.number
            for rule in spec().rules
            if rule.machine_checkable == "partial"
        }
        candidate_rules = {finding.rule for finding in report.candidates}
        if candidate_rules & partial_rules:
            self.assertEqual(report.result, "pass", report.reasons)


class TestValidationReportShape(unittest.TestCase):
    def test_json_round_trip_fields(self) -> None:
        report = validate_document(
            spec(),
            CONFORMING / "task.md",
            spec_dir=SPEC_DIR,
            check_artifacts=False,
        )
        payload = report.to_json()
        for key in (
            "path",
            "itws_version",
            "profile",
            "result",
            "reasons",
            "structural_problems",
            "artifact_problems",
            "candidates",
            "unresolved_facts",
            "lint",
        ):
            self.assertIn(key, payload)
        self.assertNotIn("state", payload)
        self.assertNotIn("tier", payload)
        self.assertNotIn("human_gates", payload)


if __name__ == "__main__":
    unittest.main()

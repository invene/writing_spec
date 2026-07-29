"""Four-state validation and the separation of machine from human gates."""

from __future__ import annotations

import unittest

import tempfile
from pathlib import Path

from tests.support import BLOCKED, CONFORMING, SPEC_DIR, VIOLATIONS, spec

from itws.checklist import annex_revision, render
from itws.lint.model import Evidence
from itws.validate import validate_document

ANNEX_C = SPEC_DIR / "annexes" / "annex-c-rule-index.md"


def generated_checklist(profile: str, tier: str, directory: Path) -> tuple[Path, str]:
    """Generate a real checklist so the Part 8 evidence checks have an input."""
    revision = annex_revision(ANNEX_C.read_text(encoding="utf-8"), spec().version)
    text = render(
        spec(),
        profile=profile,
        tier=tier,
        generated_date="2026-07-29",
        index_revision=revision,
    )
    path = directory / f"{profile}-checklist.md"
    path.write_text(text, encoding="utf-8")
    return path, revision


def complete_evidence(profile: str, tier: str, directory: Path) -> Evidence:
    path, revision = generated_checklist(profile, tier, directory)
    return Evidence(
        self_check_recorded=True,
        owner_review_recorded=True,
        proxy_review_recorded=True,
        reader_test_recorded=True,
        checklist_path=path,
        checklist_annex_hash=revision,
        artifacts_current=True,
        lint_run_version=spec().version,
    )


class TestValidationStates(unittest.TestCase):
    def test_a_clean_document_without_recorded_gates_needs_review(self) -> None:
        """Rule 8.2.4: a clean machine run never closes a human gate."""
        report = validate_document(
            spec(),
            CONFORMING / "decision-record.md",
            spec_dir=SPEC_DIR,
            evidence=Evidence(artifacts_current=True),
        )
        self.assertEqual(report.state, "blocked")
        self.assertIn(
            "author self-check (§8.1.2)", report.human_gates
        )
        self.assertEqual(
            report.human_gates["author self-check (§8.1.2)"], "not recorded"
        )

    def test_a_clean_document_with_recorded_gates_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            report = validate_document(
                spec(),
                CONFORMING / "decision-record.md",
                spec_dir=SPEC_DIR,
                evidence=complete_evidence("decision-record", "core", Path(raw)),
            )
        self.assertEqual(report.state, "pass", report.reasons)

    def test_a_machine_clean_reviewed_document_still_needs_a_human_pass(self) -> None:
        """A reviewed tier adds two gates that no machine run can close."""
        partial = Evidence(
            self_check_recorded=True,
            owner_review_recorded=None,
            proxy_review_recorded=None,
            artifacts_current=True,
            lint_run_version=spec().version,
        )
        report = validate_document(
            spec(), CONFORMING / "procedure.md", spec_dir=SPEC_DIR, evidence=partial
        )
        self.assertNotEqual(report.state, "pass")
        self.assertEqual(
            report.human_gates["subject-matter-owner review (§8.4.2)"],
            "not recorded",
        )

    def test_a_content_violation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            report = validate_document(
                spec(),
                VIOLATIONS / "term-before-definition.md",
                spec_dir=SPEC_DIR,
                evidence=complete_evidence("decision-record", "core", Path(raw)),
            )
        self.assertEqual(report.state, "fail")

    def test_a_missing_input_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            report = validate_document(
                spec(),
                BLOCKED / "stale-version.md",
                spec_dir=SPEC_DIR,
                evidence=complete_evidence("decision-record", "core", Path(raw)),
            )
        self.assertIn(report.state, {"fail", "blocked"})

    def test_a_waiver_clears_its_own_rule_only(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            waived = complete_evidence("decision-record", "core", Path(raw))
            waived.waivers = ({"rule": "2.3.1"},)
            report = validate_document(
                spec(),
                VIOLATIONS / "term-before-definition.md",
                spec_dir=SPEC_DIR,
                evidence=waived,
            )
        self.assertNotEqual(report.state, "fail")

    def test_a_publication_tier_adds_the_reader_test_gate(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            evidence = complete_evidence(
                "research-paper", "publication", Path(raw)
            )
            evidence.reader_test_recorded = None
            report = validate_document(
                spec(),
                CONFORMING / "research-paper.md",
                spec_dir=SPEC_DIR,
                evidence=evidence,
            )
        self.assertIn(
            "independent reader test (§8.3.1)", report.human_gates
        )
        self.assertNotEqual(report.state, "pass")

    def test_every_conforming_fixture_passes_with_full_evidence(self) -> None:
        for path in sorted(CONFORMING.glob("*.md")):
            profile = path.stem
            tier = spec().profile(profile).minimum_tier
            with tempfile.TemporaryDirectory() as raw:
                report = validate_document(
                    spec(),
                    path,
                    spec_dir=SPEC_DIR,
                    evidence=complete_evidence(profile, tier, Path(raw)),
                    network=True,
                )
            with self.subTest(document=path.name):
                self.assertEqual(report.state, "pass", report.reasons)

    def test_report_names_the_declared_profile_and_tier(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            report = validate_document(
                spec(),
                CONFORMING / "epic.md",
                spec_dir=SPEC_DIR,
                evidence=complete_evidence("epic", "reviewed", Path(raw)),
            )
        self.assertEqual(report.profile, "epic")
        self.assertEqual(report.tier, "reviewed")


if __name__ == "__main__":
    unittest.main()

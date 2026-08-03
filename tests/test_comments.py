"""Tests for the hosted comment-set surface (§4.13, §8.7)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from itws.analysis import validate_comment_judgments
from itws.comments.adapter import PythonAdapter
from itws.comments.changeset import (
    CommentSetManifest,
    comment_scan_path,
    load_comment_set,
    structural_manifest,
)
from itws.comments.records import MARKER_GRAMMAR_RE
from itws.model import SourceSpan, content_hash
from itws.patch import detect_comment_collisions
from itws.validate import validate_comment_set
from tests.support import REPO_ROOT, spec as load_spec

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "comments"


def _load(relative: str):
    return load_comment_set(FIXTURES / relative / "carrier.json")


def _delta_manifest(base: str, proposed: str):
    """Build a manifest holding only the two extracted comment sets."""
    adapter = PythonAdapter()
    return CommentSetManifest(
        carrier_path="memory/carrier.json",
        declarations=None,
        declaration_problems=(),
        records=(),
        base_source=base,
        proposed_source=proposed,
        base_units=tuple(adapter.extract_comments(base, "host.py")),
        proposed_units=tuple(adapter.extract_comments(proposed, "host.py")),
    )


class TestCommentDeltas(unittest.TestCase):
    """§4.13: a change set compares occurrences, not sets of comment text."""

    def test_a_moved_comment_is_a_changed_unit(self) -> None:
        base = (
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def first():\n    return 1\n\n\n"
            "def second():\n    return 2\n"
        )
        proposed = (
            "def first():\n    return 1\n\n\n"
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def second():\n    return 2\n"
        )
        manifest = _delta_manifest(base, proposed)
        moved = manifest.moved_units()
        self.assertEqual(len(moved), 1)
        self.assertNotEqual(moved[0][0].span.start_line, moved[0][1].span.start_line)
        self.assertEqual(len(manifest.changed_units()), 1)
        self.assertEqual(manifest.removed_units(), ())

    def test_a_second_identical_marker_is_a_changed_unit(self) -> None:
        base = (
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def first():\n    return 1\n"
        )
        proposed = (
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def first():\n    return 1\n\n\n"
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def second():\n    return 2\n"
        )
        manifest = _delta_manifest(base, proposed)
        self.assertEqual(len(manifest.changed_units()), 1)
        self.assertEqual(manifest.removed_units(), ())

    def test_a_dropped_duplicate_is_a_removed_unit(self) -> None:
        base = (
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def first():\n    return 1\n\n\n"
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def second():\n    return 2\n"
        )
        proposed = (
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def first():\n    return 1\n\n\n"
            "def second():\n    return 2\n"
        )
        manifest = _delta_manifest(base, proposed)
        self.assertEqual(len(manifest.removed_units()), 1)
        self.assertEqual(manifest.changed_units(), ())

    def test_an_unchanged_set_reports_no_delta(self) -> None:
        source = (
            "# TODO(TASK-9): remove when the v2 endpoint lands\n"
            "def first():\n    return 1\n"
        )
        manifest = _delta_manifest(source, source)
        self.assertEqual(manifest.changed_units(), ())
        self.assertEqual(manifest.removed_units(), ())
        self.assertEqual(manifest.moved_units(), ())

    def test_a_moved_bare_marker_is_still_uncovered(self) -> None:
        """A move with no carrier record leaves the marker uncovered."""
        base = "# TODO: fix later\ndef first():\n    return 1\n"
        proposed = (
            "def first():\n    return 1\n\n\n"
            "# TODO: fix later\ndef second():\n    return 2\n"
        )
        manifest = _delta_manifest(base, proposed)
        self.assertEqual(len(manifest.uncovered_markers()), 1)


class TestPythonAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = PythonAdapter()

    def test_extracts_grouped_comments_with_stable_spans(self) -> None:
        source = (FIXTURES / "conforming" / "retry_proposed.py").read_text(
            encoding="utf-8"
        )
        units = self.adapter.extract_comments(source, "retry_proposed.py")
        included = [unit for unit in units if not unit.excluded]
        self.assertEqual(len(included), 2)
        marker = next(unit for unit in included if unit.is_marker)
        self.assertEqual(marker.span.end_line - marker.span.start_line, 1)
        self.assertTrue(marker.text.startswith("TODO(TASK-142):"))

    def test_docstrings_are_never_comment_units(self) -> None:
        source = 'def f():\n    """A docstring, not a comment."""\n    return 1\n'
        self.assertEqual(self.adapter.extract_comments(source, "f.py"), [])

    def test_directives_shebangs_and_banners_are_excluded(self) -> None:
        source = (FIXTURES / "excluded" / "excluded_host.py").read_text(
            encoding="utf-8"
        )
        units = self.adapter.extract_comments(source, "excluded_host.py")
        self.assertTrue(units)
        self.assertTrue(all(unit.excluded for unit in units))
        reasons = {unit.exclusion_reason for unit in units}
        self.assertIn("tool directive", reasons)

    def test_generated_files_are_excluded_whole(self) -> None:
        source = (FIXTURES / "excluded" / "generated_host.py").read_text(
            encoding="utf-8"
        )
        units = self.adapter.extract_comments(source, "generated_host.py")
        self.assertTrue(units)
        for unit in units:
            self.assertTrue(unit.excluded)
            self.assertIn("generated", unit.exclusion_reason)

    def test_anchor_resolves_to_the_following_function(self) -> None:
        source = (FIXTURES / "conforming" / "retry_proposed.py").read_text(
            encoding="utf-8"
        )
        anchor = self.adapter.resolve_anchor(
            source, "retry_proposed.py", SourceSpan("retry_proposed.py", 18, 19)
        )
        self.assertEqual(anchor.construct, "function totals_shim")
        self.assertTrue(anchor.anchor_hash.startswith("sha256:"))

    def test_anchor_resolves_to_the_containing_function(self) -> None:
        source = (FIXTURES / "conforming" / "retry_proposed.py").read_text(
            encoding="utf-8"
        )
        anchor = self.adapter.resolve_anchor(
            source, "retry_proposed.py", SourceSpan("retry_proposed.py", 14, 14)
        )
        self.assertEqual(anchor.construct, "function send_with_retry")


class TestMarkerGrammar(unittest.TestCase):
    def test_complete_marker_matches(self) -> None:
        match = MARKER_GRAMMAR_RE.match(
            "TODO(TASK-142): remove this shim when the v2 endpoint is live."
        )
        self.assertIsNotNone(match)
        self.assertEqual(match.group("reference"), "TASK-142")

    def test_bare_marker_does_not_match(self) -> None:
        self.assertIsNone(MARKER_GRAMMAR_RE.match("TODO: clean this up later."))
        self.assertIsNone(MARKER_GRAMMAR_RE.match("FIXME"))


class TestChangeSetExtraction(unittest.TestCase):
    def test_conforming_set_matches_and_covers(self) -> None:
        comment_set = _load("conforming")
        self.assertEqual(comment_set.problems, ())
        self.assertEqual(comment_set.declaration_problems, ())
        self.assertEqual(len(comment_set.changed_units()), 2)
        self.assertEqual(comment_set.uncovered_markers(), ())
        self.assertEqual(comment_set.unmatched_records(), ())
        self.assertEqual(comment_set.anchor_problems(), ())

    def test_records_carry_no_assurance_provenance_fields(self) -> None:
        comment_set = _load("conforming")
        for record in comment_set.records:
            payload = record.to_json()
            for key in (
                "provenance",
                "proposal",
                "disposition",
                "conformance_tier",
            ):
                self.assertNotIn(key, payload)

    def test_recorded_source_hash_mismatch_is_structural(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            carrier = FIXTURES / "conforming" / "carrier.json"
            payload = json.loads(carrier.read_text(encoding="utf-8"))
            for name in ("retry_base.py", "retry_proposed.py"):
                (directory / name).write_text(
                    (FIXTURES / "conforming" / name).read_text(encoding="utf-8")
                    + "\n# drift\n",
                    encoding="utf-8",
                )
            target = directory / "carrier.json"
            target.write_text(json.dumps(payload), encoding="utf-8")
            comment_set = load_comment_set(target)
            self.assertTrue(
                any("does not match" in problem for problem in comment_set.problems)
            )


class TestScanPath(unittest.TestCase):
    def test_scan_path_orders_id_anchor_comment(self) -> None:
        path = comment_scan_path(_load("conforming"))
        kinds = [segment["kind"] for segment in path["segments"]]
        self.assertEqual(
            kinds, ["change-set-id", "anchor", "comment", "anchor", "comment"]
        )
        self.assertEqual(path["problems"], [])
        self.assertEqual(path["segments"][0]["text"], "CS-2026-014")
        self.assertTrue(path["scan_path_hash"].startswith("sha256:"))

    def test_missing_anchor_is_reported(self) -> None:
        comment_set = _load("conforming")
        from dataclasses import replace

        records = (
            replace(
                comment_set.records[0],
                anchor=replace(comment_set.records[0].anchor, construct=""),
            ),
        ) + comment_set.records[1:]
        comment_set.records = records
        path = comment_scan_path(comment_set)
        self.assertTrue(
            any("no anchor" in problem for problem in path["problems"])
        )


class TestStructuralManifestView(unittest.TestCase):
    def test_units_are_paragraphs_at_host_spans(self) -> None:
        comment_set = _load("conforming")
        manifest = structural_manifest(comment_set)
        self.assertEqual(len(manifest.units), 2)
        for unit in manifest.units:
            self.assertEqual(unit.node_type, "paragraph")
            self.assertEqual(unit.span.path, "retry_proposed.py")
        self.assertIsNotNone(manifest.declarations)
        self.assertEqual(manifest.declarations.profile, "maintenance-comment")

    def test_marker_syntax_is_stripped_from_the_lint_view(self) -> None:
        comment_set = _load("conforming")
        manifest = structural_manifest(comment_set)
        texts = [unit.text for unit in manifest.units]
        self.assertTrue(any(text.startswith("remove this shim") for text in texts))
        self.assertFalse(any("TODO(" in text for text in texts))


class TestJudgmentsAndCollisions(unittest.TestCase):
    def test_carrier_judgments_validate(self) -> None:
        comment_set = _load("conforming")
        self.assertEqual(
            validate_comment_judgments(comment_set, known_rules=["4.13.1"]), []
        )

    def test_unknown_comment_id_and_missing_citation_are_reported(self) -> None:
        comment_set = _load("conforming")
        comment_set.judgments = (
            {"kind": "conflict", "value": "code disagrees", "span_ids": ["C-9"],
             "support": [], "state": "proposed"},
        )
        problems = validate_comment_judgments(comment_set, known_rules=["4.13.6"])
        self.assertTrue(any("unknown comment ID" in item for item in problems))
        comment_set.judgments = (
            {
                "kind": "conflict",
                "value": "code disagrees",
                "span_ids": ["C-1"],
                "support": ["9.9.9"],
                "state": "proposed",
            },
        )
        problems = validate_comment_judgments(comment_set, known_rules=["4.13.6"])
        self.assertTrue(
            any("neither a known rule ID" in item for item in problems)
        )

    def test_two_sets_writing_one_anchor_collide(self) -> None:
        left = _load("conforming")
        right = _load("blocked/pending-disposition")
        collisions = detect_comment_collisions([("a", left), ("b", right)])
        self.assertTrue(collisions)
        self.assertEqual(collisions[0].kind, "host-anchor")

    def test_disjoint_sets_do_not_collide(self) -> None:
        left = _load("conforming")
        self.assertEqual(detect_comment_collisions([("a", left)]), [])


class TestCommentValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = load_spec()

    def _validate(self, relative: str):
        return validate_comment_set(
            self.spec,
            FIXTURES / relative / "carrier.json",
            spec_dir=REPO_ROOT / "spec",
            check_artifacts=False,
        )

    def test_bare_marker_fails(self) -> None:
        report = self._validate("violations/bare-marker")
        self.assertEqual(report.result, "fail")
        rules = {finding.rule for finding in report.lint.errors}
        self.assertIn("4.13.8", rules)

    def test_unsupported_rationale_passes_machine_checks(self) -> None:
        """A recorded basis-none reason satisfies the partial basis checker."""
        report = self._validate("violations/unsupported-rationale")
        self.assertEqual(report.result, "pass", report.reasons)

    def test_stale_recorded_hash_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            carrier = FIXTURES / "violations/stale-proposal" / "carrier.json"
            payload = json.loads(carrier.read_text(encoding="utf-8"))
            payload["proposed_hash"] = "sha256:deadbeef"
            for name in ("retry_base.py", "retry_proposed.py"):
                (directory / name).write_text(
                    (FIXTURES / "violations/stale-proposal" / name).read_text(
                        encoding="utf-8"
                    ),
                    encoding="utf-8",
                )
            target = directory / "carrier.json"
            target.write_text(json.dumps(payload), encoding="utf-8")
            report = validate_comment_set(
                self.spec, target, spec_dir=REPO_ROOT / "spec", check_artifacts=False
            )
        self.assertEqual(report.result, "fail")
        self.assertTrue(
            any("does not match" in p for p in report.structural_problems),
            report.structural_problems,
        )

    def test_markdown_profile_carrier_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            carrier = FIXTURES / "conforming" / "carrier.json"
            payload = json.loads(carrier.read_text(encoding="utf-8"))
            payload["profile"] = "task"
            for name in ("retry_base.py", "retry_proposed.py"):
                (directory / name).write_text(
                    (FIXTURES / "conforming" / name).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            target = directory / "carrier.json"
            target.write_text(json.dumps(payload), encoding="utf-8")
            report = validate_comment_set(
                self.spec, target, spec_dir=REPO_ROOT / "spec",
                check_artifacts=False,
            )
        self.assertEqual(report.result, "fail")
        self.assertTrue(
            any("§0.2.1" in p for p in report.structural_problems),
            report.structural_problems,
        )


class TestSerialization(unittest.TestCase):
    def test_manifest_serializes_deterministically(self) -> None:
        left = _load("conforming").to_json()
        right = _load("conforming").to_json()
        self.assertEqual(json.dumps(left), json.dumps(right))
        self.assertEqual(left["declarations"]["change_set_id"], "CS-2026-014")

    def test_record_hashes_round_trip(self) -> None:
        comment_set = _load("conforming")
        for record in comment_set.records:
            self.assertEqual(record.text_hash, content_hash(record.text))


if __name__ == "__main__":
    unittest.main()

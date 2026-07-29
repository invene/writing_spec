"""Structural indexing, and the semantic boundary it must not cross."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.support import CONFORMING, VIOLATIONS, conforming_documents, spec

from itws.document import outline, parse_document, scan_path
from itws.vocab import CHUNK_TYPES


class TestStructuralIndex(unittest.TestCase):
    def test_declarations_are_read_from_every_conforming_fixture(self) -> None:
        for path in conforming_documents():
            manifest = parse_document(path)
            with self.subTest(document=path.name):
                self.assertIsNotNone(manifest.declarations)
                self.assertEqual(manifest.declaration_problems, ())
                self.assertEqual(
                    manifest.declarations.itws_version, spec().version
                )

    def test_span_ids_are_stable_across_two_parses(self) -> None:
        path = CONFORMING / "decision-record.md"
        first = [unit.id for unit in parse_document(path).units]
        second = [unit.id for unit in parse_document(path).units]
        self.assertEqual(first, second)
        self.assertEqual(len(first), len(set(first)))

    def test_source_spans_recover_the_original_text(self) -> None:
        path = CONFORMING / "incident.md"
        lines = path.read_text(encoding="utf-8").splitlines()
        manifest = parse_document(path)
        for unit in manifest.units:
            excerpt = "\n".join(
                lines[unit.span.start_line - 1 : unit.span.end_line]
            )
            self.assertEqual(excerpt, unit.text, unit.id)

    def test_node_types_are_syntactic_only(self) -> None:
        manifest = parse_document(CONFORMING / "procedure.md")
        kinds = {unit.node_type for unit in manifest.units}
        self.assertTrue(kinds <= {
            "heading",
            "paragraph",
            "list",
            "table",
            "code_fence",
            "block_quote",
            "thematic_break",
        })
        for kind in kinds:
            self.assertNotIn(kind, CHUNK_TYPES)

    def test_no_unit_carries_a_semantic_classification(self) -> None:
        """The structural parser must not emit a §4.1 purpose or a layer."""
        manifest = parse_document(CONFORMING / "technical-report.md")
        for unit in manifest.units:
            payload = unit.to_json()
            self.assertNotIn("chunk_type", payload)
            self.assertNotIn("layer", payload)
            self.assertNotIn("exact_items", payload)
            self.assertNotIn("claims", payload)

    def test_slot_links_appear_only_with_explicit_evidence(self) -> None:
        skeleton = spec().skeleton("technical-report")
        manifest = parse_document(
            CONFORMING / "technical-report.md", skeleton=skeleton
        )
        for unit in manifest.units:
            if unit.canonical_slot:
                self.assertIn(
                    unit.slot_evidence,
                    {"exact-name", "permitted-rename", "section-map"},
                )
            else:
                self.assertEqual(unit.slot_evidence, "")

    def test_previous_and_next_links_form_one_chain(self) -> None:
        manifest = parse_document(CONFORMING / "explanation.md")
        units = manifest.units
        self.assertEqual(units[0].previous_id, "")
        self.assertEqual(units[-1].next_id, "")
        for left, right in zip(units, units[1:]):
            self.assertEqual(left.next_id, right.id)
            self.assertEqual(right.previous_id, left.id)

    def test_outline_reports_headings_with_spans(self) -> None:
        skeleton = spec().skeleton("epic")
        rows = outline(parse_document(CONFORMING / "epic.md", skeleton=skeleton))
        self.assertTrue(rows)
        for row in rows:
            self.assertGreaterEqual(row["end_line"], row["start_line"])


class TestScanPath(unittest.TestCase):
    def _write(self, text: str) -> Path:
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        )
        handle.write(text)
        handle.close()
        return Path(handle.name)

    def test_scan_path_extracts_title_headings_and_opening_sentences(self) -> None:
        manifest = parse_document(CONFORMING / "decision-record.md")
        result = scan_path(manifest)
        self.assertEqual(result.problems, ())
        self.assertEqual(result.segments[0].kind, "title")
        self.assertEqual(result.segments[1].heading, "Status")
        self.assertEqual(
            result.segments[1].opening_sentence,
            "Accepted on 2026-06-14 by the platform pod.",
        )
        self.assertTrue(result.scan_path_hash.startswith("sha256:"))

    def test_scan_path_excludes_appendix_content(self) -> None:
        path = self._write(
            "# Queue design\n\n"
            "ITWS version: 0.8.0-draft\nProfile: design-rfc\n"
            "Conformance tier: reviewed\n\n"
            "## Summary\n\nThe proposal bounds concurrent writes.\n\n"
            "## Appendix A\n\nThe appendix gives formal details.\n\n"
            "### Semaphore proof\n\nThe proof uses invariant I.\n"
        )
        result = scan_path(parse_document(path))
        self.assertEqual(
            [segment.heading for segment in result.segments],
            ["Queue design", "Summary"],
        )
        path.unlink()

    def test_scan_path_reports_a_section_without_an_opening_chunk(self) -> None:
        path = self._write(
            "# Queue design\n\n"
            "ITWS version: 0.8.0-draft\nProfile: design-rfc\n"
            "Conformance tier: reviewed\n\n"
            "## Risks\n\n### Shared clock\n\n"
            "A shared clock failure can stop writes.\n"
        )
        result = scan_path(parse_document(path))
        self.assertTrue(any("Risks" in problem for problem in result.problems))
        path.unlink()

    def test_scan_extraction_does_not_claim_semantic_agreement(self) -> None:
        manifest = parse_document(VIOLATIONS / "scan-widened-status.md")
        result = scan_path(manifest)
        self.assertEqual(result.problems, ())
        self.assertEqual(result.segments[0].heading, "Approved region-proof queue design")
        self.assertIn("regional failures", result.segments[1].opening_sentence)


class TestDeclarationProblems(unittest.TestCase):
    def _write(self, text: str) -> Path:
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        )
        handle.write(text)
        handle.close()
        return Path(handle.name)

    def test_conflicting_declarations_are_reported(self) -> None:
        path = self._write(
            "# T\n\nITWS version: 0.8.0-draft\nProfile: epic\n"
            "Profile: task\nConformance tier: core\n"
        )
        manifest = parse_document(path)
        self.assertIsNone(manifest.declarations)
        self.assertTrue(
            any("conflicting" in p for p in manifest.declaration_problems)
        )
        path.unlink()

    def test_missing_declaration_is_reported(self) -> None:
        path = self._write("# T\n\nProfile: epic\n")
        manifest = parse_document(path)
        self.assertIsNone(manifest.declarations)
        self.assertIn(
            "missing declaration: itws_version", manifest.declaration_problems
        )
        path.unlink()


class TestSectionMap(unittest.TestCase):
    def _document(self, body: str) -> Path:
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        )
        handle.write(body)
        handle.close()
        return Path(handle.name)

    def test_a_section_map_links_a_heading_to_a_slot(self) -> None:
        path = self._document(
            "# T\n\nITWS version: 0.8.0-draft\nProfile: decision-record\n"
            "Conformance tier: core\n\n"
            "```itws-section-map\n"
            '"Why we did this" -> Context\n'
            "```\n\n"
            "## Why we did this\n\nBody.\n"
        )
        manifest = parse_document(path, skeleton=spec().skeleton("decision-record"))
        heading = next(
            unit
            for unit in manifest.units
            if unit.node_type == "heading" and unit.heading_path[-1] == "Why we did this"
        )
        self.assertEqual(heading.canonical_slot, "Context")
        self.assertEqual(heading.slot_evidence, "section-map")
        self.assertEqual(manifest.section_map_problems, ())
        path.unlink()

    def test_a_repeated_heading_or_slot_is_rejected(self) -> None:
        path = self._document(
            "# T\n\nITWS version: 0.8.0-draft\nProfile: decision-record\n"
            "Conformance tier: core\n\n"
            "```itws-section-map\n"
            '"A" -> Context\n'
            '"B" -> Context\n'
            "```\n"
        )
        manifest = parse_document(path, skeleton=spec().skeleton("decision-record"))
        self.assertTrue(
            any("repeats slot" in p for p in manifest.section_map_problems)
        )
        path.unlink()

    def test_a_cross_profile_slot_is_rejected(self) -> None:
        path = self._document(
            "# T\n\nITWS version: 0.8.0-draft\nProfile: decision-record\n"
            "Conformance tier: core\n\n"
            "```itws-section-map\n"
            '"A" -> Rollback\n'
            "```\n"
        )
        manifest = parse_document(path, skeleton=spec().skeleton("decision-record"))
        self.assertTrue(
            any("absent from the decision-record skeleton" in p
                for p in manifest.section_map_problems)
        )
        path.unlink()


if __name__ == "__main__":
    unittest.main()

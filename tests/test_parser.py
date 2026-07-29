"""Parsing, metadata validation, line ranges, and relation resolution."""

from __future__ import annotations

import unittest

from tests.support import SPEC_DIR, spec

from itws.model import GlossaryEntry, SourceSpan
from itws.parser import SpecError, parse_rules, validate_glossary_graph
from itws.vocab import (
    AUTHORED_RELATION_TYPES,
    CHUNK_TYPES,
    CONSTRUCTS,
    CONTEXT_SCOPES,
    LAYERS,
    PROFILE_IDS,
    RESOURCES,
    REWRITE_GUIDANCE,
    TARGETS,
)


class TestRuleParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = spec()

    def test_every_rule_has_navigation_metadata(self) -> None:
        for rule in self.spec.rules:
            with self.subTest(rule=rule.number):
                navigation = rule.navigation
                self.assertIn(navigation.target, TARGETS)
                self.assertIn(navigation.layers, LAYERS)
                self.assertIn(navigation.context_scope, CONTEXT_SCOPES)
                self.assertIn(navigation.rewrite_guidance, REWRITE_GUIDANCE)
                self.assertTrue(navigation.constructs)
                for value in navigation.constructs:
                    self.assertIn(value, CONSTRUCTS)
                for value in navigation.chunk_types:
                    self.assertIn(value, CHUNK_TYPES)
                for value in navigation.reads + navigation.writes:
                    self.assertIn(value, RESOURCES)

    def test_any_never_combines_with_a_specific_value(self) -> None:
        for rule in self.spec.rules:
            for field in (rule.navigation.constructs, rule.navigation.chunk_types):
                if "any" in field:
                    self.assertEqual(len(field), 1, rule.number)

    def test_rule_ids_are_unique_and_sorted(self) -> None:
        numbers = [rule.number for rule in self.spec.rules]
        self.assertEqual(len(numbers), len(set(numbers)))
        self.assertEqual(numbers, sorted(numbers, key=lambda n: [int(p) for p in n.split(".")]))

    def test_line_ranges_point_at_the_rule_header(self) -> None:
        for rule in self.spec.rules:
            path = SPEC_DIR.parent / rule.span.path
            lines = path.read_text(encoding="utf-8").splitlines()
            header = lines[rule.span.start_line - 1]
            self.assertTrue(
                header.startswith(f"#### Rule {rule.number} "),
                f"{rule.number}: span starts at {header!r}",
            )
            self.assertGreaterEqual(rule.span.end_line, rule.span.start_line)

    def test_relations_resolve_and_are_typed(self) -> None:
        known = {rule.number for rule in self.spec.rules}
        for rule in self.spec.rules:
            for relation in rule.relations:
                self.assertIn(relation.type, AUTHORED_RELATION_TYPES)
                self.assertIn(relation.target, known)
                self.assertNotEqual(relation.target, rule.number)

    def test_profile_metadata_is_in_registry_order(self) -> None:
        for rule in self.spec.rules:
            if not rule.profiles:
                continue
            expected = tuple(p for p in PROFILE_IDS if p in rule.profiles)
            self.assertEqual(rule.profiles, expected, rule.number)

    def test_every_active_rule_has_a_contrasting_pair(self) -> None:
        for rule in self.spec.rules:
            if rule.is_active:
                self.assertTrue(rule.example.compliant, rule.number)
                self.assertTrue(rule.example.non_compliant, rule.number)

    def test_precedence_layers_follow_section_one_four(self) -> None:
        for rule in self.spec.rules:
            if rule.part in {"5", "7"}:
                self.assertEqual(rule.precedence_layer, 1, rule.number)
            elif rule.part in {"4", "6"} and rule.precedence_layer != 2:
                self.assertEqual(rule.precedence_layer, 3, rule.number)


class TestSkeletonParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = spec()

    def test_every_profile_has_a_skeleton_with_required_slots(self) -> None:
        self.assertEqual(len(self.spec.skeletons), len(PROFILE_IDS))
        for skeleton in self.spec.skeletons:
            self.assertTrue(skeleton.slots, skeleton.profile)
            self.assertTrue(
                any(slot.required for slot in skeleton.slots), skeleton.profile
            )

    def test_renames_and_merges_name_existing_slots(self) -> None:
        for skeleton in self.spec.skeletons:
            names = {slot.name for slot in skeleton.slots}
            for merge in skeleton.merges:
                for part in merge.parts:
                    self.assertIn(part, names, skeleton.profile)

    def test_templated_slot_matches_a_concrete_heading(self) -> None:
        skeleton = self.spec.skeleton("investigation-log")
        self.assertEqual(
            skeleton.canonical_for_heading("Entry 2026-07-27 E-1"),
            "Entry <date> <id>",
        )
        self.assertIsNone(skeleton.canonical_for_heading("Entry"))

    def test_permitted_rename_resolves_and_others_do_not(self) -> None:
        skeleton = self.spec.skeleton("decision-record")
        self.assertEqual(skeleton.canonical_for_heading("Outcome"), "Decision")
        self.assertIsNone(skeleton.canonical_for_heading("What we picked"))

    def test_investigation_log_declares_an_append_only_policy(self) -> None:
        skeleton = self.spec.skeleton("investigation-log")
        policies = {policy.policy for policy in skeleton.mutation_policies}
        self.assertIn("append-only", policies)


class TestGlossaryGraph(unittest.TestCase):
    def test_prerequisites_resolve(self) -> None:
        known = {entry.term for entry in spec().glossary}
        for entry in spec().glossary:
            for prerequisite in entry.prerequisites:
                self.assertIn(prerequisite, known, entry.term)

    def test_a_cycle_is_rejected(self) -> None:
        span = SourceSpan("x.md", 1, 1)

        def entry(term: str, prerequisites: tuple[str, ...]) -> GlossaryEntry:
            return GlossaryEntry(
                term=term,
                part_of_speech="noun",
                status="admitted",
                definition="d",
                approved_example="e",
                do_not_use="",
                prerequisites=prerequisites,
                assumed_prerequisites=(),
                profiles=(),
                domain_tag="other",
                version="v0",
                span=span,
            )

        entries = [entry("alpha", ("beta",)), entry("beta", ("alpha",))]
        with self.assertRaises(SpecError):
            validate_glossary_graph(SPEC_DIR / "x.md", entries)


class TestPhraseLists(unittest.TestCase):
    def test_entries_exist_and_carry_their_rule(self) -> None:
        entries = spec().phrase_lists
        self.assertGreater(len(entries), 50)
        known = {rule.number for rule in spec().rules}
        for entry in entries:
            self.assertIn(entry.rule, known)
            self.assertIn(entry.kind, {"word", "phrase", "opener", "pattern"})
            self.assertTrue(entry.pattern)

    def test_entry_ids_are_unique(self) -> None:
        ids = [entry.id for entry in spec().phrase_lists]
        self.assertEqual(len(ids), len(set(ids)))


class TestStrictParsing(unittest.TestCase):
    def test_missing_navigation_metadata_fails(self) -> None:
        import tempfile
        import shutil

        with tempfile.TemporaryDirectory() as raw:
            from pathlib import Path

            target = Path(raw) / "spec"
            shutil.copytree(SPEC_DIR, target)
            path = target / "03-sentences.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                "**Navigation:** target: sentence · chunks: any · slots: any"
                " · layers: plain · context: local · rewrite: candidate\n",
                "",
                1,
            )
            path.write_text(text, encoding="utf-8")
            with self.assertRaises(SpecError):
                parse_rules(target, require_navigation=True)

    def test_unknown_construct_value_fails(self) -> None:
        import tempfile
        import shutil

        with tempfile.TemporaryDirectory() as raw:
            from pathlib import Path

            target = Path(raw) / "spec"
            shutil.copytree(SPEC_DIR, target)
            path = target / "03-sentences.md"
            text = path.read_text(encoding="utf-8")
            text = text.replace(
                "**Constructs:** hedge\n", "**Constructs:** vibes\n", 1
            )
            path.write_text(text, encoding="utf-8")
            with self.assertRaises(SpecError):
                parse_rules(target, require_navigation=True)


if __name__ == "__main__":
    unittest.main()

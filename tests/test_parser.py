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

    def test_every_profile_has_a_shallow_model_outcome(self) -> None:
        for profile in self.spec.profiles:
            self.assertTrue(profile.shallow_model_outcome, profile.id)

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


class TestReaderBaselinePolarity(unittest.TestCase):
    """Annex B records whether the reader is assumed to hold each item."""

    def setUp(self) -> None:
        self.spec = spec()

    def _texts(self, polarity: str) -> str:
        return "\n".join(
            item.text
            for item in self.spec.baseline
            if item.polarity == polarity
        )

    def test_both_polarities_are_present(self) -> None:
        assumed = [item for item in self.spec.baseline if item.is_assumed]
        excluded = [item for item in self.spec.baseline if not item.is_assumed]
        self.assertTrue(assumed)
        self.assertTrue(excluded)

    def test_section_b1_concepts_are_assumed(self) -> None:
        api = [
            item
            for item in self.spec.baseline
            if "application programming interfaces" in item.text
        ]
        self.assertTrue(api)
        for item in api:
            self.assertTrue(item.is_assumed)
            self.assertEqual(item.kind, "concept")

    def test_section_b3_names_are_not_assumed(self) -> None:
        """§B.3 lists these to say the reader does not know them."""
        for name in ("MMLU", "GSM8K", "SOTA", "SEV-1", "SQL"):
            with self.subTest(name=name):
                self.assertIn(name, self._texts("excluded"))
                self.assertNotIn(name, self._texts("assumed"))

    def test_non_baseline_notation_is_excluded(self) -> None:
        excluded = self._texts("excluded")
        assumed = self._texts("assumed")
        self.assertIn("Summation", excluded)
        self.assertIn("Arithmetic:", assumed)

    def test_every_profile_overlay_states_a_convention(self) -> None:
        for profile in self.spec.profiles:
            with self.subTest(profile=profile.id):
                assumed = [
                    item for item in profile.reader_overlay if item.is_assumed
                ]
                self.assertTrue(assumed, "overlay states no convention")

    def test_the_host_supplement_separates_grants_from_exclusions(self) -> None:
        overlay = self.spec.profile("maintenance-comment").reader_overlay
        grants = [item for item in overlay if item.conditional]
        exclusions = [item for item in overlay if not item.is_assumed]
        self.assertTrue(grants)
        self.assertTrue(exclusions)
        for item in grants:
            self.assertTrue(item.is_assumed)
            self.assertEqual(item.kind, "host-supplement")
        for item in exclusions:
            self.assertFalse(item.conditional)
        self.assertIn(
            "The author's intent",
            "\n".join(item.text for item in exclusions),
        )


class TestConstructScoping(unittest.TestCase):
    """§1.4 item 3: a rule is scoped to its trigger, never to what it demands."""

    #: Each rule requires the construct named beside it to exist, so none of
    #: them may be scoped to that construct.
    PRESENCE_RULES = {
        "6.2.1": "worked-example",
        "6.4.1": "diagram",
        "7.1.1": "limitation",
    }

    def test_a_presence_rule_is_not_scoped_to_what_it_requires(self) -> None:
        for number, demanded in self.PRESENCE_RULES.items():
            rule = spec().rule(number)
            with self.subTest(rule=number):
                self.assertIsNotNone(rule)
                self.assertNotIn(demanded, rule.navigation.constructs)

    def test_a_presence_rule_still_applies_to_a_document_lacking_it(self) -> None:
        """The rule must survive the document that violates it."""
        for number in self.PRESENCE_RULES:
            rule = spec().rule(number)
            constructs = set(rule.navigation.constructs)
            with self.subTest(rule=number):
                self.assertTrue(
                    "any" in constructs or constructs == {"comment"},
                    f"{number} is scoped to {sorted(constructs)}",
                )


class TestCrossSurfaceWording(unittest.TestCase):
    """§0.2.1: a rule enforced on both surfaces names the governed unit."""

    def _hosted_rules(self) -> set[str]:
        """Rule IDs the linter actually runs against a comment change set."""
        from pathlib import Path as _Path

        from itws.comments.changeset import load_comment_set, structural_manifest
        from itws.lint.engine import run_lint
        from tests.support import REPO_ROOT

        carrier = (
            REPO_ROOT / "tests" / "fixtures" / "comments" / "conforming"
            / "carrier.json"
        )
        comment_set = load_comment_set(carrier)
        report = run_lint(
            spec(),
            structural_manifest(comment_set),
            profile="maintenance-comment",
            comment_set=comment_set,
        )
        return set(report.checker_rules)

    def test_no_hosted_rule_is_bounded_to_a_markdown_document(self) -> None:
        offenders = [
            rule.number
            for rule in spec().rules
            if rule.number in self._hosted_rules()
            and "governed document" in rule.statement
        ]
        self.assertEqual(
            offenders,
            [],
            "these rules run against a comment change set but their "
            "statements name only a governed document",
        )

    def test_the_hosted_profile_has_boundary_locations(self) -> None:
        """Rule 7.1.1 is vacuous for a profile §7.1 never lists."""
        part7 = (SPEC_DIR / "07-limitations-caveats-interpretation.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`maintenance-comment` — **Boundaries**", part7)


if __name__ == "__main__":
    unittest.main()

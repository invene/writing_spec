"""Navigation operations, and the boundary they must not cross."""

from __future__ import annotations

import unittest

from tests.support import catalog

from itws.catalog import CatalogError, RuleTrail
from itws.vocab import PROFILE_IDS


class TestProfileEnvelope(unittest.TestCase):
    def test_envelope_holds_every_universal_rule(self) -> None:
        for profile in PROFILE_IDS:
            envelope = {rule["id"] for rule in catalog().envelope(profile)}
            for rule in catalog().rules.values():
                if rule["status"] != "active":
                    continue
                if rule["universal"]:
                    self.assertIn(rule["id"], envelope, f"{profile}/{rule['id']}")
                elif profile in rule["profiles"]:
                    self.assertIn(rule["id"], envelope, f"{profile}/{rule['id']}")
                else:
                    self.assertNotIn(rule["id"], envelope, f"{profile}/{rule['id']}")

    def test_a_facet_narrows_a_result_and_not_the_envelope(self) -> None:
        """A narrow beam must never shrink the applicable rule set.

        This is the §1.6.1 boundary: filtering is a search aid, and a style
        rule left out of the beam stays applicable to the document.
        """
        full = {rule["id"] for rule in catalog().envelope("design-rfc")}
        narrow = catalog().filter_rules(
            profile="design-rfc", target="symbol", rewrite_guidance="review"
        )
        self.assertLess(len(narrow), len(full))
        after = {rule["id"] for rule in catalog().envelope("design-rfc")}
        self.assertEqual(full, after)

        omitted = full - {rule["id"] for rule in narrow}
        self.assertIn("3.10.4", omitted)
        self.assertIn("3.10.4", after)

    def test_unknown_facet_value_is_rejected(self) -> None:
        with self.assertRaises(CatalogError):
            catalog().filter_rules(profile="design-rfc", layers="sideways")
        with self.assertRaises(CatalogError):
            catalog().filter_rules(profile="design-rfc", vibe="calm")


class TestSearchAndRelations(unittest.TestCase):
    def test_exact_rule_id_ranks_first(self) -> None:
        matches = catalog().search_rules("7.2.1", profile="incident")
        self.assertTrue(matches)
        self.assertEqual(matches[0].rule_id, "7.2.1")
        self.assertIn("exact rule ID", matches[0].reasons)

    def test_every_match_carries_reasons_and_a_raw_score(self) -> None:
        for match in catalog().search_rules("caveat", profile="incident"):
            self.assertTrue(match.reasons)
            self.assertGreater(match.score, 0)

    def test_search_is_confined_to_the_profile_envelope(self) -> None:
        matches = catalog().search_rules("subtask parent", profile="design-rfc")
        envelope = {rule["id"] for rule in catalog().envelope("design-rfc")}
        for match in matches:
            self.assertIn(match.rule_id, envelope)

    def test_relation_expansion_reaches_neighbours_at_each_depth(self) -> None:
        shallow = catalog().expand_relations(["5.1.1"], depth=1)
        deep = catalog().expand_relations(["5.1.1"], depth=2)
        shallow_ids = {item["rule_id"] for item in shallow["reached"]}
        deep_ids = {item["rule_id"] for item in deep["reached"]}
        self.assertIn("5.1.2", shallow_ids)
        self.assertTrue(shallow_ids <= deep_ids)
        self.assertGreater(len(deep_ids), len(shallow_ids))

    def test_relation_expansion_rejects_an_unknown_seed(self) -> None:
        with self.assertRaises(CatalogError):
            catalog().expand_relations(["9.9.9"])

    def test_relation_types_can_be_selected(self) -> None:
        only_requires = catalog().expand_relations(
            ["5.1.2"], depth=1, types=["requires"]
        )
        for edge in only_requires["edges"]:
            self.assertIn("requires", edge["type"])


class TestSupportingMaterial(unittest.TestCase):
    def test_glossary_chain_is_ordered_by_prerequisite(self) -> None:
        record = catalog().get_glossary_entry("transformer")
        chain = record["prerequisite_chain"]
        self.assertIn("model", chain)
        self.assertIn("attention", chain)
        self.assertLess(chain.index("model"), chain.index("attention"))

    def test_examples_resolve_by_rule_and_profile(self) -> None:
        by_rule = catalog().get_examples(rule="7.2.1", origin="annex-d")
        self.assertTrue(by_rule)
        by_profile = catalog().get_examples(profile="procedure", origin="annex-d")
        self.assertGreaterEqual(len(by_profile), 2)

    def test_section_lookup_returns_source_locations(self) -> None:
        section = catalog().get_section("7.2")
        self.assertEqual(section["rule_count"], 2)
        self.assertTrue(section["source_files"])

    def test_context_packet_always_references_the_full_envelope(self) -> None:
        packet = catalog().assemble_context(
            profile="incident", rules=["7.2.1"], terms=["service"]
        )
        self.assertEqual(len(packet["selected_rules"]), 1)
        self.assertEqual(
            packet["envelope_reference"]["rule_count"],
            catalog().get_profile("incident")["envelope"]["rule_count"],
        )


class TestRuleTrail(unittest.TestCase):
    def test_a_trail_records_requests_and_selections(self) -> None:
        trail = RuleTrail()
        trail.record("search_rules", {"query": "caveat"}, ["7.2.1"], note="seed")
        trail.record("expand_relations", {"seeds": ["7.2.1"]}, ["7.2.2"])
        lines = trail.to_jsonl().strip().splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("7.2.1", lines[0])


if __name__ == "__main__":
    unittest.main()

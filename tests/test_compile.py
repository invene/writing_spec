"""Deterministic generation, manifest coverage, and envelope agreement."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.support import REPO_ROOT, SPEC_DIR, catalog, spec

from itws import SCHEMA_VERSION
from itws.compile import (
    GENERATED_DIRNAME,
    build_artifacts,
    build_manifest,
    check_envelope_agreement,
    check_registered_checkers,
    compile_all,
)
from itws.model import content_hash
from itws.vocab import PROFILE_IDS


class TestDeterministicGeneration(unittest.TestCase):
    def test_two_builds_produce_identical_bytes(self) -> None:
        first = {a.relative_path: a.text for a in build_artifacts(spec())}
        second = {a.relative_path: a.text for a in build_artifacts(spec())}
        self.assertEqual(first, second)

    def test_committed_artifacts_match_a_fresh_build(self) -> None:
        _artifacts, problems = compile_all(SPEC_DIR, check_only=True)
        self.assertEqual(problems, [])

    def test_manifest_covers_every_artifact_and_source(self) -> None:
        artifacts = build_artifacts(spec())
        manifest = json.loads(build_manifest(spec(), artifacts).text)
        self.assertEqual(manifest["schema_version"], SCHEMA_VERSION)
        self.assertEqual(manifest["itws_version"], spec().version)
        for artifact in artifacts:
            self.assertIn(artifact.relative_path, manifest["artifact_hashes"])
            self.assertEqual(
                manifest["artifact_hashes"][artifact.relative_path], artifact.hash
            )
        for path in sorted(SPEC_DIR.rglob("*.md")):
            if "generated" in path.parts:
                continue
            key = path.relative_to(SPEC_DIR.parent).as_posix()
            self.assertIn(key, manifest["source_hashes"])
            self.assertEqual(
                manifest["source_hashes"][key],
                content_hash(path.read_text(encoding="utf-8")),
            )

    def test_committed_manifest_hashes_match_the_files_on_disk(self) -> None:
        root = SPEC_DIR / GENERATED_DIRNAME
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        for relative, expected in manifest["artifact_hashes"].items():
            path = root / relative
            self.assertTrue(path.exists(), relative)
            self.assertEqual(
                content_hash(path.read_text(encoding="utf-8")), expected, relative
            )


class TestArtifactContent(unittest.TestCase):
    def test_every_rule_appears_exactly_once(self) -> None:
        ids = [rule["id"] for rule in catalog().rules.values()]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {rule.number for rule in spec().rules})

    def test_profile_envelope_agrees_with_checklist_filtering(self) -> None:
        self.assertEqual(check_envelope_agreement(spec()), [])

    def test_every_machine_checkable_rule_has_a_checker(self) -> None:
        self.assertEqual(check_registered_checkers(spec()), [])

    def test_every_profile_has_a_manifest_and_a_skeleton(self) -> None:
        for profile in PROFILE_IDS:
            record = catalog().get_profile(profile)
            self.assertEqual(record["id"], profile)
            self.assertGreater(record["envelope"]["rule_count"], 0)
            skeleton = catalog().get_skeleton(profile)
            self.assertTrue(skeleton["required_slots"])

    def test_rule_graph_carries_precedence_and_examples(self) -> None:
        graph = catalog().rule_graph
        self.assertEqual(len(graph["precedence_layers"]), 6)
        self.assertEqual(len(graph["rule_precedence"]), len(catalog().rules))
        kinds = {edge["type"] for edge in graph["edges"]}
        self.assertIn("exemplified-by", kinds)
        self.assertIn("requires", kinds)

    def test_annex_d_examples_reach_the_milestone(self) -> None:
        annex_d = [e for e in catalog().examples if e["origin"] == "annex-d"]
        self.assertGreaterEqual(len(annex_d), 22)
        for profile in PROFILE_IDS:
            count = sum(1 for e in annex_d if e["profile"] == profile)
            self.assertGreaterEqual(count, 2, profile)

    def test_every_annex_d_example_cites_permanent_rule_ids(self) -> None:
        for example in catalog().examples:
            if example["origin"] != "annex-d":
                continue
            self.assertTrue(example["rules_applied"], example["id"])
            for number in example["rules_applied"]:
                self.assertIn(number, catalog().rules, example["id"])


class TestCatalogLoadsFromCleanCheckout(unittest.TestCase):
    def test_from_repo_needs_no_installation(self) -> None:
        loaded = catalog()
        self.assertEqual(loaded.version, spec().version)
        self.assertTrue(loaded.glossary)
        self.assertTrue(loaded.phrase_lists)


if __name__ == "__main__":
    unittest.main()

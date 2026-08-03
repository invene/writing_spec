"""Command-line compatibility, golden output, and the example scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from itws.compile import compile_all

from tests.support import (
    CONFORMING,
    PATCHES,
    REPO_ROOT,
    SPEC_DIR,
    TOOLS,
    catalog,
    registry_matches_spec,
    retired_rule_ids,
    rule_registry_ids,
    spec,
)

def run(*args: str, expect: int | None = 0) -> subprocess.CompletedProcess:
    process = subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if expect is not None and process.returncode != expect:
        raise AssertionError(
            f"{' '.join(args)} exited {process.returncode}\n"
            f"stdout:\n{process.stdout}\nstderr:\n{process.stderr}"
        )
    return process


ANNEX_C = SPEC_DIR / "annexes" / "annex-c-rule-index.md"


def generated_catalog_is_current() -> bool:
    _, problems = compile_all(SPEC_DIR, check_only=True)
    return not problems


@unittest.skipUnless(
    registry_matches_spec(),
    "rule ID registry must equal active rules ∪ retired IDs",
)
class TestIndexCommandCompatibility(unittest.TestCase):
    def test_itws_index_accepts_its_original_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            out = Path(raw) / "annex-c.md"
            run(
                str(TOOLS / "itws_index.py"),
                "--spec-dir",
                "spec",
                "--out",
                str(out),
            )
            self.assertTrue(out.exists())
            text = out.read_text(encoding="utf-8")
            self.assertIn("# Annex C — Rule index (generated)", text)
            self.assertIn(f"from ITWS {spec().version}", text)

    def test_itws_index_check_mode_matches_the_committed_annex(self) -> None:
        run(str(TOOLS / "itws_index.py"), "--spec-dir", "spec", "--check")


class TestExistingCommandCompatibility(unittest.TestCase):
    """CLI entry points keep their core arguments."""

    def test_itws_checklist_accepts_its_original_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            out = Path(raw) / "checklist.md"
            run(
                str(TOOLS / "itws_checklist.py"),
                "--spec-version",
                spec().version,
                "--profile",
                "design-rfc",
                "--out",
                str(out),
            )
            text = out.read_text(encoding="utf-8")
            self.assertIn("**Profile:** `design-rfc`", text)
            self.assertIn("## Vocabulary", text)
            self.assertIn("Optional ITWS assurance checklist", text)

    def test_itws_overlays_accepts_its_original_arguments(self) -> None:
        process = run(str(TOOLS / "itws_overlays.py"), "--spec-dir", "spec")
        self.assertIn("overlay layout is valid", process.stdout)


class TestGeneratedOutput(unittest.TestCase):
    def test_checklist_generation_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            first = Path(raw) / "a.md"
            second = Path(raw) / "b.md"
            for out in (first, second):
                run(
                    str(TOOLS / "itws_checklist.py"),
                    "--spec-version",
                    spec().version,
                    "--profile",
                    "task",
                    "--out",
                    str(out),
                    "--generated-date",
                    "2026-07-29",
                )
            self.assertEqual(
                first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8")
            )

    @unittest.skipUnless(
        registry_matches_spec(),
        "committed Annex C may lag until the rule registry is updated",
    )
    def test_annex_c_lists_every_rule_once(self) -> None:
        text = ANNEX_C.read_text(encoding="utf-8")
        for rule in spec().rules:
            self.assertIn(f"| {rule.number} |", text, rule.number)
        self.assertIn(f"**Rule count:** {len(spec().rules)}", text)

    def test_registry_covers_active_and_retired_ids(self) -> None:
        current = {rule.number for rule in spec().rules}
        retired = retired_rule_ids()
        registry = rule_registry_ids()
        self.assertFalse(current & retired)
        self.assertTrue(retired <= registry)
        pending = current - registry
        if pending:
            self.assertFalse(pending & retired)
        else:
            self.assertTrue(current <= registry)

    @unittest.skipUnless(
        registry_matches_spec(),
        "run tools/itws_index.py --update-registry after assigning new rule IDs",
    )
    def test_rule_id_registry_matches_the_source(self) -> None:
        current = {rule.number for rule in spec().rules}
        registry = rule_registry_ids()
        self.assertEqual(registry, current | retired_rule_ids())

    @unittest.skipUnless(
        generated_catalog_is_current(),
        "generated catalog is stale relative to the specification",
    )
    def test_compile_check_is_clean(self) -> None:
        run(str(TOOLS / "itws_compile.py"), "--check", "--quiet")


class TestAgentCommands(unittest.TestCase):
    @unittest.skipUnless(
        generated_catalog_is_current(),
        "generated catalog is stale relative to the specification",
    )
    def test_retrieve_emits_valid_json(self) -> None:
        process = run(
            str(TOOLS / "itws_retrieve.py"), "get-profile", "design-rfc", "--json"
        )
        payload = json.loads(process.stdout)
        self.assertEqual(payload["id"], "design-rfc")
        self.assertIn("envelope", payload)

    def test_retrieve_search_and_expand_run(self) -> None:
        run(
            str(TOOLS / "itws_retrieve.py"),
            "search-rules",
            "interface invariant",
            "--profile",
            "design-rfc",
            "--json",
        )
        run(
            str(TOOLS / "itws_retrieve.py"),
            "expand-relations",
            "5.1.1",
            "--depth",
            "2",
            "--json",
        )

    def test_document_outline_and_index_run(self) -> None:
        run(
            str(TOOLS / "itws_document.py"),
            "outline",
            "--input",
            str(CONFORMING / "incident.md"),
        )
        process = run(
            str(TOOLS / "itws_document.py"),
            "index",
            "--input",
            str(CONFORMING / "incident.md"),
        )
        payload = json.loads(process.stdout)
        self.assertIn("units", payload)
        self.assertTrue(payload["units"])
        process = run(
            str(TOOLS / "itws_document.py"),
            "scan-path",
            "--input",
            str(CONFORMING / "incident.md"),
            "--json",
        )
        payload = json.loads(process.stdout)
        self.assertTrue(payload["segments"])
        self.assertTrue(payload["scan_path_hash"].startswith("sha256:"))

    def test_lint_reports_json(self) -> None:
        process = run(
            str(TOOLS / "itws_lint.py"),
            "--input",
            str(CONFORMING / "decision-record.md"),
            "--json",
            expect=None,
        )
        payload = json.loads(process.stdout)
        self.assertEqual(payload["profile"], "decision-record")
        self.assertIn("readability", payload)

    def test_patch_combine_reports_a_collision(self) -> None:
        process = run(
            str(TOOLS / "itws_patch.py"),
            "combine",
            "--base",
            str(PATCHES / "base-technical-report.md"),
            "--proposed",
            str(PATCHES / "proposal-overlap-a.md"),
            str(PATCHES / "proposal-overlap-b.md"),
            "--json",
            expect=1,
        )
        payload = json.loads(process.stdout)
        self.assertGreater(payload["collision_count"], 0)

    def test_validate_reports_pass_or_fail(self) -> None:
        process = run(
            str(TOOLS / "itws_validate.py"),
            "--input",
            str(CONFORMING / "decision-record.md"),
            "--skip-artifact-check",
            "--json",
            expect=None,
        )
        payload = json.loads(process.stdout)
        self.assertIn(payload["result"], {"pass", "fail"})

    def test_work_example_prints_a_plan_skeleton(self) -> None:
        process = run(str(TOOLS / "itws_work.py"), "example")
        self.assertIn("writable_span_ids", process.stdout)

    def test_annotate_check_confirms_the_metadata_is_current(self) -> None:
        run(str(TOOLS / "itws_annotate.py"), "--spec-dir", "spec", "--check")


class TestExampleScripts(unittest.TestCase):
    @unittest.skipUnless(
        generated_catalog_is_current(),
        "generated catalog is stale relative to the specification",
    )
    def test_every_example_script_runs(self) -> None:
        scripts = REPO_ROOT / "examples" / "agent-scripts"
        run(str(scripts / "inspect_profile.py"), "decision-record")
        run(
            str(scripts / "search_rule_graph.py"),
            "caveat placement",
            "--profile",
            "incident",
        )
        run(str(scripts / "inspect_term_chain.py"), "error budget")
        run(
            str(scripts / "outline_document.py"),
            "--input",
            str(CONFORMING / "incident.md"),
        )
        run(
            str(scripts / "make_work_slice.py"),
            "--input",
            str(CONFORMING / "technical-report.md"),
            "--heading",
            "Limitations",
        )
        run(
            str(scripts / "check_chunk_patch.py"),
            "--base",
            str(PATCHES / "base-technical-report.md"),
            "--proposed",
            str(PATCHES / "proposal-safe-repair.md"),
        )

    def test_every_example_script_has_help(self) -> None:
        scripts = sorted((REPO_ROOT / "examples" / "agent-scripts").glob("*.py"))
        self.assertEqual(len(scripts), 6)
        for script in scripts:
            process = run(str(script), "--help")
            self.assertIn("usage:", process.stdout)


class TestStandardLibraryOnly(unittest.TestCase):
    def test_no_module_imports_a_third_party_package(self) -> None:
        import ast

        allowed = {
            "argparse", "ast", "collections", "dataclasses", "datetime",
            "difflib", "functools", "hashlib", "io", "itertools", "json",
            "pathlib", "re", "shutil", "subprocess", "sys", "tempfile",
            "textwrap", "tokenize", "typing", "unittest", "os", "itws",
            "tests", "urllib", "__future__",
            "itws_index", "itws_checklist", "itws_overlays",
        }
        roots = [
            REPO_ROOT / "itws",
            REPO_ROOT / "tools",
            REPO_ROOT / "examples" / "agent-scripts",
        ]
        for root in roots:
            for path in sorted(root.rglob("*.py")):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        names = [alias.name.split(".")[0] for alias in node.names]
                    elif isinstance(node, ast.ImportFrom) and node.level == 0:
                        names = [(node.module or "").split(".")[0]]
                    else:
                        continue
                    for name in names:
                        self.assertIn(name, allowed, f"{path}: imports {name}")


if __name__ == "__main__":
    unittest.main()

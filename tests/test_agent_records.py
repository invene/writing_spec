"""Optional agent analysis records, work plans, and patch guards."""

from __future__ import annotations

import unittest

from tests.support import CONFORMING, PATCHES, catalog, spec

from itws.analysis import (
    AgentAnalysis,
    LedgerEntry,
    OpenQuestion,
    contradictions,
    validate_analysis,
)
from itws.document import parse_document
from itws.patch import changed_ranges, detect_collisions, inspect
from itws.work import (
    DependencyNote,
    ExecutionWave,
    PreservationNote,
    ResourceClaim,
    WorkPlan,
    WorkSlice,
    check_mutation_policies,
    detect_cycles,
    detect_write_conflicts,
    validate_plan,
)


def manifest_for(name: str, profile: str):
    return parse_document(CONFORMING / name, skeleton=spec().skeleton(profile))


class TestAgentAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = manifest_for("technical-report.md", "technical-report")
        self.analysis = AgentAnalysis(
            document_path=self.manifest.path,
            document_hash=self.manifest.document_hash,
            profile="technical-report",
        )
        self.known = {rule.number for rule in spec().rules}
        self.body = [
            unit for unit in self.manifest.units if unit.node_type == "paragraph"
        ]

    def test_a_cited_judgment_validates(self) -> None:
        self.analysis.classify([self.body[0].id], "evidence", ["7.3.1", "§4.1"])
        self.assertEqual(
            validate_analysis(self.analysis, self.manifest, known_rules=self.known), []
        )

    def test_a_judgment_without_a_citation_is_rejected(self) -> None:
        self.analysis.classify([self.body[0].id], "evidence", [])
        problems = validate_analysis(
            self.analysis, self.manifest, known_rules=self.known
        )
        self.assertTrue(any("cites no rule" in p for p in problems))

    def test_a_judgment_without_a_span_is_rejected(self) -> None:
        self.analysis.classify([], "claim", ["5.6.1"])
        problems = validate_analysis(
            self.analysis, self.manifest, known_rules=self.known
        )
        self.assertTrue(any("names no source span" in p for p in problems))

    def test_an_unknown_span_or_chunk_type_is_rejected(self) -> None:
        self.analysis.classify(["u99999-deadbeef"], "evidence", ["7.3.1"])
        self.analysis.classify([self.body[0].id], "vibe", ["7.3.1"])
        problems = validate_analysis(
            self.analysis, self.manifest, known_rules=self.known
        )
        self.assertTrue(any("unknown span ID" in p for p in problems))
        self.assertTrue(any("unknown §4.1 chunk type" in p for p in problems))

    def test_an_agent_can_revise_a_classification_after_further_search(self) -> None:
        """The earlier reading survives as `disputed`, not as a deletion."""
        first = self.analysis.classify([self.body[0].id], "claim", ["5.6.1"])
        second = self.analysis.revise(first, "evidence", ["7.3.1", "§4.1"])
        self.assertEqual(first.state, "disputed")
        self.assertEqual(second.state, "proposed")
        self.assertEqual(second.value, "evidence")
        self.assertEqual(
            validate_analysis(self.analysis, self.manifest, known_rules=self.known), []
        )

    def test_two_accepted_readings_of_one_span_are_a_contradiction(self) -> None:
        span = self.body[0].id
        self.analysis.classify([span], "claim", ["5.6.1"], state="accepted_for_run")
        self.analysis.classify([span], "evidence", ["7.3.1"], state="accepted_for_run")
        self.assertTrue(contradictions(self.analysis))

    def test_two_proposed_readings_are_not_a_contradiction(self) -> None:
        span = self.body[0].id
        self.analysis.classify([span], "claim", ["5.6.1"])
        self.analysis.classify([span], "evidence", ["7.3.1"])
        self.assertEqual(contradictions(self.analysis), [])

    def test_an_unresolved_question_records_a_gap_instead_of_a_guess(self) -> None:
        self.analysis.open_questions.append(
            OpenQuestion(
                question="what was the baseline completion time?",
                span_ids=[self.body[0].id],
                state="blocked",
                blocks=("5.4.1",),
            )
        )
        self.assertEqual(
            validate_analysis(self.analysis, self.manifest, known_rules=self.known), []
        )

    def test_a_ledger_entry_carries_its_support(self) -> None:
        self.analysis.ledger.append(
            LedgerEntry(
                ledger="term-ledger",
                key="scheduler",
                span_ids=(self.body[0].id,),
                support=("2.3.1",),
            )
        )
        self.assertEqual(
            validate_analysis(self.analysis, self.manifest, known_rules=self.known), []
        )


class TestWorkPlan(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = manifest_for("technical-report.md", "technical-report")
        self.units = [
            unit for unit in self.manifest.units if unit.node_type == "paragraph"
        ]

    def _plan(self, slices, dependencies=(), waves=()) -> WorkPlan:
        return WorkPlan(
            document_path=self.manifest.path,
            document_hash=self.manifest.document_hash,
            profile="technical-report",
            slices=list(slices),
            dependencies=list(dependencies),
            waves=list(waves),
        )

    def _slice(self, name: str, index: int, writes: str = "chunk-text") -> WorkSlice:
        return WorkSlice(
            id=name,
            writable_span_ids=(self.units[index].id,),
            rules=("5.4.1",),
            preservation=(
                PreservationNote(
                    span_ids=(self.units[index].id,),
                    what="every measured value",
                    support=("5.1.1",),
                ),
            ),
            claims=(ResourceClaim(resource=writes, mode="write"),),
        )

    def test_a_valid_plan_reports_no_problem(self) -> None:
        plan = self._plan([self._slice("s1", 0)])
        self.assertEqual(validate_plan(plan, self.manifest, catalog()), [])

    def test_an_unknown_span_or_rule_is_rejected(self) -> None:
        plan = self._plan(
            [WorkSlice(id="s1", writable_span_ids=("u404-nope",), rules=("9.9.9",))]
        )
        problems = validate_plan(plan, self.manifest, catalog())
        self.assertTrue(any("unknown span ID" in p for p in problems))
        self.assertTrue(any("unknown rule ID" in p for p in problems))

    def test_a_stale_document_hash_is_rejected(self) -> None:
        plan = self._plan([self._slice("s1", 0)])
        plan.document_hash = "sha256:0000"
        problems = validate_plan(plan, self.manifest, catalog())
        self.assertTrue(any("different document version" in p for p in problems))

    def test_a_dependency_cycle_is_reported_with_its_edges(self) -> None:
        plan = self._plan(
            [self._slice("s1", 0), self._slice("s2", 1)],
            [
                DependencyNote("s1", "s2", "evidence-before-interpretation", ("7.3.1",)),
                DependencyNote("s2", "s1", "definition-before-use", ("2.3.1",)),
            ],
        )
        cycles = detect_cycles(plan)
        self.assertTrue(cycles)
        self.assertIn("s1", cycles[0])
        self.assertIn("s2", cycles[0])

    def test_two_slices_writing_one_ledger_collide_unless_ordered(self) -> None:
        left = WorkSlice(
            id="s1",
            writable_span_ids=(self.units[0].id,),
            claims=(ResourceClaim(resource="term-ledger", mode="write"),),
        )
        right = WorkSlice(
            id="s2",
            writable_span_ids=(self.units[1].id,),
            claims=(ResourceClaim(resource="term-ledger", mode="write"),),
        )
        plan = self._plan([left, right])
        self.assertTrue(detect_write_conflicts(plan))

        plan.dependencies.append(
            DependencyNote("s1", "s2", "definition-before-use", ("2.3.1",))
        )
        self.assertEqual(detect_write_conflicts(plan), [])

    def test_a_parallel_wave_with_a_shared_write_is_rejected(self) -> None:
        plan = self._plan(
            [self._slice("s1", 0), self._slice("s2", 1)],
            waves=[ExecutionWave(index=1, slice_ids=("s1", "s2"))],
        )
        problems = validate_plan(plan, self.manifest, catalog())
        self.assertTrue(any("both write chunk-text" in p for p in problems))

    def test_wave_order_must_respect_a_declared_dependency(self) -> None:
        plan = self._plan(
            [self._slice("s1", 0), self._slice("s2", 1, writes="heading")],
            [DependencyNote("s1", "s2", "skeleton-slot-order", ("4.4.1",))],
            [
                ExecutionWave(index=1, slice_ids=("s2",)),
                ExecutionWave(index=2, slice_ids=("s1",)),
            ],
        )
        problems = validate_plan(plan, self.manifest, catalog())
        self.assertTrue(any("wave order violates dependency" in p for p in problems))

    def test_an_append_only_slot_blocks_a_writable_span(self) -> None:
        manifest = manifest_for("investigation-log.md", "investigation-log")
        skeleton = spec().skeleton("investigation-log")
        entry_units = [
            unit
            for unit in manifest.units
            if unit.node_type == "paragraph"
            and any(part.startswith("Entry ") for part in unit.heading_path)
        ]
        self.assertTrue(entry_units)
        plan = WorkPlan(
            document_path=manifest.path,
            document_hash=manifest.document_hash,
            profile="investigation-log",
            slices=[WorkSlice(id="s1", writable_span_ids=(entry_units[0].id,))],
        )
        problems = check_mutation_policies(
            plan, manifest, skeleton.mutation_policies
        )
        self.assertTrue(any("append-only" in p for p in problems))


class TestPatchGuards(unittest.TestCase):
    def setUp(self) -> None:
        self.base = PATCHES / "base-technical-report.md"
        self.manifest = parse_document(
            self.base, skeleton=spec().skeleton("technical-report")
        )

    def test_a_safe_repair_reports_its_changed_span(self) -> None:
        report = inspect(
            self.base, PATCHES / "proposal-safe-repair.md", manifest=self.manifest
        )
        self.assertEqual(len(report.changes), 1)
        self.assertTrue(report.affected_span_ids)
        self.assertTrue(report.safe_to_apply)

    def test_an_edit_outside_the_declared_spans_is_reported(self) -> None:
        allowed = WorkSlice(
            id="s1", writable_span_ids=(self.manifest.units[0].id,)
        )
        report = inspect(
            self.base,
            PATCHES / "proposal-safe-repair.md",
            manifest=self.manifest,
            work_slice=allowed,
        )
        self.assertTrue(report.outside_slice)
        self.assertFalse(report.safe_to_apply)

    def test_a_stale_source_hash_is_detected(self) -> None:
        expected = {unit.id: unit.source_hash for unit in self.manifest.units}
        target = self.manifest.units[3].id
        expected[target] = "sha256:stale"
        report = inspect(
            self.base,
            PATCHES / "proposal-safe-repair.md",
            manifest=self.manifest,
            expected_hashes=expected,
        )
        self.assertIn(target, report.stale_spans)
        self.assertFalse(report.safe_to_apply)

    def test_two_proposals_on_one_span_collide(self) -> None:
        left = inspect(
            self.base, PATCHES / "proposal-overlap-a.md", manifest=self.manifest
        )
        right = inspect(
            self.base, PATCHES / "proposal-overlap-b.md", manifest=self.manifest
        )
        collisions = detect_collisions([("a", left), ("b", right)])
        self.assertTrue(collisions)
        self.assertEqual(collisions[0].kind, "span")

    def test_collision_detection_is_order_independent(self) -> None:
        left = inspect(
            self.base, PATCHES / "proposal-rename-a.md", manifest=self.manifest
        )
        right = inspect(
            self.base, PATCHES / "proposal-rename-b.md", manifest=self.manifest
        )
        forward = detect_collisions([("a", left), ("b", right)])
        backward = detect_collisions([("b", right), ("a", left)])
        self.assertEqual(
            [c.to_json() for c in forward], [c.to_json() for c in backward]
        )

    def test_two_names_for_one_artifact_collide(self) -> None:
        left = inspect(
            self.base, PATCHES / "proposal-rename-a.md", manifest=self.manifest
        )
        right = inspect(
            self.base, PATCHES / "proposal-rename-b.md", manifest=self.manifest
        )
        slices = {
            "a": WorkSlice(
                id="a",
                writable_span_ids=tuple(left.affected_span_ids),
                claims=(ResourceClaim(resource="term-ledger", mode="write"),),
            ),
            "b": WorkSlice(
                id="b",
                writable_span_ids=tuple(right.affected_span_ids),
                claims=(ResourceClaim(resource="term-ledger", mode="write"),),
            ),
        }
        collisions = detect_collisions([("a", left), ("b", right)], slices=slices)
        self.assertTrue(any(c.kind == "resource" for c in collisions))

    def test_a_widened_claim_is_mechanically_safe_and_still_needs_a_reader(self) -> None:
        """Rule 5.1.1 is `prohibited`: no tool decides that this patch is wrong."""
        report = inspect(
            self.base, PATCHES / "proposal-widened-claim.md", manifest=self.manifest
        )
        self.assertTrue(report.safe_to_apply)
        rule = spec().rule("5.1.1")
        self.assertEqual(rule.navigation.rewrite_guidance, "prohibited")

    def test_changed_ranges_are_empty_for_an_identical_document(self) -> None:
        text = self.base.read_text(encoding="utf-8")
        self.assertEqual(changed_ranges(text, text), [])


if __name__ == "__main__":
    unittest.main()

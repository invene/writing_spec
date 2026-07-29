#!/usr/bin/env python3
"""Check an agent-authored work plan and render one context packet.

The records are optional scaffolds. An agent may use them, ignore them, or
build its own. What this tool does is mechanical: it validates identifiers,
spans, hashes, dependency endpoints, resource claims, and execution waves,
and it reports a cycle or a write collision without resolving either.

``validate``  check one plan against a document and the catalog.
``packet``    render one work slice as a compact context packet.
``example``   print a small plan skeleton to copy and edit.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.analysis import AgentAnalysis
from itws.catalog import Catalog, CatalogError
from itws.document import parse_document
from itws.jsonio import dumps
from itws.parser import SpecError, parse_specification
from itws.work import (
    COMMON_DEPENDENCIES,
    DependencyNote,
    ExecutionWave,
    PreservationNote,
    ResourceClaim,
    WorkPlan,
    WorkSlice,
    check_mutation_policies,
    context_packet,
    detect_cycles,
    validate_plan,
)

EXAMPLE_PLAN = {
    "document_path": "<document>.md",
    "document_hash": "<from itws_document.py index>",
    "profile": "design-rfc",
    "slices": [
        {
            "id": "s1",
            "writable_span_ids": ["<span id>"],
            "context_span_ids": ["<span id>"],
            "rules": ["7.2.1"],
            "sections": ["7.2"],
            "terms": [],
            "examples": ["D.7"],
            "intent": "attach the caveat to the claim it qualifies",
            "preservation": [
                {
                    "span_ids": ["<span id>"],
                    "what": "the measured endpoints and their units",
                    "support": ["5.1.1", "5.4.1"],
                }
            ],
            "resource_claims": [
                {"resource": "chunk-text", "mode": "write", "detail": ""},
                {"resource": "claim-ledger", "mode": "read", "detail": ""},
            ],
            "prohibited": ["do not widen the claim beyond its tested workload"],
            "blocker_policy": "report and stop",
        }
    ],
    "dependencies": [
        {
            "before": "s1",
            "after": "s2",
            "kind": "evidence-before-interpretation",
            "support": ["7.3.1"],
            "state": "proposed",
        }
    ],
    "waves": [{"index": 1, "slice_ids": ["s1"]}, {"index": 2, "slice_ids": ["s2"]}],
}


def parse_args() -> argparse.Namespace:
    # Shared options are declared on a parent parser so they work both before
    # and after the action name.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", type=Path, default=Path("."))
    common.add_argument("--spec-dir", type=Path, default=Path("spec"))
    common.add_argument("--json", action="store_true")

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
    )
    actions = parser.add_subparsers(dest="action", required=True)

    validate = actions.add_parser("validate", help="check one plan", parents=[common])
    validate.add_argument("--plan", type=Path, required=True)
    validate.add_argument("--document", type=Path, required=True)
    validate.add_argument("--analysis", type=Path)

    packet = actions.add_parser(
        "packet", help="render one slice as a packet", parents=[common]
    )
    packet.add_argument("--plan", type=Path, required=True)
    packet.add_argument("--document", type=Path, required=True)
    packet.add_argument("--slice", dest="slice_id", required=True)
    packet.add_argument("--analysis", type=Path)

    actions.add_parser("example", help="print a plan skeleton", parents=[common])
    return parser.parse_args()


def load_plan(path: Path) -> WorkPlan:
    payload = json.loads(path.read_text(encoding="utf-8"))
    plan = WorkPlan(
        document_path=payload["document_path"],
        document_hash=payload["document_hash"],
        profile=payload["profile"],
    )
    for item in payload.get("slices", ()):
        plan.slices.append(
            WorkSlice(
                id=item["id"],
                writable_span_ids=tuple(item.get("writable_span_ids", ())),
                context_span_ids=tuple(item.get("context_span_ids", ())),
                rules=tuple(item.get("rules", ())),
                sections=tuple(item.get("sections", ())),
                terms=tuple(item.get("terms", ())),
                examples=tuple(item.get("examples", ())),
                intent=item.get("intent", ""),
                preservation=tuple(
                    PreservationNote(
                        span_ids=tuple(note.get("span_ids", ())),
                        what=note.get("what", ""),
                        support=tuple(note.get("support", ())),
                    )
                    for note in item.get("preservation", ())
                ),
                claims=tuple(
                    ResourceClaim(
                        resource=claim["resource"],
                        mode=claim["mode"],
                        detail=claim.get("detail", ""),
                    )
                    for claim in item.get("resource_claims", ())
                ),
                prohibited=tuple(item.get("prohibited", ())),
                blocker_policy=item.get("blocker_policy", "report and stop"),
            )
        )
    for item in payload.get("dependencies", ()):
        plan.dependencies.append(
            DependencyNote(
                before=item["before"],
                after=item["after"],
                kind=item.get("kind", "unspecified"),
                support=tuple(item.get("support", ())),
                state=item.get("state", "proposed"),
            )
        )
    for item in payload.get("waves", ()):
        plan.waves.append(
            ExecutionWave(index=item["index"], slice_ids=tuple(item["slice_ids"]))
        )
    return plan


def main() -> int:
    args = parse_args()
    if args.action == "example":
        print(dumps(EXAMPLE_PLAN))
        print("Common dependency kinds:")
        for kind in COMMON_DEPENDENCIES:
            print(f"  {kind}")
        print(
            "\nThe list is a prompt, not a closed vocabulary. Cite the rule that "
            "justifies each dependency you declare."
        )
        return 0

    try:
        spec = parse_specification(args.spec_dir)
        catalog = Catalog.from_repo(args.repo)
    except (SpecError, CatalogError) as error:
        print(error, file=sys.stderr)
        return 2

    plan = load_plan(args.plan)
    skeleton = spec.skeleton(plan.profile)
    manifest = parse_document(args.document, skeleton=skeleton)

    analysis_json = None
    if args.analysis:
        analysis_json = json.loads(args.analysis.read_text(encoding="utf-8"))

    if args.action == "packet":
        work_slice = plan.slice(args.slice_id)
        if work_slice is None:
            print(f"unknown work slice: {args.slice_id}", file=sys.stderr)
            return 2
        packet = context_packet(
            plan, work_slice, manifest, catalog, analysis_json=analysis_json
        )
        print(dumps(packet))
        return 0

    problems = validate_plan(plan, manifest, catalog)
    if skeleton:
        problems.extend(
            check_mutation_policies(plan, manifest, skeleton.mutation_policies)
        )
    cycles = detect_cycles(plan)
    for cycle in cycles:
        problems.append("dependency cycle: " + " -> ".join(cycle))

    if args.json:
        print(
            dumps(
                {
                    "plan": args.plan.as_posix(),
                    "document": args.document.as_posix(),
                    "problem_count": len(problems),
                    "problems": problems,
                    "cycles": cycles,
                    "note": (
                        "a cycle and a collision are reported, never resolved; "
                        "choosing an edge is a reading of the document"
                    ),
                }
            )
        )
    else:
        for problem in problems:
            print(problem)
        print(f"\n{len(problems)} problem(s) in {args.plan}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

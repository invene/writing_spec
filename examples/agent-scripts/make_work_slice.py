#!/usr/bin/env python3
"""Build one work slice from spans, rules, context, and preservation notes.

Everything this script decides is a placeholder for your reasoning: which
spans are writable, which rules apply, and what the rewrite must preserve.
The script shows the shape and runs the mechanical checks.

    python3 examples/agent-scripts/make_work_slice.py \\
        --input <document>.md --heading Limitations
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from itws.catalog import Catalog
from itws.document import parse_document
from itws.jsonio import dumps
from itws.parser import parse_specification
from itws.work import (
    PreservationNote,
    ResourceClaim,
    WorkPlan,
    WorkSlice,
    check_mutation_policies,
    context_packet,
    validate_plan,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--heading", required=True, help="section to rewrite")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--packet", action="store_true", help="print the packet")
    args = parser.parse_args()

    spec = parse_specification(args.repo / "spec")
    catalog = Catalog.from_repo(args.repo)
    declared = parse_document(args.input).declarations
    if declared is None:
        print("the document declares no profile", file=sys.stderr)
        return 2
    skeleton = spec.skeleton(declared.profile)
    manifest = parse_document(args.input, skeleton=skeleton)

    # 1. Choose the spans. Here: every unit under one heading.
    headings = [unit for unit in manifest.units if unit.node_type == "heading"]
    target = next(
        (
            unit
            for unit in headings
            if unit.heading_path
            and unit.heading_path[-1].casefold() == args.heading.casefold()
        ),
        None,
    )
    if target is None:
        print(f"no heading named {args.heading!r}", file=sys.stderr)
        print(
            "available: "
            + ", ".join(unit.heading_path[-1] for unit in headings),
            file=sys.stderr,
        )
        return 2
    position = headings.index(target)
    end = (
        headings[position + 1].span.start_line - 1
        if position + 1 < len(headings)
        else manifest.line_count
    )
    body = [
        unit
        for unit in manifest.units_in_range(target.span.start_line, end)
        if unit.node_type != "heading"
    ]

    # 2. Choose the rules. Replace this search with your own selection; the
    #    whole envelope stays applicable either way.
    matches = catalog.search_rules(
        f"{args.heading} boundary limitation caveat",
        profile=declared.profile,
        limit=4,
    )

    # 3. State what the rewrite must not change, and cite the rule that says so.
    preservation = PreservationNote(
        span_ids=tuple(unit.id for unit in body),
        what="every measured value, unit, and stated scope",
        support=("5.1.1", "5.4.1"),
    )

    work_slice = WorkSlice(
        id="s1",
        writable_span_ids=tuple(unit.id for unit in body),
        context_span_ids=(target.id,),
        rules=tuple(match.rule_id for match in matches),
        sections=(),
        intent=f"tighten the {args.heading} section without widening any claim",
        preservation=(preservation,),
        claims=(
            ResourceClaim(resource="chunk-text", mode="write"),
            ResourceClaim(resource="claim-ledger", mode="read"),
        ),
        prohibited=("do not add a limitation the evidence does not support",),
    )

    plan = WorkPlan(
        document_path=manifest.path,
        document_hash=manifest.document_hash,
        profile=declared.profile,
        slices=[work_slice],
    )

    problems = validate_plan(plan, manifest, catalog)
    if skeleton:
        problems.extend(
            check_mutation_policies(plan, manifest, skeleton.mutation_policies)
        )

    print(f"slice s1 covers {len(work_slice.writable_span_ids)} writable span(s)")
    print(f"rules in the beam: {', '.join(work_slice.rules) or 'none'}")
    for rule_id in work_slice.rules:
        rule = catalog.get_rule(rule_id)
        print(f"  {rule_id}: rewrite {rule['navigation']['rewrite_guidance']}")
    print(f"validation problems: {len(problems)}")
    for problem in problems:
        print(f"  {problem}")

    if args.packet:
        print(dumps(context_packet(plan, work_slice, manifest, catalog)))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

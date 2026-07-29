#!/usr/bin/env python3
"""Guard a proposed rewrite without choosing it.

``check``    compares a base document with a proposal and reports changed
             ranges, affected spans, stale hashes, and edits outside a
             declared work slice.
``combine``  reports every collision among several proposals (Rule 8.6.5).
``diff``     prints the unified diff for a reader.

The tool never applies a patch, resolves a collision, or judges whether a
rewrite preserves exact meaning. Rule 5.1.1 leaves that to a reader.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.document import parse_document
from itws.jsonio import dumps
from itws.parser import SpecError, parse_specification
from itws.patch import detect_collisions, inspect, unified_diff
from itws.work import ResourceClaim, WorkSlice


def parse_args() -> argparse.Namespace:
    # Shared options are declared on a parent parser so they work both before
    # and after the action name.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--spec-dir", type=Path, default=Path("spec"))
    common.add_argument("--json", action="store_true")

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
    )
    actions = parser.add_subparsers(dest="action", required=True)

    check = actions.add_parser(
        "check", help="inspect one proposed rewrite", parents=[common]
    )
    check.add_argument("--base", type=Path, required=True)
    check.add_argument("--proposed", type=Path, required=True)
    check.add_argument("--slice", type=Path, help="a work-slice JSON file")
    check.add_argument(
        "--expected-hashes",
        type=Path,
        help="JSON mapping span IDs to the hashes the proposal was written against",
    )

    combine = actions.add_parser(
        "combine", help="report collisions among proposals", parents=[common]
    )
    combine.add_argument("--base", type=Path, required=True)
    combine.add_argument("--proposed", type=Path, nargs="+", required=True)
    combine.add_argument("--slices", type=Path, nargs="*", default=[])

    diff = actions.add_parser(
        "diff", help="print a unified diff", parents=[common]
    )
    diff.add_argument("--base", type=Path, required=True)
    diff.add_argument("--proposed", type=Path, required=True)

    return parser.parse_args()


def _load_slice(path: Path) -> WorkSlice:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return WorkSlice(
        id=payload["id"],
        writable_span_ids=tuple(payload.get("writable_span_ids", ())),
        context_span_ids=tuple(payload.get("context_span_ids", ())),
        rules=tuple(payload.get("rules", ())),
        intent=payload.get("intent", ""),
        claims=tuple(
            ResourceClaim(
                resource=claim["resource"],
                mode=claim["mode"],
                detail=claim.get("detail", ""),
            )
            for claim in payload.get("resource_claims", ())
        ),
        prohibited=tuple(payload.get("prohibited", ())),
    )


def _manifest(base: Path, spec_dir: Path):
    provisional = parse_document(base)
    skeleton = None
    if provisional.declarations:
        try:
            spec = parse_specification(spec_dir)
            skeleton = spec.skeleton(provisional.declarations.profile)
        except SpecError:
            skeleton = None
    return parse_document(base, skeleton=skeleton)


def main() -> int:
    args = parse_args()

    if args.action == "diff":
        print(unified_diff(args.base, args.proposed), end="")
        return 0

    manifest = _manifest(args.base, args.spec_dir)

    if args.action == "check":
        work_slice = _load_slice(args.slice) if args.slice else None
        expected = (
            json.loads(args.expected_hashes.read_text(encoding="utf-8"))
            if args.expected_hashes
            else {}
        )
        report = inspect(
            args.base,
            args.proposed,
            manifest=manifest,
            work_slice=work_slice,
            expected_hashes=expected,
        )
        if args.json:
            print(dumps(report.to_json()))
        else:
            print(f"base     : {report.base_path} ({report.base_hash})")
            print(f"proposed : {args.proposed} ({report.proposed_hash})")
            print(f"changes  : {len(report.changes)}")
            for change in report.changes:
                print(
                    f"  {change.operation:7} base lines "
                    f"{change.base_start}-{change.base_end}"
                )
            print(f"affected spans: {', '.join(report.affected_span_ids) or 'none'}")
            if report.stale_spans:
                print("stale spans  : " + ", ".join(report.stale_spans))
            if report.outside_slice:
                print("outside slice: " + ", ".join(report.outside_slice))
            for problem in report.problems:
                print(f"problem: {problem}")
            print(
                "safe to apply: "
                + ("yes (mechanically; meaning still needs a reader)"
                   if report.safe_to_apply else "no")
            )
        return 0 if report.safe_to_apply else 1

    reports = [
        (path.name, inspect(args.base, path, manifest=manifest))
        for path in args.proposed
    ]
    slices = {}
    for path in args.slices:
        loaded = _load_slice(path)
        slices[path.name] = loaded
    collisions = detect_collisions(reports, slices=slices)
    if args.json:
        print(
            dumps(
                {
                    "base": args.base.as_posix(),
                    "proposals": [name for name, _ in reports],
                    "collision_count": len(collisions),
                    "collisions": [item.to_json() for item in collisions],
                    "note": (
                        "collisions are reported, not resolved; Rule 8.6.5 leaves "
                        "the choice to a reader"
                    ),
                }
            )
        )
    else:
        if not collisions:
            print(f"no collision among {len(reports)} proposal(s)")
        for collision in collisions:
            print(
                f"{collision.kind}: {collision.left} vs {collision.right} — "
                f"{collision.detail}"
            )
    return 1 if collisions else 0


if __name__ == "__main__":
    raise SystemExit(main())

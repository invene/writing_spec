#!/usr/bin/env python3
"""Check a proposed edit against source hashes and allowed spans.

The check is mechanical. A patch that passes is still an unreviewed patch:
whether the rewrite preserves exact meaning is your judgment, and Rule 5.1.1
does not let a tool make it.

    python3 examples/agent-scripts/check_chunk_patch.py \\
        --base <document>.md --proposed <rewritten>.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from itws.document import parse_document
from itws.parser import parse_specification
from itws.patch import inspect
from itws.work import WorkSlice


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--proposed", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument(
        "--allow",
        nargs="*",
        default=[],
        help="span IDs the rewrite may change; omit to allow every span",
    )
    args = parser.parse_args()

    spec = parse_specification(args.repo / "spec")
    declared = parse_document(args.base).declarations
    skeleton = spec.skeleton(declared.profile) if declared else None
    manifest = parse_document(args.base, skeleton=skeleton)

    # Record the hashes the proposal was written against. In a real run you
    # captured these before the rewrite started, not after.
    expected = {unit.id: unit.source_hash for unit in manifest.units}

    work_slice = (
        WorkSlice(id="s1", writable_span_ids=tuple(args.allow))
        if args.allow
        else None
    )
    report = inspect(
        args.base,
        args.proposed,
        manifest=manifest,
        work_slice=work_slice,
        expected_hashes=expected,
    )

    print(f"changed ranges: {len(report.changes)}")
    for change in report.changes:
        print(f"  {change.operation} base {change.base_start}-{change.base_end}")
        if change.base_text:
            print(f"    - {change.base_text.splitlines()[0][:90]}")
        if change.proposed_text:
            print(f"    + {change.proposed_text.splitlines()[0][:90]}")

    print(f"affected spans: {', '.join(report.affected_span_ids) or 'none'}")
    if report.stale_spans:
        print("stale spans (source changed since the hash was taken):")
        for span_id in report.stale_spans:
            print(f"  {span_id}")
    if report.outside_slice:
        print("edits outside the allowed spans:")
        for span_id in report.outside_slice:
            print(f"  {span_id}")
    for problem in report.problems:
        print(f"problem: {problem}")

    if report.safe_to_apply:
        print(
            "\nMechanically safe. Read the changed text and confirm that it "
            "preserves every exact item before you apply it."
        )
        return 0
    print("\nNot safe to apply as written.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

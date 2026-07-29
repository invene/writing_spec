#!/usr/bin/env python3
"""Index, scan, lint, and validate one comment change set.

The change set is declared by a JSON carrier (§0.2.1). Actions:

  index      extract and match the governed comments; print the manifest
  scan-path  print the Rule 4.13.9 scan path
  lint       run the §4.13, §8.7, and shared text checks
  stale      report every recorded hash that no longer matches its source
  validate   report one §8.6.2 state: pass, fail, needs_review, or blocked

Supply recorded human gates with ``--evidence <file.json>``, exactly as
``tools/itws_validate.py`` does for a Markdown document.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.comments.changeset import (
    comment_scan_path,
    load_comment_set,
    structural_manifest,
)
from itws.jsonio import dumps
from itws.lint.engine import run_lint
from itws.lint.model import Evidence
from itws.model import content_hash
from itws.parser import SpecError, parse_specification
from itws.validate import validate_comment_set

load_evidence = Evidence.from_json_file

EXIT_CODES = {"pass": 0, "needs_review": 0, "fail": 1, "blocked": 2}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "action", choices=("index", "scan-path", "lint", "stale", "validate")
    )
    parser.add_argument("--carrier", type=Path, required=True)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--network", action="store_true")
    parser.add_argument(
        "--skip-artifact-check",
        action="store_true",
        help="do not recompile the catalog to confirm it is current",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def _stale_report(comment_set) -> dict[str, object]:
    entries: list[dict[str, str]] = []
    declarations = comment_set.declarations
    if declarations is not None:
        for attribute, source in (
            ("base", comment_set.base_source),
            ("proposed", comment_set.proposed_source),
        ):
            recorded = getattr(declarations, f"{attribute}_hash")
            if source and recorded and recorded != content_hash(source):
                entries.append(
                    {
                        "kind": f"{attribute}-source",
                        "subject": getattr(declarations, f"{attribute}_path"),
                        "detail": "the recorded hash no longer matches",
                    }
                )
    for record, message in comment_set.unmatched_records():
        entries.append(
            {"kind": "comment", "subject": record.comment_id, "detail": message}
        )
    for record, message in comment_set.stale_proposals():
        entries.append(
            {"kind": "proposal", "subject": record.comment_id, "detail": message}
        )
    for record, message in comment_set.anchor_problems():
        entries.append(
            {"kind": "anchor", "subject": record.comment_id, "detail": message}
        )
    return {"carrier_path": comment_set.carrier_path, "stale": entries}


def main() -> int:
    args = parse_args()
    if not args.carrier.is_file():
        print(f"no such carrier: {args.carrier}", file=sys.stderr)
        return 2

    if args.action == "validate":
        try:
            spec = parse_specification(args.spec_dir)
        except SpecError as error:
            print(f"specification defect: {error}", file=sys.stderr)
            return 2
        report = validate_comment_set(
            spec,
            args.carrier,
            spec_dir=args.spec_dir,
            evidence=load_evidence(args.evidence),
            network=args.network,
            check_artifacts=not args.skip_artifact_check,
        )
        if args.json:
            print(dumps(report.to_json()))
        else:
            print(f"carrier : {report.path}")
            print(f"version : {report.itws_version}")
            print(f"profile : {report.profile or '(undeclared)'}")
            print(f"tier    : {report.tier}")
            print(f"state   : {report.state}")
            for reason in report.reasons:
                print(f"  - {reason}")
            if report.human_gates:
                print("human gates:")
                for name, state in report.human_gates.items():
                    print(f"  {name}: {state}")
        return EXIT_CODES[report.state]

    comment_set = load_comment_set(args.carrier)

    if args.action == "index":
        print(dumps(comment_set.to_json()))
        return 2 if comment_set.problems else 0

    if args.action == "scan-path":
        path = comment_scan_path(comment_set)
        if args.json:
            print(dumps(path))
        else:
            for segment in path["segments"]:
                print(f"{segment['kind']:>14}: {segment['text']}")
            for problem in path["problems"]:
                print(f"       problem: {problem}")
        return 1 if path["problems"] else 0

    if args.action == "stale":
        report = _stale_report(comment_set)
        print(dumps(report))
        return 1 if report["stale"] else 0

    # action == "lint"
    try:
        spec = parse_specification(args.spec_dir)
    except SpecError as error:
        print(f"specification defect: {error}", file=sys.stderr)
        return 2
    declarations = comment_set.declarations
    profile = declarations.profile if declarations else "maintenance-comment"
    tier = declarations.tier if declarations and declarations.tier else "core"
    lint = run_lint(
        spec,
        structural_manifest(comment_set),
        profile=profile or "maintenance-comment",
        tier=tier,
        evidence=load_evidence(args.evidence),
        network=args.network,
        comment_set=comment_set,
    )
    if args.json:
        print(dumps(lint.to_json()))
    else:
        for finding in lint.findings:
            print(
                f"{finding.path}:{finding.start_line}: "
                f"[{finding.severity}/{finding.kind}] {finding.message}"
            )
        print(
            f"{len(lint.findings)} finding(s), {len(lint.errors)} error(s), "
            f"{len(lint.blocked)} blocked"
        )
    return 1 if lint.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate one governed document and report one of four states.

The states are `pass`, `fail`, `needs_review`, and `blocked` (§8.6.2). A
clean machine run never closes a human gate, and a skipped required check
never reports as a pass.

Supply recorded human gates with ``--evidence <file.json>``. The file may set
``self_check_recorded``, ``owner_review_recorded``, ``proxy_review_recorded``,
``reader_test_recorded``, ``checklist_path``, ``checklist_annex_hash``, and a
``waivers`` list of ``{"rule": "<id>", ...}`` objects.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.jsonio import dumps
from itws.lint.model import Evidence
from itws.parser import SpecError, parse_specification
from itws.validate import validate_document
from itws.vocab import PROFILE_IDS, TIERS

EXIT_CODES = {"pass": 0, "needs_review": 0, "fail": 1, "blocked": 2}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument("--profile", choices=PROFILE_IDS)
    parser.add_argument("--tier", choices=TIERS)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--network", action="store_true")
    parser.add_argument(
        "--skip-artifact-check",
        action="store_true",
        help="do not recompile the catalog to confirm it is current",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero unless the state is `pass`",
    )
    return parser.parse_args()


def load_evidence(path: Path | None) -> Evidence:
    if path is None:
        return Evidence()
    payload = json.loads(path.read_text(encoding="utf-8"))
    checklist = payload.get("checklist_path")
    return Evidence(
        checklist_path=Path(checklist) if checklist else None,
        checklist_annex_hash=payload.get("checklist_annex_hash", ""),
        self_check_recorded=payload.get("self_check_recorded"),
        lint_run_version=payload.get("lint_run_version", ""),
        lint_run_profile=payload.get("lint_run_profile", ""),
        waivers=tuple(payload.get("waivers", ())),
        owner_review_recorded=payload.get("owner_review_recorded"),
        proxy_review_recorded=payload.get("proxy_review_recorded"),
        reader_test_recorded=payload.get("reader_test_recorded"),
    )


def main() -> int:
    args = parse_args()
    if not args.input.is_file():
        print(f"no such document: {args.input}", file=sys.stderr)
        return 2
    try:
        spec = parse_specification(args.spec_dir)
    except SpecError as error:
        print(f"specification defect: {error}", file=sys.stderr)
        return 2

    report = validate_document(
        spec,
        args.input,
        spec_dir=args.spec_dir,
        profile=args.profile,
        tier=args.tier,
        evidence=load_evidence(args.evidence),
        network=args.network,
        check_artifacts=not args.skip_artifact_check,
    )

    if args.json:
        print(dumps(report.to_json()))
    else:
        print(f"document : {report.path}")
        print(f"version  : {report.itws_version}")
        print(f"profile  : {report.profile or '(undeclared)'}")
        print(f"tier     : {report.tier}")
        print(f"state    : {report.state}")
        for reason in report.reasons:
            print(f"  - {reason}")
        if report.human_gates:
            print("human gates:")
            for name, state in report.human_gates.items():
                print(f"  {name}: {state}")
        if report.lint:
            print(
                f"lint: {len(report.lint.findings)} finding(s), "
                f"{len(report.lint.errors)} error(s), "
                f"{len(report.lint.blocked)} blocked"
            )

    if args.strict:
        return 0 if report.state == "pass" else 1
    return EXIT_CODES[report.state]


if __name__ == "__main__":
    raise SystemExit(main())

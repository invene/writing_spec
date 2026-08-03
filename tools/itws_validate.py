#!/usr/bin/env python3
"""Validate one governed document and report machine ``pass`` or ``fail``.

The JSON report discloses fully checked, partially checked, and untested rule
IDs. A pass is a machine-check result, not full semantic certification.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.jsonio import dumps
from itws.parser import SpecError, parse_specification
from itws.validate import validate_document
from itws.vocab import PROFILE_IDS

EXIT_CODES = {"pass": 0, "fail": 1}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument("--profile", choices=PROFILE_IDS)
    parser.add_argument("--network", action="store_true")
    parser.add_argument(
        "--skip-artifact-check",
        action="store_true",
        help="do not recompile the catalog to confirm it is current",
    )
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


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
        network=args.network,
        check_artifacts=not args.skip_artifact_check,
    )

    if args.json:
        print(dumps(report.to_json()))
    else:
        print(f"document : {report.path}")
        print(f"version  : {report.itws_version}")
        print(f"profile  : {report.profile or '(undeclared)'}")
        print(f"result   : {report.result}")
        for reason in report.reasons:
            print(f"  - {reason}")
        if report.lint:
            print(
                f"lint: {len(report.lint.findings)} finding(s), "
                f"{len(report.lint.errors)} error(s), "
                f"{len(report.lint.candidates)} candidate(s); coverage "
                f"{len(report.lint.fully_checked_rules)} full, "
                f"{len(report.lint.partially_checked_rules)} partial, "
                f"{len(report.lint.untested_rules)} untested"
            )

    return EXIT_CODES[report.result]


if __name__ == "__main__":
    raise SystemExit(main())

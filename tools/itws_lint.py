#!/usr/bin/env python3
"""Run the repository-local ITWS linter over one governed document.

The linter uses only the Python standard library. Its word- and phrase-level
inputs are generated from the specification's phrase-list paragraphs, so the
living lists have one home (§8.2).

A `partial` rule produces a candidate. A candidate is a navigation lead for
a reader, never a confirmed violation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.jsonio import dumps
from itws.lint.engine import lint_path
from itws.lint.model import Evidence
from itws.parser import SpecError, parse_specification
from itws.vocab import PROFILE_IDS, TIERS

SEVERITY_ORDER = {"error": 0, "warning": 1, "suggestion": 2}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument("--spec", dest="spec_version", help="expected ITWS version")
    parser.add_argument("--profile", choices=PROFILE_IDS)
    parser.add_argument("--tier", choices=TIERS)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--network",
        action="store_true",
        help="enable DOI, URL, and archive checks; they are skipped by default",
    )
    parser.add_argument(
        "--severity",
        choices=("error", "warning", "suggestion"),
        default="suggestion",
        help="report findings at this severity or above",
    )
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

    if args.spec_version and args.spec_version != spec.version:
        print(
            f"requested ITWS {args.spec_version}; this checkout holds "
            f"{spec.version} (§8.2.3)",
            file=sys.stderr,
        )
        return 2

    evidence = Evidence(lint_run_version=spec.version)
    try:
        report = lint_path(
            spec,
            args.input,
            profile=args.profile,
            tier=args.tier,
            evidence=evidence,
            network=args.network,
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2

    threshold = SEVERITY_ORDER[args.severity]
    findings = [
        finding
        for finding in report.findings
        if SEVERITY_ORDER[finding.severity] <= threshold
    ]

    if args.json:
        print(dumps({**report.to_json(), "findings": [f.to_json() for f in findings]}))
    else:
        for finding in findings:
            print(
                f"{finding.path}:{finding.start_line}: {finding.severity}: "
                f"[{finding.kind}] §{finding.rule} {finding.message}"
            )
        print(
            f"\n{len(findings)} finding(s); {len(report.errors)} error(s); "
            f"{len(report.blocked)} blocked; "
            f"{len(report.checked_rules)} rule(s) checked; "
            f"Flesch-Kincaid grade {report.readability['grade_level']} "
            "(informative only)"
        )
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

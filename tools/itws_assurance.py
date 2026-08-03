#!/usr/bin/env python3
"""Optional assurance utilities; never used by default validation."""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.assurance.checklist import annex_revision, render
from itws.assurance.model import load_assurance_record
from itws.jsonio import dumps
from itws.parser import SpecError, parse_specification
from itws.vocab import PROFILE_IDS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)

    checklist = subparsers.add_parser("checklist")
    checklist.add_argument("--spec-dir", type=Path, default=Path("spec"))
    checklist.add_argument("--profile", choices=PROFILE_IDS, required=True)
    checklist.add_argument("--out", type=Path, required=True)

    inspect = subparsers.add_parser("inspect")
    inspect.add_argument("--record", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.action == "inspect":
        try:
            record = load_assurance_record(args.record)
        except (OSError, ValueError) as error:
            print(f"invalid assurance record: {error}", file=sys.stderr)
            return 2
        print(dumps(record.to_json()))
        return 1 if record.missing else 0

    try:
        spec = parse_specification(args.spec_dir)
    except SpecError as error:
        print(f"specification defect: {error}", file=sys.stderr)
        return 2
    annex = args.spec_dir / "annexes" / "annex-c-rule-index.md"
    annex_text = annex.read_text(encoding="utf-8")
    output = render(
        spec,
        profile=args.profile,
        generated_date=dt.datetime.now(dt.timezone.utc).date().isoformat(),
        index_revision=annex_revision(annex_text, spec.version),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

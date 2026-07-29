#!/usr/bin/env python3
"""Compile the ITWS Markdown into the committed agent catalog.

The catalog lives under ``spec/generated/agent/``. Every file is byte
deterministic and covered by ``manifest.json`` hashes (Rule 8.6.1).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.compile import GENERATED_DIRNAME, compile_all
from itws.parser import SpecError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the committed artifacts with a fresh build; write nothing",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="print nothing on success"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        artifacts, problems = compile_all(args.spec_dir, check_only=args.check)
    except SpecError as error:
        print(f"specification defect: {error}", file=sys.stderr)
        return 2

    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1

    if not args.quiet:
        action = "verified" if args.check else "wrote"
        target = args.spec_dir / GENERATED_DIRNAME
        print(f"{action} {len(artifacts)} artifact(s) under {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

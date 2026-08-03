#!/usr/bin/env python3
"""Generate an optional profile-aware assurance checklist.

The generator consumes the normalized model in :mod:`itws.parser`, not the
rendered Annex C table. Annex C remains the human-readable index; the
checklist is outside textual conformance and is never used by default
validation. New integrations should use ``tools/itws_assurance.py``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.assurance.checklist import (
    annex_revision,
    checklist_line,
    render,
)
from itws.parser import SpecError, parse_specification
from itws.vocab import PROFILE_IDS

__all__ = [
    "checklist_line",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-version", required=True)
    parser.add_argument("--profile", required=True, choices=PROFILE_IDS)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument(
        "--index",
        type=Path,
        default=Path("spec/annexes/annex-c-rule-index.md"),
        help="Annex C, hashed into the checklist header for provenance",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--generated-date",
        default=dt.datetime.now(dt.timezone.utc).date().isoformat(),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        spec = parse_specification(args.spec_dir)
    except SpecError as error:
        print(f"specification defect: {error}", file=sys.stderr)
        return 2

    if args.spec_version != spec.version:
        raise ValueError(
            f"the specification is {spec.version}, not requested {args.spec_version}"
        )

    revision = "not supplied"
    if args.index.exists():
        revision = annex_revision(
            args.index.read_text(encoding="utf-8"), spec.version
        )

    output = render(
        spec,
        profile=args.profile,
        generated_date=args.generated_date,
        index_revision=revision,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

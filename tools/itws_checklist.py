#!/usr/bin/env python3
"""Generate a profile- and tier-filtered ITWS conformance checklist.

The generator consumes the normalized model in :mod:`itws.parser`, not the
rendered Annex C table. Annex C remains the human-readable index; the
checklist and the profile manifest resolve one rule set, and
``tools/itws_compile.py`` fails when the two disagree.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.checklist import (
    annex_revision,
    applies_to_tier_gate,
    checklist_line,
    render,
    validate_tier,
)
from itws.parser import SpecError, parse_specification
from itws.vocab import MINIMUM_TIER, PROFILE_IDS, TIERS

__all__ = [
    "MINIMUM_TIER",
    "TIERS",
    "applies_to_tier_gate",
    "checklist_line",
    "validate_tier",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-version", required=True)
    parser.add_argument("--profile", required=True, choices=PROFILE_IDS)
    parser.add_argument("--tier", required=True, choices=TIERS)
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


def validate_minimum_tiers() -> None:
    if tuple(MINIMUM_TIER) != PROFILE_IDS:
        raise ValueError(
            "MINIMUM_TIER keys must match PROFILE_IDS in canonical order"
        )
    unknown = [tier for tier in MINIMUM_TIER.values() if tier not in TIERS]
    if unknown:
        raise ValueError(
            "MINIMUM_TIER contains unknown tier(s): " + ", ".join(sorted(set(unknown)))
        )


def main() -> int:
    validate_minimum_tiers()
    args = parse_args()
    validate_tier(args.profile, args.tier)
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
        tier=args.tier,
        generated_date=args.generated_date,
        index_revision=revision,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Print one profile's load set, reader overlay, skeleton, and rule IDs.

Copy this script and change what it prints. The catalog is a plain Python
object, so anything you can compute from a list of dictionaries is available
here.

    python3 examples/agent-scripts/inspect_profile.py design-rfc
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from itws.catalog import Catalog
from itws.vocab import PROFILE_IDS


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=PROFILE_IDS)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()

    catalog = Catalog.from_repo(args.repo)
    profile = catalog.get_profile(args.profile)
    skeleton = catalog.get_skeleton(args.profile)
    baseline = catalog.get_reader_baseline(args.profile)

    print(f"ITWS {catalog.version} — profile {profile['id']} ({profile['label']})")
    print(f"shallow-model outcome: {profile.get('shallow_model_outcome', '')}")
    print(f"job: {profile['job']}")

    print("\nload set:")
    for path in profile["load_set"]:
        print(f"  {path}")

    print("\nreader overlay (genre conventions only):")
    for item in baseline["overlay"]:
        print(f"  - {item}")

    print("\nskeleton:")
    for slot in skeleton["slots"]:
        indent = "    " if slot["parent"] else "  "
        marker = "required" if slot["required"] else "optional"
        print(f"{indent}{slot['name']} ({marker})")
    for policy in skeleton["mutation_policies"]:
        print(f"  mutation policy: {policy['scope']} is {policy['policy']}")

    envelope = catalog.envelope(args.profile)
    print(f"\nprofile envelope: {len(envelope)} active rules")
    print("  " + " ".join(rule["id"] for rule in envelope))

    # Replace this line with your own reasoning. The envelope above is the
    # widest correct rule set; narrowing it is your decision to justify.
    print("\nThe agent decides which of these rules a passage triggers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

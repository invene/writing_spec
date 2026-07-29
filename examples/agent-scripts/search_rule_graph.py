#!/usr/bin/env python3
"""Search the rule set and expand typed relations from your own seeds.

The search ranks results for convenience. Ranking is not applicability: the
whole profile envelope stays applicable no matter what this script prints.

    python3 examples/agent-scripts/search_rule_graph.py \\
        "caveat placement" --profile incident --depth 2
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from itws.catalog import Catalog, RuleTrail
from itws.vocab import PROFILE_IDS


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--profile", choices=PROFILE_IDS)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--trail", type=Path)
    args = parser.parse_args()

    catalog = Catalog.from_repo(args.repo)
    trail = RuleTrail()

    matches = catalog.search_rules(
        args.query, profile=args.profile, limit=args.limit
    )
    trail.record(
        "search_rules",
        {"query": args.query, "profile": args.profile},
        [match.rule_id for match in matches],
        note="seed selection for one passage",
    )

    print(f"seeds for {args.query!r}:")
    for match in matches:
        rule = catalog.get_rule(match.rule_id)
        print(f"  {match.rule_id:8} {rule['name']}  (score {match.score:.2f})")
        print(f"           reasons: {'; '.join(match.reasons)}")

    if not matches:
        print("  no match; widen the query or read the envelope directly")
        return 0

    seeds = [match.rule_id for match in matches]
    expansion = catalog.expand_relations(
        seeds, depth=args.depth, profile=args.profile
    )
    trail.record(
        "expand_relations",
        {"seeds": seeds, "depth": args.depth},
        [item["rule_id"] for item in expansion["reached"]],
    )

    print(f"\nrelation expansion to depth {args.depth}:")
    for item in expansion["reached"]:
        rule = catalog.get_rule(item["rule_id"])
        print(
            f"  depth {item['depth']}  {item['rule_id']:8} {rule['name']}"
            f"   [rewrite: {rule['navigation']['rewrite_guidance']}]"
        )

    prohibited = [
        rule["id"]
        for rule in expansion["rules"]
        if rule["navigation"]["rewrite_guidance"] == "prohibited"
    ]
    if prohibited:
        print(
            "\nrules in this beam forbid mutation on tooling authority alone: "
            + ", ".join(prohibited)
        )

    if args.trail:
        trail.write(args.trail)
        print(f"\nwrote rule trail to {args.trail}")

    # Replace this line with your own reasoning: decide which of these rules
    # the passage actually triggers, and record why.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

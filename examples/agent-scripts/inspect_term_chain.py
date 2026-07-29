#!/usr/bin/env python3
"""Print one glossary entry and the ladder it stands on.

Rule 2.3.2 requires a definition to use only assumed vocabulary and terms the
document already admitted. The chain below is the admission order that
satisfies that rule.

    python3 examples/agent-scripts/inspect_term_chain.py transformer
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from itws.catalog import Catalog, CatalogError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("term")
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()

    catalog = Catalog.from_repo(args.repo)
    try:
        record = catalog.get_glossary_entry(args.term)
    except CatalogError as error:
        print(error, file=sys.stderr)
        available = ", ".join(sorted(catalog.glossary))
        print(f"available terms: {available}", file=sys.stderr)
        return 1

    entry = record["entry"]
    print(f"{entry['term']} ({entry['part_of_speech']}) — {entry['status']}")
    print(f"  {entry['definition']}")
    print(f"\n  approved example: {entry['approved_example']}")
    print(f"  do not use for  : {entry['do_not_use']}")
    print(f"  profiles        : {', '.join(entry['profiles'])}")
    print(f"  source          : {entry['source_span']['path']}:"
          f"{entry['source_span']['start_line']}")

    print("\nadmission order required before this term:")
    if not record["prerequisite_chain"]:
        print("  (none; the entry stands on assumed vocabulary alone)")
    for position, name in enumerate(record["prerequisite_chain"], start=1):
        print(f"  {position}. {name}")

    if record["assumed_prerequisites"]:
        print("\nassumed under Annex B, so no admission is needed:")
        for item in record["assumed_prerequisites"]:
            print(f"  - {item}")

    total = len(record["prerequisite_chain"]) + 1
    pages = -(-total // 3)
    print(
        f"\nAdmitting {args.term} costs {total} admissions. Rule 4.8.1 caps "
        f"three per 500-word page, so the ladder needs at least {pages} page(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

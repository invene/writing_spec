#!/usr/bin/env python3
"""Print a document's headings and source spans, with no semantic labels.

The structural index reports syntax only. A slot link appears only when the
heading matches a canonical name, a permitted rename, or an authored section
map. Every other heading-to-slot relationship is yours to decide.

    python3 examples/agent-scripts/outline_document.py --input <document>.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from itws.document import parse_document
from itws.parser import parse_specification


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()

    spec = parse_specification(args.repo / "spec")
    provisional = parse_document(args.input)
    declared = provisional.declarations
    if declared is None:
        print("the document declares no profile; slots cannot be resolved")
        for problem in provisional.declaration_problems:
            print(f"  {problem}")
        manifest = provisional
        skeleton = None
    else:
        skeleton = spec.skeleton(declared.profile)
        manifest = parse_document(args.input, skeleton=skeleton)
        print(
            f"ITWS {declared.itws_version} · profile {declared.profile} · "
            f"tier {declared.tier}"
        )

    print(f"\n{len(manifest.units)} source units, {manifest.line_count} lines")
    print(f"document hash: {manifest.document_hash}\n")

    unresolved: list[str] = []
    for unit in manifest.units:
        if unit.node_type != "heading":
            continue
        title = unit.heading_path[-1]
        indent = "  " * (unit.heading_level - 1)
        if unit.canonical_slot:
            marker = f" -> {unit.canonical_slot} ({unit.slot_evidence})"
        else:
            marker = "  [no explicit slot link]"
            unresolved.append(title)
        print(
            f"{indent}{title}"
            f"   [{unit.span.start_line}-{unit.span.end_line}] {unit.id}{marker}"
        )

    if skeleton and unresolved:
        print("\nHeadings with no explicit slot link:")
        for title in unresolved:
            print(f"  {title}")
        print(
            "Deciding whether one of these fills a required slot is your "
            "judgment. Record it with a rule citation, or add a section map."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

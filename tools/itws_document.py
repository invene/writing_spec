#!/usr/bin/env python3
"""Index a governed Markdown document's structure without changing it.

The tool records syntax, never meaning. It reports headings, paragraphs,
lists, tables, code fences, quotations, links, and source spans. It never
reports that a span is a claim, a requirement, a caveat, an exact item, or
any other §4.1 purpose: §1.6.1 reserves that judgment for a reader or agent.

With ``--out`` the manifest is written to a file. Without it the JSON goes to
standard output so an agent can pipe it into its own script.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.document import outline, parse_document
from itws.jsonio import dumps
from itws.parser import SpecError, parse_specification
from itws.vocab import PROFILE_IDS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "action", choices=("index", "outline"), help="full manifest or heading list"
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument(
        "--profile",
        choices=PROFILE_IDS,
        help="override the declared profile when resolving skeleton slots",
    )
    parser.add_argument("--out", type=Path, help="write JSON here instead of stdout")
    parser.add_argument("--json", action="store_true", help="print JSON for outline")
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

    provisional = parse_document(args.input)
    declared = provisional.declarations
    profile = args.profile or (declared.profile if declared else None)
    skeleton = spec.skeleton(profile) if profile else None
    manifest = parse_document(args.input, skeleton=skeleton)
    if profile and spec.profile(profile):
        manifest.profile_envelope = tuple(
            rule.number for rule in spec.envelope(profile)
        )
    manifest.artifact_manifest_hash = spec.source_hashes.get(
        "spec/00-front-matter.md", ""
    )

    for problem in manifest.declaration_problems + manifest.section_map_problems:
        print(f"{args.input}: {problem}", file=sys.stderr)

    if args.action == "outline":
        rows = outline(manifest)
        if args.json or args.out:
            payload = dumps({"path": manifest.path, "headings": rows})
        else:
            payload = "\n".join(
                f"{'  ' * (row['level'] - 1)}{row['heading']}"
                f"   [{row['start_line']}-{row['end_line']}]"
                + (
                    f"  -> {row['canonical_slot']} ({row['slot_evidence']})"
                    if row["canonical_slot"]
                    else ""
                )
                for row in rows
            )
    else:
        payload = dumps(manifest.to_json())

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload if payload.endswith("\n") else payload + "\n",
                            encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

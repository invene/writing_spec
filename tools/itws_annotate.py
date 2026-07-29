#!/usr/bin/env python3
"""Write the curated §1.6 navigation metadata into the rule Markdown.

The Markdown files stay authoritative. This tool is a one-way authoring aid:
it inserts or replaces the four metadata lines of each rule block, and the
parser then reads those lines back from the Markdown.

Run ``--check`` to confirm that the files already carry the curated values.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.annotations import ANNOTATIONS, metadata_lines
from itws.parser import METADATA_RE, PROFILES_RE, RULE_RE, rule_files

MANAGED_PREFIXES = (
    "**Constructs:**",
    "**Navigation:**",
    "**Resources:**",
    "**Relations:**",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument(
        "--check",
        action="store_true",
        help="report files that would change instead of writing them",
    )
    return parser.parse_args()


def annotate_file(path: Path) -> tuple[list[str], list[str]]:
    """Return the rewritten lines and the rule IDs this file carries."""
    lines = path.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    covered: list[str] = []
    index = 0
    while index < len(lines):
        header = RULE_RE.match(lines[index])
        if not header:
            output.append(lines[index])
            index += 1
            continue

        number = header.group("number")
        covered.append(number)
        output.append(lines[index])
        index += 1

        if index >= len(lines) or not METADATA_RE.match(lines[index]):
            raise SystemExit(f"{path}:{index + 1}: rule {number} has no Class line")
        output.append(lines[index])
        index += 1

        if index < len(lines) and PROFILES_RE.match(lines[index]):
            output.append(lines[index])
            index += 1

        while index < len(lines) and lines[index].startswith(MANAGED_PREFIXES):
            index += 1

        output.extend(metadata_lines(number))

    return output, covered


def main() -> int:
    args = parse_args()
    changed: list[str] = []
    seen: list[str] = []

    for path in rule_files(args.spec_dir):
        original = path.read_text(encoding="utf-8")
        rewritten, covered = annotate_file(path)
        seen.extend(covered)
        text = "\n".join(rewritten) + "\n"
        if text != original:
            changed.append(path.as_posix())
            if not args.check:
                path.write_text(text, encoding="utf-8")

    missing = sorted(set(seen) - set(ANNOTATIONS))
    unused = sorted(set(ANNOTATIONS) - set(seen))
    if missing:
        print("rules without curated metadata: " + ", ".join(missing), file=sys.stderr)
    if unused:
        print("curated metadata for absent rules: " + ", ".join(unused), file=sys.stderr)
    if missing or unused:
        return 1

    if args.check:
        if changed:
            print(
                "navigation metadata is stale in: " + ", ".join(changed),
                file=sys.stderr,
            )
            return 1
        print(f"navigation metadata is current for {len(seen)} rules")
        return 0

    print(f"annotated {len(seen)} rules across {len(changed)} changed file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

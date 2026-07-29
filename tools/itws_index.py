#!/usr/bin/env python3
"""Generate Annex C from ITWS rule metadata.

The generator consumes the normalized model in :mod:`itws.parser`. The
command-line interface is unchanged from 0.5.1-draft; `--check` is additive.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.model import Rule
from itws.parser import (
    OVERLAY_DIRNAME,
    PROFILE_RULES_FILENAME,
    SHARED_DIRNAME,
    SpecError,
    parse_rules,
    parse_specification,
    read_version,
    rule_files,
)
from itws.vocab import PROFILE_FAMILIES, PROFILE_IDS

__all__ = [
    "OVERLAY_DIRNAME",
    "PROFILE_FAMILIES",
    "PROFILE_IDS",
    "PROFILE_RULES_FILENAME",
    "SHARED_DIRNAME",
    "parse_rules",
    "rule_files",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-dir", type=Path, default=Path("spec"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("spec/annexes/annex-c-rule-index.md"),
    )
    parser.add_argument(
        "--generated-date",
        default=dt.datetime.now(dt.timezone.utc).date().isoformat(),
        help="ISO date written to the generated header",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("spec/rule-ids.txt"),
        help="source-controlled permanent rule-ID registry",
    )
    parser.add_argument(
        "--update-registry",
        action="store_true",
        help="append newly assigned IDs to the permanent registry",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the committed annex with a fresh build; write nothing",
    )
    return parser.parse_args()


def escape_cell(value: str) -> str:
    return value.replace("|", r"\|")


def read_registry(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids: set[str] = set()
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not re.fullmatch(r"\d+\.\d+\.\d+", line):
            raise ValueError(f"{path}:{line_number}: malformed permanent rule ID")
        if line in ids:
            raise ValueError(f"{path}:{line_number}: duplicate permanent rule ID")
        ids.add(line)
    return ids


def write_registry(path: Path, ids: set[str]) -> None:
    ordered = sorted(
        ids, key=lambda number: tuple(int(part) for part in number.split("."))
    )
    content = (
        "# ITWS permanent rule IDs\n"
        "# Append through tools/itws_index.py --update-registry; never remove.\n"
        + "\n".join(ordered)
        + "\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render(version: str, generated_date: str, rules: list[Rule]) -> str:
    rows = []
    for rule in rules:
        applicability = (
            ", ".join(f"`{profile}`" for profile in rule.profiles)
            if rule.profiles
            else "all profiles"
        )
        navigation = rule.navigation
        rows.append(
            "| "
            + " | ".join(
                (
                    rule.number,
                    escape_cell(rule.name),
                    rule.rule_class,
                    rule.machine_checkable,
                    applicability,
                    rule.status,
                    navigation.target,
                    escape_cell(", ".join(navigation.constructs)),
                    navigation.layers,
                    navigation.context_scope,
                    navigation.rewrite_guidance,
                    str(rule.precedence_layer),
                    escape_cell(rule.source),
                    f"`{rule.span.path.removeprefix('spec/')}`",
                )
            )
            + " |"
        )

    return f"""# Annex C — Rule index (generated)

**Status:** generated {generated_date} from ITWS {version}. Do not edit this annex by hand.

## C.1 Generation contract

For each rule of Parts 2–8, this annex records:

| Field | Source |
| --- | --- |
| Rule number | `#### Rule <n>` header; permanent under §0.8 |
| Short name | rule-header title |
| Class | `Class` metadata |
| Machine-checkable | `Machine-checkable` metadata |
| Profiles | `Profiles` metadata; absence means all profiles |
| Status | optional `Status` metadata; absence means active |
| Target | §1.6 `Navigation` metadata |
| Constructs | §1.6 `Constructs` metadata; the only navigation field with normative force |
| Layers | §1.6 `Navigation` metadata |
| Context | §1.6 `Navigation` metadata |
| Rewrite | §1.6 `Navigation` metadata |
| Precedence | derived from §1.4 through §1.6.3 |
| Source framework | `Source` metadata; feeds Annex F |
| File | the spec-relative file that holds the rule; §1.5.2 fixes it |

A scoped rule keeps its section number and sits in an overlay file. The `File` column lets a reader or tool load one profile's rules without reading unrelated overlays.

The full rule record, including chunk types, skeleton slots, resources, typed relations, examples, and source line ranges, is in `spec/generated/agent/rules.jsonl`. This annex is the human-readable view of the same model.

The index is sorted numerically by rule number. It is the input to the §8.1 checklist generator, which filters rules by declared ITWS version and profile before grouping them into the four self-check passes. Tier obligations come from §0.4.3 and Part 8; they are not rule-profile metadata.

## C.2 Generation command

Regenerate this index after changing rule metadata:

```text
python3 tools/itws_index.py \\
  --spec-dir spec \\
  --out spec/annexes/annex-c-rule-index.md
```

After approving a new permanent rule ID, add `--update-registry` once to append it to `spec/rule-ids.txt`.

The generator reads the core parts and the overlay files in `spec/overlays/`. It validates rule IDs against `spec/rule-ids.txt` independently of the output path. It fails on a duplicate or removed rule number, an unregistered new ID without `--update-registry`, malformed metadata, an unknown profile ID, a profile list outside canonical registry order, an unknown §1.6 navigation value, an unresolved rule relation, or a rule outside the file that §1.5.2 requires. A deprecated rule remains in its source file with `**Status:** deprecated since <version>; replacement <rule ID | none>`; generation never drops its permanent ID.

Regenerate the machine catalog in the same change:

```text
python3 tools/itws_compile.py --spec-dir spec
```

Generate a document's §8.1 checklist from this annex:

```text
python3 tools/itws_checklist.py \\
  --spec-version {version} \\
  --profile <canonical profile ID> \\
  --tier <core | reviewed | publication> \\
  --out <document-checklist.md>
```

## C.3 Index

**Rule count:** {len(rules)}

| Rule | Short name | Class | Machine-checkable | Profiles | Status | Target | Constructs | Layers | Context | Rewrite | Precedence | Source | File |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}
"""


def main() -> int:
    args = parse_args()
    try:
        version, _status = read_version(args.spec_dir)
        spec = parse_specification(args.spec_dir)
    except SpecError as error:
        print(f"specification defect: {error}", file=sys.stderr)
        return 2
    rules = list(spec.rules)

    current_ids = {rule.number for rule in rules}
    registry_ids = read_registry(args.registry)
    if not registry_ids and not args.update_registry:
        raise ValueError(
            f"permanent rule-ID registry missing or empty: {args.registry}"
        )
    removed_ids = registry_ids - current_ids
    if removed_ids:
        raise ValueError(
            "permanent rule ID(s) removed from source: " + ", ".join(sorted(removed_ids))
        )
    new_ids = current_ids - registry_ids
    if new_ids and not args.update_registry:
        raise ValueError(
            "new rule ID(s) are not in the permanent registry; rerun with "
            "--update-registry after review: " + ", ".join(sorted(new_ids))
        )
    if args.update_registry and not args.check:
        write_registry(args.registry, registry_ids | current_ids)

    output = render(version, args.generated_date, rules)
    if args.check:
        if not args.out.exists():
            print(f"missing generated annex: {args.out}", file=sys.stderr)
            return 1
        current = args.out.read_text(encoding="utf-8")
        if _without_date(current) != _without_date(output):
            print(f"stale generated annex: {args.out}", file=sys.stderr)
            return 1
        print(f"Annex C is current for {len(rules)} rules")
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    return 0


def _without_date(text: str) -> str:
    """Ignore the generation date when comparing two renderings."""
    return re.sub(r"generated \d{4}-\d{2}-\d{2} from", "generated <date> from", text)


if __name__ == "__main__":
    raise SystemExit(main())

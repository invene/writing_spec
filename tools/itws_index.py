#!/usr/bin/env python3
"""Generate Annex C from ITWS rule metadata."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path


PROFILE_IDS = (
    "design-rfc",
    "decision-record",
    "procedure",
    "explanation",
    "incident",
    "technical-report",
    "research-paper",
    "investigation-log",
)

RULE_RE = re.compile(
    r"^#### Rule (?P<number>\d+\.\d+\.\d+) — (?P<name>.+)$"
)
METADATA_RE = re.compile(
    r"^\*\*Class:\*\* (?P<class>mandatory|recommended|permitted)"
    r" · \*\*Machine-checkable:\*\* (?P<machine>yes|partial|no)"
    r" · \*\*Source:\*\* (?P<source>.+)$"
)
PROFILES_RE = re.compile(r"^\*\*Profiles:\*\* (?P<profiles>.+)$")
STATUS_RE = re.compile(
    r"^\*\*Status:\*\* (?P<status>active|deprecated)(?P<detail>.*)$"
)
DEPRECATED_DETAIL_RE = re.compile(
    r"^ since (?P<version>\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?); "
    r"replacement (?P<replacement>\d+\.\d+\.\d+|none)$"
)
VERSION_RE = re.compile(r"^\*\*Version:\*\* (?P<version>[^ ·]+)")


@dataclass(frozen=True)
class Rule:
    number: str
    name: str
    rule_class: str
    machine_checkable: str
    source: str
    profiles: tuple[str, ...]
    status: str
    replacement: str | None

    @property
    def sort_key(self) -> tuple[int, int, int]:
        major, section, rule = self.number.split(".")
        return int(major), int(section), int(rule)


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
    return parser.parse_args()


def read_version(spec_dir: Path) -> str:
    front_matter = spec_dir / "00-front-matter.md"
    for line in front_matter.read_text(encoding="utf-8").splitlines():
        match = VERSION_RE.match(line)
        if match:
            return match.group("version")
    raise ValueError(f"missing version metadata in {front_matter}")


def parse_rules(spec_dir: Path) -> list[Rule]:
    rules: list[Rule] = []
    seen: set[str] = set()

    for path in sorted(spec_dir.glob("0[2-8]-*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            header = RULE_RE.match(line)
            if not header:
                continue

            if index + 1 >= len(lines):
                raise ValueError(f"{path}:{index + 1}: rule has no metadata")
            metadata = METADATA_RE.match(lines[index + 1])
            if not metadata:
                raise ValueError(
                    f"{path}:{index + 2}: missing or malformed rule metadata"
                )

            profiles: tuple[str, ...] = ()
            status = "active"
            replacement: str | None = None
            next_metadata_index = index + 2
            if index + 2 < len(lines):
                profile_match = PROFILES_RE.match(lines[index + 2])
                if profile_match:
                    profiles = tuple(
                        item.strip()
                        for item in profile_match.group("profiles").split(",")
                    )
                    validate_profiles(path, index + 3, profiles)
                    next_metadata_index += 1

            if next_metadata_index < len(lines):
                status_line = lines[next_metadata_index]
                status_match = STATUS_RE.match(status_line)
                if status_match:
                    status = status_match.group("status")
                    detail = status_match.group("detail")
                    if status == "active" and detail:
                        raise ValueError(
                            f"{path}:{next_metadata_index + 1}: "
                            "active status cannot carry details"
                        )
                    if status == "deprecated":
                        detail_match = DEPRECATED_DETAIL_RE.match(detail)
                        if not detail_match:
                            raise ValueError(
                                f"{path}:{next_metadata_index + 1}: deprecated "
                                "status must name version and replacement"
                            )
                        replacement_value = detail_match.group("replacement")
                        if replacement_value != "none":
                            replacement = replacement_value
                elif status_line.startswith("**Status:**"):
                    raise ValueError(
                        f"{path}:{next_metadata_index + 1}: malformed status metadata"
                    )

            number = header.group("number")
            if number in seen:
                raise ValueError(f"{path}:{index + 1}: duplicate rule {number}")
            seen.add(number)
            rules.append(
                Rule(
                    number=number,
                    name=header.group("name"),
                    rule_class=metadata.group("class"),
                    machine_checkable=metadata.group("machine"),
                    source=metadata.group("source"),
                    profiles=profiles,
                    status=status,
                    replacement=replacement,
                )
            )

    if not rules:
        raise ValueError(f"no rules found under {spec_dir}")
    return sorted(rules, key=lambda rule: rule.sort_key)


def validate_profiles(
    path: Path, line_number: int, profiles: tuple[str, ...]
) -> None:
    if not profiles:
        raise ValueError(f"{path}:{line_number}: empty Profiles metadata")
    if len(set(profiles)) != len(profiles):
        raise ValueError(f"{path}:{line_number}: duplicate profile ID")

    unknown = [profile for profile in profiles if profile not in PROFILE_IDS]
    if unknown:
        raise ValueError(
            f"{path}:{line_number}: unknown profile ID(s): {', '.join(unknown)}"
        )

    expected = tuple(profile for profile in PROFILE_IDS if profile in profiles)
    if profiles != expected:
        raise ValueError(
            f"{path}:{line_number}: profile IDs are not in registry order"
        )


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
            raise ValueError(
                f"{path}:{line_number}: malformed permanent rule ID"
            )
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
                    escape_cell(rule.source),
                )
            )
            + " |"
        )

    return f"""# Annex C — Rule index (generated)

**Status:** generated {generated_date} from ITWS {version}. Do not edit this annex by hand.

## C.1 Generation contract

For each rule in Parts 2–8, this annex records:

| Field | Source |
| --- | --- |
| Rule number | `#### Rule <n>` header; permanent under §0.8 |
| Short name | rule-header title |
| Class | `Class` metadata |
| Machine-checkable | `Machine-checkable` metadata |
| Profiles | `Profiles` metadata; absence means all profiles |
| Status | optional `Status` metadata; absence means active |
| Source framework | `Source` metadata; feeds Annex F |

The index is sorted numerically by rule number. It is the input to the §8.1 checklist generator, which filters rules by declared ITWS version and profile before grouping them into the four self-check passes. Tier obligations come from §0.4.3 and Part 8; they are not rule-profile metadata.

## C.2 Generation command

Regenerate this index after changing rule metadata:

```text
python3 tools/itws_index.py \\
  --spec-dir spec \\
  --out spec/annexes/annex-c-rule-index.md
```

After approving a new permanent rule ID, add `--update-registry` once to append it to `spec/rule-ids.txt`.

The generator validates rule IDs against `spec/rule-ids.txt` independently of the output path. It fails on a duplicate or removed rule number, an unregistered new ID without `--update-registry`, malformed metadata, an unknown profile ID, or a profile list outside canonical registry order. A deprecated rule remains in its source file with `**Status:** deprecated since <version>; replacement <rule ID | none>`; generation never drops its permanent ID.

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

| Rule | Short name | Class | Machine-checkable | Profiles | Status | Source |
| --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}
"""


def main() -> None:
    args = parse_args()
    version = read_version(args.spec_dir)
    rules = parse_rules(args.spec_dir)
    current_ids = {rule.number for rule in rules}
    for rule in rules:
        if rule.replacement is None:
            continue
        if rule.replacement == rule.number:
            raise ValueError(
                f"deprecated rule {rule.number} cannot replace itself"
            )
        if rule.replacement not in current_ids:
            raise ValueError(
                f"deprecated rule {rule.number} names missing replacement "
                f"{rule.replacement}"
            )
    registry_ids = read_registry(args.registry)
    if not registry_ids and not args.update_registry:
        raise ValueError(
            f"permanent rule-ID registry missing or empty: {args.registry}"
        )
    removed_ids = registry_ids - current_ids
    if removed_ids:
        raise ValueError(
            "permanent rule ID(s) removed from source: "
            + ", ".join(sorted(removed_ids))
        )
    new_ids = current_ids - registry_ids
    if new_ids and not args.update_registry:
        raise ValueError(
            "new rule ID(s) are not in the permanent registry; rerun with "
            "--update-registry after review: "
            + ", ".join(sorted(new_ids))
        )
    if args.update_registry:
        write_registry(args.registry, registry_ids | current_ids)
    output = render(version, args.generated_date, rules)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()

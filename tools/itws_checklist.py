#!/usr/bin/env python3
"""Generate a profile- and tier-filtered ITWS conformance checklist."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from itws_index import PROFILE_IDS


TIERS = ("core", "reviewed", "publication")
MINIMUM_TIER = {
    "design-rfc": "reviewed",
    "decision-record": "core",
    "procedure": "reviewed",
    "explanation": "core",
    "incident": "reviewed",
    "technical-report": "reviewed",
    "research-paper": "publication",
    "investigation-log": "core",
}

PASS_NAMES = {
    "2": "Vocabulary",
    "3": "Sentences",
    "4": "Structure and explanation",
    "5": "Technical exactness and evidence",
    "6": "Structure and explanation",
    "7": "Technical exactness and evidence",
}
PASS_ORDER = (
    "Vocabulary",
    "Sentences",
    "Structure and explanation",
    "Technical exactness and evidence",
)
INDEX_VERSION_RE = re.compile(
    r"^\*\*Status:\*\* generated (?P<date>\d{4}-\d{2}-\d{2}) from ITWS "
    r"(?P<version>\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?)\.",
    re.MULTILINE,
)
RULE_ROW_RE = re.compile(
    r"^\| (?P<number>\d+\.\d+\.\d+) \| "
    r"(?P<name>.*?) \| "
    r"(?P<class>mandatory|recommended|permitted) \| "
    r"(?P<machine>yes|partial|no) \| "
    r"(?P<profiles>.*?) \| "
    r"(?P<status>active|deprecated) \| "
    r"(?P<source>.*?) \|$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class IndexedRule:
    number: str
    name: str
    rule_class: str
    machine_checkable: str
    profiles: tuple[str, ...]
    status: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec-version", required=True)
    parser.add_argument("--profile", required=True, choices=PROFILE_IDS)
    parser.add_argument("--tier", required=True, choices=TIERS)
    parser.add_argument(
        "--index",
        type=Path,
        default=Path("spec/annexes/annex-c-rule-index.md"),
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--generated-date",
        default=dt.datetime.now(dt.timezone.utc).date().isoformat(),
    )
    return parser.parse_args()


def parse_index(path: Path) -> tuple[str, str, list[IndexedRule]]:
    text = path.read_text(encoding="utf-8")
    version_match = INDEX_VERSION_RE.search(text)
    if not version_match:
        raise ValueError(f"cannot read ITWS version from {path}")

    rules: list[IndexedRule] = []
    for match in RULE_ROW_RE.finditer(text):
        profile_cell = match.group("profiles")
        profiles = (
            ()
            if profile_cell == "all profiles"
            else tuple(re.findall(r"`([^`]+)`", profile_cell))
        )
        rules.append(
            IndexedRule(
                number=match.group("number"),
                name=match.group("name"),
                rule_class=match.group("class"),
                machine_checkable=match.group("machine"),
                profiles=profiles,
                status=match.group("status"),
            )
        )

    if not rules:
        raise ValueError(f"no generated rule rows found in {path}")
    revision = (
        f"generated {version_match.group('date')} "
        f"from ITWS {version_match.group('version')}; "
        f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"
    )
    return version_match.group("version"), revision, rules


def validate_tier(profile: str, tier: str) -> None:
    minimum = MINIMUM_TIER[profile]
    if TIERS.index(tier) < TIERS.index(minimum):
        raise ValueError(
            f"profile {profile} requires at least {minimum}; received {tier}"
        )


def applies_to_profile(rule: IndexedRule, profile: str) -> bool:
    return not rule.profiles or profile in rule.profiles


def applies_to_tier_gate(rule: IndexedRule, tier: str) -> bool:
    part, section, _ = rule.number.split(".")
    if part != "8":
        return False
    if section in {"1", "2", "5"}:
        return True
    if section == "4":
        return tier in {"reviewed", "publication"}
    if section == "3":
        return tier == "publication"
    return False


def checklist_line(rule: IndexedRule) -> str:
    return (
        f"- [ ] ITWS §{rule.number} — {rule.name} "
        f"({rule.rule_class}; machine-checkable: {rule.machine_checkable})"
    )


def render(
    version: str,
    profile: str,
    tier: str,
    generated_date: str,
    index_revision: str,
    rules: list[IndexedRule],
) -> str:
    applicable = [
        rule
        for rule in rules
        if rule.status == "active" and applies_to_profile(rule, profile)
    ]

    pass_rules: dict[str, list[IndexedRule]] = {
        pass_name: [] for pass_name in PASS_ORDER
    }
    for rule in applicable:
        part = rule.number.split(".", 1)[0]
        pass_name = PASS_NAMES.get(part)
        if pass_name:
            pass_rules[pass_name].append(rule)

    gates = [
        rule for rule in applicable if applies_to_tier_gate(rule, tier)
    ]
    lines = [
        "# ITWS conformance checklist",
        "",
        f"**Generated:** {generated_date}",
        f"**ITWS version:** {version}",
        f"**Profile:** `{profile}`",
        f"**Conformance tier:** `{tier}`",
        f"**Annex C revision:** {index_revision}",
        "",
        "This file is generated from Annex C. Do not edit its rule inventory by hand.",
        "",
        "## Author self-check",
    ]
    for pass_name in PASS_ORDER:
        lines.extend(("", f"### {pass_name}", ""))
        lines.extend(checklist_line(rule) for rule in pass_rules[pass_name])

    lines.extend(("", "## Conformance gates", ""))
    lines.extend(checklist_line(rule) for rule in gates)
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    validate_tier(args.profile, args.tier)
    index_version, index_revision, rules = parse_index(args.index)
    if args.spec_version != index_version:
        raise ValueError(
            f"Annex C is {index_version}, not requested {args.spec_version}"
        )
    output = render(
        version=index_version,
        profile=args.profile,
        tier=args.tier,
        generated_date=args.generated_date,
        index_revision=index_revision,
        rules=rules,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()

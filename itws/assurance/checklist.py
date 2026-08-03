"""Generate an optional profile-aware reading checklist."""

from __future__ import annotations

from itws.model import Rule, Specification, content_hash

PASS_ORDER = (
    "Vocabulary",
    "Sentences",
    "Structure and explanation",
    "Technical exactness and evidence",
)

PASS_BY_PART = {
    "2": "Vocabulary",
    "3": "Sentences",
    "4": "Structure and explanation",
    "5": "Technical exactness and evidence",
    "6": "Structure and explanation",
    "7": "Technical exactness and evidence",
}


def checklist_line(rule: Rule) -> str:
    navigation = rule.navigation
    return (
        f"- [ ] ITWS §{rule.number} — {rule.name} "
        f"({rule.rule_class}; machine-checkable: "
        f"{rule.machine_checkable}; target: {navigation.target}; "
        f"`{rule.span.path.removeprefix('spec/')}`)"
    )


def annex_revision(text: str, version: str) -> str:
    return f"generated from ITWS {version}; {content_hash(text)}"


def checklist_body(spec: Specification, *, profile: str) -> str:
    rules_by_pass: dict[str, list[Rule]] = {
        name: [] for name in PASS_ORDER
    }
    for rule in spec.envelope(profile):
        pass_name = PASS_BY_PART.get(rule.part)
        if pass_name:
            rules_by_pass[pass_name].append(rule)
    lines = [
        f"**ITWS version:** {spec.version}",
        f"**Profile:** `{profile}`",
        "",
        "This optional assurance checklist is generated from the current "
        "language-rule envelope. It is not an ITWS declaration.",
    ]
    for name in PASS_ORDER:
        lines.extend(("", f"## {name}", ""))
        lines.extend(
            checklist_line(rule) for rule in rules_by_pass[name]
        )
    return "\n".join(lines)


def render(
    spec: Specification,
    *,
    profile: str,
    generated_date: str,
    index_revision: str,
) -> str:
    body = checklist_body(spec, profile=profile)
    header = [
        "# Optional ITWS assurance checklist",
        "",
        f"**Generated:** {generated_date}",
        f"**Annex C revision:** {index_revision}",
        f"**Checklist digest:** {content_hash(body)}",
        "",
    ]
    return "\n".join(header) + body + "\n"

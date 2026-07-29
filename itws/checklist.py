"""Generation of the §8.1 conformance checklist.

The checklist and the profile manifest resolve one rule set. Both read the
normalized model, so ``tools/itws_compile.py`` can compare them and fail on a
disagreement.
"""

from __future__ import annotations

from itws.model import Rule, Specification, content_hash
from itws.vocab import CHECKLIST_PASS_ORDER, MINIMUM_TIER, TIERS


def validate_tier(profile: str, tier: str) -> None:
    """Reject a tier below the profile minimum (§0.4.3)."""
    minimum = MINIMUM_TIER[profile]
    if TIERS.index(tier) < TIERS.index(minimum):
        raise ValueError(
            f"profile {profile} requires at least {minimum}; received {tier}"
        )


def applies_to_tier_gate(rule: Rule, tier: str) -> bool:
    """Return whether a Part 8 rule is a gate for the declared tier."""
    part, section, _ = rule.number.split(".")
    if part != "8":
        return False
    if section in {"1", "2", "5", "6"}:
        return True
    if section == "4":
        return tier in {"reviewed", "publication"}
    if section == "3":
        return tier == "publication"
    return False


def checklist_line(rule: Rule) -> str:
    navigation = rule.navigation
    return (
        f"- [ ] ITWS §{rule.number} — {rule.name} "
        f"({rule.rule_class}; machine-checkable: {rule.machine_checkable}; "
        f"target: {navigation.target}; rewrite: {navigation.rewrite_guidance}; "
        f"`{rule.span.path.removeprefix('spec/')}`)"
    )


def annex_revision(text: str, version: str) -> str:
    """Provenance line that pins a checklist to one Annex C rendering."""
    return f"generated from ITWS {version}; {content_hash(text)}"


def render(
    spec: Specification,
    *,
    profile: str,
    tier: str,
    generated_date: str,
    index_revision: str,
) -> str:
    """Render the four self-check passes and the tier's conformance gates."""
    validate_tier(profile, tier)
    rules = list(spec.envelope(profile))

    pass_rules: dict[str, list[Rule]] = {name: [] for name in CHECKLIST_PASS_ORDER}
    for rule in rules:
        name = rule.checklist_pass
        if name:
            pass_rules[name].append(rule)

    gates = [rule for rule in rules if applies_to_tier_gate(rule, tier)]
    lines = [
        "# ITWS conformance checklist",
        "",
        f"**Generated:** {generated_date}",
        f"**ITWS version:** {spec.version}",
        f"**Profile:** `{profile}`",
        f"**Conformance tier:** `{tier}`",
        f"**Annex C revision:** {index_revision}",
        "",
        "This file is generated from Annex C. Do not edit its rule inventory by hand.",
        "",
        "## Author self-check",
    ]
    for name in CHECKLIST_PASS_ORDER:
        lines.extend(("", f"### {name}", ""))
        lines.extend(checklist_line(rule) for rule in pass_rules[name])

    lines.extend(("", "## Conformance gates", ""))
    lines.extend(checklist_line(rule) for rule in gates)
    lines.append("")
    return "\n".join(lines)

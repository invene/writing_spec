"""Compile the authoritative Markdown into the committed agent catalog.

The compiler writes ``spec/generated/agent/``. Every file is byte
deterministic and covered by ``manifest.json`` hashes, as Rule 8.6.1
requires. Nothing here decides what a governed document's prose means.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from itws import SCHEMA_VERSION
from itws.jsonio import dumps, dumps_lines
from itws.model import Relation, Rule, Specification, content_hash
from itws.parser import parse_specification
from itws.vocab import (
    PRECEDENCE_LAYERS,
    PROFILE_FAMILIES,
    PROFILE_IDS,
    PROFILE_SURFACES,
    SEVERITY_BY_CLASS,
    profile_families,
)

GENERATED_DIRNAME = "generated/agent"
GENERATION_COMMAND = "python3 tools/itws_compile.py --spec-dir spec"


@dataclass(frozen=True)
class Artifact:
    """One generated file, held in memory until the writer commits it."""

    relative_path: str
    text: str

    @property
    def hash(self) -> str:
        return content_hash(self.text)


def _exemplified_by(spec: Specification) -> dict[str, tuple[str, ...]]:
    """Map each rule to the Annex D examples that cite it."""
    edges: dict[str, list[str]] = {}
    for example in spec.examples:
        if example.origin != "annex-d":
            continue
        for number in example.rules_applied:
            edges.setdefault(number, []).append(example.id)
    return {number: tuple(ids) for number, ids in edges.items()}


def _rule_payload(rule: Rule, examples: tuple[str, ...]) -> dict[str, object]:
    payload = rule.to_json()
    relations = list(payload["relations"])  # type: ignore[arg-type]
    relations.extend(
        Relation(type="exemplified-by", target=example).to_json()
        for example in examples
    )
    payload["relations"] = relations
    payload["exemplified_by"] = list(examples)
    return payload


def build_artifacts(spec: Specification) -> list[Artifact]:
    """Build every artifact in deterministic order."""
    artifacts: list[Artifact] = []
    examples_by_rule = _exemplified_by(spec)

    # rules.jsonl — canonical rule order, one atom per line.
    artifacts.append(
        Artifact(
            "rules.jsonl",
            dumps_lines(
                _rule_payload(rule, examples_by_rule.get(rule.number, ()))
                for rule in spec.rules
            ),
        )
    )

    # rule-graph.json — typed, resolved edges plus the §1.4 precedence order.
    edges: list[dict[str, object]] = []
    for rule in spec.rules:
        for relation in rule.relations:
            edges.append(
                {
                    "source": rule.number,
                    "type": relation.type,
                    "target": relation.target,
                    "note": relation.note,
                }
            )
        for example in examples_by_rule.get(rule.number, ()):
            edges.append(
                {
                    "source": rule.number,
                    "type": "exemplified-by",
                    "target": example,
                    "note": "",
                }
            )
    artifacts.append(
        Artifact(
            "rule-graph.json",
            dumps(
                {
                    "itws_version": spec.version,
                    "schema_version": SCHEMA_VERSION,
                    "precedence_layers": [
                        {"layer": layer, "id": name, "statement": statement}
                        for layer, name, statement in PRECEDENCE_LAYERS
                    ],
                    "rule_precedence": {
                        rule.number: rule.precedence_layer for rule in spec.rules
                    },
                    "severity_by_class": dict(SEVERITY_BY_CLASS),
                    "edges": edges,
                }
            ),
        )
    )

    # glossary.json — the ladder, in Annex A order.
    artifacts.append(
        Artifact(
            "glossary.json",
            dumps(
                {
                    "itws_version": spec.version,
                    "schema_version": SCHEMA_VERSION,
                    "entries": [entry.to_json() for entry in spec.glossary],
                }
            ),
        )
    )

    # reader-baseline.json — Annex B plus each profile's overlay.
    artifacts.append(
        Artifact(
            "reader-baseline.json",
            dumps(
                {
                    "itws_version": spec.version,
                    "schema_version": SCHEMA_VERSION,
                    "shared": [item.to_json() for item in spec.baseline],
                    "profile_overlays": {
                        profile.id: [
                            item.to_json() for item in profile.reader_overlay
                        ]
                        for profile in spec.profiles
                    },
                    # The supplement is the conditional grant of §0.3.4 only.
                    # An exclusion beside it is not a supplement, and listing
                    # one here would read as a grant.
                    "host_supplements": {
                        profile.id: [
                            item.to_json()
                            for item in profile.reader_overlay
                            if item.conditional and item.is_assumed
                        ]
                        for profile in spec.profiles
                        if profile.surface == "hosted-comment-set"
                    },
                }
            ),
        )
    )

    # examples.jsonl — Annex D first, then each rule's contrasting pair.
    artifacts.append(
        Artifact(
            "examples.jsonl",
            dumps_lines(example.to_json() for example in spec.examples),
        )
    )

    # phrase-lists.json — the linter's generated word and phrase inputs.
    artifacts.append(
        Artifact(
            "phrase-lists.json",
            dumps(
                {
                    "itws_version": spec.version,
                    "schema_version": SCHEMA_VERSION,
                    "entries": [entry.to_json() for entry in spec.phrase_lists],
                }
            ),
        )
    )

    # profiles/<profile>.json — the resolved envelope for one profile.
    for profile in spec.profiles:
        envelope = spec.envelope(profile.id)
        payload = profile.to_json()
        payload.update(
            {
                "itws_version": spec.version,
                "schema_version": SCHEMA_VERSION,
                "families": list(profile_families(profile.id)),
                "envelope": {
                    "rule_count": len(envelope),
                    "universal": [
                        rule.number for rule in envelope if not rule.profiles
                    ],
                    "profile_scoped": [
                        rule.number for rule in envelope if rule.profiles
                    ],
                    "by_machine_checkability": {
                        state: [
                            rule.number
                            for rule in envelope
                            if rule.machine_checkable == state
                        ]
                        for state in ("yes", "partial", "no")
                    },
                },
            }
        )
        artifacts.append(
            Artifact(f"profiles/{profile.id}.json", dumps(payload))
        )

    # skeletons/<profile>.json — ordered slots, renames, merges, policies.
    for skeleton in spec.skeletons:
        payload = skeleton.to_json()
        payload["itws_version"] = spec.version
        payload["schema_version"] = SCHEMA_VERSION
        artifacts.append(
            Artifact(f"skeletons/{skeleton.profile}.json", dumps(payload))
        )

    return artifacts


def build_manifest(spec: Specification, artifacts: list[Artifact]) -> Artifact:
    """Build the inventory that pins the artifact set to its source."""
    payload = {
        "itws_version": spec.version,
        "itws_status": spec.status,
        "schema_version": SCHEMA_VERSION,
        "generation_command": GENERATION_COMMAND,
        "profiles": list(PROFILE_IDS),
        "profile_families": {
            family: list(members) for family, members in sorted(PROFILE_FAMILIES.items())
        },
        "profile_surfaces": dict(PROFILE_SURFACES),
        "counts": {
            "rules": len(spec.rules),
            "active_rules": sum(1 for rule in spec.rules if rule.is_active),
            "glossary_entries": len(spec.glossary),
            "baseline_items": len(spec.baseline),
            "examples": len(spec.examples),
            "phrase_list_entries": len(spec.phrase_lists),
        },
        "source_hashes": dict(sorted(spec.source_hashes.items())),
        "artifact_hashes": {
            artifact.relative_path: artifact.hash
            for artifact in sorted(artifacts, key=lambda item: item.relative_path)
        },
    }
    return Artifact("manifest.json", dumps(payload))


def check_envelope_agreement(spec: Specification) -> list[str]:
    """Confirm that every profile envelope follows rule applicability."""
    problems: list[str] = []
    for profile in PROFILE_IDS:
        envelope = {rule.number for rule in spec.envelope(profile)}
        expected = {
            rule.number
            for rule in spec.rules
            if rule.is_active and rule.applies_to_profile(profile)
        }
        if envelope != expected:
            missing = sorted(expected - envelope)
            extra = sorted(envelope - expected)
            problems.append(
                f"{profile}: envelope and applicability disagree "
                f"(missing {missing}; extra {extra})"
            )
    return problems


def check_registered_checkers(spec: Specification) -> list[str]:
    """Every ``Machine-checkable: yes`` rule needs a registered checker."""
    from itws.lint.registry import registered_rule_ids

    registered = registered_rule_ids()
    problems = []
    for rule in spec.rules:
        if not rule.is_active or rule.machine_checkable != "yes":
            continue
        if rule.number not in registered:
            problems.append(
                f"rule {rule.number} is machine-checkable 'yes' with no "
                "registered checker"
            )
    return problems


def compile_all(
    spec_dir: Path, *, check_only: bool = False
) -> tuple[list[Artifact], list[str]]:
    """Compile every artifact. Return the artifacts and any problems found."""
    spec = parse_specification(spec_dir)
    problems = check_envelope_agreement(spec)
    problems.extend(check_registered_checkers(spec))

    artifacts = build_artifacts(spec)
    artifacts.append(build_manifest(spec, artifacts))

    target = spec_dir / GENERATED_DIRNAME
    if check_only:
        for artifact in artifacts:
            path = target / artifact.relative_path
            if not path.exists():
                problems.append(f"missing generated artifact: {path}")
            elif path.read_text(encoding="utf-8") != artifact.text:
                problems.append(f"stale generated artifact: {path}")
        return artifacts, problems

    for artifact in artifacts:
        path = target / artifact.relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(artifact.text, encoding="utf-8")
    return artifacts, problems

"""Typed records for the ITWS specification model.

Every generator, checker, and navigation helper consumes these records.
Modules do not pass untyped dictionaries across their boundaries: a record
converts to JSON only at the serialization edge, through ``to_json``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, replace
from typing import Iterable

from itws.vocab import SEVERITY_BY_CLASS, rule_sort_key


@dataclass(frozen=True, order=True)
class SourceSpan:
    """A closed line range in one specification or document file.

    ``start_line`` and ``end_line`` are 1-indexed and inclusive, matching the
    line numbers an editor shows.
    """

    path: str
    start_line: int
    end_line: int

    def to_json(self) -> dict[str, object]:
        return {
            "path": self.path,
            "start_line": self.start_line,
            "end_line": self.end_line,
        }

    def contains(self, line: int) -> bool:
        return self.start_line <= line <= self.end_line

    def overlaps(self, other: "SourceSpan") -> bool:
        if self.path != other.path:
            return False
        return not (
            self.end_line < other.start_line or other.end_line < self.start_line
        )


@dataclass(frozen=True, order=True)
class Relation:
    """One typed edge from a rule to another rule."""

    type: str
    target: str
    note: str = ""

    def to_json(self) -> dict[str, object]:
        payload: dict[str, object] = {"type": self.type, "target": self.target}
        if self.note:
            payload["note"] = self.note
        return payload


@dataclass(frozen=True)
class Navigation:
    """Navigation facets for one rule.

    Only ``constructs`` records a normative condition. Every other field is a
    navigation aid and never narrows the profile envelope (§1.6).
    """

    target: str
    layers: str
    context_scope: str
    rewrite_guidance: str
    constructs: tuple[str, ...]
    chunk_types: tuple[str, ...]
    slots: tuple[str, ...]
    reads: tuple[str, ...]
    writes: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target,
            "layers": self.layers,
            "context_scope": self.context_scope,
            "rewrite_guidance": self.rewrite_guidance,
            "constructs": list(self.constructs),
            "chunk_types": list(self.chunk_types),
            "slots": list(self.slots),
            "reads": list(self.reads),
            "writes": list(self.writes),
        }


@dataclass(frozen=True)
class RuleExample:
    """The contrasting pair that §1.3 requires of every rule."""

    compliant: str
    non_compliant: str

    def to_json(self) -> dict[str, object]:
        return {"compliant": self.compliant, "non_compliant": self.non_compliant}


@dataclass(frozen=True)
class Rule:
    """One rule atom: identity, normative force, navigation, and source."""

    number: str
    name: str
    rule_class: str
    machine_checkable: str
    source: str
    profiles: tuple[str, ...]
    status: str
    deprecated_since: str | None
    replacement: str | None
    statement: str
    rationale: str
    example: RuleExample
    cross_references: str
    navigation: Navigation
    relations: tuple[Relation, ...]
    span: SourceSpan

    @property
    def sort_key(self) -> tuple[int, int, int]:
        return rule_sort_key(self.number)

    @property
    def part(self) -> str:
        return self.number.split(".", 1)[0]

    @property
    def section(self) -> str:
        part, section, _ = self.number.split(".")
        return f"{part}.{section}"

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def severity(self) -> str:
        """Severity under the §8.2 map."""
        return SEVERITY_BY_CLASS[self.rule_class]

    @property
    def precedence_layer(self) -> int:
        """§1.4 layer at which this rule wins a collision.

        Layer 1 holds the exact-layer and safety obligations of Parts 5 and 7.
        Layer 2 holds a profile-scoped exception that names the rule it
        displaces. Layer 3 holds the structure rules of Parts 4 and 6.
        Everything else is decided by rule class at layer 4.
        """
        if self.part in {"5", "7"}:
            return 1
        if self.profiles and "overrides" in {edge.type for edge in self.relations}:
            return 2
        if self.part in {"4", "6"}:
            return 3
        return 4

    def applies_to_profile(self, profile: str) -> bool:
        """Return whether the rule enters ``profile``'s envelope (§0.4.3)."""
        return not self.profiles or profile in self.profiles

    def to_json(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "id": self.number,
            "name": self.name,
            "class": self.rule_class,
            "machine_checkable": self.machine_checkable,
            "source": self.source,
            "profiles": list(self.profiles),
            "universal": not self.profiles,
            "status": self.status,
            "statement": self.statement,
            "rationale": self.rationale,
            "example": self.example.to_json(),
            "cross_references": self.cross_references,
            "navigation": self.navigation.to_json(),
            "relations": [relation.to_json() for relation in self.relations],
            "severity": self.severity,
            "precedence_layer": self.precedence_layer,
            "source_span": self.span.to_json(),
        }
        if self.status == "deprecated":
            payload["deprecated_since"] = self.deprecated_since
            payload["replacement"] = self.replacement
        return payload


@dataclass(frozen=True)
class Slot:
    """One canonical section of a profile skeleton."""

    name: str
    required: bool
    order: int
    description: str
    renames: tuple[str, ...] = ()
    parent: str = ""
    repeats: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "required": self.required,
            "order": self.order,
            "description": self.description,
            "renames": list(self.renames),
            "parent": self.parent,
            "repeats": self.repeats,
        }


@dataclass(frozen=True)
class Merge:
    """One permitted skeleton merge, with the heading it produces."""

    parts: tuple[str, ...]
    combined: str

    def to_json(self) -> dict[str, object]:
        return {"parts": list(self.parts), "combined": self.combined}


@dataclass(frozen=True)
class Skeleton:
    """One profile's ordered slots, renames, merges, and mutation policy."""

    profile: str
    annex_section: str
    surface: str
    dependency_order: str
    slots: tuple[Slot, ...]
    merges: tuple[Merge, ...]
    mutation_policies: tuple["MutationPolicy", ...]
    span: SourceSpan

    def slot(self, name: str) -> Slot | None:
        for candidate in self.slots:
            if candidate.name == name:
                return candidate
        return None

    def canonical_for_heading(self, heading: str) -> str | None:
        """Resolve a heading to a slot through an exact name or a rename.

        A slot name may carry ``<placeholder>`` parts, as a repeating log
        entry does. A placeholder matches one whitespace-free token.

        Returns ``None`` when the relationship is not explicit. Any other
        heading-to-slot judgment belongs to a reader or an agent (§1.6.1).
        """
        import re as _re

        normalized = heading.strip().rstrip(".").casefold()
        for slot in self.slots:
            for candidate in (slot.name, *slot.renames):
                lowered = candidate.casefold()
                if lowered == normalized:
                    return slot.name
                if "<" in lowered:
                    pattern = r"\s+".join(
                        r"\S+" if token.startswith("<") and token.endswith(">")
                        else _re.escape(token)
                        for token in lowered.split()
                    )
                    if _re.fullmatch(pattern, normalized):
                        return slot.name
        for merge in self.merges:
            if merge.combined.casefold() == normalized:
                return merge.combined
        return None

    def to_json(self) -> dict[str, object]:
        return {
            "profile": self.profile,
            "annex_section": self.annex_section,
            "surface": self.surface,
            "dependency_order": self.dependency_order,
            "slots": [slot.to_json() for slot in self.slots],
            "required_slots": [
                slot.name for slot in self.slots if slot.required
            ],
            "merges": [merge.to_json() for merge in self.merges],
            "mutation_policies": [
                policy.to_json() for policy in self.mutation_policies
            ],
            "source_span": self.span.to_json(),
        }


@dataclass(frozen=True)
class MutationPolicy:
    """A declared limit on rewriting an existing span of a governed document.

    ``append-only`` marks content that a later revision may extend but not
    change, such as an ``investigation-log`` entry that is already recorded.
    """

    scope: str
    policy: str
    rule: str
    note: str

    def to_json(self) -> dict[str, object]:
        return {
            "scope": self.scope,
            "policy": self.policy,
            "rule": self.rule,
            "note": self.note,
        }


@dataclass(frozen=True)
class GlossaryEntry:
    """One Annex A term with its ladder prerequisites."""

    term: str
    part_of_speech: str
    status: str
    definition: str
    approved_example: str
    do_not_use: str
    prerequisites: tuple[str, ...]
    assumed_prerequisites: tuple[str, ...]
    profiles: tuple[str, ...]
    domain_tag: str
    version: str
    span: SourceSpan

    def to_json(self) -> dict[str, object]:
        return {
            "term": self.term,
            "part_of_speech": self.part_of_speech,
            "status": self.status,
            "definition": self.definition,
            "approved_example": self.approved_example,
            "do_not_use": self.do_not_use,
            "prerequisites": list(self.prerequisites),
            "assumed_prerequisites": list(self.assumed_prerequisites),
            "profiles": list(self.profiles),
            "domain_tag": self.domain_tag,
            "version": self.version,
            "source_span": self.span.to_json(),
        }


@dataclass(frozen=True)
class Example:
    """One Annex D paired example or one rule's contrasting pair."""

    id: str
    origin: str
    title: str
    profile: str
    source: str
    rules_applied: tuple[str, ...]
    sections_applied: tuple[str, ...]
    before: str
    after: str
    annotation: str
    chunk_types: tuple[str, ...]
    constructs: tuple[str, ...]
    repair_operators: tuple[str, ...]
    preservation_notes: tuple[str, ...]
    span: SourceSpan

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "origin": self.origin,
            "title": self.title,
            "profile": self.profile,
            "source": self.source,
            "rules_applied": list(self.rules_applied),
            "sections_applied": list(self.sections_applied),
            "before": self.before,
            "after": self.after,
            "annotation": self.annotation,
            "chunk_types": list(self.chunk_types),
            "constructs": list(self.constructs),
            "repair_operators": list(self.repair_operators),
            "preservation_notes": list(self.preservation_notes),
            "source_span": self.span.to_json(),
        }


@dataclass(frozen=True)
class ProfileRecord:
    """One profile's language contract and reader overlay."""

    id: str
    label: str
    surface: str
    job: str
    shallow_model_outcome: str
    modules: tuple[str, ...]
    directory: str
    reader_overlay: tuple["BaselineItem", ...]
    span: SourceSpan

    @property
    def load_set(self) -> tuple[str, ...]:
        entries = [
            "spec/00-front-matter.md",
            "spec/01-foundations.md",
            "spec/02-words-and-vocabulary.md",
            "spec/03-sentences.md",
            "spec/04-structure.md",
            "spec/05-mathematical-and-empirical-content.md",
            "spec/06-explanatory-devices.md",
            "spec/07-limitations-caveats-interpretation.md",
            "spec/08-textual-conformance-and-machine-checking.md",
            "spec/annexes/annex-a-glossary.md",
            "spec/annexes/annex-b-assumed-reader-baseline.md",
            "spec/annexes/annex-c-rule-index.md",
            "spec/annexes/annex-d-examples-corpus.md",
            "spec/annexes/annex-e-document-skeletons.md",
            "spec/annexes/annex-f-traceability.md",
            "spec/annexes/annex-g-changelog.md",
            f"spec/overlays/{self.id}/README.md",
            f"spec/overlays/{self.id}/reader.md",
            f"spec/overlays/{self.id}/skeleton.md",
            f"spec/overlays/{self.id}/rules.md",
        ]
        entries.extend(f"spec/overlays/shared/{module}.md" for module in self.modules)
        return tuple(entries)

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "label": self.label,
            "surface": self.surface,
            "job": self.job,
            "shallow_model_outcome": self.shallow_model_outcome,
            "shared_modules": list(self.modules),
            "directory": self.directory,
            "reader_overlay": [item.to_json() for item in self.reader_overlay],
            "load_set": list(self.load_set),
            "source_span": self.span.to_json(),
        }


@dataclass(frozen=True)
class BaselineItem:
    """One Annex B assumption, exclusion, or notation entry.

    ``polarity`` is the field that makes the record usable. Annex B lists
    what a reader knows and what a reader expressly does not know in the
    same shape, and §0.3.3 turns the difference into an obligation: an item
    that is not assumed must reach the reader through the §2.3 ladder. A
    record without polarity cannot tell a checker which of the two it holds.

    ``conditional`` marks a grant that depends on a declaration, such as the
    §0.3.4 host-language supplement, which exists only once a carrier names
    a host adapter.
    """

    category: str
    text: str
    span: SourceSpan
    polarity: str = "assumed"
    kind: str = "concept"
    conditional: bool = False

    @property
    def is_assumed(self) -> bool:
        return self.polarity == "assumed"

    def to_json(self) -> dict[str, object]:
        return {
            "category": self.category,
            "text": self.text,
            "polarity": self.polarity,
            "kind": self.kind,
            "conditional": self.conditional,
            "source_span": self.span.to_json(),
        }


@dataclass(frozen=True)
class PhraseListEntry:
    """One generated linter input drawn from the authoritative Markdown."""

    id: str
    rule: str
    kind: str
    pattern: str
    message: str
    replacement: str
    ignore_case: bool
    span: SourceSpan

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "rule": self.rule,
            "kind": self.kind,
            "pattern": self.pattern,
            "message": self.message,
            "replacement": self.replacement,
            "ignore_case": self.ignore_case,
            "source_span": self.span.to_json(),
        }


@dataclass(frozen=True)
class Specification:
    """The parsed, resolved, and validated specification model."""

    version: str
    status: str
    rules: tuple[Rule, ...]
    profiles: tuple[ProfileRecord, ...]
    skeletons: tuple[Skeleton, ...]
    glossary: tuple[GlossaryEntry, ...]
    baseline: tuple[BaselineItem, ...]
    examples: tuple[Example, ...]
    phrase_lists: tuple[PhraseListEntry, ...]
    source_hashes: dict[str, str]

    def rule(self, number: str) -> Rule | None:
        for candidate in self.rules:
            if candidate.number == number:
                return candidate
        return None

    def profile(self, profile_id: str) -> ProfileRecord | None:
        for candidate in self.profiles:
            if candidate.id == profile_id:
                return candidate
        return None

    def skeleton(self, profile_id: str) -> Skeleton | None:
        for candidate in self.skeletons:
            if candidate.profile == profile_id:
                return candidate
        return None

    def glossary_entry(self, term: str) -> GlossaryEntry | None:
        needle = term.casefold()
        for candidate in self.glossary:
            if candidate.term.casefold() == needle:
                return candidate
        return None

    def envelope(self, profile_id: str) -> tuple[Rule, ...]:
        """Every active rule available to ``profile_id``.

        The envelope is the widest safe view. A narrower set requires an
        agent-supplied applicability decision, never a navigation facet.
        """
        return tuple(
            rule
            for rule in self.rules
            if rule.is_active and rule.applies_to_profile(profile_id)
        )


def content_hash(text: str) -> str:
    """Return the ``sha256:`` digest this repository uses for source pinning."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def dedupe(values: Iterable[str]) -> tuple[str, ...]:
    """Preserve first-seen order while removing repeats."""
    seen: list[str] = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return tuple(seen)


__all__ = [
    "BaselineItem",
    "Example",
    "GlossaryEntry",
    "Merge",
    "MutationPolicy",
    "Navigation",
    "PhraseListEntry",
    "ProfileRecord",
    "Relation",
    "Rule",
    "RuleExample",
    "Skeleton",
    "Slot",
    "SourceSpan",
    "Specification",
    "content_hash",
    "dedupe",
    "field",
    "replace",
]

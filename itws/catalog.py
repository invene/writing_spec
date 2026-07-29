"""Agent-controlled navigation over the committed ITWS catalog.

The catalog loads the generated artifacts from a repository checkout. Every
operation is small enough to combine inside a short script, and every
operation is available both as a Python function and through
``tools/itws_retrieve.py``.

The catalog never infers what a governed passage contains. It accepts a
construct, chunk type, layer, or slot only as an agent-supplied facet, and it
returns the full profile envelope before any narrower result (§1.6.1).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from itws.jsonio import dumps, read_json, read_jsonl
from itws.vocab import (
    CHUNK_TYPES,
    CONSTRUCTS,
    CONTEXT_SCOPES,
    LAYERS,
    PROFILE_IDS,
    RELATION_TYPES,
    REWRITE_GUIDANCE,
    TARGETS,
    rule_sort_key,
)

GENERATED_RELATIVE = Path("spec/generated/agent")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")

#: Facets ``filter_rules`` accepts. Every one is agent-supplied.
FACETS = {
    "target": TARGETS,
    "constructs": CONSTRUCTS,
    "chunk_types": CHUNK_TYPES,
    "layers": LAYERS,
    "context_scope": CONTEXT_SCOPES,
    "rewrite_guidance": REWRITE_GUIDANCE,
    "class": ("mandatory", "recommended", "permitted"),
    "machine_checkable": ("yes", "partial", "no"),
    "part": tuple(str(number) for number in range(2, 9)),
    "slots": (),
}


class CatalogError(RuntimeError):
    """The catalog is missing, stale, or inconsistent."""


@dataclass(frozen=True)
class Match:
    """One search result with its reasons and its raw score.

    A score orders results for convenience. It is not applicability,
    correctness, or repair priority.
    """

    rule_id: str
    score: float
    reasons: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "score": round(self.score, 4),
            "match_reasons": list(self.reasons),
        }


@dataclass
class RuleTrail:
    """An optional record of one agent's navigation path.

    Logging is never required for an ordinary lookup. An agent that wants to
    revisit or defend a decision writes the trail as JSON Lines.
    """

    entries: list[dict[str, object]] = field(default_factory=list)

    def record(
        self,
        operation: str,
        request: dict[str, object],
        selected: Sequence[str],
        note: str = "",
    ) -> None:
        self.entries.append(
            {
                "operation": operation,
                "request": request,
                "selected": list(selected),
                "note": note,
            }
        )

    def to_jsonl(self) -> str:
        return "".join(
            json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n"
            for entry in self.entries
        )

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_jsonl(), encoding="utf-8")


class Catalog:
    """Read-only access to one compiled ITWS catalog."""

    def __init__(self, root: Path) -> None:
        self.root = root
        if not root.is_dir():
            raise CatalogError(
                f"no generated catalog at {root}; run "
                "`python3 tools/itws_compile.py` first"
            )
        self.manifest = read_json(root / "manifest.json")
        self.rules: dict[str, dict] = {}
        for record in read_jsonl(root / "rules.jsonl"):
            self.rules[record["id"]] = record
        self.rule_graph = read_json(root / "rule-graph.json")
        self.glossary = {
            entry["term"]: entry
            for entry in read_json(root / "glossary.json")["entries"]
        }
        self.reader_baseline = read_json(root / "reader-baseline.json")
        self.examples = list(read_jsonl(root / "examples.jsonl"))
        self.phrase_lists = read_json(root / "phrase-lists.json")["entries"]
        self._profiles: dict[str, dict] = {}
        self._skeletons: dict[str, dict] = {}

    # -- construction -----------------------------------------------------

    @classmethod
    def from_repo(cls, repo: Path | str = ".") -> "Catalog":
        """Load the catalog committed inside a repository checkout."""
        return cls(Path(repo) / GENERATED_RELATIVE)

    @property
    def version(self) -> str:
        return str(self.manifest["itws_version"])

    # -- profile ----------------------------------------------------------

    def get_profile(self, profile: str) -> dict:
        """Return one profile's job, overlay, tier, load set, and envelope."""
        if profile not in PROFILE_IDS:
            raise CatalogError(f"unknown profile ID: {profile}")
        if profile not in self._profiles:
            self._profiles[profile] = read_json(
                self.root / "profiles" / f"{profile}.json"
            )
        return self._profiles[profile]

    def envelope(self, profile: str) -> list[dict]:
        """Every active rule available to ``profile``, in canonical order.

        This is the widest safe view. Return it before any narrower result.
        """
        data = self.get_profile(profile)["envelope"]
        ids = list(data["universal"]) + list(data["profile_scoped"])
        return [self.rules[number] for number in sorted(ids, key=rule_sort_key)]

    def get_skeleton(self, profile: str) -> dict:
        """Return one profile's ordered slots, renames, merges, and policies."""
        if profile not in PROFILE_IDS:
            raise CatalogError(f"unknown profile ID: {profile}")
        if profile not in self._skeletons:
            self._skeletons[profile] = read_json(
                self.root / "skeletons" / f"{profile}.json"
            )
        return self._skeletons[profile]

    def get_reader_baseline(self, profile: str | None = None) -> dict:
        """Return the shared baseline and, when asked, one profile overlay."""
        payload = {"shared": self.reader_baseline["shared"]}
        if profile:
            payload["profile"] = profile
            payload["overlay"] = self.reader_baseline["profile_overlays"].get(
                profile, []
            )
        return payload

    # -- rules ------------------------------------------------------------

    def get_rule(self, rule_id: str) -> dict:
        """Return one rule atom by permanent ID."""
        if rule_id not in self.rules:
            raise CatalogError(f"unknown rule ID: {rule_id}")
        return self.rules[rule_id]

    def get_section(self, section: str) -> dict:
        """Return every rule of one numbered section, with its source spans."""
        members = [
            rule
            for rule in self.rules.values()
            if rule["id"].rsplit(".", 1)[0] == section
        ]
        if not members:
            raise CatalogError(f"no rules found in section {section}")
        members.sort(key=lambda rule: rule_sort_key(rule["id"]))
        return {
            "section": section,
            "rule_count": len(members),
            "source_files": sorted(
                {rule["source_span"]["path"] for rule in members}
            ),
            "rules": members,
        }

    def search_rules(
        self,
        query: str,
        *,
        profile: str | None = None,
        limit: int = 20,
    ) -> list[Match]:
        """Literal and lexical search over the profile envelope.

        Ranking orders results for convenience only. Every result carries its
        match reasons and its raw score so an agent can judge the ordering.
        """
        pool = self.envelope(profile) if profile else list(self.rules.values())
        terms = [term.casefold() for term in WORD_RE.findall(query)]
        if not terms:
            return []
        matches: list[Match] = []
        for rule in pool:
            reasons: list[str] = []
            score = 0.0
            fields = {
                "id": rule["id"],
                "name": rule["name"],
                "statement": rule["statement"],
                "rationale": rule["rationale"],
                "constructs": " ".join(rule["navigation"]["constructs"]),
                "chunk_types": " ".join(rule["navigation"]["chunk_types"]),
                "slots": " ".join(rule["navigation"]["slots"]),
                "cross_references": rule["cross_references"],
            }
            weights = {
                "id": 6.0,
                "name": 4.0,
                "statement": 3.0,
                "constructs": 2.5,
                "slots": 2.0,
                "chunk_types": 1.5,
                "rationale": 1.0,
                "cross_references": 0.5,
            }
            if query.strip() == rule["id"]:
                score += 20.0
                reasons.append("exact rule ID")
            for name, text in fields.items():
                lowered = text.casefold()
                hits = sum(1 for term in terms if term in lowered)
                if hits:
                    score += weights[name] * hits / len(terms)
                    reasons.append(f"{name}: {hits}/{len(terms)} terms")
            if score:
                matches.append(
                    Match(rule_id=rule["id"], score=score, reasons=tuple(reasons))
                )
        matches.sort(key=lambda match: (-match.score, rule_sort_key(match.rule_id)))
        return matches[:limit]

    def filter_rules(
        self, *, profile: str | None = None, **facets: Iterable[str] | str
    ) -> list[dict]:
        """Apply agent-supplied facets to the envelope.

        A facet narrows a search result. A facet never narrows the profile
        envelope itself (§1.6.1): call :meth:`envelope` for that.
        """
        unknown = sorted(set(facets) - set(FACETS))
        if unknown:
            raise CatalogError(f"unknown facet(s): {', '.join(unknown)}")
        pool = self.envelope(profile) if profile else list(self.rules.values())
        for name, wanted in facets.items():
            values = (wanted,) if isinstance(wanted, str) else tuple(wanted)
            allowed = FACETS[name]
            if allowed:
                bad = [value for value in values if value not in allowed]
                if bad:
                    raise CatalogError(
                        f"facet {name!r} has unknown value(s): {', '.join(bad)}"
                    )
            pool = [rule for rule in pool if _facet_matches(rule, name, values)]
        pool.sort(key=lambda rule: rule_sort_key(rule["id"]))
        return pool

    def expand_relations(
        self,
        seeds: Sequence[str],
        *,
        depth: int = 1,
        types: Sequence[str] | None = None,
        profile: str | None = None,
    ) -> dict:
        """Traverse typed rule edges from agent-selected seeds."""
        wanted = tuple(types) if types else RELATION_TYPES
        unknown = [value for value in wanted if value not in RELATION_TYPES]
        if unknown:
            raise CatalogError(f"unknown relation type(s): {', '.join(unknown)}")
        available = (
            {rule["id"] for rule in self.envelope(profile)} if profile else set(self.rules)
        )
        for seed in seeds:
            if seed not in self.rules:
                raise CatalogError(f"unknown rule ID: {seed}")

        adjacency: dict[str, list[dict]] = {}
        for edge in self.rule_graph["edges"]:
            adjacency.setdefault(edge["source"], []).append(edge)
            if edge["type"] != "exemplified-by":
                adjacency.setdefault(edge["target"], []).append(
                    {
                        "source": edge["target"],
                        "type": f"inverse:{edge['type']}",
                        "target": edge["source"],
                        "note": edge["note"],
                    }
                )

        reached: dict[str, int] = {seed: 0 for seed in seeds}
        used: list[dict] = []
        frontier = list(seeds)
        for level in range(1, depth + 1):
            next_frontier: list[str] = []
            for node in frontier:
                for edge in adjacency.get(node, []):
                    base_type = edge["type"].removeprefix("inverse:")
                    if base_type not in wanted:
                        continue
                    used.append({**edge, "depth": level})
                    target = edge["target"]
                    if target.startswith("D."):
                        continue
                    if target in reached or target not in available:
                        continue
                    reached[target] = level
                    next_frontier.append(target)
            frontier = next_frontier
            if not frontier:
                break

        return {
            "seeds": list(seeds),
            "depth": depth,
            "relation_types": list(wanted),
            "reached": [
                {"rule_id": number, "depth": level}
                for number, level in sorted(
                    reached.items(), key=lambda item: (item[1], rule_sort_key(item[0]))
                )
            ],
            "edges": used,
            "rules": [
                self.rules[number]
                for number in sorted(reached, key=rule_sort_key)
            ],
        }

    # -- supporting material ----------------------------------------------

    def get_examples(
        self,
        *,
        rule: str | None = None,
        profile: str | None = None,
        origin: str | None = None,
        tags: Sequence[str] = (),
    ) -> list[dict]:
        """Return rule examples and Annex D examples by agent-supplied keys."""
        results = []
        for example in self.examples:
            if rule and rule not in example["rules_applied"]:
                continue
            if profile and example["profile"] != profile:
                continue
            if origin and example["origin"] != origin:
                continue
            if tags:
                available = set(example["chunk_types"]) | set(example["constructs"]) | set(
                    example["repair_operators"]
                )
                if not set(tags) & available:
                    continue
            results.append(example)
        return results

    def get_glossary_entry(self, term: str) -> dict:
        """Return one term with its resolved prerequisite chain."""
        entry = self.glossary.get(term)
        if entry is None:
            for name, candidate in self.glossary.items():
                if name.casefold() == term.casefold():
                    entry = candidate
                    break
        if entry is None:
            raise CatalogError(f"unknown glossary term: {term}")
        chain: list[str] = []
        seen: set[str] = set()

        def walk(name: str) -> None:
            if name in seen:
                return
            seen.add(name)
            for prerequisite in self.glossary.get(name, {}).get("prerequisites", []):
                walk(prerequisite)
            if name != entry["term"]:
                chain.append(name)

        walk(entry["term"])
        return {
            "entry": entry,
            "prerequisite_chain": chain,
            "assumed_prerequisites": entry["assumed_prerequisites"],
        }

    def get_phrase_lists(self, rule: str | None = None) -> list[dict]:
        """Return the generated linter inputs, optionally for one rule."""
        if rule is None:
            return list(self.phrase_lists)
        return [entry for entry in self.phrase_lists if entry["rule"] == rule]

    def assemble_context(
        self,
        *,
        profile: str,
        rules: Sequence[str] = (),
        sections: Sequence[str] = (),
        terms: Sequence[str] = (),
        examples: Sequence[str] = (),
        include_skeleton: bool = True,
        include_baseline: bool = False,
        note: str = "",
    ) -> dict:
        """Return exactly the records an agent selected for one step.

        The packet always carries the full envelope by reference, so a
        narrowed selection never hides an applicable rule.
        """
        profile_record = self.get_profile(profile)
        packet: dict[str, object] = {
            "itws_version": self.version,
            "profile": profile,
            "note": note,
            "envelope_reference": {
                "rule_count": profile_record["envelope"]["rule_count"],
                "artifact": f"spec/generated/agent/profiles/{profile}.json",
            },
            "selected_rules": [self.get_rule(number) for number in rules],
            "selected_sections": [self.get_section(name) for name in sections],
            "selected_terms": [self.get_glossary_entry(term) for term in terms],
            "selected_examples": [
                example for example in self.examples if example["id"] in set(examples)
            ],
        }
        if include_skeleton:
            packet["skeleton"] = self.get_skeleton(profile)
        if include_baseline:
            packet["reader_baseline"] = self.get_reader_baseline(profile)
        return packet

    def to_json(self, payload: object) -> str:
        return dumps(payload)


def _facet_matches(rule: dict, name: str, values: tuple[str, ...]) -> bool:
    navigation = rule["navigation"]
    if name == "target":
        return navigation["target"] in values
    if name == "layers":
        return navigation["layers"] in values
    if name == "context_scope":
        return navigation["context_scope"] in values
    if name == "rewrite_guidance":
        return navigation["rewrite_guidance"] in values
    if name in {"constructs", "chunk_types", "slots"}:
        return bool(set(navigation[name]) & set(values))
    if name == "class":
        return rule["class"] in values
    if name == "machine_checkable":
        return rule["machine_checkable"] in values
    if name == "part":
        return rule["id"].split(".", 1)[0] in values
    return False

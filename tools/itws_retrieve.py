#!/usr/bin/env python3
"""Navigate the compiled ITWS catalog from the command line.

Every action prints a compact text form by default and JSON with ``--json``.
The same operations are importable::

    from itws.catalog import Catalog
    catalog = Catalog.from_repo(".")
    profile = catalog.get_profile("design-rfc")

The catalog returns the full profile envelope before any narrower result. A
facet is an agent-supplied search aid; it never narrows applicability (§1.6.1).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from itws.catalog import Catalog, CatalogError, RuleTrail
from itws.jsonio import dumps
from itws.vocab import PROFILE_IDS, RELATION_TYPES


def parse_args() -> argparse.Namespace:
    # Shared options are declared on a parent parser so they work both before
    # and after the action name.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", type=Path, default=Path("."))
    common.add_argument("--json", action="store_true", help="print JSON")
    common.add_argument(
        "--trail",
        type=Path,
        help="append this lookup to a JSON Lines rule trail",
    )

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
    )
    actions = parser.add_subparsers(dest="action", required=True)

    def action(name: str, help_text: str) -> argparse.ArgumentParser:
        return actions.add_parser(name, help=help_text, parents=[common])

    profile = action("get-profile", "one profile's full envelope")
    profile.add_argument("profile", choices=PROFILE_IDS)

    rule = action("get-rule", "one rule atom by permanent ID")
    rule.add_argument("rule_id")

    search = action("search-rules", "literal and lexical search")
    search.add_argument("query")
    search.add_argument("--profile", choices=PROFILE_IDS)
    search.add_argument("--limit", type=int, default=20)

    filters = action("filter-rules", "apply agent-supplied facets")
    filters.add_argument("--profile", choices=PROFILE_IDS)
    filters.add_argument("--target")
    filters.add_argument("--constructs")
    filters.add_argument("--chunk-types", dest="chunk_types")
    filters.add_argument("--slots")
    filters.add_argument("--layers")
    filters.add_argument("--context-scope", dest="context_scope")
    filters.add_argument("--rewrite-guidance", dest="rewrite_guidance")
    filters.add_argument("--class", dest="rule_class")
    filters.add_argument("--machine-checkable", dest="machine_checkable")
    filters.add_argument("--part")

    relations = action("expand-relations", "traverse typed edges")
    relations.add_argument("seeds", nargs="+")
    relations.add_argument("--depth", type=int, default=1)
    relations.add_argument("--profile", choices=PROFILE_IDS)
    relations.add_argument("--types", nargs="*", choices=RELATION_TYPES)

    section = action("get-section", "one numbered section")
    section.add_argument("section")

    examples = action("get-examples", "rule and Annex D examples")
    examples.add_argument("--rule")
    examples.add_argument("--profile", choices=PROFILE_IDS)
    examples.add_argument("--origin", choices=("rule", "annex-d"))
    examples.add_argument("--tags", nargs="*", default=[])

    glossary = action("get-glossary-entry", "one term and its chain")
    glossary.add_argument("term")

    skeleton = action("get-skeleton", "one profile's skeleton")
    skeleton.add_argument("profile", choices=PROFILE_IDS)

    baseline = action("get-reader-baseline", "Annex B plus overlay")
    baseline.add_argument("--profile", choices=PROFILE_IDS)

    phrases = action("get-phrase-lists", "generated linter inputs")
    phrases.add_argument("--rule")

    packet = action("assemble-context", "one reasoning packet")
    packet.add_argument("profile", choices=PROFILE_IDS)
    packet.add_argument("--rules", nargs="*", default=[])
    packet.add_argument("--sections", nargs="*", default=[])
    packet.add_argument("--terms", nargs="*", default=[])
    packet.add_argument("--examples", nargs="*", default=[])
    packet.add_argument("--baseline", action="store_true")
    packet.add_argument("--note", default="")

    return parser.parse_args()


def _split(value: str | None) -> list[str]:
    return [item.strip() for item in value.split(",")] if value else []


def _text_profile(payload: dict) -> str:
    envelope = payload["envelope"]
    lines = [
        f"{payload['id']} — {payload['label']}",
        f"  minimum tier : {payload['minimum_tier']}",
        f"  job          : {payload['job']}",
        f"  reader test  : {payload['reader_test_outcome']}",
        f"  owner focus  : {payload['owner_review_focus']}",
        f"  modules      : {', '.join(payload['shared_modules']) or 'none'}",
        f"  envelope     : {envelope['rule_count']} active rules "
        f"({len(envelope['universal'])} universal, "
        f"{len(envelope['profile_scoped'])} profile-scoped)",
        "  load set:",
    ]
    lines.extend(f"    {item}" for item in payload["load_set"])
    lines.append("  rules by self-check pass:")
    for name, ids in envelope["by_checklist_pass"].items():
        lines.append(f"    {name}: {len(ids)}")
    return "\n".join(lines)


def _text_rule(rule: dict) -> str:
    navigation = rule["navigation"]
    return "\n".join(
        [
            f"Rule {rule['id']} — {rule['name']}",
            f"  class        : {rule['class']} ({rule['severity']})",
            f"  machine      : {rule['machine_checkable']}",
            f"  profiles     : "
            + (", ".join(rule["profiles"]) if rule["profiles"] else "all profiles"),
            f"  source file  : {rule['source_span']['path']}:"
            f"{rule['source_span']['start_line']}",
            f"  target       : {navigation['target']}",
            f"  constructs   : {', '.join(navigation['constructs'])}",
            f"  chunks/slots : {', '.join(navigation['chunk_types'])} / "
            f"{', '.join(navigation['slots'])}",
            f"  layer/context: {navigation['layers']} / {navigation['context_scope']}",
            f"  rewrite      : {navigation['rewrite_guidance']}",
            f"  reads/writes : {', '.join(navigation['reads'])} / "
            f"{', '.join(navigation['writes'])}",
            f"  precedence   : layer {rule['precedence_layer']} (§1.4)",
            "",
            "  " + rule["statement"].replace("\n", "\n  "),
            "",
            f"  Rationale: {rule['rationale']}",
            f"  Compliant: {rule['example']['compliant']}",
            f"  Non-compliant: {rule['example']['non_compliant']}",
            "  Relations: "
            + (
                "; ".join(
                    f"{edge['type']} {edge['target']}" for edge in rule["relations"]
                )
                or "none"
            ),
        ]
    )


def main() -> int:
    args = parse_args()
    try:
        catalog = Catalog.from_repo(args.repo)
    except CatalogError as error:
        print(error, file=sys.stderr)
        return 2

    trail = RuleTrail()
    payload: object
    text: str

    try:
        if args.action == "get-profile":
            payload = catalog.get_profile(args.profile)
            text = _text_profile(payload)
            trail.record("get_profile", {"profile": args.profile}, [args.profile])
        elif args.action == "get-rule":
            payload = catalog.get_rule(args.rule_id)
            text = _text_rule(payload)
            trail.record("get_rule", {"rule_id": args.rule_id}, [args.rule_id])
        elif args.action == "search-rules":
            matches = catalog.search_rules(
                args.query, profile=args.profile, limit=args.limit
            )
            payload = {
                "query": args.query,
                "profile": args.profile,
                "envelope_note": (
                    "ranking orders results only; the full envelope remains "
                    "applicable"
                ),
                "matches": [match.to_json() for match in matches],
            }
            text = "\n".join(
                f"{match.score:7.2f}  {match.rule_id:8}  "
                f"{catalog.get_rule(match.rule_id)['name']}"
                f"   [{'; '.join(match.reasons)}]"
                for match in matches
            ) or "no match"
            trail.record(
                "search_rules",
                {"query": args.query, "profile": args.profile},
                [match.rule_id for match in matches],
            )
        elif args.action == "filter-rules":
            facets: dict[str, object] = {}
            for name, value in (
                ("target", args.target),
                ("constructs", args.constructs),
                ("chunk_types", args.chunk_types),
                ("slots", args.slots),
                ("layers", args.layers),
                ("context_scope", args.context_scope),
                ("rewrite_guidance", args.rewrite_guidance),
                ("class", args.rule_class),
                ("machine_checkable", args.machine_checkable),
                ("part", args.part),
            ):
                if value:
                    facets[name] = _split(value)
            rules = catalog.filter_rules(profile=args.profile, **facets)
            payload = {
                "profile": args.profile,
                "facets": facets,
                "rule_count": len(rules),
                "rules": rules,
            }
            text = "\n".join(
                f"{rule['id']:8}  {rule['class']:11}  {rule['name']}"
                for rule in rules
            ) or "no rule matches these facets"
            trail.record(
                "filter_rules", facets, [rule["id"] for rule in rules]
            )
        elif args.action == "expand-relations":
            payload = catalog.expand_relations(
                args.seeds,
                depth=args.depth,
                types=args.types,
                profile=args.profile,
            )
            text = "\n".join(
                f"depth {item['depth']}  {item['rule_id']:8}  "
                f"{catalog.get_rule(item['rule_id'])['name']}"
                for item in payload["reached"]
            )
            trail.record(
                "expand_relations",
                {"seeds": args.seeds, "depth": args.depth},
                [item["rule_id"] for item in payload["reached"]],
            )
        elif args.action == "get-section":
            payload = catalog.get_section(args.section)
            text = "\n".join(
                [f"§{args.section} — {payload['rule_count']} rules"]
                + [f"  in {name}" for name in payload["source_files"]]
                + [
                    f"  {rule['id']:8}  {rule['name']}"
                    for rule in payload["rules"]
                ]
            )
            trail.record("get_section", {"section": args.section}, [args.section])
        elif args.action == "get-examples":
            found = catalog.get_examples(
                rule=args.rule,
                profile=args.profile,
                origin=args.origin,
                tags=args.tags,
            )
            payload = {"count": len(found), "examples": found}
            text = "\n".join(
                f"{example['id']:14}  {example['profile'] or '-':18}  "
                f"{example['title']}"
                for example in found
            ) or "no example matches"
            trail.record(
                "get_examples",
                {"rule": args.rule, "profile": args.profile},
                [example["id"] for example in found],
            )
        elif args.action == "get-glossary-entry":
            payload = catalog.get_glossary_entry(args.term)
            entry = payload["entry"]
            text = "\n".join(
                [
                    f"{entry['term']} ({entry['part_of_speech']}) — {entry['status']}",
                    f"  definition   : {entry['definition']}",
                    f"  example      : {entry['approved_example']}",
                    f"  do not use   : {entry['do_not_use']}",
                    f"  prerequisites: "
                    + (" → ".join(payload["prerequisite_chain"]) or "none"),
                    f"  assumed      : "
                    + (", ".join(payload["assumed_prerequisites"]) or "none"),
                    f"  profiles     : {', '.join(entry['profiles'])}",
                ]
            )
            trail.record("get_glossary_entry", {"term": args.term}, [args.term])
        elif args.action == "get-skeleton":
            payload = catalog.get_skeleton(args.profile)
            lines = [f"{args.profile} skeleton (Annex {payload['annex_section']})"]
            for slot in payload["slots"]:
                marker = "required" if slot["required"] else "optional"
                indent = "    " if slot["parent"] else "  "
                renames = (
                    f"  [renames: {', '.join(slot['renames'])}]"
                    if slot["renames"]
                    else ""
                )
                lines.append(f"{indent}{slot['name']} ({marker}){renames}")
            for merge in payload["merges"]:
                lines.append(
                    f"  merge: {' + '.join(merge['parts'])} -> {merge['combined']}"
                )
            for policy in payload["mutation_policies"]:
                lines.append(
                    f"  mutation policy: {policy['scope']} is {policy['policy']} "
                    f"(rule {policy['rule']})"
                )
            text = "\n".join(lines)
            trail.record("get_skeleton", {"profile": args.profile}, [args.profile])
        elif args.action == "get-reader-baseline":
            payload = catalog.get_reader_baseline(args.profile)
            lines = [f"shared baseline: {len(payload['shared'])} items"]
            if args.profile:
                lines.append(f"{args.profile} overlay:")
                lines.extend(f"  - {item}" for item in payload["overlay"])
            text = "\n".join(lines)
            trail.record(
                "get_reader_baseline", {"profile": args.profile}, [args.profile or ""]
            )
        elif args.action == "get-phrase-lists":
            entries = catalog.get_phrase_lists(args.rule)
            payload = {"count": len(entries), "entries": entries}
            text = "\n".join(
                f"{entry['id']:34}  {entry['kind']:8}  {entry['pattern']}"
                for entry in entries
            ) or "no phrase-list entry"
            trail.record(
                "get_phrase_lists", {"rule": args.rule}, [entry["id"] for entry in entries]
            )
        else:  # assemble-context
            payload = catalog.assemble_context(
                profile=args.profile,
                rules=args.rules,
                sections=args.sections,
                terms=args.terms,
                examples=args.examples,
                include_baseline=args.baseline,
                note=args.note,
            )
            text = (
                f"context packet for {args.profile}: "
                f"{len(payload['selected_rules'])} rules, "
                f"{len(payload['selected_sections'])} sections, "
                f"{len(payload['selected_terms'])} terms, "
                f"{len(payload['selected_examples'])} examples; "
                f"full envelope of {payload['envelope_reference']['rule_count']} "
                "rules remains applicable"
            )
            trail.record(
                "assemble_context", {"profile": args.profile}, list(args.rules)
            )
    except CatalogError as error:
        print(error, file=sys.stderr)
        return 1

    if args.trail:
        existing = (
            args.trail.read_text(encoding="utf-8") if args.trail.exists() else ""
        )
        args.trail.parent.mkdir(parents=True, exist_ok=True)
        args.trail.write_text(existing + trail.to_jsonl(), encoding="utf-8")

    print(dumps(payload) if args.json else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

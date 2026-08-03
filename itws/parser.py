"""One conservative line scanner for the authoritative ITWS Markdown.

Every generator and checker reads the model this module produces. The scanner
understands only the Markdown forms that ITWS uses, and it keeps exact line
ranges for every extracted item so a tool can point a reader back at the
source.

The scanner never infers meaning. It reports the forms an author wrote and
fails loudly on a form it does not recognize.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from itws.model import (
    BaselineItem,
    Example,
    GlossaryEntry,
    Merge,
    MutationPolicy,
    Navigation,
    PhraseListEntry,
    ProfileRecord,
    Relation,
    Rule,
    RuleExample,
    Skeleton,
    Slot,
    SourceSpan,
    Specification,
    content_hash,
    dedupe,
)
from itws.vocab import (
    AUTHORED_RELATION_TYPES,
    CHUNK_TYPES,
    CONSTRUCTS,
    CONTEXT_SCOPES,
    LAYERS,
    MACHINE_CHECKABILITY,
    PROFILE_FAMILIES,
    PROFILE_IDS,
    PROFILE_LABELS,
    RESOURCES,
    REWRITE_GUIDANCE,
    RULE_CLASSES,
    profile_families,
    profile_surface,
    rule_sort_key,
)

OVERLAY_DIRNAME = "overlays"
SHARED_DIRNAME = "shared"
PROFILE_RULES_FILENAME = "rules.md"

RULE_RE = re.compile(r"^#### Rule (?P<number>\d+\.\d+\.\d+) — (?P<name>.+)$")
METADATA_RE = re.compile(
    r"^\*\*Class:\*\* (?P<class>mandatory|recommended|permitted)"
    r" · \*\*Machine-checkable:\*\* (?P<machine>yes|partial|no)"
    r" · \*\*Source:\*\* (?P<source>.+)$"
)
PROFILES_RE = re.compile(r"^\*\*Profiles:\*\* (?P<profiles>.+)$")
CONSTRUCTS_RE = re.compile(r"^\*\*Constructs:\*\* (?P<constructs>.+)$")
NAVIGATION_RE = re.compile(r"^\*\*Navigation:\*\* (?P<navigation>.+)$")
RESOURCES_RE = re.compile(r"^\*\*Resources:\*\* (?P<resources>.+)$")
RELATIONS_RE = re.compile(r"^\*\*Relations:\*\* (?P<relations>.+)$")
STATUS_RE = re.compile(r"^\*\*Status:\*\* (?P<status>active|deprecated)(?P<detail>.*)$")
DEPRECATED_DETAIL_RE = re.compile(
    r"^ since (?P<version>\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?); "
    r"replacement (?P<replacement>\d+\.\d+\.\d+|none)$"
)
VERSION_RE = re.compile(
    r"^\*\*Version:\*\* (?P<version>[^ ·]+) · \*\*Status:\*\* (?P<status>.+)$"
)
RATIONALE_RE = re.compile(r"^\*\*Rationale:\*\* (?P<text>.+)$")
COMPLIANT_RE = re.compile(r"^\*\*Compliant:\*\*(?P<text>.*)$")
NON_COMPLIANT_RE = re.compile(r"^\*\*Non-compliant:\*\*(?P<text>.*)$")
XREF_RE = re.compile(r"^\*\*Cross-references:\*\* (?P<text>.+)$")

PHRASE_LIST_RE = re.compile(
    r"^\*\*Phrase list (?P<rule>\d+\.\d+\.\d+) — (?P<label>[^:(]+?)"
    r" \((?P<kind>word|phrase|pattern|opener)(?P<flags>[^)]*)\):\*\* (?P<items>.+)$"
)
PHRASE_ITEM_RE = re.compile(
    r'"(?P<literal>[^"]+)"'
    r'(?: → "(?P<replacement>[^"]*)")?'
    r"(?: \((?P<note>[^)]*)\))?"
)

RULE_REFERENCE_RE = re.compile(r"\b(\d+\.\d+\.\d+)\b")

FIELD_SEPARATOR = " · "

# --- Skeleton syntax -------------------------------------------------------

SKELETON_TITLE_RE = re.compile(
    r"^# Annex E §(?P<section>E\.\d+) — `(?P<profile>[a-z-]+)` skeleton$"
)
SLOT_RE = re.compile(
    r"^(?P<indent> *)(?P<name>[^(]*?)\s+\((?P<status>required[^)]*|optional[^)]*)\)"
    r"(?P<description>.*)$"
)
RENAMES_RE = re.compile(r"^Permitted renames: (?P<body>.+)$")
MERGES_RE = re.compile(r"^(?:Use .*?\. )?Permitted merges: (?P<body>.+)$")
RENAME_PAIR_RE = re.compile(r"`(?P<from>[^`]+)` → (?P<to>[^;.]+)")
MERGE_PAIR_RE = re.compile(r"`(?P<a>[^`]+)` \+ `(?P<b>[^`]+)` → `(?P<combined>[^`]+)`")
MUTATION_RE = re.compile(
    r"^\*\*Mutation policy:\*\* (?P<scope>[^·]+) · (?P<policy>[a-z-]+)"
    r" · rule (?P<rule>\d+\.\d+\.\d+) · (?P<note>.+)$"
)

# --- Section map syntax (§E.0.2) -------------------------------------------

SECTION_MAP_ENTRY_RE = re.compile(
    r'^(?P<heading>".+?"|\S.*?)\s*->\s*(?P<slot>\S.*?)\s*$'
)

# --- Glossary syntax -------------------------------------------------------

GLOSSARY_HEADER_RE = re.compile(
    r"^### (?P<term>.+?) \((?P<pos>[a-z ]+)\) — (?P<status>admitted|deprecated)$"
)
GLOSSARY_FIELD_RE = re.compile(r"^(?P<key>[A-Za-z /]+?):\s{2,}(?P<value>.*)$")

# --- Annex D syntax --------------------------------------------------------

EXAMPLE_HEADER_RE = re.compile(r"^### Example (?P<id>D\.\d+) — (?P<title>.+)$")
EXAMPLE_FIELD_RE = re.compile(r"^(?P<key>[A-Za-z ]+): (?P<value>.+)$")

# --- Overlay README syntax -------------------------------------------------

OVERLAY_VERSION_RE = re.compile(
    r"^\*\*ITWS version:\*\* (?P<version>\S+)$",
    re.MULTILINE,
)
JOB_RE = re.compile(r"^\*\*Job:\*\* (?P<job>.+)$")
SHALLOW_MODEL_OUTCOME_RE = re.compile(
    r"^The scan path shall support this outcome \(§4\.12\): "
    r"(?P<outcome>.+)$"
)
MODULE_LINK_RE = re.compile(r"\.\./shared/(?P<module>[a-z-]+)\.md")


class SpecError(ValueError):
    """A defect in the authoritative Markdown, reported with its location."""


@dataclass
class _RawBlock:
    lines: list[str]
    start: int


def _fail(path: Path, line_number: int, message: str) -> "SpecError":
    return SpecError(f"{path}:{line_number}: {message}")


def _split_fields(raw: str) -> dict[str, str]:
    """Split ``key: value · key: value`` into a mapping, preserving order."""
    fields: dict[str, str] = {}
    for chunk in raw.split(FIELD_SEPARATOR):
        key, separator, value = chunk.partition(":")
        if not separator:
            raise ValueError(f"field {chunk!r} has no 'key: value' form")
        key = key.strip()
        if key in fields:
            raise ValueError(f"duplicate field {key!r}")
        fields[key] = value.strip()
    return fields


def _split_list(raw: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in raw.split(",") if item.strip())


def _check_closed(
    path: Path, line_number: int, field: str, values: tuple[str, ...], allowed
) -> None:
    unknown = [value for value in values if value not in allowed]
    if unknown:
        raise _fail(
            path,
            line_number,
            f"{field} has unknown value(s): {', '.join(unknown)}",
        )


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------


def read_version(spec_dir: Path) -> tuple[str, str]:
    """Return the ITWS version and status label from the front matter."""
    front_matter = spec_dir / "00-front-matter.md"
    for line in front_matter.read_text(encoding="utf-8").splitlines():
        match = VERSION_RE.match(line)
        if match:
            return match.group("version"), match.group("status")
    raise SpecError(f"{front_matter}: missing version metadata line")


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


def rule_files(spec_dir: Path) -> list[Path]:
    """Every file that may hold rules: core parts first, then overlays."""
    paths = sorted(spec_dir.glob("0[2-8]-*.md"))
    overlays = spec_dir / OVERLAY_DIRNAME
    for profile in PROFILE_IDS:
        candidate = overlays / profile / PROFILE_RULES_FILENAME
        if candidate.exists():
            paths.append(candidate)
    for family in sorted(PROFILE_FAMILIES):
        candidate = overlays / SHARED_DIRNAME / f"{family}.md"
        if candidate.exists():
            paths.append(candidate)
    return paths


def _validate_profiles(path: Path, line_number: int, profiles: tuple[str, ...]) -> None:
    if not profiles:
        raise _fail(path, line_number, "empty Profiles metadata")
    if len(set(profiles)) != len(profiles):
        raise _fail(path, line_number, "duplicate profile ID")
    unknown = [profile for profile in profiles if profile not in PROFILE_IDS]
    if unknown:
        raise _fail(
            path, line_number, f"unknown profile ID(s): {', '.join(unknown)}"
        )
    expected = tuple(profile for profile in PROFILE_IDS if profile in profiles)
    if profiles != expected:
        raise _fail(path, line_number, "profile IDs are not in registry order")


def _validate_placement(
    spec_dir: Path, path: Path, line_number: int, profiles: tuple[str, ...]
) -> None:
    """Enforce §1.5.2: the Profiles metadata determines the rule's file."""
    overlays = spec_dir / OVERLAY_DIRNAME
    profile_set = set(profiles)
    families = [
        family
        for family, members in PROFILE_FAMILIES.items()
        if profile_set and profile_set <= set(members)
    ]
    if len(profiles) == 1:
        expected = overlays / profiles[0] / PROFILE_RULES_FILENAME
    elif families:
        expected = overlays / SHARED_DIRNAME / f"{families[0]}.md"
    else:
        expected = None

    if expected is None:
        if path.is_relative_to(overlays):
            raise _fail(
                path,
                line_number,
                "a rule scoped across families belongs in Parts 2-8, not an overlay",
            )
        return

    if path != expected:
        raise _fail(
            path,
            line_number,
            f"rule scoped to {', '.join(profiles)} belongs in "
            f"{expected.relative_to(spec_dir).as_posix()}, "
            f"not {path.relative_to(spec_dir).as_posix()}",
        )


def _parse_navigation(
    path: Path,
    constructs_line: tuple[int, str] | None,
    navigation_line: tuple[int, str] | None,
    resources_line: tuple[int, str] | None,
) -> Navigation | None:
    if navigation_line is None:
        return None
    line_number, raw = navigation_line
    try:
        fields = _split_fields(raw)
    except ValueError as error:
        raise _fail(path, line_number, f"malformed Navigation metadata: {error}")

    required = {"target", "chunks", "slots", "layers", "context", "rewrite"}
    missing = required - set(fields)
    if missing:
        raise _fail(
            path,
            line_number,
            f"Navigation metadata is missing: {', '.join(sorted(missing))}",
        )
    extra = set(fields) - required
    if extra:
        raise _fail(
            path,
            line_number,
            f"Navigation metadata has unknown field(s): {', '.join(sorted(extra))}",
        )

    chunk_types = _split_list(fields["chunks"])
    slots = _split_list(fields["slots"])
    _check_closed(path, line_number, "chunks", chunk_types, CHUNK_TYPES)
    if fields["layers"] not in LAYERS:
        raise _fail(path, line_number, f"unknown layer scope {fields['layers']!r}")
    if fields["context"] not in CONTEXT_SCOPES:
        raise _fail(path, line_number, f"unknown context scope {fields['context']!r}")
    if fields["rewrite"] not in REWRITE_GUIDANCE:
        raise _fail(
            path, line_number, f"unknown rewrite guidance {fields['rewrite']!r}"
        )
    from itws.vocab import TARGETS

    if fields["target"] not in TARGETS:
        raise _fail(path, line_number, f"unknown target {fields['target']!r}")
    if "any" in chunk_types and len(chunk_types) > 1:
        raise _fail(path, line_number, "chunks: 'any' cannot combine with a type")

    if constructs_line is None:
        raise _fail(path, line_number, "Navigation metadata without a Constructs line")
    construct_number, construct_raw = constructs_line
    constructs = _split_list(construct_raw)
    _check_closed(path, construct_number, "constructs", constructs, CONSTRUCTS)
    if "any" in constructs and len(constructs) > 1:
        raise _fail(
            path, construct_number, "constructs: 'any' cannot combine with a construct"
        )
    if not constructs:
        raise _fail(path, construct_number, "empty Constructs metadata")

    if resources_line is None:
        raise _fail(path, line_number, "Navigation metadata without a Resources line")
    resource_number, resource_raw = resources_line
    try:
        resource_fields = _split_fields(resource_raw)
    except ValueError as error:
        raise _fail(path, resource_number, f"malformed Resources metadata: {error}")
    if set(resource_fields) != {"reads", "writes"}:
        raise _fail(
            path, resource_number, "Resources metadata needs exactly 'reads' and 'writes'"
        )
    reads = _split_list(resource_fields["reads"])
    writes = _split_list(resource_fields["writes"])
    _check_closed(path, resource_number, "reads", reads, RESOURCES)
    _check_closed(path, resource_number, "writes", writes, RESOURCES)

    return Navigation(
        target=fields["target"],
        layers=fields["layers"],
        context_scope=fields["context"],
        rewrite_guidance=fields["rewrite"],
        constructs=constructs,
        chunk_types=chunk_types,
        slots=slots,
        reads=reads,
        writes=writes,
    )


def _parse_relations(
    path: Path, line: tuple[int, str] | None
) -> tuple[Relation, ...]:
    if line is None:
        return ()
    line_number, raw = line
    if raw.strip() == "none":
        return ()
    relations: list[Relation] = []
    for chunk in raw.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(None, 1)
        if len(parts) != 2:
            raise _fail(path, line_number, f"malformed relation {chunk!r}")
        relation_type, target = parts[0], parts[1].strip()
        if relation_type not in AUTHORED_RELATION_TYPES:
            raise _fail(
                path, line_number, f"unknown relation type {relation_type!r}"
            )
        note = ""
        if " (" in target and target.endswith(")"):
            target, _, note = target.partition(" (")
            note = note[:-1]
        if not re.fullmatch(r"\d+\.\d+\.\d+", target):
            raise _fail(
                path, line_number, f"relation target {target!r} is not a rule ID"
            )
        relations.append(Relation(type=relation_type, target=target, note=note))
    return tuple(relations)


def _collect_prose(lines: list[str], start: int, stop: int) -> dict[str, object]:
    """Collect the statement, rationale, example pair, and cross-references."""
    statement: list[str] = []
    rationale = ""
    examples: dict[str, list[str]] = {"compliant": [], "non_compliant": []}
    cross_references = ""
    collecting: str | None = None
    in_statement = True
    for index in range(start, stop):
        line = lines[index]
        if in_statement and (line.startswith("> ") or line == ">"):
            statement.append(line[2:].strip() if len(line) > 1 else "")
            continue
        if line.startswith("**"):
            in_statement = False
        rationale_match = RATIONALE_RE.match(line)
        compliant_match = COMPLIANT_RE.match(line)
        non_compliant_match = NON_COMPLIANT_RE.match(line)
        xref_match = XREF_RE.match(line)
        if rationale_match:
            collecting = None
            rationale = rationale_match.group("text")
        elif non_compliant_match:
            collecting = "non_compliant"
            text = non_compliant_match.group("text").strip()
            if text:
                examples["non_compliant"].append(text)
        elif compliant_match:
            collecting = "compliant"
            text = compliant_match.group("text").strip()
            if text:
                examples["compliant"].append(text)
        elif xref_match:
            collecting = None
            cross_references = xref_match.group("text")
        elif collecting:
            if line.startswith("**"):
                collecting = None
            elif line.strip():
                examples[collecting].append(line.rstrip())
    compliant = "\n".join(examples["compliant"]).strip()
    non_compliant = "\n".join(examples["non_compliant"]).strip()
    joined = "\n".join(statement).strip()
    joined = re.sub(r"\n{2,}", "\n", joined)
    return {
        "statement": joined,
        "rationale": rationale,
        "compliant": compliant,
        "non_compliant": non_compliant,
        "cross_references": cross_references,
    }


def parse_rules(spec_dir: Path, *, require_navigation: bool = True) -> list[Rule]:
    """Parse every rule from the core parts and the overlay files."""
    rules: list[Rule] = []
    seen: dict[str, str] = {}

    for path in rule_files(spec_dir):
        lines = path.read_text(encoding="utf-8").splitlines()
        headers = [
            index for index, line in enumerate(lines) if RULE_RE.match(line)
        ]
        for position, index in enumerate(headers):
            header = RULE_RE.match(lines[index])
            stop = headers[position + 1] if position + 1 < len(headers) else len(lines)
            if index + 1 >= len(lines):
                raise _fail(path, index + 1, "rule has no metadata")
            metadata = METADATA_RE.match(lines[index + 1])
            if not metadata:
                raise _fail(path, index + 2, "missing or malformed rule metadata")

            cursor = index + 2
            profiles: tuple[str, ...] = ()
            profile_match = (
                PROFILES_RE.match(lines[cursor]) if cursor < len(lines) else None
            )
            if profile_match:
                profiles = tuple(
                    item.strip()
                    for item in profile_match.group("profiles").split(",")
                )
                _validate_profiles(path, cursor + 1, profiles)
                _validate_placement(spec_dir, path, cursor + 1, profiles)
                cursor += 1
            elif path.is_relative_to(spec_dir / OVERLAY_DIRNAME):
                raise _fail(
                    path,
                    index + 1,
                    "a rule without Profiles metadata is shared core and "
                    "belongs in Parts 2-8",
                )

            constructs_line: tuple[int, str] | None = None
            navigation_line: tuple[int, str] | None = None
            resources_line: tuple[int, str] | None = None
            relations_line: tuple[int, str] | None = None
            for matcher, slot in (
                (CONSTRUCTS_RE, "constructs"),
                (NAVIGATION_RE, "navigation"),
                (RESOURCES_RE, "resources"),
                (RELATIONS_RE, "relations"),
            ):
                if cursor >= len(lines):
                    break
                match = matcher.match(lines[cursor])
                if not match:
                    continue
                captured = (cursor + 1, match.group(1))
                if slot == "constructs":
                    constructs_line = captured
                elif slot == "navigation":
                    navigation_line = captured
                elif slot == "resources":
                    resources_line = captured
                else:
                    relations_line = captured
                cursor += 1

            navigation = _parse_navigation(
                path, constructs_line, navigation_line, resources_line
            )
            if navigation is None and require_navigation:
                raise _fail(
                    path,
                    index + 1,
                    f"rule {header.group('number')} has no Navigation metadata; "
                    "§1.6 requires it on every active rule",
                )
            relations = _parse_relations(path, relations_line)

            status = "active"
            deprecated_since: str | None = None
            replacement: str | None = None
            if cursor < len(lines):
                status_line = lines[cursor]
                status_match = STATUS_RE.match(status_line)
                if status_match:
                    status = status_match.group("status")
                    detail = status_match.group("detail")
                    if status == "active" and detail:
                        raise _fail(
                            path, cursor + 1, "active status cannot carry details"
                        )
                    if status == "deprecated":
                        detail_match = DEPRECATED_DETAIL_RE.match(detail)
                        if not detail_match:
                            raise _fail(
                                path,
                                cursor + 1,
                                "deprecated status must name version and replacement",
                            )
                        deprecated_since = detail_match.group("version")
                        value = detail_match.group("replacement")
                        replacement = None if value == "none" else value
                    cursor += 1
                elif status_line.startswith("**Status:**"):
                    raise _fail(path, cursor + 1, "malformed status metadata")

            if navigation is None:
                navigation = Navigation(
                    target="document",
                    layers="both",
                    context_scope="document",
                    rewrite_guidance="review",
                    constructs=("any",),
                    chunk_types=("any",),
                    slots=("any",),
                    reads=("chunk-text",),
                    writes=("none",),
                )

            prose = _collect_prose(lines, cursor, stop)
            if not prose["statement"]:
                raise _fail(path, index + 1, "rule has no normative statement")
            if status == "active" and not (
                prose["compliant"] and prose["non_compliant"]
            ):
                raise _fail(path, index + 1, "rule has no contrasting example pair")

            number = header.group("number")
            location = path.relative_to(spec_dir.parent).as_posix()
            if number in seen:
                raise _fail(
                    path, index + 1, f"duplicate rule {number} (also in {seen[number]})"
                )
            seen[number] = location

            end = stop - 1
            while end > index and not lines[end].strip():
                end -= 1
            rules.append(
                Rule(
                    number=number,
                    name=header.group("name"),
                    rule_class=metadata.group("class"),
                    machine_checkable=metadata.group("machine"),
                    source=metadata.group("source"),
                    profiles=profiles,
                    status=status,
                    deprecated_since=deprecated_since,
                    replacement=replacement,
                    statement=str(prose["statement"]),
                    rationale=str(prose["rationale"]),
                    example=RuleExample(
                        compliant=str(prose["compliant"]),
                        non_compliant=str(prose["non_compliant"]),
                    ),
                    cross_references=str(prose["cross_references"]),
                    navigation=navigation,
                    relations=relations,
                    span=SourceSpan(location, index + 1, end + 1),
                )
            )

    if not rules:
        raise SpecError(f"no rules found under {spec_dir}")
    return sorted(rules, key=lambda rule: rule.sort_key)


# ---------------------------------------------------------------------------
# Phrase lists
# ---------------------------------------------------------------------------


def parse_phrase_lists(spec_dir: Path) -> list[PhraseListEntry]:
    """Collect every declared phrase list from the core parts.

    A phrase-list paragraph has the §8.2.1 form::

        **Phrase list 2.6.6 — warpath markers (phrase):** "previously we"; …

    The generated entries are the linter's only word- and phrase-level input.
    """
    entries: list[PhraseListEntry] = []
    for path in sorted(spec_dir.glob("0[2-8]-*.md")):
        location = path.relative_to(spec_dir.parent).as_posix()
        in_fence = False
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = PHRASE_LIST_RE.match(line)
            if not match:
                if line.startswith("**Phrase list"):
                    raise _fail(path, index + 1, "malformed phrase-list paragraph")
                continue
            rule = match.group("rule")
            label = match.group("label").strip()
            kind = match.group("kind")
            flags = match.group("flags")
            ignore_case = "case-sensitive" not in flags
            span = SourceSpan(location, index + 1, index + 1)
            items = list(PHRASE_ITEM_RE.finditer(match.group("items")))
            if not items:
                raise _fail(path, index + 1, "phrase list has no quoted items")
            slug = re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")
            for ordinal, item in enumerate(items, start=1):
                literal = item.group("literal")
                note = item.group("note") or ""
                replacement = item.group("replacement") or ""
                message = f"{label}: {literal!r} (§{rule})"
                if replacement:
                    message = f"{message} — use {replacement!r} instead"
                if note:
                    message = f"{message} — {note}"
                if kind == "pattern":
                    try:
                        re.compile(literal)
                    except re.error as error:
                        raise _fail(
                            path, index + 1, f"invalid pattern {literal!r}: {error}"
                        )
                entries.append(
                    PhraseListEntry(
                        id=f"{rule}/{slug}/{ordinal:02d}",
                        rule=rule,
                        kind=kind,
                        pattern=literal,
                        message=message,
                        replacement=replacement,
                        ignore_case=ignore_case,
                        span=span,
                    )
                )
    entries.sort(key=lambda entry: (rule_sort_key(entry.rule), entry.id))
    seen_ids = set()
    for entry in entries:
        if entry.id in seen_ids:
            raise SpecError(
                f"{entry.span.path}:{entry.span.start_line}: duplicate phrase-list "
                f"entry {entry.id}"
            )
        seen_ids.add(entry.id)
    return entries


# ---------------------------------------------------------------------------
# Profiles and skeletons
# ---------------------------------------------------------------------------


def parse_profiles(spec_dir: Path) -> list[ProfileRecord]:
    """Read each profile's language contract and shared modules."""
    overlays = spec_dir / OVERLAY_DIRNAME
    records: list[ProfileRecord] = []
    current_version, _ = read_version(spec_dir)
    for profile in PROFILE_IDS:
        readme = overlays / profile / "README.md"
        if not readme.is_file():
            raise SpecError(f"missing overlay README: {readme}")
        text = readme.read_text(encoding="utf-8")
        lines = text.splitlines()
        location = readme.relative_to(spec_dir.parent).as_posix()

        version_match = OVERLAY_VERSION_RE.search(text)
        if not version_match:
            raise SpecError(f"{readme}: missing version metadata line")
        if version_match.group("version") != current_version:
            raise SpecError(
                f"{readme}: records ITWS version "
                f"{version_match.group('version')}; expected {current_version}"
            )

        job = ""
        shallow_model_outcome = ""
        for line in lines:
            if not job and JOB_RE.match(line):
                job = JOB_RE.match(line).group("job")
            if (
                not shallow_model_outcome
                and SHALLOW_MODEL_OUTCOME_RE.match(line)
            ):
                shallow_model_outcome = SHALLOW_MODEL_OUTCOME_RE.match(
                    line
                ).group("outcome")
        for field_name, value in (
            ("Job", job),
            ("shallow-model outcome", shallow_model_outcome),
        ):
            if not value:
                raise SpecError(f"{readme}: missing {field_name}")

        modules = tuple(sorted(set(MODULE_LINK_RE.findall(text))))
        expected_modules = profile_families(profile)
        if modules != expected_modules:
            raise SpecError(
                f"{readme}: load set names modules {modules or ('none',)}; "
                f"expected {expected_modules or ('none',)}"
            )

        reader_path = overlays / profile / "reader.md"
        if not reader_path.is_file():
            raise SpecError(f"missing reader overlay: {reader_path}")
        overlay_items = parse_reader_overlay(reader_path, spec_dir, profile)
        if not overlay_items:
            raise SpecError(
                f"{reader_path}: the overlay states no reader convention; "
                "Annex B §B.4 requires each overlay to state its own"
            )

        records.append(
            ProfileRecord(
                id=profile,
                label=PROFILE_LABELS[profile],
                surface=profile_surface(profile),
                job=job,
                shallow_model_outcome=shallow_model_outcome,
                modules=modules,
                directory=f"spec/overlays/{profile}",
                reader_overlay=overlay_items,
                span=SourceSpan(location, 1, len(lines)),
            )
        )
    return records


def _parse_renames(body: str) -> dict[str, tuple[str, ...]]:
    renames: dict[str, list[str]] = {}
    if body.strip().rstrip(".") == "none":
        return {}
    for clause in body.split(";"):
        match = RENAME_PAIR_RE.search(clause)
        if not match:
            continue
        source = match.group("from")
        targets = re.findall(r"`([^`]+)`", clause.split("→", 1)[1])
        renames.setdefault(source, []).extend(targets)
    return {key: tuple(dedupe(value)) for key, value in renames.items()}


def parse_skeletons(spec_dir: Path) -> list[Skeleton]:
    """Read each profile's ordered slots, renames, merges, and mutation policy."""
    overlays = spec_dir / OVERLAY_DIRNAME
    skeletons: list[Skeleton] = []
    for profile in PROFILE_IDS:
        path = overlays / profile / "skeleton.md"
        if not path.is_file():
            raise SpecError(f"missing skeleton file: {path}")
        lines = path.read_text(encoding="utf-8").splitlines()
        location = path.relative_to(spec_dir.parent).as_posix()

        title = SKELETON_TITLE_RE.match(lines[0]) if lines else None
        if not title:
            raise _fail(path, 1, "skeleton file needs an 'Annex E §E.n' title")
        if title.group("profile") != profile:
            raise _fail(
                path, 1, f"skeleton title names {title.group('profile')!r}"
            )

        dependency_order = ""
        in_block = False
        raw_slots: list[tuple[int, str, str, str]] = []
        renames: dict[str, tuple[str, ...]] = {}
        merges: list[Merge] = []
        policies: list[MutationPolicy] = []
        pending_description: list[str] = []

        for index, line in enumerate(lines):
            if line.startswith("```"):
                in_block = not in_block
                continue
            if in_block:
                match = SLOT_RE.match(line)
                if match:
                    if raw_slots and pending_description:
                        indent, name, status, description = raw_slots[-1]
                        raw_slots[-1] = (
                            indent,
                            name,
                            status,
                            (description + " " + " ".join(pending_description)).strip(),
                        )
                        pending_description = []
                    raw_slots.append(
                        (
                            len(match.group("indent")),
                            match.group("name").strip(),
                            match.group("status").strip(),
                            match.group("description").strip(),
                        )
                    )
                elif line.strip() and raw_slots:
                    if not line.startswith(" "):
                        # A slot name too long for its column wraps to the next
                        # line. Its continuation starts at column 0.
                        head, separator, tail = line.partition("  ")
                        indent, name, status, description = raw_slots[-1]
                        raw_slots[-1] = (
                            indent,
                            f"{name} {head.strip()}".strip(),
                            status,
                            description,
                        )
                        if separator and tail.strip():
                            pending_description.append(tail.strip())
                    else:
                        pending_description.append(line.strip())
                continue
            if not dependency_order and line.startswith("A ") and "(§4.4)" in line:
                dependency_order = line.strip()
            elif not dependency_order and line.startswith("An ") and "(§4.4)" in line:
                dependency_order = line.strip()
            rename_match = RENAMES_RE.match(line)
            if rename_match:
                renames = _parse_renames(rename_match.group("body"))
            merge_match = MERGES_RE.match(line)
            if merge_match:
                body = merge_match.group("body")
                if body.strip().rstrip(".") != "none":
                    for pair in MERGE_PAIR_RE.finditer(body):
                        merges.append(
                            Merge(
                                parts=(pair.group("a"), pair.group("b")),
                                combined=pair.group("combined"),
                            )
                        )
            policy_match = MUTATION_RE.match(line)
            if policy_match:
                policies.append(
                    MutationPolicy(
                        scope=policy_match.group("scope").strip(),
                        policy=policy_match.group("policy"),
                        rule=policy_match.group("rule"),
                        note=policy_match.group("note").strip(),
                    )
                )

        if raw_slots and pending_description:
            indent, name, status, description = raw_slots[-1]
            raw_slots[-1] = (
                indent,
                name,
                status,
                (description + " " + " ".join(pending_description)).strip(),
            )

        if not raw_slots:
            raise _fail(path, 1, "skeleton file declares no slots")

        slots: list[Slot] = []
        parents: dict[int, str] = {}
        for order, (indent, name, status, description) in enumerate(raw_slots, start=1):
            parent = ""
            for level in sorted(parents):
                if level < indent:
                    parent = parents[level]
            parents = {level: value for level, value in parents.items() if level < indent}
            parents[indent] = name
            slots.append(
                Slot(
                    name=name,
                    required=status.startswith("required"),
                    order=order,
                    description=" ".join(description.split()),
                    renames=renames.get(name, ()),
                    parent=parent,
                    repeats="for each" in status,
                )
            )

        slot_names = {slot.name for slot in slots}
        unknown_renames = sorted(set(renames) - slot_names)
        if unknown_renames:
            raise _fail(
                path,
                1,
                "rename source(s) are not slots: " + ", ".join(unknown_renames),
            )
        for merge in merges:
            missing = [part for part in merge.parts if part not in slot_names]
            if missing:
                raise _fail(
                    path, 1, "merge names unknown slot(s): " + ", ".join(missing)
                )

        skeletons.append(
            Skeleton(
                profile=profile,
                annex_section=title.group("section"),
                surface=profile_surface(profile),
                dependency_order=dependency_order,
                slots=tuple(slots),
                merges=tuple(merges),
                mutation_policies=tuple(policies),
                span=SourceSpan(location, 1, len(lines)),
            )
        )
    return skeletons


# ---------------------------------------------------------------------------
# Glossary and reader baseline
# ---------------------------------------------------------------------------


def parse_glossary(spec_dir: Path) -> list[GlossaryEntry]:
    """Parse Annex A entries and their ladder prerequisites."""
    path = spec_dir / "annexes" / "annex-a-glossary.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    location = path.relative_to(spec_dir.parent).as_posix()
    entries: list[GlossaryEntry] = []

    index = 0
    while index < len(lines):
        header = GLOSSARY_HEADER_RE.match(lines[index])
        if not header:
            index += 1
            continue
        start = index
        index += 1
        if index >= len(lines) or not lines[index].startswith("```"):
            raise _fail(path, index + 1, "glossary entry has no field block")
        index += 1
        fields: dict[str, str] = {}
        current: str | None = None
        while index < len(lines) and not lines[index].startswith("```"):
            field_match = GLOSSARY_FIELD_RE.match(lines[index])
            if field_match:
                current = field_match.group("key").strip().rstrip(":")
                fields[current] = field_match.group("value").strip()
            elif current:
                fields[current] = (fields[current] + " " + lines[index].strip()).strip()
            index += 1
        end = index
        index += 1

        required = {
            "Definition",
            "Approved example",
            "Do not use for / say",
            "Ladder prerequisites",
            "Profiles",
            "Domain tag",
            "Version",
        }
        missing = required - set(fields)
        if missing:
            raise _fail(
                path,
                start + 1,
                f"glossary entry {header.group('term')!r} is missing: "
                + ", ".join(sorted(missing)),
            )

        raw_prereq = fields["Ladder prerequisites"]
        assumed = tuple(
            item.strip()
            for item in re.findall(r"assumed baseline \(([^)]*)\)", raw_prereq)
        )
        without_assumed = re.sub(r"assumed baseline \([^)]*\)", "", raw_prereq)
        prerequisites = tuple(
            item.strip()
            for item in re.split(r"[;,]", without_assumed)
            if item.strip()
        )
        profiles = tuple(
            item.strip() for item in fields["Profiles"].split(",") if item.strip()
        )
        unknown = [profile for profile in profiles if profile not in PROFILE_IDS]
        if unknown:
            raise _fail(
                path,
                start + 1,
                f"glossary entry {header.group('term')!r} names unknown "
                f"profile(s): {', '.join(unknown)}",
            )

        entries.append(
            GlossaryEntry(
                term=header.group("term"),
                part_of_speech=header.group("pos"),
                status=header.group("status"),
                definition=" ".join(fields["Definition"].split()),
                approved_example=" ".join(fields["Approved example"].split()),
                do_not_use=" ".join(fields["Do not use for / say"].split()),
                prerequisites=prerequisites,
                assumed_prerequisites=assumed,
                profiles=profiles,
                domain_tag=fields["Domain tag"],
                version=fields["Version"],
                span=SourceSpan(location, start + 1, end + 1),
            )
        )

    if not entries:
        raise SpecError(f"{path}: no glossary entries found")
    validate_glossary_graph(path, entries)
    return entries


def validate_glossary_graph(path: Path, entries: list[GlossaryEntry]) -> None:
    """Reject an unknown prerequisite or a cycle in the term ladder."""
    known = {entry.term for entry in entries}
    edges: dict[str, tuple[str, ...]] = {}
    for entry in entries:
        unknown = [term for term in entry.prerequisites if term not in known]
        if unknown:
            raise _fail(
                path,
                entry.span.start_line,
                f"{entry.term!r} names unknown prerequisite(s): "
                + ", ".join(unknown),
            )
        edges[entry.term] = entry.prerequisites

    state: dict[str, int] = {}

    def visit(term: str, trail: list[str]) -> None:
        mark = state.get(term, 0)
        if mark == 1:
            cycle = " → ".join(trail + [term])
            raise SpecError(f"{path}: glossary prerequisite cycle: {cycle}")
        if mark == 2:
            return
        state[term] = 1
        for prerequisite in edges.get(term, ()):
            visit(prerequisite, trail + [term])
        state[term] = 2

    for term in sorted(edges):
        visit(term, [])


#: Wording that marks a line as stating what the reader does *not* know.
#: Section 0.3.3 resolves every borderline case the same way, so a cue that
#: fires wrongly can only move an item out of the assumed set, never into it.
NEGATIVE_BASELINE_RE = re.compile(
    r"not assume|does not admit|remain(?:s)? unassumed|remains unavailable|"
    r"requires? admission|\bAdmit\b|not in the baseline|shall not use|"
    r"not assumed to know|grants nothing else|not knowledge",
    re.IGNORECASE,
)

#: Wording that makes a grant depend on a declaration rather than hold
#: outright, as the §0.3.4 host-language supplement does.
CONDITIONAL_GRANT_RE = re.compile(r"\bconditional\b|\bWhen\b")

#: Sections of Annex B that carry baseline items. §B.4 is the profile
#: registry and §B.5 is the change process; neither states an assumption.
BASELINE_SECTION_POLARITY: dict[str, tuple[str, str]] = {
    "B.1": ("assumed", "concept"),
    "B.2": ("assumed", "notation"),
    "B.3": ("excluded", "concept"),
}


def parse_reader_baseline(spec_dir: Path) -> list[BaselineItem]:
    """Parse Annex B assumptions, notation, and explicit exclusions.

    Each item records whether the reader is assumed to hold it. A bullet
    takes the polarity of the group it sits under. A prose line becomes an
    item only when it carries a negative cue, because §B.1 and §B.2 mix
    exclusions into otherwise positive sections and the surrounding
    commentary states no assumption at all.
    """
    path = spec_dir / "annexes" / "annex-b-assumed-reader-baseline.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    location = path.relative_to(spec_dir.parent).as_posix()
    items: list[BaselineItem] = []
    section = ""
    group = ""
    default_polarity = "assumed"
    kind = "concept"
    polarity = "assumed"

    for index, line in enumerate(lines):
        stripped = line.strip()
        if line.startswith("## B."):
            section = line[3:].strip()
            number = section.split()[0]
            default_polarity, kind = BASELINE_SECTION_POLARITY.get(
                number, ("", "")
            )
            polarity = default_polarity
            group = ""
            continue
        if not section or not default_polarity:
            continue
        if stripped.endswith(":") and not stripped.startswith(("-", "|", "#")):
            group = stripped[:-1].strip()
            # A new group restores the section's own polarity, so a negative
            # aside cannot leak into the list that follows it.
            polarity = default_polarity
            if NEGATIVE_BASELINE_RE.search(group):
                polarity = "excluded"
            continue

        category = section if not group else f"{section} — {group}"
        if stripped.startswith("- "):
            items.append(
                BaselineItem(
                    category=category,
                    text=stripped[2:].strip(),
                    span=SourceSpan(location, index + 1, index + 1),
                    polarity=polarity,
                    kind=kind,
                )
            )
            continue
        if not stripped or stripped.startswith(("|", "#", "**")):
            continue
        if NEGATIVE_BASELINE_RE.search(stripped):
            items.append(
                BaselineItem(
                    category=category,
                    text=stripped,
                    span=SourceSpan(location, index + 1, index + 1),
                    polarity="excluded",
                    kind=kind,
                )
            )
            # Bullets that follow an exclusion sentence with no group
            # heading of their own continue that exclusion.
            polarity = "excluded"

    if not items:
        raise SpecError(f"{path}: no baseline items found")
    if not any(item.is_assumed for item in items):
        raise SpecError(f"{path}: no assumed baseline item was parsed")
    return items


def parse_reader_overlay(
    path: Path, spec_dir: Path, profile: str
) -> tuple[BaselineItem, ...]:
    """Parse one profile's `reader.md` into polarity-bearing records.

    An overlay adds document conventions, and one overlay adds the §0.3.4
    host-language supplement. Both appear as prose, as bullets, or as both,
    so the parser reads all three and keeps each item's polarity with it.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    location = path.relative_to(spec_dir.parent).as_posix()
    section = f"B.4 {profile}"
    items: list[BaselineItem] = []
    lead_in = ""
    polarity = "assumed"
    conditional = False

    def category() -> str:
        return f"{section} — {lead_in}" if lead_in else section

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "**", "|")):
            continue
        if stripped.endswith(":"):
            # The clause nearest the list is the one that introduces it.
            lead_in = stripped[:-1].strip().split(". ")[-1].strip()
            polarity = (
                "excluded" if NEGATIVE_BASELINE_RE.search(stripped) else "assumed"
            )
            # A grant introduced by a condition holds only while it does.
            conditional = bool(CONDITIONAL_GRANT_RE.search(stripped))
            continue
        if stripped.startswith("- "):
            items.append(
                BaselineItem(
                    category=category(),
                    text=stripped[2:].strip(),
                    span=SourceSpan(location, index + 1, index + 1),
                    polarity=polarity,
                    kind="host-supplement" if conditional else "convention",
                    conditional=conditional,
                )
            )
            continue
        if stripped.startswith("The reader "):
            items.append(
                BaselineItem(
                    category=section,
                    text=stripped,
                    span=SourceSpan(location, index + 1, index + 1),
                    polarity=(
                        "excluded"
                        if NEGATIVE_BASELINE_RE.search(stripped)
                        else "assumed"
                    ),
                    kind="convention",
                )
            )
    return tuple(items)


# ---------------------------------------------------------------------------
# Annex D examples
# ---------------------------------------------------------------------------


def parse_examples(spec_dir: Path, rules: list[Rule]) -> list[Example]:
    """Parse Annex D paired examples and each rule's contrasting pair."""
    path = spec_dir / "annexes" / "annex-d-examples-corpus.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    location = path.relative_to(spec_dir.parent).as_posix()
    known_rules = {rule.number for rule in rules}
    examples: list[Example] = []

    headers = [
        index for index, line in enumerate(lines) if EXAMPLE_HEADER_RE.match(line)
    ]
    for position, index in enumerate(headers):
        header = EXAMPLE_HEADER_RE.match(lines[index])
        stop = headers[position + 1] if position + 1 < len(headers) else len(lines)
        while stop > index and (
            not lines[stop - 1].strip() or lines[stop - 1].startswith("## ")
        ):
            stop -= 1

        fields: dict[str, str] = {}
        body_start = index + 1
        for cursor in range(index + 1, stop):
            field_match = EXAMPLE_FIELD_RE.match(lines[cursor])
            if field_match and field_match.group("key") in {
                "Profile",
                "Source",
                "Rules applied",
                "Chunk types",
                "Constructs",
                "Repair operators",
                "Preservation notes",
            }:
                fields[field_match.group("key")] = field_match.group("value").strip()
                body_start = cursor + 1
            elif lines[cursor].strip() == "":
                continue
            else:
                break

        for required in ("Profile", "Source", "Rules applied"):
            if required not in fields:
                raise _fail(
                    path, index + 1, f"example {header.group('id')} lacks {required}"
                )
        profile = fields["Profile"]
        if profile not in PROFILE_IDS:
            raise _fail(
                path, index + 1, f"example {header.group('id')} names unknown profile"
            )

        raw_rules = fields["Rules applied"]
        rule_ids = tuple(dedupe(RULE_REFERENCE_RE.findall(raw_rules)))
        unknown = [number for number in rule_ids if number not in known_rules]
        if unknown:
            raise _fail(
                path,
                index + 1,
                f"example {header.group('id')} cites unknown rule(s): "
                + ", ".join(unknown),
            )
        sections = tuple(dedupe(re.findall(r"§(\d+\.\d+)(?!\.\d)", raw_rules)))

        before, after, annotation = _split_example_body(lines, body_start, stop)
        examples.append(
            Example(
                id=header.group("id"),
                origin="annex-d",
                title=header.group("title"),
                profile=profile,
                source=fields["Source"],
                rules_applied=rule_ids,
                sections_applied=sections,
                before=before,
                after=after,
                annotation=annotation,
                chunk_types=_split_list(fields.get("Chunk types", "")),
                constructs=_split_list(fields.get("Constructs", "")),
                repair_operators=_split_list(fields.get("Repair operators", "")),
                preservation_notes=tuple(
                    item.strip()
                    for item in fields.get("Preservation notes", "").split(";")
                    if item.strip()
                ),
                span=SourceSpan(location, index + 1, stop),
            )
        )

    for example in examples:
        _check_closed(
            path, example.span.start_line, "Chunk types", example.chunk_types, CHUNK_TYPES
        )
        _check_closed(
            path, example.span.start_line, "Constructs", example.constructs, CONSTRUCTS
        )

    for rule in rules:
        examples.append(
            Example(
                id=f"rule:{rule.number}",
                origin="rule",
                title=rule.name,
                profile=rule.profiles[0] if rule.profiles else "",
                source=rule.source,
                rules_applied=(rule.number,),
                sections_applied=(rule.section,),
                before=rule.example.non_compliant,
                after=rule.example.compliant,
                annotation=rule.rationale,
                chunk_types=rule.navigation.chunk_types,
                constructs=rule.navigation.constructs,
                repair_operators=(),
                preservation_notes=(),
                span=rule.span,
            )
        )
    return examples


def _split_example_body(lines: list[str], start: int, stop: int) -> tuple[str, str, str]:
    sections: dict[str, list[str]] = {"Before": [], "After": [], "Annotation": []}
    current: str | None = None
    for cursor in range(start, stop):
        stripped = lines[cursor].strip()
        if stripped in {"Before:", "After:", "Annotation:"}:
            current = stripped[:-1]
            continue
        if current:
            sections[current].append(lines[cursor])
    return tuple(
        "\n".join(value).strip() for value in (
            sections["Before"], sections["After"], sections["Annotation"]
        )
    )


# ---------------------------------------------------------------------------
# Whole-specification assembly
# ---------------------------------------------------------------------------


def _resolve_relations(rules: list[Rule]) -> None:
    known = {rule.number for rule in rules}
    for rule in rules:
        for relation in rule.relations:
            if relation.target not in known:
                raise SpecError(
                    f"{rule.span.path}:{rule.span.start_line}: rule "
                    f"{rule.number} names unknown relation target {relation.target}"
                )
            if relation.target == rule.number:
                raise SpecError(
                    f"{rule.span.path}:{rule.span.start_line}: rule "
                    f"{rule.number} relates to itself"
                )


def _validate_replacements(rules: list[Rule]) -> None:
    known = {rule.number for rule in rules}
    for rule in rules:
        if rule.replacement is None:
            continue
        if rule.replacement == rule.number:
            raise SpecError(f"deprecated rule {rule.number} cannot replace itself")
        if rule.replacement not in known:
            raise SpecError(
                f"deprecated rule {rule.number} names missing replacement "
                f"{rule.replacement}"
            )


def _validate_phrase_rules(
    rules: list[Rule], phrase_lists: list[PhraseListEntry]
) -> None:
    known = {rule.number for rule in rules}
    for entry in phrase_lists:
        if entry.rule not in known:
            raise SpecError(
                f"{entry.span.path}:{entry.span.start_line}: phrase list names "
                f"unknown rule {entry.rule}"
            )


def _validate_slots(rules: list[Rule], skeletons: list[Skeleton]) -> None:
    """Every named skeleton slot in rule metadata must exist somewhere."""
    slot_names = {"any"}
    for skeleton in skeletons:
        slot_names.update(slot.name for slot in skeleton.slots)
        slot_names.update(merge.combined for merge in skeleton.merges)
        for slot in skeleton.slots:
            slot_names.update(slot.renames)
    for rule in rules:
        unknown = [
            slot for slot in rule.navigation.slots if slot not in slot_names
        ]
        if unknown:
            raise SpecError(
                f"{rule.span.path}:{rule.span.start_line}: rule {rule.number} "
                f"names unknown skeleton slot(s): {', '.join(unknown)}"
            )


def source_hashes(spec_dir: Path) -> dict[str, str]:
    """Hash every governed Markdown source, keyed by repository-relative path."""
    hashes: dict[str, str] = {}
    for path in sorted(spec_dir.rglob("*.md")):
        if "generated" in path.parts:
            continue
        key = path.relative_to(spec_dir.parent).as_posix()
        hashes[key] = content_hash(path.read_text(encoding="utf-8"))
    registry = spec_dir / "rule-ids.txt"
    if registry.exists():
        hashes[registry.relative_to(spec_dir.parent).as_posix()] = content_hash(
            registry.read_text(encoding="utf-8")
        )
    return hashes


def parse_specification(
    spec_dir: Path, *, require_navigation: bool = True
) -> Specification:
    """Parse, resolve, and validate the whole specification."""
    version, status = read_version(spec_dir)
    rules = parse_rules(spec_dir, require_navigation=require_navigation)
    _resolve_relations(rules)
    _validate_replacements(rules)
    profiles = parse_profiles(spec_dir)
    skeletons = parse_skeletons(spec_dir)
    if require_navigation:
        _validate_slots(rules, skeletons)
    glossary = parse_glossary(spec_dir)
    baseline = parse_reader_baseline(spec_dir)
    examples = parse_examples(spec_dir, rules)
    phrase_lists = parse_phrase_lists(spec_dir)
    _validate_phrase_rules(rules, phrase_lists)

    return Specification(
        version=version,
        status=status,
        rules=tuple(rules),
        profiles=tuple(profiles),
        skeletons=tuple(skeletons),
        glossary=tuple(glossary),
        baseline=tuple(baseline),
        examples=tuple(examples),
        phrase_lists=tuple(phrase_lists),
        source_hashes=source_hashes(spec_dir),
    )

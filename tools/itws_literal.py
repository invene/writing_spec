#!/usr/bin/env python3
"""Decide the literal ITWS rules over a corpus, and report what was left undecided.

This tool is NOT part of ITWS. No rule refers to it, it is outside the load set,
and deleting it changes no obligation. It decides no conformance question: ITWS
§0.5 keeps the result textual — applied `M` rules plus reported departures — and
a clean run here is a coverage statement rather than a result.

Load the full seven-file rule set first, always. This tool replaces *reading for*
the literal rules. It never replaces loading them.

It carries no copy of any rule string. Every phrase list, profile ID, disclosure
value, strength phrase, and `D` marker is parsed from `spec/` at run time, so the
tool cannot drift from the specification it screens. It does hold the list of rule
IDs it evaluates; a rule whose ID no longer has a row in `spec/` stops the run.

Usage:
    itws_literal.py FILE [FILE ...]        screen a corpus
    itws_literal.py --json FILE            machine-readable findings
    itws_literal.py --self-test            run the fixtures

Exit status is 0 whenever the run completed. A finding is not an error: a person
decides every screened finding, and the exit code must never read as a verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Rules this tool evaluates. Everything else in the load set is NOT evaluated,
# and `--coverage` says so. The D marker for each is read out of `spec/` at run
# time rather than written here: a hardcoded copy is a second record of the
# specification, and a second record drifts.
EVALUATED_RULES = (
    "4.3.1", "4.3.4", "4.3.5",
    "2.3.3", "2.6.7", "3.10.2", "3.10.4",
    "4.6.2", "4.8.2", "4.8.3", "4.10.5", "7.3.3",
    "2.1.3", "2.6.3", "2.6.4", "2.6.5", "2.6.6",
    "2.6.8", "2.6.9", "2.6.10", "2.6.11",
    "3.1.1", "3.1.2", "3.6.2", "3.8.1", "3.9.1",
    "3.10.6", "4.12.3", "5.6.1",
)

# Filled by parse_decidability() before any screening runs.
EVALUATED: dict[str, str] = {}


RULE_ROW_RE = re.compile(r"^\|\s*(\d+(?:\.\d+)+)\s*\|\s*[MRP]\s*\|\s*([LSJ])\s*\|", re.M)


def parse_decidability(spec_dir: Path) -> dict[str, str]:
    """Read each evaluated rule's `D` marker from its own row in `spec/`.

    A rule reclassified from `L` to `S` in the specification must change what
    this tool prints without anyone remembering to edit this file."""
    found: dict[str, str] = {}
    for path in [spec_dir / "core.md", *sorted((spec_dir / "profiles").glob("*.md"))]:
        for rule, d in RULE_ROW_RE.findall(path.read_text(encoding="utf-8")):
            found.setdefault(rule, d)
    missing = [r for r in EVALUATED_RULES if r not in found]
    if missing:
        raise SystemExit(
            "no rule row found in spec/ for: " + ", ".join(missing) +
            ". A screened rule whose ID has moved must be re-pointed here."
        )
    return {r: found[r] for r in EVALUATED_RULES}

SPEC_ROOT_MARKERS = ("spec/phrases.md", "spec/core.md")


# --------------------------------------------------------------------------
# Locating the specification
# --------------------------------------------------------------------------

def find_spec_dir(start: Path) -> Path:
    """Walk up from `start` until a directory holds both spec files."""
    for candidate in [start, *start.parents]:
        if all((candidate / marker).is_file() for marker in SPEC_ROOT_MARKERS):
            return candidate / "spec"
    raise SystemExit(
        "cannot find spec/phrases.md and spec/core.md above "
        f"{start}. Run this from inside a writing_spec checkout."
    )


# --------------------------------------------------------------------------
# Parsing the closed sets out of spec/
# --------------------------------------------------------------------------

@dataclass
class PhraseList:
    rule: str
    name: str
    kind: str          # word | phrase | pattern | opener
    cls: str           # M | R | P
    items: list[str] = field(default_factory=list)


SECTION_RE = re.compile(
    r"^##\s+§([\d.]+)\s+—\s+(.+?)\s+\((word|phrase|pattern|opener)\)\s+·\s+`([MRP])`\s*$"
)


def parse_phrase_lists(phrases_md: Path) -> list[PhraseList]:
    """Read every list out of spec/phrases.md. The strings live there, not here."""
    lists: list[PhraseList] = []
    current: PhraseList | None = None
    body: list[str] = []

    def flush() -> None:
        if current is None:
            return
        text = "\n".join(body)
        if re.search(r"^\|\s*Avoid\s*\|", text, re.M):
            # A replacement table: the first column holds the prohibited string.
            for row in re.findall(r"^\|\s*([^|]+?)\s*\|", text, re.M):
                if row.lower() in ("avoid", "---") or set(row) <= {"-"}:
                    continue
                current.items.append(row)
        elif current.kind == "pattern":
            current.items.extend(re.findall(r"`([^`]+)`", text))
        else:
            current.items.extend(re.findall(r'"([^"]+)"', text))
        lists.append(current)

    for line in phrases_md.read_text(encoding="utf-8").splitlines():
        match = SECTION_RE.match(line)
        if match:
            flush()
            current = PhraseList(rule=match.group(1), name=match.group(2),
                                 kind=match.group(3), cls=match.group(4))
            body = []
        elif line.startswith("## "):
            flush()
            current, body = None, []
        elif current is not None:
            body.append(line)
    flush()
    return [pl for pl in lists if pl.items]


def parse_profile_ids(core_md: Path) -> set[str]:
    text = core_md.read_text(encoding="utf-8")
    block = _section(text, "### 0.1 Profile registry")
    return set(re.findall(r"^\|\s*`([a-z-]+)`\s*\|", block, re.M))


def parse_disclosure_values(core_md: Path) -> set[str]:
    text = core_md.read_text(encoding="utf-8")
    block = text.split("**`AI disclosure` values (closed):**", 1)
    if len(block) < 2:
        return set()
    return set(re.findall(r"^\|\s*`([a-z]+)`\s*\|", block[1][:600], re.M))


def parse_strength_phrases(core_md: Path) -> dict[str, list[str]]:
    """Tier -> phrases, from the core §5.6 closed table."""
    text = core_md.read_text(encoding="utf-8")
    block = _section(text, "### 5.6 Evidential strength")
    tiers: dict[str, list[str]] = {}
    for tier, phrases in re.findall(
        r"^\|\s*(verified|observed|interpretive|adopted|proposed|speculative)\s*\|\s*(.+?)\s*\|",
        block, re.M,
    ):
        tiers[tier] = re.findall(r"\*\*(.+?)\*\*", phrases)
    return tiers


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    nxt = text.find("\n### ", start + len(heading))
    return text[start: nxt if nxt > 0 else len(text)]


# --------------------------------------------------------------------------
# Reading a document as prose
#
# Four traps, every one of which has produced a wrong result in practice:
#   - a period inside a closing quote still ends a sentence;
#   - a heading, table row, indented example, and code block are not prose,
#     and counting them as sentences inflates every length check;
#   - a declaration field is metadata, not governed prose (core §0.5);
#   - a bounded-block label is a template label, not a sentence.
# --------------------------------------------------------------------------

@dataclass
class Line:
    number: int
    text: str
    is_prose: bool
    in_speculation: bool
    is_declaration: bool
    in_block: bool = False
    in_fence: bool = False


DECLARATION_RE = re.compile(r"^\**(ITWS version|Profile|AI disclosure)\**\s*:", re.I)
BLOCK_LABEL_RE = re.compile(r"^>\s*\*\*\[(Detail|Intuition|Speculation)\s+—\s+[^\]]+\]\*\*")


def read_lines(text: str) -> list[Line]:
    lines: list[Line] = []
    in_fence = False
    in_speculation = False
    in_block = False
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            lines.append(Line(number, raw, False, in_speculation, False, in_block,
                              True))
            continue

        if BLOCK_LABEL_RE.match(stripped):
            in_block = True
            in_speculation = "[Speculation" in stripped
        elif not stripped.startswith(">") and stripped:
            in_block = False
            in_speculation = False

        is_declaration = bool(DECLARATION_RE.match(stripped.lstrip("> ").lstrip("-* ")))
        # An indented line opens a code block only after a blank line. Indented
        # after prose it is a wrapped continuation or a list body, and dropping
        # it silently removes real sentences from every check.
        indented = (raw.startswith("    ") or raw.startswith("\t")) and not (
            lines and lines[-1].is_prose
        )
        is_prose = not (
            in_fence
            or not stripped
            or stripped.startswith("#")
            or stripped.startswith("|")
            or set(stripped) <= set("-=*_ |:")
            or indented
            or is_declaration
        )
        lines.append(Line(number, raw, is_prose, in_speculation, is_declaration,
                          in_block, in_fence))
    return lines


def prose_text(line: Line) -> str:
    """Strip carrier syntax so a match lands on the words, not the markup."""
    text = re.sub(r"^\s*>+\s*", "", line.text)
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", text)
    text = BLOCK_LABEL_RE.sub("", text)
    return text


@dataclass
class Paragraph:
    """Consecutive prose lines, joined. Markdown wraps a sentence across lines,
    so every sentence-level check runs over a paragraph rather than a line —
    counting per line silently misses every wrapped sentence."""
    start: int
    text: str
    in_speculation: bool
    on_scan_path: bool = False
    is_heading: bool = False


def paragraphs(lines: list[Line]) -> list[Paragraph]:
    """Group consecutive prose lines, and mark the ones standing in for a
    section's opening chunk (core §4.12.1).

    Two approximations, both deliberate and both widening rather than narrowing:
    the whole opening paragraph is marked, not §4.12.1's first sentence of it,
    and appendix content is not detected, so an appendix section's opening
    paragraph is screened like any other. A bounded block is excluded, and it
    does not consume the section's opening slot — the prose behind a
    `[Detail — …]` block after a heading is still the opening chunk."""
    out: list[Paragraph] = []
    buf: list[str] = []
    start, spec, block, opening = 0, False, False, False
    fresh_heading = True
    for line in lines:
        if line.is_prose:
            if not buf:
                start, spec, block = line.number, line.in_speculation, line.in_block
                opening = fresh_heading and not line.in_block
            buf.append(prose_text(line).strip())
        else:
            if buf:
                out.append(Paragraph(start, " ".join(buf), spec, opening))
                buf = []
                if not block:
                    fresh_heading = False
            if not line.in_fence and line.text.lstrip().startswith("#"):
                fresh_heading = True
    if buf:
        out.append(Paragraph(start, " ".join(buf), spec, opening))
    return out


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


def scan_path_headings(lines: list[Line]) -> list[Paragraph]:
    """The document title and every heading, as scan-path elements.

    `read_lines` classifies a heading as non-prose, which is right for the
    length and semicolon checks and wrong for §4.12.3 — the title is the first
    thing on the scan path core §4.12.1 describes, and a heading that qualifies
    away its own claim is exactly what the rule screens for."""
    out: list[Paragraph] = []
    for line in lines:
        if line.in_fence or line.in_speculation:
            continue
        match = HEADING_RE.match(line.text.strip())
        if match:
            out.append(Paragraph(line.number, match.group(2), False,
                                 on_scan_path=True, is_heading=True))
    return out


# A sentence may also open with inline code, bold, italics, or a digit, so the
# lookahead admits their markers. Missing one merges two sentences into a single
# over-long count, which makes every §3.1 result on that paragraph wrong.
SENTENCE_END = re.compile(
    '(?<=[.!?])["\u2019\u201d\')\\]*_`]*\\s+'
    '(?=[`*_\u00a7\\[(\u201c"\\x00]*[A-Z0-9`*_\u00a7\\x00])')
CODE_SPAN = re.compile(r"`[^`]*`")


def split_sentences(text: str) -> list[str]:
    """A period inside a closing quote still ends a sentence.

    An inline code span is masked before splitting, so `a. B` does not split,
    and restored afterwards, so §3.1.3 can still count it."""
    spans: list[str] = []

    def mask(match: re.Match[str]) -> str:
        spans.append(match.group(0))
        return f"\x00{len(spans) - 1}\x00"

    masked = CODE_SPAN.sub(mask, text)
    parts = [p.strip() for p in SENTENCE_END.split(masked)]
    restored = [
        re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], p)
        for p in parts
    ]
    return [p for p in restored if p]


OPERATOR_RE = re.compile(r"[+\-*/^=<>\u2264\u2265\u00d7\u00f7\u2211\u220f\u222b]")


def count_words(sentence: str) -> int:
    """Core §3.1.3: one math symbol = 1 word; an inline expression containing any
    operator = 3 words."""
    total = 0
    for code in CODE_SPAN.findall(sentence):
        inner = code.strip("`")
        total += 3 if OPERATOR_RE.search(inner) else max(1, len(inner.split()))
    plain = CODE_SPAN.sub(" ", sentence)
    total += len([w for w in re.split(r"\s+", plain.strip()) if w])
    return total


# --------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------

@dataclass
class Finding:
    path: str
    line: int
    rule: str
    decidability: str
    detail: str

    def render(self) -> str:
        mark = {"L": "decided", "S": "screened", "J": "judgment"}[self.decidability]
        return f"{self.path}:{self.line}  ITWS §{self.rule} [{mark}]  {self.detail}"


def compile_matcher(pl: PhraseList, item: str) -> re.Pattern[str]:
    # Every list folds case. spec/phrases.md states the rule for all four kinds
    # — "matching is case-insensitive unless an entry says otherwise" — and no
    # entry says otherwise. Compiling `pattern` items case-sensitively narrows a
    # screened rule from inside the tool, which is the failure this file exists
    # to avoid: sentence-initial "No" and "Not only" stop producing candidates
    # and a reader is told to stop looking. The `<workbook>`-shaped false
    # positives that motivated the narrowing are handled where they belong, by
    # masking inline code spans in `screen_text` below.
    if pl.kind == "pattern":
        return re.compile(item, re.I)
    escaped = re.escape(item)
    # `\b` asserts a word/non-word transition, so appending it to a phrase
    # ending in punctuation ("certainly!") demands a word character after the
    # `!` and the entry can never match. Anchor only against a word edge that
    # actually exists.
    lead = r"\b" if item[:1].isalnum() or item[:1] == "_" else ""
    tail = r"\b" if item[-1:].isalnum() or item[-1:] == "_" else ""
    if pl.kind == "opener":
        return re.compile(rf"^{escaped}{tail}", re.I)
    return re.compile(rf"{lead}{escaped}{tail}", re.I)


def screen_text(text: str) -> str:
    """Blank every inline code span before phrase screening.

    A phrase inside backticks is a quoted token — a filename pattern, a schema
    placeholder, a leaked marker being named — not the document asserting it.
    The placeholder is a non-word character, so a `\\b` boundary still closes
    against it and a sentence opening with a code span cannot match an `opener`
    list at position 0."""
    return CODE_SPAN.sub("\x00", text)


def screen_phrase_lists(path: Path, paras: list[Paragraph],
                        lists: list[PhraseList],
                        headings: list[Paragraph]) -> list[Finding]:
    findings: list[Finding] = []
    for para in [*paras, *headings]:
        sentences = [screen_text(s) for s in split_sentences(para.text)]
        body = screen_text(para.text)
        for pl in lists:
            if pl.rule not in EVALUATED:
                continue
            if para.is_heading and pl.rule != "4.12.3":
                continue  # a heading is a scan-path element, not prose
            if pl.rule == "4.12.3" and not para.on_scan_path:
                continue  # core §4.12.1 bounds this rule to the scan path
            haystacks = sentences if pl.kind == "opener" else [body]
            for item in pl.items:
                matcher = compile_matcher(pl, item)
                for haystack in haystacks:
                    if matcher.search(haystack):
                        findings.append(Finding(
                            str(path), para.start, pl.rule, EVALUATED[pl.rule],
                            f'{pl.name}: "{item}"',
                        ))
                        break


    return findings


def check_sentence_length(path: Path, paras: list[Paragraph]) -> list[Finding]:
    """§3.1.1 caps a descriptive sentence at 25 words, §3.1.2 a load-bearing one
    at 20. Which cap applies is a reader's judgment, so a sentence between 21 and
    25 words is reported against §3.1.2 as a candidate, never as a decision."""
    findings: list[Finding] = []
    for para in paras:
        for sentence in split_sentences(para.text):
            words = count_words(sentence)
            if words > 25:
                findings.append(Finding(
                    str(path), para.start, "3.1.1", "S",
                    f"{words}-word sentence, over the 25-word descriptive cap: "
                    f"\u201c{sentence[:60]}\u2026\u201d",
                ))
            elif words > 20:
                findings.append(Finding(
                    str(path), para.start, "3.1.2", "S",
                    f"{words}-word sentence; over the 20-word cap if it is "
                    f"load-bearing \u2014 you decide which cap applies: "
                    f"\u201c{sentence[:60]}\u2026\u201d",
                ))
    return findings


def check_semicolons(path: Path, paras: list[Paragraph]) -> list[Finding]:
    """§3.8.1 prohibits a semicolon joining two independent clauses. A semicolon
    inside a list is permitted, so every hit is a candidate."""
    findings = []
    for para in paras:
        for sentence in split_sentences(para.text):
            if ";" in CODE_SPAN.sub("", sentence):
                findings.append(Finding(
                    str(path), para.start, "3.8.1", "S",
                    "semicolon \u2014 a finding only where it joins two "
                    "independent clauses",
                ))
    return findings


def check_declarations(path: Path, text: str, lines: list[Line],
                       profile_ids: set[str],
                       disclosure_values: set[str]) -> list[Finding]:
    """Core §0.5, §4.3.1, §4.3.4 — three declarations, a closed profile ID, a
    closed disclosure value, and the note form."""
    findings: list[Finding] = []
    head = text.split("\n## ", 1)[0]

    version = re.search(r"ITWS version:\**\s*([^\n·|]+)", head)
    profile = re.search(r"Profile:\**\s*`?([a-z-]+)`?", head)
    disclosure = re.search(r"AI disclosure:\**\s*([a-z]+)([^\n|]*)", head, re.I)

    if not version:
        findings.append(Finding(str(path), 1, "4.3.5", EVALUATED["4.3.5"],
                                "no `ITWS version` declaration in the front matter"))
    if not profile:
        findings.append(Finding(str(path), 1, "4.3.1", EVALUATED["4.3.1"],
                                "no `Profile` declaration in the front matter"))
    elif profile.group(1) not in profile_ids:
        findings.append(Finding(
            str(path), 1, "4.3.1", EVALUATED["4.3.1"],
            f"`{profile.group(1)}` is not a §0.1 profile ID "
            f"({', '.join(sorted(profile_ids))})",
        ))

    if not disclosure:
        findings.append(Finding(str(path), 1, "4.3.4", EVALUATED["4.3.4"],
                                "no `AI disclosure` declaration in the front matter"))
    else:
        value, note = disclosure.group(1).lower(), disclosure.group(2)
        if value not in disclosure_values:
            findings.append(Finding(
                str(path), 1, "4.3.4", EVALUATED["4.3.4"],
                f"`{value}` is not a §0.5 disclosure value "
                f"({', '.join(sorted(disclosure_values))})",
            ))
        elif value != "none" and not note.strip().startswith("—"):
            findings.append(Finding(
                str(path), 1, "4.3.4", EVALUATED["4.3.4"],
                f"`{value}` carries no provenance note "
                "(`<value> — <what the tooling did>`)",
            ))
    return findings


def check_bounded_blocks(path: Path, lines: list[Line]) -> list[Finding]:
    """§4.6.2 — a bounded block's first line carries exactly one bold bracketed
    label from the three permitted forms."""
    findings = []
    for line in lines:
        stripped = line.text.strip()
        if not stripped.startswith(">"):
            continue
        if re.match(r"^>\s*\*\*\[", stripped) and not BLOCK_LABEL_RE.match(stripped):
            findings.append(Finding(
                str(path), line.number, "4.6.2", "L",
                "bounded-block label is not one of "
                "**[Detail — <topic>]**, **[Intuition — <topic>]**, "
                "**[Speculation — <topic>]**",
            ))
    return findings


INFLECTION = {
    "show": "shows|showed|shown", "shows": "show|showed|shown",
    "confirms": "confirm|confirmed", "observed": "observe|observes",
    "indicates": "indicate|indicated", "suggests": "suggest|suggested",
    "decided": "decide|decides", "requires": "require|required",
    "propose": "proposes|proposed", "find": "finds|found",
    "hypothesize": "hypothesizes|hypothesized",
    "speculate": "speculates|speculated",
}


def inflected(phrase: str) -> str:
    """Core §5.6: grammatical inflection preserving the phrase is permitted.

    Matching the table's citation form alone misses "the record showed" and
    "we proposed", which are the same phrase carrying the same tier."""
    parts = []
    for word in phrase.split():
        alt = INFLECTION.get(word.lower())
        parts.append(f"(?:{re.escape(word)}|{alt})" if alt else re.escape(word))
    return r"\b" + r"\s+".join(parts) + r"\b"


def check_speculation_blocks(path: Path, paras: list[Paragraph],
                             tiers: dict[str, list[str]]) -> list[Finding]:
    """§7.3.3 — a speculation block uses only speculative-tier phrases.

    "we find" also has non-strength readings ("we find the socket already
    open"). §7.3.3 is `L` on the phrase itself, so the match stands as the
    specification states it, and a reader separates the two."""
    banned = [(tier, phrase) for tier, phrases in tiers.items()
              if tier != "speculative" for phrase in phrases]
    findings = []
    for para in paras:
        if not para.in_speculation:
            continue
        for tier, phrase in banned:
            if re.search(inflected(phrase), para.text, re.I):
                findings.append(Finding(
                    str(path), para.start, "7.3.3", "L",
                    f'speculation block carries the {tier}-tier phrase "{phrase}"',
                ))
    return findings


def check_section_length(path: Path, lines: list[Line]) -> list[Finding]:
    """§4.8.2 section ≤ 1,500 words; §4.8.3 subsection ≤ 600.

    Runs off the classified lines rather than the raw text. A `## ` inside a
    fenced example is not a heading, and fenced and tabular content is not
    prose, so counting either attributes words to the wrong section or to no
    section at all."""
    findings: list[Finding] = []
    heading, start, words = None, 0, 0
    level = 2

    def emit(name: str, line_no: int, count: int, lvl: int) -> None:
        cap, rule = (1500, "4.8.2") if lvl == 2 else (600, "4.8.3")
        if count > cap:
            findings.append(Finding(str(path), line_no, rule, EVALUATED[rule],
                                    f'"{name}" runs {count} words, over the {cap}-word cap'))

    for line in lines:
        match = None if line.in_fence else re.match(r"^(#{2,3})\s+(.*)$", line.text)
        if match:
            if heading is not None:
                emit(heading, start, words, level)
            heading, start, words = match.group(2), line.number, 0
            level = len(match.group(1))
        elif heading is not None and line.is_prose:
            words += len(prose_text(line).split())
    if heading is not None:
        emit(heading, start, words, level)
    return findings


# --------------------------------------------------------------------------
# Comment-hash recipe (maintenance-comment profile)
#
# The recipe lives in spec/profiles/maintenance-comment.md. This function is
# the computation that recipe describes. Expected hashes live in the fixture,
# not here: a hardcoded table in this file cannot be regenerated from the
# recipe, and would drift. `--self-test` recomputes every fixture hash.
# --------------------------------------------------------------------------

_STRING_PREFIXES = ("rf", "fr", "rb", "br", "r", "f", "b", "u")
_BLOCK_OPENERS = ("/**", "/*", "<!--", '"""', "'''")
_BLOCK_CLOSERS = ("*/", "-->", '"""', "'''")
_LINE_INTROS = ("///", "//!", "//", "#", "--")
_TRIPLE_QUOTES = ('"""', "'''")

REQUIRED_HASH_VECTORS = (
    "interior-indentation",
    "block-no-continuation-marker",
    "line-comments-differing-indents",
    "blank-interior-line",
    "non-ascii",
)


def _starts_with_block_opener(body: str) -> bool:
    if any(body.startswith(op) for op in _BLOCK_OPENERS):
        return True
    return any(
        body.startswith(prefix + quote)
        for prefix in _STRING_PREFIXES
        for quote in _TRIPLE_QUOTES
    )


def _strip_opener(line: str) -> str:
    body = line.lstrip(" \t")
    for prefix in _STRING_PREFIXES:
        for quote in _TRIPLE_QUOTES:
            token = prefix + quote
            if body.startswith(token):
                return body[len(token):]
    for opener in _BLOCK_OPENERS:
        if body.startswith(opener):
            return body[len(opener):]
    return line


def _strip_closer(line: str) -> str:
    trimmed = line.rstrip(" \t")
    for closer in _BLOCK_CLOSERS:
        if trimmed.endswith(closer):
            return trimmed[:-len(closer)]
    return line


def _strip_block_continuation(line: str) -> str:
    i = 0
    n = len(line)
    while i < n and line[i] in " \t":
        i += 1
    if i < n and line[i] == "*" and not line[i:].startswith("*/"):
        i += 1
        if i < n and line[i] == " ":
            i += 1
        return line[i:]
    return line


def _strip_line_introducer(line: str) -> str:
    i = 0
    n = len(line)
    while i < n and line[i] in " \t":
        i += 1
    rest = line[i:]
    for intro in _LINE_INTROS:
        if rest.startswith(intro):
            rest = rest[len(intro):]
            if rest.startswith(" "):
                rest = rest[1:]
            return rest
    return line


def normalize_comment(source: str) -> str:
    """Apply the maintenance-comment hash recipe, steps 1–7."""
    lines = source.split("\n")
    first = lines[0].lstrip(" \t") if lines else ""
    if _starts_with_block_opener(first):
        lines[0] = _strip_opener(lines[0])
        lines[-1] = _strip_closer(lines[-1])
        lines = [_strip_block_continuation(line) for line in lines]
    else:
        lines = [_strip_line_introducer(line) for line in lines]
    lines = [line.rstrip(" \t") for line in lines]
    return "\n".join(lines).strip()


def comment_hash(source: str) -> str:
    """SHA-256 of the normalized comment, lowercase hex (recipe steps 8–9)."""
    return hashlib.sha256(normalize_comment(source).encode("utf-8")).hexdigest()


def load_hash_vectors(path: Path) -> list[dict]:
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        records.append(json.loads(line))
    return records


def self_test_comment_hashes(fixture: Path) -> int:
    records = load_hash_vectors(fixture)
    ids = [r["id"] for r in records]
    missing = [v for v in REQUIRED_HASH_VECTORS if v not in ids]
    print(f"hash fixture: {fixture}")
    print(f"vectors: {len(records)}")
    failed = False
    if missing:
        print("FAIL — missing required vector: " + ", ".join(missing))
        failed = True
    for record in records:
        computed = comment_hash(record["source"])
        expected = record["sha256"]
        if computed != expected:
            print(
                f"FAIL — {record['id']}: computed {computed}, "
                f"fixture {expected}"
            )
            failed = True
        elif comment_hash(record["source"]) != computed:
            print(f"FAIL — {record['id']}: recipe is not deterministic")
            failed = True
    if failed:
        return 1
    print("OK — every vector's hash matches the recipe.")
    return 0


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def screen_file(path: Path, lists: list[PhraseList], profile_ids: set[str],
                disclosure_values: set[str],
                tiers: dict[str, list[str]]) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    lines = read_lines(text)
    paras = paragraphs(lines)
    headings = scan_path_headings(lines)
    findings = [
        *check_declarations(path, text, lines, profile_ids, disclosure_values),
        *screen_phrase_lists(path, paras, lists, headings),
        *check_sentence_length(path, paras),
        *check_semicolons(path, paras),
        *check_bounded_blocks(path, lines),
        *check_speculation_blocks(path, paras, tiers),
        *check_section_length(path, lines),
    ]
    return sorted(findings, key=lambda f: (f.line, _key(f.rule)))


def coverage_report(lists: list[PhraseList]) -> str:
    decided = sorted((r for r, d in EVALUATED.items() if d == "L"), key=_key)
    screened = sorted((r for r, d in EVALUATED.items() if d == "S"), key=_key)
    listed = sorted({pl.rule for pl in lists}, key=_key)
    unscreened = [r for r in listed if r not in EVALUATED]
    return "\n".join([
        "Coverage (ITWS §8, obligation 5 — this tool's own statement)",
        "",
        f"  Decided (D = L):  {', '.join('§' + r for r in decided)}",
        f"  Screened (D = S): {', '.join('§' + r for r in screened)}",
        f"  Phrase lists present but not screened: "
        f"{', '.join('§' + r for r in unscreened) if unscreened else 'none'}",
        "",
        "  NOT evaluated: every other rule in your load set, including every",
        "  rule marked D = J. This run establishes nothing about them, and",
        "  nothing about conformance at any decidability (ITWS §0.5, §8).",
        "  A screened finding is a candidate. You decide it.",
        "",
        "  §4.12.3 runs on an approximation of the §4.12.1 scan path: every",
        "  heading including the title, plus the whole opening paragraph of",
        "  each section rather than its first sentence, and with no appendix",
        "  detection. It over-includes, so a finding here may sit off the",
        "  real path. Read the path yourself before you decide one.",
    ])


def _key(rule: str) -> tuple[int, ...]:
    return tuple(int(part) for part in rule.split("."))


def unmatchable_items(lists: list[PhraseList]) -> list[tuple[str, str, str]]:
    """Every list entry that cannot match its own source string.

    The fixture guarantee is per rule ID, so one broken entry inside a working
    list stays invisible: `\\bcertainly!\\b` demanded a word character after the
    `!` and could never fire, while the rest of §2.6.11 kept the rule green.
    This asks each compiled matcher to find the string it was built from."""
    broken = []
    for pl in lists:
        for item in pl.items:
            probe = item if pl.kind != "pattern" else None
            if probe is None:
                try:
                    re.compile(item)
                except re.error as exc:
                    broken.append((pl.rule, item, f"will not compile: {exc}"))
                continue
            if not compile_matcher(pl, item).search(probe):
                broken.append((pl.rule, item, "matcher cannot match its own string"))
    return broken


def self_test(spec_dir: Path, fixture: Path, hash_fixture: Path) -> int:
    lists = parse_phrase_lists(spec_dir / "phrases.md")
    findings = screen_file(
        fixture, lists,
        parse_profile_ids(spec_dir / "core.md"),
        parse_disclosure_values(spec_dir / "core.md"),
        parse_strength_phrases(spec_dir / "core.md"),
    )
    hit = {f.rule for f in findings}
    expected = {pl.rule for pl in lists if pl.rule in EVALUATED}
    missed = sorted(expected - hit, key=_key)
    broken = unmatchable_items(lists)
    total_items = sum(len(pl.items) for pl in lists)
    print(f"fixture: {fixture}")
    print(f"phrase lists parsed from spec/phrases.md: {len(lists)}")
    print(f"screened rules exercised by the fixture: {len(expected - set(missed))}"
          f"/{len(expected)}")
    print(f"list entries that can match their own string: "
          f"{total_items - len(broken)}/{total_items}")
    phrase_failed = bool(missed or broken)
    if missed:
        print("FAIL — no finding for: " + ", ".join("§" + r for r in missed))
    for rule, item, why in broken:
        print(f"FAIL — §{rule} entry {item!r}: {why}")
    if not phrase_failed:
        print("OK — every screened list produced a finding, and every entry can match.")
    print()
    hash_rc = self_test_comment_hashes(hash_fixture)
    if phrase_failed or hash_rc:
        return 1
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Screen a corpus for the literal ITWS rules. Decides no "
                    "conformance question (ITWS §0.5, §8).")
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--json", action="store_true", help="machine-readable findings")
    parser.add_argument("--self-test", action="store_true", help="run the fixture")
    args = parser.parse_args(argv)

    here = Path(__file__).resolve().parent
    spec_dir = find_spec_dir(here)
    EVALUATED.update(parse_decidability(spec_dir))

    if args.self_test:
        return self_test(
            spec_dir,
            here / "fixtures" / "phrase-list-fixture.md",
            here / "fixtures" / "comment-hash-vectors.jsonl",
        )

    if not args.files:
        parser.error("name at least one file to screen")

    lists = parse_phrase_lists(spec_dir / "phrases.md")
    profile_ids = parse_profile_ids(spec_dir / "core.md")
    disclosure_values = parse_disclosure_values(spec_dir / "core.md")
    tiers = parse_strength_phrases(spec_dir / "core.md")

    findings: list[Finding] = []
    for path in args.files:
        findings.extend(screen_file(path, lists, profile_ids, disclosure_values, tiers))

    if args.json:
        print(json.dumps({
            "findings": [f.__dict__ for f in findings],
            "evaluated": EVALUATED,
            "not_evaluated": "every other rule in the load set, including every "
                             "rule marked D = J",
        }, indent=2))
        return 0

    for finding in findings:
        print(finding.render())
    print()
    print(f"{len(findings)} finding(s) across {len(args.files)} file(s).")
    print()
    print(coverage_report(lists))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

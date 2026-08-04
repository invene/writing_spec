#!/usr/bin/env python3
"""Decide the literal ITWS rules over a corpus, and report what was left undecided.

This tool is NOT part of ITWS. No rule refers to it, it is outside the load set,
and deleting it changes no obligation. It decides no conformance question: ITWS
§0.5 keeps conformance binary and textual, and a clean run here is a coverage
statement rather than a result.

Load the full seven-file rule set first, always. This tool replaces *reading for*
the literal rules. It never replaces loading them.

It carries no copy of any rule string. Every phrase list, profile ID, disclosure
value, and strength phrase is parsed from `spec/` at run time, so the tool cannot
drift from the specification it screens.

Usage:
    itws_literal.py FILE [FILE ...]        screen a corpus
    itws_literal.py --json FILE            machine-readable findings
    itws_literal.py --self-test            run the fixture

Exit status is 0 whenever the run completed. A finding is not an error: a person
decides every screened finding, and the exit code must never read as a verdict.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Rules this tool evaluates. Everything else in the load set is NOT evaluated,
# and `--coverage` says so. Keys are rule IDs; values are the D marker the
# specification carries for them (spec/legend.md).
EVALUATED = {
    "0.5": "L", "4.3.1": "L", "4.3.4": "L",
    "2.3.3": "L", "2.6.7": "L", "3.10.2": "L", "3.10.4": "L",
    "4.6.2": "L", "4.8.2": "L", "4.8.3": "L", "4.10.5": "L", "7.3.3": "L",
    "2.1.3": "S", "2.6.3": "S", "2.6.4": "S", "2.6.5": "S", "2.6.6": "S",
    "2.6.8": "S", "2.6.9": "S", "2.6.10": "S", "2.6.11": "S",
    "3.1.1": "S", "3.1.2": "S", "3.6.2": "S", "3.8.1": "S", "3.9.1": "S",
    "3.10.6": "S", "4.12.3": "S", "5.6.1": "S",
}

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


DECLARATION_RE = re.compile(r"^\**(ITWS version|Profile|AI disclosure)\**\s*:", re.I)
BLOCK_LABEL_RE = re.compile(r"^>\s*\*\*\[(Detail|Intuition|Speculation)\s+—\s+[^\]]+\]\*\*")


def read_lines(text: str) -> list[Line]:
    lines: list[Line] = []
    in_fence = False
    in_speculation = False
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            lines.append(Line(number, raw, False, in_speculation, False))
            continue

        if BLOCK_LABEL_RE.match(stripped):
            in_speculation = stripped.startswith(">") and "[Speculation" in stripped
        elif not stripped.startswith(">") and stripped:
            in_speculation = False

        is_declaration = bool(DECLARATION_RE.match(stripped.lstrip("> ").lstrip("-* ")))
        is_prose = not (
            in_fence
            or not stripped
            or stripped.startswith("#")
            or stripped.startswith("|")
            or set(stripped) <= set("-=*_ |:")
            or raw.startswith("    ")
            or raw.startswith("\t")
            or is_declaration
        )
        lines.append(Line(number, raw, is_prose, in_speculation, is_declaration))
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


def paragraphs(lines: list[Line]) -> list[Paragraph]:
    out: list[Paragraph] = []
    buf: list[str] = []
    start = 0
    spec = False
    for line in lines:
        if line.is_prose:
            if not buf:
                start, spec = line.number, line.in_speculation
            buf.append(prose_text(line).strip())
        elif buf:
            out.append(Paragraph(start, " ".join(buf), spec))
            buf = []
    if buf:
        out.append(Paragraph(start, " ".join(buf), spec))
    return out


SENTENCE_END = re.compile(r'(?<=[.!?])["\u2019\u201d\')\]]*\s+(?=[A-Z"\u201c(\[])')
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
        mark = {"L": "decided", "S": "screened"}[self.decidability]
        return f"{self.path}:{self.line}  ITWS §{self.rule} [{mark}]  {self.detail}"


def compile_matcher(pl: PhraseList, item: str) -> re.Pattern[str]:
    if pl.kind == "pattern":
        return re.compile(item, re.I)
    escaped = re.escape(item)
    if pl.kind == "opener":
        return re.compile(rf"^{escaped}\b", re.I)
    return re.compile(rf"\b{escaped}\b", re.I)


def screen_phrase_lists(path: Path, paras: list[Paragraph],
                        lists: list[PhraseList]) -> list[Finding]:
    findings: list[Finding] = []
    for para in paras:
        sentences = split_sentences(para.text)
        for pl in lists:
            if pl.rule not in EVALUATED:
                continue
            haystacks = sentences if pl.kind == "opener" else [para.text]
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
        findings.append(Finding(str(path), 1, "0.5", "L",
                                "no `ITWS version` declaration in the front matter"))
    if not profile:
        findings.append(Finding(str(path), 1, "4.3.1", "L",
                                "no `Profile` declaration in the front matter"))
    elif profile.group(1) not in profile_ids:
        findings.append(Finding(
            str(path), 1, "4.3.1", "L",
            f"`{profile.group(1)}` is not a §0.1 profile ID "
            f"({', '.join(sorted(profile_ids))})",
        ))

    if not disclosure:
        findings.append(Finding(str(path), 1, "4.3.4", "L",
                                "no `AI disclosure` declaration in the front matter"))
    else:
        value, note = disclosure.group(1).lower(), disclosure.group(2)
        if value not in disclosure_values:
            findings.append(Finding(
                str(path), 1, "4.3.4", "L",
                f"`{value}` is not a §0.5 disclosure value "
                f"({', '.join(sorted(disclosure_values))})",
            ))
        elif value != "none" and not note.strip().startswith("—"):
            findings.append(Finding(
                str(path), 1, "4.3.4", "L",
                f"`{value}` carries no scope-and-review note "
                "(`<value> — <what the tooling did>; reviewed by <who>`)",
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


def check_speculation_blocks(path: Path, paras: list[Paragraph],
                             tiers: dict[str, list[str]]) -> list[Finding]:
    """§7.3.3 \u2014 a speculation block uses only speculative-tier phrases."""
    banned = [(tier, phrase) for tier, phrases in tiers.items()
              if tier != "speculative" for phrase in phrases]
    findings = []
    for para in paras:
        if not para.in_speculation:
            continue
        for tier, phrase in banned:
            if re.search(rf"\b{re.escape(phrase)}\b", para.text, re.I):
                findings.append(Finding(
                    str(path), para.start, "7.3.3", "L",
                    f'speculation block carries the {tier}-tier phrase "{phrase}"',
                ))
    return findings


def check_section_length(path: Path, text: str) -> list[Finding]:
    """§4.8.2 section ≤ 1,500 words; §4.8.3 subsection ≤ 600."""
    findings: list[Finding] = []
    heading, start, words = None, 0, 0
    level = 2

    def emit(name: str, line_no: int, count: int, lvl: int) -> None:
        cap, rule = (1500, "4.8.2") if lvl == 2 else (600, "4.8.3")
        if count > cap:
            findings.append(Finding(str(path), line_no, rule, "L",
                                    f'"{name}" runs {count} words, over the {cap}-word cap'))

    for number, raw in enumerate(text.splitlines(), start=1):
        match = re.match(r"^(#{2,3})\s+(.*)$", raw)
        if match:
            if heading is not None:
                emit(heading, start, words, level)
            heading, start, words = match.group(2), number, 0
            level = len(match.group(1))
        elif heading is not None:
            words += len(raw.split())
    if heading is not None:
        emit(heading, start, words, level)
    return findings


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def screen_file(path: Path, lists: list[PhraseList], profile_ids: set[str],
                disclosure_values: set[str],
                tiers: dict[str, list[str]]) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    lines = read_lines(text)
    paras = paragraphs(lines)
    findings = [
        *check_declarations(path, text, lines, profile_ids, disclosure_values),
        *screen_phrase_lists(path, paras, lists),
        *check_sentence_length(path, paras),
        *check_semicolons(path, paras),
        *check_bounded_blocks(path, lines),
        *check_speculation_blocks(path, paras, tiers),
        *check_section_length(path, text),
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
    ])


def _key(rule: str) -> tuple[int, ...]:
    return tuple(int(part) for part in rule.split("."))


def self_test(spec_dir: Path, fixture: Path) -> int:
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
    print(f"fixture: {fixture}")
    print(f"phrase lists parsed from spec/phrases.md: {len(lists)}")
    print(f"screened rules exercised by the fixture: {len(expected - set(missed))}"
          f"/{len(expected)}")
    if missed:
        print("FAIL — no finding for: " + ", ".join("§" + r for r in missed))
        return 1
    print("OK — every screened phrase list produced at least one finding.")
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

    if args.self_test:
        return self_test(spec_dir, here / "fixtures" / "phrase-list-fixture.md")

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

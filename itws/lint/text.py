"""Shared text utilities for the lint checks.

Every helper is deterministic and uses only the standard library. The
sentence splitter and word counter implement the conventions that Rules
3.1.1–3.1.3 and 4.8.1 state, so one convention has one implementation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from itws.document import SourceUnit, StructuralManifest, split_sentence_text
INLINE_MATH_RE = re.compile(r"\$(?P<body>[^$\n]+)\$|`(?P<code>[^`\n]+)`")
MATH_OPERATOR_RE = re.compile(r"[+\-*/=<>≤≥±×÷^]")
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-]*")
ADMISSION_RE = re.compile(r"(?<!\*)\*(?P<italic>[^*\n]{2,60})\*(?!\*)|\*\*(?P<bold>[^*\n]{2,60})\*\*")
#: An acronym is an all-capital token that is not the prefix of a stable
#: identifier such as ``INV-1``: Rules 4.11.8 and 5.9.3 create those, and
#: §2.1.4 does not reach them.
ACRONYM_RE = re.compile(r"\b(?P<short>[A-Z][A-Z0-9]{1,7})s?\b(?!-?\d)")
EXPANSION_RE = re.compile(r"\b(?P<expansion>[A-Za-z][A-Za-z\-]*(?: [A-Za-z][A-Za-z\-]*){0,6}) \((?P<short>[A-Z][A-Z0-9]{1,7})s?\)")
SYMBOL_DEFINITION_RE = re.compile(r"\b(?:let|where|denote[sd]?|write)\b", re.IGNORECASE)
BOUNDED_BLOCK_RE = re.compile(r"\*\*\[(?P<label>[A-Za-z]+)(?: — (?P<topic>[^\]]*))?\]\*\*")
CROSS_REFERENCE_RE = re.compile(r"§\d+(?:\.\d+)*|\b(?:Figure|Table|Section|Rule) \d+")
POSITIONAL_REFERENCE_RE = re.compile(
    r"\b(?:as (?:previously|described|discussed) (?:above|below|earlier)|"
    r"(?:see|in) the (?:section|table|figure) (?:above|below)|"
    r"(?:above|below|earlier|previously) (?:in this|we))\b",
    re.IGNORECASE,
)

#: Function words that break a noun cluster under Rule 3.5.1.
FUNCTION_WORDS = frozenset(
    """
    a an the and or but nor for so yet of to in on at by with from into over under
    between among through during before after above below up down out off again
    further then once here there when where why how all any both each few more most
    other some such no not only own same than too very can will just should now
    is are was were be been being has have had do does did may might must shall
    this that these those it its their his her our your my we you they he she i
    if while because as per via about against across along around behind beneath
    beside besides beyond despite except inside near outside since toward towards
    underneath until upon within without
    one two three four five six seven eight nine ten
    first second third next last another every each
    """.split()
)

#: A determiner or preposition marks the start of a noun phrase. Rule 3.5.1
#: counts nouns inside one phrase, so the detector anchors on these.
NOUN_PHRASE_OPENERS = frozenset(
    """
    a an the this that these those its their our your my his her
    of to in on at by with from into over under between among through
    each every one both several many few no
    """.split()
)

#: Verb forms that break a noun cluster. The list is closed and small on
#: purpose: a false split costs a missed finding, a false join costs a false
#: candidate on a rule a reader still confirms.
CLUSTER_BREAKING_SUFFIXES = ("ing", "ed", "ly")

#: Finite verbs and relative pronouns that end a noun run. Many are also
#: plural-noun homographs, so the detector reports a candidate, not a
#: violation: Rule 3.5.1 is `partial` for exactly this reason.
CLUSTER_BREAKING_WORDS = frozenset(
    """
    is are was were be been being am has have had do does did
    who whom whose which what where when why either neither
    means makes allows prevents causes reflects shows suggests indicates
    remains becomes gives leads creates requires ensures returns accepts
    reads writes stores sends holds keeps drops lives names uses runs
    stops starts fails passes covers states applies depends loses
    began ran took gave held kept sent read wrote met set put found
    rose fell grew came went saw knew left cost
    """.split()
)

#: A stable identifier such as ``INV-1`` or ``CC-2`` is one token, not a noun
#: in a stack. Rules 4.11.8 and 5.9.3 create these deliberately.
IDENTIFIER_TOKEN_RE = re.compile(r"^[A-Z]{1,4}-?\d")

#: Auxiliaries and finite verbs that expose a bare demonstrative opener.
#: "This is" leaves the referent unnamed; "This queue" names it.
OPENER_FOLLOWERS = frozenset(
    """
    is are was were be been has have had will would can could may might
    must should shall does do did means makes allows prevents causes
    reflects shows suggests indicates remains becomes gives leads creates
    requires ensures happens occurs matters explains implies
    """.split()
)


@dataclass(frozen=True)
class Sentence:
    """One sentence with its position in the document."""

    text: str
    unit_id: str
    line: int
    offset: int

    @property
    def words(self) -> list[str]:
        return WORD_RE.findall(strip_inline_markup(self.text))

    @property
    def counted_length(self) -> int:
        """Word count under Rule 3.1.3."""
        return counted_word_length(self.text)


def strip_inline_markup(text: str) -> str:
    """Remove emphasis, link syntax, and inline code fences from ``text``."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    return text


def counted_word_length(text: str) -> int:
    """Count words the way Rule 3.1.3 requires.

    One mathematical symbol counts as one word. An inline expression that
    contains any operator counts as three words.
    """
    total = 0
    remainder = text
    for match in INLINE_MATH_RE.finditer(text):
        body = match.group("body") or match.group("code") or ""
        total += 3 if MATH_OPERATOR_RE.search(body) else 1
        remainder = remainder.replace(match.group(0), " ")
    total += len(WORD_RE.findall(strip_inline_markup(remainder)))
    return total


def unbalanced_math(text: str) -> bool:
    """Return whether inline math delimiters are unbalanced.

    An unbalanced delimiter makes the Rule 3.1.3 count undecidable.
    """
    without_math = INLINE_MATH_RE.sub(" ", text)
    return without_math.count("$") % 2 == 1 or without_math.count("`") % 2 == 1


def split_sentences(unit: SourceUnit) -> list[Sentence]:
    """Split one source unit into sentences, tracking start lines."""
    sentences: list[Sentence] = []
    for line_offset, raw_line in enumerate(unit.text.splitlines()):
        line = raw_line.strip()
        if not line:
            continue
        pieces = split_sentence_text(line)
        offset = 0
        for piece in pieces:
            if piece.strip():
                sentences.append(
                    Sentence(
                        text=piece.strip(),
                        unit_id=unit.id,
                        line=unit.span.start_line + line_offset,
                        offset=offset,
                    )
                )
            offset += len(piece)
    return sentences

def prose_units(manifest: StructuralManifest) -> list[SourceUnit]:
    """Every unit whose text is governed prose.

    Code fences, tables, and thematic breaks are excluded: §0.2 places code
    outside conformance, and a table is checked by Part 5 rules instead.
    """
    return [
        unit
        for unit in manifest.units
        if unit.node_type in {"paragraph", "list", "block_quote", "heading"}
    ]


def body_units(manifest: StructuralManifest) -> list[SourceUnit]:
    """Governed prose below the declaration region, headings excluded."""
    declaration_end = (
        manifest.declarations.span.end_line if manifest.declarations else 0
    )
    return [
        unit
        for unit in prose_units(manifest)
        if unit.node_type != "heading" and unit.span.start_line > declaration_end
    ]


def document_words(manifest: StructuralManifest) -> list[tuple[str, int]]:
    """Every prose word with its line number, in reading order."""
    words: list[tuple[str, int]] = []
    for unit in prose_units(manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            for word in WORD_RE.findall(strip_inline_markup(line)):
                words.append((word, unit.span.start_line + line_offset))
    return words


#: §0.4.1 gives these bold lowercase forms a conformance meaning. They are
#: not term admissions, and §4.10.2 also permits bold for template labels.
CONFORMANCE_KEYWORDS = frozenset(
    {"shall", "shall not", "should", "should not", "may"}
)


def admissions(manifest: StructuralManifest) -> list[tuple[str, int, str]]:
    """Terms the document admits, in reading order.

    A term admission is an italic or bold span, which Rules 2.3.1 and 4.10.2
    together reserve for that purpose. A §0.4.1 conformance keyword and a
    template label are excluded: neither admits a term.

    The scanner reports the form the author wrote. It does not judge whether
    the surrounding prose is a definition.
    """
    found: list[tuple[str, int, str]] = []
    seen: set[str] = set()
    for unit in prose_units(manifest):
        for line_offset, line in enumerate(unit.text.splitlines()):
            for match in ADMISSION_RE.finditer(line):
                term = (match.group("italic") or match.group("bold") or "").strip()
                if not term or term.endswith((":", ".")):
                    continue
                key = term.casefold()
                if key in CONFORMANCE_KEYWORDS or key in seen:
                    continue
                seen.add(key)
                found.append((term, unit.span.start_line + line_offset, unit.id))
    return found


def noun_clusters(sentence: Sentence) -> list[tuple[str, ...]]:
    """Return each candidate noun stack longer than three nouns.

    The detector is lexical, so it reports a candidate rather than a
    violation. A run counts only when a determiner or preposition opens it,
    every token is an uninflected non-function word, and no token is a
    stable identifier. A reader confirms the reading; the repair is always
    available (add a preposition).
    """
    clusters: list[tuple[str, ...]] = []
    run: list[str] = []
    anchored = False
    for word in sentence.words:
        lowered = word.casefold()
        if lowered in NOUN_PHRASE_OPENERS:
            if anchored and len(run) > 3:
                clusters.append(tuple(run))
            run = []
            anchored = True
            continue
        breaks = (
            lowered in FUNCTION_WORDS
            or lowered in CLUSTER_BREAKING_WORDS
            or any(lowered.endswith(suffix) for suffix in CLUSTER_BREAKING_SUFFIXES)
            or IDENTIFIER_TOKEN_RE.match(word)
            or not word[0].isalpha()
        )
        if breaks:
            if anchored and len(run) > 3:
                clusters.append(tuple(run))
            run = []
            anchored = False
        else:
            run.append(word)
    if anchored and len(run) > 3:
        clusters.append(tuple(run))
    return clusters


def syllables(word: str) -> int:
    """Count syllables with the standard vowel-group heuristic."""
    lowered = word.casefold()
    groups = re.findall(r"[aeiouy]+", lowered)
    count = len(groups)
    if lowered.endswith("e") and count > 1 and not lowered.endswith(("le", "ee")):
        count -= 1
    return max(count, 1)


def flesch_kincaid(sentences: list[Sentence]) -> dict[str, float]:
    """Flesch-Kincaid grade and reading ease. These never gate conformance."""
    words = [word for sentence in sentences for word in sentence.words]
    if not sentences or not words:
        return {"sentences": 0.0, "words": 0.0, "grade_level": 0.0, "reading_ease": 0.0}
    syllable_total = sum(syllables(word) for word in words)
    words_per_sentence = len(words) / len(sentences)
    syllables_per_word = syllable_total / len(words)
    grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    ease = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    return {
        "sentences": float(len(sentences)),
        "words": float(len(words)),
        "grade_level": round(grade, 2),
        "reading_ease": round(ease, 2),
    }

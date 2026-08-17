# ITWS legend — how to read this specification

**ITWS version:** 1.0

Load this file first. It fixes the notation used by every other ITWS file.

## Voice fence (read before anything else)

This specification is written in compressed notation for agent reading. **Governed documents are not.**

| Surface | Voice |
|---|---|
| ITWS spec files (this tree) | compressed: articles dropped, fragments, tables, symbols |
| Governed documents you write or rewrite | normal professional English, full sentences, ITWS rules |
| Findings, commit messages, chat replies to the user | normal professional English |

The compression is an input encoding. It never becomes an output style. A rewritten document that reads like this file has failed §3 and §4.

Good output: "The gateway rejects a token whose signature does not verify. Section 4 states the rejection response."

Bad output: "gateway → reject bad-sig token. see §4 for response."

## Rule table notation

Rules appear in tables:

| ID | C | D | Rule |
|---|---|---|---|
| 2.1.1 | M | J | word = one meaning, whole doc |

- **ID** — permanent rule identifier. Cite this in every finding: "ITWS §2.1.1". IDs are never reused or renumbered.
- **C** — class, and the rule's normative force:
  - `M` — **mandatory**. The strong default. Reads as *shall* / *shall not*. Apply unless applying it makes the passage worse. Then leave the passage and report the departure (core §0.5).
  - `R` — **recommended**. Reads as *should* / *should not*. Skip where it does not help. Skipping is not an `M` departure.
  - `P` — **permitted**. Reads as *may*. Creates no requirement.
- **D** — decidability: how much of the rule a machine settles without reading for meaning.
  - `L` — **literal**. A match, a count, or a closed-set test settles it. Reading for an `L` rule is unreliable: a closed list of nineteen prohibited words is not something prose review catches.
  - `S` — **screened**. A match or count finds every candidate. A reader decides each one. Most phrase-list rules are `S`, because the list carries exceptions the list itself states.
  - `J` — **judgment**. Nothing mechanical narrows the candidates. Spend attention here.
- **Rule** — the normative statement, compressed. The class column carries the modality; where a rule statement still spells out *shall*, *should*, or *may*, that word governs that clause.

`D` allocates attention. It changes no rule's force: an `L` and a `J` rule marked `M` are equally mandatory. A tool decides no conformance question (core §8).

A rule with a trigger applies only when the trigger is present: "if equation: ..." is inapplicable to a document with no equation. A rule with no trigger applies to every governed unit of every profile it is listed under.

## Symbols

| Symbol | Meaning |
|---|---|
| `→` | produces, maps to, replace with |
| `!` | prohibited, never |
| `+` | and, together with |
| `=` | is, equals |
| `≠` | is not |
| `≤` `≥` | at most, at least |
| `§n.n.n` | rule or section reference |
| `X \| Y` | X or Y (closed choice) |

## What is never compressed

Do not paraphrase, translate, or "clean up" any of these when reading or quoting them:

- Rule IDs and section numbers.
- The exact strings in [phrases.md](phrases.md) — they are matched literally.
- The exact strength phrases in core §5.6 — they are a closed vocabulary.
- Numbers, caps, thresholds, and version strings.
- Slot names in [profiles/](profiles/) — they are heading text.
- URLs, file paths, and code.

## Load order

1. `legend.md` (this file)
2. [ontology.md](ontology.md) — external standards ITWS borrows from
3. [core.md](core.md) — the shared normative core
4. [phrases.md](phrases.md) — literal prohibited and replacement strings
5. [glossary.md](glossary.md) — canonical admitted terms
6. [reader.md](reader.md) — what the assumed reader knows
7. [profiles/&lt;profile&gt;.md](profiles/) — exactly one profile

Load one profile. Never load two. [AGENTS.md](../AGENTS.md) states the full working sequence.

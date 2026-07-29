# Annex C — Rule index (generated)

**Status:** generated 2026-07-29 from ITWS 0.6.0-draft. Do not edit this annex by hand.

## C.1 Generation contract

For each rule of Parts 2–8, this annex records:

| Field | Source |
| --- | --- |
| Rule number | `#### Rule <n>` header; permanent under §0.8 |
| Short name | rule-header title |
| Class | `Class` metadata |
| Machine-checkable | `Machine-checkable` metadata |
| Profiles | `Profiles` metadata; absence means all profiles |
| Status | optional `Status` metadata; absence means active |
| Target | §1.6 `Navigation` metadata |
| Constructs | §1.6 `Constructs` metadata; the only navigation field with normative force |
| Layers | §1.6 `Navigation` metadata |
| Context | §1.6 `Navigation` metadata |
| Rewrite | §1.6 `Navigation` metadata |
| Precedence | derived from §1.4 through §1.6.3 |
| Source framework | `Source` metadata; feeds Annex F |
| File | the spec-relative file that holds the rule; §1.5.2 fixes it |

A scoped rule keeps its section number and sits in an overlay file. The `File` column lets a reader or tool load one profile's rules without reading unrelated overlays.

The full rule record, including chunk types, skeleton slots, resources, typed relations, examples, and source line ranges, is in `spec/generated/agent/rules.jsonl`. This annex is the human-readable view of the same model.

The index is sorted numerically by rule number. It is the input to the §8.1 checklist generator, which filters rules by declared ITWS version and profile before grouping them into the four self-check passes. Tier obligations come from §0.4.3 and Part 8; they are not rule-profile metadata.

## C.2 Generation command

Regenerate this index after changing rule metadata:

```text
python3 tools/itws_index.py \
  --spec-dir spec \
  --out spec/annexes/annex-c-rule-index.md
```

After approving a new permanent rule ID, add `--update-registry` once to append it to `spec/rule-ids.txt`.

The generator reads the core parts and the overlay files in `spec/overlays/`. It validates rule IDs against `spec/rule-ids.txt` independently of the output path. It fails on a duplicate or removed rule number, an unregistered new ID without `--update-registry`, malformed metadata, an unknown profile ID, a profile list outside canonical registry order, an unknown §1.6 navigation value, an unresolved rule relation, or a rule outside the file that §1.5.2 requires. A deprecated rule remains in its source file with `**Status:** deprecated since <version>; replacement <rule ID | none>`; generation never drops its permanent ID.

Regenerate the machine catalog in the same change:

```text
python3 tools/itws_compile.py --spec-dir spec
```

Generate a document's §8.1 checklist from this annex:

```text
python3 tools/itws_checklist.py \
  --spec-version 0.6.0-draft \
  --profile <canonical profile ID> \
  --tier <core | reviewed | publication> \
  --out <document-checklist.md>
```

## C.3 Index

**Rule count:** 195

| Rule | Short name | Class | Machine-checkable | Profiles | Status | Target | Constructs | Layers | Context | Rewrite | Precedence | Source | File |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1.1 | One word, one meaning | mandatory | partial | all profiles | active | term | admitted-term | both | document | review | 4 | ASD-STE100 | `02-words-and-vocabulary.md` |
| 2.1.2 | No synonym variation | mandatory | partial | all profiles | active | term | admitted-term | both | document | candidate | 4 | ASD-STE100 | `02-words-and-vocabulary.md` |
| 2.1.3 | Prefer the plain verb | recommended | yes | all profiles | active | word | verb | plain | local | mechanical | 4 | Google/Microsoft word lists, ASD-STE100 | `02-words-and-vocabulary.md` |
| 2.1.4 | Expand every acronym at first use | mandatory | yes | all profiles | active | term | acronym | both | document | candidate | 4 | Google/Microsoft style guides | `02-words-and-vocabulary.md` |
| 2.1.5 | One form per acronym after introduction | mandatory | yes | all profiles | active | term | acronym | both | document | candidate | 4 | Google/Microsoft style guides | `02-words-and-vocabulary.md` |
| 2.2.1 | The permitted-vocabulary test | mandatory | partial | all profiles | active | term | domain-term | both | document | review | 4 | original (baseline enumerated in Annex B) | `02-words-and-vocabulary.md` |
| 2.3.1 | Define before first use | mandatory | yes | all profiles | active | term | domain-term | both | document | review | 4 | original | `02-words-and-vocabulary.md` |
| 2.3.2 | Definitions stand only on lower rungs | mandatory | yes | all profiles | active | term | definition | both | document | review | 4 | original | `02-words-and-vocabulary.md` |
| 2.3.3 | No forward references | mandatory | yes | all profiles | active | term | domain-term | both | document | review | 4 | original | `02-words-and-vocabulary.md` |
| 2.3.4 | Definitions are operational | mandatory | no | all profiles | active | term | definition | exact | local | review | 4 | original | `02-words-and-vocabulary.md` |
| 2.4.1 | Substitutability | mandatory | no | all profiles | active | term | definition | exact | document | review | 4 | ISO 704 | `02-words-and-vocabulary.md` |
| 2.4.2 | No circular definitions | mandatory | partial | all profiles | active | term | definition | exact | document | review | 4 | ISO 704 | `02-words-and-vocabulary.md` |
| 2.4.3 | Genus and differentia | recommended | no | all profiles | active | term | definition | plain | local | candidate | 4 | ISO 704 | `02-words-and-vocabulary.md` |
| 2.4.4 | Definition length cap | mandatory | yes | all profiles | active | term | definition | plain | local | mechanical | 4 | original (per ISO 704 single-phrase convention, relaxed) | `02-words-and-vocabulary.md` |
| 2.4.5 | No definition by synonym or citation alone | mandatory | partial | all profiles | active | term | definition | exact | local | review | 4 | ISO 704, original | `02-words-and-vocabulary.md` |
| 2.5.1 | Documents do not contradict the glossary | mandatory | partial | all profiles | active | term | admitted-term | exact | collection | review | 4 | original | `02-words-and-vocabulary.md` |
| 2.5.2 | Use canonical wording at definitional first use | recommended | partial | all profiles | active | term | admitted-term | exact | collection | candidate | 4 | original | `02-words-and-vocabulary.md` |
| 2.5.3 | Recurring terms are proposed to the glossary | recommended | no | all profiles | active | term | admitted-term | plain | collection | prohibited | 4 | original | `02-words-and-vocabulary.md` |
| 2.6.1 | No jargon as shorthand | mandatory | partial | all profiles | active | sentence | domain-term | plain | local | candidate | 4 | PlainLanguage.gov | `02-words-and-vocabulary.md` |
| 2.6.2 | No opaque named artifacts | mandatory | partial | all profiles | active | term | name | plain | document | candidate | 4 | Google style guide, original | `02-words-and-vocabulary.md` |
| 2.6.3 | No unearned superlatives | mandatory | yes | all profiles | active | sentence | prohibited-phrase, measurement | plain | local | candidate | 4 | Google style guide, PlainLanguage.gov | `02-words-and-vocabulary.md` |
| 2.6.4 | The prohibited-word list (living) | mandatory | yes | all profiles | active | word | prohibited-phrase | plain | local | mechanical | 4 | Wikipedia "Signs of AI writing" | `02-words-and-vocabulary.md` |
| 2.6.5 | Agency language requires an operational definition | mandatory | partial | all profiles | active | sentence | verb | plain | document | review | 4 | original (extends Google's anthropomorphism guidance) | `02-words-and-vocabulary.md` |
| 2.6.6 | No warpath markers | mandatory | yes | all profiles | active | sentence | prohibited-phrase | plain | local | mechanical | 4 | original (phrase-level enforcement of §4.9) | `02-words-and-vocabulary.md` |
| 2.6.7 | No editorializing asides | mandatory | yes | all profiles | active | sentence | prohibited-phrase | plain | local | mechanical | 4 | Wikipedia "Signs of AI writing" | `02-words-and-vocabulary.md` |
| 2.6.8 | No vague attribution or source-count inflation | mandatory | partial | all profiles | active | sentence | citation, claim | exact | local | review | 4 | Wikipedia "Signs of AI writing" | `02-words-and-vocabulary.md` |
| 2.6.9 | No gap-speculation phrasing | mandatory | partial | all profiles | active | sentence | speculation | exact | local | review | 4 | Wikipedia "Signs of AI writing" | `02-words-and-vocabulary.md` |
| 2.6.10 | Connectives earn their place | mandatory | yes | all profiles | active | sentence | connective | plain | neighboring | mechanical | 4 | Wikipedia "Signs of AI writing" | `02-words-and-vocabulary.md` |
| 2.6.11 | No conversational or template artifacts | mandatory | yes | all profiles | active | sentence | tool-artifact | plain | local | mechanical | 4 | Wikipedia "Signs of AI writing" | `02-words-and-vocabulary.md` |
| 2.7.1 | Names are admitted like terms | mandatory | partial | all profiles | active | term | name | plain | document | candidate | 4 | original (extends §2.3) | `02-words-and-vocabulary.md` |
| 2.7.2 | Descriptive names over allusive names | recommended | no | all profiles | active | term | name | plain | document | review | 4 | Google naming conventions | `02-words-and-vocabulary.md` |
| 2.7.3 | One name per artifact | mandatory | partial | all profiles | active | term | name | both | document | candidate | 4 | Google naming conventions, ASD-STE100 | `02-words-and-vocabulary.md` |
| 2.7.4 | References to external artifacts are version-pinned | mandatory | partial | all profiles | active | citation | citation, name | exact | local | review | 4 | Google style guide, ML Reproducibility Checklist | `02-words-and-vocabulary.md` |
| 3.1.1 | Descriptive sentence cap | mandatory | yes | all profiles | active | sentence | any | plain | local | candidate | 4 | ASD-STE100 (adapted) | `03-sentences.md` |
| 3.1.2 | Load-bearing sentence cap | mandatory | partial | all profiles | active | sentence | claim | exact | local | candidate | 4 | ASD-STE100 (adapted) | `03-sentences.md` |
| 3.1.3 | Inline-math word counting | mandatory | yes | all profiles | active | sentence | equation | exact | local | mechanical | 4 | original | `03-sentences.md` |
| 3.1.4 | Split, never blur | mandatory | no | all profiles | active | sentence | claim | exact | local | review | 4 | original | `03-sentences.md` |
| 3.2.1 | One idea per sentence | mandatory | no | all profiles | active | sentence | any | plain | local | review | 4 | ASD-STE100 | `03-sentences.md` |
| 3.2.2 | One reviewable assertion per sentence | mandatory | no | all profiles | active | sentence | claim | exact | local | review | 4 | original (extends ASD-STE100) | `03-sentences.md` |
| 3.3.1 | Active voice by default | mandatory | partial | all profiles | active | sentence | verb | plain | local | candidate | 4 | ASD-STE100 + PlainLanguage.gov + Microsoft | `03-sentences.md` |
| 3.3.2 | "We" names the reporting actors | mandatory | partial | all profiles | active | sentence | pronoun | plain | local | candidate | 4 | original | `03-sentences.md` |
| 3.4.1 | Tense follows the table | mandatory | no | all profiles | active | sentence | verb | plain | local | candidate | 4 | ASD-STE100 + Google (adapted) | `03-sentences.md` |
| 3.4.2 | No ambiguous conditionals | mandatory | partial | all profiles | active | sentence | verb, hedge | exact | local | candidate | 4 | original | `03-sentences.md` |
| 3.5.1 | Three-noun cap | mandatory | partial | all profiles | active | sentence | noun-cluster | plain | local | candidate | 4 | ASD-STE100 | `03-sentences.md` |
| 3.5.2 | Admitted terms count as one noun | permitted | partial | all profiles | active | sentence | noun-cluster, admitted-term | plain | document | mechanical | 4 | original | `03-sentences.md` |
| 3.6.1 | Unambiguous antecedents | mandatory | no | all profiles | active | sentence | pronoun | plain | neighboring | candidate | 4 | ASD-STE100 + PlainLanguage.gov | `03-sentences.md` |
| 3.6.2 | No bare "this," "that," or "it" openers | mandatory | yes | all profiles | active | sentence | pronoun | plain | local | mechanical | 4 | Google + Microsoft (adapted) | `03-sentences.md` |
| 3.7.1 | "Only" sits next to what it modifies | mandatory | partial | all profiles | active | sentence | word | exact | local | candidate | 4 | Microsoft + Google | `03-sentences.md` |
| 3.7.2 | "Respectively" restricted | mandatory | yes | all profiles | active | sentence | list | exact | local | mechanical | 4 | Google + Microsoft (adapted) | `03-sentences.md` |
| 3.7.3 | One negation per clause | mandatory | partial | all profiles | active | sentence | word | plain | local | candidate | 4 | ASD-STE100 + PlainLanguage.gov | `03-sentences.md` |
| 3.7.4 | Explicit quantifier scope | mandatory | no | all profiles | active | sentence | generalization | exact | local | review | 4 | original (seeded by STE ambiguity rules) | `03-sentences.md` |
| 3.8.1 | No semicolon between independent clauses | mandatory | yes | all profiles | active | sentence | any | plain | local | mechanical | 4 | Google (tightened) | `03-sentences.md` |
| 3.8.2 | Serial comma | mandatory | yes | all profiles | active | sentence | list | plain | local | mechanical | 4 | Google | `03-sentences.md` |
| 3.8.3 | Connectives keep their reserved meaning | mandatory | partial | all profiles | active | sentence | connective | plain | local | candidate | 4 | ASD-STE100 + Google (adapted) | `03-sentences.md` |
| 3.9.1 | No vague hedges | mandatory | yes | all profiles | active | sentence | hedge | exact | local | mechanical | 4 | original (list seeded from PlainLanguage.gov and Wikipedia "Signs of AI writing") | `03-sentences.md` |
| 3.9.2 | Certainty language comes from §5.6 only | mandatory | partial | all profiles | active | sentence | hedge, claim | exact | local | candidate | 4 | original (mechanism forked from IPCC calibrated language) | `03-sentences.md` |
| 3.10.1 | No rule-of-three padding | mandatory | partial | all profiles | active | list | list | plain | local | review | 4 | Wikipedia "Signs of AI writing" | `03-sentences.md` |
| 3.10.2 | No negative parallelism | mandatory | yes | all profiles | active | sentence | prohibited-phrase | plain | local | mechanical | 4 | Wikipedia "Signs of AI writing" | `03-sentences.md` |
| 3.10.3 | No formulaic em dashes | mandatory | partial | all profiles | active | sentence | any | plain | local | candidate | 4 | Wikipedia "Signs of AI writing" | `03-sentences.md` |
| 3.10.4 | No trailing significance participles | mandatory | yes | all profiles | active | sentence | prohibited-phrase | plain | local | mechanical | 4 | Wikipedia "Signs of AI writing" | `03-sentences.md` |
| 3.10.5 | No false ranges | mandatory | partial | all profiles | active | sentence | quantity | exact | local | candidate | 4 | Wikipedia "Signs of AI writing" | `03-sentences.md` |
| 3.10.6 | No copula avoidance | mandatory | partial | all profiles | active | sentence | prohibited-phrase, verb | plain | local | mechanical | 4 | Wikipedia "Signs of AI writing" + ASD-STE100 (simple verbs) | `03-sentences.md` |
| 4.1.1 | One purpose per chunk | mandatory | partial | all profiles | active | chunk | any | both | local | review | 3 | Information Mapping | `04-structure.md` |
| 4.2.1 | Main point before qualification in a sentence | recommended | no | all profiles | active | sentence | any | plain | local | candidate | 3 | PlainLanguage.gov | `04-structure.md` |
| 4.2.2 | Chunk opens with its point | mandatory | partial | all profiles | active | chunk | any | plain | local | candidate | 3 | PlainLanguage.gov / pyramid principle | `04-structure.md` |
| 4.2.3 | Section opens with its takeaway or purpose | mandatory | no | all profiles | active | section | section | plain | section | review | 3 | pyramid principle | `04-structure.md` |
| 4.2.4 | Document states its main point before detail | mandatory | no | `design-rfc`, `decision-record`, `procedure`, `explanation`, `incident`, `technical-report`, `research-paper`, `epic`, `task` | active | document | any | plain | document | review | 3 | PlainLanguage.gov / IMRaD (adapted) | `04-structure.md` |
| 4.3.1 | Declare the profile | mandatory | yes | all profiles | active | declaration | declaration | exact | document | prohibited | 3 | Diátaxis (adapted) | `04-structure.md` |
| 4.3.2 | Stay in the profile job | mandatory | no | all profiles | active | document | any | both | document | review | 3 | Diátaxis | `04-structure.md` |
| 4.3.3 | Annex E required sections are present | mandatory | yes | all profiles | active | document | section | both | document | candidate | 3 | ISO/IEC/IEEE 26514 (adapted) | `04-structure.md` |
| 4.4.1 | Use the declared profile skeleton | mandatory | yes | all profiles | active | document | section | both | document | candidate | 3 | Diátaxis / IMRaD (adapted) | `04-structure.md` |
| 4.4.2 | Seed prerequisites before load-bearing detail | mandatory | partial | all profiles | active | document | domain-term | both | document | review | 3 | original | `04-structure.md` |
| 4.4.3 | State the main outcome plainly, then exactly | mandatory | no | `design-rfc`, `decision-record`, `procedure`, `incident`, `technical-report`, `research-paper`, `epic`, `task` | active | document | claim | both | document | review | 3 | original | `04-structure.md` |
| 4.5.1 | Headings are informative | mandatory | partial | all profiles | active | heading | heading | plain | section | candidate | 3 | PlainLanguage.gov / Google Developer Style Guide | `04-structure.md` |
| 4.6.1 | Exact detail beyond the plain layer goes in a bounded block or appendix | mandatory | no | all profiles | active | chunk | bounded-block | exact | section | review | 3 | original | `04-structure.md` |
| 4.6.2 | Bounded blocks use the standard markup | mandatory | yes | all profiles | active | bounded-block | bounded-block | both | local | mechanical | 3 | original | `04-structure.md` |
| 4.6.3 | Main text passes the skip test | mandatory | no | all profiles | active | document | bounded-block | both | document | review | 3 | original | `04-structure.md` |
| 4.7.1 | A section opens by locating itself | mandatory | no | all profiles | active | section | section | plain | section | candidate | 3 | original | `04-structure.md` |
| 4.7.2 | Forward pointers are few and explicit | recommended | partial | all profiles | active | section | cross-reference | plain | document | candidate | 3 | original | `04-structure.md` |
| 4.7.3 | Cross-references cite numbers, not positions | mandatory | yes | all profiles | active | sentence | cross-reference | both | document | mechanical | 3 | Google Developer Style Guide | `04-structure.md` |
| 4.8.1 | At most three term admissions per page | mandatory | yes | all profiles | active | document | domain-term | both | document | review | 3 | original | `04-structure.md` |
| 4.8.2 | Sections stay under the length ceiling | recommended | yes | all profiles | active | section | section | plain | section | candidate | 3 | original | `04-structure.md` |
| 4.8.3 | Subsections stay under the length ceiling | recommended | yes | all profiles | active | section | section | plain | section | candidate | 3 | original | `04-structure.md` |
| 4.9.1 | No residual-history asides | mandatory | partial | all profiles | active | sentence | prohibited-phrase | plain | local | candidate | 3 | Google Developer Style Guide (timeless documentation, extended) | `04-structure.md` |
| 4.9.2 | Necessary path information is promoted to a framed prior | mandatory | no | all profiles | active | chunk | any | both | section | review | 3 | original | `04-structure.md` |
| 4.9.3 | Every path reference passes delete-or-promote | mandatory | no | all profiles | active | sentence | any | both | section | review | 3 | original | `04-structure.md` |
| 4.10.1 | Headings use sentence case | mandatory | yes | all profiles | active | heading | heading | plain | local | mechanical | 3 | Wikipedia "Signs of AI writing" / Google Developer Style Guide | `04-structure.md` |
| 4.10.2 | Boldface is earned and rare | mandatory | partial | all profiles | active | sentence | any | plain | local | candidate | 3 | Wikipedia "Signs of AI writing" | `04-structure.md` |
| 4.10.3 | No inline-header lists in place of prose | mandatory | partial | all profiles | active | list | list | plain | local | candidate | 3 | Wikipedia "Signs of AI writing" | `04-structure.md` |
| 4.10.4 | No tables for what a sentence says better | recommended | partial | all profiles | active | table | table | plain | local | review | 3 | Wikipedia "Signs of AI writing" | `04-structure.md` |
| 4.10.5 | No emoji | mandatory | yes | all profiles | active | document | any | plain | local | mechanical | 3 | Wikipedia "Signs of AI writing" | `04-structure.md` |
| 4.10.6 | No canned section formulas | mandatory | partial | all profiles | active | section | section | plain | section | review | 3 | Wikipedia "Signs of AI writing" | `04-structure.md` |
| 4.11.1 | Epic titles state the strategic outcome | mandatory | partial | `epic` | active | heading | title | exact | document | candidate | 3 | PlainLanguage.gov / original | `overlays/epic/rules.md` |
| 4.11.2 | User-journey task titles state the journey | mandatory | partial | `task` | active | heading | title, user-journey | exact | document | candidate | 3 | original | `overlays/task/rules.md` |
| 4.11.3 | Engineering-only task titles state the technical outcome | mandatory | partial | `task` | active | heading | title | exact | document | candidate | 3 | original | `overlays/task/rules.md` |
| 4.11.4 | Subtask titles state the contribution | mandatory | partial | `subtask` | active | heading | title | exact | document | candidate | 3 | original | `overlays/subtask/rules.md` |
| 4.11.5 | Tasks declare both classifications | mandatory | yes | `task` | active | document | declaration | exact | document | review | 3 | original | `overlays/task/rules.md` |
| 4.11.6 | Defect corrections identify the violated contract | mandatory | partial | `task` | active | document | requirement | exact | document | review | 3 | ISO/IEC/IEEE 26514 / original | `overlays/task/rules.md` |
| 4.11.7 | Engineering-only tasks identify their support | mandatory | partial | `task` | active | document | invariant | exact | document | review | 3 | original | `overlays/task/rules.md` |
| 4.11.8 | Epic invariants have stable identifiers | mandatory | yes | `epic` | active | document | invariant | exact | document | mechanical | 3 | ISO/IEC/IEEE 26514 / original | `overlays/epic/rules.md` |
| 4.11.9 | Children preserve inherited invariants | mandatory | no | `task`, `subtask` | active | document | invariant | exact | collection | prohibited | 3 | ISO/IEC/IEEE 26514 / original | `overlays/shared/work-item.md` |
| 4.11.10 | Epics remain strategic | mandatory | no | `epic` | active | document | any | both | document | review | 3 | Diátaxis / original | `overlays/epic/rules.md` |
| 4.11.11 | Tasks are independently acceptable | mandatory | no | `task` | active | document | any | exact | collection | review | 3 | original | `overlays/task/rules.md` |
| 4.11.12 | Subtasks name one parent | mandatory | yes | `subtask` | active | document | parent-link | exact | collection | prohibited | 3 | original | `overlays/subtask/rules.md` |
| 4.11.13 | Subtasks name one parent condition | mandatory | yes | `subtask` | active | document | parent-link | exact | collection | prohibited | 3 | original | `overlays/subtask/rules.md` |
| 4.11.14 | Independent outcomes use task | mandatory | no | `task`, `subtask` | active | document | any | exact | collection | prohibited | 3 | original | `overlays/shared/work-item.md` |
| 4.11.15 | Tasks summarize delegated sad paths | mandatory | partial | `task` | active | document | user-journey | exact | collection | review | 3 | IEC/IEEE 82079-1 / original | `overlays/task/rules.md` |
| 4.11.16 | Aggregate sad paths stay with the task | mandatory | no | `task` | active | document | user-journey | exact | collection | prohibited | 3 | original | `overlays/task/rules.md` |
| 4.11.17 | Technical hints do not carry normative content | mandatory | partial | `task`, `subtask` | active | chunk | any | exact | local | review | 3 | ISO/IEC Directives Part 2 / original | `overlays/shared/work-item.md` |
| 4.11.18 | Happy paths state the complete journey | mandatory | partial | `task` | active | document | user-journey | exact | document | review | 3 | ISO/IEC/IEEE 26514 / original | `overlays/task/rules.md` |
| 4.11.19 | Sad paths state failure and recovery | mandatory | partial | `task` | active | document | user-journey | exact | document | review | 3 | IEC/IEEE 82079-1 / original | `overlays/task/rules.md` |
| 4.11.20 | Engineering success paths state the technical outcome | mandatory | partial | `task` | active | document | any | exact | document | review | 3 | ISO/IEC/IEEE 26514 / original | `overlays/task/rules.md` |
| 4.11.21 | Engineering failure paths state recovery | mandatory | partial | `task` | active | document | any | exact | document | review | 3 | IEC/IEEE 82079-1 / original | `overlays/task/rules.md` |
| 5.1.1 | Simplification preserves exact meaning | mandatory | no | all profiles | active | chunk | claim | both | neighboring | prohibited | 1 | original | `05-mathematical-and-empirical-content.md` |
| 5.1.2 | Simplified statements trace to exact statements | mandatory | partial | all profiles | active | chunk | cross-reference, claim | both | document | candidate | 1 | original | `05-mathematical-and-empirical-content.md` |
| 5.2.1 | Define every non-baseline symbol at first use | mandatory | partial | all profiles | active | symbol | symbol | exact | document | review | 1 | original (mechanism from §2.3) | `05-mathematical-and-empirical-content.md` |
| 5.2.2 | One symbol, one meaning | mandatory | yes | all profiles | active | symbol | symbol | exact | document | review | 1 | ASD-STE100 (adapted) | `05-mathematical-and-empirical-content.md` |
| 5.2.3 | Notation table above six symbols | mandatory | yes | all profiles | active | table | symbol, table | exact | document | candidate | 1 | original | `05-mathematical-and-empirical-content.md` |
| 5.3.1 | Every displayed equation gets a plain-language reading | mandatory | partial | all profiles | active | equation | equation | both | local | review | 1 | original | `05-mathematical-and-empirical-content.md` |
| 5.3.2 | Keep inline math atomic | mandatory | partial | all profiles | active | equation | equation | exact | local | candidate | 1 | original | `05-mathematical-and-empirical-content.md` |
| 5.4.1 | Material statements carry a complete evidence record | mandatory | partial | all profiles | active | chunk | claim, measurement | exact | document | review | 1 | ISO/IEC/IEEE 26514; IEC 82079-1; APA JARS / NeurIPS checklist (research adaptation) | `05-mathematical-and-empirical-content.md` |
| 5.4.2 | No naked percentages | mandatory | partial | all profiles | active | sentence | quantity | exact | local | review | 1 | ISO/IEC/IEEE 26514; APA JARS (effect size + uncertainty, restated) | `05-mathematical-and-empirical-content.md` |
| 5.4.3 | Every citation resolves | mandatory | yes | all profiles | active | citation | citation | exact | document | prohibited | 1 | Wikipedia "Signs of AI writing" (citations) | `05-mathematical-and-empirical-content.md` |
| 5.4.4 | Cited sources support the claim | mandatory | no | all profiles | active | citation | citation, claim | exact | collection | prohibited | 1 | Wikipedia "Signs of AI writing" (citations) | `05-mathematical-and-empirical-content.md` |
| 5.4.5 | Source counts are accurate | mandatory | partial | all profiles | active | sentence | citation | exact | local | candidate | 1 | Wikipedia "Signs of AI writing" (source-count inflation) | `05-mathematical-and-empirical-content.md` |
| 5.5.1 | Label axes, units, and series completely | mandatory | partial | all profiles | active | figure | figure | exact | local | review | 1 | APA / IEEE figure conventions | `05-mathematical-and-empirical-content.md` |
| 5.5.2 | The caption states the takeaway | mandatory | no | all profiles | active | figure | figure, table | both | local | candidate | 1 | ISO/IEC/IEEE 26514; Nature-style figure guidance | `05-mathematical-and-empirical-content.md` |
| 5.5.3 | Figures stand alone for the assumed reader | mandatory | partial | all profiles | active | figure | figure, admitted-term | plain | document | review | 1 | original | `05-mathematical-and-empirical-content.md` |
| 5.6.1 | Strength and authority language comes from the table only | mandatory | partial | all profiles | active | sentence | claim | exact | local | candidate | 1 | IPCC calibrated language (mechanism) | `05-mathematical-and-empirical-content.md` |
| 5.6.2 | Strength matches the evidential standard | mandatory | no | all profiles | active | sentence | claim | exact | document | prohibited | 1 | IPCC calibrated language (mechanism) | `05-mathematical-and-empirical-content.md` |
| 5.7.1 | Admit ladder-required statistical concepts before use | mandatory | partial | `technical-report`, `research-paper` | active | term | statistic | exact | document | review | 1 | original (mechanism from §2.3) | `overlays/shared/report.md` |
| 5.7.2 | Headline statistical results use bare concepts | mandatory | no | `technical-report`, `research-paper` | active | sentence | statistic | both | document | review | 1 | original | `overlays/shared/report.md` |
| 5.8.1 | Reports include the applicable checkability statement | mandatory | yes | `technical-report`, `research-paper` | active | document | section | exact | document | candidate | 1 | ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS checklist / ML Reproducibility Checklist (research adaptation) | `overlays/shared/report.md` |
| 5.8.2 | The statement reads in assumed-reader vocabulary | mandatory | partial | `technical-report`, `research-paper` | active | section | section | plain | document | review | 1 | original | `overlays/shared/report.md` |
| 5.9.1 | One definition of done per work item | mandatory | yes | `epic`, `task`, `subtask` | active | document | section | exact | document | candidate | 1 | original | `overlays/shared/work-item.md` |
| 5.9.2 | Completion conditions state the pass test | mandatory | partial | `epic`, `task`, `subtask` | active | chunk | requirement | exact | local | review | 1 | ISO/IEC/IEEE 26514; IEC/IEEE 82079-1 | `overlays/shared/work-item.md` |
| 5.9.3 | Task conditions have stable identifiers | mandatory | yes | `task` | active | chunk | requirement | exact | document | mechanical | 1 | original | `overlays/task/rules.md` |
| 5.9.4 | Subtask evidence verifies the parent condition | mandatory | partial | `subtask` | active | document | parent-link | exact | collection | review | 1 | ISO/IEC/IEEE 26514 / original | `overlays/subtask/rules.md` |
| 5.9.5 | Tasks verify integrated behavior | mandatory | partial | `task` | active | document | requirement | exact | document | review | 1 | original | `overlays/task/rules.md` |
| 5.9.6 | Closed subtasks do not close the task | mandatory | partial | `task` | active | document | requirement | exact | collection | prohibited | 1 | original | `overlays/task/rules.md` |
| 5.9.7 | Epic completion verifies outcome and invariants | mandatory | partial | `epic` | active | document | invariant | exact | collection | review | 1 | ISO/IEC/IEEE 26514 / original | `overlays/epic/rules.md` |
| 5.9.8 | Every completion condition must pass | mandatory | partial | `epic`, `task`, `subtask` | active | document | requirement | exact | collection | prohibited | 1 | original | `overlays/shared/work-item.md` |
| 6.1.1 | Anchor analogies in assumed-reader vocabulary | mandatory | no | all profiles | active | chunk | analogy | plain | local | review | 3 | original | `06-explanatory-devices.md` |
| 6.1.2 | State the breaking point | mandatory | partial | all profiles | active | chunk | analogy | plain | local | review | 3 | original | `06-explanatory-devices.md` |
| 6.1.3 | At most one analogy per concept | mandatory | partial | all profiles | active | chunk | analogy | plain | document | review | 3 | original | `06-explanatory-devices.md` |
| 6.2.1 | Central mechanisms get a worked example | mandatory | no | all profiles | active | chunk | worked-example | plain | section | review | 3 | Carroll minimalism | `06-explanatory-devices.md` |
| 6.2.2 | Examples carry no incidental complexity | mandatory | no | all profiles | active | chunk | worked-example | plain | local | candidate | 3 | Carroll minimalism / Google style guide | `06-explanatory-devices.md` |
| 6.2.3 | Examples use realistic values | recommended | no | all profiles | active | chunk | worked-example | plain | local | review | 3 | Google style guide | `06-explanatory-devices.md` |
| 6.3.1 | Intuition is bounded and labeled | mandatory | yes | all profiles | active | bounded-block | bounded-block | plain | local | mechanical | 3 | ASD-STE100 (note blocks) | `06-explanatory-devices.md` |
| 6.3.2 | Exact content does not live only in intuition blocks | mandatory | partial | all profiles | active | bounded-block | bounded-block, requirement | exact | document | prohibited | 3 | ISO/IEC Directives Part 2 | `06-explanatory-devices.md` |
| 6.3.3 | Main text survives block removal | mandatory | no | all profiles | active | document | bounded-block | both | document | review | 3 | original | `06-explanatory-devices.md` |
| 6.4.1 | Diagram structures that prose cannot carry | recommended | no | all profiles | active | figure | diagram | plain | section | review | 3 | ISO/IEC/IEEE 26514 / IEC 82079-1 | `06-explanatory-devices.md` |
| 6.4.2 | Every diagram is referenced from the text | mandatory | yes | all profiles | active | figure | diagram, cross-reference | plain | document | mechanical | 3 | ISO/IEC/IEEE 26514 | `06-explanatory-devices.md` |
| 6.4.3 | Diagram labels use admitted terms only | mandatory | yes | all profiles | active | figure | diagram, admitted-term | plain | document | review | 3 | original | `06-explanatory-devices.md` |
| 6.4.4 | Diagrams carry alt text | recommended | yes | all profiles | active | figure | diagram | plain | local | candidate | 3 | Google style guide | `06-explanatory-devices.md` |
| 6.5.1 | Repeat verbatim or not at all | mandatory | partial | all profiles | active | sentence | admitted-term, claim | both | document | review | 3 | ASD-STE100 | `06-explanatory-devices.md` |
| 6.5.2 | Recall distant definitions at reuse | recommended | yes | all profiles | active | sentence | admitted-term | plain | document | candidate | 3 | original (instructional-design spaced recall) | `06-explanatory-devices.md` |
| 6.5.3 | Recap the ladder at part boundaries | permitted | yes | all profiles | active | section | section | plain | section | candidate | 3 | original | `06-explanatory-devices.md` |
| 6.5.4 | No hollow summaries | mandatory | partial | all profiles | active | chunk | prohibited-phrase | plain | section | candidate | 3 | Wikipedia "Signs of AI writing" | `06-explanatory-devices.md` |
| 7.1.1 | Boundary material is required | mandatory | partial | all profiles | active | document | limitation | exact | document | candidate | 1 | ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS Paper Checklist (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.1.2 | State the scope of validity | mandatory | no | all profiles | active | chunk | limitation | exact | document | review | 1 | ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS Paper Checklist / Model Cards (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.1.3 | Disclose known failure modes and adverse effects | mandatory | no | all profiles | active | chunk | limitation, risk | exact | document | review | 1 | ISO/IEC/IEEE 26514; IEC 82079-1; Model Cards (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.1.4 | Disclose what was not tested or verified | mandatory | no | all profiles | active | chunk | limitation | exact | document | review | 1 | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / Datasheets for Datasets (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.1.5 | Disclose data limitations | mandatory | no | all profiles | active | chunk | limitation, measurement | exact | document | review | 1 | ISO/IEC/IEEE 26514; Datasheets for Datasets (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.1.6 | Plausible boundary gaps are explicit | mandatory | partial | all profiles | active | chunk | limitation | exact | document | review | 1 | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.2.1 | Caveats attach to their claims | mandatory | no | all profiles | active | chunk | caveat, claim | exact | neighboring | review | 1 | IEC 82079-1 / ASD-STE100 (warning placement) | `07-limitations-caveats-interpretation.md` |
| 7.2.2 | Boundary material aggregates, it does not replace | mandatory | no | all profiles | active | document | caveat | exact | document | review | 1 | IEC 82079-1 | `07-limitations-caveats-interpretation.md` |
| 7.3.1 | Separate observation from interpretation | mandatory | partial | `incident`, `technical-report`, `research-paper`, `investigation-log`, `task`, `subtask` | active | chunk | observation | exact | local | review | 1 | ISO/IEC/IEEE 26514; IMRaD / APA JARS (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.3.2 | Speculation only in marked blocks | mandatory | yes | `incident`, `technical-report`, `research-paper`, `investigation-log`, `task`, `subtask` | active | bounded-block | speculation | exact | local | mechanical | 1 | original (§6.3 mechanism) | `07-limitations-caveats-interpretation.md` |
| 7.3.3 | Speculation uses the speculative tier | mandatory | partial | `incident`, `technical-report`, `research-paper`, `investigation-log`, `task`, `subtask` | active | bounded-block | speculation | exact | local | candidate | 1 | IPCC calibrated language (via §5.6) | `07-limitations-caveats-interpretation.md` |
| 7.4.1 | Extrapolations name the target setting | mandatory | no | all profiles | active | sentence | generalization | exact | document | review | 1 | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / APA JARS (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 7.4.2 | Beyond the boundary, drop evidential strength | mandatory | partial | all profiles | active | sentence | generalization, claim | exact | document | candidate | 1 | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / CONSORT (research adaptation) | `07-limitations-caveats-interpretation.md` |
| 8.1.1 | Checklist is generated, not authored | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | STE checker workflows | `08-review-compliance-tooling.md` |
| 8.1.2 | Four self-check passes | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.1.3 | Regeneration on rule change | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.2.1 | Lint gate | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | STE checker practice | `08-review-compliance-tooling.md` |
| 8.2.2 | Severity maps to rule class | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.2.3 | Version-pinned checking | mandatory | yes | all profiles | active | conformance-record | declaration | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.2.4 | Machine checks do not close human gates | mandatory | no | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.3.1 | Publication gate | mandatory | no | all profiles | active | conformance-record | any | both | document | prohibited | 4 | ISO 26514 / plain-language testing practice | `08-review-compliance-tooling.md` |
| 8.3.2 | Participant sampling | mandatory | no | all profiles | active | conformance-record | any | both | document | prohibited | 4 | plain-language testing practice | `08-review-compliance-tooling.md` |
| 8.3.3 | Protocol and pass criteria | mandatory | no | all profiles | active | conformance-record | any | both | document | prohibited | 4 | teach-back method, adapted | `08-review-compliance-tooling.md` |
| 8.3.4 | Reader-test failures are recorded | mandatory | no | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.3.5 | Failed documents are revised and independently retested | mandatory | no | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.4.1 | Reviewed tiers use two independent roles | mandatory | no | all profiles | active | conformance-record | any | both | document | prohibited | 4 | ISO 26514 / IEC 82079-1 review process | `08-review-compliance-tooling.md` |
| 8.4.2 | Subject-matter-owner scope | mandatory | no | all profiles | active | conformance-record | any | exact | document | prohibited | 4 | ISO 26514, renamed to §1.2 | `08-review-compliance-tooling.md` |
| 8.4.3 | Assumed-reader proxy scope | mandatory | no | all profiles | active | conformance-record | any | plain | document | prohibited | 4 | ISO 26514, renamed to §1.2 | `08-review-compliance-tooling.md` |
| 8.4.4 | Findings cite rules | mandatory | partial | all profiles | active | conformance-record | cross-reference | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.5.1 | Deviation requires a recorded waiver | mandatory | partial | all profiles | active | conformance-record | waiver | both | document | prohibited | 4 | IEC 82079-1 / engineering-standard practice | `08-review-compliance-tooling.md` |
| 8.5.2 | Waiver content | mandatory | yes | all profiles | active | conformance-record | waiver | both | document | mechanical | 4 | engineering-standard practice | `08-review-compliance-tooling.md` |
| 8.6.1 | Generated artifacts satisfy the generation contract | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.6.2 | Stale artifacts are rejected, not reused | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.6.3 | Validation reports one of four states | mandatory | yes | all profiles | active | conformance-record | any | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.6.4 | Agent-authored judgments cite their support | mandatory | partial | all profiles | active | conformance-record | cross-reference | both | document | prohibited | 4 | original | `08-review-compliance-tooling.md` |
| 8.6.5 | Colliding rewrites are reported, not merged | mandatory | yes | all profiles | active | conformance-record | any | both | collection | prohibited | 4 | original | `08-review-compliance-tooling.md` |

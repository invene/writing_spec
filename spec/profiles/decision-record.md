# Profile: `decision-record`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Record a decision, its context, the alternatives considered, and its consequences.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the decision, its status, the main reason, and its material consequence or boundary.**

## Reader overlay (genre knowledge only)

The reader recognizes a compact record of status, context, decision, and consequences, and expects an explicit recorded decision. Navigation only.

## Skeleton

Dependency order: state the decision plainly, then seed context and terms before the exact decision and consequences (core §4.4.2).

`Summary` carries the plain member of the §4.4.3 plain/exact pair; `Decision` carries the exact member. `Summary` precedes `Context` because the reader needs the destination before the forces that produced it. `Decision` follows `Alternatives` because its scope depends on terms admitted there.

| Slot | Required | Job |
|---|---|---|
| Status | yes | proposed, accepted, superseded, or another defined state; identify a superseding record when one exists |
| Summary | yes | the decision in one or two sentences of assumed-reader vocabulary, before any supporting detail; links to `Decision` under §5.1.2 |
| Context | yes | the durable facts, forces, and constraints that made a decision necessary |
| Alternatives | yes | credible options considered, including no change where relevant, and why they were not selected |
| Decision | yes | the exact restatement of `Summary`: selected option in direct present-tense language, with scope, thresholds, identifiers |
| Consequences | yes | expected benefits, costs, trade-offs, follow-on work, and conditions that would justify revisiting |

**Renames:** `Alternatives` → `Options considered` · `Decision` → `Outcome` · `Consequences` → `Consequences and trade-offs`.

**Merges:** none. `Status` may appear as a front-matter field immediately before `Context`; that satisfies the slot but does not make status optional.

## Boundary locations (core §7.1)

- **Context** — environment, version, dependency bounds.
- **Alternatives** — capacity, security, privacy, data, reversibility trade-offs.
- **Consequences** — accepted failure, recovery, duration, unknown boundaries.

## Evidence-record additions (core §5.4)

The decision state and date, the options considered, and the consequences or trade-offs accepted.

## Applicable core rules with profile scope

§4.2.4 and §4.4.3 both apply. §7.3 is optional here.

## Scoped rules

None. Every obligation comes from core.

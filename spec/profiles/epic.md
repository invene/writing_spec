# Profile: `epic`

**ITWS version:** 1.0 · **Surface:** `markdown-document` · **Family:** work-item

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Define one strategic product outcome, its scope, success measures, technical invariants, cross-task risks, and child-task boundaries.

An `epic` is a concise product requirements document. It states product strategy and technical invariants. It holds **no** child-task acceptance detail and **no** implementation design.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the strategic outcome, its §5.6 strength, the scope boundary, and the success-measure boundary.**

## Work-item vocabulary

Available without definition in `epic`, `task`, and `subtask`.

**work item** — a governed `epic`, `task`, or `subtask`. **strategic outcome** — one requiring several independently acceptable tactical outcomes. **tactical outcome** — one accepted at a single product or technical boundary. **technical boundary** — an interface, invariant, operational state, or artifact engineering can verify. **technical invariant** — a stable property every applicable child work item must preserve. **user journey** — one actor's path from a stated starting condition to an observable outcome. **happy path** — a journey path reaching the intended outcome under expected conditions. **sad path** — a path naming a blocking condition, expected response, safe state, and recovery. **accepted behavior contract** — an approved requirement, invariant, journey, or documented behavior defining expected behavior. **definition of done (DoD)** — one work item's authoritative closure contract. **completion condition** — one observable, independently testable part of a DoD. **integrated acceptance** — verification of behavior appearing only when all completion conditions work together. **technical hint** — non-normative information about relevant components, tests, evidence, or likely implementation sites.

## Reader overlay (genre knowledge only)

The reader recognizes a concise product requirements document organized around one strategic outcome, scope, success measures, technical invariants, child tasks, and completion. Navigation only.

## Skeleton

Dependency order: seed the product problem, users, scope, and terms before success measures, technical invariants, risks, and child-task boundaries (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | the strategic change, affected users, and the state of the thing being changed. ! the epic's own workflow position (core §0.5) |
| Strategic outcome | yes | one product-level outcome requiring several independently acceptable tactical outcomes |
| Problem and evidence | yes | the current problem, its observed effects, and the evidence supporting strategic work |
| Users and journeys | yes | affected actors and the user journeys included or excluded |
| Scope and non-goals | yes | included product boundaries, excluded outcomes, applicable environments, release boundaries |
| Success measures | yes | observable product-level measures, comparison points, thresholds, evaluation window |
| Technical invariants | yes | stable identified properties every applicable child task must preserve |
| Task map | yes | child task outcomes, dependencies, sequencing constraints |
| Cross-task risks | yes | failure modes, unknowns, mitigations depending on more than one child task |
| Relations | yes | governing design, decision, research, or policy documents, and any superseded epic |
| Definition of done | yes | one authoritative closure contract verifying the strategic outcome and every technical invariant |

Optional: `Shared vocabulary`, holding the domain terms this epic's child work items may use without re-admitting them (§2.3.5). Each entry satisfies core §2.3 and §2.4 as an in-document definition does, and counts against **this** document's §4.8.1 budget, never a child's (§4.8.4). Place it before `Scope and non-goals`, so the terms precede the exact detail depending on them (core §4.4.2).

**Renames:** `Strategic outcome` → `Outcome` · `Problem and evidence` → `Problem` · `Users and journeys` → `Users` · `Technical invariants` → `Invariants` · `Task map` → `Child tasks` · `Cross-task risks` → `Risks`.

**Merges:** `Summary` + `Strategic outcome` → `Summary and outcome` · `Problem and evidence` + `Users and journeys` → `Problem and users` · `Scope and non-goals` + `Success measures` → `Scope and success`. Each merge keeps the canonical jobs as separately labeled subsections.

## Boundary locations (core §7.1)

- **Scope and non-goals** — environment, version, dependency, security, privacy, data boundaries.
- **Success measures** — capacity, duration, evidence boundaries.
- **Technical invariants** — mandatory cross-task limits.
- **Cross-task risks** — failure, recovery, unverified conditions.

## Evidence-record additions (core §5.4)

The strategic outcome, problem evidence, success measures, technical-invariant IDs, child-task boundaries, cross-task risks, and DoD verification.

## §2.3 + §4.8 Scoped rules — epic-scoped admission

Shared with `epic`, `task`, `subtask`. Core §2.3 and §4.8 carry the unscoped rules; these three apply only inside a work-item family.

| ID | C | D | Rule |
|---|---|---|---|
| 2.3.5 | P | J | a child work item may use a term its ancestor `epic` admits, without re-admitting it — **epic-scoped admission** |
| 2.3.6 | M | S | a child using an inherited term names the term and the admitting `epic` in the slot carrying its parent reference or its boundaries |
| 4.8.4 | M | J | a term admitted under §2.3.5 counts against the admitting `epic`'s §4.8.1 budget, ! against any child's |

The per-document ladder does not compose across a *family* sharing one domain vocabulary: a 500-word `task` depending on eight family terms must duplicate ~200 words of verbatim definition (§6.5.1), or fail §2.3.1. ITWS already grants a family vocabulary twice — §0.6 meta-vocabulary, and the work-item block in these three profiles — and §2.3.5 extends it from the *genre's* vocabulary to the *subject's*. Admission is unchanged: an `epic` `Shared vocabulary` entry satisfies §2.3.1–§2.4.5 as an in-document definition does. A child expected to circulate alone may instead recall an inherited definition verbatim under §6.5.3, trading length for independence.

## §4.11 Scoped rules — work-item hierarchy

| ID | C | D | Rule |
|---|---|---|---|
| 4.11.1 | M | J | an `epic` title states its strategic product outcome |
| 4.11.8 | M | L | each technical invariant in an `epic` has a unique stable identifier |
| 4.11.10 | M | J | an `epic` ! contain acceptance detail that independently performs a child `task` or `subtask` job |

## §5.9 Scoped rules — definition-of-done composition

Shared with `task` and `subtask`:

| ID | C | D | Rule |
|---|---|---|---|
| 5.9.1 | M | L | exactly one authoritative `Definition of done` slot per work item |
| 5.9.2 | M | S | each completion condition identifies an observable pass condition and its verification method |

Scoped to `epic`:

| ID | C | D | Rule |
|---|---|---|---|
| 5.9.7 | M | S | an `epic` DoD verifies its strategic outcome **and** every technical invariant |

A DoD states what closure would require. Whether the item has closed, who owns it now, and whether anyone approved it = workflow facts outside ITWS (core §0.5, *Text, not process*). An `epic` may record ownership, status, or a requested alignment in any slot where it has them. No slot requires them.

## Applicable core rules with profile scope

§4.2.4 and §4.4.3 both apply. §7.3 is optional here.

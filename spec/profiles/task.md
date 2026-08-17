# Profile: `task`

**ITWS version:** 1.0 · **Surface:** `markdown-document` · **Family:** work-item

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Specify one independently acceptable tactical outcome, through a user journey or an explicit engineering-only contract.

A `task` normally contains one user journey. An engineering-only `task` uses a named technical boundary instead. The classification does not change the requirement for observable acceptance.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the tactical outcome, classification, critical boundary, and integrated acceptance condition.**

## Reader overlay (genre knowledge only)

The reader recognizes one tactical outcome with classification, one user journey or engineering-only outcome, paths, completion conditions, integrated acceptance, and child subtasks. Navigation only.

## Work-item vocabulary

Available without definition in `epic`, `task`, and `subtask`.

**work item** — a governed `epic`, `task`, or `subtask`. **strategic outcome** — one requiring several independently acceptable tactical outcomes. **tactical outcome** — one accepted at a single product or technical boundary. **technical boundary** — an interface, invariant, operational state, or artifact engineering can verify. **technical invariant** — a stable property every applicable child work item must preserve. **user journey** — one actor's path from a stated starting condition to an observable outcome. **happy path** — a journey path reaching the intended outcome under expected conditions. **sad path** — a path naming a blocking condition, expected response, safe state, and recovery. **accepted behavior contract** — an approved requirement, invariant, journey, or documented behavior defining expected behavior. **definition of done (DoD)** — one work item's authoritative closure contract. **completion condition** — one observable, independently testable part of a DoD. **integrated acceptance** — verification of behavior appearing only when all completion conditions work together. **technical hint** — non-normative information about relevant components, tests, evidence, or likely implementation sites. **feature work** — work adding or changing accepted behavior without correcting a documented deviation. **defect correction** — work restoring behavior an accepted behavior contract requires. **maintenance or enabler work** — work preserving behavior or preparing a later independently acceptable outcome. **engineering-only task** — a `task` with no independently acceptable user outcome, accepted at a named technical boundary.

## Classifications (closed)

- **Outcome class:** `user-journey` | `engineering-only`
- **Change reason:** `feature` | `defect-correction` | `maintenance-or-enabler`

## Path field sets

- **happy-path fields** — starting condition, actor action, product response, observable outcome.
- **sad-path fields** — blocking condition, expected response, safe state, recovery.
- **technical-success fields** — starting state, applied change or condition, observable technical outcome, verification method.
- **technical-failure fields** — failure condition, technical effect, safe state, recovery.
- **delegated sad-path fields** — path ID, blocking condition, expected response, safe state, recovery, owning `subtask`.

## Skeleton

Dependency order: seed parent context, classification, and terms before paths, completion conditions, and integrated acceptance (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | the tactical outcome, affected product or technical boundary |
| Classification | yes | one Outcome class and one Change reason, no additional values |
| Parent and invariants | yes | one parent epic or `None` with a reason, every applicable inherited invariant ID, and every inherited term this task relies on, each named with its admitting `epic` (§2.3.6) |
| Context and boundaries | yes | current state, included and excluded conditions, environment, version, dependencies, relevant limits |
| Contract and deviation evidence | yes | for `defect-correction`, the accepted behavior contract and observed deviation evidence; otherwise `Not applicable` with a reason |
| Journey or engineering outcome | yes | exactly one user journey, or one engineering-only outcome with its technical boundary and supported journey or epic invariant |
| Happy or technical success path | yes | every happy-path field, or every technical-success field |
| Sad or technical failure paths | yes | material sad paths or technical failure and recovery paths; `None identified` with a reason when none is known |
| Definition of done | yes | one authoritative closure contract whose named completion conditions state pass tests and methods |
| Integrated acceptance | yes | checks for behavior appearing only when several completion conditions work together, or `Not applicable` with a reason |
| Subtask map | yes | each child subtask and its parent completion-condition ID; `None` with a reason when there are none |

Optional: `Technical hints`, holding only non-normative implementation information. An unverified hypothesis uses a Speculation block.

**Renames:** `Parent and invariants` → `Parent epic` · `Contract and deviation evidence` → `Defect evidence` · `Journey or engineering outcome` → `User journey` or `Engineering outcome` · `Happy or technical success path` → `Happy path` or `Technical success` · `Sad or technical failure paths` → `Sad paths` or `Technical failures` · `Subtask map` → `Child subtasks`.

**Merges:** `Summary` + `Classification` → `Summary and classification` · `Parent and invariants` + `Context and boundaries` → `Context` · `Definition of done` + `Integrated acceptance` → `Acceptance`. Each merge keeps the canonical jobs as separately labeled subsections. **`Contract and deviation evidence` shall not merge with `Technical hints`.**

## Boundary locations (core §7.1)

- **Context and boundaries** — environment, version, dependency, capacity, authority, security, privacy, data limits.
- **Sad or technical failure paths** — failure and recovery behavior.
- **Integrated acceptance** — cross-condition and unverified conditions.

## Evidence-record additions (core §5.4)

Both classifications, parent and invariant links, journey or technical boundary, path records, completion-condition IDs, and integrated-acceptance evidence. A defect correction also carries its accepted behavior contract and deviation evidence.

## §2.3 + §4.8 Scoped rules — epic-scoped admission

Shared with `epic`, `task`, `subtask`. Core §2.3 and §4.8 carry the unscoped rules; these three apply only inside a work-item family.

| ID | C | D | Rule |
|---|---|---|---|
| 2.3.5 | P | J | a child work item may use a term its ancestor `epic` admits, without re-admitting it — **epic-scoped admission** |
| 2.3.6 | M | S | a child using an inherited term names the term and the admitting `epic` in the slot carrying its parent reference or its boundaries |
| 4.8.4 | M | J | a term admitted under §2.3.5 counts against the admitting `epic`'s §4.8.1 budget, ! against any child's |

The per-document ladder does not compose across a *family* sharing one domain vocabulary: a 500-word `task` depending on eight family terms must duplicate ~200 words of verbatim definition (§6.5.1), or fail §2.3.1. ITWS already grants a family vocabulary twice — §0.6 meta-vocabulary, and the work-item block in these three profiles — and §2.3.5 extends it from the *genre's* vocabulary to the *subject's*. Admission is unchanged: an `epic` `Shared vocabulary` entry satisfies §2.3.1–§2.4.5 as an in-document definition does. A child expected to circulate alone may instead recall an inherited definition verbatim under §6.5.3, trading length for independence.

## §4.11 Scoped rules — work-item hierarchy

Scoped to `task`:

| ID | C | D | Rule |
|---|---|---|---|
| 4.11.2 | M | J | a user-journey `task` title names its actor, trigger, and observable outcome |
| 4.11.3 | M | J | an engineering-only `task` title states its observable technical outcome |
| 4.11.5 | M | L | a `task` declares one permitted Outcome class and one permitted Change reason |
| 4.11.6 | M | S | a `defect-correction` task identifies its accepted behavior contract and observed deviation evidence |
| 4.11.7 | M | S | an engineering-only `task` identifies its technical boundary and supported journey or `epic` invariant |
| 4.11.11 | M | J | a `task` defines an outcome accepted independently of sibling `task` documents |
| 4.11.15 | M | S | a `task` summarizes each delegated sad path with every delegated sad-path field |
| 4.11.16 | M | J | an aggregate sad path stays specified and verified in its parent `task` |
| 4.11.18 | M | S | a user-journey `task` states every happy-path field |
| 4.11.19 | M | S | each sad path in a user-journey `task` states every sad-path field |
| 4.11.20 | M | S | an engineering-only `task` states every technical-success field |
| 4.11.21 | M | S | each material failure path in an engineering-only `task` states every technical-failure field |

Shared with `subtask`:

| ID | C | D | Rule |
|---|---|---|---|
| 4.11.9 | M | J | a child work item ! weaken an applicable inherited technical invariant |
| 4.11.14 | M | J | work with an independently acceptable outcome uses `task`, not `subtask` |
| 4.11.17 | M | J | a technical hint ! contain a requirement, technical invariant, or completion condition |

## §5.9 Scoped rules — definition-of-done composition

Shared with `epic` and `subtask`:

| ID | C | D | Rule |
|---|---|---|---|
| 5.9.1 | M | L | exactly one authoritative `Definition of done` slot per work item |
| 5.9.2 | M | S | each completion condition identifies an observable pass condition and its verification method |

Scoped to `task`:

| ID | C | D | Rule |
|---|---|---|---|
| 5.9.3 | M | L | each completion condition in a `task` has a unique stable identifier |
| 5.9.5 | M | J | a `task` defines integrated-acceptance checks for behavior depending on several completion conditions |

A `task` whose acceptance would follow from its subtasks alone has written no integrated-acceptance check — a §5.9.5 finding against the text. Whether the task was accepted, by whom, and when = workflow facts outside ITWS (core §0.5, *Text, not process*). A `task` may record lifecycle state or ownership where it has them. No slot requires them.

## Applicable core rules with profile scope

§4.2.4 and §4.4.3 both apply. **§7.3 is mandatory for this profile** — an observation carries no interpretive addition, and an unverified hypothesis goes in a marked speculation block, including inside `Technical hints`.

# Profile: `subtask`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document` · **Family:** work-item

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Verify one named completion condition under exactly one parent `task`, without creating an independent outcome.

A `subtask` is **not** independently acceptable. It may carry local implementation or verification detail. The parent retains the tactical outcome and integrated acceptance.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader **identify the parent condition, bounded contribution, inherited invariant, and evidence status.**

## Reader overlay (genre knowledge only)

The reader recognizes one non-independent contribution linked to one parent task and one named parent completion condition. Navigation only.

## Work-item vocabulary

Available without definition in `epic`, `task`, and `subtask`.

**work item** — a governed `epic`, `task`, or `subtask`. **strategic outcome** — one requiring several independently acceptable tactical outcomes. **tactical outcome** — one accepted at a single product or technical boundary. **technical boundary** — an interface, invariant, operational state, or artifact engineering can verify. **technical invariant** — a stable property every applicable child work item must preserve. **user journey** — one actor's path from a stated starting condition to an observable outcome. **happy path** — a journey path reaching the intended outcome under expected conditions. **sad path** — a path naming a blocking condition, expected response, safe state, and recovery. **definition of done (DoD)** — one work item's authoritative closure contract. **completion condition** — one observable, independently testable part of a DoD. **integrated acceptance** — verification of behavior appearing only when all completion conditions work together. **technical hint** — non-normative information about relevant components, tests, evidence, or likely implementation sites.

## Skeleton

Dependency order: seed the parent condition and inherited invariants before contribution details, delegated paths, and verification (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | the contribution and the parent condition it verifies, without a separate product outcome |
| Parent task | yes | exactly one authoritative parent task reference |
| Named completion condition | yes | exactly one stable completion-condition ID from the parent task, with its exact meaning and scope preserved |
| Contribution | yes | the implementation, test, documentation, data, or operational contribution supplied |
| Boundaries and invariants | yes | local scope, applicable inherited invariant IDs, relevant failure limits, excluded work |
| Delegated path details | yes | detail for each sad path delegated by the parent, or `None` with a reason; the detail preserves the parent's user-visible outcome |
| Definition of done | yes | one local closure contract verifying the named parent completion condition |
| Verification evidence | yes | artifact, environment, inputs, method, observable result, and link back to the parent condition |

Optional: `Technical hints`, holding only non-normative implementation information. An unverified hypothesis uses a Speculation block.

**Renames:** `Named completion condition` → `Parent condition` · `Boundaries and invariants` → `Boundaries` · `Delegated path details` → `Delegated paths` · `Verification evidence` → `Evidence`.

**Merges:** `Summary` + `Parent task` → `Summary and parent` · `Contribution` + `Boundaries and invariants` → `Contribution and boundaries`. Each merge keeps the canonical jobs as separately labeled subsections. **`Definition of done` shall not merge with `Technical hints`.**

## Boundary locations (core §7.1)

- **Boundaries and invariants** — local environment, version, dependency, security, privacy, data, and inherited limits.
- **Delegated path details** — assigned failure and recovery behavior.
- **Verification evidence** — unverified conditions and evidence limits.

## Evidence-record additions (core §5.4)

The parent task, named parent condition, inherited invariants, bounded contribution, delegated path detail, and verification evidence.

## §4.11 Scoped rules — work-item hierarchy

Scoped to `subtask`:

| ID | C | Rule |
|---|---|---|
| 4.11.4 | M | a `subtask` title states the contribution it verifies |
| 4.11.12 | M | a `subtask` identifies exactly one parent `task` |
| 4.11.13 | M | a `subtask` identifies exactly one completion-condition ID from its parent `task` |

Shared with `task`:

| ID | C | Rule |
|---|---|---|
| 4.11.9 | M | a child work item ! weaken an applicable inherited technical invariant |
| 4.11.14 | M | work with an independently acceptable outcome uses `task`, not `subtask` |
| 4.11.17 | M | a technical hint ! contain a requirement, technical invariant, or completion condition |

## §5.9 Scoped rules — definition-of-done composition

Shared with `epic` and `task`:

| ID | C | Rule |
|---|---|---|
| 5.9.1 | M | exactly one authoritative `Definition of done` slot per work item |
| 5.9.2 | M | each completion condition identifies an observable pass condition and its verification method |
| 5.9.8 | M | a work item closes only after every applicable completion condition passes |

Scoped to `subtask`:

| ID | C | Rule |
|---|---|---|
| 5.9.4 | M | a `subtask` DoD states how its evidence verifies the named parent completion condition |

## Applicable core rules with profile scope

**§4.2.4 does not apply** to this profile — a subtask has no independent main point; its point is the parent condition. **§4.4.3 does not apply.**

**§7.3 is mandatory for this profile** — verification evidence carries no interpretive addition, and an unverified hypothesis goes in a marked speculation block.

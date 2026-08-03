# Profile: `design-rfc`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Propose or specify a technical design: requirements, interfaces, invariants, alternatives, and acceptance conditions.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **what the design proposes, its approval status, and where the proposal stops.**

## Reader overlay (genre knowledge only)

The reader recognizes a proposal organized around context, requirements, a proposed design, alternatives, risks, rollout, and unresolved questions. This grants navigation only — no unexplained domain term inside those sections.

## Skeleton

Dependency order: seed the problem, constraints, and specialized vocabulary before exact design and risk detail (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | the proposed change, who or what it affects, and the decision reviewers are asked to make |
| Context | yes | current condition, problem, relevant constraints — no decision-path history (§4.9) |
| Requirements | yes | verifiable outcomes and constraints; mandatory requirements distinguished from preferences |
| Proposal | yes | the design and mechanism, ordered from assumed-reader view to exact detail |
| Interfaces and invariants | yes | inputs, outputs, boundaries, compatibility, properties that must remain true |
| Alternatives | yes | credible alternatives, including no change where relevant, compared against the requirements |
| Risks | yes | failure modes, security and reliability concerns, unknowns, mitigations with bounded claims |
| Rollout | yes | implementation stages, validation gates, rollback, ownership or handoff points |
| Open questions | yes | unresolved decisions and the evidence or owner needed to close each |

**Renames:** `Proposal` → `Proposed design` · `Interfaces and invariants` → `Contracts and invariants` · `Rollout` → `Migration and rollout` · `Open questions` → `Unresolved questions`.

**Merges:** `Context` + `Requirements` → `Context and requirements` · `Proposal` + `Interfaces and invariants` → `Design` · `Risks` + `Rollout` → `Risks and rollout`. Each merge keeps the canonical jobs as separately labeled subsections.

## Boundary locations (core §7.1)

- **Context** — environment, version, dependency bounds.
- **Requirements** + **Interfaces and invariants** — capacity, security, privacy, data constraints.
- **Risks** — failure modes and unknowns.
- **Rollout** — duration, recovery, unverified-gate boundaries.

## Evidence-record additions (core §5.4)

Affected interfaces and invariants. Interfaces cover inputs, outputs, errors, compatibility, and versioning. Invariants apply before, during, and after the change.

## Applicable core rules with profile scope

§4.2.4 (main point in earliest applicable slot) and §4.4.3 (plain outcome then exact outcome, linked) both apply. §7.3 (observation/interpretation split) is optional here.

## Scoped rules

None. Every obligation comes from core.

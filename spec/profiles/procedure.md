# Profile: `procedure`

**ITWS version:** 1.0 · **Surface:** `markdown-document`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Enable a reader to complete an operational or development task safely and repeatably.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the task goal, verified scope, critical precondition, and rollback boundary.**

## Reader overlay (genre knowledge only)

The reader recognizes prerequisites, ordered steps, verification, recovery, and escalation as instruction-document conventions. Navigation only.

## Skeleton

Dependency order: seed prerequisites, safety conditions, permissions, and terms before the first dependent step (core §4.4.2).

The procedure supports recovery where possible, and escalation where recovery is unsafe or fails.

| Slot | Required | Job |
|---|---|---|
| Goal | yes | the end state the procedure produces |
| Scope | yes | applicable systems, conditions, exclusions, required authority |
| Prerequisites | yes | access, tools, inputs, backups, captured state, checks completed before the first change |
| Steps | yes | ordered actions with named objects and stop conditions |
| Verification | yes | observable checks and pass criteria for the goal |
| Rollback | yes | steps restoring the prior safe state, or an explicit explanation of why rollback is unavailable |
| Failure and escalation | yes | conditions for stopping, safe state while stopped, evidence to collect, a named role or documented channel |

Verification checks may also sit beside individual steps. The `Verification` slot must still summarize the final pass criteria.

**Renames:** `Goal` → `Outcome` · `Prerequisites` → `Before you begin` · `Failure and escalation` → `Stop conditions and escalation`.

**Merges:** `Goal` + `Scope` → `Goal and scope` · `Rollback` + `Failure and escalation` → `Recovery and escalation`. Each merge keeps the canonical jobs as separately labeled subsections.

## Boundary locations (core §7.1)

- **Scope** — environment, version, capacity, duration, data bounds.
- **Prerequisites** — dependency, authority, security, privacy assumptions.
- **Rollback** — reversibility limits.
- **Failure and escalation** — known failure modes and unverified conditions.

## Evidence-record additions (core §5.4)

Preconditions and verification after critical steps and at completion. Rollback or recovery instructions, including any unsafe rollback point.

## Precedence note

Safe task order and warning placement beat claim-first ordering and sentence smoothness (core §1.3 items 1 and 3). Never rearrange a warning for rhetorical effect.

## Applicable core rules with profile scope

§4.2.4 and §4.4.3 both apply. §7.3 is optional here.

## Scoped rules

None. Every obligation comes from core.

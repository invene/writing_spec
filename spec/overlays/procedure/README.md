# `procedure` overlay

**ITWS version:** 0.10.0-draft

**Job:** enable a defined reader to complete or verify a bounded operational or development task safely and repeatably.

A `procedure` supplies prerequisites, ordered actions, verification, rollback, and escalation. Explanation appears only where an action depends on it.

## Load set

A writer, rewriting agent, or tool loads the following material for a `procedure` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to a `procedure` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): state the task goal, verified scope, critical precondition, and rollback boundary.

## Examples

Annex D contains two `procedure` examples: D.5 and D.15.

# `procedure` overlay

**ITWS version:** 0.6.0-draft · **Minimum conformance tier:** `reviewed`

**Job:** enable a defined reader to complete or verify a bounded operational or development task safely and repeatably.

A `procedure` supplies prerequisites, ordered actions, verification, rollback, and escalation. Explanation appears only where an action depends on it.

## Load set

A writer, reviewer, or tool loads the following material for a `procedure` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to a `procedure` document.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): perform or tabletop the critical path and identify its preconditions, verification, rollback, and point of no return.

## Owner review focus

The subject-matter owner focuses on preconditions, verification, and rollback (§8.4).

## Examples

Annex D contains one `procedure` example: D.5.

# `subtask` overlay

**ITWS version:** 0.8.0-draft · **Minimum conformance tier:** `core`

**Job:** verify one named completion condition for exactly one parent `task`.

A `subtask` is not independently acceptable. It may contain detail for a delegated sad path. The parent `task` retains the path's user-visible outcome and owner.

## Load set

A writer, reviewer, or tool loads the following material for a `subtask` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- The shared overlay module [../shared/work-item.md](../shared/work-item.md).

No other profile overlay applies to a `subtask` document.

## Scan-test outcome

A scan test at every tier measures this shallow outcome (§4.12, §8.1): identify the parent condition, bounded contribution, inherited invariant, and evidence status.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): identify the parent condition, bounded contribution, inherited invariants, delegated paths, and evidence without inventing an independent outcome.

## Owner review focus

The subject-matter owner focuses on parent alignment and local verification (§8.4).

## Examples

Annex D contains one `subtask` example: D.12.

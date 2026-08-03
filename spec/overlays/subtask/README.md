# `subtask` overlay

**ITWS version:** 0.10.0-draft

**Job:** verify one named completion condition for exactly one parent `task`.

A `subtask` is not independently acceptable. It may contain detail for a delegated sad path. The parent `task` retains the path's user-visible outcome and owner.

## Load set

A writer, rewriting agent, or tool loads the following material for a `subtask` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- The shared overlay module [../shared/work-item.md](../shared/work-item.md).

No other profile overlay applies to a `subtask` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): identify the parent condition, bounded contribution, inherited invariant, and evidence status.

## Examples

Annex D contains two `subtask` examples: D.12 and D.22.

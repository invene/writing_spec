# `task` overlay

**ITWS version:** 0.10.0-draft

**Job:** define the smallest independently acceptable tactical outcome.

A `task` normally states one user journey. An engineering-only `task` states acceptance at a technical boundary and cites the journey or `epic` invariant it supports. A `task` defines its paths, completion conditions, and integrated acceptance. A `task` does not give the ordered instructions of a `procedure`.

## Load set

A writer, rewriting agent, or tool loads the following material for a `task` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- The shared overlay module [../shared/work-item.md](../shared/work-item.md).

No other profile overlay applies to a `task` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): state the tactical outcome, classification, critical boundary, and integrated-acceptance status.

## Examples

Annex D contains two `task` examples: D.11 and D.23.

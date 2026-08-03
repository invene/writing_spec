# `technical-report` overlay

**ITWS version:** 0.10.0-draft

**Job:** answer a bounded technical question or document a system, method, evaluation, or result at sustained detail.

A `technical-report` carries evidence, interpretation, limits, and enough information to reproduce the method or verify the system.

## Load set

A writer, rewriting agent, or tool loads the following material for a `technical-report` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- The shared overlay module [../shared/report.md](../shared/report.md).

No other profile overlay applies to a `technical-report` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): state the technical question or outcome, its evidential strength, and its validity boundary.

## Examples

Annex D contains two `technical-report` examples: D.8 and D.18.

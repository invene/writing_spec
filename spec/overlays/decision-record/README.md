# `decision-record` overlay

**ITWS version:** 0.10.0-draft

**Job:** preserve one settled technical decision, its context and options, its status, and its consequences.

A `decision-record` tells future readers what governs and why. A `decision-record` is not a design survey or implementation procedure.

## Load set

A writer, rewriting agent, or tool loads the following material for a `decision-record` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to a `decision-record` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): state the decision, its status, the main reason, and its material consequence or boundary.

## Examples

Annex D contains two `decision-record` examples: D.4 and D.14.

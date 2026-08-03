# `design-rfc` overlay

**ITWS version:** 0.10.0-draft

**Job:** specify a technical design before implementation or rollout.

The text exposes its requirements, interfaces, invariants, alternatives, risks, and acceptance conditions. A `design-rfc` seeks an informed decision. A `design-rfc` does not present an already settled decision as open.

## Load set

A writer, rewriting agent, or tool loads the following material for a `design-rfc` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to a `design-rfc` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): state what the design proposes, its approval status, and where the proposal stops.

## Examples

Annex D contains two `design-rfc` examples: D.3 and D.13.

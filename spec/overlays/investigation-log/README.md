# `investigation-log` overlay

**ITWS version:** 0.10.0-draft

**Job:** maintain an append-only working record during an active investigation.

Each dated entry records its question, configuration or context, observations, and next step. Each entry also records an interpretation or states that no interpretation exists. An entry does not present provisional findings as settled.

## Load set

A writer, rewriting agent, or tool loads the following material for an `investigation-log` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to an `investigation-log` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): state the current question, strongest observation, unresolved hypothesis, and next discriminating check.

## Examples

Annex D contains two `investigation-log` examples: D.9 and D.20.

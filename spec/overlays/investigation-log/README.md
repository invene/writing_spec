# `investigation-log` overlay

**ITWS version:** 0.6.0-draft · **Minimum conformance tier:** `core`

**Job:** maintain an append-only working record during an active investigation.

Each dated entry records its question, configuration or context, observations, and next step. Each entry also records an interpretation or states that no interpretation exists. An entry does not present provisional findings as settled.

## Load set

A writer, reviewer, or tool loads the following material for an `investigation-log` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to an `investigation-log` document.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): distinguish observations from hypotheses, state what remains unknown, and identify the next discriminating check.

## Owner review focus

The subject-matter owner focuses on observation and hypothesis separation (§8.4).

## Examples

Annex D contains one `investigation-log` example: D.9.

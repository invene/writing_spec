# `decision-record` overlay

**ITWS version:** 0.6.0-draft · **Minimum conformance tier:** `core`

**Job:** preserve one settled technical decision, its context and options, its status, and its consequences.

A `decision-record` tells future readers what governs and why. A `decision-record` is not a design survey or implementation procedure.

## Load set

A writer, reviewer, or tool loads the following material for a `decision-record` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to a `decision-record` document.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): state the decision, why it was chosen, the rejected alternatives, and its consequences.

## Owner review focus

The subject-matter owner focuses on alternatives and consequences (§8.4).

## Examples

Annex D contains one `decision-record` example: D.4.

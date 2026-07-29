# `design-rfc` overlay

**ITWS version:** 0.8.0-draft · **Minimum conformance tier:** `reviewed`

**Job:** specify a technical design before implementation or rollout.

Reviewers evaluate its requirements, interfaces, invariants, alternatives, risks, and acceptance conditions. A `design-rfc` seeks an informed decision. A `design-rfc` does not present an already settled decision as open.

## Load set

A writer, reviewer, or tool loads the following material for a `design-rfc` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to a `design-rfc` document.

## Scan-test outcome

A scan test at every tier measures this shallow outcome (§4.12, §8.1): state what the design proposes, its approval status, and where the proposal stops.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): explain the proposed design, affected interfaces, invariants, material trade-offs, and approval status.

## Owner review focus

The subject-matter owner focuses on interfaces and invariants (§8.4).

## Examples

Annex D contains one `design-rfc` example: D.3.

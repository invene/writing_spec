# `technical-report` overlay

**ITWS version:** 0.8.0-draft · **Minimum conformance tier:** `reviewed`

**Job:** answer a bounded technical question or document a system, method, evaluation, or result at sustained detail.

A `technical-report` carries evidence, interpretation, limits, and enough information to reproduce the method or verify the system.

## Load set

A writer, reviewer, or tool loads the following material for a `technical-report` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- The shared overlay module [../shared/report.md](../shared/report.md).

No other profile overlay applies to a `technical-report` document.

## Scan-test outcome

A scan test at every tier measures this shallow outcome (§4.12, §8.1): state the technical question or outcome, its evidential strength, and its validity boundary.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): explain the main technical claim or operational outcome, its evidence, and its boundaries.

## Owner review focus

The subject-matter owner focuses on statistical and reproducibility-or-verification rigor (§8.4).

## Examples

Annex D contains one `technical-report` example: D.8.

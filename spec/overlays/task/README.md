# `task` overlay

**ITWS version:** 0.6.0-draft · **Minimum conformance tier:** `core`

**Job:** define the smallest independently acceptable tactical outcome.

A `task` normally states one user journey. An engineering-only `task` states acceptance at a technical boundary and cites the journey or `epic` invariant it supports. A `task` defines its paths, completion conditions, and integrated acceptance. A `task` does not give the ordered instructions of a `procedure`.

## Load set

A writer, reviewer, or tool loads the following material for a `task` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- The shared overlay module [../shared/work-item.md](../shared/work-item.md).

No other profile overlay applies to a `task` document.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): reconstruct the user journey or engineering outcome, its paths, inherited invariants, completion conditions, and integrated acceptance.

## Owner review focus

The subject-matter owner focuses on paths, completion conditions, and integrated acceptance (§8.4).

## Examples

Annex D contains one `task` example: D.11.

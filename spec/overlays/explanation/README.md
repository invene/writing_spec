# `explanation` overlay

**ITWS version:** 0.8.0-draft · **Minimum conformance tier:** `core`

**Job:** build an accurate mental model of a concept, system, or mechanism.

An `explanation` answers how or why. An `explanation` does not direct a task, approve a design, or present a working investigation chronology.

## Load set

A writer, reviewer, or tool loads the following material for an `explanation` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to an `explanation` document.

## Scan-test outcome

A scan test at every tier measures this shallow outcome (§4.12, §8.1): name the central concept or mechanism, its main relationship, and where the model stops.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): explain the central concept or mechanism accurately in new words and apply it to one fresh example.

## Owner review focus

The subject-matter owner focuses on mechanism fidelity, example correctness, and the stated limits (§8.4).

An explanation fails most damagingly when its mental model reads well but is causally wrong. The reader proxy cannot detect that failure, because a plausible mechanism passes a review from ignorance. The owner therefore checks three exact-layer slots. The mechanism describes how the subject actually behaves, and any simplification omits detail without changing that behavior (§1.2). Each worked example produces the outcome the stated mechanism predicts. The limits state where the presented model stops (§7.1).

## Examples

Annex D contains one `explanation` example: D.6.

# `explanation` overlay

**ITWS version:** 0.10.0-draft

**Job:** build an accurate mental model of a concept, system, or mechanism.

An `explanation` answers how or why. An `explanation` does not direct a task, approve a design, or present a working investigation chronology.

## Load set

A writer, rewriting agent, or tool loads the following material for an `explanation` document:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).
- Shared overlay modules: none.

No other profile overlay applies to an `explanation` document.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): name the central concept or mechanism, its main relationship, and where the model stops.

An explanation fails most damagingly when its mental model reads well but is causally wrong. The exact layer therefore ties together three slots. The mechanism describes how the subject actually behaves, and any simplification omits detail without changing that behavior (§1.2). Each worked example produces the outcome the stated mechanism predicts. The limits state where the presented model stops (§7.1).

## Examples

Annex D contains two `explanation` examples: D.6 and D.16.

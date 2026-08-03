# `maintenance-comment` overlay

**ITWS version:** 0.10.0-draft

**Job:** preserve durable code knowledge by governing the comments a maintenance change adds, modifies, or removes.

A `maintenance-comment` unit is not a Markdown document. Its governed surface is a **hosted comment set** (§0.2.1): the governed comments changed between one recorded base version and one proposed version of a host source file. A JSON declaration carrier records the declarations and comment records. The host source file itself stays outside ITWS conformance, and it carries no ITWS boilerplate.

The governed set is selected explicitly. It contains every changed `TODO` or `FIXME` marker and every changed natural-language comment that the carrier records. Conformance does not depend on authorship.

## Load set

A writer, rewriting agent, or tool loads the following material for a `maintenance-comment` change set:

- The shared core in `spec/00-front-matter.md` through `spec/08-textual-conformance-and-machine-checking.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).

No shared overlay module and no other profile overlay applies to a `maintenance-comment` change set.

## Shallow-model outcome

The scan path shall support this outcome (§4.12): state what knowledge each governed comment preserves, where it applies, its basis, and any removal trigger.

## Examples

Annex D contains two `maintenance-comment` examples: D.24 and D.25.

# `maintenance-comment` overlay

**ITWS version:** 0.8.0-draft · **Minimum conformance tier:** `core`

**Job:** preserve durable code knowledge by governing the comments a maintenance change adds, modifies, or removes.

A `maintenance-comment` unit is not a Markdown document. Its governed surface is a **hosted comment set** (§0.2.1): the governed comments changed between one recorded base version and one proposed version of a host source file. A JSON declaration carrier records the declarations, the comment records, and the conformance evidence. The host source file itself stays outside ITWS conformance, and it carries no ITWS boilerplate.

The governed set is selected explicitly. It contains every changed `TODO` or `FIXME` marker and every changed natural-language comment that the carrier records, including each comment an artificial-intelligence agent proposed. Tooling never classifies a comment as machine-authored from its prose style (§8.7).

## Load set

A writer, reviewer, or tool loads the following material for a `maintenance-comment` change set:

- The shared core in `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md`.
- The shared annexes in `spec/annexes/`.
- This directory: [reader.md](reader.md), [skeleton.md](skeleton.md), and [rules.md](rules.md).

No shared overlay module and no other profile overlay applies to a `maintenance-comment` change set.

## Scan-test outcome

A scan test at every tier measures this shallow outcome (§4.12, §8.1): state what knowledge each governed comment preserves, where it applies, its basis, and any removal trigger.

## Reader-test outcome

A publication-tier document measures this primary outcome (§8.3): reconstruct, for each governed comment, the preserved knowledge, its anchored location, its basis, its lifecycle, and the disposition of any machine-proposed text.

## Owner review focus

The subject-matter owner focuses on information delta, basis durability, and code-comment agreement (§8.4).

## Examples

Annex D contains two `maintenance-comment` examples: D.24 and D.25.

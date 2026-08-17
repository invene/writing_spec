# Profile: `explanation`

**ITWS version:** 1.0 · **Surface:** `markdown-document`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Build an accurate mental model of a system, mechanism, or concept.

The explanation must not become instructions or a design decision (core §4.3.2).

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader **name the central concept or mechanism, its main relationship, and where the model stops.**

## Reader overlay (genre knowledge only)

The reader recognizes a concept-to-mechanism explanation supported by examples and bounded by limits. Navigation only.

## Skeleton

Dependency order: build from the assumed-reader baseline before introducing the mechanism explained (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | the idea and why it matters, in assumed-reader vocabulary |
| Concepts | yes | terms and relationships admitted in ladder order (§2.3) |
| Mechanism | yes | how or why the subject behaves, from plain model to bounded exact detail |
| Examples | yes | representative worked cases exercising the mechanism, not merely restating it |
| Limits | yes | where the model stops, counterexamples, trade-offs, details intentionally left out |

**Renames:** `Concepts` → `Key concepts` · `Mechanism` → `How it works` · `Limits` → `Limits and trade-offs`.

**Merges:** `Concepts` + `Mechanism` → `Concepts and mechanism`, with the canonical jobs as separately labeled subsections. No other merge.

## Boundary locations (core §7.1)

- **Limits** — every applicable dimension.

## Evidence-record additions (core §5.4)

The exact definition or mechanism being explained, the conditions under which it applies, and sources or evidence for its factual assertions.

## Applicable core rules with profile scope

§4.2.4 applies. **§4.4.3 does not apply** to this profile. §7.3 is optional here.

This is the profile where §6 does the most work: analogies (§6.1), worked examples (§6.2), intuition blocks (§6.3), and diagrams (§6.4). All four remain plain-layer devices — none of them may be the sole home of exact content (§6.3.2).

## Scoped rules

None. Every obligation comes from core.

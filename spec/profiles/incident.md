# Profile: `incident`

**ITWS version:** 1.0 · **Surface:** `markdown-document`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Record impact, response, evidence, causes or contributing factors, and follow-up work.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the impact, causal status, unresolved point, and follow-up state.**

## Reader overlay (genre knowledge only)

The reader recognizes impact and timeline as factual records, treats causal analysis as a separate interpretation, and treats remediation and follow-up as separate jobs. Navigation only.

## Skeleton

Dependency order: supply necessary system context and vocabulary before dependent timeline or causal analysis (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | what happened, current state, and the bounded causal claim if any |
| Impact | yes | affected users or systems, duration, severity measures, known exclusions |
| Timeline | yes | timestamped events with time zone, and source where the source matters |
| Observations | yes | logs, measurements, changes, reproduced facts — **no causal interpretation** |
| Causal analysis | yes | supported causal chain, contributing conditions, confidence, contrary evidence; state "undetermined" when the evidence does not identify a cause |
| Remediation | yes | actions taken to restore or contain, and evidence that service or process recovered |
| Follow-up | yes | preventive and detective work, owners or roles, due states, verification of completion |

**Renames:** `Causal analysis` → `Cause and contributing conditions` · `Remediation` → `Containment and recovery` · `Follow-up` → `Corrective actions`.

**Merges:** `Summary` + `Impact` → `Summary and impact` · `Remediation` + `Follow-up` → `Remediation and follow-up`. **`Timeline` and `Observations` shall not merge with `Causal analysis`.** Each permitted merge keeps the canonical jobs as separately labeled subsections.

## Boundary locations (core §7.1)

- **Impact** — capacity, duration, security, privacy, data effects.
- **Observations** — environment, version, dependency, data-quality bounds.
- **Causal analysis** — uncertainty and unverified conditions.
- **Follow-up** — detection and recovery gaps.

## Evidence-record additions (core §5.4)

A timestamped timeline with one stated time zone. The timeline links evidence to each material event and covers impact and evidence of mitigation or recovery. Inferred events are marked as interpretation.

## Applicable core rules with profile scope

§4.2.4 and §4.4.3 both apply.

**§7.3 is mandatory for this profile.** Observations carry no interpretive addition (§7.3.1); anything beyond interpretive-tier support goes in a marked speculation block (§7.3.2) using speculative-tier phrases only (§7.3.3). The worked split in core §7.3 is an incident example — read it.

History is legitimately recorded here, as identified dated events, not as path-relative phrasing (core §4.9.1).

## Scoped rules

None. Every obligation comes from core.

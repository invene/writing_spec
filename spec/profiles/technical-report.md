# Profile: `technical-report`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document` · **Family:** report

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Present a technical analysis, system, method, or result in sustained detail. The report carries enough detail for a reader to assess the evidence and to reproduce the method or verify the system.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the technical question or outcome, its evidential strength, and its validity boundary.**

## Reader overlay (genre knowledge only)

The reader recognizes a report separating system or method, evidence, interpretation, limitations, and reproducibility or verification. Navigation only.

## Skeleton

Dependency order: seed prerequisites before the methods, evidence, and claims that use them (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | main result or deliverable, scope, audience, headline evidence, in assumed-reader vocabulary |
| Context | yes | question, need, prior state, constraints |
| System or method | yes | what was built, examined, or done; interfaces, configuration, mechanism at audit detail |
| Evidence | yes | measurements, observations, comparisons, or worked cases with the §5.4 reporting elements |
| Interpretation | yes | what the evidence supports, separated from observation, calibrated per §5.6 |
| Limitations | yes | scope, failure modes, missing evidence, what was not tested |
| Reproducibility or verification | yes | see §5.8 below; state the steps, inputs, and pass criteria |

**Renames:** `System or method` → `System`, `Method`, or `Approach` · `Evidence` → `Results` · `Interpretation` → `Discussion` · `Reproducibility or verification` → `Reproducibility`, `Verification`, or `Reproducibility and verification`.

**Merges:** `Evidence` + `Interpretation` → `Results and interpretation`, with separately labeled subsections. No other merge.

## Boundary locations (core §7.1)

- **Limitations** — every applicable dimension.
- **Reproducibility or verification** — environment, version, dependency, data, resource, and unverified-access bounds on independent checking.

## Evidence-record additions (core §5.4)

The relevant system configuration, dependency versions, method, and evidence for each reported operational outcome.

## §5.7 Statistical evidence

The reader has only [reader.md](../reader.md) §1 basic quantitative knowledge unless this document admits more.

**Bare** — usable without definition: count, minimum, maximum, range, mean or average, median, percentage, ratio, rate.

**Ladder-required** — admit under core §2.3 before use: mode and percentiles (including p50, p99) · standard deviation, variance, standard error · confidence interval, p-value, statistical significance · any named distribution, including "normal" and "power law" · correlation, regression, effect size · formal probability, expected value, sampling error, statistical power · every hypothesis-testing concept.

| ID | C | Rule |
|---|---|---|
| 5.7.1 | M | a ladder-required concept, or "significant" in its statistical sense, ! appear before §2.3 admission; admitting "significant" includes its underlying test |
| 5.7.2 | M | every headline statistical result includes a statement using **only bare concepts**; a ladder-required formulation may accompany it but ! replace it |

## §5.8 Checkability statement

A `technical-report` uses **reproducibility** when another reader can repeat the reported method, **verification** when it assesses a system or artifact, and both when both promises matter.

A verification statement identifies the artifact and version, inputs and environment, checks or procedure, and pass criteria, plus any unavailable input or access needed to run those checks.

| ID | C | Rule |
|---|---|---|
| 5.8.1 | M | the report includes its applicable checkability statement, containing every element listed above for its subject and selected form |
| 5.8.2 | M | the statement uses only assumed or previously admitted terms, and ! delegate required statement content entirely to a technical appendix or external artifact |

The statement summarizes the check in the main document. An appendix may carry command-, configuration-, or instrument-level detail; it does not replace the statement.

## Applicable core rules with profile scope

§4.2.4 and §4.4.3 both apply. **§7.3 is mandatory for this profile** — observation and interpretation stay separate, and speculation stays in marked blocks.

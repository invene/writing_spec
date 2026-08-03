# Profile: `investigation-log`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Preserve dated questions, actions, observations, hypotheses, and next steps while an investigation proceeds. Another reader must be able to reconstruct the question, conditions, observations, interpretation, and next action.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the current question, strongest observation, unresolved hypothesis, and next discriminating check.**

## Reader overlay (genre knowledge only)

The reader recognizes dated, append-only entries separating objective, configuration or context, observations, interpretation, and next step. Navigation only.

## Skeleton

Dependency order: maintain log-level definitions and admit entry-local terms before the observation or hypothesis needing them (core §4.4.2).

**Log header** — once per log:

| Slot | Required | Job |
|---|---|---|
| Subject | yes | the system, behavior, or question under investigation |
| Scope | yes | included and excluded environments, versions, time range, stop condition |
| Governing artifacts | yes | links to the design, procedure, incident, issue, or other source framing the investigation; `None` with a reason when none exists |
| Admitted terms | yes | the log-wide admitted-term set and definition links; entry-local terms are admitted inside their entry |

**Entry `<date> <id>`** — repeated per entry; include time zone when time matters:

| Slot | Required | Job |
|---|---|---|
| Objective | yes | the question this entry is intended to answer |
| Configuration or context | yes | absolute settings, inputs, environment, or non-experimental context needed to interpret observations |
| Observations | yes | what happened or was found, with source and measurements where available — **no causal claim** |
| Interpretation | yes | what the observations support and do not support; `No interpretation yet` when evidence is insufficient |
| Next step | yes | the next discriminating check, decision, or stop condition, stated as a plan |

**Renames:** `Objective` → `Question` · `Configuration or context` → `Configuration`, `Context`, `Setup`, or `Configuration and context` (use the combined form when both apply) · `Observations` → `Findings` · `Next step` → `Next action`.

**Merges:** none. **`Observations` and `Interpretation` shall never merge.**

The log as a whole carries the ITWS declaration. Entries do not repeat it.

## Mutation policy — append-only

A recorded entry is **fixed**. A correction is a new dated entry citing the earlier one. Do not rewrite an earlier entry. This is the §4.9.1 discipline applied to the log surface: the log's history is its content.

## Boundary locations (core §7.1)

- Each entry's **Configuration or context** — environment, version, dependency, data bounds.
- **Observations** — source, duration, quality bounds.
- **Interpretation** — uncertainty and unverified conditions.

## Evidence-record additions (core §5.4)

The time and configuration of each observation and its evidence source, plus the status of each hypothesis.

## Applicable core rules with profile scope

**§4.2.4 does not apply** to this profile — a log has no single document-level main point. **§4.4.3 does not apply.**

**§7.3 is mandatory for this profile.** The observation/interpretation split is the log's core discipline: `Observations` carries no causal claim, and an unsupported hypothesis goes in a marked speculation block.

History is legitimately recorded here, as identified dated entries, not as path-relative phrasing (core §4.9.1).

## Scoped rules

None. Every obligation comes from core.

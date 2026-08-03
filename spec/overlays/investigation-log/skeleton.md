# Annex E §E.8 — `investigation-log` skeleton

**ITWS version:** 0.10.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

Another reader must be able to reconstruct the question, conditions, observations, interpretation, and next action.

## Dependency order

An `investigation-log` maintains log-level definitions and admits entry-local terms before the observation or hypothesis that needs them (§4.4).

## Required sections

```
Log header                 (required once for the log)
  Subject                  (required) The system, behavior, or question under investigation.
  Scope                    (required) Included and excluded environments, versions, time
                           range, and stop condition.
  Governing artifacts      (required) Links to the design, procedure, incident, issue, or
                           other source that authorizes or frames the investigation.
                           Write "None" with a reason when no such artifact exists.
  Admitted terms           (required) The log-wide admitted-term set and definition links;
                           entry-local terms are admitted inside their entry.
Entry <date> <id>          (required for each entry; include time zone when time matters)
  Objective                (required) The question this entry is intended to answer.
  Configuration or context (required) Absolute settings, inputs, environment, or
                           non-experimental context needed to interpret observations.
                           Include both configuration and context when both matter.
  Observations             (required) What happened or was found, with source and
                           measurements where available. Include no causal claim.
  Interpretation           (required) What the observations support and do not support.
                           Write "No interpretation yet" when evidence is insufficient.
  Next step                (required) The next discriminating check, decision, or stop
                           condition, stated as a plan.
```

Permitted renames: `Objective` → `Question`; `Configuration or context` → `Configuration`, `Context`, `Setup`, or `Configuration and context`; `Observations` → `Findings`; `Next step` → `Next action`.

Use `Configuration and context` when both kinds of content apply. Permitted merges: none.

`Observations` and `Interpretation` shall never merge.

The log as a whole carries the ITWS declaration. Entries do not repeat the declaration.

Entries are append-only. A correction must cite the earlier entry. Add the correction as a new dated statement.

Do not rewrite the earlier entry.

**Mutation policy:** Entry <date> <id> · append-only · rule 4.9.1 · A recorded entry is fixed. A correction is a new dated entry that cites the earlier one.

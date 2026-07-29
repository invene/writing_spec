# Annex E §E.10 — `task` skeleton

**ITWS version:** 0.8.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

A `task` normally contains one user journey. An engineering-only `task` uses a named technical boundary instead. The classification does not change the requirement for observable acceptance.

## Dependency order

A `task` seeds its parent context, classification, and terms before paths, completion conditions, and integrated acceptance (§4.4).

## Required sections

```
Summary                    (required) The tactical outcome, affected product or
                           technical boundary, and current lifecycle state.
Classification             (required) One Outcome class and one Change reason from
                           Rule 4.11.5, with no additional values.
Parent and invariants      (required) One parent epic or "None" with a reason, plus
                           every applicable inherited invariant ID.
Context and boundaries     (required) Current state, included and excluded conditions,
                           environment, version, dependencies, and relevant limits.
Contract and deviation     (required) For defect correction, the accepted behavior
evidence                   contract and observed deviation evidence. Otherwise, state
                           "Not applicable" and why.
Journey or engineering     (required) Exactly one user journey, or one engineering-only
outcome                    outcome with its technical boundary and supported journey
                           or epic invariant.
Happy or technical         (required) For a user journey, every happy-path field. For
success path               engineering-only work, the starting state, change, and
                           observable technical outcome.
Sad or technical           (required) Material sad paths or technical failure and
failure paths              recovery paths. State "None identified" with a reason when
                           no material path is known.
Definition of done         (required) One authoritative closure contract whose named
                           completion conditions state pass tests and methods.
Integrated acceptance      (required) Checks for behavior that appears only when
                           multiple completion conditions work together, or "Not
                           applicable" with a reason.
Subtask map                (required) Each child subtask, its parent completion-condition
                           ID, and its current ownership or status. State "None" with
                           a reason when the task has no subtasks.
```

Optional: `Technical hints`, containing only non-normative implementation information. An unverified hypothesis uses a Speculation block.

Permitted renames: `Parent and invariants` → `Parent epic`; `Contract and deviation evidence` → `Defect evidence`; `Journey or engineering outcome` → `User journey` or `Engineering outcome`; `Happy or technical success path` → `Happy path` or `Technical success`; `Sad or technical failure paths` → `Sad paths` or `Technical failures`; `Subtask map` → `Child subtasks`.

Permitted merges: `Summary` + `Classification` → `Summary and classification`; `Parent and invariants` + `Context and boundaries` → `Context`; `Definition of done` + `Integrated acceptance` → `Acceptance`.

Each permitted merge must retain the canonical jobs as separately labeled subsections. `Contract and deviation evidence` shall not merge with Technical hints.

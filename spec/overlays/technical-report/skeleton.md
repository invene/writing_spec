# Annex E §E.6 — `technical-report` skeleton

**ITWS version:** 0.8.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

The report must include enough detail for a reader to assess the evidence.

A reader must be able to reproduce the method or verify the system.

## Dependency order

A `technical-report` seeds prerequisites before methods, evidence, and claims that use them (§4.4).

## Required sections

```
Summary                    (required) Main result or deliverable, scope, audience, and
                           headline evidence in assumed-reader vocabulary.
Context                    (required) Question, need, prior state, and constraints.
System or method           (required) What was built, examined, or done; interfaces,
                           configuration, and mechanism at the detail needed for audit.
Evidence                   (required) Measurements, observations, comparisons, or worked
                           cases with the reporting elements required by Part 5.
Interpretation             (required) What the evidence supports, separated from
                           observation and calibrated per §5.6.
Limitations                (required) Scope, failure modes, missing evidence, and what
                           was not tested.
Reproducibility or         (required) Use reproducibility when another reader can repeat
verification               the method. Use verification when claims are checked against
                           a system or artifact. State the steps, inputs, and pass
                           criteria. A report may include both.
```

Permitted renames: `System or method` → `System`, `Method`, or `Approach`; `Evidence` → `Results`; `Interpretation` → `Discussion`; `Reproducibility or verification` → `Reproducibility`, `Verification`, or `Reproducibility and verification`.

Permitted merges: `Evidence` + `Interpretation` → `Results and interpretation`, with separate labeled subsections. No other merge is permitted.

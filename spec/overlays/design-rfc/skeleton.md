# Annex E §E.1 — `design-rfc` skeleton

**ITWS version:** 0.8.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

## Dependency order

A `design-rfc` seeds the problem, constraints, and specialized vocabulary before exact design and risk detail (§4.4).

## Required sections

```
Summary                    (required) The proposed change, who or what it affects, and
                           the decision reviewers are being asked to make.
Context                    (required) The current condition, problem, and relevant
                           constraints, without decision-path history (§4.9).
Requirements               (required) Verifiable outcomes and constraints. Distinguish
                           mandatory requirements from preferences.
Proposal                   (required) The design and mechanism, ordered from the
                           assumed-reader view to exact detail.
Interfaces and invariants  (required) Inputs, outputs, boundaries, compatibility, and
                           properties that must remain true.
Alternatives               (required) Credible alternatives, including no change when
                           relevant, compared against the requirements.
Risks                      (required) Failure modes, security/reliability concerns,
                           unknowns, and mitigations with bounded claims.
Rollout                    (required) Implementation stages, validation gates, rollback,
                           and ownership or handoff points.
Open questions             (required) Unresolved decisions and the evidence or owner
                           needed to close each one.
```

Permitted renames: `Proposal` → `Proposed design`; `Interfaces and invariants` → `Contracts and invariants`; `Rollout` → `Migration and rollout`; `Open questions` → `Unresolved questions`.

Permitted merges: `Context` + `Requirements` → `Context and requirements`; `Proposal` + `Interfaces and invariants` → `Design`; `Risks` + `Rollout` → `Risks and rollout`.

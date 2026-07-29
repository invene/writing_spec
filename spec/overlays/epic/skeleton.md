# Annex E §E.9 — `epic` skeleton

**ITWS version:** 0.8.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

An `epic` is a concise product requirements document. It states product strategy and technical invariants. It does not contain child-task acceptance detail or an implementation design.

## Dependency order

An `epic` seeds the product problem, users, scope, and terms before success measures, technical invariants, risks, and child-task boundaries (§4.4).

## Required sections

```
Summary                    (required) The strategic change, affected users, current
                           state, and approval or alignment requested.
Strategic outcome          (required) One product-level outcome that requires several
                           independently acceptable tactical outcomes.
Problem and evidence       (required) The current problem, its observed effects, and
                           the evidence supporting strategic work.
Users and journeys         (required) Affected actors and the user journeys included
                           or excluded by the epic.
Scope and non-goals        (required) Included product boundaries, excluded outcomes,
                           applicable environments, and release boundaries.
Success measures           (required) Observable product-level measures, comparison
                           points, thresholds, and evaluation window.
Technical invariants       (required) Stable identified properties that every
                           applicable child task must preserve.
Task map                   (required) Child task outcomes, dependencies, sequencing
                           constraints, and current ownership or status.
Cross-task risks           (required) Failure modes, unknowns, and mitigations that
                           depend on more than one child task.
Relations                  (required) Governing design, decision, research, or policy
                           documents and any superseded epic.
Definition of done         (required) One authoritative closure contract that verifies
                           the strategic outcome and every technical invariant.
```

Permitted renames: `Strategic outcome` → `Outcome`; `Problem and evidence` → `Problem`; `Users and journeys` → `Users`; `Technical invariants` → `Invariants`; `Task map` → `Child tasks`; `Cross-task risks` → `Risks`.

Permitted merges: `Summary` + `Strategic outcome` → `Summary and outcome`; `Problem and evidence` + `Users and journeys` → `Problem and users`; `Scope and non-goals` + `Success measures` → `Scope and success`.

Each permitted merge must retain the canonical jobs as separately labeled subsections.

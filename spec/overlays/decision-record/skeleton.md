# Annex E §E.2 — `decision-record` skeleton

**ITWS version:** 0.8.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

## Dependency order

A `decision-record` seeds decision context and terms before the exact decision and consequences (§4.4).

## Required sections

```
Status                     (required) Proposed, accepted, superseded, or another defined
                           state. Identify a superseding record when one exists.
Context                    (required) The durable facts, forces, and constraints that
                           made a decision necessary.
Alternatives               (required) The credible options considered, including no
                           change when relevant, and why they were not selected.
Decision                   (required) The selected option in direct, present-tense
                           language, including its scope.
Consequences               (required) Expected benefits, costs, trade-offs, follow-on
                           work, and conditions that would justify revisiting it.
```

Permitted renames: `Alternatives` → `Options considered`; `Decision` → `Outcome`; `Consequences` → `Consequences and trade-offs`.

Permitted merges: none. `Status` may appear as a front-matter field immediately before `Context`.

Front-matter placement satisfies the slot but does not make status optional.

# Annex E §E.2 — `decision-record` skeleton

**ITWS version:** 0.10.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

## Dependency order

A `decision-record` states its decision plainly, then seeds decision context and terms before the exact decision and consequences (§4.4).

Rules 4.2.4 and 4.4.3 cover this profile, so `Summary` carries the plain member of the plain/exact outcome pair and `Decision` carries the exact member. `Summary` precedes `Context` because the reader needs the destination before the forces that produced it; `Decision` follows `Alternatives` because its scope depends on terms admitted there.

## Required sections

```
Status                     (required) Proposed, accepted, superseded, or another defined
                           state. Identify a superseding record when one exists.
Summary                    (required) The decision in one or two sentences of
                           assumed-reader vocabulary, before any supporting detail.
                           Links to `Decision` under §5.1.
Context                    (required) The durable facts, forces, and constraints that
                           made a decision necessary.
Alternatives               (required) The credible options considered, including no
                           change when relevant, and why they were not selected.
Decision                   (required) The exact restatement of `Summary`: the selected
                           option in direct, present-tense language, including its scope,
                           thresholds, and identifiers.
Consequences               (required) Expected benefits, costs, trade-offs, follow-on
                           work, and conditions that would justify revisiting it.
```

Permitted renames: `Alternatives` → `Options considered`; `Decision` → `Outcome`; `Consequences` → `Consequences and trade-offs`.

Permitted merges: none. `Status` may appear as a front-matter field immediately before `Context`.

Front-matter placement satisfies the slot but does not make status optional.

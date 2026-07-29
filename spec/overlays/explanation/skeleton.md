# Annex E §E.4 — `explanation` skeleton

**ITWS version:** 0.6.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

The explanation must not become instructions or a design decision.

## Dependency order

An `explanation` builds from the assumed-reader baseline before introducing the mechanism it explains (§4.4).

## Required sections

```
Summary                    (required) The idea and why it matters, in assumed-reader
                           vocabulary.
Concepts                   (required) Terms and relationships admitted in ladder order
                           (§2.3).
Mechanism                  (required) How or why the subject behaves, from plain model
                           to bounded exact detail.
Examples                   (required) Representative worked cases that exercise the
                           mechanism, not merely restate it.
Limits                     (required) Where the model stops, counterexamples, trade-offs,
                           and details intentionally left out.
```

Permitted renames: `Concepts` → `Key concepts`; `Mechanism` → `How it works`; `Limits` → `Limits and trade-offs`.

Permitted merges: `Concepts` + `Mechanism` → `Concepts and mechanism`. No other merge is permitted.

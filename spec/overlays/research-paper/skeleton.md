# Annex E §E.7 — `research-paper` skeleton

**ITWS version:** 0.8.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

The overlay assumes familiarity with research-paper navigation. The overlay assumes no knowledge of machine learning ([reader.md](reader.md)).

## Dependency order

A `research-paper` seeds prerequisites before methods, evidence, and claims that use them (§4.4).

## Required sections

```
Abstract                   (required) State the claim first in assumed-reader vocabulary.
                           Include scope, strength, and a headline comparison where
                           applicable.
Introduction               (required) Research question, importance, main claim, and
                           document map.
Background from first      (required) The ladder-seeding section: admit every
principles                 non-assumed term needed by the main line, in dependency order.
Method or what we built    (required) Procedure and mechanism, with exact detail in
                           bounded technical blocks when needed.
Experimental setup         (required) Data or materials, conditions, comparisons,
                           measures, and symbols needed to interpret the evidence.
Results                    (required) Observations and measurements. Include uncertainty
                           and self-contained figures or tables where applicable.
Discussion                 (required) Interpretation, relation to prior evidence, and
                           bounded generalization. Keep speculation labeled.
Limitations                (required) Scope of validity, known failure modes, untested
                           cases, and aggregation of claim-local caveats.
Reproducibility statement  (required) Plain-language account of what repeating the work
                           requires, distinct from an optional technical appendix.
```

Permitted renames: `Background from first principles` → a topic-specific heading that is mapped to `Background from first principles`; `Method or what we built` → `Method`, `Methods`, or `System`; `Discussion` → `Interpretation`; `Reproducibility statement` → `Reproducibility`.

Permitted merges: `Method or what we built` + `Experimental setup` → `Methods`, with separate mechanism and setup subsections.

`Results` and `Discussion` may merge as `Results and discussion` only when a publication format requires the merge.

The merged section must contain separately labeled observation and interpretation subsections.

`Background from first principles` shall not merge into `Introduction`.

Optional appendices may contain full formalism, proofs, extended tables, instruments, or configuration. An appendix does not replace any required job.

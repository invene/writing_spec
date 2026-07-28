# Annex G — Changelog

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Section 0.8 defines version semantics. Every entry that changes a rule cites the rule number. Rule numbers are permanent, and deprecation replaces deletion (§0.8).

## [Unreleased]

- Pending: validate the Annex B base reader with working software engineers and validate that each profile overlay adds conventions only.
- Pending: pilot the §8.3 reader protocol on documents from multiple profiles. Keep pass/fail criteria provisional until then.
- Pending: expand Annex D to at least 16 examples, at least two per profile, using a mix of public, approved anonymized, and constructed sources.
- Pending: use every Annex E skeleton for one end-to-end document and record any required-slot, rename, or merge defects.
- Pending: implement `itws-lint` so it selects exactly one version and profile and reports shared-core findings separately from profile findings.

## [0.2.1-draft] — 2026-07-28

Editorial rewrite that applies the shared-core writing rules to ITWS itself.

### Changed

- Rewrote authored prose across the repository for shorter sentences, one-purpose chunks, plain verbs, explicit references, and consistent terms.
- Rewrote rule statements across Rules 2.1.1–8.5.2 to meet the 20-word cap without intending to change conformance.
- Added the §0.7 self-application boundary. Metadata, templates, tables, quoted counterexamples, source names, and generated artifacts remain fixtures.
- Clarified Rules 2.3.4, 2.5.2, 2.7.2, 4.4.3, and 4.8.1. Also clarified Rules 5.4.3, 6.1.3, and 8.4.1.
- Corrected rule examples, word counts, cross-references, profile wording, Annex E rename guidance, and Annex F source mappings.
- Updated current-version declarations to 0.2.1-draft and regenerated Annex C.

## [0.2.0-draft] — 2026-07-28

Draft expansion from a research-only writing specification to the Invene Technical Writing Specification (ITWS).

### Changed

- Replaced the four-type research-only scope with a shared core and exactly eight profiles: `design-rfc`, `decision-record`, `procedure`, `explanation`, `incident`, `technical-report`, `research-paper`, and `investigation-log`.
- Replaced the single review gate with cumulative `core`, `reviewed`, and `publication` conformance tiers and profile-specific minimum tiers.
- Kept one working-software-engineer base reader for the shared core. Profile overlays may add familiar genre conventions but may not add domain knowledge or organization-local shorthand.
- Made the `research-paper` overlay expressly assume no machine-learning knowledge.
- Generalized Parts 2–8 from research-only prose to profile-aware vocabulary, structure, technical exactness, evidence, limitations, review, and release rules while preserving all permanent rule IDs.
- Added explicit `Profiles` applicability metadata to rules that do not apply to all eight profiles. Rules without that metadata remain shared core.
- Clarified that ordinary English is assumed, but specialized senses remain ladder-gated. Required Annex A definitions to be admitted in each document before use.
- Separated evidential strength and uncertainty from lifecycle or authority status in exact-item records and calibrated language.
- Made Annex B the sole notation baseline and mapped every profile's boundary dimensions to canonical Annex E slots.
- Reworked Annex E into one required-section skeleton per profile and specified the only permitted section renames and merges.
- Rebalanced Annex D across all profiles while retaining the two original research examples. Replaced the source-restricted expansion target with a source-diverse, per-profile milestone.
- Re-scoped Annex F. Diátaxis, ISO 26514, and IEC 82079-1 are general anchors. APA JARS, the NeurIPS Paper Checklist, and Model Cards apply only to `research-paper`.

### Added

- Added profile and domain metadata to Annex A. Retained the 15 machine-learning entries.
- Added the specialized stored-setting sense of `parameter` as their first ladder rung.
- Added reliability/platform and security/governance dependency chains.
- Added Annex B's closed profile registry and convention-only overlay boundary.
- Added profile coverage and balance rules for the examples corpus.
- Added `tools/itws_index.py`, the independent permanent-ID registry, and a regenerated Annex C with profile applicability and source metadata for all 161 rules.
- Added `tools/itws_checklist.py` to generate the four author passes and tier-specific conformance gates from Annex C.
- Added Rules 4.8.3, 7.1.6, and 8.3.5 to keep subsection ceilings, unknown-boundary disclosure, and reader-test retesting independently checkable.
- Added deprecation-replacement validation and content-hash provenance for generated checklists.

### Migration notes

- A document now declares ITWS 0.2.0-draft, one of the eight profile IDs, and a permitted conformance tier. Human-readable document labels are not additional profile IDs.
- Documents written against 0.1 retain their original declaration under §0.8. This repository does not include a checkable 0.1 snapshot.

## [0.1.0] — 2026-07-26

First-pass draft of the complete specification skeleton.

### Added

- Front matter §0.1–0.8: scope, assumed reader, conformance keywords and classes, references, meta-vocabulary, usage guidance, versioning, permanent rule numbers, and checkability.
- Part 1: design principles P1–P7 (including specific-over-generic), the two-layer model (normative), the rule template, precedence rules with three resolved collisions.
- Parts 2–7: first-pass rules for vocabulary and the term ladder, sentences, structure and path-agnostic prose, mathematical and empirical content, explanatory devices, and limitations/interpretation.
- Part 8: checklist generation and linter behavior (Rules 8.1.1–8.2.4).
- Part 8: reader testing (Rules 8.3.1–8.3.4) and the two-reviewer model (Rules 8.4.1–8.4.4).
- Part 8: waiver process and template (Rules 8.5.1–8.5.2).
- Annex A: entry format and 15-entry glossary seed with one complete dependency chain (model → … → fine-tuning/overfitting).
- Annex B: assumed-reader baseline v0.1 — assumed concepts, assumed notation (with explicit exclusions), explicitly-not-assumed list.
- Annex C: generation contract and generator sketch (index not yet generated).
- Annex D: paired-example format and 2 constructed illustrative rewrites.
- Annex E: fill-in skeletons for paper, technical report, experiment log, and negative-result note.
- Annex F: traceability matrix at section granularity.
- Annex G: this changelog.

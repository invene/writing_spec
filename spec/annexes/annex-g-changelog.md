# Annex G — Changelog

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Section 0.8 defines version semantics. Every entry that changes a rule cites the rule number. Rule numbers are permanent, and deprecation replaces deletion (§0.8).

## [Unreleased]

- Pending: validate Annex B with members across software engineering pod roles. Also validate that each profile overlay adds conventions only.
- Pending: pilot the §8.3 reader protocol on documents from multiple profiles. Keep pass/fail criteria provisional until then.
- Pending: widen Annex D's source mix. Every profile now has at least two examples, but all 21 non-research examples are constructed.
- Pending: run the four cold-start agent pilots listed in `spec/agent/README.md` §A.7. Each needs a fresh session that receives only the repository URL, a raw document, and a one-sentence rewrite request. The 0.6.0-draft release verified the machine path with the fixture suite; it did not verify the cold start.
- Pending: calibrate the Rule 3.5.1 noun-cluster detector against reader-test results. The lexical detector reports candidates and produces false positives on verb-noun homographs.

## [0.6.0-draft] — 2026-07-29

Draft change that makes the specification navigable by an artificial-intelligence agent. The change adds rule navigation metadata, a committed machine catalog, a repository-local linter, and four validation states.

### Added

- Added §1.6, which defines rule navigation metadata: closed value sets for target, constructs, chunk types, skeleton slots, layers, context scope, rewrite guidance, resources, and typed relations. Section 1.6.1 states that only the construct condition carries normative force and that a navigation field never narrows the profile envelope.
- Added §1.6.3, which generates the §1.4 precedence order as a machine relation. The generated layer restates §1.4 and never replaces it.
- Added the four navigation metadata lines to the §1.3 rule template, and annotated all 190 existing rules.
- Added §8.6 with Rules 8.6.1–8.6.5: the generation contract, stale-artifact rejection, the four validation states, the agent-record citation obligation, and the collision report.
- Added §E.0.2, which fixes the optional `Section map` syntax as an `itws-section-map` fenced block with closed rejection conditions.
- Added §E.0.3, which lets a skeleton declare a mutation policy. The `investigation-log` skeleton now declares its entries append-only.
- Added `spec/generated/agent/`, the committed machine catalog: `manifest.json`, `rules.jsonl`, `rule-graph.json`, `glossary.json`, `reader-baseline.json`, `examples.jsonl`, `phrase-lists.json`, and one profile manifest and skeleton per profile.
- Added `spec/agent/README.md`, the entry point for an agent that rewrites a governed document.
- Added the `itws` package: one parser and typed model, the compiler, the navigation catalog, the structural document index, the optional analysis and work-plan records, the patch guards, the linter, and the validator.
- Added `tools/itws_compile.py`, `tools/itws_retrieve.py`, `tools/itws_document.py`, `tools/itws_work.py`, `tools/itws_patch.py`, `tools/itws_lint.py`, `tools/itws_validate.py`, `tools/itws_annotate.py`, and `tools/itws_check_all.py`.
- Added `examples/agent-scripts/` with six copyable scripts, and `skills/itws-rewrite/SKILL.md`.
- Added `tests/` with unit tests and document fixtures for all eleven profiles, plus focused fixtures for a term used before definition, a reordered safety dependency, a widened claim, a detached caveat, two names for one artifact, an edited log entry, overlapping writes, and a stale source hash.
- Added eleven Annex D examples (D.13–D.23), reaching 23 examples with at least two for every profile.
- Added §1.6 annotation fields to the Annex D example format: chunk types, constructs, repair operators, and preservation notes.
- Added the §0.6 definitions of `navigation metadata`, `profile envelope`, and `generated artifact`.
- Added Annex F rows for §1.6, §8.6, and §E.0.2, and Annex F §F.5, which records the removed Vale dependency.

### Changed

- Rewrote §8.2. `itws-lint` is now a repository-local engine that uses only the Python standard library. The reference consumption environment can run Python but cannot install a binary or fetch a style package, and §8.2 now sets the tooling floor at what that environment can run.
- Restated every phrase list as a §8.2.1 phrase-list paragraph beside its own rule, so each living list has exactly one home and the linter reads it from the specification. The lists affected belong to Rules 2.1.3, 2.3.3, 2.6.3–2.6.11, 3.6.2, 3.9.1, 3.10.2, 3.10.4, 3.10.6, 4.10.5, and 6.5.4.
- Changed Rule 8.2.1's `Source` from "Vale / STE checker practice" to "STE checker practice". The rule statement is unchanged.
- Changed Rule 3.5.1 and Rule 3.5.2 from `Machine-checkable: yes` to `partial`. Counting nouns needs a part-of-speech reading that a standard-library checker cannot produce. Both rationales now record that limit, and the linter reports a candidate that a reader confirms. Neither rule statement, class, nor applicability changed.
- Extended Annex C with target, constructs, layers, context, rewrite, and precedence columns. The full rule record now lives in `rules.jsonl`, and Annex C is its human-readable view.
- Changed `tools/itws_checklist.py` to read the normalized model instead of parsing Annex C's rendered table. The checklist and the profile manifest now resolve one rule set, and `tools/itws_compile.py` fails when the two disagree.
- Migrated `tools/itws_index.py`, `tools/itws_checklist.py`, and `tools/itws_overlays.py` onto the shared parser. Their command-line arguments are unchanged; `--check` is additive on the index generator.
- Normalized every Annex D `Rules applied` field to permanent rule IDs. Section citations moved into the annotations.
- Split `AGENTS.md` by session purpose. A maintainer session edits the specification and owes a changelog entry and a version increment. A consumer session rewrites an external document and owes neither.
- Rewrote the root README with an agent-facing entry point, one application path for writers, and one for tool authors.
- Updated current-version declarations to 0.6.0-draft and regenerated Annex C.

### Compatibility

- This pre-1.0 minor release is not breaking for a governed document. No rule statement, class, applicability, permanent ID, section number, or tier obligation changed.
- Rules 8.6.1–8.6.5 are new mandatory rules, but they govern tooling and recorded evidence rather than a document's prose. A document that already satisfied §8.1 and §8.2 satisfies them.
- The two machine-checkability reclassifications reduce what tooling asserts. They do not change what either rule requires.
- Documents pinned to 0.5.x retain the 0.5.x layout, registry, applicability, and phrase lists under §0.4.4 and §0.8.

### Migration notes

- A tool that read the phrase lists from prose now reads `spec/generated/agent/phrase-lists.json`, or the phrase-list paragraphs the compiler reads.
- A tool that parsed Annex C's rendered table now reads `spec/generated/agent/rules.jsonl`.
- A new rule needs the four §1.6 metadata lines. `python3 tools/itws_annotate.py --spec-dir spec` writes them from `itws/annotations.py`.
- A rule marked `Machine-checkable: yes` needs a registered checker in `itws/lint/`; the compiler fails without one.
- A pipeline that treated a clean lint run as conformance now reads one of four states from `tools/itws_validate.py`.

## [0.5.1-draft] — 2026-07-28

Patch that defines the §8.4 owner review focus for `explanation`. This closes the gap that 0.5.0-draft recorded as pending.

### Added

- Added the `explanation` owner review focus to its overlay README: mechanism fidelity, example correctness, and the stated limits.
- Added the `explanation` example to the Rule 8.4.2 rationale's focus illustrations.

### Changed

- Removed the pending owner-review-focus item from `Unreleased`.
- Corrected the front-matter status label from `work-item-profile draft` to `overlay-layout draft`, matching the 0.5.x line.
- Updated current-version declarations to 0.5.1-draft and regenerated Annex C.

### Compatibility

- This is a patch release. The focus narrows the owner's attention and does not change the Rule 8.4.2 owner review scope, any rule statement, applicability, or tier obligation.

## [0.5.0-draft] — 2026-07-28

Draft reorganization that gives each profile overlay its own directory, separate from the shared core.

The reorganization lets a reader, writer, or tool load one profile and ignore every unrelated overlay.

### Added

- Added §1.5, which defines the overlay layout, the rule-placement policy, the load set, and their enforcement.
- Added `spec/overlays/` with a registry, eleven profile directories, and a `shared/` module directory.
- Added the profile-family concept with two families: work item (`epic`, `task`, `subtask`) and report (`technical-report`, `research-paper`).
- Added §0.6 definitions for `profile family` and `load set`, and extended the `rule` definition with rule placement.
- Added `tools/itws_overlays.py`, which validates directories, registry rows, declared minimum tiers, and module links.
- Added overlay discovery and rule-placement validation to `tools/itws_index.py`.
- Added a `File` column to Annex C and to each generated checklist line.
- Added the §1.5 traceability row and the overlay-layout entry to Annex F.

### Changed

- Moved each profile job statement from §4.3 to the `README.md` of its overlay directory.
- Moved each profile dependency-order statement from §4.4 to its overlay `skeleton.md`.
- Moved the §B.4 per-profile conventions to each overlay `reader.md`. Section B.4 now registers those files as §B.4.1–§B.4.11.
- Moved Annex E §§E.1–E.11 to each overlay `skeleton.md`. Annex E now holds the slot, rename, and merge policy and registers those files.
- Moved Rules 4.11.1–4.11.21 and 5.9.1–5.9.8 to the work-item overlays and to `overlays/shared/work-item.md`.
- Moved Rules 5.7.1–5.7.2 and 5.8.1–5.8.2 to `overlays/shared/report.md`.
- Moved the §8.3 reader-test outcomes and the §8.4 owner review focus to each overlay `README.md`.
- Retitled §5.7 from "Statistical evidence for research profiles" to "Statistical evidence for report profiles".
- Replaced the moved bodies of §§4.3, 4.4, 4.11, 5.7–5.9, §B.4, and Annex E with registries and pointers.
- Updated current-version declarations to 0.5.0-draft and regenerated Annex C.
- No rule statement, class, machine-checkability, source, applicability, permanent ID, or section number changed.

### Compatibility

- This pre-1.0 minor release is not breaking. A conforming 0.4.0-draft document remains conforming under 0.5.0-draft.
- Rule 4.11.1 and every other scoped rule keep their permanent IDs and their core section numbers.
- A citation of the form "Annex E §E.9" or "Annex B §B.4" resolves through the registry table in that annex.
- Documents pinned to 0.4.x retain the 0.4.x layout, registry, and applicability under §0.4.4 and §0.8.

### Migration notes

- A tool that read profile-scoped rules from `spec/04-structure.md` or `spec/05-mathematical-and-empirical-content.md` now reads them from the file named in Annex C's `File` column.
- A writer loads the §1.5.3 load set for one profile and ignores the other ten overlays.
- A new profile requires a directory with `README.md`, `reader.md`, `skeleton.md`, and `rules.md`, plus a registry row.
- A rule whose applicability narrows or widens moves to the file that §1.5.2 requires.

## [0.4.0-draft] — 2026-07-28

Breaking draft change that adds governed `epic`, `task`, and `subtask` work items.

### Added

- Added the three profile IDs to §0.2, Annex B, Annex E, and the profile-aware generators.
- Added §0.6 definitions for work-item hierarchy, journeys, paths, accepted behavior, DoD composition, and technical hints.
- Added Rules 4.11.1–4.11.21 for work-item titles, classification, hierarchy, invariant inheritance, path ownership, and technical hints.
- Added Rules 5.9.1–5.9.8 for one DoD, completion-condition verification, parent-child alignment, integrated acceptance, and epic completion.
- Added Annex E skeletons E.9–E.11 and one Annex D example for each new profile.
- Added section-level traceability rows for the new rule sets and skeletons in Annex F.
- Added minimum-tier registry validation to the checklist generator.

### Changed

- Expanded Rule 4.2.4 and Rule 4.4.3 applicability to `epic` and `task`.
- Expanded Rules 7.3.1–7.3.3 applicability to `task` and `subtask`.
- Added work-item exactness fields to §5.4 and boundary locations to §7.1.
- Added work-item reader tasks and review focus to Part 8.
- Changed the Annex D two-per-profile milestone from 16 examples to 22.
- Updated current-version declarations to 0.4.0-draft and regenerated Annex C.

### Compatibility

- This pre-1.0 minor release is breaking because it adds canonical profiles and mandatory profile rules.
- The shared core now governs eleven profiles.
- The `epic` minimum tier is `reviewed`.
- The `task` and `subtask` minimum tiers are `core`.
- Existing profile minimum tiers and the Annex B base-reader baseline remain unchanged.
- Documents pinned to 0.3.x retain the 0.3.x registry, applicability, and overlays under §0.4.4 and §0.8.

### Migration notes

- A structured issue-tracker item may claim ITWS conformance through `epic`, `task`, or `subtask`.
- A `task` now declares Outcome class and Change reason separately.
- Each work item has one authoritative Definition of done.
- A `subtask` maps to one parent task and one named parent completion condition.
- A delegated sad path remains summarized in its parent `task`.

## [0.3.0-draft] — 2026-07-28

Breaking draft change that broadens the base reader from a software engineer to any technical member of a software engineering pod.

### Changed

- Replaced the computer-science-curriculum, coding-fluency, engineering-tenure, and seasoned-engineer assumptions in §0.3 and Annex B.
- Defined a cross-functional base reader spanning software engineering, product design, engineering management, quality assurance, product, and operations roles.
- Retained basic software, delivery, quality, and quantitative concepts learned through regular proximity to software work.
- Made programming implementation, code and command literacy, systems internals, formal statistics, algebra, and most mathematical notation ladder-required.
- Updated §5.2 and §5.7 to match the narrower notation and statistical baselines.
- Defined `software engineering pod` in §0.6 and updated the `base reader` definition.
- Updated Annex A's function prerequisite label and replaced the ACM curriculum mapping in Annex F.
- Updated audience-sensitive framing, rationales, or examples for Rules 3.1.1–3.1.2, 3.2.2, 4.6.1, and 5.2.1–5.3.1.
- Updated audience-sensitive rationales or examples in Rules 5.4.1, 5.5.1–5.5.2, 5.7.1–5.7.2, 6.1.1, 6.2.1, 8.3.2, 8.4.1, and 8.4.3.
- Refreshed version fixtures or draft labels in Rules 2.6.4, 4.3.1, 4.7.2, 4.8.1–4.8.3, 8.1.1, 8.2.1, 8.2.3, and 8.3.1.
- No normative rule statement changed.
- Updated current-version declarations to 0.3.0-draft and regenerated Annex C.

### Removed

- Removed implementation-level programming, data-structure, algorithm, and complexity assumptions from §B.1.
- Removed systems, distributed-systems, and database-internals assumptions from §B.1.
- Removed first-year-undergraduate mathematics and formal probability assumptions from §B.1.
- Removed variables, function application, subscripts, scientific notation, summation, logarithms, factorial, Big-O, and set notation from §B.2.

### Compatibility

- This pre-1.0 minor release is breaking because Annex B removes assumed concepts and notation.
- The change affects all eight profiles and all three conformance tiers.
- Profile overlays, minimum tiers, and rule applicability remain unchanged.
- Documents pinned to 0.2.x retain their 0.2.x reader baseline under §0.4.4 and §0.8.

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

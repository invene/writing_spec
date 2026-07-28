# Invene Technical Writing Specification (ITWS)

ITWS is a controlled-language specification for technical documents. The specification adapts ASD-STE100's rule architecture.

ITWS adds practices for software documentation, information for use, and specific genres.

Each document uses one shared core and exactly one declared profile.

**Version 0.2.1-draft:** self-conformance rewrite draft.

## Architecture

Every conforming document declares these fields:

```text
ITWS version: 0.2.1-draft
Profile: <canonical profile ID>
Conformance tier: <core | reviewed | publication>
```

The shared core governs vocabulary, sentences, structure, exact content, explanatory devices, limitations, and compliance.

A profile overlay adds only the purpose, structure, and other rules specific to its genre. Rules apply to all profiles by default.

A rule with different applicability includes a `**Profiles:**` metadata line.

The base reader is a working software engineer. Annex B defines that baseline and each profile's genre-knowledge overlay.

An overlay does not admit domain terminology. For example, the `research-paper` overlay assumes no knowledge of machine learning.

## Profile registry

The canonical profile IDs and labels are:

| Profile ID | Label | Minimum conformance tier |
|---|---|---|
| `design-rfc` | Design / RFC | `reviewed` |
| `decision-record` | Architecture decision record | `core` |
| `procedure` | Runbook / how-to | `reviewed` |
| `explanation` | Concept / explanation | `core` |
| `incident` | Incident report / postmortem | `reviewed` |
| `technical-report` | Technical report | `reviewed` |
| `research-paper` | Research paper | `publication` |
| `investigation-log` | Investigation log | `core` |

The conformance tiers are cumulative.

`core` requires all applicable mandatory rules, lint, and a recorded self-check.

`reviewed` adds independent reviews by a subject-matter owner and reader proxy.

`publication` adds an independent reader test and release checks.

A profile may use a tier above its minimum.

## Contents

| File | Contents |
|---|---|
| [00-front-matter.md](00-front-matter.md) | §0.1–0.8: foreword, scope and profile registry, assumed reader, conformance tiers, references, meta-vocabulary, usage, and versioning policy |
| [01-foundations.md](01-foundations.md) | Part 1: design principles, the exact/plain two-layer model, tier-proportional acceptance, the rule template and applicability convention, and precedence |
| [02-words-and-vocabulary.md](02-words-and-vocabulary.md) | Part 2: word rules, permitted vocabulary, the term ladder, definition quality, glossary governance, prohibited patterns, and naming |
| [03-sentences.md](03-sentences.md) | Part 3: length, one claim per sentence, voice, tense, noun clusters, reference, ambiguity, punctuation, hedging, and formulaic constructions |
| [04-structure.md](04-structure.md) | Part 4: chunk model, claim-first ordering, profile structures and skeletons, headings, progressive disclosure, navigation, density budgets, path-agnostic prose, and formatting |
| [05-mathematical-and-empirical-content.md](05-mathematical-and-empirical-content.md) | Part 5: exact-content rules, notation, equations in prose, evidence reporting, figures, status calibration, statistics, reproducibility, and verification |
| [06-explanatory-devices.md](06-explanatory-devices.md) | Part 6: analogies, worked examples, intuition blocks, diagrams, and repetition |
| [07-limitations-caveats-interpretation.md](07-limitations-caveats-interpretation.md) | Part 7: required limitations, caveat co-location, observation/interpretation separation, and generalization claims |
| [08-review-compliance-tooling.md](08-review-compliance-tooling.md) | Part 8: profile-aware checklists, automated checks, self-checks, independent review, reader testing, release checks, and waivers |
| [annexes/annex-a-glossary.md](annexes/annex-a-glossary.md) | Annex A: the glossary (normative, living) |
| [annexes/annex-b-assumed-reader-baseline.md](annexes/annex-b-assumed-reader-baseline.md) | Annex B: the base-reader baseline and profile overlays (normative) |
| [annexes/annex-c-rule-index.md](annexes/annex-c-rule-index.md) | Annex C: rule index (build artifact) |
| [annexes/annex-d-examples-corpus.md](annexes/annex-d-examples-corpus.md) | Annex D: examples corpus |
| [annexes/annex-e-document-skeletons.md](annexes/annex-e-document-skeletons.md) | Annex E: profile skeletons |
| [annexes/annex-f-traceability.md](annexes/annex-f-traceability.md) | Annex F: mapping to source frameworks |
| [annexes/annex-g-changelog.md](annexes/annex-g-changelog.md) | Annex G: changelog |

## Reading order

Writers should read Part 1 once. They should then choose a profile and permitted tier.

Writers should draft from the corresponding Annex E skeleton. Keep Parts 2, 3, and 5 open while drafting.

Reviewers and releasers should read §0.4, §0.7, and Part 8.

Rule IDs are permanent. A document is evaluated against the exact ITWS version that it cites.

Annex G records the Research Writing Specification (RWS) 0.1 lineage. This repository does not contain a checkable 0.1 snapshot.

## Build artifacts

Regenerate Annex C after changing a rule's header, class, machine-checkability, source, or `Profiles` metadata:

```text
python3 tools/itws_index.py --spec-dir spec --out spec/annexes/annex-c-rule-index.md
```

The generator validates permanent rule-ID uniqueness against `spec/rule-ids.txt`.

Before writing the index, the generator also validates canonical profile metadata.

After approving a new ID, run the command once with `--update-registry`. Never remove an ID from the registry.

Generate a document checklist from Annex C. Use the exact declared version, profile, and permitted tier:

```text
python3 tools/itws_checklist.py \
  --spec-version 0.2.1-draft \
  --profile design-rfc \
  --tier reviewed \
  --out design-rfc-checklist.md
```

# Invene Technical Writing Specification (ITWS)

ITWS is a controlled-language specification for technical writing. The specification adapts ASD-STE100's rule architecture.

ITWS adds practices for software documentation, information for use, and specific genres.

Each governed unit uses one shared core and exactly one declared profile. Eleven profiles govern Markdown documents; `maintenance-comment` governs a comment change set inside a host source file (§0.2.1).

**Version 0.8.0-draft:** agent-navigation draft.

## Architecture

Every conforming governed unit declares these fields, in its Markdown front matter or in its JSON declaration carrier:

```text
ITWS version: 0.8.0-draft
Profile: <canonical profile ID>
Conformance tier: <core | reviewed | publication>
```

The shared core governs vocabulary, sentences, structure, exact content, explanatory devices, limitations, and compliance.

A profile overlay adds only the purpose, structure, and other rules specific to its genre. Rules apply to all profiles by default.

A rule with different applicability includes a `**Profiles:**` metadata line.

Each overlay has its own directory under [overlays/](overlays/). A writer, reviewer, or tool loads the shared core, the shared annexes, one profile directory, and the shared modules that directory lists. Section 1.5 defines the layout, the rule-placement policy, and the load set.

The base reader is any working member of a software engineering pod. Annex B defines that technical baseline and each profile's genre-knowledge overlay.

An overlay does not admit domain terminology. For example, the `research-paper` overlay assumes no knowledge of machine learning.

## Profile registry

The canonical profile IDs and labels are:

| Profile ID | Label | Minimum conformance tier | Surface |
|---|---|---|---|
| `design-rfc` | Design / RFC | `reviewed` | `markdown-document` |
| `decision-record` | Architecture decision record | `core` | `markdown-document` |
| `procedure` | Runbook / how-to | `reviewed` | `markdown-document` |
| `explanation` | Concept / explanation | `core` | `markdown-document` |
| `incident` | Incident report / postmortem | `reviewed` | `markdown-document` |
| `technical-report` | Technical report | `reviewed` | `markdown-document` |
| `research-paper` | Research paper | `publication` | `markdown-document` |
| `investigation-log` | Investigation log | `core` | `markdown-document` |
| `epic` | Epic | `reviewed` | `markdown-document` |
| `task` | Task | `core` | `markdown-document` |
| `subtask` | Subtask | `core` | `markdown-document` |
| `maintenance-comment` | Maintenance comment set | `core` | `hosted-comment-set` |

The conformance tiers are cumulative.

`core` requires all applicable mandatory rules, lint, and a recorded self-check.

`reviewed` adds independent reviews by a subject-matter owner and reader proxy.

`publication` adds an independent reader test and release checks.

A profile may use a tier above its minimum.

## Contents

| File | Contents |
|---|---|
| [00-front-matter.md](00-front-matter.md) | §0.1–0.8: foreword, scope and profile registry, assumed reader, conformance tiers, references, meta-vocabulary, usage, and versioning policy |
| [01-foundations.md](01-foundations.md) | Part 1: design principles, the exact/plain two-layer model, tier-proportional acceptance, the rule template and applicability convention, precedence, the overlay layout, and the §1.6 rule navigation metadata |
| [02-words-and-vocabulary.md](02-words-and-vocabulary.md) | Part 2: word rules, permitted vocabulary, the term ladder, definition quality, glossary governance, prohibited patterns, and naming |
| [03-sentences.md](03-sentences.md) | Part 3: length, one claim per sentence, voice, tense, noun clusters, reference, ambiguity, punctuation, hedging, and formulaic constructions |
| [04-structure.md](04-structure.md) | Part 4: chunks, ordering, profile skeletons, headings, progressive disclosure, navigation, density, path-agnostic prose, formatting, and the work-item hierarchy section that points to its overlays |
| [05-mathematical-and-empirical-content.md](05-mathematical-and-empirical-content.md) | Part 5: exact content, notation, equations, evidence, figures, calibration, and the statistics, reproducibility, verification, and definition-of-done sections that point to their overlays |
| [06-explanatory-devices.md](06-explanatory-devices.md) | Part 6: analogies, worked examples, intuition blocks, diagrams, and repetition |
| [07-limitations-caveats-interpretation.md](07-limitations-caveats-interpretation.md) | Part 7: required limitations, caveat co-location, observation/interpretation separation, and generalization claims |
| [08-review-compliance-tooling.md](08-review-compliance-tooling.md) | Part 8: profile-aware checklists, automated checks, self-checks, independent review, reader testing, release checks, waivers, and the §8.6 generated-artifact contract with its four validation states |
| [annexes/annex-a-glossary.md](annexes/annex-a-glossary.md) | Annex A: the glossary (normative, living) |
| [annexes/annex-b-assumed-reader-baseline.md](annexes/annex-b-assumed-reader-baseline.md) | Annex B: the base-reader baseline and the reader-overlay registry (normative) |
| [annexes/annex-c-rule-index.md](annexes/annex-c-rule-index.md) | Annex C: rule index (build artifact) |
| [annexes/annex-d-examples-corpus.md](annexes/annex-d-examples-corpus.md) | Annex D: examples corpus |
| [annexes/annex-e-document-skeletons.md](annexes/annex-e-document-skeletons.md) | Annex E: slot policy and the profile-skeleton registry |
| [annexes/annex-f-traceability.md](annexes/annex-f-traceability.md) | Annex F: mapping to source frameworks |
| [annexes/annex-g-changelog.md](annexes/annex-g-changelog.md) | Annex G: changelog |
| [overlays/README.md](overlays/README.md) | the overlay registry, directory contents, and shared modules |
| [overlays/`<profile ID>`/](overlays/) | one profile's job, reader overlay, skeleton, and scoped rules |
| [overlays/shared/](overlays/shared/) | the rules that one profile family shares |
| [agent/README.md](agent/README.md) | the entry point for an artificial-intelligence agent that rewrites a governed document |
| [generated/agent/](generated/agent/) | the committed navigation catalog (build artifact) |

## Reading order

Writers should read Part 1 once. They should then choose a profile and permitted tier.

Writers should then load that profile's overlay directory and draft from its skeleton. Keep Parts 2, 3, and 5 open while drafting.

Reviewers and releasers should read §0.4, §0.7, and Part 8.

Rule IDs are permanent. A document is evaluated against the exact ITWS version that it cites.

Annex G records the Research Writing Specification (RWS) 0.1 lineage. This repository does not contain a checkable 0.1 snapshot.

## Build artifacts

The Markdown files in this directory are authoritative. Every artifact below derives from them, and a disagreement is a specification defect.

### Generated artifact contract

`generated/agent/` holds the machine catalog that §8.6 defines. It is committed, so a reader can inspect the current version without running a build.

| File | Contents |
|---|---|
| `manifest.json` | version, schema version, generation command, source hashes, artifact hashes, and counts |
| `rules.jsonl` | one rule atom per rule: identity, statement, rationale, examples, navigation metadata, relations, and source span |
| `rule-graph.json` | typed and resolved rule relations, plus the §1.4 precedence layer of every rule |
| `glossary.json` | Annex A entries with their ladder prerequisites |
| `reader-baseline.json` | Annex B assumptions, exclusions, and each profile's overlay |
| `examples.jsonl` | Annex D paired examples and each rule's contrasting pair |
| `phrase-lists.json` | the generated linter inputs |
| `profiles/<profile>.json` | the resolved profile envelope, load set, tier, surface, and review focus |
| `skeletons/<profile>.json` | ordered slots, renames, merges, and mutation policies |

Generation is byte deterministic. Two runs over one unchanged source tree produce identical bytes.

### Commands

Run everything at once:

```text
python3 tools/itws_check_all.py
```

Run one step at a time:

| Command | What it does |
|---|---|
| `python3 tools/itws_overlays.py --spec-dir spec` | checks the overlay layout, registry, and declared minimum tiers |
| `python3 tools/itws_annotate.py --spec-dir spec --check` | confirms every rule carries its curated §1.6 metadata |
| `python3 tools/itws_index.py --spec-dir spec` | regenerates Annex C; `--check` compares instead of writing |
| `python3 tools/itws_compile.py --spec-dir spec` | regenerates the catalog; `--check` compares instead of writing |
| `python3 -m unittest discover -s tests -t .` | runs the unit tests |

Regenerate Annex C and the catalog after changing a rule's header, class, machine-checkability, source, `Profiles` metadata, or §1.6 navigation metadata.

After approving a new permanent rule ID, run the index generator once with `--update-registry`. Never remove an ID from `rule-ids.txt`.

Generate a document checklist. Use the exact declared version, profile, and permitted tier:

```text
python3 tools/itws_checklist.py \
  --spec-version 0.8.0-draft \
  --profile design-rfc \
  --tier reviewed \
  --out design-rfc-checklist.md
```

### Agent commands

These read the generated catalog and a governed document. None of them changes the specification.

| Command | What it does |
|---|---|
| `python3 tools/itws_retrieve.py get-profile <profile>` | the full profile envelope, load set, and review focus |
| `python3 tools/itws_retrieve.py search-rules "<query>" --profile <profile>` | ranked search with match reasons |
| `python3 tools/itws_retrieve.py expand-relations <rule> --depth 2` | typed relation traversal from agent-selected seeds |
| `python3 tools/itws_document.py index --input <document>.md` | the structural manifest, with no semantic labels |
| `python3 tools/itws_work.py validate --plan <plan>.json --document <document>.md` | cycle, span, resource, and wave checks over an agent-authored plan |
| `python3 tools/itws_patch.py check --base <a>.md --proposed <b>.md` | changed ranges, affected spans, stale hashes, and out-of-slice edits |
| `python3 tools/itws_lint.py --input <document>.md` | the repository-local linter |
| `python3 tools/itws_validate.py --input <document>.md` | the four-state conformance report |
| `python3 tools/itws_comment.py validate --carrier <set>.json` | the same four states for a comment change set; `index`, `scan-path`, `lint`, and `stale` cover the earlier steps |

An agent that needs something these commands do not cover imports `itws` directly and writes its own script. [agent/README.md](agent/README.md) describes that path.

---
name: itws-rewrite
description: Write, review, or rewrite a document against the Invene Technical Writing Specification (ITWS). Use when asked to make a design RFC, decision record, procedure or runbook, explanation, incident report, technical report, research paper, investigation log, epic, task, or subtask conform to ITWS; when asked to review or check a document against ITWS rules; when asked to govern the code comments a change adds, edits, or removes (the maintenance-comment profile); or when asked to bring an inventory, register, or data-sources spreadsheet under ITWS (the data-table profile).
---

# Write or rewrite a document against ITWS

ITWS 1.0.0 is a markdown-only specification. There is no Python package, no linter, no validator, and no generated catalog. You read the rules, you apply them, and you report what you checked. There is no machine `pass` result to hide behind.

The specification lives at https://github.com/invene/writing_spec. Work from a checkout; if you are already inside one, the paths below are relative to its root.

## 1. Load the rule set

Load these files, in this order, and **exactly one** profile:

```text
spec/legend.md          notation and the voice fence — read first
spec/ontology.md        external standards; recall is optional, never block on a fetch
spec/core.md            the shared normative core
spec/phrases.md         literal prohibited and replacement strings
spec/glossary.md        canonical admitted terms
spec/reader.md          what the assumed reader knows
spec/profiles/<id>.md   exactly one file from spec/profiles/
```

That set is the complete applicable rule set. Nothing else needs retrieving, and the whole load runs about 22,000 tokens, so it fits alongside the document you are working on.

Read `spec/legend.md` before anything else. It fixes the `ID | C | Rule` notation, and it states the voice fence described below.

## 2. Pick the profile

If the document declares a profile, use that one. If it does not, classify it against the profile registry in core §0.1 — each profile ID is listed there with the job it does — and say which one you chose and why. If two fit equally well, ask.

Never load two profiles. A document that seems to need two needs companion documents instead (core §0.1).

## 3. Respect the voice fence

The specification is written in compressed notation: dropped articles, fragments, symbols. **Nothing you produce is.**

| Surface | Voice |
|---|---|
| `spec/` files | compressed, for reading only |
| the document you write or rewrite | normal professional English, full sentences, ITWS rules applied |
| findings, commit messages, replies to the user | normal professional English |

Reading compressed input biases output toward compressed output. Check your draft against this before returning it. A rewrite that reads like `spec/core.md` has failed §3 and §4.

## 4. Read and classify before you edit

Read the document first. For each passage, decide its §4.1 chunk purpose and its layer — exact or plain, under the core §1.2 two-layer model. That judgment is yours; nothing decides it for you.

Note the document's declared ITWS version. A document is checked against **its** declared version, not the newest one.

## 5. Apply the rules

Work rule by rule, by ID. Where two applicable rules collide on one passage, use the core §1.3 precedence order. Never resolve a collision ad hoc.

Exact content — claims, requirements, interfaces, invariants, procedure steps, measurements — is never edited to satisfy a style rule. Repair the surrounding text and report the local limitation instead.

## 6. Self-check before returning

Core §8 sets these obligations. All of them apply every time.

1. **Cite the rule.** Every finding and every material semantic judgment names an ID: "ITWS §4.12.3". A finding without an ID is not a finding.
2. **Report, never invent.** A missing fact is reported as missing. Never generate a value, citation, timestamp, owner, or measurement to fill a slot. This outranks completing the draft.
3. **Continue around blocks.** An unresolved span does not stop work on independent spans. Return the best safe draft plus an explicit missing-fact list.
4. **Walk the scan path.** Read the title, the headings, and the opening sentences alone (core §4.12). Confirm the profile's shallow-model outcome still survives, with its status, strength, and material boundaries intact. Two profiles replace this path with their own: `maintenance-comment` (§4.13.9) and `data-table` (§4.14.18). Walk whichever one the declared profile defines.
5. **Set the AI disclosure.** You are generative AI tooling. If you contributed any content, the `AI disclosure` field is at least `assisted` (core §0.5, §4.3.4). State what you did — which sections you drafted or rewrote. For review, write `not yet reviewed` unless the user has told you a review happened; naming a reviewer you cannot verify violates obligation 2. Never leave a stale `none` on a document you edited, and never downgrade an existing value.
6. **State coverage.** Say which rules you checked and which you did not. A clean self-check is a disclosed-coverage statement, not a certification.

## 7. Return

Return the rewritten document, the missing-fact list, and the findings with their rule IDs. Say plainly what you could not resolve.

## What you must not do

- Do not edit anything under `spec/`. Changing the specification itself is a maintainer session with its own rules, changelog entry, and version bump; see `AGENTS.md` in the repository.
- Do not change `CHANGELOG.md` or the declared ITWS version.
- Do not invent a threshold, a measurement, a source, an owner, or an acceptance condition. Report it as missing.
- Do not weaken or widen an exact statement to make a sentence shorter. Core §3.1.4 requires a split; core §5.1.1 forbids the change.
- Do not report a document as conforming when you did not check the rules that would decide it. Report coverage instead.
- Do not edit a comment or its surrounding code merely to force agreement between them. ITWS §4.13.6, in the `maintenance-comment` profile, requires preserving the conflict, reporting it, and continuing elsewhere.

# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-08-03

The first stable release. ITWS becomes a markdown-only specification read directly by a person or an agent.

### Added

- **Rule 4.3.4 — AI disclosure.** Every governed unit declares an `AI disclosure` field alongside `ITWS version` and `Profile`, on the same surface. Closed values: `none`, `assisted`, `generated`. Any value other than `none` carries a note stating what the tooling did and who reviewed the result; where no review has happened, the note says `not yet reviewed` rather than naming a reviewer.

  The field records provenance for transparency. **It does not affect the conformance result** — conformance remains a property of the text, not of its authorship (core §0.5). A `generated` unit satisfying every applicable mandatory rule conforms.

  Affects: core §0.5 (declaration block), core §4.3 (new rule), `maintenance-comment` (the `Change scope` carrier field). No reader assumption changes. Every profile is affected, because the declaration is a document element rather than a profile slot.

- **Declaration fields are metadata.** Core §0.5 now states that §3 sentence rules do not apply to declaration fields, so the disclosure note's punctuation is not judged as prose.

- **`AGENTS.md` self-check step 5.** A rewriting agent must set the disclosure to at least `assisted`, must not leave a stale `none` or downgrade an existing value, and must not name a reviewer it cannot verify.

- **The `tabular-document` surface and the `data-table` profile.** ITWS gains a third governed surface and a thirteenth profile, so that register-style workbooks are governed rather than excluded. The governed artifact is the table itself, not a documentation layer over a grid, so nothing anchors into an ungoverned substrate.

  A `tabular-document` is a workbook of named sheets: one Title sheet, one Glossary sheet, and one or more data grids of homogeneous rows. Cells hold governed prose. Rendering is outside conformance, as Markdown rendering is, and the file format — `.xlsx`, a CSV set, or a hosted sheet — is a carrier rather than a conformance surface.

  Affects: core §0.1 (registry row), §0.2 (surface), §0.3 (computational workbooks excluded), §0.5 (applicability count, declaration surface), §0.6 (vocabulary pointer), §4.2.4 (profile exclusion list), §4.12.1 (scan-path replacement note), and the new §4.14 pointer. New file `spec/profiles/data-table.md` carries rules §4.14.1 through §4.14.21. No reader-baseline item is added or removed, so no existing document's admission obligations change.

- **Four named exceptions, scoped to `data-table` alone.** §4.14.6 displaces §2.3.1 and §2.3.3 — a table has no linear reading order, so define-before-first-use is unsatisfiable, and a Glossary registry entry replaces it. §4.14.9 displaces §4.8.1, because a per-page admission budget has no page to count; §4.14.10 substitutes a per-cell reader-effort bound. §4.14.18 displaces §4.12.1 with a scan surface — Title sheet, sheet names, header rows, and the registry `Columns` section — while §4.12.2 through §4.12.4 continue to govern it unchanged.

  Each exception is mandatory and names the rule it displaces, per core §1.3 item 2. No other profile is affected.

- **Two `data-table` rules with no precedent elsewhere.** §4.14.5 requires each registry `Columns` entry to declare its column's §7.3 role — observation, interpretation, or metadata — which makes the observation/interpretation split checkable from the Glossary sheet instead of by reading every row. §4.14.14 treats a row ID, a column header, and a value from a declared closed value set as metadata rather than governed prose, following the precedent core §0.5 sets for declaration fields.

### Removed — breaking

- **The `itws` Python package.** Parser, model, compiler, catalog builder, linter, validator, and scaffolds.
- **Every `tools/` command.** `itws_compile.py`, `itws_validate.py`, `itws_lint.py`, `itws_retrieve.py`, `itws_document.py`, `itws_patch.py`, `itws_index.py`, `itws_annotate.py`, `itws_overlays.py`, `itws_check_all.py`, and the rest.
- **The generated navigation catalog** under `spec/generated/agent/`: `manifest.json`, `rules.jsonl`, `profiles/*.json`, `phrase-lists.json`, `glossary.json`, `examples.jsonl`.
- **The test suite** (`tests/`) and the copyable agent scripts (`examples/agent-scripts/`).
- **The machine result.** There is no `pass` / `fail`. Rules 8.2.1, 8.2.2, 8.2.3, 8.2.5, 8.6.1, 8.6.2, and 8.6.6 are withdrawn; their IDs stay reserved and are never reassigned. Part 8 is now a self-check procedure.
- **Per-rule tool metadata.** `Machine-checkable`, `Constructs`, `Navigation`, `Resources`, and `Relations` lines are gone from every rule, along with the §1.6 closed value sets and the generated precedence table. §1.4's precedence order remains and is authoritative.
- **The non-normative `assurance/` companion** and the `skills/` directory.

Any conformance claim recorded against 0.10.0-draft or earlier does not carry over. Re-check the document against 1.0.0, or keep citing the version it was checked against.

### Changed — breaking

- **Tree layout.** The numbered chapter files (`spec/00-front-matter.md` … `spec/08-textual-conformance-and-machine-checking.md`), Annexes A–G, and `spec/overlays/<profile>/{README,reader,skeleton,rules}.md` are replaced by:

  | New file | Replaces |
  |---|---|
  | `spec/legend.md` | new — notation and the voice fence |
  | `spec/ontology.md` | Annex F |
  | `spec/core.md` | Parts 0–8 |
  | `spec/phrases.md` | the §8.2.1 phrase-list paragraphs |
  | `spec/glossary.md` | Annex A |
  | `spec/reader.md` | Annex B |
  | `spec/profiles/<id>.md` | Annex E §E.n + `spec/overlays/<id>/` (all four files) |

- **Rule statements are compressed.** Every rule keeps its ID, class, and normative force. Rationales, paired compliant/non-compliant examples, and cross-reference lines are dropped. The specification is now written in the compressed notation `spec/legend.md` defines.
- **Voice fence added.** `spec/legend.md` and `AGENTS.md` state that the compression is an input encoding only. Governed documents, findings, and commit messages stay in normal professional English. This is new, and it binds.
- **Load set.** Now `legend` + `ontology` + `core` + `phrases` + `glossary` + `reader` + exactly one profile — about 22,000 tokens, down from roughly 150,000 tokens of authoritative markdown plus a 196,000-token generated catalog. §1.5's overlay layout and placement policy are replaced by the placement table in `AGENTS.md`.
- **Shared rules are repeated, not referenced.** Rules scoped to several profiles (4.11.9, 4.11.14, 4.11.17, 5.9.1, 5.9.2, 5.9.8, 5.7.1, 5.7.2, 5.8.1, 5.8.2) now appear verbatim in each profile file that carries them, replacing `spec/overlays/shared/`.
- **Profile-scoped vocabulary moved out of core.** Work-item terms moved to `epic`, `task`, and `subtask`; hosted-comment terms moved to `maintenance-comment`.
- **External sources carry a recall policy.** `spec/ontology.md` marks each source `required` or `optional` and instructs against blocking on a fetch. Only RFC 2119 / RFC 8174 is `required`.

### Kept

- **Every permanent rule ID**, unchanged. §2.1.1 in 1.0.0 is the rule §2.1.1 was in 0.10.0-draft. Existing citations remain valid.
- **Every rule class.** No rule was reclassified in either direction.
- **All twelve profile IDs carried over from 0.10.0-draft**, with their jobs, shallow-model outcomes, skeleton slots, permitted renames, and permitted merges. `data-table` is new in this release, bringing the registry to thirteen.
- **The assumed-reader baseline**, complete. No item was added or removed, so no document's admission obligations change.
- **Every phrase list**, string for string.
- **All 24 glossary entries**, with their ladder prerequisites.
- **The ITWS-original doctrines**: two-layer model, term ladder, open-but-gated vocabulary, scan path and shallow-model outcomes, evidence record, calibrated strength, caveat placement, path-agnostic prose, work-item hierarchy, definition-of-done composition, and the maintenance-comment surface.

### Why

The 0.x tree cost roughly 370,000 tokens of tooling, tests, and generated artifacts to carry, and the machine check covered only the rules a standard-library linter could decide. The rules a reader most needs help with were the ones the linter could never reach. 1.0.0 spends the whole budget on the rules themselves and puts the judgment where it always was.

---

## Earlier versions

0.1.0 through 0.10.0-draft were released between 2026-07-26 and 2026-07-29 under the tool-backed architecture. 0.1.0 used the name *Research Writing Specification (RWS)*; that name and its four-type conformance model remain valid for documents citing 0.1.0.

Those releases are recoverable from git history. Their per-version detail lived in `spec/annexes/annex-g-changelog.md`, removed in 1.0.0. The pre-1.0 checkability guarantee did not promise a retained revision for a draft, and 1.0.0 makes no such promise retroactively: a document citing a 0.x draft is re-pinned to 1.0.0 before its conformance is recorded.

From 1.0.0 onward every released version is retained.

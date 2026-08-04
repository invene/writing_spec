# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [Semantic Versioning](https://semver.org/).

## [1.0.0] — amended 2026-08-04

**1.0.0 is pre-release.** The amendments below land in 1.0.0 in place, with no version bump, because 1.0.0 has not been declared stable. Core §9's semantic-versioning rules start binding at that declaration. Under §9 as written, several of these changes would be **major**: §5.4.6 adds a mandatory rule, §4.13.3 tightens one, and §5.9.6 and §5.9.8 are withdrawn.

Each amendment comes from a field report filed against 1.0.0 by a real consumer session, tracked as [STY-71](https://linear.app/inveneprod/issue/STY-71) and its children.

### Amended — text is governed, process is not (STY-81, closing STY-68 and STY-70)

ITWS is agnostic of process. The §0.5 declaration block is now stated to be the **only** process artifact the specification defines. Nothing else records review state, approval state, or lifecycle position, and no rule conditions conformance on an event outside the text.

The observed failure: a session convened to fix prose ended up litigating what was approved, what could close, and whether the owner's own review counted — with the specification as its citation. An opt-in partition would have left that failure available, so the content is removed rather than reclassified.

- **New in core §0.5** — the *Text, not process* boundary, with its subject-versus-passage test. A process state that is the document's own subject stays exact content: a `decision-record`'s `Status`, an `incident`'s resolution state, an `investigation-log`'s hypothesis state, a `data-table` status column. All four are unchanged.
- **Withdrawn: §5.9.6, §5.9.8.** Acceptance procedure and closing gates. Both IDs stay reserved and are never reassigned (core §9). §5.9.8 leaves `epic`, `task`, and `subtask`; §5.9.6 leaves `task`. §5.9.5 already carries §5.9.6's textual content — a task whose acceptance would follow from its subtasks alone has written no integrated-acceptance check.
- **Amended: §5.6.2.** Strength now matches "the evidence the document carries for it". The coupling to approval status is gone; the decision semantics already live inside the `adopted` and `proposed` tier definitions, which are unchanged.
- **Amended: core §5.4 evidence record — field 6 removed.** The **open question STY-81 left to this session is decided by removal.** "Lifecycle or authority status" was the last place process state was mandatory document content outside the stamp. STY-68's reader-protection argument is answered inside the text instead: §5.6 now states that the tier carries the settled/unsettled distinction, so an unsettled item takes the `proposed` or `interpretive` tier and reads correctly from the tier alone. The record is now **five** shared fields.
- **Amended slots.** `epic` `Summary` drops "approval or alignment requested"; `epic` `Task map` and `task` `Subtask map` drop "current ownership or status"; `task` `Summary` drops "current lifecycle state". A document may state any of these where it genuinely has them; no slot requires them. *The two `map` slots are not named in STY-81's enumeration; they are removed under its definition of done, which reaches any slot requiring workflow state as document content.*
- **Amended shallow-model outcomes.** `epic` and `design-rfc` no longer put approval status on the scan path; both now carry the §5.6 strength instead. An unapproved design read as settled — `design-rfc`'s sharpest hazard — is protected by the `proposed` tier.
- **`AGENTS.md` and `skills/itws-rewrite/SKILL.md`** both state the process fence: the agent governs the text, records the owner's account of their own review without overruling it, and never invents a reviewer.

Reader assumptions: unchanged. No baseline or genre-knowledge item is added or removed.

### Added — locators on external references (STY-75)

- **New rule §5.4.6 (`M`).** A first reference to an external source or artifact carries a resolvable locator: a URL, a DOI, or a path valid at the declared scope. Later references use the established short name (§2.1.2). Where no locator exists, the reference says so; §8 obligation 2 bars inventing one.

§2.6.8 required naming a source, §2.7.4 a version pin, and §5.4.3 that a citation resolve — so `see CLP-123` satisfied all three while leaving the finding step to the reader. Locator and pin are distinct obligations: a link without a pin drifts, a pin without a link cannot be followed. §5.4.3 now tests the locator §5.4.6 requires.

Affects: core §5.4 (new rule and prose). §2.6.8, §2.7.4, and §5.4.3 are unchanged in wording and now compose with §5.4.6. Every profile inherits the rule. No reader assumption changes.

### Added — epic-scoped vocabulary (STY-62)

The term ladder admits per document (§2.3.1) and caps admissions per page (§4.8.1). Neither composes across a *family* of work items sharing one domain vocabulary: a 500-word `task` depending on eight family terms had to duplicate roughly 200 words of verbatim definition (§6.5.1) or fail §2.3.1.

- **New rule §2.3.5 (`P`).** A child work item may use a term its ancestor `epic` admits, without re-admitting it.
- **New rule §2.3.6 (`M`).** The child names each inherited term and the admitting `epic` in the slot carrying its parent reference. The pointer is explicit and resolvable, never assumed.
- **New rule §4.8.4 (`M`).** An inherited term counts against the admitting `epic`'s §4.8.1 budget, never a child's.
- **New optional `epic` slot: `Shared vocabulary`.** Entries satisfy §2.3 and §2.4 exactly as in-document definitions do.
- **Amended slots.** `task` `Parent and invariants` and `subtask` `Boundaries and invariants` now carry the inherited-term list.

The unbounded-inheritance cap STY-62 raised as an option is **not** adopted — no defensible number exists yet. A child expected to circulate alone may recall an inherited definition verbatim under §6.5.3, which is already permitted and needs no new rule.

Affects: core §2.3, §4.8; `epic`, `task`, `subtask`. §2.3.1 through §2.3.4 and §4.8.1 are unchanged in wording. No reader assumption changes.

### Changed — the maintenance-comment anchor is content-addressed (STY-63)

At one point 165 of 660 recorded spans — a quarter of a corpus — pointed at lines that did not carry the comment they claimed, and every one satisfied the only available check, because a span that fits inside the file proves nothing.

- **Amended §4.13.3 (`M`).** An anchor is now the host file, the enclosing named construct, and a **comment hash** of the comment's own text with markers stripped. The line span is no longer part of it. This tightens a mandatory rule.
- **New rule §4.13.10 (`M`).** An anchor resolves when exactly one comment in the named source matches its hash. Zero matches means the comment is gone or edited; two is the ambiguity §4.13.3 already forbade but could not detect.
- **New rule §4.13.11 (`P`).** A carrier may cache a `line span` for navigation, marked derived. A cached span disagreeing with the hash is a finding against **the carrier**, never against the host file.
- **New optional carrier field `Line span`**; `Anchor` amended. `enclosing named construct` stays mandatory as the stable human pointer.

**Migration for a carrier written against the 1.0.0 skeleton:** add a comment hash to every `Anchor`, and re-mark the existing `line span` as the derived `Line span` field. A carrier whose spans have drifted resolves correctly once the hashes are added; the drifted spans become carrier findings rather than silent misdirection.

### Added — the first conversion has a home (STY-65)

The profile governed "a comment change set, not a corpus at rest", which left the one change every adopting repository must make unspecified — and three readings of it differ by two orders of magnitude in cost.

- **New `Change kind` value `converted`**, alongside `added`, `modified`, `removed`.
- **New rule §4.13.12 (`M`).** A `converted` record's base is the boundary's pre-conversion state, and `Change kind` carries no editorial signal in a conversion.
- **New rule §4.13.13 (`M`).** **The question STY-65 left open is decided: a conversion does not compel removal.** A `converted` record for a comment with no information delta states the empty delta and records it as a §4.13.6 finding. The owner decides what happens next. §4.13.6's discipline — report the conflict, never silently edit either side — extends to the corpus case, and deleting comments at scale is an editorial act the profile never asked for.
- **New rule §4.13.14 (`R`).** Audit before converting: a read-only pass recording §4.13.1 gaps and §4.13.6 conflicts, editing nothing.
- **Stated plainly:** a conversion is optional. A repository that adopts the profile for future changes alone conforms.

### Changed — a carrier may cover a boundary, not only a file (STY-69)

218 per-file carriers totalled 2.9 MB against 215 KB of tracked prose documentation — the conformance apparatus outweighed the documentation it protected by more than thirteen to one, and nothing read it.

- **Amended core §0.2.** The `hosted-comment-set` surface now covers one change set in one host file **or** one **declaration boundary** — a repository, package, or directory tree — holding a corpus at rest.
- **New rule §4.13.15 (`P`).** One carrier's declarations may cover a declaration boundary rather than one host file.
- **New rule §4.13.16 (`M`).** A `change-set` carrier carries one `Comment record` per governed comment. A `corpus-at-rest` carrier may omit the records, and conformance then rests on the comment text alone — which core §0.5 already makes the test.
- **Amended slots.** `Change scope` declares the carrier shape and what it covers; `Comment record` is required for a change set and optional for a corpus at rest; `Boundaries` now bounds the carrier rather than the change set.

STY-69's counter-argument is honoured by keeping the record mandatory exactly where it does its work — a change set beside a diff — and optional only where the field report showed it produced a liability instead.

### Added — every rule states whether a machine can decide it (STY-64)

1.0.0 removed the per-rule `Machine-checkable` metadata along with the tooling. The reason was sound and the conclusion took the useful half with the useless one: a closed list of nineteen prohibited words is not something prose review catches, and every consumer now rebuilds the same checker and gets the same edge cases wrong.

- **New `D` column on every rule table**, in `core.md` and all thirteen profile files — 216 rows. Values, defined in `spec/legend.md`:
  - `L` **literal** — a match, a count, or a closed-set test settles it.
  - `S` **screened** — a match or count finds every candidate; a reader decides each one.
  - `J` **judgment** — nothing mechanical narrows the candidates.

  The three-value scale is finer than STY-64 proposed, and it earns the extra value: most phrase-list rules are `S` rather than `L`, because the lists carry exceptions the lists themselves state. Marking them `L` would tell a reader to stop looking, which is how the two false positives in the field report arose.

  `D` changes **no rule's force**. An `L` rule and a `J` rule marked `M` are equally mandatory. This is not a reclassification: no rule's `C` value changed.

- **Amended core §8.** Part 8 now states what a checker may and may not establish, and adds **obligation 6** — decide `L` rules by match or count, treat an `S` list as a finder, and spend the attention saved on the `J` rules. Three constraints keep a checker from becoming an authority: it names what it did not evaluate, no rule refers to it, and it replaces *reading for* the literal rules rather than loading them.

- **New, and outside the specification: `tools/itws_literal.py`** with `tools/fixtures/phrase-list-fixture.md` and `tools/README.md`. It screens a corpus for the `L` and `S` rules and ends every run with its own coverage statement. It carries **no copy of any rule string**: every phrase list, profile ID, disclosure value, and strength phrase is parsed out of `spec/` at run time, so it cannot drift. It points at the corpus being edited and never at `spec/` as a query surface — the failure that cost 1.0.0 its tooling. No rule refers to it; deleting `tools/` changes no obligation.

  `--self-test` fails when a phrase list stops producing a fixture finding, which catches a list added to `spec/phrases.md` without a matching fixture line.

### Added — corpus and fan-out guidance (STY-66, STY-67)

Both surfaces are **non-normative**. Neither adds a rule, a slot, or a reader assumption.

- **`AGENTS.md` gains "When the unit of work is a corpus"** (consumer session, step 6): verify each session's output rather than its report, aggregate coverage so §8 obligation 5 composes, bound the repair loop and stop when a round stops reducing findings, and state what the disclosure records when several tools contribute.
- **`skills/itws-rewrite/SKILL.md` gains four sections** — deciding the literal rules mechanically (with the four traps: a period inside a closing quote, non-prose lines and wrapped sentences, phrase-list exceptions, and matching the rule rather than the resemblance); working on a corpus; working in the `maintenance-comment` profile; and the failure modes a self-check misses. Four additions to "What you must not do".

  STY-67's proposed section 8 is applied in its **reduced** form, because STY-64 shipped in the same change: the `D` marker carries the rule list, and the skill keeps the traps, which a decidability marker does not address.

- **Moved, not cut:** the core §7.3 worked observation/interpretation split now lives in `SKILL.md` §5, and the §4.4 section-map example is compressed to one line. Both are micro-examples under the `AGENTS.md` budget policy; §7.3's rules are unchanged.

### Added — the two open `data-table` questions carry decisions (STY-79)

Both questions the spreadsheet-overlay proposal deliberately left open are now recorded as `decision-record` documents under a new `decisions/` directory, and `spec/profiles/data-table.md` states both outcomes.

- **[decisions/0001](decisions/0001-tabular-ai-disclosure-scope.md) — a tabular document declares one `AI disclosure` for the whole workbook.** No cell, row, column, or sheet carries its own, and a cell edit updates the Title-sheet note like any other edit. The question was framed around "post-approval cell edits"; that framing is rejected, because an approval is an event outside the document (core §0.5, *Text, not process*). Where several tools contributed, the note uses the ordered-contributions form `AGENTS.md` already states for a corpus.
- **[decisions/0002](decisions/0002-csv-set-sheet-identity.md) — a CSV set names its sheets in its filenames**, as `<workbook>-<sheet>.csv`, with `-title.csv` and `-glossary.csv` reserved. A `.xlsx` file and a hosted sheet store their own sheet names; a CSV set stores none, so §4.14.1–§4.14.4 had nothing to read on that carrier. A manifest file was rejected because a second artifact describing the first drifts from it, which is the failure STY-63 reports on the comment surface.

Both records carry `Status: proposed`. Neither has been accepted by a maintainer, and recording an acceptance that did not happen is barred by core §8 obligation 2.

**No rule identifier is assigned, and no rule changes.** §4.14.1 already puts the declarations on the Title sheet, and §4.14.1–§4.14.4 already require the sheets. The additions to `spec/profiles/data-table.md` state how those rules read on each carrier, which core §0.2 keeps outside conformance. STY-72's `INV-1`, `INV-2`, `INV-4`, and `INV-5` hold; `INV-3` is the load-set band recorded as a known defect above. No reader assumption changes.

### Added — the `data-table` profile has a validated pilot fixture (STY-78)

`fixtures/data-table/` holds the profile's first real unit: a fictional document-search technology inventory, carried as a CSV set so that it also exercises the [decisions/0002](decisions/0002-csv-set-sheet-identity.md) naming convention. `fixtures/data-table/CHECK.md` is the recorded consumer-session check — every applicable rule with its result, the scan-surface walk, and the missing-fact list.

**Ten findings were raised and repaired. Every one was a fixture defect; none was a profile defect.** The profile held on first contact. The finding that matters most is §4.14.5: no registry `Columns` entry declared its column's §7.3 role, in a workbook that otherwise looked finished — which is exactly the rule `spec/profiles/data-table.md` names as most often biting.

Nothing in `spec/` changed for this. The fixture is outside the load set and no rule refers to it.

### Fixed

- `spec/ontology.md` said "all 12 profiles". There are thirteen.
- **Self-application pass over every line this change adds to `spec/`** (core §8: "its own prose follows core rules where meaningful"). `spec/profiles/task.md` carried "§5.9.5 is what §5.9.6 used to enforce procedurally" — a §4.9.1 residual-history aside about a rule this same change withdraws, which passes delete-or-promote by deleting. Core §0.2 used "corpus at rest" before its admission (§2.3.1), which lives in the `maintenance-comment` vocabulary block. The epic-scoped-admission chunk opened on the problem rather than its point (§4.2.2). Nine semicolons joining independent clauses became sentences (§3.8.1), two bare "This is" openers named their referent (§3.6.2), seven over-cap sentences were split (§3.1.1, §3.1.2), and parenthetical em dashes in core §0.2 became parentheses (§3.10.3).

  Left as they are, with reasons: `·` enumerations and vocabulary-block definition entries are the file's fixture forms, and §2.4.4 governs a definition rather than §3.1. The remaining over-cap lines are pre-existing text this change only reflowed.
- `tools/itws_literal.py` compiled `pattern` lists case-insensitively, so `<[A-Z_]{3,}>` matched lowercase text and `\bTBD\b` matched "tbd". A regular expression states its own case sensitivity; only the literal lists fold case, as `spec/phrases.md` says. Found by screening the two decision records with the tool.
- `tools/itws_literal.py` applied §4.12.3 to all prose. Core §4.12.1 bounds that rule to the scan path, and the tool now screens only the title and each section's opening chunk.
- `tools/itws_literal.py` failed to end a sentence before one opening with inline code, bold, or italics, which merged two sentences into one over-cap word count.

### Known defect — the load set exceeds its band

`AGENTS.md` fixes the load set at 15,000–25,000 tokens and calls anything over 25,000 a defect to fix in the same change. After compression, three profiles are over:

| Load set | Tokens | Over |
|---|---|---|
| base + `maintenance-comment` | 26,150 | +1,150 |
| base + `task` | 25,652 | +652 |
| base + `data-table` | 25,308 | +308 |

Base is 23,247, up from 22,121. 1.0.0 shipped with about 800 tokens of headroom, and this change set adds eleven rules (§2.3.5, §2.3.6, §4.8.4, §4.13.10–§4.13.16, §5.4.6), withdraws two, adds three ITWS-original mechanisms, and adds a column across 216 rows.

Everything the budget policy names as cuttable — restated source material and micro-examples — has been cut. Closing the remaining gap means deleting a normative statement, a closed list, or an ITWS-original mechanism, which the same policy forbids. The two instructions now conflict, and resolving it is a maintainer decision rather than a drafting one.

**Recommended resolution:** drop `spec/ontology.md` (1,690 tokens) from the consumer load set, keeping it as maintainer reading. By its own front matter it adds no obligation — "every ITWS obligation is stated in `core.md`, `phrases.md`, and the profile file" — and removing it brings every profile to roughly 24,500 with headroom restored. This is not applied here: it changes the load set every other file names, and that is the maintainer's call.

---

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

- **The `itws-rewrite` skill, rewritten.** `skills/itws-rewrite/SKILL.md` returns as the Claude skill that runs a consumer session: load the seven-file rule set, pick exactly one profile, respect the voice fence, classify each passage before editing, apply the rules by ID, and discharge the core §8 self-check obligations before returning.

  The skill is **non-normative**. It restates the consumer session `AGENTS.md` already describes, in a form a skill runtime can load, and it adds no rule, no slot, and no reader assumption. A document is checked against `spec/`, never against the skill.

  The 0.10.0-draft skill drove `itws_compile.py`, `itws_comment.py`, and the generated catalog through a fixed command sequence, so none of it survives the removals below and the file is replaced rather than edited. The replacement names the two profiles that substitute their own scan path for §4.12.1 — `maintenance-comment` (§4.13.9) and `data-table` (§4.14.18) — and drops every reference to a machine `pass` result.

### Removed — breaking

- **The `itws` Python package.** Parser, model, compiler, catalog builder, linter, validator, and scaffolds.
- **Every `tools/` command.** `itws_compile.py`, `itws_validate.py`, `itws_lint.py`, `itws_retrieve.py`, `itws_document.py`, `itws_patch.py`, `itws_index.py`, `itws_annotate.py`, `itws_overlays.py`, `itws_check_all.py`, and the rest.
- **The generated navigation catalog** under `spec/generated/agent/`: `manifest.json`, `rules.jsonl`, `profiles/*.json`, `phrase-lists.json`, `glossary.json`, `examples.jsonl`.
- **The test suite** (`tests/`) and the copyable agent scripts (`examples/agent-scripts/`).
- **The machine result.** There is no `pass` / `fail`. Rules 8.2.1, 8.2.2, 8.2.3, 8.2.5, 8.6.1, 8.6.2, and 8.6.6 are withdrawn; their IDs stay reserved and are never reassigned. Part 8 is now a self-check procedure.
- **Per-rule tool metadata.** `Machine-checkable`, `Constructs`, `Navigation`, `Resources`, and `Relations` lines are gone from every rule, along with the §1.6 closed value sets and the generated precedence table. §1.4's precedence order remains and is authoritative.
- **The non-normative `assurance/` companion.** The `skills/` directory was removed with it, then restored in this same release as a rewritten, tool-free skill; see Added above.

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
- **The ITWS-original doctrines**: two-layer model, term ladder, open-but-gated vocabulary, scan path and shallow-model outcomes, evidence record, calibrated strength, caveat placement, path-agnostic prose, work-item hierarchy, definition-of-done composition, and the maintenance-comment surface. The tabular-document surface joins them in this release.

### Why

The 0.x tree cost roughly 370,000 tokens of tooling, tests, and generated artifacts to carry, and the machine check covered only the rules a standard-library linter could decide. The rules a reader most needs help with were the ones the linter could never reach. 1.0.0 spends the whole budget on the rules themselves and puts the judgment where it always was.

---

## Earlier versions

0.1.0 through 0.10.0-draft were released between 2026-07-26 and 2026-07-29 under the tool-backed architecture. 0.1.0 used the name *Research Writing Specification (RWS)*; that name and its four-type conformance model remain valid for documents citing 0.1.0.

Those releases are recoverable from git history. Their per-version detail lived in `spec/annexes/annex-g-changelog.md`, removed in 1.0.0. The pre-1.0 checkability guarantee did not promise a retained revision for a draft, and 1.0.0 makes no such promise retroactively: a document citing a 0.x draft is re-pinned to 1.0.0 before its conformance is recorded.

From 1.0.0 onward every released version is retained.

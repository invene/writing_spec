# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [Semantic Versioning](https://semver.org/).

## [1.0.0] — amended 2026-08-17

**1.0.0 is pre-release.** The amendments below land in 1.0.0 in place, with no version bump, because 1.0.0 has not been declared stable. Core §9's semantic-versioning rules start binding at that declaration. Under §9 as written, several of these changes would be **major**: §5.4.6 adds a mandatory rule, §4.13.3 tightens one, and §5.9.6 and §5.9.8 are withdrawn.

Each amendment comes from a field report filed against 1.0.0 by a real consumer session, tracked as [STY-71](https://linear.app/inveneprod/issue/STY-71) and its children.

### Amended — guidance with judgment, not a binary gate (STY-87)

ITWS is a general guideline. Agents loading it were spending a rewrite session clearing a pass/fail gate. Two posture changes, and no individual style rule is reclassified.

**What `M` means.** Every rule keeps its current `C` value. The binary statement in core §0.5 is gone. The rules are guidance a writer applies with judgment. An `M` rule is the strong default: apply it unless applying it makes the passage worse, then leave the passage and report the departure. The owner of the document has final say. `legend.md` now states this force for `M`, `R`, and `P`. The ontology Conformance delta no longer says "binary textual conformance".

A unit conforms when every applicable `M` rule was applied or a departure from it was reported. The word stays. Its gate meaning does not.

**Boundary narrowed to workflow events (review finding).** The `conforms` definition lets a reported departure change the result, and that report lives in the session's coverage statement, not in the unit. STY-81's boundary sentence ("None conditions a result on an event outside the text") forbade that. **Resolved by narrowing the boundary, not by requiring the departure inside the unit.** The boundary now bars conditioning on a workflow event: a review, an approval, or a lifecycle transition. A reported departure is the writer's account of the text, named in the session's coverage statement (§8 obligation 5). STY-81 stays closed: no rule records review, approval, or lifecycle state; none of those events changes the result; the subject-versus-passage test is unchanged. `AGENTS.md` and `README.md` restatements of the boundary follow. STY-81's CHANGELOG entry is left as the historical record of what that change closed.

**Duplicated agent-scope lead merged (review finding).** The *Owner has final say* paragraph no longer ends "An agent applying ITWS governs the text and reports. The owner judges." That statement now appears once, in the *Text, not process* block, with that block's specific prohibitions intact.

**Load-set figures updated (review finding).** `README.md` and `AGENTS.md` stated the pre-STY-87 22,000 / 22,900–26,000 range. Both now state the measured range. `SKILL.md` carried the same stale range and was updated with them.

**The departure loop (practice, not a rule).** A reported departure carries a strong encouragement — never a requirement — to file an issue against the specification repository's issue tracker, recording how, when, and why applying the rule would have worsened the passage. This sits in core §0.5 prose, `AGENTS.md`, and `skills/itws-rewrite/SKILL.md`. It carries no rule ID and no class marker. Filing is an event outside the document; §4.13.14 was withdrawn for that reason, and this change does not put the same event back in a rule table.

**The review clause leaves the AI disclosure.** The disclosure keeps its provenance note. The review half goes.

- **Amended §4.3.4 (`M`).** Any value other than `none` carries the provenance note. The scope-and-review note is gone. `C` is unchanged.
- **Amended core §0.5.** The form is `<value> — <what the tooling did>`. The `reviewed by` clause, the `not yet reviewed` line, and the example's review clause are gone.
- **Amended `data-table` Title-sheet guidance.** Several tools still list each contribution in order. The note no longer ends with human review status.
- **Amended `AGENTS.md` and `SKILL.md`.** Consumer step 5 no longer writes `not yet reviewed`. Core §8 obligation 2 still bars inventing a reviewer.

**§8 and §9.** A partial check names what it evaluated and what it did not; it does not stand in for applying the load set. Obligation 5 names coverage and reported departures; it no longer frames a self-check as a certification. §9 major still turns on a change that can make a unit that conformed under the previous edition no longer conform under this one, with "conforms" now meaning applied-with-departures-reported. Patch no longer says "no change to conformance".

**Amended §4.13.16.** A `corpus-at-rest` carrier that omits records leaves the comment text as the governed surface. The row no longer says conformance "rests on" that text as a test.

No `C` value moved. No rule ID was reused or renumbered. No version string changed.

Load-set proxy (characters ÷ 4) after this change: base 23,254. Five profiles sit over the 25,000 target: `maintenance-comment` 26,346, `task` 25,968, `data-table` 25,501, `epic` 25,202, `subtask` 25,098. Nothing was cut; the §0.5 rewrite, the departure-loop paragraph, and the workflow-event clarification are new normative prose. Cost of this review round against the prior STY-87 measurement: base +35 (23,219 → 23,254). The band is a target, not a limit.

Affects: core §0.5, §4.3.4, §8, §9; `legend.md` class definitions; `ontology.md` Conformance delta; `data-table` (Title-sheet disclosure guidance); `maintenance-comment` (§4.13.16 wording). `AGENTS.md`, `SKILL.md`, `README.md`, `tools/itws_literal.py`, and `tools/README.md` follow. Reader assumptions: unchanged.

### Changed — load-set partitions, comment hash, comment proportion, rationale-once, and conversion product (STY-90)

This section records [STY-90](https://linear.app/inveneprod/issue/STY-90). Round A is STY-91 and STY-86. Round B is STY-83, STY-84, and STY-85. The heading was renamed so it covers both rounds.

**STY-91 — the ontology partitions.**

Dropping `spec/ontology.md` from the consumer load set was considered and **rejected**. The file does two jobs the recall-compression strategy rests on, and both stay. **Recall activation:** the anchors table names each source and what ITWS borrows, and the recall policy gives a model that does not know a source a fetch escape hatch. **Recall correction:** the deltas table stops a model that knows a source well from resolving ITWS's forks from that source. The better the recall, the more that guard matters. The recall policy, the general anchors table, and the deltas table stay in the base load set.

What left the base is what only some profiles use.

The research-only anchors moved into `research-paper` and `technical-report`, repeated verbatim under a "shared with" heading. The previous heading read "`research-paper`; `technical-report` where noted" while the closing line charged both profiles for all four sources. **Resolved:** APA JARS, the NeurIPS Paper Checklist and ML Reproducibility Checklist, and Model Cards / Datasheets for Datasets are shared by both. IMRaD is `research-paper` only. The split follows the genre fork already on the page. `research-paper`'s overlay and skeleton are IMRaD — section order, and results kept apart from discussion. `technical-report`'s overlay and skeleton are not: they separate system or method, evidence, interpretation, limitations, and checkability. §5.8.1 already diverges on purpose: a research paper promises reproducibility, and a technical report widens the same ID to reproducibility, verification, or both. The three shared sources serve method, result, reproducibility, and artifact disclosure, which both profiles ask for.

Ousterhout, *A Philosophy of Software Design* (2018), moved to `maintenance-comment`. It is the comment-knowledge source that profile forks, and it serves no other.

The scan-path evidence — nine citations justifying core §4.12 — moved to `appendices/scan-path-evidence.md`, outside `spec/` and outside the load set. `ontology.md` keeps a pointer: trust your own recall of that research and your judgment of the §4.12 rules; open the appendix only when a judgment call on §4.12 genuinely turns on a citation; never block on opening it. This is context discipline. A discovered file gets pulled into context reflexively, and this one is background a reader almost never needs. The rules remain complete without it.

**STY-86 — the comment hash is reproducible.**

The recipe said to strip each line's leading continuation marker "and the whitespace around it". That does not settle interior indentation — the leading whitespace inside a docstring after the marker is gone. Two implementations of the same comment text hashed two different ways. Nothing detected it until later anchors stopped resolving. §4.13.10 and §4.13.17 are both `M` with `D = L`. A `D = L` marker tells a reader the question is mechanically settled, which is where an under-specified recipe does the most damage.

The `comment hash` vocabulary entry now points at a numbered computation. Interior indentation is part of the text. The recipe also settles a block comment whose continuation lines carry no marker, a line-comment run at differing host indents, a blank interior line, and non-ASCII content including combining characters, with no Unicode normalization form applied.

- **Amended §4.13.10 (`M`, `L`).** An anchor now resolves when exactly one comment in its **enclosing named construct**, in the named source, matches its hash. Zero and two-or-more matches are restated against that construct. The construct is already part of the anchor under §4.13.3, so this costs no new data and resolves identical comments in different functions. `C` is unchanged.
- **New §4.13.18 (`M`, `S`).** Identical normalized text inside one enclosing named construct is out of scope for anchoring. The carrier names each such comment in `Boundaries`. No comment is edited to make an anchor unique. This answers the case where §4.13.17 previously mandated something unsatisfiable: a file with two byte-identical comments could never make every anchor resolve. An occurrence ordinal was **rejected** because position-derived data is what §4.13.11 keeps out of an anchor.
- **Amended the `Comment text` record field.** It now records the normalized text the recipe produces, before UTF-8 encoding. The recorded text is the hash input, so §4.13.11's cached-span check — a span whose text does not match the hash is a finding against the carrier — has something to compare against.
- **Amended the `Boundaries` slot and the boundary-locations list** to carry the §4.13.18 residue. No new slot.

§4.13.3, §4.13.11, §4.13.16, and §4.13.17 are unchanged in their rule rows. The "Why the anchor is content-addressed" paragraph now names the construct as resolution scope and the §4.13.18 residue.

Test vectors ship at `tools/fixtures/comment-hash-vectors.jsonl`, outside the load set. `--self-test` recomputes every digest from the recipe in the profile rather than hardcoding hashes the tool cannot regenerate. The worked example — hashing a comment with interior indentation by hand — lives in `SKILL.md`, outside the load set, per the budget policy on micro-examples.

**Classes, IDs, versions.** No `C` value moved except the new §4.13.18. No rule ID was reused or renumbered. §4.13.14 stays withdrawn and reserved. No version string changed.

Load-set proxy (characters ÷ 4) after this change: base 22,883 (23,254 → 22,883; STY-91 bought 371 tokens). Three profiles sit over the 25,000 target, down from five: `maintenance-comment` 26,757, `task` 25,597, `data-table` 25,130. `epic` 24,831 and `subtask` 24,727 came back under. Remaining: `research-paper` 24,590, `technical-report` 24,299, `investigation-log` 23,852, `design-rfc` 23,741, `incident` 23,686, `procedure` 23,621, `decision-record` 23,587, `explanation` 23,468. `maintenance-comment` rose from 26,346 because the hash recipe is normative prose that cannot be cut, and it is the profile that most needed the headroom STY-91 bought. The band is a target, not a limit; the content wins; the overage is recorded.

Affects: `ontology.md` (research and Ousterhout rows removed from the base; scan-path pointer); `research-paper` and `technical-report` (research anchors); `maintenance-comment` (Ousterhout, hash recipe, §4.13.10, new §4.13.18, `Comment text`, `Boundaries`). `appendices/scan-path-evidence.md` is new and outside the load set. `AGENTS.md`, `SKILL.md`, `README.md`, `tools/itws_literal.py`, `tools/README.md`, and `tools/fixtures/comment-hash-vectors.jsonl` follow. Reader assumptions: unchanged. No baseline or genre-knowledge item is added or removed.

**STY-84 — a governed comment is bounded by the code it anchors.**

A conversion that met §4.13.1 on every added sentence still grew comment characters 61%. Sentence quality improved. The growth was sentence count. Nothing in the rule set weighed an added sentence against the cost of reading it beside the code.

**Rule row, not profile prose.** §4.13.1 and the length test fail independently: a comment can add information and still cost more than the code it sits on. Separate IDs follow the format rule. `M` is the strong default a writer departs from and reports, not a gate, so a recommended row is no longer needed to keep judgment available. `R` would recreate the skip that produced the growth. The exception a writer needs — a long comment on a subtle invariant — is applying the rule, not departing from it: length answers to that code.

- **New §4.13.19 (`M`, `J`).** A governed comment's length answers to the anchored code and the cost of reading it there. Length is earned by recording what a reader cannot recover from that code. The row names four examples of that recovery — a hazard, a measured fact, a decision and its consequence, a defect a test pins — as illustrations, not a closed set. No character or word cap.
- **Placement.** The principle sits in the same §4.13 section, in a paragraph a writer reads immediately before the §4.13.1 row, and in the §4.13.19 row itself. Document profiles are out of scope: their reader has no adjacent code. Stated there, not in the rule's test, because a profile-only row already does not apply to them.
- **Worked pair** (one comment that earned its length, one that did not) lives in `skills/itws-rewrite/SKILL.md`, outside the load set.

§4.13.1 is unchanged in wording and in `C`.

**STY-85 — one rationale per declaration boundary.**

Inside one file, one rationale appeared fourteen times at fourteen anchors. Each restatement was freshly worded for its site, so each passed §4.13.1 and no string match found the set. Redundancy is visible at the declaration boundary §4.13.15 already names.

**Rule row, not profile prose.** Same independence: every per-comment test can pass while the boundary still restates. `M` with a stated exception is the right force. Stated without the exception the row reads as "never repeat", and the first casualty is the restatement that was carrying its weight. The exception is a `may` clause inside the row, the same pattern as §4.13.4's `None` with a reason.

- **New §4.13.20 (`M`, `J`).** A rationale is recorded once inside a declaration boundary. A later dependent anchor refers to that recording by enclosing construct or module docstring, never by line number. Exception: the site where getting it wrong is fatal may state the thing rather than point. Scope is the declaration boundary, not the repository. A test pinning a specific defect keeps that defect's rationale.
- **Optional checker: not added.** Counting a distinctive phrase inside one host file was considered. The observed restatements were freshly worded, which is why a string match measured 0.4% verbatim duplication and missed the defect. The rule is `D = J`. The checker screens Markdown, not host-language comments. A screen that cannot find the reported failure is not a screen.

**STY-83 — a conversion leaves rewritten copy and nothing else.**

One conversion produced 28,602 lines of scaffolding against 20,238 lines of rewritten comments. Optional per-comment records on `corpus-at-rest` carriers took on §4.13.17 for free. Every carrier claimed the §4.13.16 omission and carried the records anyway. A pre-commit screen treated an absent hash as "ungoverned", which §4.13.16 does not say.

**Practice, not a rule row.** This content is what a converter *does*, not what the text *is*. §4.13.14 was withdrawn for putting that kind of event in a rule table. The conversion product, the teardown, the audit's output location, the ban on conformance tooling in a consuming repository, and the handoff case sit in `AGENTS.md` and `SKILL.md` §9, which a converter reads before starting. Two things always survive teardown: the declaration block, which keeps ITWS boilerplate out of source files, and the `change-set` carrier, which a repository governing its own future changes uses continuously. Neither is conversion scaffolding. Per-comment records on a `corpus-at-rest` carrier come out by default; they stay where the repository has chosen to govern its corpus with them and will maintain them under §4.13.17. The audit itself is not forbidden; two urgent production defects were found on the run that produced this ticket. Only leaving its output in the converted repository is wrong.

The one textual amendment:

- **Amended §4.13.16 (`M`, `L`).** A `corpus-at-rest` carrier that carries records incurs §4.13.17. The cost is also named on the `Comment record` slot, where the choice is made. `C` and `D` are unchanged. The permission to omit records is unchanged.

The profile's adopting paragraph now states the conversion's product: rewritten comments and a `corpus-at-rest` carrier of declarations only.

**Classes, IDs, versions (round B).** New rows: §4.13.19 `M` `J`, §4.13.20 `M` `J`. Amended: §4.13.16, `C` unchanged. §4.13.1 is untouched. No `C` value moved on an existing row. No rule ID was reused or renumbered. §4.13.14 stays withdrawn and reserved. No version string changed.

**§4.13.19 forms are illustrative (review finding).** The row named four earned forms in the colon-plus-`·` list this specification uses for closed sets. A writer would treat an unlisted legitimate comment — a non-obvious performance characteristic, a constraint an external contract imposes, the reason an obvious simpler implementation fails — as unearned length, and delete it. The test is unchanged: what a reader cannot recover from the anchored code earns length. The four forms are examples. The label is now "Examples, not a closed set", and the list uses an em dash and commas rather than the closed-set notation. §4.13.18, §4.13.16, and §4.13.20 were checked for the same hazard; none of them writes an open collection in closed-set form. §4.13.20's "enclosing construct or module docstring" names the permitted referral method, not an illustrative list of content.

**Teardown item 4 is the default, not a ban (review finding).** §4.13.16 permits per-comment records on a `corpus-at-rest` carrier at §4.13.17's cost. Teardown listed their removal unconditionally. Removal remains the default at handoff, matching the conversion product. Keep the records where the repository has chosen to govern its corpus with them and will maintain them. `AGENTS.md` and `SKILL.md` now state that case on the conversion paragraph, teardown item 4, and the skill's "must not do" list. The profile's adopting paragraph is unchanged: conversion still delivers a declarations-only carrier; keeping records is an ongoing-governance choice, not leftover scaffolding.

Load-set proxy (characters ÷ 4) after round B: base 22,883 (unchanged). `maintenance-comment` 27,059 (26,757 → 27,059; +297). Other profiles unchanged. Three profiles sit over the 25,000 target: `maintenance-comment` 27,059, `task` 25,597, `data-table` 25,130. Nothing normative was cut. Examples, the worked pair, the conversion teardown, and the handoff case were pushed to `SKILL.md` and `AGENTS.md`, outside the load set. The band is a target, not a limit; the content wins; the overage is recorded. The review-finding wording on §4.13.19 does not change these figures materially.

Affects (round B): `maintenance-comment` (new §4.13.19, new §4.13.20, amended §4.13.16, `Comment record` slot, §4.13 orientation paragraph, adopting paragraph). `AGENTS.md`, `SKILL.md`, and `README.md` follow. `tools/itws_literal.py` is unchanged. Reader assumptions: unchanged. No baseline or genre-knowledge item is added or removed.

### Amended — text is governed, process is not (STY-81, closing STY-68 and STY-70)

ITWS is agnostic of process. The §0.5 declaration block is now stated to be the **only** process artifact the specification defines. Nothing else records review state, approval state, or lifecycle position, and no rule conditions conformance on an event outside the text.

The observed failure: a session convened to fix prose ended up litigating what was approved, what could close, and whether the owner's own review counted — with the specification as its citation. An opt-in partition would have left that failure available, so the content is removed rather than reclassified.

- **New in core §0.5** — the *Text, not process* boundary, with its subject-versus-passage test. A process state that is the document's own subject stays exact content: a `decision-record`'s `Status`, an `incident`'s resolution state, an `investigation-log`'s hypothesis state, a `data-table` status column. All four are unchanged.
- **Withdrawn: §5.9.6, §5.9.8.** Acceptance procedure and closing gates. Both IDs stay reserved and are never reassigned (core §9). §5.9.8 leaves `epic`, `task`, and `subtask`; §5.9.6 leaves `task`. §5.9.5 already carries §5.9.6's textual content — a task whose acceptance would follow from its subtasks alone has written no integrated-acceptance check.
- **Amended: §5.6.2.** Strength now matches "the evidence the document carries for it". The coupling to approval status is gone; the decision semantics already live inside the `adopted` and `proposed` tier definitions, which are unchanged.
- **Amended: core §5.4 evidence record — field 6 removed.** The **open question STY-81 left to this session is decided by removal.** "Lifecycle or authority status" was the last place process state was mandatory document content outside the stamp. STY-68's reader-protection argument is answered inside the text instead: §5.6 now states that the tier carries the settled/unsettled distinction, so an unsettled item takes the `proposed` or `interpretive` tier and reads correctly from the tier alone. The record is now **five** shared fields.
- **Amended slots.** `epic` `Summary` drops "approval or alignment requested"; `epic` `Task map` and `task` `Subtask map` drop "current ownership or status"; `task` `Summary` drops "current lifecycle state". A document may state any of these where it genuinely has them; no slot requires them. *The two `map` slots are not named in STY-81's enumeration; they are removed under its definition of done, which reaches any slot requiring workflow state as document content.*
- **Amended shallow-model outcomes.** `epic` and `design-rfc` no longer put approval status on the scan path; both now carry the §5.6 strength instead.
- **Amended `design-rfc` `Summary`.** The slot asked for "the decision reviewers are asked to make" and now asks for "the decision this document asks for". The named audience was the last place a slot pointed at a review event rather than at content. An unapproved design read as settled — `design-rfc`'s sharpest hazard — is protected by the `proposed` tier.
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
- **Amended rule §4.13.9 (`M`).** The scan path of a carrier is its change-set ID **or declaration boundary**, then in host order each host anchor and its complete governed comment. The rule previously named only a comment change set, which a boundary-scoped carrier does not have.
- **Amended slots.** `Change scope` declares the carrier shape and what it covers; `Comment record` is required for a change set and optional for a corpus at rest; `Boundaries` now bounds the carrier rather than the change set.
- **Amended reader overlay.** The `maintenance-comment` reader now recognizes "one carrier" rather than "one comment change set". Reader assumption affected: the reader is no longer assumed to be looking at a diff.

STY-69's counter-argument is honoured by keeping the record mandatory exactly where it does its work — a change set beside a diff — and optional only where the field report showed it produced a liability instead.

### Added — every rule states whether a machine can decide it (STY-64)

1.0.0 removed the per-rule `Machine-checkable` metadata along with the tooling. The reason was sound and the conclusion took the useful half with the useless one: a closed list of nineteen prohibited words is not something prose review catches, and every consumer now rebuilds the same checker and gets the same edge cases wrong.

- **New `D` column on every rule table**, in `core.md` and each of the eight profile files carrying one — 216 distinct rule IDs across 227 physical rows. Five profiles carry no rule table. Values, defined in `spec/legend.md`:
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

Both profile paragraphs carry the "no rule ID" marker and name the record's `proposed` status, so a reader reaching them from the profile alone sees that nothing there has been accepted. Rejecting either record reverts its paragraph and nothing else.

**No rule identifier is assigned, and no rule changes.** §4.14.1 already puts the declarations on the Title sheet, and §4.14.1–§4.14.4 already require the sheets. The additions to `spec/profiles/data-table.md` state how those rules read on each carrier, which core §0.2 keeps outside conformance. No reader assumption changes.

**STY-72's `INV-3` is over its target.** `INV-1`, `INV-2`, `INV-4`, and `INV-5` hold. `INV-3` aims for base plus `data-table` inside the 15,000–25,000 band; it measures 25,506, and the measurement table below records that figure rather than the stale one. The profile was already 312 tokens over when this work began, and this change adds 194 more. The band is a target rather than a limit, so the overage is reported and the epic closes on it.

### Added — the `data-table` profile has a validated pilot fixture (STY-78)

`fixtures/data-table/` holds the profile's first real unit: a fictional document-search technology inventory, carried as a CSV set so that it also exercises the [decisions/0002](decisions/0002-csv-set-sheet-identity.md) naming convention. `fixtures/data-table/CHECK.md` is the recorded consumer-session check — every applicable rule with its result, the scan-surface walk, and the missing-fact list.

**Ten findings were raised and repaired. Every one was a fixture defect; none was a profile defect.** The profile held on first contact. The finding that matters most is §4.14.5: no registry `Columns` entry declared its column's §7.3 role, in a workbook that otherwise looked finished — which is exactly the rule `spec/profiles/data-table.md` names as most often biting.

Nothing in `spec/` changed for this. The fixture is outside the load set and no rule refers to it.

### Fixed

- `spec/ontology.md` said "all 12 profiles". There are thirteen.
- **Self-application pass over every line this change adds to `spec/`** (core §8: "its own prose follows core rules where meaningful"). `spec/profiles/task.md` carried "§5.9.5 is what §5.9.6 used to enforce procedurally" — a §4.9.1 residual-history aside about a rule this same change withdraws, which passes delete-or-promote by deleting. Core §0.2 used "corpus at rest" before its admission (§2.3.1), which lives in the `maintenance-comment` vocabulary block. The epic-scoped-admission chunk opened on the problem rather than its point (§4.2.2). Nine semicolons joining independent clauses became sentences (§3.8.1), two bare "This is" openers named their referent (§3.6.2), seven over-cap sentences were split (§3.1.1, §3.1.2), and parenthetical em dashes in core §0.2 became parentheses (§3.10.3).

  Left as they are, with reasons: `·` enumerations and vocabulary-block definition entries are the file's fixture forms, and §2.4.4 governs a definition rather than §3.1. The remaining over-cap lines are pre-existing text this change only reflowed.
- `tools/itws_literal.py` screened a quoted token as though the document asserted it, so `<[A-Z_]{3,}>` matched a `<workbook>` written in backticks. The tool now blanks inline code spans before screening. An earlier attempt at this compiled `pattern` lists case-sensitively instead; that contradicted `spec/phrases.md`, which states one rule for all four list kinds — matching folds case unless an entry says otherwise — and no entry says otherwise. It also silently narrowed a screened rule, so sentence-initial "No" and "Not only" stopped producing §4.12.3 and §3.10.2 candidates. Every list folds case again.
- `tools/itws_literal.py` applied §4.12.3 to all prose. Core §4.12.1 bounds that rule to the scan path, and the tool now screens every heading including the title, plus each section's opening chunk. A bounded block no longer consumes its section's opening slot, so a `[Detail — …]` block under a heading cannot hide the opening chunk behind it. The approximation over-includes — a whole opening paragraph rather than its first sentence, and no appendix detection — and the run's coverage statement now says so.
- `tools/itws_literal.py` failed to end a sentence before one opening with inline code, bold, or italics, which merged two sentences into one over-cap word count.
- `tools/fixtures/phrase-list-fixture.md` carried its §4.12.3 line mid-section, off the scan path the rule is bounded to, so the line produced nothing and `--self-test` passed only because the intro paragraph happened to carry a negation. The line now sits in a section that exercises the heading, the opening chunk, and a bounded block between them.
- `fixtures/data-table/CHECK.md` attributed judgment rules to a script. §2.6.1, §2.6.2, §3.10.1, §4.3.2, and §4.14.10 are `J`, and no script decides a `J` rule. Every coverage row now says what settled it in the `D` column's own vocabulary — decided, screened then read, or read — and the record states that no checked-in tool reads CSV, so its counts came from scripts that were not retained. The record also claimed no external artifact was referenced while recording STY-78's locator two rows later; §2.7.4 is now `not applicable` with its reason.
- Both decision records read their own ticket as the question it carries, used "below" as a cross-reference against §4.7.3, and stated selections in the past tense while carrying `Status: proposed`. 0002 also asserted that every delivery format preserves filenames, an unmarked declarative carrying verified-tier force with nothing behind it (§5.6.2); it now records the assumption as untested.
- The pilot fixture's `Infrastructure` registry entry said "nothing in this fixture has been built" while the `Build or reuse` entry defined Reuse as "exists and runs today" (§2.1.1). The entry now separates the unbuilt system from the components a Reuse row names.

### Amended — the review of the STY-71 change set (STY-71 follow-up)

The STY-71 change set was reviewed after it merged. Every finding below comes from that review, and each is a defect in the amendments themselves rather than a new field report.

**A gap where a mandatory obligation was missing.**

- **New rule §4.13.17 (`M`).** Every anchor in a carrier resolves. §4.13.10 defined when an anchor *resolves* but no rule required one *to*, so two identical comments in one file violated no stated mandatory rule. §1.3 precedence cannot repair a gap.
- **Amended §4.13.10.** "Two matches = the ambiguity §4.13.3 forbids" no longer named a real prohibition: amended §4.13.3 constrains anchors per comment, not comments per hash, and 1.0.0's "resolving to one construct span" clause was dropped in the same change. The row now states the consequence directly and §4.13.17 carries the force.
- **Amended the `comment hash` vocabulary entry.** It named no algorithm, encoding, or normalization, so two checkers could disagree — which fails `legend.md`'s test for `D = L` on the two rules that depend on it. The entry now states SHA-256, lowercase hex, and the normalization order, including the block-comment continuation marker the old wording left ambiguous.

**Three decidability markers corrected.** A wrong `L` tells a reader to stop looking, which is the direction that costs most.

- **§4.13.8 `L` → `S`.** A match finds the marker keyword and the work-item reference; whether a clause states a *removal condition* is judgment, as §4.13.7 already recognises.
- **§2.3.3 `L` → `S`.** The rule bans using a term on a promise to define it later. `phrases.md` carries only the settled instances and its own front matter routes a near miss to the rule statement, which is `S` by definition.
- **New rule §4.3.5 (`M`, `L`).** A governed unit declares the ITWS version it is written against. §0.5 required the field with no rule row behind it, so a finding about it could only cite a section.

**§4.13.14 withdrawn, ID reserved.** It recommended a read-only audit before converting. Whether an audit happened is an event outside the document, so the row falsified core §0.5's own boundary — and STY-70's failure mode reaches `R` rows too, because an agent enforces anything carrying a class marker. The practice moves to `AGENTS.md` and `SKILL.md`, where it carries no marker.

**§5.4.6 amended.** "A path valid at the declared scope" was untestable: no §0.5 declaration carries a scope. A path is now a locator only where the unit names the repository it is relative to.

**§2.3.5, §2.3.6, and §4.8.4 move from core into `epic`, `task`, and `subtask`**, under a shared heading, with wording identical in all three. `AGENTS.md`'s placement table and budget arithmetic both call for it: three profile-scoped rules in core charged all thirteen load sets. The worked example moves to `SKILL.md` §5, as the §7.3 example did.

- **§2.3.6 amended while moving.** It required the inherited-term list in "the slot carrying its parent reference", but `subtask`'s skeleton puts it in `Boundaries and invariants`, and citing §2.3.6 as a slot's basis does not displace it under §1.3(2). The rule now names either slot, so `task` and `subtask` are both conformant as written.

**§5.8.1 diverges between `research-paper` and `technical-report` on purpose**, and each file now says so. Without the note, `AGENTS.md`'s keep-the-wording-identical instruction read as violated. §5.8.2 is identical in both and is marked shared.

**`spec/phrases.md` §4.10.5 emoji set corrected.** `\U0001FE0F` is an unassigned codepoint; U+FE0F, the variation selector, was meant. Regional-indicator flags (U+1F1E6–U+1F1FF) fall between two of the ranges and were uncovered, so the closed set under-covered its own `L`-marked rule.

**Changelog completeness, per `AGENTS.md`.** Three amendments this change set made were not named in it, and are now: §4.13.9's wording (STY-69), the `maintenance-comment` reader-overlay row, and the `design-rfc` `Summary` slot. The `D`-column entry said "all thirteen profile files"; five profiles carry no rule table, and the 216 count is of distinct rule IDs across 227 physical rows.

**STY-81 residuals.** `task` and `subtask` shallow-model outcomes still promised "integrated-acceptance **status**" and "evidence **status**", the same word the amendment removed from `epic` and `design-rfc`; both now name the condition and the evidence instead. `epic` `Summary` said "current state", which invited the removed lifecycle reading, and now says whose state and bars the epic's own.

**Voice.** Four bare "It" openers in core §0.5 and §8 name their referent (§3.6.2).

Reader assumptions: one changes. The `maintenance-comment` reader is no longer assumed to be reading a diff.

### Fixed — the checker, again

Eight defects found by the same review. None changes a rule; all eight made the tool's output wrong or its own claims overstated.

- **`D` markers are now parsed from `spec/` at run time.** The tool hardcoded 28 of them, so its "carries no copy / cannot drift" claim was true of phrase strings and false of decidability. A rule reclassified in the specification now changes what the tool prints with no code change. It still holds the *list* of IDs it evaluates, and a rule whose ID no longer has a row stops the run rather than screening silently against nothing.
- **A sentence beginning with a digit now splits.** The lookahead admitted no `0-9`, so "…over the cap. 12 sentences ran long" counted as one sentence and every §3.1 result on that paragraph was wrong.
- **`"certainly!"` can match.** `\b` after `!` demanded a following word character, so the entry could never fire. The boundary is now anchored only where a word edge exists.
- **`--self-test` checks every entry, not every rule.** Its guarantee was per rule ID, which is exactly how the broken entry above stayed invisible while §2.6.11 kept passing. Each entry is now asked to match its own source string. `tools/README.md` overstated the old guarantee and now states this one.
- **`check_section_length` tracks fences.** A `##` inside a fenced example reset section attribution, and fenced and tabular words counted against §4.8.2–§4.8.3.
- **An indented continuation line is prose again.** Four-space indentation opens a code block only after a blank line; indented after prose it is a wrapped line, and every check silently skipped it.
- **§7.3.3 matches the inflections §5.6 permits.** "The record showed" and "we proposed" are the same phrases at the same tiers, and only the citation forms matched. The non-strength reading of "we find" stays a match, because §7.3.3 is `L` on the phrase itself.
- **A missing version declaration cites §4.3.5**, a rule row, rather than §0.5, a section.

### Measured — the load set against its target band

`AGENTS.md` aims the load set at 15,000–25,000 tokens and asks that any overage be measured and reported in the same change. After compression, 3 profiles are over:

| Load set | Tokens | Over |
|---|---|---|
| base + `maintenance-comment` | 26,070 | +1,070 |
| base + `task` | 25,691 | +691 |
| base + `data-table` | 25,233 | +233 |

Base is 22,977, up from 22,121. 1.0.0 shipped with about 800 tokens of headroom, and this change set adds twelve rules (§2.3.5, §2.3.6, §4.3.5, §4.8.4, §4.13.10–§4.13.17, §5.4.6), withdraws three, adds three ITWS-original mechanisms, and adds a column across 216 rule IDs.

Two rounds of compression have run against it. Moving §2.3.5, §2.3.6, and §4.8.4 out of core took roughly 270 tokens off ten of the thirteen load sets and put them back into the three that actually use them; `epic` and `subtask` land back under the target and `task` does not. Everything else the budget policy names as cuttable — restated source material and micro-examples — is already cut. Closing the remaining gap means deleting a normative statement, a closed list, or an ITWS-original mechanism, which the policy puts ahead of the target. So the compression stops here and the three figures stand as measured.

**This is a measurement, not a blocker.** The band is a target: nothing here fails conformance, and no change was held back for it. STY-72 closes with `INV-3` over target, recorded.

**One option remains open, for whenever it is wanted:** drop `spec/ontology.md` (1,681 tokens) from the consumer load set, keeping it as maintainer reading. By its own front matter it adds no obligation — "every ITWS obligation is stated in `core.md`, `phrases.md`, and the profile file" — and removing it brings every profile under 24,500 with headroom restored. This is not applied here: it changes the load set every other file names, and that is the maintainer's call.


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

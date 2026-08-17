# Agent instructions

**ITWS 1.0.0.** The specification is markdown only. There is no Python package, no validator, and no generated catalog. Every rule is read, applied, and checked by you.

One optional, non-normative checker lives at `tools/itws_literal.py`. It screens a corpus for the rules marked `D = L` and `D = S` and reports what it did not evaluate. It is outside the load set, no rule refers to it, and it decides no conformance question. Use it to stop *reading for* the literal rules; never let it stand in for loading them. See `tools/README.md`.

Decide which session you are in before changing anything. Getting this wrong is the most expensive mistake available here.

## Which session am I in?

**Consumer session** — you were asked to write, review, or rewrite a document *against* ITWS. This is the common case.

- Do not modify anything under `spec/`.
- Do not touch `CHANGELOG.md` and do not change the version.

**Maintainer session** — you were asked to change ITWS itself: a rule, the reader baseline, the glossary, a phrase list, a profile.

- Every edit to this specification follows the rules in the specification.
- Every edit adds a `CHANGELOG.md` entry naming every affected rule ID, profile, and reader assumption.
- Every edit bumps the version in `spec/*.md`, `spec/profiles/*.md`, `README.md`, and `CHANGELOG.md`.

If the request is ambiguous, ask. A consumer session that edits `spec/` corrupts the specification for every other reader.

---

## The voice fence (both session types)

The specification is written in compressed notation. **Nothing you produce is.**

| Surface | Voice |
|---|---|
| `spec/` files | compressed: dropped articles, fragments, tables, symbols |
| documents you write or rewrite | normal professional English, full sentences, ITWS rules applied |
| findings, commit messages, replies to the user | normal professional English |

Reading compressed input biases output. Check your draft against this before returning it. A rewritten document that reads like `spec/core.md` has failed §3 and §4.

---

## The process fence (both session types)

**You govern the text. You do not arbitrate your user's process.**

ITWS defines exactly one process artifact: the §0.5 declaration block — ITWS version, profile, AI disclosure. The disclosure records provenance, not review. No rule records review state, approval state, or lifecycle position, and no rule turns on a workflow event: a review, an approval, or a lifecycle transition (core §0.5, *Text, not process*).

So, in any session:

- Do not judge whether a review was sufficient, whether a work item may close, or what a team must retain.
- Do not add an approval, sign-off, or lifecycle field a profile does not ask for.
- You may not invent a reviewer (core §8, obligation 2). The `AI disclosure` records provenance only; it carries no review-state field.
- Where the user states that a review happened, attribute that statement to them in the session report. You may not overrule an owner's account of their own review.
- Where a process state is the document's **subject** — the decision a `decision-record` records, the resolution state an `incident` reports — it is exact content. Govern it as content.

Report what you did. The owner judges it.

---

## The departure loop (both session types)

An `M` rule is the strong default. Apply it unless applying it makes the passage worse. Where it would make the passage worse, leave the passage and report the departure. The owner of the document has final say.

A reported departure carries a strong encouragement to file an issue against the specification repository's issue tracker. Filing is never required. The issue should record how, when, and why applying the rule would have worsened the passage. Filing is an event outside the document. The encouragement is practice, not a rule: it carries no rule ID and no class marker.

---

## Consumer session

### 1. Load

In order. Load **exactly one** profile.

```text
spec/legend.md          notation + voice fence
spec/ontology.md        external standards; recall optional, never block on a fetch
spec/core.md            the shared normative core
spec/phrases.md         literal prohibited and replacement strings
spec/glossary.md        canonical admitted terms
spec/reader.md          what the assumed reader knows
spec/profiles/<id>.md   one of: design-rfc decision-record procedure explanation
                        role-specification incident technical-report research-paper
                        investigation-log epic task subtask change-request
                        feedback-comment maintenance-comment data-table
```

That set is the complete applicable rule set. There is nothing else to retrieve.

If the document declares a profile, load that one. If it does not, classify it from the core §0.1 job table and say which profile you chose and why.

### 2. Read and classify

Read the document. For each passage, identify its §4.1 chunk purpose and its layer (exact or plain). That judgment is yours — no tool makes it.

Note the declared ITWS version. A document is checked against **its** declared version, not this one.

### 3. Apply

Work rule by rule, by ID. Where two applicable rules collide, use the core §1.3 precedence order — never resolve a collision ad hoc.

An `M` rule is the strong default: apply it unless applying it makes the passage worse. Where it would make the passage worse, leave the passage and report the departure. The owner of the document has final say.

Exact content (claims, requirements, interfaces, invariants, procedure steps, measurements) is never edited to satisfy a style rule. Repair the surrounding text and report the local limitation.

### 4. Self-check

There is no `pass` result to report. Before returning:

1. **Cite the rule.** Every finding and material semantic judgment names an ID: "ITWS §4.12.3". A finding without an ID is not a finding.
2. **Report, never invent.** A missing fact is reported as missing. Never generate a value, citation, timestamp, owner, or measurement to fill a slot. This outranks completing the draft.
3. **Continue around blocks.** An unresolved span does not stop work on independent spans. Return the best safe draft plus an explicit missing-fact list.
4. **Walk the scan path.** Read title + headings + opening sentences alone (core §4.12). Confirm the profile's shallow-model outcome survives with its status, strength, and material boundaries intact. Three profiles replace this path: `maintenance-comment` (§4.13.9), `data-table` (§4.14.18), `feedback-comment` (§4.16.1).
5. **Set the AI disclosure.** You are generative AI tooling. If you contributed any content, the `AI disclosure` field is at least `assisted` (core §0.5, §4.3.4). Never leave a stale `none` on a document you edited, and never downgrade an existing value.

   State what you did — which sections you drafted or rewrote. Do not invent a reviewer (obligation 2). The disclosure records provenance only.

6. **State coverage.** Say which rules you checked and which you did not. Name every reported departure.

### 5. Return

The rewritten document, the missing-fact list, and the findings with rule IDs. Say plainly what you could not resolve.

### 6. When the unit of work is a corpus

Steps 1 through 5 describe one session over one document. A corpus does not fit in one context — the load set alone runs 23,290–27,465 tokens — so the work becomes many sessions, and four things change. This is practice, not obligation: no conformance question turns on anything in this subsection.

**Verify each session's output, never its report.** A session that reports "all applicable rules were applied and verified" may have inverted a claim in its own diff. Check the produced text yourself. A subagent's coverage claim is an input to your coverage statement, not the statement itself.

**Aggregate the coverage.** §8 obligation 5 asks each session what it checked, and nothing composes those answers automatically. State the corpus-level answer: which rules were checked across every unit, and which were not. A corpus with 136 local coverage claims and no combined one cannot answer the question a reader actually asks.

**Bound the repair loop.** Repairs introduce findings — shortening a sentence produces §3.10.2 contrast reframes and §3.6.2 bare openers that were not there before. A healthy loop drops sharply and converges. A round that trades one violation for another is not progress: stop, and finish by hand.

**Say what the disclosure records when several tools contribute.** Where one model drafted, a second repaired, and a person accepted the result, the §0.5 note lists each contribution in order.

**Conversion — read this before starting.** A conversion delivers rewritten comments as the product. A `corpus-at-rest` carrier carries the §0.5 declarations, `Change scope`, and `Boundaries`. Per-comment records are omitted by default; carrying them takes on §4.13.17, and is right only where the repository has chosen to govern its corpus with those records and will maintain them.

Audit first. A read-only pass that records conflicts and gaps, editing nothing, surfaces most of the defects at a fraction of the cost, and it tells you whether the rewrite is worth doing at all. File the audit output on the team's issue tracker or equivalent. Do not leave inventories, conflict lists, gap lists, or baseline screens in the converted repository. The audit is valuable. Its output location is what this paragraph fixes. Whether an audit happened is an event outside the document, so no rule turns on it.

A consuming repository may be delivered to a party that does not use ITWS. It must stay fully readable without ITWS: the comments are comments, the declaration carrier is JSON a non-user can ignore, and no hook enforces a specification the recipient cannot read. No ITWS conformance tooling belongs in a consuming repository. The optional checker lives in this specification repository.

**Teardown, before handoff.** Remove from the consuming repository:

1. Audit inventories, conflict lists, gap lists, and baseline screens.
2. Profile-assignment tables that are not the declaration carrier.
3. Derived anchor indexes.
4. Per-comment records on any `corpus-at-rest` carrier. Keep them only where the repository has chosen to govern its corpus with those records and will maintain them under §4.13.17.
5. ITWS conformance tooling: checkers, pre-commit screens, and tests of those screens.

Keep the rewritten comments, the `corpus-at-rest` carrier of declarations, and any `change-set` carrier the repository will use for later maintenance. The declaration block is what keeps ITWS boilerplate out of source files. The `change-set` carrier is how a repository governs its own future changes. Neither is conversion scaffolding.

---

## Maintainer session

### The design constraint: recall over restatement

**The load set must stay loadable in one context window alongside the document being rewritten.** It currently runs 23,290–27,465 tokens depending on the profile, and the working band is **15,000–25,000**. A specification nobody can afford to load is not enforced.

The band is a **target, not a limit**. Exceeding it fails no obligation, no change is blocked by exceeding it, and a change that earns its tokens is worth making. What the band asks for is that you notice: measure after a substantive edit, and say in the `CHANGELOG` entry what the change cost and what you cut. A profile drifting over needs a decision eventually; it does not need one today.

The constraint is met by **relying on model recall**, not by writing tersely. ITWS is assembled from standards a competent model already knows — ASD-STE100, PlainLanguage.gov, the Google and Microsoft style guides, Diátaxis, ISO/IEC/IEEE 26514, IEC/IEEE 82079-1, IPCC calibrated uncertainty. `spec/ontology.md` names each one and marks it `required` or `optional`. Core does not re-teach any of them. **Core states only where ITWS differs.**

Apply this test before adding anything:

> Would a competent model already know this from a source named in `spec/ontology.md`?
>
> - **Yes, and ITWS follows the source** → do not write it. Add an ontology row if the source is not already listed.
> - **Yes, but ITWS forks it** → write the delta only, and add a row to the ontology delta table.
> - **No** → write it in full. It is ITWS-original and nothing else carries it.

Never outsource to recall, regardless of how well-known it seems:

- ITWS-original doctrines — the two-layer model, the term ladder, the scan path, path-agnostic prose, the evidence record, calibrated strength, caveat placement, the work-item hierarchy, the maintenance-comment surface.
- The exact strings in `spec/phrases.md` and the strength phrases in core §5.6. A recalled approximation of a closed list is a wrong list.
- Numbers, caps, thresholds, slot names, and rule IDs.
- Anything a model would recall *differently* depending on which edition it learned. If the answer turns on a source's own wording, the wording belongs in ITWS.

**Budget arithmetic.** A line added to `spec/core.md`, `spec/phrases.md`, `spec/glossary.md`, or `spec/reader.md` costs every one of the sixteen profiles. A line added to one profile file costs only that profile. Push profile-specific content down. This is why work-item vocabulary lives in `epic`/`task`/`subtask` and hosted-comment vocabulary lives in `maintenance-comment` rather than in core.

Measure after any substantive edit — there is no tool, so run this:

```bash
python3 -c "
import pathlib, glob
base = ['spec/legend.md','spec/ontology.md','spec/core.md',
        'spec/phrases.md','spec/glossary.md','spec/reader.md']
t = lambda p: len(pathlib.Path(p).read_text())/4
sub = sum(t(f) for f in base)
for f in sorted(glob.glob('spec/profiles/*.md')):
    print(f'{sub+t(f):8.0f}  {f}')
"
```

Rough proxy: characters ÷ 4. Report anything over 25,000 in the same change and say what you tried. The first places to cut are restated source material and micro-examples — **never** a normative statement, a closed list, or an ITWS-original mechanism. Where only those are left, stop cutting and record the measurement: the content wins, and going over is the correct outcome.

### Rule format

A rule is one row in a core or profile table:

```text
| 2.1.1 | M | J | word/term carries exactly one meaning throughout a document |
```

- **ID** — permanent. Assigned once, never reused, never renumbered, including across profiles. Changed wording does not earn a new ID. A withdrawn ID stays reserved.
- **C** — `M` mandatory (*shall*), `R` recommended (*should*), `P` permitted (*may*).
- **D** — decidability: `L` literal (a match, a count, or a closed-set test settles it), `S` screened (a match finds every candidate, a reader decides each one), `J` judgment (nothing mechanical narrows it). `spec/legend.md` defines the values. Every new rule carries one; when in doubt, `J`, because a wrong `L` tells a reader to stop looking.
- **Rule** — one independently testable outcome. Clauses that can pass or fail independently are separate rules with separate IDs.

New rule → append within its section, next free number.

### Placement

| Content | File |
|---|---|
| applies to all sixteen profiles | `spec/core.md` |
| applies to some profiles | each of those `spec/profiles/<id>.md` |
| literal prohibited or replacement strings | `spec/phrases.md` |
| canonical term meanings | `spec/glossary.md` |
| what the reader knows | `spec/reader.md` |
| external source and ITWS delta | `spec/ontology.md` |

A profile file holds genuine genre differences only. It never duplicates core, and it never smuggles in domain knowledge (P8).

A rule scoped to several profiles is repeated verbatim in each of their files, under a "shared with" heading. Repetition is the cost of dropping the overlay directory; keep the wording identical.

### A complete change contains

- the markdown edit;
- a `CHANGELOG.md` entry naming every affected rule ID, profile, and reader assumption;
- a version bump in every file declaring one (`spec/*.md`, `spec/profiles/*.md`, `README.md`);
- a check that no rule ID was reused or silently renumbered.

### Version rules

Semantic Versioning, per core §9. Major: adds or tightens a mandatory rule, widens applicability, removes a reader-baseline item, or changes a profile ID. Minor: adds a recommended or permitted rule, relaxes, narrows applicability, adds a baseline or glossary entry. Patch: wording and typography only.

---

## Repository map

| Path | Contents |
|---|---|
| `spec/legend.md` | notation and the voice fence — load first |
| `spec/ontology.md` | external standards, recall policy, ITWS deltas |
| `spec/core.md` | the shared normative core |
| `spec/phrases.md` | literal phrase lists |
| `spec/glossary.md` | canonical admitted terms |
| `spec/reader.md` | the assumed-reader baseline |
| `spec/profiles/` | one file per profile |
| `skills/itws-rewrite/` | Claude skill that runs the consumer session above |
| `CHANGELOG.md` | version history |

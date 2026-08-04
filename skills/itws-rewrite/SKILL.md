---
name: itws-rewrite
description: Write, review, or rewrite a document against the Invene Technical Writing Specification (ITWS). Use when asked to make a design RFC, decision record, procedure or runbook, explanation, incident report, technical report, research paper, investigation log, epic, task, or subtask conform to ITWS; when asked to review or check a document against ITWS rules; when asked to govern the code comments a change adds, edits, or removes (the maintenance-comment profile); or when asked to bring an inventory, register, or data-sources spreadsheet under ITWS (the data-table profile).
---

# Write or rewrite a document against ITWS

ITWS 1.0.0 is a markdown-only specification. There is no validator and no generated catalog. You read the rules, you apply them, and you report what you checked. There is no machine `pass` result to hide behind.

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

There is a second fence, and it separates text from process. **You govern the text. You do not arbitrate your user's process.** ITWS defines one process artifact — the §0.5 declaration block — and nothing else in the specification records review state, approval state, or lifecycle position (core §0.5, *Text, not process*). Do not judge whether a review was sufficient, whether a work item may close, or what a team must retain. Where the user says a review happened, record their statement and attribute it to them; where a process state is the document's own subject, such as the decision a `decision-record` records, govern it as exact content.

## 4. Read and classify before you edit

Read the document first. For each passage, decide its §4.1 chunk purpose and its layer — exact or plain, under the core §1.2 two-layer model. That judgment is yours; nothing decides it for you.

Note the document's declared ITWS version. A document is checked against **its** declared version, not the newest one.

## 5. Apply the rules

Work rule by rule, by ID. Where two applicable rules collide on one passage, use the core §1.3 precedence order. Never resolve a collision ad hoc.

Exact content — claims, requirements, interfaces, invariants, procedure steps, measurements — is never edited to satisfy a style rule. Repair the surrounding text and report the local limitation instead.

The §7.3 observation/interpretation split is the rule this step gets wrong most often. One fused paragraph at three strengths:

> Connection use reached 100% at 09:14 UTC, demonstrating that the client upgrade leaked connections, and a credential refresh probably triggered the first leak.

becomes:

> We observed connection use reach the configured maximum of 800 at 09:14:22 UTC on all three affected hosts. Trace links and clock bounds are in Timeline events I-17 through I-20.
>
> The evidence indicates that connection exhaustion caused request failures: failures begin after the pool reaches 800 and stop after capacity is restored. The evidence does not establish what began the connection growth.
>
> > **[Speculation — first connection failure]** We speculate that a credential refresh began the growth, but authentication logs for that interval had expired.

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

## 8. Decide the literal rules mechanically, not by reading

Every rule carries a `D` marker beside its class (`spec/legend.md`):

- `L` — a string match, a count, or a closed-set test settles it.
- `S` — a match finds every candidate; you decide each one.
- `J` — nothing mechanical narrows it. This is where your attention belongs.

Reading for an `L` rule is unreliable, not merely wasteful. A closed list of nineteen prohibited words is not something prose review catches, and a writer who has just spent attention on meaning is the least likely reader to notice one. Check the `L` and `S` rules with a script, a grep, or a pass done deliberately as a separate step. The optional checker at `tools/itws_literal.py` covers most of them and reports what it did not evaluate; it decides no conformance question.

Four traps, all of which have produced wrong results in practice:

- **A period inside a closing quote still ends a sentence.** `…sort it out." That copy is…` is two sentences.
- **A Markdown heading, a table row, an indented example, and a code block are not prose.** Counting them as sentences inflates every length check. A sentence also wraps across source lines, so count over the paragraph, not the line.
- **The phrase lists carry exceptions, and the exceptions matter.** `underscore` is permitted for a physical mark, `landscape` for physical terrain, and `significant` and `robust` in the statistical sense once §5.7 admits them. `rather than` is a comparative, not the §3.9.1 hedge `rather`. This is what the `S` marker means.
- **Match what a rule states, not what it resembles.** A phrase close to a listed one is judged under the rule's statement (`spec/phrases.md`, front matter).

Spend the attention you save on the `J` rules: §4.13.1, §4.13.4, §4.13.6, §5.1.1, and the §4.12 scan path.

## 9. Working on a corpus rather than one document

Sections 1 through 7 describe one document. A corpus does not fit in one context — the load set alone is about 22,000 tokens — so the work becomes many sessions, and four things change.

**Verify each session's output, never its report.** A session that reports "all applicable rules were applied and verified" may have inverted a claim in its diff. Check the produced text yourself. A subagent's coverage claim is an input to your coverage statement, not the statement itself.

**Give a delegated session the whole rule set, not just its findings.** A repair prompt carrying only "this sentence is too long" reliably produces a shorter sentence that trips §3.10.2 or §3.6.2 instead.

**Expect the repair loop to converge, and watch that it does.** Repairs introduce findings. A healthy loop drops sharply — sixty, then thirteen, then two. A round that trades one violation for another is not progress; stop and finish by hand.

**Aggregate the coverage.** Obligation 6 below asks each session what it checked. Nothing composes those answers, so state the corpus-level one yourself: which rules were checked across every unit, and which were not.

Before converting a corpus, audit it first (§4.13.14). A read-only pass that records conflicts and gaps, editing nothing, surfaces most of the defects at a fraction of the cost, and it tells you whether the rewrite is worth doing.

## 10. Working in the `maintenance-comment` profile

**The anchor is the comment hash, not the line span.** §4.13.3 identifies a governed comment by its host file, its enclosing named construct, and a hash of its own text with markers stripped. An anchor resolves when exactly one comment in the source matches that hash (§4.13.10). Zero matches means the comment is gone or edited and the record needs a second reading; two means the anchor is ambiguous.

**A cached line span is derived data, and it goes stale constantly.** It moves when your own edits change a comment above it, when a repair round runs, and when a formatter reflows the file. §4.13.11 permits caching one for navigation and lets nothing rely on it. Re-derive it after your last edit, and treat a cached span whose text does not match the hash as a finding against the carrier — never against the host file.

**Know the host language's comment shape before you scan for one.** A prefix test per line is not enough:

- A block comment's continuation lines carry no marker at all. That is true of `/* */`, and of the `<!-- -->` comments a Svelte or HTML template uses. Scan with state, not with a per-line prefix.
- A Rust module header is often one unbroken run of `//!` and `///` lines with no code between, and it can carry several governed comments. Treating the whole run as one anchor collapses them.
- A shell `#!` line is not a comment.

**Check the formatter's baseline before you edit, and again after.** Whether a formatter is enforced differs per language in the same repository. Rewriting comments can break a formatter that was clean, and running one that was already failing produces a large unrelated diff.

**Verify a path before you cite it in a `Basis`.** A wrong path already present in the comment you are rewriting is a §4.13.6 finding to report, not a citation to carry forward.

**A conversion is not a licence to delete.** §4.13.13 has you record an empty information delta as a finding and leave the comment for the owner. Removing it is their call, not yours.

## Failure modes to check your own draft against

Each of these has survived a self-check that reported the document clean.

- **A dropped qualifier changes the claim.** "prod ships **intentionally** unseeded" is not "prod ships unseeded". Words like *intentionally*, *deliberately*, *only*, *never*, *at most*, and *would otherwise* are load-bearing under §5.1.1.
- **A negation inverted while being shortened.** "the failure **would otherwise** look like an outage" says the warning prevents a misreading. "the failure appears to be an outage" asserts the opposite.
- **A plausible citation that does not resolve.** Open the file before naming it. A path that looks right and does not exist is worse than `None` with a reason, which §4.13.4 expressly permits. §5.4.6 requires a locator on a first reference and expressly permits stating that none exists.
- **A count or threshold copied from prose rather than read from the source.** A stale rate limit and a stale test count are both defects the code states plainly.

## What you must not do

- Do not edit anything under `spec/`. Changing the specification itself is a maintainer session with its own rules and changelog entry; see `AGENTS.md` in the repository.
- Do not change `CHANGELOG.md` or the declared ITWS version.
- Do not invent a threshold, a measurement, a source, a locator, an owner, or an acceptance condition. Report it as missing.
- Do not weaken or widen an exact statement to make a sentence shorter. Core §3.1.4 requires a split; core §5.1.1 forbids the change.
- Do not report a document as conforming when you did not check the rules that would decide it. Report coverage instead.
- Do not edit a comment or its surrounding code merely to force agreement between them. ITWS §4.13.6, in the `maintenance-comment` profile, requires preserving the conflict, reporting it, and continuing elsewhere.
- Do not accept a delegated session's self-report as your coverage statement. Check its output.
- Do not record a line span you have not confirmed contains its comment.
- Do not name a reviewer you cannot verify. Where a person accepted work without reading it line by line, say that; §0.5 forbids recording a review that did not occur, and it does not forbid recording a qualified one.
- Do not arbitrate process. You govern the text, not whether a review sufficed or a work item may close (core §0.5, *Text, not process*).

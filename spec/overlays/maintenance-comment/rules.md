# `maintenance-comment` scoped rules

**ITWS version:** 0.8.0-draft · **Status:** normative

This file holds every rule scoped to `maintenance-comment` alone. Every shared-core rule in Parts 2–8 also applies unless its `Profiles` metadata excludes `maintenance-comment` or its construct is absent from the comment set. A comment set has no headings, figures, equations, or sections, so the rules gated on those constructs are inapplicable without an exception.

## Rules from §4.13 — maintenance comments carry durable knowledge

A governed comment exists to prevent cognitive debt: the future reader effort created when recorded knowledge is missing, stale, or misplaced (§0.6). The rules below make each governed comment earn its place, attach where it applies, and name what supports it.

#### Rule 4.13.1 — Comments state their information delta
**Class:** mandatory · **Machine-checkable:** no · **Source:** Ousterhout 2018; Google style guides (adapted)
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment · chunks: any · slots: Information delta · layers: both · context: local · rewrite: review
**Resources:** reads: comment-text · writes: comment-text
**Relations:** constrains 4.13.5; pairs-with 4.13.4

> A governed comment **shall** add information that its anchored code does not state to a reader with the declared host-language supplement.

**Rationale:** A comment that restates its code doubles the maintenance surface and adds nothing a reader can use (P5). The valuable comment records what the code cannot show: why, under what constraint, or at what risk. The record's Information delta field states what deletion would lose, so a reviewer can test the delta instead of guessing it. The judgment is semantic; a reader or agent makes it and cites this rule.

**Compliant:** `Retry uses 250 ms because the payment gateway rejects bursts faster than 4 per second (DR-12).` above a `sleep` call.
**Non-compliant:** `Increment the retry counter by one.` above `retries += 1`.

**Cross-references:** Rule 4.13.4, Rule 4.13.5, §4.13 scan outcome

Permitted comment purposes are closed:

- **`rationale`** — why the code takes this form.
- **`invariant`** — a property the anchored code must preserve.
- **`caution`** — a hazard, ordering constraint, or unsafe edit.
- **`history`** — a recorded past state that still constrains the present.
- **`reference`** — a pointer to a durable external contract or record.
- **`marker`** — a `TODO` or `FIXME` work marker.

#### Rule 4.13.2 — One purpose per comment
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Information Mapping (adapted)
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment · chunks: any · slots: Purpose · layers: both · context: local · rewrite: candidate
**Resources:** reads: comment-text, declaration-block · writes: declaration-block
**Relations:** requires 4.13.1

> A governed comment record **shall** declare exactly one purpose from the closed purpose list.

**Rationale:** The purpose typing is the §4.1 chunk discipline carried onto the hosted surface. One declared purpose tells a reviewer which obligations attach: a `rationale` owes a basis, a `temporary` marker owes a removal condition, and a `caution` owes the hazard it protects. A comment doing two jobs splits into two governed comments (P2, P7).

**Compliant:** A record declares `purpose: invariant` for `Callers must hold the ledger lock before entry.`
**Non-compliant:** A record declares `purpose: rationale, caution` for one comment, or invents the purpose `note`.

**Cross-references:** Rule 4.13.1, §4.1, Annex E §E.12

#### Rule 4.13.3 — Comments attach to one host anchor
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** comment, host-anchor
**Navigation:** target: comment · chunks: any · slots: Anchor · layers: exact · context: local · rewrite: candidate
**Resources:** reads: comment-text, host-anchor-ledger · writes: host-anchor-ledger
**Relations:** constrains 4.13.9; pairs-with 8.7.4

> A governed comment **shall** attach to exactly one host anchor that resolves to one construct span in the proposed source.

**Rationale:** A comment's meaning depends on what it describes. An unanchored comment drifts: a later edit moves the code, and the knowledge silently applies to nothing. The recorded anchor names the file, line span, and enclosing named construct, so a tool can verify the attachment and detect the drift mechanically (P6, P7).

**Compliant:** A record anchors `The queue drains before shutdown completes.` to `function drain_queue, lines 41-58` of the proposed file.
**Non-compliant:** A file-bottom comment `Watch out for shutdown ordering.` with no recorded anchor, ten screens from the shutdown code.

**Cross-references:** Rule 4.13.9, Rule 8.7.4, Annex E §E.12

#### Rule 4.13.4 — Rationale, invariants, and history carry a durable basis
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment · chunks: any · slots: Basis · layers: exact · context: document · rewrite: review
**Resources:** reads: comment-text, evidence-ledger · writes: comment-text
**Relations:** requires 4.13.1; pairs-with 5.4.1

> A governed comment whose purpose is `rationale`, `invariant`, or `history` **shall** name a durable basis or record `None` with the reason no durable basis exists.

**Rationale:** These purposes make claims about the world beyond the code: why a choice was made, what must stay true, what happened before. P6 requires such claims to carry their support. A durable basis is a code element, test, contract, work item, decision record, or incident that a future reader can still open. A chat message or a generation prompt is not durable. The tool checks presence; a reader judges durability and sufficiency.

**Compliant:** `Basis: test test_burst_rejection; decision record DR-12.`
**Non-compliant:** `Basis: discussed in standup.` for an invariant that gates a lock order.

**Cross-references:** Rule 5.4.1, Rule 8.7.2, §0.6 (comment proposal record)

#### Rule 4.13.5 — Intent is not inferred from implementation alone
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment · chunks: any · slots: any · layers: exact · context: local · rewrite: prohibited
**Resources:** reads: comment-text · writes: none
**Relations:** requires 4.13.4; pairs-with 7.3.1

> A governed comment **shall not** present an intent, purpose, or requirement claim whose only support is the current implementation's behavior.

**Rationale:** Code shows what a system does, not what it is for. A writer or agent who reads a bounds check and writes "this enforces the compliance limit" has invented a requirement. If the intent claim later disagrees with reality, maintainers preserve a fiction. What the code observably does may be stated as observation; intent needs a basis under Rule 4.13.4, or the gap is recorded as an open question (P6, §7.3).

**Compliant:** `Rejects batches above 500 rows. No recorded requirement found; limit's origin is an open question (Q-3).`
**Non-compliant:** `Rejects batches above 500 rows to satisfy the audit requirement.` with no cited requirement anywhere.

**Cross-references:** Rule 7.3.1, Rule 4.13.4, Rule 8.6.4

#### Rule 4.13.6 — Code-comment conflicts are reported, not reconciled
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment · chunks: any · slots: any · layers: exact · context: local · rewrite: prohibited
**Resources:** reads: comment-text · writes: conformance-record
**Relations:** pairs-with 8.6.3

> A writer or agent who finds a governed comment contradicting its anchored code **shall** record the conflict as a finding and **shall not** silently edit either side into agreement.

**Rationale:** When a comment and its code disagree, one of them is wrong, and only someone who knows the system can say which. An agent that "fixes" the comment to match the code may be erasing the last record of the intended behavior; one that edits code to match a stale comment is worse. The conflict is a `blocked` fact under Rule 8.6.3: report it and let an owner decide (P3, P7).

**Compliant:** "Finding: the comment says retries stop after 3 attempts; `max_retries` is 5. Conflict recorded; neither side changed."
**Non-compliant:** The rewrite updates the comment to say 5 attempts because "the code is probably right."

**Cross-references:** Rule 8.6.3, Rule 8.6.5, §7.3

#### Rule 4.13.7 — Temporary comments carry a removal condition
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** comment, removal-condition
**Navigation:** target: comment · chunks: any · slots: Lifecycle · layers: exact · context: local · rewrite: candidate
**Resources:** reads: comment-text, declaration-block · writes: declaration-block
**Relations:** constrains 4.13.8

> A governed comment with lifecycle `temporary` **shall** record an observable removal condition.

**Rationale:** A temporary comment without an exit is a permanent one. The removal condition states the observable fact that ends the comment's life, such as a shipped migration, a closed work item, or a removed flag, so a later maintainer can delete with confidence instead of archaeology (P7).

**Compliant:** `Lifecycle: temporary. Remove when migration M-77 has run in production and TASK-142 is closed.`
**Non-compliant:** `Lifecycle: temporary. Remove later.`

**Cross-references:** Rule 4.13.8, §0.6 (removal condition)

#### Rule 4.13.8 — Markers are complete
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google style guides (TODO format, adapted)
**Profiles:** maintenance-comment
**Constructs:** marker
**Navigation:** target: comment · chunks: any · slots: Comment text · layers: exact · context: local · rewrite: candidate
**Resources:** reads: comment-text · writes: comment-text
**Relations:** requires 4.13.7

> A changed `TODO` or `FIXME` marker **shall** contain the marker keyword, one durable work-item or issue reference, and a removal condition.

**Rationale:** A bare `TODO` transfers work to an unnamed future person with no route back to context. The reference makes the work traceable; the condition makes the marker deletable. The grammar is `TODO(<reference>): <removal condition>`, which a tool checks mechanically. Whether the condition is genuinely observable remains a Rule 4.13.7 reading (P6, P7).

**Compliant:** `# TODO(TASK-142): remove this shim when the v2 API returns totals directly.`
**Non-compliant:** `# TODO: clean this up.`

**Cross-references:** Rule 4.13.7, §5.9 (work-item references)

#### Rule 4.13.9 — Comment sets use the defined scan path
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Duggan and Payne 2009; original
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment-set · chunks: any · slots: any · layers: plain · context: document · rewrite: candidate
**Resources:** reads: comment-text, host-anchor-ledger · writes: none
**Relations:** overrides 4.12.1 (hosted comment-set scan path); requires 4.13.3

> The scan path of a comment change set **shall** contain the change-set ID and then, in host order, each host anchor and its complete governed comment. For a `maintenance-comment` change set, this path replaces the Rule 4.12.1 title-and-headings path.

**Rationale:** A hosted comment set has no title, headings, or opening sentences, so Rule 4.12.1's surface does not exist; this exception supplies the surface that does. A reviewer who reads only the path learns what each governed comment preserves and where it applies, which is the §8.1 scan outcome for this profile. Rule 4.12.2's truth conditions apply to this path unchanged (P4).

**Compliant:** A scan path lists `CS-2026-014`, then `function drain_queue, lines 41-58` with its invariant comment, then each remaining anchor and comment in file order.
**Non-compliant:** The scan path lists comment texts with no anchors, so a reviewer cannot say where any preserved fact applies.

**Cross-references:** Rules 4.12.1–4.12.4, Rule 8.1.4, §8.1

## Rules from §8.7 — machine-proposed comments carry a human disposition

Section 8.7 gates one construct: a governed comment whose provenance is `ai-proposed`. The gate is construct-specific evidence, like a waiver record. It does not add reviewer roles and does not replace the two-role `reviewed` tier of §8.4.

#### Rule 8.7.1 — Every machine-proposed comment has a proposal record
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** proposal-record
**Navigation:** target: conformance-record · chunks: any · slots: Provenance · layers: both · context: document · rewrite: prohibited
**Resources:** reads: proposal-record, declaration-block · writes: proposal-record
**Relations:** constrains 8.7.3; pairs-with 8.6.4

> Each governed comment with provenance `ai-proposed` **shall** carry one comment proposal record.

**Rationale:** Machine-proposed prose enters the codebase on the strength of its record, not its fluency. The record makes the proposal auditable: what produced it, what supports it, and who accepted it. Provenance is declared, never inferred; a comment whose record claims `human-authored` is taken at its word, and falsifying that word is a process failure outside tooling's reach (P7).

**Compliant:** The carrier holds one proposal record for comment C-3, the only `ai-proposed` comment in the set.
**Non-compliant:** Two comments are recorded `ai-proposed`; the carrier holds one proposal record.

**Cross-references:** Rule 8.6.4, §0.6 (comment proposal record), Annex E §E.12

#### Rule 8.7.2 — Proposal bases are durable
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** proposal-record
**Navigation:** target: conformance-record · chunks: any · slots: Provenance · layers: exact · context: document · rewrite: prohibited
**Resources:** reads: proposal-record, evidence-ledger · writes: proposal-record
**Relations:** requires 8.7.1; pairs-with 4.13.4

> A comment proposal record **shall** cite at least one durable code, test, contract, work-item, or decision reference as a basis, and the generation prompt **shall not** count as one.

**Rationale:** The prompt explains where the words came from; it does not make them true. A model told "document this function's locking rationale" will produce a confident rationale whether or not one exists. The record keeps the prompt as provenance and requires a basis a future reader can open independently. A proposal with no durable basis is a Rule 4.13.5 intent guess wearing a record (P6).

**Compliant:** `Bases: test test_lock_order; incident INC-31. Prompt provenance: recorded separately.`
**Non-compliant:** `Basis: generated from the prompt "explain why this lock is taken".`

**Cross-references:** Rule 4.13.4, Rule 4.13.5, Rule 8.7.1

#### Rule 8.7.3 — A human disposition gates pass
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** proposal-record
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: proposal-record, conformance-record · writes: conformance-record
**Relations:** requires 8.7.1; constrains 8.6.3

> A validation run **shall not** report `pass` while any governed `ai-proposed` comment lacks a recorded human disposition of `accepted` or `revised`.

**Rationale:** Rule 8.2.4 already says a clean machine run closes no human gate. This rule names the gate for machine-proposed comments: a person disposes of each proposal, and until then validation reports the open gate instead of a pass. The disposition is per construct and may come from any qualified person; the §8.4 tier roles remain separate and unchanged (P7).

**Compliant:** Every proposal record carries `disposition: accepted` with a name and date, and validation may then report `pass`.
**Non-compliant:** A proposal record reads `disposition: pending` and the run reports `pass` because lint found nothing.

**Cross-references:** Rule 8.2.4, Rule 8.6.3, §8.4

#### Rule 8.7.4 — Stale records invalidate their disposition
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** proposal-record
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: proposal-record, host-anchor-ledger · writes: conformance-record
**Relations:** requires 8.7.3; pairs-with 8.1.5

> A comment proposal record **shall** pin the proposed source, anchor, and comment hashes, and a recorded disposition **shall not** support conformance after a pinned hash ceases to match.

**Rationale:** A disposition approves one comment at one anchor in one source state. Change any of the three and the approval describes something that no longer exists. Pinned hashes turn that drift into a detected failure, exactly as Rule 8.1.5 does for scan tests and Rule 8.6.2 does for artifacts. The remedy is cheap: re-read, re-dispose, re-pin (P7).

**Compliant:** After the anchored function is rewritten, validation reports the stale anchor hash and the reviewer re-disposes the updated comment.
**Non-compliant:** The release cites a disposition recorded three revisions ago against a function that has since changed shape.

**Cross-references:** Rule 8.1.5, Rule 8.6.2, Rule 8.7.3

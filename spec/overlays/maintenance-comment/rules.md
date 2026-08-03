# `maintenance-comment` scoped rules

**ITWS version:** 0.10.0-draft · **Status:** normative

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
**Relations:** constrains 4.13.9

> A governed comment **shall** attach to exactly one host anchor that resolves to one construct span in the source its change kind names: the proposed source for an added or modified comment, and the base source for a removed one.

**Rationale:** A comment's meaning depends on what it describes. An unanchored comment drifts: a later edit moves the code, and the knowledge silently applies to nothing. The recorded anchor names the file, line span, and enclosing named construct, so a tool can verify the attachment and detect the drift mechanically (P6, P7).

A removed comment is absent from the proposed source, so an anchor into that source could never resolve. Its anchor names where the comment stood, which is what a reviewer needs to judge whether the knowledge left with it. The change kind (§E.12) selects the source, so each record resolves against exactly one.

**Compliant:** A record anchors `The queue drains before shutdown completes.` to `function drain_queue, lines 41-58` of the proposed file. A removal record anchors the deleted comment to `function drain_queue, lines 39-40` of the base file.
**Non-compliant:** A file-bottom comment `Watch out for shutdown ordering.` with no recorded anchor, ten screens from the shutdown code.

**Cross-references:** Rule 4.13.9, Annex E §E.12

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

**Cross-references:** Rule 5.4.1

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

**Cross-references:** Rule 7.3.1, Rule 4.13.4

#### Rule 4.13.6 — Code-comment conflicts are reported, not reconciled
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment · chunks: any · slots: any · layers: exact · context: local · rewrite: prohibited
**Resources:** reads: comment-text · writes: none
**Relations:** pairs-with 7.3.1

> A writer or agent who finds a governed comment contradicting its anchored code **shall** record the conflict as a finding and **shall not** silently edit either side into agreement.

**Rationale:** When a comment and its code disagree, one of them is wrong, and the available text does not decide which. An agent that "fixes" the comment to match the code may erase the last record of intended behavior; one that edits code to match a stale comment is worse. Preserve both sides, report the local conflict, and continue work on independent comments (P3, P7).

**Compliant:** "Finding: the comment says retries stop after 3 attempts; `max_retries` is 5. Conflict recorded; neither side changed."
**Non-compliant:** The rewrite updates the comment to say 5 attempts because "the code is probably right."

**Cross-references:** Rule 7.3.1, §7.3

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

> A `TODO` or `FIXME` marker the change set adds or modifies **shall** contain the marker keyword, one durable work-item or issue reference, and a removal condition.

**Rationale:** A bare `TODO` transfers work to an unnamed future person with no route back to context. The reference makes the work traceable; the condition makes the marker deletable. The grammar is `TODO(<reference>): <removal condition>`, which a tool checks mechanically. Whether the condition is genuinely observable remains a Rule 4.13.7 reading (P6, P7).

The rule reaches the markers the change set leaves behind. A removed marker is gone from the proposed source, so requiring it to be complete would make deleting a bare `TODO` a violation and leave the incomplete marker in place as the conforming option. Deleting one is the repair this rule exists to encourage.

**Compliant:** `# TODO(TASK-142): remove this shim when the v2 API returns totals directly.` Deleting `# TODO: clean this up.` also conforms; the change set records the removal.
**Non-compliant:** Adding `# TODO: clean this up.`

**Cross-references:** Rule 4.13.7, §5.9 (work-item references)

#### Rule 4.13.9 — Comment sets use the defined scan path
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Duggan and Payne 2009; original
**Profiles:** maintenance-comment
**Constructs:** comment
**Navigation:** target: comment-set · chunks: any · slots: any · layers: plain · context: document · rewrite: candidate
**Resources:** reads: comment-text, host-anchor-ledger · writes: none
**Relations:** overrides 4.12.1 (hosted comment-set scan path); requires 4.13.3

> The scan path of a comment change set **shall** contain the change-set ID and then, in host order, each host anchor and its complete governed comment. For a `maintenance-comment` change set, this path replaces the Rule 4.12.1 title-and-headings path.

**Rationale:** A hosted comment set has no title, headings, or opening sentences, so Rule 4.12.1's surface does not exist; this exception supplies the surface that does. A reader or agent who reads only the path learns what each governed comment preserves and where it applies, which is the profile's shallow-model outcome. Rule 4.12.2's truth conditions apply to this path unchanged (P4).

**Compliant:** A scan path lists `CS-2026-014`, then `function drain_queue, lines 41-58` with its invariant comment, then each remaining anchor and comment in file order.
**Non-compliant:** The scan path lists comment texts with no anchors, so a reviewer cannot say where any preserved fact applies.

**Cross-references:** Rules 4.12.1–4.12.4

# Work-item overlay module

**ITWS version:** 0.8.0-draft · **Status:** normative

**Family:** work item · **Profiles:** `epic`, `task`, `subtask`

This module holds the rules that more than one work-item profile shares. Rules scoped to one profile alone are in that profile's `rules.md`.

## Rules from §4.11 — work-item hierarchy

The three work-item profiles form a document hierarchy. An `epic` supplies strategy and shared technical invariants. A `task` supplies one independently acceptable outcome. A `subtask` verifies one named part of that outcome.

The hierarchy does not determine implementation order or release mechanics. Parent and child links establish scope, inheritance, and acceptance ownership.

#### Rule 4.11.9 — Children preserve inherited invariants
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514 / original
**Profiles:** task, subtask
**Constructs:** invariant
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: chunk-text, exact-item-ledger · writes: none
**Relations:** requires 4.11.8

> A child work item **shall not** weaken an applicable inherited technical invariant.

**Rationale:** An `epic` cannot ground its children when local acceptance silently reduces a shared constraint (P3, P6).

**Compliant:** A child cites INV-2 and verifies that every covered rejection preserves billing data.
**Non-compliant:** INV-2 covers every failed payment, but one child preserves data only for expired cards.

**Cross-references:** Rule 4.11.8, Rule 5.9.7

#### Rule 4.11.14 — Independent outcomes use task
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** task, subtask
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: chunk-text · writes: none
**Relations:** requires 4.11.11

> Work with an independently acceptable outcome **shall** use `task`, not `subtask`.

**Rationale:** Size, duration, repository count, and team count do not define the hierarchy. Acceptance independence does (P8).

**Compliant:** A separately releasable account-recovery journey uses `task`, although its implementation changes one file.
**Non-compliant:** A complete user journey remains a `subtask` because the implementation is small.

**Cross-references:** Rule 4.11.11, Rule 4.11.13

#### Rule 4.11.17 — Technical hints do not carry normative content
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC Directives Part 2 / original
**Profiles:** task, subtask
**Constructs:** any
**Navigation:** target: chunk · chunks: any · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 5.9.1

> A technical hint **shall not** contain a requirement, technical invariant, or completion condition.

**Rationale:** A reader may skip a hint. Normative content must remain in the exact acceptance contract (P3, P6).

**Compliant:** "Technical hint: the existing expired-card test fixture may supply the rejection response."
**Non-compliant:** "Technical hint: the implementation must preserve billing data for 30 days."

**Cross-references:** Rule 4.6.3, Rule 5.9.1, §7.3

## Rules from §5.9 — definition-of-done composition

A definition of done is an exact acceptance record. An `epic`, `task`, or `subtask` has one such record. The record may contain several completion conditions where the profile permits them.

An `epic` treats its strategic outcome check and each technical invariant check as completion conditions under Rule 5.9.2.

A child document can supply evidence for a parent condition. The parent retains ownership of its outcome, scope, and integrated acceptance.

#### Rule 5.9.1 — One definition of done per work item
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** epic, task, subtask
**Constructs:** section
**Navigation:** target: document · chunks: any · slots: Definition of done · layers: exact · context: document · rewrite: candidate
**Resources:** reads: heading, skeleton-order · writes: heading
**Relations:** requires 4.3.3

> Each work item **shall** contain exactly one authoritative `Definition of done` slot.

**Rationale:** Separate product, engineering, and quality definitions create competing closure authorities. One slot makes completion auditable (P2, P7).

**Compliant:** One `task` has one Definition of done containing conditions CC-1 through CC-3.
**Non-compliant:** The `task` has separate Product done, Engineering done, and Quality done sections.

**Cross-references:** Rule 4.3.3, Annex E §§E.9–E.11

#### Rule 5.9.2 — Completion conditions state the pass test
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; IEC/IEEE 82079-1
**Profiles:** epic, task, subtask
**Constructs:** requirement
**Navigation:** target: chunk · chunks: requirement · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: chunk-text, exact-item-ledger · writes: chunk-text
**Relations:** requires 5.9.1

> Each completion condition **shall** identify an observable pass condition and its verification method.

**Rationale:** A condition without an observation or method cannot support acceptance without reviewer invention (P6).

**Compliant:** "CC-1 passes when checkout retains all five billing fields after test response `expired_card`."
**Non-compliant:** "CC-1: Handle expired cards correctly."

**Cross-references:** Rule 4.1.1, Rule 5.4.1

#### Rule 5.9.8 — Every completion condition must pass
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** epic, task, subtask
**Constructs:** requirement
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: chunk-text · writes: none
**Relations:** requires 5.9.2

> A work item **shall** close only after every applicable completion condition passes.

**Rationale:** A definition of done requires all its conditions. One failed condition leaves the work item's closure contract unsatisfied (P6, P7).

**Compliant:** CC-1 and CC-2 pass. Integrated check V-6 passes. The `task` closes.
**Non-compliant:** CC-1 passes and CC-2 fails. The `task` closes because one path works.

**Cross-references:** Rule 5.9.2, Rule 5.9.5, Rule 5.9.6

# `subtask` scoped rules

**ITWS version:** 0.6.0-draft · **Status:** normative

This file holds every rule scoped to `subtask` alone. The work-item rules shared with `epic` and `task` are in [../shared/work-item.md](../shared/work-item.md). Every shared-core rule in Parts 2–8 also applies unless its `Profiles` metadata excludes `subtask`. Rules 4.2.4 and 4.4.3 exclude this profile.

## Rules from §4.11 — work-item hierarchy

#### Rule 4.11.4 — Subtask titles state the contribution
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** subtask
**Constructs:** title
**Navigation:** target: heading · chunks: any · slots: any · layers: exact · context: document · rewrite: candidate
**Resources:** reads: heading · writes: heading
**Relations:** requires 4.11.13

> A `subtask` title **shall** state the contribution it verifies.

**Rationale:** A subtask is useful only when its contribution to the parent condition is visible without opening the document (P5).

**Compliant:** "Preserve entered billing data after an expired-card response"
**Non-compliant:** "Frontend work"

**Cross-references:** Rule 4.11.13, Annex E §E.11

#### Rule 4.11.12 — Subtasks name one parent
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** subtask
**Constructs:** parent-link
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: chunk-text · writes: none
**Relations:** constrains 4.11.13

> A `subtask` **shall** identify exactly one parent `task`.

**Rationale:** A contribution with two parents has ambiguous scope, inheritance, and acceptance ownership (P6, P7).

**Compliant:** `Parent task: T-18`
**Non-compliant:** `Parent tasks: T-18, T-21`

**Cross-references:** Rule 4.11.13, Annex E §E.11

#### Rule 4.11.13 — Subtasks name one parent condition
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** subtask
**Constructs:** parent-link
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: chunk-text · writes: none
**Relations:** requires 4.11.12

> A `subtask` **shall** identify exactly one completion-condition ID from its parent `task`.

**Rationale:** The condition is the subtask's complete reason for existing. A missing or multiple mapping makes its acceptance boundary unclear (P6, P7).

**Compliant:** `Parent completion condition: T-18 CC-2`
**Non-compliant:** `Supports the task definition of done`

**Cross-references:** Rule 4.11.12, Rule 5.9.4, Annex E §E.11

## Rules from §5.9 — definition-of-done composition

#### Rule 5.9.4 — Subtask evidence verifies the parent condition
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514 / original
**Profiles:** subtask
**Constructs:** parent-link
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: review
**Resources:** reads: chunk-text, evidence-ledger · writes: chunk-text
**Relations:** requires 5.9.3

> A `subtask` DoD **shall** state how its evidence verifies the named parent completion condition.

**Rationale:** A local implementation result does not establish parent acceptance unless the evidence reaches the parent's exact condition (P3, P6).

**Compliant:** "Test V-4 verifies T-18 CC-2 by comparing all five billing fields before and after the rejection."
**Non-compliant:** "The form component tests pass."

**Cross-references:** Rule 4.11.13, Rule 5.1.2

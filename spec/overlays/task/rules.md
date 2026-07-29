# `task` scoped rules

**ITWS version:** 0.6.0-draft · **Status:** normative

This file holds every rule scoped to `task` alone. The work-item rules shared with `epic` and `subtask` are in [../shared/work-item.md](../shared/work-item.md). Every shared-core rule in Parts 2–8 also applies unless its `Profiles` metadata excludes `task`.

## Rules from §4.11 — work-item hierarchy

#### Rule 4.11.2 — User-journey task titles state the journey
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** task
**Constructs:** title, user-journey
**Navigation:** target: heading · chunks: any · slots: any · layers: exact · context: document · rewrite: candidate
**Resources:** reads: heading · writes: heading
**Relations:** requires 4.11.5

> A user-journey `task` title **shall** name its actor, trigger, and observable outcome.

**Rationale:** The title must preserve the journey's smallest useful account. A component or activity title hides the user outcome (P5, P6).

**Compliant:** "A buyer can retry checkout after replacing an expired card"
**Non-compliant:** "Fix expired cards"

**Cross-references:** Rule 4.11.5, Annex E §E.10

#### Rule 4.11.3 — Engineering-only task titles state the technical outcome
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** task
**Constructs:** title
**Navigation:** target: heading · chunks: any · slots: any · layers: exact · context: document · rewrite: candidate
**Resources:** reads: heading · writes: heading
**Relations:** requires 4.11.5

> An engineering-only `task` title **shall** state its observable technical outcome.

**Rationale:** Engineering-only work still needs an acceptance target. Activity labels such as "refactor" or "cleanup" do not supply one (P5, P6).

**Compliant:** "Checkout events preserve order during payment retries"
**Non-compliant:** "Refactor checkout events"

**Cross-references:** Rule 4.11.7, Annex E §E.10

Permitted `task` classifications are closed:

- **Outcome class:** `user-journey` or `engineering-only`.
- **Change reason:** `feature`, `defect-correction`, or `maintenance-or-enabler`.

#### Rule 4.11.5 — Tasks declare both classifications
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** task
**Constructs:** declaration
**Navigation:** target: document · chunks: any · slots: Classification · layers: exact · context: document · rewrite: review
**Resources:** reads: declaration-block · writes: declaration-block
**Relations:** constrains 4.11.6

> A `task` **shall** declare one permitted Outcome class and one permitted Change reason.

**Rationale:** The two fields separate what accepts the work from why the work exists. One overloaded type cannot represent both decisions (P2, P7).

**Compliant:** `Outcome class: user-journey` and `Change reason: defect-correction`
**Non-compliant:** `Type: bug`, with no Outcome class

**Cross-references:** Rule 4.11.6, Rule 4.11.7, Annex E §E.10

#### Rule 4.11.6 — Defect corrections identify the violated contract
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514 / original
**Profiles:** task
**Constructs:** requirement
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, evidence-ledger · writes: chunk-text
**Relations:** requires 4.11.5

> A `defect-correction` task **shall** identify its accepted behavior contract and observed deviation evidence.

**Rationale:** Unwanted behavior is not necessarily a defect. The contract distinguishes restoration from a new product requirement (P6).

**Compliant:** "Contract: Task T-18 requires saved billing fields after payment rejection. Evidence: recording R-4 shows those fields become empty."
**Non-compliant:** "Users dislike the current behavior, so this is a bug."

**Cross-references:** Rule 5.4.1, Annex E §E.10

#### Rule 4.11.7 — Engineering-only tasks identify their support
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** task
**Constructs:** invariant
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.11.5

> An engineering-only `task` **shall** identify its technical boundary and supported journey or `epic` invariant.

**Rationale:** The required link prevents engineering-only classification from becoming a way to omit product or system purpose (P5, P6).

**Compliant:** "Technical boundary: checkout event order. Supported invariant: Epic E-7 INV-3."
**Non-compliant:** "This task has no user impact, parent outcome, or inherited invariant."

**Cross-references:** Rule 4.11.3, Rule 4.11.9, Annex E §E.10

#### Rule 4.11.11 — Tasks are independently acceptable
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** task
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 4.11.14

> A `task` **shall** define an outcome accepted independently of sibling `task` documents.

**Rationale:** Independent acceptance is the tactical boundary between one task and several tasks under an `epic` (P6, P8).

**Compliant:** "A buyer can retry checkout after replacing an expired card."
**Non-compliant:** One task combines retrying checkout, exporting invoices, and changing account ownership.

**Cross-references:** Rule 4.11.10, Rule 4.11.14, Annex E §E.10

Delegated sad-path fields are the path ID, blocking condition, expected response, safe state, recovery, and owning `subtask`.

#### Rule 4.11.15 — Tasks summarize delegated sad paths
**Class:** mandatory · **Machine-checkable:** partial · **Source:** IEC/IEEE 82079-1 / original
**Profiles:** task
**Constructs:** user-journey
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.11.19

> A `task` **shall** summarize each delegated sad path with every delegated sad-path field.

**Rationale:** Delegation can move technical detail. It cannot remove user-visible behavior from the tactical acceptance contract (P3, P6).

**Compliant:** "SP-2: The bank times out. Checkout preserves billing data and offers retry. Owner: Subtask ST-4."
**Non-compliant:** "Payment failures: see ST-4."

**Cross-references:** Rule 4.11.16, Rule 5.1.2, Annex E §E.10

An aggregate sad path depends on the combined behavior of multiple completion conditions.

#### Rule 4.11.16 — Aggregate sad paths stay with the task
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** task
**Constructs:** user-journey
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: chunk-text · writes: none
**Relations:** requires 4.11.15

> An aggregate sad path **shall** remain specified and verified in its parent `task`.

**Rationale:** No one subtask can own behavior that appears only after several completion conditions interact (P6).

**Compliant:** T-18 verifies rollback after the form saves data and the payment retry fails.
**Non-compliant:** T-18 delegates the combined rollback path to the form subtask alone.

**Cross-references:** Rule 4.11.15, Rule 5.9.5

Happy-path fields are the starting condition, actor action, product response, and observable outcome.

#### Rule 4.11.18 — Happy paths state the complete journey
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514 / original
**Profiles:** task
**Constructs:** user-journey
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.11.2

> A user-journey `task` **shall** state every happy-path field.

**Rationale:** The title compresses the journey. The happy path restores the complete acceptance sequence without requiring implementation steps (P6).

**Compliant:** "The buyer has an expired card. The buyer replaces it. Checkout retries payment and confirms the order."
**Non-compliant:** "The buyer completes checkout."

**Cross-references:** Rule 4.11.2, Rule 4.11.19, Annex E §E.10

Sad-path fields are the blocking condition, expected response, safe state, and recovery.

#### Rule 4.11.19 — Sad paths state failure and recovery
**Class:** mandatory · **Machine-checkable:** partial · **Source:** IEC/IEEE 82079-1 / original
**Profiles:** task
**Constructs:** user-journey
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.11.18

> Each sad path in a user-journey `task` **shall** state every sad-path field.

**Rationale:** A failure account is incomplete when it omits the product response, preserved state, or available recovery (P6).

**Compliant:** "The retry times out. Checkout reports the timeout, preserves billing data, and offers another retry."
**Non-compliant:** "The retry can fail."

**Cross-references:** Rule 4.11.15, Rule 7.1.3, Annex E §E.10

Technical-success fields are the starting state, applied change or condition, observable technical outcome, and verification method.

#### Rule 4.11.20 — Engineering success paths state the technical outcome
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514 / original
**Profiles:** task
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.11.3

> An engineering-only `task` **shall** state every technical-success field.

**Rationale:** Engineering acceptance needs a reproducible transition and observation even when no user journey changes (P6).

**Compliant:** "With event order recorded, enable retry. Verification confirms that all retried events retain their original order."
**Non-compliant:** "Refactor the retry code and run tests."

**Cross-references:** Rule 4.11.3, Rule 4.11.7, Annex E §E.10

Technical-failure fields are the failure condition, technical effect, safe state, and recovery.

#### Rule 4.11.21 — Engineering failure paths state recovery
**Class:** mandatory · **Machine-checkable:** partial · **Source:** IEC/IEEE 82079-1 / original
**Profiles:** task
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.11.20

> Each material failure path in an engineering-only `task` **shall** state every technical-failure field.

**Rationale:** A technical outcome is incomplete when its failure leaves system state or recovery unspecified (P6).

**Compliant:** "If retry reorders an event, stop release. Keep the existing processor active and restore the recorded configuration."
**Non-compliant:** "Handle retry failures."

**Cross-references:** Rule 4.11.20, Rule 7.1.3, Annex E §E.10

## Rules from §5.9 — definition-of-done composition

#### Rule 5.9.3 — Task conditions have stable identifiers
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Profiles:** task
**Constructs:** requirement
**Navigation:** target: chunk · chunks: requirement · slots: any · layers: exact · context: document · rewrite: mechanical
**Resources:** reads: chunk-text, exact-item-ledger · writes: chunk-text, exact-item-ledger
**Relations:** requires 5.9.2

> Each completion condition in a `task` **shall** have a unique stable identifier.

**Rationale:** A stable identifier lets one `subtask` map to one condition without copying or renaming the acceptance statement (P2, P7).

**Compliant:** `CC-1`, `CC-2`, and `CC-3` identify three distinct completion conditions.
**Non-compliant:** Three unnumbered checkboxes are referenced as "the first two items" by child documents.

**Cross-references:** Rule 4.11.13, Rule 5.9.4

#### Rule 5.9.5 — Tasks verify integrated behavior
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** task
**Constructs:** requirement
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 5.9.2

> A `task` **shall** define integrated-acceptance checks for behavior that depends on multiple completion conditions.

**Rationale:** Local conditions can pass while their combined user journey or technical outcome fails (P6).

**Compliant:** After CC-1 and CC-2 pass, T-18 retries payment and verifies that saved billing data reaches the new request.
**Non-compliant:** T-18 checks each component alone and never retries payment through the complete journey.

**Cross-references:** Rule 4.11.16, Rule 5.9.6

#### Rule 5.9.6 — Closed subtasks do not close the task
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** task
**Constructs:** requirement
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: chunk-text · writes: none
**Relations:** requires 5.9.5

> A `task` **shall not** be accepted solely because its child `subtask` documents are closed.

**Rationale:** Tracker status is not evidence that the independently acceptable outcome passes its integrated checks (P6, P7).

**Compliant:** Every child is closed. The `task` closes after its happy path and aggregate sad paths pass.
**Non-compliant:** Automation closes the `task` when the final child closes, although integrated retry fails.

**Cross-references:** Rule 4.11.11, Rule 5.9.5

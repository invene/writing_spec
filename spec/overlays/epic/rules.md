# `epic` scoped rules

**ITWS version:** 0.6.0-draft · **Status:** normative

This file holds every rule scoped to `epic` alone. The work-item rules shared with `task` and `subtask` are in [../shared/work-item.md](../shared/work-item.md). Every shared-core rule in Parts 2–8 also applies unless its `Profiles` metadata excludes `epic`.

## Rules from §4.11 — work-item hierarchy

#### Rule 4.11.1 — Epic titles state the strategic outcome
**Class:** mandatory · **Machine-checkable:** partial · **Source:** PlainLanguage.gov / original
**Profiles:** epic
**Constructs:** title
**Navigation:** target: heading · chunks: any · slots: any · layers: exact · context: document · rewrite: candidate
**Resources:** reads: heading · writes: heading
**Relations:** pairs-with 4.5.1

> An `epic` title **shall** state its strategic product outcome.

**Rationale:** An outcome title lets readers distinguish a strategic change from a topic or project container (P5).

**Compliant:** "Reduce checkout abandonment after recoverable payment failures"
**Non-compliant:** "Checkout improvements"

**Cross-references:** Rule 4.5.1, Annex E §E.9

#### Rule 4.11.8 — Epic invariants have stable identifiers
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ISO/IEC/IEEE 26514 / original
**Profiles:** epic
**Constructs:** invariant
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: document · rewrite: mechanical
**Resources:** reads: chunk-text, exact-item-ledger · writes: chunk-text, exact-item-ledger
**Relations:** constrains 4.11.9

> Each technical invariant in an `epic` **shall** have a unique stable identifier.

**Rationale:** Stable identifiers let child work items inherit one exact property without copying wording that can drift (P2, P6).

**Compliant:** "INV-2: A failed payment shall not delete entered billing data."
**Non-compliant:** An unnumbered list of constraints that child tasks paraphrase independently.

**Cross-references:** Rule 2.7.3, Rule 4.11.9, Annex E §E.9

#### Rule 4.11.10 — Epics remain strategic
**Class:** mandatory · **Machine-checkable:** no · **Source:** Diátaxis / original
**Profiles:** epic
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.3.2

> An `epic` **shall not** contain acceptance detail that independently performs a child `task` or `subtask` job.

**Rationale:** The `epic` grounds work. It does not replace the tactical documents that own independently acceptable outcomes and contributions (P8).

**Compliant:** The `epic` states INV-2 and links Task T-18 for the expired-card journey.
**Non-compliant:** The `epic` embeds T-18's path steps, local test cases, and implementation contribution.

**Cross-references:** Rule 4.3.2, Rule 4.11.11, Annex E §E.9

## Rules from §5.9 — definition-of-done composition

#### Rule 5.9.7 — Epic completion verifies outcome and invariants
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514 / original
**Profiles:** epic
**Constructs:** invariant
**Navigation:** target: document · chunks: any · slots: any · layers: exact · context: collection · rewrite: review
**Resources:** reads: chunk-text, exact-item-ledger · writes: chunk-text
**Relations:** requires 4.11.8

> An `epic` DoD **shall** verify its strategic outcome and every technical invariant.

**Rationale:** Child completion does not establish the product-level outcome or preservation of the constraints that grounded those children (P6).

**Compliant:** The `epic` records its outcome measure and verification for INV-1 through INV-3 after all in-scope tasks close.
**Non-compliant:** The `epic` closes when its task list is empty, with no outcome or invariant check.

**Cross-references:** Rule 4.11.8, Rule 4.11.9, Annex E §E.9

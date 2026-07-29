# Part 4 — Paragraphs, chunks, and document structure

Part 4 is shared core. Part 4 governs everything above the sentence in every ITWS profile. A rule applies to all profiles unless `**Profiles:**` metadata narrows it.

Sections 4.1–4.5 govern chunks, ordering, profile jobs, skeletons, and headings. Sections 4.6–4.10 govern detail, navigation, density, path-agnostic prose, and formatting. Section 4.11 governs the work-item hierarchy and keeps its rules in the overlay directories (§1.5).

ASD-STE100 stops at the sentence. This part draws on Information Mapping, Diátaxis, IMRaD, and plain-language ordering guidance.

Annex E registers each profile skeleton, and the overlay `skeleton.md` file holds it. IMRaD applies only to the `research-paper` profile.

## 4.1 The chunk model: one purpose per chunk

A chunk is a paragraph-level unit with exactly one purpose (§0.6). The taxonomy adapts Information Mapping to the eleven ITWS profile jobs. Profiles need not use every type. However, every body paragraph must fit exactly one type below. A reviewer who cannot classify a paragraph has found mixed or missing purpose.

A tool may assign an identifier to a source span while it processes a document. That identifier is a processing handle for one run. It is not a chunk boundary, it is not a chunk type, and an author never writes one into a governed document. Deciding which §4.1 type a passage carries is a reader's judgment, and §1.6.1 keeps it there.

Each type states its job, a review test, and a representative example.

#### Context / prior

A context chunk supplies a fact, constraint, event, or prior that later content needs. A context chunk does not introduce a new requirement, choice, or conclusion.

Test: does the paragraph answer "what must the reader know before the next point makes sense?"

Example: "The billing service writes invoices to one regional database. The database has no cross-region replica. The single-region design predates the regional availability target."

#### Definition

A definition chunk admits a term to the ladder (§2.3) with an operational meaning built from assumed or previously admitted vocabulary.

Test: after reading the paragraph, can the reader use the term correctly in a sentence they have not seen?

Example: "A *quorum* is the smallest number of cluster members that must agree before the cluster accepts a change. This cluster has five members and requires three agreements."

#### Requirement

A requirement chunk states a condition the design, implementation, procedure, or result must satisfy. Its force is explicit and testable.

Test: could a reviewer turn the paragraph into an acceptance check without inventing a threshold or actor?

Example: "The migration **shall** keep write unavailability below 30 seconds. The migration **shall** preserve every acknowledged write."

#### Claim

A claim chunk states a conclusion or finding at a strength governed by §5.6.

Test: does the paragraph tell the reader what the work establishes? If deleted, would the document assert less?

Example: "The new index halves median query latency. Across six production-shaped workloads, median latency fell from 84 ms to 41 ms."

#### Decision

A decision chunk records one selected course of action, its status, and the scope in which it governs.

Test: after reading the paragraph, can the assumed reader state what was chosen without reconstructing it from alternatives?

Example: "We chose three synchronous replicas for invoice writes. The decision applies to new regional deployments from release 2026.08 onward."

#### Mechanism / explanation

A mechanism chunk explains how or why something works without asserting a new result, requirement, or decision.

Test: does the paragraph answer "how does this happen?" and remain true if the document's measured results change?

Example: "A write reaches all three replicas in parallel. The service returns success after two replicas persist the write, so one unavailable replica does not stop progress."

#### Procedure / instruction

A procedure chunk gives ordered actions to perform or audit. A procedure chunk contains commands or a reproducible account of actions, not their interpretation.

Test: could the assumed reader follow or repeat the actions in the stated order?

Example: "Stop the worker. Wait until the queue count reaches zero. Replace the image. Start the worker. Verify one successful health check."

#### Evidence / observation

An evidence chunk reports measurements, events, counts, or comparisons without interpreting them.

Test: could two people who disagree about the conclusion still accept every sentence as the recorded observation?

Example: "Errors began at 14:03 UTC after the configuration rollout. The rate reached 18% at 14:07 and returned below 0.1% at 14:36 after rollback."

#### Interpretation

An interpretation chunk states what evidence means, at a calibrated strength (§5.6), and is labeled when §7.3 requires.

Test: could a reasonable person accept the evidence but dispute this paragraph?

Example: "The evidence indicates that the shared configuration caused the synchronized restarts. This evidence suggests replica count was not the initiating fault."

#### Risk

A risk chunk states an uncertain condition and its consequence. Probability, impact, and evidence use the calibration required by §§5.6 and 7.3.

Test: does the paragraph answer "what could go wrong, under what condition, and with what consequence?"

Example: "A region-wide clock error could expire every lease together. In that case, writes stop until a majority of members obtain new leases."

#### Limitation / boundary

A limitation chunk bounds a claim, decision, procedure, or explanation: its scope, known failure modes, exclusions, or untested cases (§7.1).

Test: does the paragraph reduce the reach of content stated elsewhere?

Example: "The latency result covers read-only workloads below 20,000 requests per second. We did not test mixed reads and writes or region loss."

#### Rule 4.1.1 — One purpose per chunk
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Information Mapping
**Constructs:** any
**Navigation:** target: chunk · chunks: any · slots: any · layers: both · context: local · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 4.2.2; pairs-with 7.3.1

> Each chunk of a governed document **shall** serve exactly one purpose from the §4.1 taxonomy.

**Rationale:** Mixed-purpose paragraphs hide transitions between facts, requirements, choices, evidence, and interpretation (P6, P7). One purpose lets a reviewer classify the paragraph and apply the rules for that information type.

**Compliant:** An incident paragraph reports error counts. A separate interpretation paragraph assesses the cause. A third decision paragraph records the follow-up.
**Non-compliant:** "Errors rose to 18%, proving the shared configuration caused the outage, so we will add a regional override." (Evidence, interpretation, and decision share one chunk.)

**Cross-references:** §7.3 (observation and interpretation), §5.6 (claim strength), §4.10.3 (lists as unclassified chunks)

## 4.2 Main point first at every level

Main-point-first ordering applies at four levels: sentence, chunk, section, and document. The ordering combines PlainLanguage.gov's guidance, the convention of stating the bottom line first, and the pyramid principle. A main point may be a requirement, proposal, decision, instruction goal, explanatory takeaway, incident outcome, or evidential claim. The reader should not hold unexplained machinery while waiting to learn why it matters.

#### Rule 4.2.1 — Main point before qualification in a sentence
**Class:** recommended · **Machine-checkable:** no · **Source:** PlainLanguage.gov
**Constructs:** any
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 4.2.2

> A sentence **should** state its main point in the main clause before subordinate qualifications.

**Rationale:** Front-loaded qualifiers make the reader buffer conditions before knowing what they condition (P1). Caveats remain co-located under §7.2. They follow the point they qualify or use a separate sentence.

**Compliant:** "The gateway remains available during one replica failure, under the tested request load."
**Non-compliant:** "Under the tested request load, and with failures limited to one replica, the gateway remains available."

**Cross-references:** §3.2 (one reviewable assertion per sentence), §7.2 (caveat placement)

#### Rule 4.2.2 — Chunk opens with its point
**Class:** mandatory · **Machine-checkable:** partial · **Source:** PlainLanguage.gov / pyramid principle
**Constructs:** any
**Navigation:** target: chunk · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.1.1

> A chunk **shall** state its point in its first sentence. Remaining sentences **shall** support, elaborate, or bound that point.

**Rationale:** Readers scan first sentences. They must read a point-last paragraph twice: once before learning the point and once after. The rule is the paragraph-level form of the pyramid principle: answer first, reasoning after.

**Compliant:** "The queue limits concurrent writes. Each worker permits 32 writes at once, and a shared counter enforces the global limit."
**Non-compliant:** "Each worker permits 32 writes at once, and a shared counter enforces the global limit. The queue therefore limits concurrent writes."

**Cross-references:** §4.1.1, §6.5 (a closing restatement of the opening point is a hollow summary)

#### Rule 4.2.3 — Section opens with its takeaway or purpose
**Class:** mandatory · **Machine-checkable:** no · **Source:** pyramid principle
**Constructs:** section
**Navigation:** target: section · chunks: any · slots: any · layers: plain · context: section · rewrite: review
**Resources:** reads: chunk-text, heading · writes: chunk-text
**Relations:** requires 4.2.2; pairs-with 4.7.1

> A section **shall** state its takeaway or operational purpose in its opening chunk before presenting supporting material.

**Rationale:** Section openings are the second navigation layer after headings. Headings and opening chunks should give a scanning reader a correct, shallow model. They should also identify the action in an instruction section (P1, P4).

**Compliant:** A design section opens: "The gateway keeps writes available by acknowledging after two of three replicas persist them."
**Non-compliant:** A design section opens: "This section first describes the request types and message fields used by the replication protocol."

**Cross-references:** §4.5 (the heading states the same point in short form), §4.7.1

Early Annex E slots include Summary, Goal, Decision, and each profile's equivalent slot. Supporting detail includes implementation, mechanism, method, chronology, and evidence.

#### Rule 4.2.4 — Document states its main point before detail
**Class:** mandatory · **Machine-checkable:** no · **Source:** PlainLanguage.gov / IMRaD (adapted)
**Profiles:** design-rfc, decision-record, procedure, explanation, incident, technical-report, research-paper, epic, task
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: Summary · layers: plain · context: document · rewrite: review
**Resources:** reads: chunk-text, skeleton-order · writes: chunk-text
**Relations:** requires 4.4.1; pairs-with 4.4.3

> A governed document **shall** state its profile-specific main point in the earliest applicable Annex E slot. The point **shall** precede supporting detail.

**Rationale:** This rule applies main-point-first ordering at document scale. Annex E gives each listed profile an appropriate early slot. Annex E does not force every profile to have an abstract. `investigation-log` is excluded because its outcome develops entry by entry. The outcome does not exist at the document's start. `subtask` is excluded because it contributes to a parent outcome and introduces no independent main outcome. Where Rule 4.4.3 applies, the early point is the plain member of the plain/exact pair.

**Compliant:** A `design-rfc` summary opens: "The proposed design keeps invoice writes available when one region fails."
**Non-compliant:** A `design-rfc` opens with replica message formats and does not state the proposed availability outcome until its final section.

**Cross-references:** §4.4.3 (plain/exact outcome pair), §1.4 precedence item 3

Before and after at paragraph scale:

Before: "Each write is sent to three replicas. A replica records the write before acknowledging it. The gateway returns success after two acknowledgements. This protocol keeps writes available when one replica fails."

After: "The protocol keeps writes available when one replica fails. Each write goes to three replicas, and the gateway returns success after two replicas record it. §5 gives the message and retry details."

## 4.3 Profiles: one job per document

ITWS 0.6.0-draft defines eleven canonical profiles. A profile is a document job in the Diátaxis sense. The profile determines the document's purpose, applicable Annex E skeleton, and narrowed rules. Content with another job belongs in another document. Local, skippable content may use a bounded block.

Each profile states its job in the `README.md` of its overlay directory. Section 0.2 lists the canonical IDs and their purposes. Section 1.5 defines the overlay layout and the load set. The overlay registry is `spec/overlays/README.md`.

#### Rule 4.3.1 — Declare the profile
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Diátaxis (adapted)
**Constructs:** declaration
**Navigation:** target: declaration · chunks: any · slots: any · layers: exact · context: document · rewrite: prohibited
**Resources:** reads: declaration-block · writes: none
**Relations:** constrains 4.4.1

> A governed document **shall** declare exactly one canonical §0.2 profile ID in its front matter.

**Rationale:** Skeleton selection, profile-scoped rules, review, and linting key off the declared profile. An inferred or noncanonical profile makes conformance unverifiable (P7).

**Compliant:**
```text
ITWS version: 0.6.0-draft
Profile: decision-record
Conformance tier: core
```
**Non-compliant:** `type: ADR` with no canonical profile ID, or a profile inferred only from the filename.

**Cross-references:** §0.4.3 (conformance statement), §4.4.1, Annex E

Subordinate content remains within a profile when Annex E requires it or the declared job needs it.

#### Rule 4.3.2 — Stay in the profile job
**Class:** mandatory · **Machine-checkable:** no · **Source:** Diátaxis
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: review
**Resources:** reads: chunk-text, skeleton-order · writes: chunk-text
**Relations:** requires 4.3.1

> A governed document **shall not** independently perform another profile's primary job. Required subordinate content **shall** remain within the declared profile.

**Rationale:** Job mixing makes procedures become architecture essays, decision records reopen settled choices, and investigation logs present provisional hypotheses as report conclusions (P5, P7). Profile-required subordinate content is not mixing: a design RFC needs rollout planning, and an incident report needs remediation. The violation occurs when that subordinate content becomes an independent second purpose that should have its own governed document.

**Compliant:** A `procedure` gives the commands for rotating a key and uses one Detail block to explain a flag needed for a safe check.
**Non-compliant:** A `procedure` spends three sections comparing key-management architectures and selecting one. That work belongs in `design-rfc` or `decision-record`.

**Cross-references:** §4.1.1, §7.3, §4.6.1

#### Rule 4.3.3 — Annex E required sections are present
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ISO/IEC/IEEE 26514 (adapted)
**Constructs:** section
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: candidate
**Resources:** reads: heading, skeleton-order · writes: heading, skeleton-order
**Relations:** requires 4.4.1

> A governed document **shall** include each required Annex E section and structural slot for its profile. The document **shall** preserve Annex E's order.

**Rationale:** The skeleton gives each profile guarantee a stable home. Procedures hold prerequisites, incidents hold impact, and decision records hold consequences. Design RFCs hold risks, and evidence-bearing reports hold limitations. A missing required section is a missing guarantee.

**Compliant:** An `incident` contains every section Annex E marks required, including impact and evidence-backed causal analysis, in the specified order.
**Non-compliant:** An `incident` omits impact because the affected users are "already known."

**Cross-references:** §4.4, §7.1, §5.8, Annex E

## 4.4 Applying profile skeletons

Annex E states the shared slot policy and registers each profile's skeleton. A skeleton defines its required sections and slots, their order, and its permitted merges or renames. Part 4 explains how to apply those skeletons. Part 4 does not create a universal outline. IMRaD and the research sequence of abstract, method, results, and discussion belong only to `research-paper`.

The shared application pattern is dependency order. Every profile seeds its prerequisites before the detail that depends on them. Each `skeleton.md` in the overlay directory states that profile's dependency order.

Annex E also controls empty slots: a required job with no content remains present as `None` or `Not applicable` with a reason. Optional bounded blocks and appendices may be omitted. A bounded block may seed terms used only inside that block because the block remains locally complete and skippable.

#### Rule 4.4.1 — Use the declared profile skeleton
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Diátaxis / IMRaD (adapted)
**Constructs:** section
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: candidate
**Resources:** reads: heading, skeleton-order · writes: heading, skeleton-order
**Relations:** requires 4.3.1; constrains 4.3.3

> A governed document **shall** apply the Annex E skeleton associated with its declared profile.

**Rationale:** One declaration must produce one predictable structure. Substituting another profile's familiar outline silently changes the document's job and its required guarantees. IMRaD remains valuable, but only where Annex E assigns it: `research-paper`.

**Compliant:** A `research-paper` applies the IMRaD-derived `research-paper` skeleton. A `design-rfc` applies the design-review skeleton.
**Non-compliant:** A `technical-report` copies an abstract–method–results–discussion outline and omits the sections its own Annex E skeleton requires.

**Cross-references:** §4.3.1, §4.3.3, Annex E

Prerequisites for Rule 4.4.2 are facts, constraints, priors, non-assumed terms, and symbols. Dependent details are requirements, interfaces, invariants, decisions, steps, risks, claims, results, and causal analyses.

#### Rule 4.4.2 — Seed prerequisites before load-bearing detail
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** domain-term
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: review
**Resources:** reads: chunk-text, term-ledger, skeleton-order · writes: chunk-text
**Relations:** requires 2.3.1

> A document **shall** introduce each prerequisite before the first dependent load-bearing detail.

**Rationale:** Dependency order is the term ladder generalized to structure (P4). Each profile seeds different material, but none may make the reader execute a step, assess a choice, or accept a claim with missing prerequisites. A term used only in a bounded block may be admitted inside that block.

**Compliant:** A `procedure` states the required role, defines *deployment ring*, and verifies backup status before the first rollout step uses those prerequisites.
**Non-compliant:** An `incident` attributes failures to lease expiry before defining *lease* or stating that all replicas shared one clock source.

**Cross-references:** §2.3, §4.9.2, §5.2 (symbols), §4.8.1 (admission density), Annex E

Covered main outcomes are proposals, decisions, operational outcomes, strategic outcomes, tactical outcomes, and evidential claims.

#### Rule 4.4.3 — State the main outcome plainly, then exactly
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** design-rfc, decision-record, procedure, incident, technical-report, research-paper, epic, task
**Constructs:** claim
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: review
**Resources:** reads: chunk-text, exact-item-ledger · writes: chunk-text
**Relations:** requires 5.1.2; pairs-with 4.2.4

> A covered document **shall** state its main outcome early in assumed-reader vocabulary. The document **shall** restate that outcome precisely after admitting all dependencies. The document **shall** link both statements under §5.1.

**Rationale:** This rule resolves main-point-first ordering against define-before-use (§1.4). The early statement gives the reader the destination without ladder debt. The later statement supplies exact scope, thresholds, identifiers, and uncertainty. The link proves that both statements express one outcome at two resolutions. `explanation` is excluded because its primary outcome is a mental model built through the document. `investigation-log` is excluded because it has no settled outcome during entry creation. `subtask` is excluded because its parent condition already supplies the exact outcome it contributes to.

**Compliant:** A `design-rfc` summary says, "Invoice writes continue when one region fails." After admitting *quorum* and *replica*, the document gives Outcome O-1. "Writes succeed while any one of three regional replicas is unavailable when two replicas durably acknowledge each write." Outcome O-1 links to the summary.
**Non-compliant:** A `technical-report` says only "the new index is faster" in its summary and never restates that claim with workloads, comparison, measured values, and uncertainty.

**Cross-references:** §5.1, §4.2.4, §1.2

## 4.5 Headings state the point, not the topic

A heading is the shortest form of its section's takeaway or operational purpose. Topic headings such as "Design details" and "Further analysis" identify only the location. Informative headings state what matters, such as "Two replicas preserve write availability" and "Rollback restores the old token format." Required Annex E top-level names are navigational landmarks and are exempt. Lower-level headings are not exempt.

#### Rule 4.5.1 — Headings are informative
**Class:** mandatory · **Machine-checkable:** partial · **Source:** PlainLanguage.gov / Google Developer Style Guide
**Constructs:** heading
**Navigation:** target: heading · chunks: any · slots: any · layers: plain · context: section · rewrite: candidate
**Resources:** reads: heading, chunk-text · writes: heading
**Relations:** pairs-with 4.10.1

> Below required Annex E top-level sections, a heading **shall** state its section's point or operational purpose. The heading **shall not** merely name the topic.

**Rationale:** Headings plus first paragraphs are the document a scanning reader actually reads (§4.2.3). Informative headings make that document true. This file's own section headings are drafted under this rule and serve as its first compliance check.

**Compliant:** "One failed replica does not stop writes" · "Verify that the old key no longer authenticates"
**Non-compliant:** "Design details" · "Discussion of data" · "Analysis"

**Cross-references:** §4.10.1 (sentence case), §4.2.3

## 4.6 Progressive disclosure: layered detail that skips cleanly

A governed document carries detail in three layers: plain main text, bounded technical blocks, and appendix formalism. The main text serves the assumed reader end to end. Bounded blocks hold exact detail a reader may want in place. Appendices hold full formalism. The load-bearing property is skip-coherence: the main text, with every bounded block removed, still reads as a complete, correct document.

A bounded block uses a quotation. Its first line has one bold bracketed label: `[Detail — <topic>]`, `[Intuition — <topic>]` (§6.3), or `[Speculation — <topic>]` (§7.3). The block ends with the quotation. In print formats, the same three labels head a framed box.

#### Rule 4.6.1 — Exact detail beyond the plain layer goes in a bounded block or appendix
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** bounded-block
**Navigation:** target: chunk · chunks: any · slots: any · layers: exact · context: section · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 4.6.3; pairs-with 6.3.1

> Technical detail unnecessary to the assumed reader's main line **shall** appear in a bounded block or appendix. Such detail **shall not** appear in main text.

**Rationale:** This rule is the structural half of §1.2. The plain layer stays plain because the exact layer has a defined location. Section 5.1 prohibits deleting exactness to keep prose readable.

**Compliant:** After admitting *gateway*, *write*, *replica*, *log position*, *retry*, and symbols `r` and `n`: Main text: "The gateway accepts a write after enough replicas store it." Followed by: "> **[Detail — acknowledgement rule]** A write succeeds after 2 of 3 replicas persist record `r` at log position `n`. Appendix B specifies retries."
**Non-compliant:** The log positions, acknowledgement states, and retry timing occupy three sentences in the middle of the plain mechanism paragraph.

**Cross-references:** §1.4 precedence item 1, §5.1, §6.3

#### Rule 4.6.2 — Bounded blocks use the standard markup
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** bounded-block
**Navigation:** target: bounded-block · chunks: any · slots: any · layers: both · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** validates 4.6.1

> Every bounded block **shall** use standard markup with exactly one label: Detail, Intuition, or Speculation.

**Rationale:** Unlabeled blocks defeat both the reader's skip decision and §8.2's ability to check block rules mechanically (P7). The label set is closed so each block type's rules (§6.3, §7.3) attach unambiguously.

**Compliant:** "> **[Intuition — why two acknowledgements tolerate one failure]** ..."
**Non-compliant:** An indented aside beginning "As an aside, ..." with no label.

**Cross-references:** §6.3 (intuition blocks), §7.3 (speculation blocks), §8.2

#### Rule 4.6.3 — Main text passes the skip test
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** bounded-block
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.6.1

> The main text **shall** remain coherent when every bounded block is removed. The main text **shall** have no dangling references or broken argument.

**Rationale:** Skip-coherence makes the block layer honest. If removal breaks the text, the block held load-bearing content. That content belongs in main text, or the main claim needs more precision (P4). The review test is mechanical: delete all blocks and read.

**Compliant:** The §4.6.1 compliant example: with the Detail block deleted, the main sentence still describes write acknowledgement at plain resolution.
**Non-compliant:** Main text reading "we use the threshold derived below" where "below" is inside a Detail block — deleting the block orphans the reference.

**Cross-references:** §4.6.1, §4.7.3

Demonstration on a sample passage. With blocks present: "The queue limits how many writes reach the database at once. > **[Detail — queue bound]** Each worker permits 32 in-flight writes. Semaphore `S` enforces a global limit of 256. > The limit protects the database during request bursts." With blocks removed, the passage reads: "The queue limits how many writes reach the database at once. The limit protects the database during request bursts." The result is coherent, complete, and one level shallower. The test passes.

## 4.7 Transitions and navigation

Sections locate themselves. References point by number. The document never depends on unread content.

#### Rule 4.7.1 — A section opens by locating itself
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** section
**Navigation:** target: section · chunks: any · slots: any · layers: plain · context: section · rewrite: candidate
**Resources:** reads: chunk-text, heading · writes: chunk-text
**Relations:** pairs-with 4.2.3

> Within its first chunk, a section **shall** state its function and connection to preceding content.

**Rationale:** Under §4.2.3, the opening chunk carries the takeaway and the connection. Readers arriving from the table of contents can orient themselves without rereading (P4).

**Compliant:** "§6 reports the failure tests for the design in §5. §7 states which deployment risks remain."
**Non-compliant:** A section that opens directly with "Table 4 shows per-region timeout rates."

**Cross-references:** §4.2.3

#### Rule 4.7.2 — Forward pointers are few and explicit
**Class:** recommended · **Machine-checkable:** partial · **Source:** original
**Constructs:** cross-reference
**Navigation:** target: section · chunks: any · slots: any · layers: plain · context: document · rewrite: candidate
**Resources:** reads: chunk-text, cross-reference-ledger · writes: chunk-text
**Relations:** constrains 2.3.3

> A section **should** contain at most two forward pointers. Each pointer **should** name a numbered section without depending on unread content.

**Rationale:** A forward pointer is a promise. Prose that needs unread material is a forward *dependence*. Section 2.3 already prohibits such dependence for terms. Rule 4.7.2 discourages it for all other content. The provisional cap prevents signposting from replacing sound ordering.

**Compliant:** "§7.2 bounds this availability claim to single-region failures."
**Non-compliant:** "As will become clear, this choice is the reason the later anomaly appears." (An unnumbered promise the reader cannot act on.)

**Cross-references:** §2.3 (no forward references for terms), §4.2

#### Rule 4.7.3 — Cross-references cite numbers, not positions
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google Developer Style Guide
**Constructs:** cross-reference
**Navigation:** target: sentence · chunks: any · slots: any · layers: both · context: document · rewrite: mechanical
**Resources:** reads: chunk-text, cross-reference-ledger · writes: chunk-text, cross-reference-ledger
**Relations:** requires 4.7.2

> Cross-references **shall** cite a numbered section, figure, or table. They **shall not** use "above," "below," or "as previously discussed."

**Rationale:** Positional references break under reorganization and under the §4.6.3 skip test, and "as previously discussed" is unverifiable by the reader (P7). Numbered references survive both.

**Compliant:** "The rollback check is defined in §5.1."
**Non-compliant:** "Using the check described above, ..."

**Cross-references:** §4.6.3, §8.2

## 4.8 Length and density budgets

The ladder makes rigor possible. Budgets make the ladder manageable. A document may satisfy §2.3 but still admit terms faster than the reader can absorb them. Both numeric values below are provisional draft calibrations. Section 8.3 reader-test outcomes may change them under §0.8.

For Rule 4.8.1, a page is a consecutive, non-overlapping 500-word window. Any remainder forms the document's final page.

#### Rule 4.8.1 — At most three term admissions per page
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** domain-term
**Navigation:** target: document · chunks: any · slots: any · layers: both · context: document · rewrite: review
**Resources:** reads: chunk-text, term-ledger · writes: chunk-text
**Relations:** requires 2.3.1; pairs-with 4.4.2

> A governed document **shall not** admit more than three new terms or symbols per defined page.

**Rationale:** Admission is the costliest thing a document asks of the reader. Three per page is a provisional draft value based on working-memory guidance. Section 8.3 calibration may change the value. The cap forces the writer to spread the ladder or reduce scope. Persistent overshoot signals missing structure, not a need for waiver.

**Compliant:** A context section admits "replica," "quorum," and "failover" across its first page, then builds on them.
**Non-compliant:** A first page admits "replica," "quorum," "lease," "epoch," "consensus," and "linearizability"—six rungs in 500 words.

**Cross-references:** §2.3, §4.4.2, §8.3

#### Rule 4.8.2 — Sections stay under the length ceiling
**Class:** recommended · **Machine-checkable:** yes · **Source:** original
**Constructs:** section
**Navigation:** target: section · chunks: any · slots: any · layers: plain · context: section · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 4.8.3

> A section **should not** exceed 1,500 words.

**Rationale:** The provisional draft section ceiling forces useful structure. An oversized section usually contains two sections or detail for a bounded block or appendix (§4.6.1). The ceiling is recommended because some evidence and incident-timeline sections are legitimately long.

**Compliant:** A 2,100-word incident analysis split into three sections with informative headings.
**Non-compliant:** A single 2,100-word "Analysis" section with no internal structure.

**Cross-references:** §4.5.1, §4.6.1

#### Rule 4.8.3 — Subsections stay under the length ceiling
**Class:** recommended · **Machine-checkable:** yes · **Source:** original
**Constructs:** section
**Navigation:** target: section · chunks: any · slots: any · layers: plain · context: section · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.8.2

> A subsection **should not** exceed 600 words.

**Rationale:** The subsection ceiling is independently checkable from the section ceiling. A subsection above the provisional draft value usually contains two points or skippable detail that belongs in a bounded block.

**Compliant:** A 1,400-word section divided into three 350–550-word subsections.
**Non-compliant:** A 1,400-word section whose only subsection contains 1,200 words under one heading.

**Cross-references:** Rule 4.8.2, §4.5.1, §4.6.1

## 4.9 Path-agnostic prose: the no-warpath rule

Prose states current facts without relying on the decision path that produced them. Residual-history asides include "...instead of the old approach" and "...unlike what we did before." They also include "previously we tried X and it failed, so...." Such asides make the reader infer a history they do not share. Investigation logs and incident timelines legitimately record history. Those profiles identify events and prior entries instead of relying on private path-relative phrasing.

Google's timeless-documentation guidance is the nearest prior art. The guidance bans time-relative statements such as "currently" and "the new API." Section 4.9 extends that mechanism to decision-path relativity. Section 2.6 holds the lintable warpath-marker list. This section holds the structural rule.

Necessary path information receives promotion. The concept's framing chunk states it as a prior (§0.6) in path-agnostic terms. Later text can then build on it openly. The ladder discipline extends from vocabulary to context. Section 2.3 admits terms before use. Section 4.9 admits context before reliance.

Rule 4.9.1 permits a history reference only as a §4.9.2 framed prior or an identified chronological event under §4.3.

#### Rule 4.9.1 — No residual-history asides
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Google Developer Style Guide (timeless documentation, extended)
**Constructs:** prohibited-phrase
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 4.9.2; pairs-with 2.6.6

> Prose **shall not** refer to superseded approaches, prior drafts, or abandoned states outside the permitted contexts.

**Rationale:** Decision-path residue is context debt: it references state only the authors hold (P5). A reader with zero project history should never wonder "which old approach?" An `incident` event or `investigation-log` entry citing an earlier event by identifier is a record, not residue.

**Compliant:** "The loader validates each record before writing it."
**Non-compliant:** "The loader validates before writing—unlike our earlier setup—which avoids the corruption problem we used to have."

**Cross-references:** §2.6 (warpath-marker phrase list), §4.3 (`incident`, `investigation-log`), §8.2

#### Rule 4.9.2 — Necessary path information is promoted to a framed prior
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** any
**Navigation:** target: chunk · chunks: context · slots: any · layers: both · context: section · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.9.1

> Necessary path information **shall** appear as a prior in the concept's framing chunk. The prior **shall** use path-agnostic terms.

**Rationale:** Some history is real content. A constraint discovered through failure remains a constraint. Promotion moves that information from an aside to admitted context. Later text may rely on it because the reader receives it first (P4).

**Compliant:** "Writing before validation can store malformed records. The loader therefore validates each record first." (The discovered constraint is framed as fact.)
**Non-compliant:** "...we now validate records, which fixes the issue we had with the old loader." (The constraint arrives as residue, after reliance.)

**Cross-references:** §4.1 (context, definition, and mechanism chunks), §2.3

A clause deletes cleanly when its removal leaves the sentence intact.

#### Rule 4.9.3 — Every path reference passes delete-or-promote
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** any
**Navigation:** target: sentence · chunks: any · slots: any · layers: both · context: section · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.9.1; requires 4.9.2

> A clause about a superseded state or abandoned approach **shall** pass delete-or-promote. The clause **shall** delete cleanly or receive §4.9.2 promotion.

**Rationale:** This rule gives reviewers the operative §4.9 test. Read the clause, delete it, and inspect the result. An intact sentence identifies residue. A broken sentence identifies load-bearing information that belongs upstream as a prior. There is no third option (P7).

**Compliant:** Delete residue: "We validate each record ~~, unlike the previous loader~~." → "We validate each record." Promote load-bearing context as in the §4.9.2 compliant example.
**Non-compliant:** Keeping the clause because "reviewers might remember the old pipeline."

**Cross-references:** §4.9.1, §4.9.2

## 4.10 Formatting rules: signs of machine-generated text

These rules convert formatting-level patterns from Wikipedia's "Signs of AI writing" catalog into prohibitions. They bind regardless of who or what drafted the text: each pattern substitutes formatting for structure. Markdown-authored RFCs, reports, procedures, and logs are where these habits often accumulate unnoticed.

#### Rule 4.10.1 — Headings use sentence case
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing" / Google Developer Style Guide
**Constructs:** heading
**Navigation:** target: heading · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: heading · writes: heading
**Relations:** validates 4.5.1

> Headings **shall** use sentence case.

**Rationale:** Sentence case is this specification's single heading style (P2 applied to formatting). Title case is also the source catalog's strongest formatting-level machine-generation sign. The rule extends §4.5.1. An informative heading uses sentence casing.

**Compliant:** "## One failed replica does not stop writes"
**Non-compliant:** "## One Failed Replica Does Not Stop Writes"

**Cross-references:** §4.5.1, §8.2

#### Rule 4.10.2 — Boldface is earned and rare
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** any
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 2.3.1

> Body boldface **shall** appear only in term admissions (§2.3) and template-required labels. Body boldface **shall not** emphasize selected running words or phrases.

**Rationale:** Mechanical key-takeaway bolding delegates emphasis to formatting instead of ordering. Under §4.2, the takeaway is already first. The bolding therefore carries no information (P5). A page with scattered bold phrases is the formatting form of a hollow summary.

**Compliant:** "A **quorum** is the smallest number of members that must agree..." (admission), then plain prose throughout.
**Non-compliant:** "Replication **prevents outages**, has **minimal overhead**, and is the **recommended default**."

**Cross-references:** §2.3, §4.2.2

#### Rule 4.10.3 — No inline-header lists in place of prose
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** list
**Navigation:** target: list · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.1.1

> Prose content **shall** use prose form. A vertical "**Term**: description" list **shall not** substitute for prose.

**Rationale:** A bolded-fragment list is usually an unclassified chunk (§4.1.1). The list flattens claims, mechanisms, and evidence into bullets that avoid support. Lists remain correct for enumerable items such as steps, required sections, and closed sets.

**Compliant:** "The rollback has three checks. The old image must be running, the error rate must be below 0.1%, and new writes must be visible."
**Non-compliant:** "- **Image**: old. - **Errors**: low. - **Writes**: visible."

**Cross-references:** §4.1.1, §4.10.4

#### Rule 4.10.4 — No tables for what a sentence says better
**Class:** recommended · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** table
**Navigation:** target: table · chunks: any · slots: any · layers: plain · context: local · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 5.5.1

> A table **should not** replace a sentence that states two to four facts equally well. Tables **should** contain genuinely tabular data under §5.5.

**Rationale:** A small table adds grid-reading overhead to content without grid structure. The table can signal template-driven drafting instead of data (P5). The 2–4-row flag is a lint candidate, not a verdict. Some small tables, such as symbol tables, are genuinely tabular.

**Compliant:** "Median latency was 84 ms before the index change and 41 ms after."
**Non-compliant:** A two-row table titled "Latency results" with columns "Setting" and "Latency" holding those same facts.

**Cross-references:** §5.5, §5.2 (notation tables are tabular)

**Phrase list 4.10.5 — emoji code points (pattern):** "[\U0001F300-\U0001FAFF]"; "[\U00002600-\U000027BF]"; "[\U0001F000-\U0001F0FF]"; "[\U0001FE0F-\U0001FE0F]".

#### Rule 4.10.5 — No emoji
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** any
**Navigation:** target: document · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** none

> Governed documents **shall not** contain emoji.

**Rationale:** Emoji are register markers from another medium. In governed technical prose, they add tone where calibrated language already fixes tone (§5.6, P2). A regular expression can perform the check.

**Compliant:** "The index also cut median query time by 9%."
**Non-compliant:** "The index also cut median query time by 9% 🎉"

**Cross-references:** §5.6, §8.2

Rule 4.10.6 covers boilerplate outline sections such as "Challenges / Future Prospects."

#### Rule 4.10.6 — No canned section formulas
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** section
**Navigation:** target: section · chunks: any · slots: any · layers: plain · context: section · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 6.5.4

> A document **shall not** contain a section that could apply unchanged to another subject. The document **shall not** use a covered boilerplate outline.

**Rationale:** This rule is the structural form of specific-over-generic (P5). Sections exist to meet the document's needs. An outline slot alone does not justify a section. The test applies P5's sentence test to sections. A section that survives a subject swap asserts nothing.

**Compliant:** A risk section states that the design has not been tested under region loss and that clock skew can expire all leases together.
**Non-compliant:** "Despite its promise, the architecture faces several challenges. Despite these challenges, its future remains bright."

**Cross-references:** §1.1 P5, §7.1, §6.5

## 4.11 Work items separate strategy, acceptance, and contribution

Section 4.11 governs the work-item hierarchy. Its rules apply to `epic`, `task`, and `subtask` only. Section 1.5 places those rules in the overlay directories:

- Rules shared by more than one work-item profile are in `spec/overlays/shared/work-item.md`.
- Rules scoped to one profile are in that profile's `rules.md`.

Annex C indexes every §4.11 rule with its profile applicability and its file.

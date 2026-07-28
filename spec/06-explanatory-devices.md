# Part 6 — Explanatory devices

Part 6 governs devices that explain concepts to the profile's assumed reader (§0.3). These devices include analogies, worked examples, intuition blocks, diagrams, and repetition. The devices carry the plain layer of the two-layer model (§1.2). The devices inform. These devices never carry the exact layer. Requirements, design invariants, procedure conditions, decisions, incident findings, and research claims are exact content. An analogy, intuition block, or explanatory diagram alone cannot establish exact content.

## 6.1 Analogies

An analogy maps a new concept onto something the profile's assumed reader already knows. The anchor comes from that profile's baseline or from vocabulary the document has already admitted. An unfamiliar anchor asks the reader to learn two things instead of one. Every analogy is wrong somewhere. The rules below make that wrongness explicit.

**Permitted analogy anchors:** concepts from the declared profile's assumed-reader baseline (Annex B) and previously admitted terms.

#### Rule 6.1.1 — Anchor analogies in assumed-reader vocabulary
**Class:** mandatory · **Machine-checkable:** no · **Source:** original

> Every analogy **shall** map its explained concept onto a permitted analogy anchor.

**Rationale:** An analogy explains only if its anchor is already understood (P4). Profile awareness matters: an API contract may be baseline vocabulary for one reader profile and ladder-required for another.

**Compliant:** In an explanation for software engineers: "A schema invariant is like a type invariant. Unlike a type invariant, the schema invariant spans persisted versions and concurrent writers."
**Non-compliant:** In a procedure for the same reader: "The rollback boundary is like an aircraft's V1 speed." The anchor is outside the declared baseline. The document has not admitted the anchor.

**Cross-references:** §0.3, Annex B, Rule 2.3.1.

#### Rule 6.1.2 — State the breaking point
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

> Every analogy **shall** state where it breaks: the first property of the anchor that does not transfer to the concept.

**Rationale:** The reader cannot tell which anchor properties transfer. The writer can identify those properties (P3). An analogy without a breaking point silently exports false properties. The "except" clause is the price of using the analogy. A linter can flag analogy markers without an adjacent "except," "unlike," or "but" clause. A human confirms the substantive break.

**Compliant:** "A circuit breaker works like a conditional guard around a dependency call. Unlike the guard, the circuit breaker remembers recent failures and changes state over time."
**Non-compliant:** "A circuit breaker works like a conditional guard around a dependency call."

**Cross-references:** Rule 6.1.1, Rule 6.3.2.

**Analogy consistency conditions:** a concept uses at most one analogy within the document, and each analogy uses exactly one anchor.

#### Rule 6.1.3 — At most one analogy per concept
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

> Every analogy use **shall** meet both analogy consistency conditions.

**Rationale:** Stacked analogies force the reader to reconcile multiple anchors with the concept. The document never states that reconciliation (P4). A concept needing more support requires a definition or worked example, not another analogy.

**Compliant:** "Rollback restores the last compatible database schema and then replays queued writes. Rollback does not reverse messages already delivered to external systems."
**Non-compliant:** "Rollback is like rewinding a recording, or perhaps like restoring a version-control commit while the service traffic is a river." Three anchors compete.

**Cross-references:** Rule 6.1.1, Rule 6.2.1.

## 6.2 Worked examples

A worked example runs a mechanism, decision test, or procedure path on concrete values. The reader can compare personal understanding against that run. The rules adapt Carroll's minimalist documentation principles and the Google style guide's example-quality rules.

**Central mechanisms:** mechanisms on which the document's primary outcome depends.

**Worked-example trace:** concrete inputs through the mechanism to concrete outputs, states, or decisions.

#### Rule 6.2.1 — Central mechanisms get a worked example
**Class:** mandatory · **Machine-checkable:** no · **Source:** Carroll minimalism

> Every central mechanism **shall** have one worked example.
>
> The example **shall** include the complete worked-example trace.

**Rationale:** The assumed-reader test (§1.2) fails most often at mechanisms the writer understood too well to walk through. A worked example is the only device the reader can check themselves against (P4). A peripheral mechanism **may** rely on definition alone.

**Compliant:** In a procedure: "Before the change, node A is primary and node B is caught up at log position 840. Promote B, verify that a test write reaches position 841 on B, then demote A. If the test write does not appear within 30 seconds, stop and run rollback step R1."
**Non-compliant:** "Promote the replica, verify success, and roll back if needed." The procedure asserts its central state transition without tracing the transition.

**Cross-references:** Rule 6.2.2, §5.3 (equations get plain readings), §4.1 (a worked example is a mechanism chunk).

#### Rule 6.2.2 — Examples carry no incidental complexity
**Class:** mandatory · **Machine-checkable:** no · **Source:** Carroll minimalism / Google style guide

> A worked example **shall not** contain detail that the point being shown does not need.

**Rationale:** Every incidental detail is a candidate explanation the reader must rule out (P4). Two nodes show a failover state transition as well as a 40-node fleet. Three timeline events show evidence ordering as well as thirty.

**Compliant:** In a privacy explanation: "Start with one log entry containing an email address and a request identifier. Show the redaction step replacing the email address while retaining the identifier used for debugging."
**Non-compliant:** "Start with the full production event, including 40 unrelated metadata fields. Follow the event through every analytics export." The extra fields and systems do not help explain redaction.

**Cross-references:** Rule 6.2.1, Rule 6.2.3.

**Realistic-value definition:** values drawn from the reported task, data, or system, even when simplified in scale.

#### Rule 6.2.3 — Examples use realistic values
**Class:** recommended · **Machine-checkable:** no · **Source:** Google style guide

> Worked-example values **should** meet the realistic-value definition.

**Rationale:** Placeholder values include "foo," "widget," and x₁…x₉. Such values force the reader to map the example back to reality. The worked example should perform that mapping (P5).

**Compliant:** In a hardware procedure: "Discharge a 5 Ah test battery at 25 °C and 1 A for 30 minutes. The example uses the procedure's cell type and units at a shorter duration."
**Non-compliant:** "Device A receives value `foo` and returns value `bar`."

**Cross-references:** Rule 6.2.2, §2.7 (naming).

## 6.3 Intuition blocks

An intuition block is a bounded, labeled span of informal explanation. The block is the document's sanctioned place for "roughly speaking." The mechanism comes from STE's informative-note system. Notes inform, and no requirement may live in a note. The same discipline protects every profile's exact layer. Exact content may not live only in an intuition block. Section 7.3's speculation blocks reuse this mechanism with a different label and vocabulary.

**Intuition-block form:** a blockquote starting with the bold label **[Intuition — <topic>]** under Rule 4.6.2. The block ends where the blockquote ends.

#### Rule 6.3.1 — Intuition is bounded and labeled
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ASD-STE100 (note blocks)

> Informal explanation **shall** appear only in the intuition-block form.

**Rationale:** The boundary tells the reader and linter where precision is suspended (P3). Unmarked informality in main text blurs the sentence's layer.

**Compliant:**
> **[Intuition — backpressure]** Think of the bounded queue as a buffer between a fast producer and a slow consumer. Unlike an in-process buffer, the queue may reject producers. Producers must handle that response.

**Non-compliant:** "Requests then enter the queue. Loosely, the queue absorbs any traffic spike, which is why overload cannot reach the database." The informality is inline and unbounded. The passage states the informal explanation as a guarantee.

**Cross-references:** §4.6 (bounded technical blocks use the same delimiting), Rule 7.3.2 (speculation blocks).

**Exact-content types:** requirements, decisions, preconditions, verifications, rollback conditions, findings, measurements, comparisons, and other exact statements.

#### Rule 6.3.2 — Exact content does not live only in intuition blocks
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC Directives Part 2

> An intuition block **shall not** be the only location of an exact-content type.

**Rationale:** Rule 6.3.2 extends ISO/IEC Directives Part 2's "notes shall not contain requirements" to every profile. Exact content hidden in an intuition block escapes evidence rules (§5.4, §5.6). The content may also escape required subject-matter review (§8.4). Block content must derive from the exact layer or remain removable without harm. A linter can flag calibrated phrases and normative keywords inside intuition blocks. A human must find unphrased exact content.

**Compliant:**
> **[Intuition — compatibility window]** Keeping both response fields for one release resembles briefly supporting two function signatures. Unlike local callers, network clients upgrade independently. Section 4.2 gives the exact compatibility invariant and removal date.

**Non-compliant:**
> **[Intuition — compatibility]** Old clients can use field `name` until 30 September. After that date, the service returns only `display_name`. The requirement and date exist nowhere else in the design.

**Cross-references:** Rule 6.3.3, §5.1, §1.4 (normative text over notes).

#### Rule 6.3.3 — Main text survives block removal
**Class:** mandatory · **Machine-checkable:** no · **Source:** original

> The main text **shall** remain coherent and complete when every intuition block is removed.

**Rationale:** The block boundary promises that its content is optional (P4). A later sentence cannot depend on content found only in an intuition block. Such content is load-bearing and belongs in main text. Rule 6.3.3 applies §4.6's skip-coherence requirement to intuition blocks.

**Compliant:** main text defines the compatibility invariant, an intuition block offers the two-signature picture, and later sections use only the exact invariant.
**Non-compliant:** An intuition block introduces a "safe window." The procedure later says "deploy during the safe window" without defining dates or checks in main text.

**Cross-references:** §4.6, Rule 6.3.1.

## 6.4 Diagrams

The requirements adapt ISO/IEC/IEEE 26514 and IEC 82079-1 guidance on illustration need, labeling, and text references. Caption and alt-text guidance comes from the Google style guide. Section 5.5 governs figures that present evidence. Section 6.4 governs diagrams that explain structure, sequence, state, or causality. Section 5.5 also applies when a diagram presents evidence.

**Diagram-trigger structure:** three or more interacting components on which the document's primary outcome depends.

#### Rule 6.4.1 — Diagram structures that prose cannot carry
**Class:** recommended · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514 / IEC 82079-1

> A diagram-trigger structure **should** be shown as a diagram.
>
> The structure **should not** be described only in prose.

**Rationale:** Prose serializes information. Structure is parallel (P4). Three interacting components create more pairwise relations than one sentence can hold in working memory.

**Compliant:** A design RFC shows the gateway, queue, worker, and database as labeled boxes with request and failure paths. The prose walks the diagram.
**Non-compliant:** "The gateway sends accepted jobs to the queue. The worker drains the queue while writing state to the database. During overload, the gateway rejects jobs before enqueue." No diagram shows these interactions.

**Cross-references:** Rule 6.4.2, §5.5.

#### Rule 6.4.2 — Every diagram is referenced from the text
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ISO/IEC/IEEE 26514

> Every diagram **shall** be referenced from the main text by its number, at the point where the reader needs it.

**Rationale:** An unreferenced diagram forces the reader to integrate content without guidance. Otherwise, the diagram is decoration (P7). The reference tells the reader when to leave the prose.

**Compliant:** "Figure 2 shows the failover states and the verification path used in steps 4–7."
**Non-compliant:** A state diagram floats above the procedure. No step or sentence mentions the diagram.

**Cross-references:** §5.5, Rule 6.4.3.

**Diagram text:** labels, node names, edge annotations, and legend entries.

#### Rule 6.4.3 — Diagram labels use admitted terms only
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original

> Diagram text **shall** use only assumed vocabulary (Annex B) and previously admitted terms.
>
> Admission **shall** precede the diagram's first reference.

**Rationale:** A reader reads a diagram as a unit. One unadmitted label can make the whole picture illegible to the assumed reader (P2, P4). The check uses the document's ladder state at the referencing sentence. Section 2.3 applies the same check to prose.

**Compliant:** A diagram referenced in §2 labels its middle state "traffic drained," a term admitted in §1.
**Non-compliant:** The same diagram labels the state "L7 quiesced" when neither "L7" nor "quiesced" has been admitted for the profile's assumed reader.

**Cross-references:** Rule 2.3.1, Rule 6.4.2, §8.2.

#### Rule 6.4.4 — Diagrams carry alt text
**Class:** recommended · **Machine-checkable:** yes · **Source:** Google style guide

> Every diagram **should** carry alt text that states what the diagram shows, using the same admitted terms as its labels.

**Rationale:** Some tools that display governed documents may not render images. Alt text also tests whether the diagram has one stateable point.

**Compliant:** `alt="Requests flow from gateway to queue to worker. Overload rejection occurs before the queue."`
**Non-compliant:** `alt="diagram"`.

**Cross-references:** Rule 6.4.3, §5.5.

## 6.5 Repetition and reinforcement

Many prose traditions prize elegant variation. This specification prohibits elegant variation (P2). The specification permits repetition that restores distant information the assumed reader needs. Examples include a definition recalled at reuse and a ladder recap at a major boundary.

Prohibited restatement repeats recently read content without adding information. Permitted redundancy helps a reader who has forgotten distant information. A hollow summary addresses a reader who just read the section and needs nothing.

#### Rule 6.5.1 — Repeat verbatim or not at all
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100

> Repeated definitions, claims, and admitted terms **shall** use wording identical to the original in every load-bearing element.

**Rationale:** Varied restatement forces the reader to check whether the variation is a new statement (P2). Identical wording makes the repetition instantly recognizable as recall, not news. Rule 6.5.1 generalizes STE's consistent-repetition principle from terms to statements.

**Compliant:** "Recall: the rollback boundary is the last step after which the previous version can be restored without data repair." (Identical to the §2 definition.)
**Non-compliant:** "Recall that rollback is the safe way back to the old system." (A new, weaker framing wearing a recall marker.)

**Cross-references:** Rule 2.1.2 (no synonym variation), Rule 6.5.2.

**Distant-reuse trigger:** an admitted term's next use occurs after more than 2,500 intervening words.

**Distant-reuse support:** a verbatim definition recall or a section reference.

#### Rule 6.5.2 — Recall distant definitions at reuse
**Class:** recommended · **Machine-checkable:** yes · **Source:** original (instructional-design spaced recall)

> A use meeting the distant-reuse trigger **should** include distant-reuse support.

**Rationale:** The ladder admits a term once, but admission does not ensure retention (P1, P4). The 2,500-word threshold represents five Rule 4.8.1 pages. The threshold is provisional. Section 8.3 reader-testing results calibrate it.

**Compliant:** "The replay harness (§2.3: the tool that sends a recorded request set to a test deployment) reproduces the timeout in 92% of runs."
**Non-compliant:** After more than 2,500 intervening words, "the replay harness" reappears bare. The assumed reader must re-derive its meaning.

**Cross-references:** Rule 2.3.1, Rule 6.5.1, §4.8.

**Boundary recap:** a paragraph or list introduced by "Recall:" that contains every admitted term the section depends on and each term's verbatim definition.

#### Rule 6.5.3 — Recap the ladder at part boundaries
**Class:** permitted · **Machine-checkable:** yes · **Source:** original

> A major section **may** open with a boundary recap.

**Rationale:** A recap at the boundary lets a returning reader re-enter without rereading (P1). The recap remains ordinary main-flow content, not a §4.6 bounded block. `Recall` is not one of the closed bounded-block labels.

**Compliant:** "Recall: *rollback boundary* means the last step after which the previous version can be restored without data repair. *Verification query* means the read-only query that confirms the new version serves current data."

**Non-compliant:** A recap is woven into opening prose as new content and explains rollback in fresh words. The recap fails Rule 6.5.1. Without a marker, the recap reads as news.

**Cross-references:** Rule 6.5.1, Rule 6.5.2.

#### Rule 6.5.4 — No hollow summaries
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"

> A section **shall not** end with a paragraph that restates content without adding information.
>
> A section **shall** end on its last substantive point.

**Rationale:** A hollow closing paragraph repeats content the reader just read. Common openers include "In summary," "Overall," and "Taken together, these results." This pattern is opposite to Rule 6.5.2's distant recall. The pattern is also a clear structural symptom of generic prose (P5). A conforming document deletes a closing paragraph that adds nothing. A closing paragraph remains substantive when it adds a consequence, bound, or forward pointer. Linters flag the opener phrases. A human confirms deletability.

**Compliant:** An incident-analysis section ends with its last bound: "The traces establish when retries began. Retention expired before the first connection failure. The trigger therefore remains unknown."
**Non-compliant:** "In summary, this section reviewed the incident timeline and discussed the major contributing factors."

**Worked deletion:** Append the non-compliant paragraph above after the compliant paragraph. Delete the non-compliant paragraph. Every referenced fact, including "timeline" and "contributing factors," appeared earlier. Nothing is lost. The section now ends on the unresolved evidence boundary, its strongest point.

**Cross-references:** P5, §3.10 (formulaic constructions), §4.2 (claim-first makes trailing summaries redundant), §8.2.

# Part 5 — Technical exactness and evidence

Part 5 governs the exact layer of every governed document. That layer includes claims, decisions, requirements, interfaces, invariants, procedure controls, incident timelines, notation, equations, evidence, figures, statistics, reproducibility, and verification.

By §1.4, these rules override Parts 2–4 and 6 wherever they collide. A plain rendering traces to an exact statement (§5.1). Symbols use the same ladder as terms (§5.2). Equations receive plain readings (§5.3). Material exact items carry a complete evidence record (§5.4). Evidential strength and decision authority use calibrated language (§5.6).

Profile-specific exactness fields extend that shared record. They do not replace the shared record. Sections 5.7–5.9 are profile-scoped and keep their rules in the overlay directories (§1.5).

## 5.1 The exactness principle

Plain prose may simplify an explanation. Plain prose may never blur an exact statement. A simpler restatement remains a rendering of an exact statement elsewhere in the document. The reader can follow a link from the restatement to that exact statement.

#### Rule 5.1.1 — Simplification preserves exact meaning
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** claim
**Navigation:** target: chunk · chunks: any · slots: any · layers: both · context: neighboring · rewrite: prohibited
**Resources:** reads: chunk-text, exact-item-ledger · writes: none
**Relations:** constrains 5.1.2

> A plain-language rendering **shall not** change the scope, status, strength, conditions, or required behavior of the exact statement it renders.

**Rationale:** The two-layer model (§1.2) fails silently when a simplified statement loses exact content. A decision may lose a trade-off. A procedure may lose a precondition. A result may widen its scope. The rendering reads well but is wrong. Serves P3.

**Compliant:** "The new queue protects checkout from traffic spikes (exact design constraints in §4.2)." Section 4.2 limits the statement to a stated load range. Section 4.2 also defines the latency and loss invariants.
**Non-compliant:** "The new queue prevents checkout failures" as the plain rendering of a design that only bounds overload behavior below 20,000 requests per second.

**Cross-references:** §1.2, Rule 5.6.2, Rule 7.4.1

**Simplified material items:** claims, decisions, requirements, conditions, and outcomes.

#### Rule 5.1.2 — Simplified statements trace to exact statements
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** cross-reference, claim
**Navigation:** target: chunk · chunks: any · slots: any · layers: both · context: document · rewrite: candidate
**Resources:** reads: chunk-text, exact-item-ledger · writes: chunk-text, cross-reference-ledger
**Relations:** requires 5.1.1

> Every simplified rendering of a simplified material item **shall** explicitly reference the exact statement it renders.

**Rationale:** Traceability makes Rule 5.1.1 checkable. A reviewer compares the rendering against its target instead of searching for the target. Serves P3 and P7. A linter can flag simplified-claim markers without references. A human judges equivalence.

**Compliant:** "In plain terms: stop the rollout if verification fails (exact checks and rollback boundary in Procedure §6)."
**Non-compliant:** "In plain terms: stop if anything looks wrong." The statement has no pointer to the exact checks, threshold, or rollback boundary.

**Cross-references:** Rule 5.1.1, §4.6 (layering), §8.2

## 5.2 Notation

Notation is vocabulary. The §2.3 term ladder applies equally to symbols and terms. A small baseline set is free. Writers admit every other symbol by definition at first use. Each symbol means one thing throughout the document.

Annex B §B.2 is the sole normative **baseline notation set**. The baseline contains:

- Arithmetic operators and parentheses.
- Equality and comparison operators.
- Percent notation, plain ratios, and plain numeric ranges.

The following notation is not baseline and therefore requires ladder admission:

- Variables, named constants, function application, and subscripted indexing.
- Approximation, powers, absolute value, scientific notation, and interval notation.
- Summation, product, logarithmic, exponential, factorial, Big-O, and set notation.
- Matrix and vector notation and operations.
- Norms, gradients (∇), and derivatives.
- Expectation and probability operators (𝔼, Pr).
- Argmax, argmin, and distribution symbols (`~`).
- Tensor index conventions and any ML-community shorthand, including θ for parameters and ℒ for loss.

**Permitted symbol-definition vocabulary:** baseline notation, admitted symbols, and admitted terms.

#### Rule 5.2.1 — Define every non-baseline symbol at first use
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (mechanism from §2.3)
**Constructs:** symbol
**Navigation:** target: symbol · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, symbol-ledger · writes: chunk-text, symbol-ledger
**Relations:** requires 2.3.1; constrains 5.2.2

> A symbol outside the baseline notation set **shall** be defined in prose at or before first use.
>
> The definition **shall** use only the permitted symbol-definition vocabulary.

**Rationale:** A reader cannot expand an unknown symbol. Unlike an unknown word, the symbol cannot even be sounded out. The term ladder also applies to notation. Serves P4. A linter can flag symbols that appear before a defining sentence. A human judges definition quality.

**Compliant:** After admitting *model* and *training*: "Write θ for the model's stored numbers. Write L for the scoring function. L(θ) means the score for the model configured by θ."
**Non-compliant:** "We minimize L(θ) by stochastic gradient descent." Neither L nor θ has been defined.

**Cross-references:** §2.3, Rule 5.2.2, Annex B §B.2

#### Rule 5.2.2 — One symbol, one meaning
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ASD-STE100 (adapted)
**Constructs:** symbol
**Navigation:** target: symbol · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, symbol-ledger · writes: symbol-ledger
**Relations:** requires 5.2.1; pairs-with 2.1.1

> A symbol **shall** have exactly one meaning within a document.
>
> A meaning **shall** be written with exactly one symbol.

**Rationale:** Symbol reuse forces the reader to remember which local meaning applies. The assumed reader may choose the wrong meaning when it matters. Serves P2. Tooling can check the document's symbol table.

**Compliant:** α is the learning rate everywhere in the document. The significance level is written out or receives a different symbol at admission.
**Non-compliant:** α is the learning rate in §3 and the significance level in §5.

**Cross-references:** Rule 5.2.1, §2.1, §8.2

**Required notation-table fields:** every defined symbol, its meaning, and its admission section.

#### Rule 5.2.3 — Notation table above six symbols
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** symbol, table
**Navigation:** target: table · chunks: any · slots: any · layers: exact · context: document · rewrite: candidate
**Resources:** reads: symbol-ledger · writes: chunk-text, symbol-ledger
**Relations:** requires 5.2.1

> A document defining more than six non-baseline symbols **shall** include a notation table.
>
> The table **shall** contain every required notation-table field.

**Rationale:** In-prose definitions scale to a handful of symbols. Beyond that number, the reader needs an index to recover a definition without rereading. The threshold of six remains provisional. Serves P4.

**Compliant:** A capacity report defining λ, μ, Q, W, C, U, and R includes a notation table before the first analysis section.
**Non-compliant:** The same report defines all seven symbols across nine pages of prose with no table.

**Cross-references:** Rule 5.2.1, §4.8

## 5.3 Equations in prose

An equation the reader cannot read aloud is an image, not a statement. Every displayed equation has a plain-language reading. Inline math remains simple enough to preserve its sentence.

**Required equation-reading content:** what the equation computes and why it appears at that point.

#### Rule 5.3.1 — Every displayed equation gets a plain-language reading
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** equation
**Navigation:** target: equation · chunks: any · slots: any · layers: both · context: local · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 5.2.1

> Every displayed equation **shall** have an adjacent plain-language reading.
>
> The reading **shall** include all required equation-reading content.

**Rationale:** The assumed reader follows basic software concepts but may parse neither code nor mathematical notation fluently. The reading documents the equation. The reading also explains why the equation appears there. A reader may skip an unmotivated equation. Section 4.6 permits that skip only for bounded blocks, not load-bearing equations. Serves P3 and P4. A linter can flag displayed equations without adjacent readings. A human judges adequacy.

**Compliant:**

Before the display, the document defines every symbol. N is the number of examples. The symbol i identifies one example. The expression x_i is that example's input. The expression y_i is its correct answer. The expression f(x_i) is the model's prediction. L is the average error. Σ means add the following expression for every i from 1 through N. The superscript 2 means multiply the difference by itself.

    L = (1/N) Σ_{i=1..N} (y_i − f(x_i))²

"This is the model's average error on the training data. For each of the N training examples, subtract the model's prediction f(x_i) from the correct answer y_i. Square each difference, so overshooting and undershooting both count as error. Then average the squared differences across all examples. Training, defined in §2, searches for parameters that make this number small. The rest of this section measures how that search behaves."

**Non-compliant:** The same displayed equation is followed directly by "Optimization proceeds by stochastic gradient descent." No reading explains what L measures or why L matters here.

**Cross-references:** Rule 5.2.1, §4.6, §6.2

**Atomic inline forms:** single symbols, function applications, and single binary relations.

**Display-required forms:** expressions containing a summation, product, fraction, or nested subexpression.

#### Rule 5.3.2 — Keep inline math atomic
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** equation
**Navigation:** target: equation · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 5.3.1; pairs-with 3.1.3

> Inline mathematics **shall** use only atomic inline forms.
>
> Every display-required form **shall** be displayed.

**Rationale:** Complex inline math breaks the sentence's grammatical thread. Sentence length caps (§3.1) also become meaningless. Displayed equations receive a reading under Rule 5.3.1. Inline fragments cannot receive that reading. Serves P1. Rule 5.3.2 is the construct-specific override anticipated in §1.4(5).

**Compliant:** "The error L falls below 0.05 after one pass over the data, as shown in Equation 2."
**Non-compliant:** "Since L = (1/N) Σ_{i=1..N} (y_i − f(x_i))² < 0.05 after one epoch, we proceed to ablations."

**Cross-references:** §3.1, Rule 5.3.1

## 5.4 Reporting claims, decisions, and operational outcomes

**Materiality outcomes:** implementation, action, approval decision, risk judgment, conclusion, or evaluation of the profile job.

A statement is **material** when changing or omitting it could change a materiality outcome. Supporting color and non-load-bearing examples are not material.

A material statement is complete when the reader can recover its exact content and audit why the document makes it. The **complete evidence record** has these shared fields:

1. **Exact item** — the claim, decision, requirement, interface, invariant, procedure control, observation, measurement, or operational outcome.
2. **Context** — the environment, version, dependency state, data, population, operating condition, time window, or other boundary needed to know where the statement holds.
3. **Baseline or alternatives** — the previous state, expected state, comparison point, rejected options, or an explicit statement that no meaningful baseline exists.
4. **Evidence** — measurements, tests, logs, traces, sources, proofs, or decision rationale that support the statement.
5. **Evidential strength and uncertainty** — the applicable §5.6 strength. Include quantified or bounded uncertainty when evidence is sampled, variable, incomplete, or inferential. Otherwise, state that no such uncertainty applies.
6. **Lifecycle or authority status** — the applicable approval, verification, adoption, release, or investigation state. The state prevents unsettled items from reading as settled. Otherwise, state that no lifecycle status applies.

The fields take the form appropriate to the item. A requirement's evidence may be its governing constraint or decision rationale. Its authority status includes normative force and acceptance condition. A decision uses alternatives and approval state. An observed outcome uses a comparison point, measurements, uncertainty, and verification state. A field need not appear in every sentence. An item may link to one section-level or document-level record that supplies the field. Profile-specific fields are document or section obligations unless an individual item needs a narrower value.

The record gains these profile-specific fields:

- `design-rfc` — affected interfaces and invariants. Interfaces cover inputs, outputs, errors, compatibility, and versioning. Invariants apply before, during, and after the change.
- `decision-record` — the decision state and date, the options considered, and the consequences or trade-offs accepted.
- `procedure` — preconditions and verification after critical steps and at completion. The profile field also covers rollback or recovery instructions, including any unsafe rollback point.
- `explanation` — the exact definition or mechanism being explained, the conditions under which it applies, and sources or evidence for its factual assertions.
- `incident` — a timestamped timeline with one stated time zone. The timeline links evidence to each material event. The timeline covers impact and evidence of mitigation or recovery. Inferred events are marked as interpretation.
- `technical-report` — the relevant system configuration, dependency versions, method, and evidence for each reported operational outcome.
- `research-paper` — the statistical and reproducibility detail required by §§5.7–5.8.
- `investigation-log` — the time and configuration of each observation and its evidence source. The profile field also covers the status of each hypothesis.
- `epic` — the strategic outcome, problem evidence, success measures, technical-invariant IDs, child-task boundaries, cross-task risks, and DoD verification.
- `task` — both classifications, parent and invariant links, journey or technical boundary, path records, completion-condition IDs, and integrated-acceptance evidence. A defect correction also carries its accepted behavior contract and deviation evidence.
- `subtask` — the parent task, named parent condition, inherited invariants, bounded contribution, delegated path detail, and verification evidence.

The citation-integrity rules in this section apply in every profile. Fabricated-but-plausible references are a realistic failure mode in any machine-generated draft.

**Complete evidence-record fields:** the six shared fields and every applicable profile-specific field defined in §5.4.

#### Rule 5.4.1 — Material statements carry a complete evidence record
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; IEC 82079-1; APA JARS / NeurIPS checklist (research adaptation)
**Constructs:** claim, measurement
**Navigation:** target: chunk · chunks: claim, evidence · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, evidence-ledger · writes: chunk-text, evidence-ledger
**Relations:** constrains 5.4.2; pairs-with 5.6.2

> Every material exact item listed in §5.4 **shall** carry the complete evidence record.
>
> The item, immediate context, or explicit links **shall** supply every field.

**Rationale:** An incomplete exact item cannot be checked, reproduced, implemented, or compared. Context, alternatives, evidence, strength, uncertainty, and status make the item complete. Profile fields make each profile's exact items complete. Serves P6.

**Compliant:** After admitting *p99* under §2.3: "For API v3, we replayed 12,000 requests/s. Verification confirms the proposed bounded queue keeps p99 latency below the existing 450 ms objective. The current implementation reached 710 ms. The proposed build reached 398–421 ms across five runs. Section 3 defines interface changes and the no-loss invariant. Section 6 links the harness and traces. The measured range reports run-to-run uncertainty. The design is proposed, not approved."
**Non-compliant:** "The new queue fixes latency." The statement has no version, load context, baseline, evidence, invariant, evidential strength, uncertainty, or proposal status.

**Cross-references:** Rule 5.4.2, Rule 5.6.2, §§5.7–5.8

**Required change context:** base values and an absolute-or-relative marker.

#### Rule 5.4.2 — No naked percentages
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; APA JARS (effect size + uncertainty, restated)
**Constructs:** quantity
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: chunk-text, evidence-ledger · writes: chunk-text
**Relations:** requires 5.4.1

> A percentage or improvement figure **shall not** appear without the required change context.

**Rationale:** "Improved by 5%" can mean 61% → 66%. The phrase can also mean 61% → 64.05%. Headline numbers often travel without their context. Rule 5.4.2 applies the specificity principle (P5) to numbers.

**Compliant:** "Latency fell 18% relative (from 340 ms to 279 ms median across 10,000 requests in the production replay)."
**Non-compliant:** "Our method reduces latency by 18%."

**Cross-references:** Rule 5.4.1, §1.1 (P5)

**Citation-resolution checks:**

- A digital object identifier (DOI) resolves to the referenced publication.
- A uniform resource locator (URL) is live or archived.
- A book citation carries page numbers.

#### Rule 5.4.3 — Every citation resolves
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing" (citations)
**Constructs:** citation
**Navigation:** target: citation · chunks: any · slots: any · layers: exact · context: document · rewrite: prohibited
**Resources:** reads: citation-ledger · writes: none
**Relations:** constrains 5.4.4

> Every citation **shall** pass every applicable citation-resolution check.

**Rationale:** A valid-looking DOI that resolves elsewhere and a dead, unarchived link are hallucination signals, not ordinary link rot. Mechanical resolution checks run in §8.2. Serves P6.

**Compliant:** "RFC 9110, *HTTP Semantics*, https://www.rfc-editor.org/rfc/rfc9110.html." The URL resolves to that RFC.
**Non-compliant:** A citation whose DOI resolves to an unrelated article, or whose URL does not resolve and has no archived copy.

**Cross-references:** Rule 5.4.4, §8.2

#### Rule 5.4.4 — Cited sources support the claim
**Class:** mandatory · **Machine-checkable:** no · **Source:** Wikipedia "Signs of AI writing" (citations)
**Constructs:** citation, claim
**Navigation:** target: citation · chunks: any · slots: any · layers: exact · context: collection · rewrite: prohibited
**Resources:** reads: citation-ledger, claim-ledger · writes: none
**Relations:** requires 5.4.3

> The cited page or section **shall** state or directly support the claim it is cited for.

**Rationale:** Resolution (Rule 5.4.3) is necessary but insufficient. A real source may not support the claim for which it is cited. An unsupported citation is the harder-to-catch half of citation fabrication. The subject-matter-owner review (§8.4) checks support where that review tier applies.

**Compliant:** Citing API contract §3.2 for "clients may retry this operation safely" when §3.2 specifies idempotent retry behavior.
**Non-compliant:** Citing an architecture overview for a retry guarantee it never states.

**Cross-references:** Rule 5.4.3, §8.4

#### Rule 5.4.5 — Source counts are accurate
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing" (source-count inflation)
**Constructs:** citation
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text, citation-ledger · writes: chunk-text
**Relations:** requires 5.4.3; pairs-with 2.6.8

> Plural attributions ("several studies," "multiple reports") **shall** be backed by at least that many distinct cited sources.

**Rationale:** Source-count inflation borrows authority the evidence does not have. Section 2.6 prohibits vague-attribution phrasing. Rule 5.4.5 covers the counted form. Serves P5 and P6.

**Compliant:** "Two studies report the same reversal (Kim 2024; Osei 2025)."
**Non-compliant:** "Several studies report the same reversal (Kim 2024)."

**Cross-references:** §2.6, Rule 5.4.4

## 5.5 Figures and tables

A useful figure or table communicates its exact takeaway and bounds without surrounding text. Axis, unit, and legend conventions come from APA and IEEE practice. The self-containment requirements are original. Part 6 governs explanatory diagrams. Both parts apply when a diagram also presents evidence.

**Quantitative figure labels:** quantity and unit for each axis, every plotted series, and any nonlinear scale.

#### Rule 5.5.1 — Label axes, units, and series completely
**Class:** mandatory · **Machine-checkable:** partial · **Source:** APA / IEEE figure conventions
**Constructs:** figure
**Navigation:** target: figure · chunks: any · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: figure-ledger · writes: figure-ledger
**Relations:** constrains 5.5.2

> Every quantitative figure **shall** include every quantitative figure label.

**Rationale:** An unlabeled axis makes the figure unfalsifiable. A hidden logarithmic scale makes the figure misleading. Serves P6.

**Compliant:** After admitting *p99* and *logarithmic scale*: X axis "request rate (requests/s)," Y axis "p99 latency (ms)," legend naming the current and proposed queue, caption noting the logarithmic X axis.
**Non-compliant:** A curve labeled "performance" over an unlabeled X axis.

**Cross-references:** Rule 5.5.2, §6.4

**Caption-supported items:** claims, decisions, and operational outcomes.

#### Rule 5.5.2 — The caption states the takeaway
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514; Nature-style figure guidance
**Constructs:** figure, table
**Navigation:** target: figure · chunks: any · slots: any · layers: both · context: local · rewrite: candidate
**Resources:** reads: chunk-text, figure-ledger · writes: chunk-text, figure-ledger
**Relations:** requires 5.5.1

> A figure or table caption **shall** state the caption-supported item the artifact supports.
>
> The caption **shall not** state only what the artifact depicts.

**Rationale:** Readers, especially skimming readers, read captions before body text. "Latency by load" only describes the artifact. "The proposed queue meets the latency invariant through 12,000 requests/s" informs the reader. Rule 5.5.2 applies §4.5's informative-heading rule to captions. Serves P5.

**Compliant:** After admitting *p99* under §2.3: "Figure 3: The proposed queue meets the 450 ms p99 invariant through 12,000 requests/s. Each point is the median of five replays. Bars show minimum and maximum."
**Non-compliant:** "Figure 3: Queue latency."

**Cross-references:** §4.5, Rule 5.5.3

**Figure text locations:** a figure, its caption, and its legend.

#### Rule 5.5.3 — Figures stand alone for the assumed reader
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** figure, admitted-term
**Navigation:** target: figure · chunks: any · slots: any · layers: plain · context: document · rewrite: review
**Resources:** reads: figure-ledger, term-ledger · writes: figure-ledger
**Relations:** requires 2.3.1

> Every term and symbol in a figure text location **shall** be assumed (§0.3) or previously admitted.
>
> Admission **shall** precede the figure.

**Rationale:** Figures travel: they are extracted into slides, reviews, and summaries without their body text. A figure that depends on unadmitted vocabulary breaks exactly when it travels. The admitted-terms-only constraint is checkable against the document's ladder state (§8.2). Serves P4.

**Compliant:** An incident timeline uses "request router," "database connection pool," and "rollback." All labels are assumed or admitted before the figure. The caption states: "Figure 3: Error rate recovered only after the router rollback. Increasing the connection pool did not change the error rate."
**Non-compliant:** The same timeline labeled only with internal codenames and unexplained alert abbreviations.

**Cross-references:** §2.3, §6.4, §8.2

## 5.6 Evidential strength and authority

This section is the single source of phrases used to signal evidential strength or decision authority. §3.9 (hedging) and §§7.3–7.4 (interpretation and extrapolation) defer to it. The mechanism is forked from the IPCC's calibrated uncertainty language and extended for design, decision, procedure, incident, and investigation documents. Grammatical changes that preserve the listed phrase are allowed.

Profile lifecycle fields are separate from this phrase table.

**Lifecycle values:** `proposed`, `accepted`, `superseded`, `mitigated`, `resolved`, `open`, and `closed`.

Lifecycle values describe an artifact or workflow state. Annex E or the document defines their allowed values. Lifecycle values do not express evidential strength. An unmarked declarative material claim has verified-tier force. Rule 5.6.2 requires that claim to meet the verified-tier standard.

| Phrase | Standard | Example use |
|---|---|---|
| **the record shows** / **verification confirms** / **we show** | Cited evidence, a stated verification, or a proof directly establishes the statement over its full stated scope. | "Verification confirms that restart preserves every accepted job in API v3 under the fault cases in Table 4." |
| **we observed** / **we find** | The document directly records the observation in a stated context. The observation does not claim a general fact beyond that context. | "We observed connection exhaustion on all three affected hosts between 09:14 and 09:22 UTC." |
| **the evidence indicates** / **this suggests** | The interpretation is consistent with the evidence, but material alternatives remain or no direct test separates them. | "The evidence indicates that connection exhaustion triggered the retries, but the traces do not identify why exhaustion began." |
| **we decided** / **this document requires** | The statement records an adopted choice or normative constraint. Its authority comes from decision or approval status, not from presenting the choice as an empirical fact. | "We decided to keep API v2 through 2027 because two clients cannot migrate this year." |
| **we propose** | The choice, design, or requirement is pending approval or implementation. | "We propose a versioned response envelope. Section 4 lists its compatibility invariant." |
| **we hypothesize** / **we speculate** | The statement goes beyond the available evidence. The statement appears only inside a marked speculation block where §7.3 applies. | "We hypothesize that a credential refresh caused the first burst of retries." |

**Unsupported modifiers:** any unsupported certainty or significance modifier, including "clearly," "obviously," "importantly," "dramatic," and "we believe."

#### Rule 5.6.1 — Strength and authority language comes from the table only
**Class:** mandatory · **Machine-checkable:** partial · **Source:** IPCC calibrated language (mechanism)
**Constructs:** claim
**Navigation:** target: sentence · chunks: claim, interpretation · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text, claim-ledger · writes: chunk-text
**Relations:** constrains 5.6.2; pairs-with 3.9.2

> A governed document **shall** use only §5.6 table phrases to signal evidential strength or decision authority.
>
> The document **shall not** use an unsupported modifier.

**Rationale:** With a closed vocabulary, the reader can distinguish verified behavior, observation, interpretation, adopted decision, proposal, and hypothesis. With an open vocabulary, every adverb is a negotiation. Intensifiers on top of table phrases smuggle strength the evidence or approval status never earned. Serves P6 and P7.

**Compliant:** "We propose a bounded queue. Verification confirms that the prototype meets the no-loss invariant in the fault cases in Table 4."
**Non-compliant:** "The obviously superior queue clearly guarantees that no jobs can be lost."

**Cross-references:** §3.9, Rule 5.6.2, §7.3

**Calibrated statements:** marked claims, decisions, proposals, and interpretations, plus unmarked declarative material claims at verified-tier force.

**Calibration basis:** the document's evidence and approval status.

#### Rule 5.6.2 — Strength matches the evidential standard
**Class:** mandatory · **Machine-checkable:** no · **Source:** IPCC calibrated language (mechanism)
**Constructs:** claim
**Navigation:** target: sentence · chunks: claim, interpretation · slots: any · layers: exact · context: document · rewrite: prohibited
**Resources:** reads: chunk-text, claim-ledger, evidence-ledger · writes: none
**Relations:** requires 5.6.1

> Each calibrated statement **shall** have strength matching the calibration basis.

**Rationale:** The table works only when the mapping is honest. "Verification confirms" backed by an unrun test violates calibration. "We decided" for an unapproved proposal also violates calibration. Both phrases belong to the permitted vocabulary. The subject-matter owner (§8.4) audits this mapping where that review tier applies. Serves P6.

**Compliant:** "We observed the timeout on all five replay runs. The evidence indicates that the dependency limit is involved. We did not vary that limit."
**Non-compliant:** "Verification confirms the dependency caused the timeout." Only correlation in five replay runs supports the claim.

**Cross-references:** Rule 5.6.1, Rule 7.4.1, §8.4

## 5.7 Statistical evidence for report profiles

Section 5.7 governs statistical admission and reporting. Its rules apply to `technical-report` and `research-paper` only. Section 1.5 places them in `spec/overlays/shared/report.md`, together with the bare and ladder-required concept sets.

Other profiles admit statistical concepts under §2.3.

## 5.8 Reproducibility and verification statements

Section 5.8 governs the plain-language checkability statement. Its rules apply to `technical-report` and `research-paper` only. Section 1.5 places them in `spec/overlays/shared/report.md`, together with the statement forms and their required elements.

## 5.9 Definitions of done compose without losing acceptance

Section 5.9 governs definition-of-done composition. Its rules apply to `epic`, `task`, and `subtask` only. Section 1.5 places those rules in the overlay directories:

- Rules shared by more than one work-item profile are in `spec/overlays/shared/work-item.md`.
- Rules scoped to one profile are in that profile's `rules.md`.

Annex C indexes every §5.7, §5.8, and §5.9 rule with its profile applicability and its file.

---

Annex F records traceability for every Part 5 rule, including the rules that §§5.7–5.9 place in overlay files. Machine-checkable and partial rules feed the §8.2 lint set.

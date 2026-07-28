# Part 5 — Technical exactness and evidence

Part 5 governs the exact layer of every governed document. That layer includes claims, decisions, requirements, interfaces, invariants, procedure controls, incident timelines, notation, equations, evidence, figures, statistics, reproducibility, and verification.

By §1.4, these rules override Parts 2–4 and 6 wherever they collide. A plain rendering traces to an exact statement (§5.1). Symbols use the same ladder as terms (§5.2). Equations receive plain readings (§5.3). Material exact items carry a complete evidence record (§5.4). Evidential strength and decision authority use calibrated language (§5.6).

Profile-specific exactness fields extend that shared record. They do not replace the shared record.

## 5.1 The exactness principle

Plain prose may simplify an explanation. Plain prose may never blur an exact statement. A simpler restatement remains a rendering of an exact statement elsewhere in the document. The reader can follow a link from the restatement to that exact statement.

#### Rule 5.1.1 — Simplification preserves exact meaning
**Class:** mandatory · **Machine-checkable:** no · **Source:** original

> A plain-language rendering **shall not** change the scope, status, strength, conditions, or required behavior of the exact statement it renders.

**Rationale:** The two-layer model (§1.2) fails silently when a simplified statement loses exact content. A decision may lose a trade-off. A procedure may lose a precondition. A result may widen its scope. The rendering reads well but is wrong. Serves P3.

**Compliant:** "The new queue protects checkout from traffic spikes (exact design constraints in §4.2)." Section 4.2 limits the statement to a stated load range. Section 4.2 also defines the latency and loss invariants.
**Non-compliant:** "The new queue prevents checkout failures" as the plain rendering of a design that only bounds overload behavior below 20,000 requests per second.

**Cross-references:** §1.2, Rule 5.6.2, Rule 7.4.1

**Simplified material items:** claims, decisions, requirements, conditions, and outcomes.

#### Rule 5.1.2 — Simplified statements trace to exact statements
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

> Every simplified rendering of a simplified material item **shall** explicitly reference the exact statement it renders.

**Rationale:** Traceability makes Rule 5.1.1 checkable. A reviewer compares the rendering against its target instead of searching for the target. Serves P3 and P7. A linter can flag simplified-claim markers without references. A human judges equivalence.

**Compliant:** "In plain terms: stop the rollout if verification fails (exact checks and rollback boundary in Procedure §6)."
**Non-compliant:** "In plain terms: stop if anything looks wrong." The statement has no pointer to the exact checks, threshold, or rollback boundary.

**Cross-references:** Rule 5.1.1, §4.6 (layering), §8.2

## 5.2 Notation

Notation is vocabulary. The §2.3 term ladder applies equally to symbols and terms. A small baseline set is free. Writers admit every other symbol by definition at first use. Each symbol means one thing throughout the document.

Annex B §B.2 is the sole normative **baseline notation set**. The baseline contains:

- Function application, variables, named constants, and subscripted indexing.
- Arithmetic, equality and approximation, inequalities, ranges, absolute value, percentages, and scientific notation.
- Summation over an explicit index, and product notation when accompanied by the reading Annex B requires.
- Logarithms, exponentials, factorial, and Big-O notation.
- Basic set notation, including membership, subset, union, intersection, the empty set, and set-builder notation with the reading Annex B requires.

The following notation is not baseline and therefore requires ladder admission:

- Matrix and vector notation and operations.
- Norms, gradients (∇), and derivatives.
- Expectation and probability operators (𝔼, Pr).
- Argmax, argmin, and distribution symbols (`~`).
- Tensor index conventions and any ML-community shorthand, including θ for parameters and ℒ for loss.

**Permitted symbol-definition vocabulary:** baseline notation, admitted symbols, and admitted terms.

#### Rule 5.2.1 — Define every non-baseline symbol at first use
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (mechanism from §2.3)

> A symbol outside the baseline notation set **shall** be defined in prose at or before first use.
>
> The definition **shall** use only the permitted symbol-definition vocabulary.

**Rationale:** A reader cannot expand an unknown symbol. Unlike an unknown word, the symbol cannot even be sounded out. The term ladder also applies to notation. Serves P4. A linter can flag symbols that appear before a defining sentence. A human judges definition quality.

**Compliant:** "Write θ for the model's parameters: the list of numbers that training adjusts. The loss L(θ) is a function. The function scores how badly the model with parameters θ performs on the training examples."
**Non-compliant:** "We minimize L(θ) by stochastic gradient descent." Neither L nor θ has been defined.

**Cross-references:** §2.3, Rule 5.2.2, Annex B §B.2

#### Rule 5.2.2 — One symbol, one meaning
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ASD-STE100 (adapted)

> A symbol **shall** have exactly one meaning within a document.
>
> A meaning **shall** be written with exactly one symbol.

**Rationale:** Symbol reuse forces the reader to track scope like a compiler tracks shadowed variables. The assumed reader may resolve the symbol incorrectly when it matters. Serves P2. Tooling can check the document's symbol table.

**Compliant:** α is the learning rate everywhere in the document. The significance level is written out or receives a different symbol at admission.
**Non-compliant:** α is the learning rate in §3 and the significance level in §5.

**Cross-references:** Rule 5.2.1, §2.1, §8.2

**Required notation-table fields:** every defined symbol, its meaning, and its admission section.

#### Rule 5.2.3 — Notation table above six symbols
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original

> A document defining more than six non-baseline symbols **shall** include a notation table.
>
> The table **shall** contain every required notation-table field.

**Rationale:** In-prose definitions scale to a handful of symbols. Beyond that number, the reader needs an index to recover a definition without rereading. The threshold of six is provisional for v0.2. Serves P4.

**Compliant:** A capacity report defining λ, μ, Q, W, C, U, and R includes a notation table before the first analysis section.
**Non-compliant:** The same report defines all seven symbols across nine pages of prose with no table.

**Cross-references:** Rule 5.2.1, §4.8

## 5.3 Equations in prose

An equation the reader cannot read aloud is an image, not a statement. Every displayed equation has a plain-language reading. Inline math remains simple enough to preserve its sentence.

**Required equation-reading content:** what the equation computes and why it appears at that point.

#### Rule 5.3.1 — Every displayed equation gets a plain-language reading
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

> Every displayed equation **shall** have an adjacent plain-language reading.
>
> The reading **shall** include all required equation-reading content.

**Rationale:** The assumed reader parses code fluently but may not know mathematical convention. The reading documents the equation. The reading also explains why the equation appears there. A reader may skip an unmotivated equation. Section 4.6 permits that skip only for bounded blocks, not load-bearing equations. Serves P3 and P4. A linter can flag displayed equations without adjacent readings. A human judges adequacy.

**Compliant:**

    L = (1/N) Σ_{i=1..N} (y_i − f(x_i))²

"This is the model's average error on the training data. For each of the N training examples, subtract the model's prediction f(x_i) from the correct answer y_i. Square each difference, so overshooting and undershooting both count as error. Then average the squared differences across all examples. Training, defined in §2, searches for parameters that make this number small. The rest of this section measures how that search behaves."

**Non-compliant:** The same displayed equation is followed directly by "Optimization proceeds by stochastic gradient descent." No reading explains what L measures or why L matters here.

**Cross-references:** Rule 5.2.1, §4.6, §6.2

**Atomic inline forms:** single symbols, function applications, and single binary relations.

**Display-required forms:** expressions containing a summation, product, fraction, or nested subexpression.

#### Rule 5.3.2 — Keep inline math atomic
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

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

The citation-integrity rules in this section apply in every profile. Fabricated-but-plausible references are a realistic failure mode in any machine-generated draft.

**Complete evidence-record fields:** the six shared fields and every applicable profile-specific field defined in §5.4.

#### Rule 5.4.1 — Material statements carry a complete evidence record
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; IEC 82079-1; APA JARS / NeurIPS checklist (research adaptation)

> Every material exact item listed in §5.4 **shall** carry the complete evidence record.
>
> The item, immediate context, or explicit links **shall** supply every field.

**Rationale:** An incomplete exact item cannot be checked, reproduced, implemented, or compared. Context, alternatives, evidence, strength, uncertainty, and status make the item complete. Profile fields make each profile's exact items complete. Serves P6.

**Compliant:** "For API v3, we replayed 12,000 requests/s. Verification confirms the proposed bounded queue keeps p99 latency below the existing 450 ms objective. The current implementation reached 710 ms. The proposed build reached 398–421 ms across five runs. Section 3 defines interface changes and the no-loss invariant. Section 6 links the harness and traces. The measured range reports run-to-run uncertainty. The design is proposed, not approved."
**Non-compliant:** "The new queue fixes latency." The statement has no version, load context, baseline, evidence, invariant, evidential strength, uncertainty, or proposal status.

**Cross-references:** Rule 5.4.2, Rule 5.6.2, §§5.7–5.8

**Required change context:** base values and an absolute-or-relative marker.

#### Rule 5.4.2 — No naked percentages
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; APA JARS (effect size + uncertainty, restated)

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

> Every citation **shall** pass every applicable citation-resolution check.

**Rationale:** A valid-looking DOI that resolves elsewhere and a dead, unarchived link are hallucination signals, not ordinary link rot. Mechanical resolution checks run in §8.2. Serves P6.

**Compliant:** "RFC 9110, *HTTP Semantics*, https://www.rfc-editor.org/rfc/rfc9110.html." The URL resolves to that RFC.
**Non-compliant:** A citation whose DOI resolves to an unrelated article, or whose URL does not resolve and has no archived copy.

**Cross-references:** Rule 5.4.4, §8.2

#### Rule 5.4.4 — Cited sources support the claim
**Class:** mandatory · **Machine-checkable:** no · **Source:** Wikipedia "Signs of AI writing" (citations)

> The cited page or section **shall** state or directly support the claim it is cited for.

**Rationale:** Resolution (Rule 5.4.3) is necessary but insufficient. A real source may not support the claim for which it is cited. An unsupported citation is the harder-to-catch half of citation fabrication. The subject-matter-owner review (§8.4) checks support where that review tier applies.

**Compliant:** Citing API contract §3.2 for "clients may retry this operation safely" when §3.2 specifies idempotent retry behavior.
**Non-compliant:** Citing an architecture overview for a retry guarantee it never states.

**Cross-references:** Rule 5.4.3, §8.4

#### Rule 5.4.5 — Source counts are accurate
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing" (source-count inflation)

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

> Every quantitative figure **shall** include every quantitative figure label.

**Rationale:** An unlabeled axis makes the figure unfalsifiable. A hidden logarithmic scale makes the figure misleading. Serves P6.

**Compliant:** X axis "request rate (requests/s)," Y axis "p99 latency (ms)," legend naming the current and proposed queue, caption noting the log-scaled X axis.
**Non-compliant:** A curve labeled "performance" over an unlabeled X axis.

**Cross-references:** Rule 5.5.2, §6.4

**Caption-supported items:** claims, decisions, and operational outcomes.

#### Rule 5.5.2 — The caption states the takeaway
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514; Nature-style figure guidance

> A figure or table caption **shall** state the caption-supported item the artifact supports.
>
> The caption **shall not** state only what the artifact depicts.

**Rationale:** Readers, especially skimming readers, read captions before body text. "Latency by load" only describes the artifact. "The proposed queue meets the latency invariant through 12,000 requests/s" informs the reader. Rule 5.5.2 applies §4.5's informative-heading rule to captions. Serves P5.

**Compliant:** "Figure 3: The proposed queue meets the 450 ms p99 invariant through 12,000 requests/s. Each point is the median of five replays. Bars show minimum and maximum."
**Non-compliant:** "Figure 3: Queue latency."

**Cross-references:** §4.5, Rule 5.5.3

**Figure text locations:** a figure, its caption, and its legend.

#### Rule 5.5.3 — Figures stand alone for the assumed reader
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

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

> Each calibrated statement **shall** have strength matching the calibration basis.

**Rationale:** The table works only when the mapping is honest. "Verification confirms" backed by an unrun test violates calibration. "We decided" for an unapproved proposal also violates calibration. Both phrases belong to the permitted vocabulary. The subject-matter owner (§8.4) audits this mapping where that review tier applies. Serves P6.

**Compliant:** "We observed the timeout on all five replay runs. The evidence indicates that the dependency limit is involved. We did not vary that limit."
**Non-compliant:** "Verification confirms the dependency caused the timeout." Only correlation in five replay runs supports the claim.

**Cross-references:** Rule 5.6.1, Rule 7.4.1, §8.4

## 5.7 Statistical evidence for research profiles

For technical reports and research papers, the assumed reader has only the profile's baseline probability knowledge unless the document admits more. Statistical concepts therefore split into a bare set and a ladder-required set. Rule 5.7.1 governs admission of the ladder-required set.

**Bare** (usable without definition): count, minimum, maximum, range, mean/average, median, percentage, ratio, percentile (engineers use p50/p99 daily).

**Ladder-required** (admit per §2.3 before use):

- Standard deviation, variance, and standard error.
- Confidence interval, p-value, and statistical significance.
- Any named distribution, including "normal" and "power law."
- Correlation, regression, and effect size.
- Every hypothesis-testing concept.

**Admission-controlled statistical uses:** ladder-required concepts and "significant" in its statistical sense.

#### Rule 5.7.1 — Admit ladder-required statistical concepts before use
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (mechanism from §2.3)
**Profiles:** technical-report, research-paper

> An admission-controlled statistical use **shall not** appear before §2.3 admission.
>
> Admission of "significant" **shall** include its underlying test.

**Rationale:** "Significant" is the sharpest trap in the set. The assumed reader hears "large." The writer means "unlikely under a null hypothesis the reader has never met." Serves P2 and P4.

**Compliant:** "The gap (4.2 points) is larger than the seed-to-seed spread of either model (at most 0.8 points across 5 runs)."
**Non-compliant:** "The improvement is statistically significant (p < 0.05)" in a document that never admits p-values.

**Cross-references:** §2.3, §0.3.2, Rule 5.7.2

**Headline formulation:** a statement of the result using only bare statistical concepts.

#### Rule 5.7.2 — Headline statistical results use bare concepts
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Profiles:** technical-report, research-paper

> Every headline statistical result **shall** include the headline formulation.
>
> Ladder-required formulations **may** accompany that formulation but **shall not** replace it.

**Rationale:** The two-layer model also applies to statistics. The exact formulation remains available to the expert. The assumed reader receives the finding in familiar vocabulary. Serves P3 and P4.

**Compliant:** "Across 5 runs, the fine-tuned model beat the baseline every time, by 3.9 to 4.6 points (mean 4.2). A paired t-test, defined below, gives p = 0.003."
**Non-compliant:** "The fine-tuned model outperformed the baseline (paired t-test, p = 0.003)" as the only statement of the result.

**Cross-references:** Rule 5.4.1, §1.2

## 5.8 Reproducibility and verification statements

Technical reports and research papers carry a plain-language statement that tells the assumed reader how another person can check the reported work. The profile and subject determine which form applies:

- A `research-paper` uses a **reproducibility statement**. The statement identifies what another person needs to repeat the work. The reproducibility statement covers data or materials, code or procedure, compute or other resources, and key settings. The statement also identifies any unavailable input or component.
- A `technical-report` uses **reproducibility** when another reader can repeat the reported method. The report uses **verification** when it assesses a system or artifact. The report uses both when both promises matter. A verification statement identifies the artifact and version, inputs and environment, checks or procedure, and pass criteria. The statement also identifies unavailable input or access needed to run those checks.

The statement summarizes the check in the main document. A technical appendix may carry command-level, configuration-level, or instrument-level detail, but does not replace the statement.

**Applicable statement elements:** every element §5.8 lists for the profile, subject, and selected statement form.

#### Rule 5.8.1 — Reports include the applicable checkability statement
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS checklist / ML Reproducibility Checklist (research adaptation)
**Profiles:** technical-report, research-paper

> A technical report or research paper **shall** include its applicable checkability statement.
>
> The statement **shall** contain every applicable statement element.

**Rationale:** A claim that cannot be repeated or independently checked remains dependent on the authors' environment and access. The profile-specific form makes checkability explicit without forcing an experiment-oriented statement onto a system report. Serves P6.

**Compliant:** A system report's "Verification" section names the tested build, replay input, environment, commands, pass thresholds, and access gap. A research paper's "Reproducing this work" section covers data, code or procedure, resources, key settings, and gaps.
**Non-compliant:** A system report says only "tests passed," or a research paper scatters settings across footnotes without stating data availability or required resources.

**Cross-references:** Rule 5.4.1, §4.4, §8.2

**Required statement content:** every element required by §5.8.

#### Rule 5.8.2 — The statement reads in assumed-reader vocabulary
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Profiles:** technical-report, research-paper

> The §5.8 statement **shall** use only assumed or previously admitted terms.
>
> The statement **shall not** delegate required statement content entirely to a technical appendix or external artifact.

**Rationale:** The assumed reader uses the statement to assess independent checking. A pointer where an answer should appear defeats the section. An appendix or linked harness extends the statement. The appendix or harness does not replace the statement. Serves P3 and P4.

**Compliant:** "Reproducing this work: We trained on the public C4 text dataset, about 750 GB, available from its maintainers. Training code and configurations are in our internal repository `forge/plateau-study`. The reported runs used 64 H100 GPUs for roughly 9 days total across all experiments. The most important settings are the 0.001 learning rate and the data order. Appendix B gives the learning-rate schedule. We fix data order with the seeds in Table 5. The evaluation questions are private. A reproducer would need to substitute a comparable question set. Appendix C describes how we built our question set."
**Non-compliant:** "See Appendix B for hyperparameters and infrastructure details."

**Cross-references:** Rule 5.8.1, §2.3, §4.6

---

Annex F records traceability for every rule above. Machine-checkable and partial rules feed the §8.2 lint set.

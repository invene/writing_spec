# Report overlay module

**ITWS version:** 0.8.0-draft · **Status:** normative

**Family:** report · **Profiles:** `technical-report`, `research-paper`

This module holds the rules that both report profiles share. Rules scoped to one profile alone are in that profile's `rules.md`.

## Rules from §5.7 — statistical evidence

For technical reports and research papers, the reader has only Annex B's basic quantitative knowledge unless the document admits more. Statistical concepts therefore split into a bare set and a ladder-required set. Rule 5.7.1 governs admission of the ladder-required set.

**Bare** (usable without definition): count, minimum, maximum, range, mean or average, median, percentage, ratio, and rate.

**Ladder-required** (admit per §2.3 before use):

- Mode and percentiles, including p50 and p99.
- Standard deviation, variance, and standard error.
- Confidence interval, p-value, and statistical significance.
- Any named distribution, including "normal" and "power law."
- Correlation, regression, and effect size.
- Formal probability, expected value, sampling error, and statistical power.
- Every hypothesis-testing concept.

**Admission-controlled statistical uses:** ladder-required concepts and "significant" in its statistical sense.

#### Rule 5.7.1 — Admit ladder-required statistical concepts before use
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (mechanism from §2.3)
**Profiles:** technical-report, research-paper
**Constructs:** statistic
**Navigation:** target: term · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, term-ledger · writes: chunk-text, term-ledger
**Relations:** requires 2.3.1

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
**Constructs:** statistic
**Navigation:** target: sentence · chunks: any · slots: any · layers: both · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 5.7.1

> Every headline statistical result **shall** include the headline formulation.
>
> Ladder-required formulations **may** accompany that formulation but **shall not** replace it.

**Rationale:** The two-layer model also applies to statistics. The exact formulation remains available to the expert. The assumed reader receives the finding in familiar vocabulary. Serves P3 and P4.

**Compliant:** "Across 5 runs, the fine-tuned model beat the baseline every time, by 3.9 to 4.6 points (mean 4.2). Using the paired t-test and p-value defined in §3, p = 0.003."
**Non-compliant:** "The fine-tuned model outperformed the baseline (paired t-test, p = 0.003)" as the only statement of the result.

**Cross-references:** Rule 5.4.1, §1.2

## Rules from §5.8 — reproducibility and verification statements

Technical reports and research papers carry a plain-language statement that tells the assumed reader how another person can check the reported work. The profile and subject determine which form applies:

- A `research-paper` uses a **reproducibility statement**. The statement identifies what another person needs to repeat the work. The reproducibility statement covers data or materials, code or procedure, compute or other resources, and key settings. The statement also identifies any unavailable input or component.
- A `technical-report` uses **reproducibility** when another reader can repeat the reported method. The report uses **verification** when it assesses a system or artifact. The report uses both when both promises matter. A verification statement identifies the artifact and version, inputs and environment, checks or procedure, and pass criteria. The statement also identifies unavailable input or access needed to run those checks.

The statement summarizes the check in the main document. A technical appendix may carry command-level, configuration-level, or instrument-level detail, but does not replace the statement.

**Applicable statement elements:** every element §5.8 lists for the profile, subject, and selected statement form.

#### Rule 5.8.1 — Reports include the applicable checkability statement
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS checklist / ML Reproducibility Checklist (research adaptation)
**Profiles:** technical-report, research-paper
**Constructs:** section
**Navigation:** target: document · chunks: any · slots: Reproducibility or verification · layers: exact · context: document · rewrite: candidate
**Resources:** reads: chunk-text, skeleton-order · writes: chunk-text
**Relations:** requires 4.3.3

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
**Constructs:** section
**Navigation:** target: section · chunks: any · slots: Reproducibility or verification · layers: plain · context: document · rewrite: review
**Resources:** reads: chunk-text, term-ledger · writes: chunk-text
**Relations:** requires 5.8.1

> The §5.8 statement **shall** use only assumed or previously admitted terms.
>
> The statement **shall not** delegate required statement content entirely to a technical appendix or external artifact.

**Rationale:** The assumed reader uses the statement to assess independent checking. A pointer where an answer should appear defeats the section. An appendix or linked harness extends the statement. The appendix or harness does not replace the statement. Serves P3 and P4.

**Compliant:** "Reproducing this work: We trained on the public C4 text dataset, about 750 GB, available from its maintainers. Training code and configurations are in our internal repository `forge/plateau-study`. The reported runs used 64 H100 GPUs for roughly 9 days total across all experiments. The most important settings are the 0.001 learning rate and the data order. Appendix B gives the learning-rate schedule. We fix data order with the seeds in Table 5. The evaluation questions are private. A reproducer would need to substitute a comparable question set. Appendix C describes how we built our question set."
**Non-compliant:** "See Appendix B for hyperparameters and infrastructure details."

**Cross-references:** Rule 5.8.1, §2.3, §4.6

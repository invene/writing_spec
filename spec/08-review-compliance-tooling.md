# Part 8 — Review, compliance, and tooling

Part 8 defines practical checks for ITWS conformance. Section 8.1 defines the generated profile checklist and scan test. Section 8.2 defines automated checks and the author self-check. Section 8.3 defines publication reader testing and release checks. Section 8.4 defines reviewed-tier roles. Section 8.5 defines waivers. Section 8.6 defines the generated artifacts and the states a validation run may report. Section 8.7 gates machine-proposed comments and keeps its rules in the `maintenance-comment` overlay (§1.5).

Parts 2–7 define a conforming document. Part 8 defines how anyone verifies conformance.

Every governed document declares one canonical profile ID and one conformance tier. Rules apply to all profiles by default. A rule carrying `**Profiles:**` applies only when the declared profile appears in that list.

The minimum tier for each profile is:

- **Core:** `decision-record`, `explanation`, `investigation-log`, `task`, `subtask`, `maintenance-comment`.
- **Reviewed:** `design-rfc`, `procedure`, `incident`, `technical-report`, `epic`.
- **Publication:** `research-paper`.

A document may target a higher tier than its profile minimum. A document may not target a lower tier.

- **Core** requires every applicable mandatory rule, a version- and profile-pinned lint run, and a documented author self-check.
- **Reviewed** includes core and adds independent review by a subject-matter owner and a reader proxy.
- **Publication** includes reviewed and adds an independent reader test plus release checks.

## 8.1 Conformance checklist

The conformance checklist is a build artifact. Annex C rule metadata generates the checklist for the declared specification version, profile, and tier. Default rules enter the checklist. Rules also enter when their `Profiles` metadata includes the declared profile. Rules narrowed to other profiles do not enter.

**Checklist-generation inputs:** Annex C rule metadata and the document's declared specification version, profile, and tier.

#### Rule 8.1.1 — Checklist is generated, not authored
**Class:** mandatory · **Machine-checkable:** yes · **Source:** STE checker workflows
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** constrains 8.1.3

> The conformance checklist **shall** be generated from every checklist-generation input.
>
> The checklist **shall not** be edited by hand.

**Rationale:** A hand-maintained checklist diverges from the rules the first time a rule changes (P7). Generation makes the checklist correct by construction.

**Compliant:** The checklist header records ITWS 0.8.0-draft, profile `procedure`, tier `reviewed`, and the Annex C revision from which it was generated.
**Non-compliant:** A reviewer copies the `research-paper` checklist, deletes statistics by hand, and calls the result a procedure checklist.

**Cross-references:** Annex C; Rule 8.1.3.

**Self-check passes:**

- Vocabulary.
- Sentence.
- Structure and explanation.
- Technical exactness and evidence.

#### Rule 8.1.2 — Four self-check passes
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.1.1

> Before recording conformance at any tier, the author **shall** complete the generated checklist.
>
> The author **shall** use every self-check pass, filtered for the profile.

**Rationale:** Core still requires substantive human checking. Lint alone cannot judge operational definitions, coherent structure, exact interfaces, or evidence quality. Four passes with one concern each keep that check usable (P7). Reviewed and publication tiers reuse the completed checklist instead of making reviewers rediscover basic defects.

**Compliant:** The author of a `decision-record` completes all four passes. The passes include the applicable alternatives, consequences, status, and boundary checks.
**Non-compliant:** "`itws-lint` passed, so self-check is complete." No author checked the partial and human-only rules.

**Cross-references:** Rule 8.2.4; §8.4 (reviewed tiers independently review both layers).

**Checklist-regeneration triggers:**

- A change to a rule's statement, class, status, or profile applicability.
- A change to conformance-tier obligations in §0.4.3 or Part 8.

#### Rule 8.1.3 — Regeneration on rule change
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** requires 8.1.1

> The checklist **shall** be regenerated after every checklist-regeneration trigger.

**Rationale:** Section 0.8 permits rules to change between versions. Profile and tier metadata also determine applicability. A stale checklist silently checks the wrong specification or document class.

**Compliant:** Adding `technical-report` to a rule's `Profiles` line triggers checklist regeneration before the specification release.
**Non-compliant:** A rule is reclassified recommended → mandatory and existing generated checklists still list it as optional.

**Cross-references:** §0.8; Annex C; Annex G.

### 8.1.1 Scan-test protocol

A scan test measures recall, not confidence. The test uses the selected profile's scan-test outcome and its defined scan path: the Rule 4.12.1 path for a Markdown document, or the Rule 4.13.9 path for a hosted comment set.

A **scan-test key** contains:

1. the expected purpose and main point;
2. the applicable status or strength, or `Not applicable` with a reason;
3. every material boundary needed to prevent widening;
4. links to the exact and body items that support each expected field; and
5. one strengthened foil for each protected status, strength, or material boundary.

A **strengthened foil** is a plausible paraphrase that raises authority or evidential strength, widens scope, or removes a material boundary.

A **scan-test record** contains the role and profile, document and scan-path hashes, key hash, linked-source hashes, intervening task and elapsed interval, generated response, foil responses, result, and findings.

The scan-test procedure has six steps:

1. Prepare the key before the test. At `reviewed` and `publication`, the subject-matter owner approves it before the proxy or participant sees it.
2. Let the reader view the complete scan path once without taking notes.
3. Close the document. Complete a preselected source-independent task that occupies attention without using the document's subject.
4. Generate the profile's scan-test outcome from memory without viewing the key or foils.
5. Present each foil and record whether the reader accepts or rejects it.
6. Compare the response with the approved key and record each mismatch.

The protocol uses an intervening task rather than an invented time threshold. Thiede, Anderson, and Therriault delayed keyword generation until participants had read all six texts. Their procedure fixed no elapsed-time threshold. ITWS adapts that ordering and records its task and elapsed interval for later calibration.

A scan response passes when it states every required key field, rejects every foil, invents nothing, and reports absent information as missing.

#### Rule 8.1.4 — Complete the scan test
**Class:** mandatory · **Machine-checkable:** no · **Source:** Thiede, Anderson, and Therriault 2003; Glenberg, Wilkinson, and Epstein 1982; Duggan and Payne 2009; original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record, exact-item-ledger · writes: conformance-record
**Relations:** requires 8.1.2; validates 4.12.2; pairs-with 8.4.3

> Before recording conformance at any tier, the author **shall** prepare a scan-test key and complete the scan-test procedure. The scan-test record **shall** contain every required field. The response **shall** pass.

**Rationale:** Immediate self-reports overstate comprehension. Closed-document generation exposes what the scan path actually left in memory. The exact-layer key and strengthened foils test both failure directions: omission and widening. Core receives an author check; higher tiers repeat the protocol independently (P4, P7).

**Compliant:** An author closes a decision record after scanning it, completes the preselected task, recalls the proposed decision and scope, and rejects the foil that calls it approved.
**Non-compliant:** The author rereads each heading while checking "clear" boxes. No generated response, key, foil result, or delayed recall exists.

**Cross-references:** Rules 4.12.1–4.12.4, 8.3.3, 8.4.2, 8.4.3

#### Rule 8.1.5 — Retest after a dependent change
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record, heading, chunk-text, exact-item-ledger · writes: conformance-record
**Relations:** requires 8.1.4; pairs-with 8.1.3

> A scan-test key and record **shall** become stale after a change to the title, a heading, an opening sentence, or a linked source item. A stale scan-test record **shall not** support conformance.

**Rationale:** A smoothing edit can change the scan model or its relation to the body. Hashes detect changes to recorded dependencies. A reader confirms that the key links every source item it summarizes (P3, P7).

**Compliant:** An editor changes the Summary opener. The author rebuilds the path, updates the key, and repeats the scan test.
**Non-compliant:** A title changes "proposed" to "approved." The release keeps the earlier passing scan record.

**Cross-references:** Rules 8.1.3, 8.1.4, 8.6.1

## 8.2 Automated checks

`itws-lint` is the conformance linter. The linter is a repository-local engine that uses only the Python standard library. Its checks are generated from this specification. A reader who can clone the repository and run Python can run the complete lint gate, with no installed binary, downloaded style package, or network access. The linter reports readability metrics, including Flesch-Kincaid. Readability metrics do not gate conformance.

The word-use, punctuation, and usage adjudications that Parts 2–3 adapted from the Google Developer Style Guide and the Microsoft Writing Style Guide are stated in those parts. Annex F records the adaptation. The linter reads those adjudications from the phrase-list paragraphs below, not from an external package.

### 8.2.1 Check inventory (informative)

**Phrase-list paragraph form.** A phrase-list paragraph declares one machine-readable list and is the linter's only word- and phrase-level input. The paragraph has this form:

```text
**Phrase list <rule ID> — <label> (<kind>[, case-sensitive]):** "<item>" (<note>); "<item>"; …
```

The kind is `word`, `phrase`, `opener`, or `pattern`. A `word` item matches on word boundaries. A `phrase` item matches a literal span. An `opener` item matches only at the start of a sentence. A `pattern` item is a regular expression. A parenthesized note states an exclusion that a reader applies; the generated finding repeats the note. A rule that names a covered item resolves it against the phrase-list paragraph carrying that rule's ID. The list is the versioned living artifact of §2.5 and §0.8; it has exactly one home in this specification.

Custom rules for original mechanisms:

- **Profile applicability** — the declared canonical profile selects default rules plus matching `Profiles` rules. Unknown profile IDs are errors.
- **Ladder ordering** — every term on the Annex B not-assumed list (or in Annex A) that appears before its definition chunk is flagged (§2.3).
- **Undefined-term detection** — terms in neither Annex B's assumed lists nor the document's admitted set are flagged (§2.3, §0.3.3).
- **One symbol, one meaning** — a symbol bound twice in one document is flagged (§5.2).
- **Profile exactness fields** — candidates for missing interfaces, invariants, procedure controls, incident evidence, research reproducibility, work-item paths, DoD conditions, and parent links are flagged (§5.4).

Each phrase-list rule keeps its list beside its own rule, in the paragraph form above. The rules that carry a list are:

| Rule | List |
|---|---|
| 2.1.3 | plain-verb replacements |
| 2.6.3 | unearned superlatives |
| 2.6.4 | the prohibited-word list |
| 2.6.5 | agency verbs |
| 2.6.6 | warpath markers |
| 2.6.7 | editorializing asides |
| 2.6.8 | vague-authority phrases |
| 2.6.9 | gap-speculation phrases |
| 2.6.10 | formulaic connectives |
| 2.6.11 | conversational artifacts, unfilled placeholders, and tool-leakage patterns |
| 3.6.2 | bare openers |
| 3.9.1 | vague hedges |
| 3.10.2 | contrast-reframe templates |
| 3.10.4 | trailing significance participles |
| 3.10.6 | inflated copula substitutes |
| 4.10.5 | emoji ranges |
| 6.5.4 | hollow-summary openers |

The Rule 2.6.11 patterns are near-definitive signals of unreviewed machine-generated text. They cover tool leakage, referrer leakage, and unfilled template placeholders, and they carry the error severity of their mandatory rule.

Citation-integrity checks (§5.4) need network access. Section 8.2.3 separates them from offline checks:

- Every DOI resolves, and resolves to the cited work.
- No dead links without an archived copy (a dead link with no archive is treated as a fabrication signal, not ordinary link rot).
- No placeholder access dates.

A skipped network check leaves validation incomplete. Section 8.6 gives that outcome its own state; a skipped check never reports as a pass.

### 8.2.2 Linter behavior

**Lint-gate outcomes:**

- Zero error-severity findings from a version- and profile-pinned `itws-lint` run.
- An ITWS waiver (§8.5) for each remaining error.

#### Rule 8.2.1 — Lint gate
**Class:** mandatory · **Machine-checkable:** yes · **Source:** STE checker practice
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.2.3; pairs-with 8.5.1

> Before recording conformance at any tier, a governed document **shall** satisfy one lint-gate outcome.

**Rationale:** Machine-checkable violations are the cheapest to find and the most embarrassing to ship. The lint gate is part of core, so short-lived documents receive it even when their minimum tier has no independent reviewers.

**Compliant:** A core `investigation-log` links a clean `itws-lint` run pinned to ITWS 0.8.0-draft and profile `investigation-log`.
**Non-compliant:** "The linter is noisy. Readers can ignore the linter." Errors remain for review or release.

**Cross-references:** Rule 8.2.2; Rule 8.5.1.

**Severity map:**

- Mandatory rule: error.
- Recommended rule: warning.
- Permitted-practice hint: suggestion.

#### Rule 8.2.2 — Severity maps to rule class
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** validates 8.2.1

> Each automated check **shall** carry the severity assigned by the severity map.

**Rationale:** Section 0.4.2's three classes lose meaning when tooling flattens them. A blocking warning teaches writers to ignore severity. A nonblocking error does the same.

**Compliant:** The §3.10 copula-avoidance check enforces a mandatory rule and reports an error. A recommended density-budget heuristic reports a warning.
**Non-compliant:** All custom checks report warnings "to be safe."

**Cross-references:** §0.4.2.

**Version-pinned check inputs:**

- The document's declared specification version and canonical profile.
- The declared version's Annex A, Annex B, rule applicability, and phrase lists.

#### Rule 8.2.3 — Version-pinned checking
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** declaration
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: declaration-block, conformance-record · writes: none
**Relations:** requires 4.3.1

> Tooling **shall** use every version-pinned check input when checking a document.

**Rationale:** Sections 0.4.4 and 0.8 guarantee checking against the cited version. Profile applicability decides which rules enter that check. A linter that always runs the latest lists or guesses a profile breaks both guarantees.

**Compliant:** `itws-lint --spec 0.8.0-draft --profile design-rfc queue-design.md` loads the 0.8.0-draft lists and the `design-rfc` rule set.
**Non-compliant:** A 0.8.0-draft `procedure` is checked against the latest lists and the `research-paper` profile inferred from its references section.

**Cross-references:** §0.4.4; §0.8.

**Human gates:** the §8.1 author self-check and every reviewer, reader-test, or release gate required by the declared tier.

#### Rule 8.2.4 — Machine checks do not close human gates
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** constrains 8.2.1

> A clean automated run **shall not** complete a human gate.

**Rationale:** Most mandatory rules are `partial` or `no` on machine-checkability. The linter finds phrase-list and ordering violations. The linter does not find every blurred interface, unsafe rollback, unsupported causal claim, or misleading explanation. Treating lint as human verification is the failure mode P7 prevents.

**Compliant:** Lint passes. The author still completes all four self-check passes. A reviewed-tier procedure then receives both required independent reviews.
**Non-compliant:** "CI is green, ship it." No self-check is recorded.

**Cross-references:** §8.4; Rule 8.1.2.

## 8.3 Publication reader test and release checks

The independent reader test is the assumed-reader half of §1.2's dual acceptance test. The test adapts plain-language teach-back testing and ISO/IEC/IEEE 26514 documentation-evaluation guidance. The publication tier requires the test. Other tiers do not require the test. A document may target publication above its profile's minimum. The test then measures that profile's primary outcome. Each overlay `README.md` states the reader-test outcome for its profile (§1.5).

Publication release checks confirm:

1. specification version, canonical profile, tier, and conformance statement are final and consistent;
2. the generated checklist, pinned lint output, and every waiver are current and linked;
3. both reviewed-tier approvals are complete;
4. citations, internal links, figures, tables, alt text, and referenced artifacts resolve in the release form;
5. profile-required deliverables, including reproducibility material where applicable, are accessible or their access limits are stated; and
6. the independent reader-test record includes the scan phase, full-read phase, participant criteria, outcomes, and any revisions.

> **Drafting note (STY-52):** the profile-specific pass/fail tasks remain provisional until the protocol has been piloted and recorded for each profile that targets publication.

**Publication gate elements:** the independent reader test and every release check listed in §8.3.

#### Rule 8.3.1 — Publication gate
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514 / plain-language testing practice
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.3.3

> Before recording its conformance statement, a publication-tier document **shall** pass every publication gate element.

**Rationale:** Publication claims both independent comprehension and release readiness. The reader test catches a plain layer that changes the primary outcome. Release checks catch a correct draft with stale metadata, broken evidence, inaccessible artifacts, or missing approvals.

**Compliant:** A `research-paper` release record includes reviewed-tier approvals and a new independent participant's successful result teach-back. The record also includes resolved citations and artifacts. The checklist was generated for ITWS 0.8.0-draft.
**Non-compliant:** "The reader-proxy reviewer said it reads fine." The proxy is not an independent test participant. No release checks are recorded.

**Cross-references:** §1.2; §8.4; Rule 8.3.2.

**Participant baseline:** the declared profile's assumed-reader baseline.

**Disqualified participants:** authors, subject-matter owner reviewers, reader-proxy reviewers, contributors to the work, and prior readers of any draft.

#### Rule 8.3.2 — Participant sampling
**Class:** mandatory · **Machine-checkable:** no · **Source:** plain-language testing practice
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.3.1

> The test participant **shall** match the participant baseline.
>
> The participant **shall not** be a disqualified participant.

**Rationale:** The test measures what the document teaches, not what the participant already knew or absorbed in drafting, review, or project discussion. Subject expertise above the baseline can silently fill the same gaps. Contaminated or overqualified participants pass documents that fail real readers.

**Compliant:** A quality assurance specialist from an unrelated pod matches the `procedure` baseline. They have never seen the system change. They use the final procedure to walk through the task.
**Non-compliant:** The reader-proxy reviewer, who has read three drafts, is the test participant.

**Cross-references:** §0.3; Annex B; Rule 8.4.3.

**Publication test phases:** first complete the §8.1.1 scan-test procedure. Record the scan response and foil decisions before opening the full document. Then read the full document once, unassisted and at the participant's pace. Produce the reader-test outcome stated in the declared profile's overlay.

**Passing response:**

- Preserves the primary outcome's applicable context, status or strength, and boundaries.
- Invents no fact, mechanism, step, decision, cause, or result.

#### Rule 8.3.3 — Protocol and pass criteria
**Class:** mandatory · **Machine-checkable:** no · **Source:** teach-back method, adapted
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.3.1; requires 8.1.4

> The participant **shall** complete the scan phase before reading the full document.
>
> The document **shall** pass only when the participant produces a passing scan response and a passing full-read response.

**Rationale:** The scan phase tests the shallow model before full text can repair it. A universal research-result test would not measure every profile's primary outcome. Such a test would miss procedure execution, decision recovery, and safe incident interpretation. The profile tasks tie both phases to the document's job. The tasks retain two common failure directions: boundary creep (§7.4) and status or strength creep (§5.6).

**Compliant:** For a procedure, the participant waits until replica lag is below 2 seconds. The participant performs the verification query. When the query fails, the participant chooses rollback R1.
**Non-compliant:** The participant can summarize why the maintenance matters but skips the precondition and invents a restart as rollback.

**Cross-references:** §5.6; §7.4; §8.3 drafting note.

#### Rule 8.3.4 — Reader-test failures are recorded
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** requires 8.3.3

> A failed reader-test record **shall** state what the participant misstated or could not do.

**Rationale:** The misstatement or failed action is the finding: it points at the section that failed to teach and gives the revision a testable target.

**Compliant:** "Participant omitted the point of no return in step 6 and chose rollback after step 8."
**Non-compliant:** "Reader test failed." The record states no misstatement or failed action.

**Cross-references:** Rule 8.3.5.

#### Rule 8.3.5 — Failed documents are revised and independently retested
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.3.4

> A publication-tier document that fails a reader test **shall** be revised.
>
> Before recording conformance, the document **shall** pass a retest with a new qualified participant.

**Rationale:** Revision closes the recorded comprehension gap. A new participant tests the document, not the first participant's memory of the session.

**Compliant:** A participant misses a rollback boundary. The author moves the boundary next to the affected step. A second qualified participant tests and passes the revision.
**Non-compliant:** The same participant rereads the revised draft and supplies the answer discussed after the first test.

**Cross-references:** Rule 8.3.2, Rule 8.3.4; §8.5 (an ITWS waiver may cover retest sampling when no untainted participant exists, with justification).

## 8.4 Reviewer roles

Reviewed and publication tiers assign §1.2's two layers to independent people. Core documents do not require these reviewers unless they target reviewed or publication. The **subject-matter owner** is accountable for correctness in the relevant system or domain. The **reader proxy** reviews from the declared profile's assumed-reader baseline. The proxy may hold any pod role if they match that baseline. Neither reviewer may be an author.

**Required review roles:**

- An independent subject-matter owner for the exact layer.
- An independent reader proxy for the plain layer.

#### Rule 8.4.1 — Reviewed tiers use two independent roles
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514 / IEC 82079-1 review process
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.1.2

> Every reviewed-tier or publication-tier document **shall** receive reviews from both required roles.
>
> One person **shall not** fill both roles for the same document.

**Rationale:** The two layers fail in opposite ways. The owner can fill gaps from domain knowledge, but the proxy cannot judge technical correctness. Splitting the roles runs both acceptance tests without imposing two reviewers on core-tier documents.

**Compliant:** A service owner signs a reviewed `design-rfc` for interfaces, invariants, evidence, and boundaries. A product designer from another pod signs for the plain layer.
**Non-compliant:** The RFC author reviews it "wearing both hats," or a core `decision-record` is rejected solely because it did not recruit two reviewers.

**Cross-references:** §1.2; Rule 8.1.2 (pass assignment); Rule 8.3.2 (the proxy is not the test participant).

**Owner review scope:**

- Correctness of the exact layer.
- Traceability of simplified statements (§5.1).
- The complete evidence record, including lifecycle or authority status (§5.4).
- Calibration of evidential strength and decision authority (§5.6).
- Boundary coverage (Part 7).
- Accuracy and completeness of the scan-test key and strengthened foils (§8.1.1).

#### Rule 8.4.2 — Subject-matter-owner scope
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514, renamed to §1.2
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: exact · context: document · rewrite: prohibited
**Resources:** reads: conformance-record, exact-item-ledger · writes: none
**Relations:** requires 8.4.1; requires 8.1.4

> The subject-matter owner **shall** check every item in the owner review scope.

**Rationale:** These checks require knowing what the domain permits and what the evidence supports. Each overlay `README.md` gives its profile a concrete owner review focus, such as interfaces and invariants for a `design-rfc`, mechanism fidelity for an `explanation`, or integrated acceptance for a `task`. The focus narrows the owner's attention. The focus does not reduce the owner review scope above.

**Compliant:** The owner flags a procedure whose rollback step is unsafe after the schema migration even though the draft calls rollback available throughout.
**Non-compliant:** The owner copyedits sentence length and skips the interface invariant because "the proxy has the checklist."

**Cross-references:** Part 5; Part 7; Rule 8.1.2.

**Proxy review areas:** vocabulary, sentences, structure, and explanatory devices.

**Proxy blockers:** every term, symbol, transition, or missing explanation that prevents recovery of the profile's primary outcome.

#### Rule 8.4.3 — Assumed-reader proxy scope
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514, renamed to §1.2
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: plain · context: document · rewrite: prohibited
**Resources:** reads: conformance-record, term-ledger · writes: none
**Relations:** requires 8.4.1; requires 8.1.4

> Before the full plain-layer review, the reader proxy **shall** complete the scan-test procedure without viewing its key.
>
> The reader proxy **shall** check every proxy review area from the declared profile's assumed-reader baseline.
>
> The proxy **shall** flag every proxy blocker.

**Rationale:** The proxy's value is disciplined ignorance: they read as the declared Annex B baseline, not as themselves. Specialist knowledge cannot fill a scan-path gap. A proxy who fills gaps from project knowledge silently passes documents that fail the real reader.

**Compliant:** The proxy flags "quiesce L7" in a procedure because neither term is assumed or admitted. The state transition is required to execute the critical path.
**Non-compliant:** The proxy lets "fence the old primary" pass because the database team knows its meaning. The declared assumed reader does not know the phrase.

**Cross-references:** §0.3; Annex B; Rule 8.1.2.

#### Rule 8.4.4 — Findings cite rules
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** cross-reference
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** pairs-with 8.4.1

> Every required review finding **shall** cite the rule number it enforces.
>
> A finding without a citable rule **shall** be recorded as an opinion, not a required change.

**Rationale:** Rule plus violation is the complete enforcement model (P7, §1.3). The model ends arguments and reveals gaps. A recurring opinion without a citable rule is a candidate for the next specification version.

**Compliant:** "§3.10 violation: replace 'serves as the backbone of' with 'is'."
**Non-compliant:** "this section feels weak" with a requested rewrite and no rule.

**Cross-references:** §1.3; §0.8 (recurring opinions feed rule proposals); Annex G.

## 8.5 Waivers and deviations

The standard engineering deviation pattern applies. Mandatory rules bend only visibly, in writing, and with a named approver. ITWS waivers make exceptions explicit. Recurring waiver records provide evidence for changing a rule.

**Waiver prerequisites:**

- A recorded ITWS waiver for the mandatory-rule violation.
- Approval before recording the conformance statement.

#### Rule 8.5.1 — Deviation requires a recorded waiver
**Class:** mandatory · **Machine-checkable:** partial · **Source:** IEC 82079-1 / engineering-standard practice
**Constructs:** waiver
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: waiver-record · writes: none
**Relations:** constrains 8.5.2

> A governed document violating a mandatory rule **shall** satisfy every waiver prerequisite.
>
> Rule 8.5.1 **shall not** be waived.

**Rationale:** An undocumented deviation is indistinguishable from an unnoticed deviation. Silent exceptions damage the entire rule set (P7). The self-exclusion prevents Rule 8.5.1 from nullifying itself.

**Compliant:** a §4.8 density-budget violation in a survey section, waived with justification and an approver, linked from the conformance statement.
**Non-compliant:** "Everyone knows Section 3 does not follow the ladder. The deviation is fine."

**Cross-references:** §0.4.3; Rule 8.5.2.

**Waiver template fields:** deviated rule, document location, justification, compensating measure or "none," approver, and scope of validity.

#### Rule 8.5.2 — Waiver content
**Class:** mandatory · **Machine-checkable:** yes · **Source:** engineering-standard practice
**Constructs:** waiver
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: mechanical
**Resources:** reads: waiver-record · writes: waiver-record
**Relations:** requires 8.5.1

> An ITWS waiver **shall** complete every waiver template field.

**Rationale:** A waiver missing its location or approver cannot be audited. A waiver missing its scope silently becomes permanent policy.

**Compliant:** the filled template below.
**Non-compliant:** a repository-wide "waived: §2.3" note with no location, approver, or expiry.

**Cross-references:** Rule 8.5.1; Annex G (waiver-pattern analysis feeds rule changes per §0.8).

### 8.5.1 Waiver template

```
Waiver — ITWS deviation record
------------------------------------------------
Deviated rule:        <rule number and short name>
Document / location:  <document id, section or line range>
Justification:        <why conformance is not achievable or not desirable here>
Compensating measure: <what limits the damage, or "none">
Approver:             <name, role, date>
Scope of validity:    <this document only | this section only | until version X | expiry date>
------------------------------------------------
```

A waiver binds one document. A deviation needed by many documents is not a waiver. The deviation is a rule-change proposal (§0.8).

## 8.6 Generated artifacts and validation states

Sections 8.1 and 8.2 already require generated, version-pinned inputs. Section 8.6 states the contract those artifacts satisfy and the states a validation run may report. The contract exists so a reader or an artificial-intelligence agent can load one profile's rules, examples, glossary chain, and skeleton without reading every part first.

### 8.6.1 The generation contract

The Markdown files of `spec/` are authoritative. Every generated artifact derives from them. `spec/generated/agent/` holds the artifacts, and `manifest.json` holds their inventory.

An artifact set **shall** satisfy every generation-contract condition:

1. It records the ITWS version, the artifact schema version, and the generation command.
2. It records a content hash for every governed source file and for every generated file.
3. It is byte deterministic: two runs over one unchanged source tree produce identical bytes.
4. It preserves the canonical order of profiles, skeleton slots, glossary prerequisites, and rule statements. It sorts only what carries no normative order.
5. It contains every active and deprecated permanent rule exactly once.

**Generation-contract conditions:** the five conditions above.

#### Rule 8.6.1 — Generated artifacts satisfy the generation contract
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** requires 8.2.3; pairs-with 8.1.1

> A published artifact set **shall** satisfy every generation-contract condition.

**Rationale:** A checklist, a rule index, and a navigation catalog are only trustworthy when a reader can regenerate them and compare bytes. Recorded source hashes turn a stale artifact into a detected error rather than a silent one. Determinism keeps a regeneration diff readable, so a reviewer sees the rule change instead of reordering noise.

**Compliant:** `python3 tools/itws_compile.py --check` reports no difference, and `manifest.json` records ITWS 0.8.0-draft with a hash for every file under `spec/`.
**Non-compliant:** A committed `rules.jsonl` names ITWS 0.5.1-draft while the front matter reads 0.8.0-draft, and no command reproduces the file.

**Cross-references:** §0.4.4; §0.8; Rule 8.1.1; Rule 8.2.3.

**Stale-artifact conditions:**

- A recorded source hash differs from the current source file.
- A recorded ITWS version differs from the document's declared version.

#### Rule 8.6.2 — Stale artifacts are rejected, not reused
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.6.1

> A tool **shall not** report a conformance result computed from an artifact set that meets a stale-artifact condition.

**Rationale:** Section 0.4.4 checks a document against its declared version. An artifact generated from different source silently checks a different specification. Rejecting the run turns that mismatch into a visible failure, which is the outcome Rule 8.2.3 already requires of every version-pinned input.

**Compliant:** The validator stops and reports which source file changed after generation.
**Non-compliant:** The validator notices the changed hash, prints a warning, and still reports `pass`.

**Cross-references:** Rule 8.2.3; Rule 8.6.1.

### 8.6.2 Machine findings and human gates

A validation run reports exactly one state:

- **`pass`** — every machine-checkable applicable rule passed, and no required check was skipped.
- **`fail`** — at least one error-severity finding remains without a waiver.
- **`needs_review`** — no error-severity finding remains, and at least one `partial` or `no` rule still awaits a reader. Every human gate of the declared tier also reports here until it is recorded.
- **`blocked`** — a required input is missing. Examples are absent source evidence, an unavailable network check, and an unresolved exact item.

**Validation states:** the four states above.

#### Rule 8.6.3 — Validation reports one of four states
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** requires 8.2.4; pairs-with 8.2.1

> A validation run **shall** report exactly one validation state.
>
> A run with an unrecorded human gate or a skipped required check **shall not** report `pass`.

**Rationale:** A two-state report forces every unfinished check into either a false pass or a false failure. Rule 8.2.4 already says a clean machine run does not close a human gate; separate states let a tool say so instead of implying the opposite. The `blocked` state also gives a pipeline somewhere to put a missing fact, so it reports the gap rather than inventing content.

**Compliant:** A `decision-record` with a clean lint run and no recorded self-check reports `needs_review`, and the report names the missing gate.
**Non-compliant:** The same document reports `pass` because the linter found nothing.

**Cross-references:** §0.4.3; Rule 8.1.2; Rule 8.2.4; Rule 8.5.1.

### 8.6.3 Agent-authored records

An artificial-intelligence agent may read the generated artifacts, classify passages, and propose rewrites. Section 1.6.1 already reserves that judgment to a reader or agent. Section 8.6.3 states what such an agent owes when it records the judgment.

**Agent-record fields:** the source spans the judgment covers, the rule or specification section that supports it, and one judgment state from `proposed`, `accepted_for_run`, `disputed`, or `unresolved`.

#### Rule 8.6.4 — Agent-authored judgments cite their support
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** cross-reference
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: prohibited
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** pairs-with 8.4.4; requires 8.6.3

> A recorded semantic judgment about a governed passage **shall** state every agent-record field.

**Rationale:** Rule 8.4.4 already requires a review finding to cite its rule. A machine-authored classification needs the same discipline for the same reason: a judgment without a citation cannot be checked, argued with, or revised. The judgment state keeps an uncertain reading available instead of forcing a premature choice.

**Compliant:** "Lines 41–48 are an evidence chunk (§4.1, Rule 7.3.1); state: proposed."
**Non-compliant:** "Lines 41–48 are evidence." No rule, no span, and no state.

**Cross-references:** §1.6.1; Rule 8.4.4; Rule 8.6.3.

**Write-collision conditions:**

- Two proposed rewrites change one source span.
- Two proposed rewrites write one resource named in §1.6.2 without a declared order between them.

#### Rule 8.6.5 — Colliding rewrites are reported, not merged
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** any
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: collection · rewrite: prohibited
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.6.4; constrains 8.6.3

> A tool combining proposed rewrites **shall** report every write-collision condition it detects.
>
> The tool **shall not** choose between colliding rewrites.

**Rationale:** Parallel repairs are safe only where they touch disjoint text and disjoint ledgers. Two rewrites that both rename one artifact, or both edit one paragraph, produce a document that no reviewer approved. A tool can detect the collision mechanically. Only a reader can decide which rewrite survives, because the decision depends on meaning.

**Compliant:** The patch report lists both proposals, the shared span, and the shared `term-ledger` write, and it applies neither.
**Non-compliant:** The tool applies the later patch and silently discards the earlier one.

**Cross-references:** §1.6.2; Rule 2.7.3; Rule 8.6.4.

## 8.7 Machine-proposed comments carry a human disposition

Section 8.7 governs one construct of the `maintenance-comment` profile: a governed comment whose recorded provenance is `ai-proposed`. Its rules apply to that profile only, and §1.5 places them in `spec/overlays/maintenance-comment/rules.md`.

The gate is construct-specific evidence. Each machine-proposed comment carries one comment proposal record (§0.6) with its provenance, durable bases, pinned hashes, and recorded human disposition. The gate does not add reviewer roles and does not replace the two-role `reviewed` tier of §8.4. Annex C indexes every §8.7 rule with its profile applicability and its file.

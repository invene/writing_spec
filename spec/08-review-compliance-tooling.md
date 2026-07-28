# Part 8 — Review, compliance, and tooling

Part 8 defines practical checks for ITWS conformance. Section 8.1 defines the generated profile checklist. Section 8.2 defines automated checks and the author self-check. Section 8.3 defines publication reader testing and release checks. Section 8.4 defines reviewed-tier roles. Section 8.5 defines waivers.

Parts 2–7 define a conforming document. Part 8 defines how anyone verifies conformance.

Every governed document declares one canonical profile ID and one conformance tier. Rules apply to all profiles by default. A rule carrying `**Profiles:**` applies only when the declared profile appears in that list.

The minimum tier for each profile is:

- **Core:** `decision-record`, `explanation`, `investigation-log`.
- **Reviewed:** `design-rfc`, `procedure`, `incident`, `technical-report`.
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

> The conformance checklist **shall** be generated from every checklist-generation input.
>
> The checklist **shall not** be edited by hand.

**Rationale:** A hand-maintained checklist diverges from the rules the first time a rule changes (P7). Generation makes the checklist correct by construction.

**Compliant:** The checklist header records ITWS 0.2.1-draft, profile `procedure`, tier `reviewed`, and the Annex C revision from which it was generated.
**Non-compliant:** A reviewer copies the `research-paper` checklist, deletes statistics by hand, and calls the result a procedure checklist.

**Cross-references:** Annex C; Rule 8.1.3.

**Self-check passes:**

- Vocabulary.
- Sentence.
- Structure and explanation.
- Technical exactness and evidence.

#### Rule 8.1.2 — Four self-check passes
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original

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

> The checklist **shall** be regenerated after every checklist-regeneration trigger.

**Rationale:** Section 0.8 permits rules to change between versions. Profile and tier metadata also determine applicability. A stale checklist silently checks the wrong specification or document class.

**Compliant:** Adding `technical-report` to a rule's `Profiles` line triggers checklist regeneration before the specification release.
**Non-compliant:** A rule is reclassified recommended → mandatory and existing generated checklists still list it as optional.

**Cross-references:** §0.8; Annex C; Annex G.

## 8.2 Automated checks

`itws-lint` is the conformance linter. The linter uses Vale. Packaged Vale rule sets cover most content that Parts 2–3 adapt from the Google and Microsoft style guides. Custom rules cover profile selection, original mechanisms, and phrase lists. The linter reports readability metrics, including Flesch-Kincaid. Readability metrics do not gate conformance.

### 8.2.1 Check inventory (informative)

Inherited packages:

- Vale `Google` package — punctuation, word list, and usage rules forked in Parts 2–3.
- Vale `Microsoft` package — word-list adjudications and passive-voice heuristics.

Custom rules for original mechanisms:

- **Profile applicability** — the declared canonical profile selects default rules plus matching `Profiles` rules. Unknown profile IDs are errors.
- **Ladder ordering** — every term on the Annex B not-assumed list (or in Annex A) that appears before its definition chunk is flagged (§2.3).
- **Undefined-term detection** — terms in neither Annex B's assumed lists nor the document's admitted set are flagged (§2.3, §0.3.3).
- **One symbol, one meaning** — a symbol bound twice in one document is flagged (§5.2).
- **Profile exactness fields** — candidates for missing interfaces/invariants, procedure controls, incident timeline evidence, and research reproducibility are flagged (§5.4).

Custom phrase-list rules (each list versioned per §0.8):

- **Warpath markers** — "instead of the old approach," "unlike what we did before," "previously we," "as before" (§2.6 phrase list enforcing §4.9).
- **Puffery / machine-generated vocabulary** — the §2.6 living list ("delve," "underscore," "tapestry," "testament," "pivotal," "showcase," "intricate," "landscape," "boasts," …).
- **Editorializing asides** — "it's important to note," "it should be emphasized" (§2.6).
- **Vague attribution** — "experts say," "studies show," "widely regarded as" (§2.6).
- **Gap-speculation phrasing** — "while specific details are limited," "not widely documented" (§2.6).
- **Negative parallelism** — "not just X, it's Y" and variants (§3.10).
- **Copula avoidance** — "serves as," "stands as," "functions as," "boasts," "features" where "is"/"has" is meant; "refers to" openers (§3.10).
- **Trailing significance participles** — "…highlighting the need for," "…underscoring the importance of," "…reflecting a broader trend" (§3.10).
- **Hollow-summary openers** — section-final "In summary," "Overall," "In conclusion" (§6.5).
- **Conversational artifacts** — "I hope this helps," "certainly," "let's explore," "Would you like" (§2.6).
- **Formatting patterns** — title-case headings, inline-header vertical lists, emoji (§4.10, §4.5).

Mechanical artifact regexes are near-definitive signals of unreviewed machine-generated text. All have error severity:

- Tool leakage: `oaicite`, `contentReference`, `turn0search\d*`, `[cite: N]`, `grok_card`, `grok_render_citation`, `[span_\d+](start_span)`, `attached_file`, lenticular-bracket citations (`【N†…】`).
- Referrer leakage: `utm_source=chatgpt.com`, `utm_source=openai`, `utm_source=copilot.com`, `referrer=grok.com`.
- Unfilled placeholders: `[Your Name]`, `INSERT_`, `XX-XX` dates, empty template fields.
- Format bleed: code fences or `#` headings in non-Markdown output contexts.

Citation-integrity checks (§5.4):

- Every DOI resolves, and resolves to the cited work.
- No dead links without an archived copy (a dead link with no archive is treated as a fabrication signal, not ordinary link rot).
- No placeholder access dates.

### 8.2.2 Linter behavior

**Lint-gate outcomes:**

- Zero error-severity findings from a version- and profile-pinned `itws-lint` run.
- An ITWS waiver (§8.5) for each remaining error.

#### Rule 8.2.1 — Lint gate
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Vale / STE checker practice

> Before recording conformance at any tier, a governed document **shall** satisfy one lint-gate outcome.

**Rationale:** Machine-checkable violations are the cheapest to find and the most embarrassing to ship. The lint gate is part of core, so short-lived documents receive it even when their minimum tier has no independent reviewers.

**Compliant:** A core `investigation-log` links a clean `itws-lint` run pinned to ITWS 0.2.1-draft and profile `investigation-log`.
**Non-compliant:** "The linter is noisy. Readers can ignore the linter." Errors remain for review or release.

**Cross-references:** Rule 8.2.2; Rule 8.5.1.

**Severity map:**

- Mandatory rule: error.
- Recommended rule: warning.
- Permitted-practice hint: suggestion.

#### Rule 8.2.2 — Severity maps to rule class
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original

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

> Tooling **shall** use every version-pinned check input when checking a document.

**Rationale:** Sections 0.4.4 and 0.8 guarantee checking against the cited version. Profile applicability decides which rules enter that check. A linter that always runs the latest lists or guesses a profile breaks both guarantees.

**Compliant:** `itws-lint --spec 0.2.1-draft --profile design-rfc queue-design.md` loads the 0.2.1-draft lists and the `design-rfc` rule set.
**Non-compliant:** A 0.2.1-draft `procedure` is checked against the latest lists and the `research-paper` profile inferred from its references section.

**Cross-references:** §0.4.4; §0.8.

**Human gates:** the §8.1 author self-check and every reviewer, reader-test, or release gate required by the declared tier.

#### Rule 8.2.4 — Machine checks do not close human gates
**Class:** mandatory · **Machine-checkable:** no · **Source:** original

> A clean automated run **shall not** complete a human gate.

**Rationale:** Most mandatory rules are `partial` or `no` on machine-checkability. The linter finds phrase-list and ordering violations. The linter does not find every blurred interface, unsafe rollback, unsupported causal claim, or misleading explanation. Treating lint as human verification is the failure mode P7 prevents.

**Compliant:** Lint passes. The author still completes all four self-check passes. A reviewed-tier procedure then receives both required independent reviews.
**Non-compliant:** "CI is green, ship it." No self-check is recorded.

**Cross-references:** §8.4; Rule 8.1.2.

## 8.3 Publication reader test and release checks

The independent reader test is the assumed-reader half of §1.2's dual acceptance test. The test adapts plain-language teach-back testing and ISO/IEC/IEEE 26514 documentation-evaluation guidance. The publication tier requires the test. Other tiers do not require the test. A document may target publication above its profile's minimum. The test then measures that profile's primary outcome:

- `design-rfc` — explain the proposed design, affected interfaces, invariants, material trade-offs, and approval status.
- `decision-record` — state the decision, why it was chosen, the rejected alternatives, and its consequences.
- `procedure` — perform or tabletop the critical path and identify its preconditions, verification, rollback, and point of no return.
- `explanation` — explain the central concept or mechanism accurately in new words and apply it to one fresh example.
- `incident` — reconstruct impact and timeline, distinguish confirmed evidence from interpretation, and state unresolved causes and follow-up actions.
- `technical-report` — explain the main technical claim or operational outcome, its evidence, and its boundaries.
- `research-paper` — explain the main research result with correct context, baseline, evidence, uncertainty, scope, and strength.
- `investigation-log` — distinguish observations from hypotheses, state what remains unknown, and identify the next discriminating check.

Publication release checks confirm:

1. specification version, canonical profile, tier, and conformance statement are final and consistent;
2. the generated checklist, pinned lint output, and every waiver are current and linked;
3. both reviewed-tier approvals are complete;
4. citations, internal links, figures, tables, alt text, and referenced artifacts resolve in the release form;
5. profile-required deliverables, including reproducibility material where applicable, are accessible or their access limits are stated; and
6. the independent reader-test record identifies the participant criteria, task, outcome, and any revisions.

> **Drafting note (STY-52):** the profile-specific pass/fail tasks remain provisional until the protocol has been piloted and recorded for each profile that targets publication.

**Publication gate elements:** the independent reader test and every release check listed in §8.3.

#### Rule 8.3.1 — Publication gate
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514 / plain-language testing practice

> Before recording its conformance statement, a publication-tier document **shall** pass every publication gate element.

**Rationale:** Publication claims both independent comprehension and release readiness. The reader test catches a plain layer that changes the primary outcome. Release checks catch a correct draft with stale metadata, broken evidence, inaccessible artifacts, or missing approvals.

**Compliant:** A `research-paper` release record includes reviewed-tier approvals and a new independent participant's successful result teach-back. The record also includes resolved citations and artifacts. The checklist was generated for ITWS 0.2.1-draft.
**Non-compliant:** "The reader-proxy reviewer said it reads fine." The proxy is not an independent test participant. No release checks are recorded.

**Cross-references:** §1.2; §8.4; Rule 8.3.2.

**Participant baseline:** the declared profile's assumed-reader baseline.

**Disqualified participants:** authors, subject-matter owner reviewers, reader-proxy reviewers, contributors to the work, and prior readers of any draft.

#### Rule 8.3.2 — Participant sampling
**Class:** mandatory · **Machine-checkable:** no · **Source:** plain-language testing practice

> The test participant **shall** match the participant baseline.
>
> The participant **shall not** be a disqualified participant.

**Rationale:** The test measures what the document teaches, not what the participant already knew or absorbed in drafting, review, or project discussion. Contaminated participants pass documents that fail real readers.

**Compliant:** An engineer from an unrelated team who matches the `procedure` reader baseline and has never seen the system change table-tops the final procedure.
**Non-compliant:** The reader-proxy reviewer, who has read three drafts, is the test participant.

**Cross-references:** §0.3; Annex B; Rule 8.4.3.

**Reader-test procedure:** read the document once, unassisted and at the participant's pace, then complete the §8.3 profile-specific task.

**Passing response:**

- Preserves the primary outcome's applicable context, status or strength, and boundaries.
- Invents no fact, mechanism, step, decision, cause, or result.

#### Rule 8.3.3 — Protocol and pass criteria
**Class:** mandatory · **Machine-checkable:** no · **Source:** teach-back method, adapted

> The participant **shall** follow the reader-test procedure.
>
> The document **shall** pass only when the participant produces a passing response.

**Rationale:** A universal research-result test would not measure every profile's primary outcome. Such a test would miss procedure execution, decision recovery, and safe incident interpretation. The profile task ties the acceptance test to the document's job. The task retains two common failure directions: boundary creep (§7.4) and status or strength creep (§5.6).

**Compliant:** For a procedure, the participant waits until replica lag is below 2 seconds. The participant performs the verification query. When the query fails, the participant chooses rollback R1.
**Non-compliant:** The participant can summarize why the maintenance matters but skips the precondition and invents a restart as rollback.

**Cross-references:** §5.6; §7.4; §8.3 drafting note.

#### Rule 8.3.4 — Reader-test failures are recorded
**Class:** mandatory · **Machine-checkable:** no · **Source:** original

> A failed reader-test record **shall** state what the participant misstated or could not do.

**Rationale:** The misstatement or failed action is the finding: it points at the section that failed to teach and gives the revision a testable target.

**Compliant:** "Participant omitted the point of no return in step 6 and chose rollback after step 8."
**Non-compliant:** "Reader test failed." The record states no misstatement or failed action.

**Cross-references:** Rule 8.3.5.

#### Rule 8.3.5 — Failed documents are revised and independently retested
**Class:** mandatory · **Machine-checkable:** no · **Source:** original

> A publication-tier document that fails a reader test **shall** be revised.
>
> Before recording conformance, the document **shall** pass a retest with a new qualified participant.

**Rationale:** Revision closes the recorded comprehension gap. A new participant tests the document, not the first participant's memory of the session.

**Compliant:** A participant misses a rollback boundary. The author moves the boundary next to the affected step. A second qualified participant tests and passes the revision.
**Non-compliant:** The same participant rereads the revised draft and supplies the answer discussed after the first test.

**Cross-references:** Rule 8.3.2, Rule 8.3.4; §8.5 (an ITWS waiver may cover retest sampling when no untainted participant exists, with justification).

## 8.4 Reviewer roles

Reviewed and publication tiers assign §1.2's two layers to independent people. Core documents do not require these reviewers unless they target reviewed or publication. The **subject-matter owner** is accountable for correctness in the relevant system or domain. The **reader proxy** reviews from the declared profile's assumed-reader baseline. Neither reviewer may be an author.

**Required review roles:**

- An independent subject-matter owner for the exact layer.
- An independent reader proxy for the plain layer.

#### Rule 8.4.1 — Reviewed tiers use two independent roles
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514 / IEC 82079-1 review process

> Every reviewed-tier or publication-tier document **shall** receive reviews from both required roles.
>
> One person **shall not** fill both roles for the same document.

**Rationale:** The two layers fail in opposite ways. The owner can fill gaps from domain knowledge, but the proxy cannot judge technical correctness. Splitting the roles runs both acceptance tests without imposing two reviewers on core-tier documents.

**Compliant:** A service owner signs a reviewed `design-rfc` for interfaces, invariants, evidence, and boundaries. An engineer outside the change signs for the plain layer.
**Non-compliant:** The RFC author reviews it "wearing both hats," or a core `decision-record` is rejected solely because it did not recruit two reviewers.

**Cross-references:** §1.2; Rule 8.1.2 (pass assignment); Rule 8.3.2 (the proxy is not the test participant).

**Owner review scope:**

- Correctness of the exact layer.
- Traceability of simplified statements (§5.1).
- The complete evidence record, including lifecycle or authority status (§5.4).
- Calibration of evidential strength and decision authority (§5.6).
- Boundary coverage (Part 7).

#### Rule 8.4.2 — Subject-matter-owner scope
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514, renamed to §1.2

> The subject-matter owner **shall** check every item in the owner review scope.

**Rationale:** These checks require knowing what the domain permits and what the evidence supports. The profile record gives each profile a concrete focus. A `design-rfc` focuses on interfaces and invariants. A `decision-record` focuses on alternatives and consequences. A `procedure` focuses on preconditions, verification, and rollback. An `incident` focuses on timeline and evidence. A `technical-report` and `research-paper` focus on statistical and reproducibility-or-verification rigor. An `investigation-log` focuses on observation and hypothesis separation.

**Compliant:** The owner flags a procedure whose rollback step is unsafe after the schema migration even though the draft calls rollback available throughout.
**Non-compliant:** The owner copyedits sentence length and skips the interface invariant because "the proxy has the checklist."

**Cross-references:** Part 5; Part 7; Rule 8.1.2.

**Proxy review areas:** vocabulary, sentences, structure, and explanatory devices.

**Proxy blockers:** every term, symbol, transition, or missing explanation that prevents recovery of the profile's primary outcome.

#### Rule 8.4.3 — Assumed-reader proxy scope
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 26514, renamed to §1.2

> The reader proxy **shall** check every proxy review area from the declared profile's assumed-reader baseline.
>
> The proxy **shall** flag every proxy blocker.

**Rationale:** The proxy's value is disciplined ignorance: they read as the declared Annex B baseline, not as themselves. A proxy who fills gaps from project knowledge silently passes documents that fail the real reader.

**Compliant:** The proxy flags "quiesce L7" in a procedure because neither term is assumed or admitted. The state transition is required to execute the critical path.
**Non-compliant:** The proxy lets "fence the old primary" pass because the database team knows its meaning. The declared reader profile does not know the phrase.

**Cross-references:** §0.3; Annex B; Rule 8.1.2.

#### Rule 8.4.4 — Findings cite rules
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

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

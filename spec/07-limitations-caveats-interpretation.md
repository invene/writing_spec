# Part 7 — Limitations, caveats, and interpretation

Part 7 governs boundaries that keep a technical statement safe to use. The highest-stakes boundary varies by profile:

- In a design, the boundary may concern an invariant or unsupported capacity assumption.
- In a procedure, the boundary may concern a precondition or unsafe rollback.
- In an incident, the boundary may separate evidence from causal interpretation.
- In research, the boundary may limit a result's scope.
- In a work item, the boundary may concern an inherited invariant, delegated failure, or incomplete integrated acceptance.

Section 7.1 defines required disclosures. Section 7.2 defines caveat placement. Section 7.3 separates observations from load-bearing interpretations. Section 7.4 calibrates statements beyond established boundaries. Section 5.6 supplies the evidential-strength and decision-authority vocabulary.

## 7.1 Required boundary content

Every profile identifies its applicable boundaries from this shared inventory:

- **Environment** — deployment, region, topology, hardware, operating system, runtime, or physical conditions.
- **Version and dependencies** — software, schema, protocol, model, configuration, external service, and compatibility ranges.
- **Capacity and duration** — load, scale, rate, storage, resource, concurrency, time window, and exhaustion limits.
- **Failure and recovery** — known failure modes, partial-failure behavior, detection gaps, rollback boundaries, and irreversible effects.
- **Security and privacy** — trust assumptions, privileges, threat boundaries, secret handling, data classification, exposure, consent, and retention.
- **Data** — provenance, collection conditions, coverage, quality, missing cases, transformations, and known errors.
- **Untested or unverified conditions** — plausible conditions the primary outcome invites a reader to assume are covered but are not.

Not every dimension applies to every document. Conforming boundary material names the relevant dimensions. The material marks a plausibly relevant dimension as unknown or untested instead of silently omitting that dimension.

Annex E supplies the boundary locations for each profile:

- `design-rfc` — **Context** carries environment, version, and dependency bounds. **Requirements** and **Interfaces and invariants** carry capacity, security, privacy, and data constraints. **Risks** carries failure modes and unknowns. **Rollout** carries duration, recovery, and unverified-gate boundaries.
- `decision-record` — **Context** carries environment, version, and dependency bounds. **Alternatives** carries capacity, security, privacy, data, and reversibility trade-offs. **Consequences** carries accepted failure, recovery, duration, and unknown boundaries.
- `procedure` — **Scope** carries environment, version, capacity, duration, and data bounds. **Prerequisites** carries dependency, authority, security, and privacy assumptions. **Rollback** carries reversibility limits. **Failure and escalation** carries known failure modes and unverified conditions.
- `explanation` — **Limits** carries every applicable dimension.
- `incident` — **Impact** carries capacity, duration, security, privacy, and data effects. **Observations** carries environment, version, dependency, and data-quality bounds. **Causal analysis** carries uncertainty and unverified conditions. **Follow-up** carries detection and recovery gaps.
- `technical-report` — **Limitations** carries every applicable dimension. **Reproducibility or verification** carries environment, version, dependency, data, resource, and unverified-access bounds on independent checking.
- `research-paper` — **Limitations** carries every applicable dimension. **Reproducibility statement** carries data, dependency, resource, and unavailable-input bounds on repeating the work.
- `investigation-log` — each entry's **Configuration or context** carries environment, version, dependency, and data bounds. **Observations** carries source, duration, and quality bounds. **Interpretation** carries uncertainty and unverified conditions.
- `epic` — **Scope and non-goals** carries environment, version, dependency, security, privacy, and data boundaries. **Success measures** carries capacity, duration, and evidence boundaries. **Technical invariants** carries mandatory cross-task limits. **Cross-task risks** carries failure, recovery, and unverified conditions.
- `task` — **Context and boundaries** carries environment, version, dependency, capacity, authority, security, privacy, and data limits. **Sad or technical failure paths** carries failure and recovery behavior. **Integrated acceptance** carries cross-condition and unverified conditions.
- `subtask` — **Boundaries and invariants** carries local environment, version, dependency, security, privacy, data, and inherited limits. **Delegated path details** carries assigned failure and recovery behavior. **Verification evidence** carries unverified conditions and evidence limits.
- `maintenance-comment` — **Boundaries** carries the comments, files, and conditions the change set does not cover, and the environment, version, and dependency bounds within which each governed comment stays true. Each record's **Lifecycle** carries the removal condition of a temporary comment (Rule 4.13.7). Each record's **Basis** carries the evidence limits of a comment whose basis is `None`.

These profile-equivalent locations form the governed unit's boundary material for Rules 7.1.1, 7.1.2, and 7.2.2. A document may add a separate Boundaries section as an aggregate. The aggregate does not permit omission or weakening of an Annex E slot.

**Applicable boundary locations:** every Annex E location listed for the profile in §7.1.

#### Rule 7.1.1 — Boundary material is required
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS Paper Checklist (research adaptation)
**Constructs:** any
**Navigation:** target: document · chunks: limitation · slots: any · layers: exact · context: document · rewrite: candidate
**Resources:** reads: chunk-text, skeleton-order · writes: chunk-text
**Relations:** requires 4.3.3

> Every governed unit **shall** contain clearly identified boundary material in every applicable boundary location.

**Rationale:** The aggregation point for §7.2's in-line caveats must exist before it can aggregate (P6). Short profiles may keep the section brief, but no profile is exempt from stating where its primary outcome stops.

**Compliant:** A decision record puts version and dependency limits in **Context**. The decision record puts option-specific security and reversibility trade-offs in **Alternatives**. The decision record puts accepted failure and revisit conditions in **Consequences**.
**Non-compliant:** A decision record whose only compatibility limit appears in a footnote beside one rejected option.

**Cross-references:** Rule 7.2.2, §4.4 (skeleton placement).

#### Rule 7.1.2 — State the scope of validity
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS Paper Checklist / Model Cards (research adaptation)
**Constructs:** limitation
**Navigation:** target: chunk · chunks: limitation · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 7.1.1

> The boundary material **shall** state each applicable §7.1 dimension within which the document's primary outcome is valid.

**Rationale:** Scope is part of an exact statement (P6). Readers often assume wider compatibility, load tolerance, trust boundaries, data coverage, or external validity than the evidence establishes. Boundary disclosure prevents that silent widening.

**Compliant:** "This procedure is verified for service versions 4.8–4.10 on Kubernetes 1.32, at up to 200 active jobs per worker. The procedure assumes operator access to the recovery vault. The procedure is not verified for the managed-cloud deployment, whose rollback API differs."
**Non-compliant:** "This procedure restores the service." The statement has no environment, version, dependency, capacity, privilege, or verification boundary.

**Cross-references:** Rule 7.1.6, Rule 7.4.1, Rule 5.4.1 (evidence records).

#### Rule 7.1.3 — Disclose known failure modes and adverse effects
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514; IEC 82079-1; Model Cards (research adaptation)
**Constructs:** limitation, risk
**Navigation:** target: chunk · chunks: limitation, risk · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 7.1.1

> The boundary material **shall** describe known failure modes and their operational, security, privacy, data-integrity, or safety effects.

**Rationale:** Failure modes are findings (P6). Omitting an observed failure converts a known boundary into a reader's surprise. Omitting the failure's effect hides risk needed for a design, decision, procedure, or deployment choice.

**Compliant:** "If vault access expires after step 6, rollback cannot restore the old encryption key. New writes remain readable. Records written before rotation become unavailable until access is restored. No data is deleted."
**Non-compliant:** The expired-access failure appears in test logs but nowhere in the procedure or its boundaries.

**Cross-references:** Rule 7.2.1, §5.4 (failures are reported with the same rigor as successes).

#### Rule 7.1.4 — Disclose what was not tested or verified
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / Datasheets for Datasets (research adaptation)
**Constructs:** limitation
**Navigation:** target: chunk · chunks: limitation · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, evidence-ledger · writes: chunk-text
**Relations:** requires 7.1.1

> The boundary material **shall** identify the untested or unverified conditions that a reader would most plausibly assume the document covers.

**Rationale:** A list of everything untested would be infinite. The dangerous gap contains untested conditions the primary outcome invites the reader to assume (P6). Rule 7.1.4 turns the checklist assumptions item into a disclosure.

**Compliant:** "We did not test cross-region failover or dependency versions before 3.6. We also did not test sustained load above 12,000 requests/s or recovery after step 9's point of no return."
**Non-compliant:** A design validated in one region at 2,000 requests/s says "supports failover at production scale" and names no untested boundary.

**Cross-references:** Rule 7.1.2, Rule 7.4.2.

**Central data reliance:** central reliance on collected, generated, sampled, or logged data.

**Required data-boundary fields:** provenance, collection conditions, coverage gaps, transformations, retention limits, and known quality errors.

#### Rule 7.1.5 — Disclose data limitations
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514; Datasheets for Datasets (research adaptation)
**Constructs:** limitation, measurement
**Navigation:** target: chunk · chunks: limitation · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, evidence-ledger · writes: chunk-text
**Relations:** requires 7.1.1

> Boundary material for central data reliance **shall** state every required data-boundary field.

**Rationale:** Data flaws propagate silently into every conclusion derived from the data (P6). A research claim inherits its dataset's limitations. An incident conclusion inherits log retention and clock quality. A capacity decision inherits traffic-sample coverage limits.

**Compliant:** "Gateway logs came from all six affected hosts, but worker debug logs had seven-day retention and expired for the first 18 minutes. Host clocks were synchronized within 200 ms. The export removed request bodies because they contain personal data."
**Non-compliant:** "The logs show the worker caused the outage." The statement omits provenance, retention gaps, clock bounds, transformations, and privacy handling.

**Cross-references:** Rule 7.1.2, Rule 5.4.1.

#### Rule 7.1.6 — Plausible boundary gaps are explicit
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; NeurIPS Paper Checklist (research adaptation)
**Constructs:** limitation
**Navigation:** target: chunk · chunks: limitation · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 7.1.1; requires 7.1.2

> The boundary material **shall** identify each plausibly relevant §7.1 dimension that is unknown, untested, unverified, or not applicable.

**Rationale:** Silent omission makes an unknown boundary look unlimited. An explicit state distinguishes deliberate exclusion from a missed disclosure. "Plausibly relevant" avoids an infinite inventory of impossible conditions.

**Compliant:** "Data scope: not applicable. This decision uses no collected or generated data. Cross-region behavior: untested."
**Non-compliant:** A design names its tested version but says nothing about the visibly relevant cross-region condition.

**Cross-references:** Rule 7.1.1, Rule 7.1.2, Rule 7.1.4.

## 7.2 Caveat placement

The STE and IEC 82079-1 warning-placement mechanism puts a warning at the hazard, not only in a general safety chapter. Section 7.2 puts a caveat at the exact content it bounds. The hazard is a reader acting on an exact statement without its boundary.

**Caveated material types:** material claims, decisions, requirements, procedure steps, and outcomes.

#### Rule 7.2.1 — Caveats attach to their claims
**Class:** mandatory · **Machine-checkable:** no · **Source:** IEC 82079-1 / ASD-STE100 (warning placement)
**Constructs:** caveat, claim
**Navigation:** target: chunk · chunks: claim · slots: any · layers: exact · context: neighboring · rewrite: review
**Resources:** reads: chunk-text, claim-ledger · writes: chunk-text
**Relations:** constrains 7.2.2

> Every caveat **shall** share a chunk with the caveated material it qualifies.
>
> The caveat **shall** appear at every load-bearing statement of that content.

**Rationale:** Readers quote claims and act on decisions and procedure steps where those statements appear (P6). An unreached or distant caveat does not bound the statement in the reader's mind. For the same reason, "disconnect power first" belongs at the affected step, not only in a preface.

**Compliant:** "Run step 8 only while replica lag is below 2 seconds. Above that value, promotion can lose acknowledged writes. Section 7.1 collects the full recovery boundary."
**Non-compliant:** Step 8 says "Promote the replica," while the 2-second precondition appears only in the procedure's later boundary material.

**Cross-references:** Rule 7.2.2, Rule 5.4.1, §4.1 (the caveat is part of the claim chunk).

#### Rule 7.2.2 — Boundary material aggregates, it does not replace
**Class:** mandatory · **Machine-checkable:** no · **Source:** IEC 82079-1
**Constructs:** caveat
**Navigation:** target: document · chunks: limitation · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 7.2.1

> The profile's boundary material **shall** collect the document's caveats.
>
> Boundary material **shall not** be the only place a caveat appears.

**Rationale:** The aggregate view supports a reader assessing the whole document. The in-line caveat supports the reader at the point of use (P6). Each location has a separate job. Neither location replaces the other. Moving a caveat only to aggregated material hides the caveat from its point of use. The warning-placement rule prevents that failure.

**Compliant:** The 2-second promotion limit appears in step 8 and again with the other caveats under Scope and Failure and escalation.
**Non-compliant:** The procedure's boundary material is the first and only mention of the promotion limit.

**Cross-references:** Rule 7.1.1, Rule 7.2.1.

## 7.3 Interpretation discipline

Incident reviews, investigation logs, technical reports, research papers, tasks, and subtasks can turn observations into interpretations. The move is useful and dangerous. Section 4.1 supplies evidence and interpretation chunks. Section 6.3 supplies the block mechanism that bounds speculation. Section 5.6 supplies the permitted strength vocabulary. Other profiles may use the split. The split is mandatory only for the profiles listed on these rules.

**Interpretive additions:** causes, meanings, recommendations, and broader conclusions inferred from evidence.

#### Rule 7.3.1 — Separate observation from interpretation
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; IMRaD / APA JARS (research adaptation)
**Profiles:** incident, technical-report, research-paper, investigation-log, task, subtask
**Constructs:** observation
**Navigation:** target: chunk · chunks: evidence, interpretation · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: chunk-text, evidence-ledger · writes: chunk-text
**Relations:** requires 4.1.1

> A chunk recording an observation or measurement **shall not** include an interpretive addition.

**Rationale:** Observation and interpretation have different evidential standards (§5.6). Mixing them lets an interpretation borrow certainty from its adjacent timestamp, trace, test, or measurement (P6). A linter can flag chunks that mix measurement syntax with interpretive phrases. A human confirms the distinction.

**Compliant:** The split incident passage below.
**Non-compliant:** "Database connections reached the configured maximum at 09:14 UTC. The dependency upgrade therefore caused the outage." The observation and causal interpretation share one chunk.

**Cross-references:** Rule 4.1.1, Rule 7.3.2, Rule 5.6.1.

**Speculative statements:** statements exceeding the support available at §5.6's interpretive tier.

**Required speculation form:** a bounded block labeled **[Speculation — <topic>]** that remains removable under Rule 4.6.3.

#### Rule 7.3.2 — Speculation only in marked blocks
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original (§6.3 mechanism)
**Profiles:** incident, technical-report, research-paper, investigation-log, task, subtask
**Constructs:** speculation
**Navigation:** target: bounded-block · chunks: any · slots: any · layers: exact · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 4.6.2

> Every speculative statement **shall** appear only in the required speculation form.

**Rationale:** Speculation records the authors' best guess for future work. Speculation has value only when readers cannot mistake it for a finding (P3, P6). The standard block boundary identifies its status. Rule 4.6.3 keeps the main text coherent after removal of non-load-bearing speculation.

**Compliant:**
> **[Speculation — first connection failure]** We speculate that a credential refresh started the connection churn, but the relevant authentication logs had expired.

**Non-compliant:** "A credential refresh probably started the connection churn." The statement appears unmarked in main text. Retained evidence does not support the statement.

**Cross-references:** Rule 4.6.2, Rule 4.6.3, Rule 7.3.3, Rule 5.6.1.

**Speculative-tier phrases:** "we hypothesize" and "we speculate."

**Non-speculative tiers:** verified, observed, interpretive, adopted, and proposed.

#### Rule 7.3.3 — Speculation uses the speculative tier
**Class:** mandatory · **Machine-checkable:** partial · **Source:** IPCC calibrated language (via §5.6)
**Profiles:** incident, technical-report, research-paper, investigation-log, task, subtask
**Constructs:** speculation
**Navigation:** target: bounded-block · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text, claim-ledger · writes: chunk-text
**Relations:** requires 7.3.2; requires 5.6.1

> A speculation block **shall** use only speculative-tier phrases for strength.
>
> The block **shall not** use a phrase from a non-speculative tier.

**Rationale:** "The record shows" or "we decided" reintroduces certainty or authority inside a speculation block (P2). One table governs evidential-strength and decision-authority language (§5.6). The block label and its phrases must agree.

**Compliant:**
> **[Speculation — credential refresh]** We hypothesize that the unrecorded credential refresh started the connection churn.
**Non-compliant:** "**[Speculation — credential refresh]** The record shows that a credential refresh started the churn." "The record shows" is a verified-tier phrase.

**Cross-references:** Rule 7.3.2, Rule 5.6.1, Rule 3.9.2.

### Example: a passage correctly split

Non-compliant original (one paragraph, three strengths fused):

> Connection use reached 100% at 09:14 UTC, demonstrating that the client upgrade leaked connections, and a credential refresh probably triggered the first leak.

Conforming split:

> We observed connection use reach the configured maximum of 800 at 09:14:22 UTC on all three affected hosts. Trace links and clock bounds are in Timeline events I-17 through I-20.
>
> The evidence indicates that connection exhaustion caused request failures: failures begin after the pool reaches 800 and stop after capacity is restored. The evidence does not establish what began the connection growth.
>
> > **[Speculation — first connection failure]** We speculate that a credential refresh began the growth, but authentication logs for that interval had expired.

Each statement now carries its own strength. The timeline observation has full precision. The causal interpretation uses the interpretive tier. The unsupported hypothesis appears inside a bounded speculation block.

## 7.4 Statements beyond established boundaries

Section 7.4 adapts research scope-of-claims guidance and engineering compatibility practice. A statement beyond an established boundary is a different, weaker statement. The prose must identify that difference.

**Boundary-extension statements:** statements that extend a claim, decision rationale, verified procedure, incident conclusion, or result beyond its established boundary.

**Extrapolation targets:** environments, versions, dependencies, capacities, populations, data sources, and time periods.

#### Rule 7.4.1 — Extrapolations name the target setting
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / APA JARS (research adaptation)
**Constructs:** generalization
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: document · rewrite: review
**Resources:** reads: chunk-text, claim-ledger · writes: chunk-text
**Relations:** requires 7.1.2

> Every boundary-extension statement **shall** name its extrapolation target.

**Rationale:** "This works in production" is a claim about an unstated universe (P5, P6). Naming the target converts an unbounded extrapolation into a checkable one and forces the writer to distinguish what is established from what is expected.

**Compliant:** "For the managed-cloud deployment on service version 4.11, the evidence indicates that the same rollback sequence may work. The deployment's different snapshot API must satisfy the preconditions in §3."
**Non-compliant:** "The rollback procedure works everywhere."

**Cross-references:** Rule 7.1.2, Rule 7.4.2.

**Unestablished-setting forms:**

- The §5.6 interpretive tier: "the evidence indicates" or "this suggests."
- The proposed tier for a pending design choice.
- A marked speculation block.

#### Rule 7.4.2 — Beyond the boundary, drop evidential strength
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / CONSORT (research adaptation)
**Constructs:** generalization, claim
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: document · rewrite: candidate
**Resources:** reads: chunk-text, claim-ledger · writes: chunk-text
**Relations:** requires 7.4.1; requires 5.6.1

> A statement about a setting not established by the document's evidence **shall** use an unestablished-setting form.
>
> The statement **shall not** use a verified or observed phrase.

**Rationale:** Evidence earned in one setting supports, at most, an interpretation or proposal about another (P6). Strength must decrease at the established boundary. Section 5.6 supplies fixed vocabulary for that decrease. A linter can flag verified or observed phrases near settings absent from the evidence record. A human confirms the boundary.

**Compliant:** "Verification confirms the procedure on versions 4.8–4.10. The evidence indicates, but does not establish, that the procedure works on 4.11. Version 4.11 was unavailable during verification."
**Non-compliant:** "Verification confirms the procedure on versions 4.8–4.11." Version 4.11 was never tested or otherwise established.

**Cross-references:** Rule 7.4.1, Rule 5.6.1, Rule 7.3.2.

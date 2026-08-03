# Annex D — Examples corpus

**Status:** v0.10.0-draft. The corpus has 25 paired examples, at least two for every ITWS profile.

Both original research examples remain. The other 23 examples are constructed and cover every profile.

The corpus provides training material for writers.

The corpus also tests acceptance of the shared core and profile overlays.

The corpus is a machine input as well. The compiler extracts each example's metadata into `spec/generated/agent/examples.jsonl`, and a rule's `exemplified-by` relation points at the examples that cite it.

If a representative rewrite loses necessary meaning, inspect the applicable rules. Do not assume that the passage is faulty.

## D.1 Paired-example format

ITWS forks this paired-example format from STE and adds the annotation fields that §1.6 navigation needs:

```
### Example D.<n> — <one-line description of the failure mode>
Profile:           <one ITWS profile ID>
Source:            <public citation and passage location | approved anonymized source |
                    "constructed" for illustrations>
Rules applied:     <permanent rule IDs, comma separated>
Chunk types:       <§4.1 purposes the passage carries>
Constructs:        <§1.6.2 constructs present>
Repair operators:  <kebab-case names for the moves the rewrite makes>
Preservation notes: <what the rewrite had to carry through unchanged; semicolon separated>

Before:
<the original passage, verbatim>

After:
<the conforming rewrite>

Annotation:
<what changed and which rule forced each change>
```

The `Rules applied` field carries permanent rule IDs only. A section citation belongs in the annotation, where it gives context without pretending to be an applicability record.

`Chunk types`, `Constructs`, `Repair operators`, and `Preservation notes` are authored. The compiler extracts them; it does not derive them from the prose. An absent field means the author did not label the example, not that the example lacks the property.

Constructed examples do not assert facts about any organization or product.

An example may be an excerpt rather than a complete document. An excerpt conforms only for the jobs shown.

A complete governed document must still contain every required Annex E job.

Balance policy: the corpus shall contain at least two examples for every profile before any profile receives a third.

Sources should include public, approved anonymized, and constructed material. No source venue or repository is mandatory.

## D.2 Examples

### Example D.1 — Hype vocabulary and formulaic constructions in an abstract
Profile: research-paper
Source: constructed (representative of ML-abstract register)
Rules applied: 2.3.1, 2.6.1, 2.6.3, 2.6.4, 3.10.2, 3.10.4, 3.10.6, 5.4.2, 5.6.1, 7.4.1
Chunk types: claim, evidence, limitation
Constructs: prohibited-phrase, domain-term, quantity, claim, generalization
Repair operators: delete-puffery, admit-term, split-claim, add-change-context, bound-generalization
Preservation notes: the 43% reduction and both endpoint rates; the 1.9-times cost figure; the tested task family

Before:

> Large language models have revolutionized NLP, but hallucination remains a
> pivotal challenge, underscoring the need for robust mitigation strategies. We
> introduce VeriFrame, a novel framework that serves as a crucial bridge between
> generation and verification. VeriFrame doesn't just detect hallucinations — it
> prevents them, achieving a remarkable 43% improvement and showcasing the
> transformative potential of verification-aware decoding.

After:

> A *model* is a function plus many stored numeric settings, called parameters,
> that determine how the function maps inputs to outputs. A model that generates
> text sometimes states facts its input does not support. We call these facts
> unsupported statements.
>
> We built VeriFrame, a system that checks each generated sentence against the
> input before accepting it.
>
> On three question-answering test sets, VeriFrame produced 43% fewer
> unsupported statements than the same model without checking. The rate fell
> from 8.1% of sentences to 4.6%. VeriFrame used 1.9× the generation cost.
>
> The evidence does not establish a benefit on summarization because the tests
> covered only question answering.

Annotation:

- Section 2.6 requires deletion of these empty puffery terms: "revolutionized," "pivotal," "underscoring," "robust," "novel," "crucial," "remarkable," "showcasing," and "transformative." None describes this system (P5).
- The passage uses "hallucination" before defining it. The rewrite uses a defined plain term under §2.3. The original term can be admitted later.
- The passage also uses "models" in the machine-learning sense, which Annex B §B.3 lists as not assumed. The rewrite admits *model* with its Annex A definition before first use, as Rule 2.3.1 requires of an Annex A term.
- "Doesn't just detect" and "it prevents" form negative parallelism under §3.10. The rewrite states what the system does.
- "Serves as a crucial bridge" combines an inflated copula substitute with a metaphor. Section 3.10 requires its deletion.
- "A remarkable 43% improvement" is a naked percentage under §5.4. The rewrite names the quantity, endpoints, comparison condition, and cost.
- "Showcasing the transformative potential" is a trailing significance participle under §3.10. The rewrite rejects the unsupported generalization and states the tested scope.

### Example D.2 — Vague attribution and blurred claim in a results discussion
Profile: research-paper
Source: constructed (representative of results-section register)
Rules applied: 2.6.8, 2.6.9, 3.6.2, 5.4.1, 5.6.1, 7.3.1
Chunk types: evidence, interpretation, limitation
Constructs: citation, claim, speculation, pronoun, measurement
Repair operators: name-the-source, replace-bare-opener, split-observation-from-interpretation, report-absent-measurement
Preservation notes: the 9-of-11 count and the 4.2-point median; the two arithmetic exceptions

Before:

> It is widely known that larger models generalize better. Our results confirm
> this: performance improved across the board. While detailed per-task numbers
> are limited, this likely reflects the emergence of more general capabilities,
> which several studies have also observed.

After:

> On 9 of the 11 tasks, the 7-billion-parameter model scored higher than the
> 1-billion-parameter model. The median gain was 4.2 points. Table 3 gives the
> per-task results.
>
> The two exceptions are the arithmetic tasks. Both models scored below 15
> points on those tasks.
>
> We did not measure per-task variance across training runs. Therefore, we
> cannot determine which individual gains are stable.
>
> The evidence
> indicates that the size–score trend is consistent with published scaling
> results [12, 14]. Why the arithmetic tasks are exceptions remains an open
> question.

Annotation:

- "It is widely known" uses vague attribution under §2.6. The rewrite attaches two concrete citations to the specific trend that both sources support.
- "Performance improved across the board" is falsely general. Section 5.4 requires the measure, context, and comparison. The rewrite exposes both counterexamples.
- "While detailed numbers are limited, this likely reflects" turns missing evidence into a claim. Section 2.6 prohibits this gap speculation. The rewrite names the missing measurement.
- "This likely reflects the emergence of" starts with a bare demonstrative and uses uncalibrated "likely." Sections 3.6 and 5.6 prohibit those forms.
- The rewrite separates the interpretation under §7.3. The interpretation uses the phrase that §5.6 defines.

### Example D.3 — A design selected before requirements are stated
Profile: design-rfc
Source: constructed
Rules applied: 2.3.1, 2.6.2, 4.2.4, 4.4.1, 5.6.1, 7.1.3
Chunk types: requirement, decision, mechanism, risk
Constructs: requirement, name, claim, risk
Repair operators: state-requirements-first, admit-named-artifact, replace-absolute-with-invariant, add-staged-rollout
Preservation notes: the durability requirement; the repeat-safety obligation on each handler

Before:

> We should move background work to Kafka. It is the industry standard, gives
> exactly-once semantics, and will future-proof the platform. The migration
> should be straightforward.

After:

> **Summary.** We propose a persistent queue for accepted background jobs.
>
> **Requirements.** A worker restart must not lose an accepted job. A job may
> run more than once. Each handler must safely reject a repeated job ID.
>
> **Proposal.** Store each accepted job before acknowledging the request. A
> worker reads a stored job. The worker records completion under the job ID.
> Then, the worker removes the job from the queue.
>
> **Alternatives.** Keeping jobs only in worker memory is simpler. However, a
> worker restart loses accepted work.
>
> **Risks and rollout.**
>
> **Risks.** Duplicate delivery remains possible.
>
> **Rollout.** Test each handler with repeated job IDs. Then, enable the queue
> for one job class. Expand use only after that stage passes.

Annotation:

- The rewrite states requirements before selecting a mechanism.
- The rewrite removes the unexplained product name and "industry standard" appeal. The proposal describes behavior with admitted or baseline terms.
- "Exactly once," "future-proof," and "straightforward" are unsupported absolutes. The rewrite states the invariant, remaining risk, and staged rollout.

### Example D.4 — A decision hidden inside chronology
Profile: decision-record
Source: constructed
Rules applied: 4.2.4, 4.4.1, 4.9.1, 4.9.2, 5.6.1
Chunk types: context, decision, limitation
Constructs: prohibited-phrase, claim, requirement
Repair operators: delete-decision-path, promote-constraint-to-prior, state-decision-explicitly, replace-vague-benefit
Preservation notes: the rejected file option and its trade-off; the access-check consequence

Before:

> We first discussed storing the setting in a file, then considered a database.
> After several meetings we landed on the database option. This should be much
> better going forward.

After:

> **Status:** accepted
>
> **Context.** Multiple processes must read the setting. An operator must update
> it without replacing application files.
>
> **Alternatives.** A file avoids a database dependency. However, updating the
> file requires replacement in every running process.
>
> **Decision.** Store the setting in the existing configuration database.
>
> **Consequences.** Reads now depend on database availability. Updates can use
> the existing access checks. The existing record identifies who changed the
> setting and when. File-only startup is no longer sufficient.

Annotation:

- The meeting sequence is decision-path residue. Durable constraints replace that sequence.
- The rejected file option is preserved as an alternative with its material trade-off.
- The decision is explicit rather than buried in "landed on."
- Concrete positive and negative consequences replace "much better."

### Example D.5 — A procedure without a success test or recovery path
Profile: procedure
Source: constructed
Rules applied: 3.6.1, 4.1.1, 4.4.1, 5.4.1, 7.1.3
Chunk types: procedure, evidence, limitation
Constructs: procedure-step, measurement, warning
Repair operators: name-the-object, add-observable-check, add-executable-rollback, add-stop-condition
Preservation notes: the recorded prior version that rollback depends on; the zero active-job precondition

Before:

> Drain the host, deploy the new binary, and watch the dashboards. If anything
> looks bad, roll it back and ask the team for help.

After:

> **Goal.** Replace the worker binary on one host without accepting new work
> during replacement.
>
> **Prerequisites.**
> 1. Record the current binary version.
> 2. Confirm that another host can accept the queued work.
>
> **Steps.**
> 1. Disable new work on the selected host.
> 2. Wait until its active-job count is zero.
> 3. Install the new binary and start the worker.
>
> **Verification.**
> 1. Confirm that the worker reports the new version.
> 2. Submit one test job.
> 3. Confirm that the worker completes the test job without an error.
>
> **Rollback.** If any verification check fails, complete these steps:
> 1. Disable new work.
> 2. Reinstall the recorded version.
> 3. Restart the worker.
> 4. Repeat the verification checks.
>
> **Failure and escalation.** Stop if the active-job count does not reach zero.
> Also stop if the recorded version cannot be restored. Send the command output
> and host identifier to the designated role for failed changes.

Annotation:

- Named objects, observable conditions, and a role replace "the host," "anything," "looks bad," and "the team."
- Verification defines success. Rollback is executable. The rollback uses a prerequisite captured before change.
- Escalation states when to stop and what evidence to provide. The guidance does not invent an organization-specific contact.

### Example D.6 — An explanation that substitutes metaphor for mechanism
Profile: explanation
Source: constructed
Rules applied: 2.3.1, 4.1.1, 4.4.1, 6.1.1, 6.1.2, 6.2.1, 7.1.2
Chunk types: definition, mechanism, limitation
Constructs: analogy, definition, worked-example, domain-term
Repair operators: replace-metaphor-with-mechanism, admit-term, add-worked-example, state-analogy-breaking-point
Preservation notes: the expiration condition on a stored result; the staleness limit

Before:

> A cache is a magical shortcut: it remembers answers so the database does not
> have to work. Hot keys can cause a stampede, which is why caching is tricky.

After:

> **Summary.** A cache can reduce read latency by returning a recently stored
> result instead of repeating a slower lookup.
>
> **Concepts.** A cache stores a result under the same key used to request it.
> Each stored result has an expiration condition.
>
> **Mechanism.** If the key has a stored, unexpired result, the cache returns it.
> Otherwise, the caller performs the original lookup. The caller stores the
> result. Then, the caller returns the result.
>
> **Examples.** If 100 requests ask for the same record while it is stored, the
> system can serve 100 cache reads instead of 100 database reads.
>
> **Limits.** A stored result can be stale. Simultaneous misses can still repeat
> the original lookup. Caching trades memory and freshness for fewer slow source
> reads.

Annotation:

- The metaphor is replaced by an operational definition and a stepwise mechanism.
- Unadmitted shorthand ("hot keys," "stampede") is removed.
- The example is concrete. The limits state where the shortcut analogy breaks.

### Example D.7 — An incident report that turns correlation into root cause
Profile: incident
Source: constructed
Rules applied: 4.4.1, 5.4.1, 5.6.1, 7.2.1, 7.3.1
Chunk types: evidence, interpretation, limitation
Constructs: observation, claim, caveat, measurement
Repair operators: replace-cause-with-contribution, split-observation-from-interpretation, add-measured-impact, state-what-remains-unknown
Preservation notes: the 18-minute window and 12% error rate; the timestamps

Before:

> A deployment caused yesterday's outage. Error rates exploded right after it,
> proving that a bad change took the service down. We rolled back and everything
> was fine.

After:

> **Summary.** Requests failed for 18 minutes. Failures began three minutes
> after a deployment. They ended two minutes after rollback completed.
>
> **Impact.** From 14:07 to 14:25 UTC, 12% of requests returned an error.
>
> **Timeline.** Deployment completed at 14:04. The error rate crossed the alert
> threshold at 14:07. Rollback completed at 14:23. The error rate returned below
> the threshold at 14:25.
>
> **Observations.** The affected requests all used the changed code path. No
> comparable errors appear in the preceding hour.
>
> **Causal analysis.** The evidence indicates that the deployment contributed
> to the failures. The timing and code path match the change. The evidence does
> not identify which changed component produced the failures.
>
> **Remediation and follow-up.**
>
> **Remediation.** Keep the change disabled.
>
> **Follow-up.** Reproduce one failed request against each changed component.
> Record which condition triggers the error.

Annotation:

- Measured impact and timestamps replace "exploded," "outage," and "everything was fine."
- Observation is separated from causal interpretation.
- The rewrite states what the evidence supports and what remains unknown.

### Example D.8 — A report with a scale-free performance claim
Profile: technical-report
Source: constructed
Rules applied: 4.4.1, 5.4.1, 5.4.2, 5.6.1, 7.1.2, 7.1.4, 7.3.1
Chunk types: claim, evidence, interpretation, limitation
Constructs: comparison, measurement, claim, limitation
Repair operators: name-the-workload, replace-scale-free-claim, add-measured-endpoints, add-untested-conditions
Preservation notes: both completion times and their ranges; the memory comparison

Before:

> The new scheduler is 2× faster at scale and has negligible overhead. These
> results show that it is ready for production.

After:

> **Summary.** In the test configuration, the new scheduler completed the
> workload in 51 seconds versus 103 seconds for the current scheduler.
>
> **System or method.** A scheduler assigns queued jobs to workers. Both
> schedulers processed the same 10,000 independent jobs on 16 workers. Each
> result is the median of five runs.
>
> **Evidence.** Completion times were 49–54 seconds for the new scheduler and
> 100–108 seconds for the current scheduler. Peak memory was 1.8 GB for the new
> scheduler. Peak memory was 1.5 GB for the current scheduler.
>
> **Interpretation.** The evidence indicates a completion-time improvement for
> this workload. The new scheduler used about 20% more peak memory.
>
> **Limitations.** We did not test dependent jobs, worker failure, or more than
> 16 workers.
>
> **Verification.** A production-readiness decision requires those checks.

Annotation:

- "At scale" is replaced with the actual workload and worker count.
- "Negligible overhead" is replaced with measured memory endpoints.
- The report separates measurements, interpretation, limits, and the remaining verification work.

### Example D.9 — A log entry that depends on remembered prior state
Profile: investigation-log
Source: constructed
Rules applied: 4.4.1, 4.9.1, 4.9.2, 5.4.1, 7.3.1
Chunk types: context, evidence, interpretation
Constructs: measurement, observation, prohibited-phrase
Repair operators: replace-relative-config-with-absolute, replace-impression-with-measurement, label-interpretation, isolate-next-variable
Preservation notes: the four failing requests and their timing; every listed setting

Before:

> Tried it again today with the old config except for a larger timeout. It still
> behaved strangely, so tomorrow we will tweak the pool.

After:

> **2026-07-28 — Objective.** Determine whether a 10-second request timeout
> prevents the observed client failures.
>
> **Configuration.** Request timeout: 10 seconds. Worker count: 8. Reusable
> database connection count: 16. Workload: 500 requests at 20 requests per
> second.
>
> **Observations.** Four requests failed between 9.8 and 10.0 seconds. The other
> 496 completed in 0.2–3.1 seconds.
>
> **Interpretation.** Raising the timeout did not eliminate the failure pattern.
> The evidence indicates that timeout expiration ended those requests. However,
> the evidence does not identify why they remained active until the timeout.
>
> **Next step.** Repeat the same workload with connection wait time recorded for
> every request. Keep all listed settings unchanged.

Annotation:

- Absolute configuration replaces "old config" and "larger."
- Numbers replace "strangely."
- The interpretation is labeled and bounded. The next step changes one observable dimension and holds the listed settings fixed.

### Example D.10 — An epic that substitutes implementation work for strategy
Profile: epic
Source: constructed
Rules applied: 4.11.1, 4.11.8, 4.11.9, 4.11.10, 5.9.7
Chunk types: claim, evidence, requirement
Constructs: title, invariant, measurement, requirement
Repair operators: state-strategic-outcome, add-invariant-identifier, replace-activity-with-measure, delegate-tactical-acceptance
Preservation notes: the 580-of-1,380 baseline; both invariant statements

Before:

> # Checkout improvements
>
> Update the payment form and retry code. Add tests for expired cards. This epic
> is done when every pull request merges.

After:

> # Reduce checkout abandonment after recoverable payment failures
>
> **Strategic outcome.** Buyers can recover from a rejected payment without
> restarting checkout.
>
> **Problem and evidence.** During the last 30 days, 580 of 1,380 buyers
> completed a purchase within 24 hours after a recoverable payment failure.
>
> **Success measures.** During the 30-day evaluation window, at least 690 of
> each 1,380 covered buyers complete a purchase within 24 hours.
>
> **Technical invariants.**
>
> - INV-1: A failed payment **shall not** delete entered billing data.
> - INV-2: Checkout **shall not** create an order before payment succeeds.
>
> **Task map.** T-18 owns expired-card recovery. T-19 owns timeout recovery.
>
> **Definition of done.** The epic is done when the success measure passes and
> verification confirms INV-1 and INV-2 across every in-scope task.

Annotation:

- The title states the strategic outcome instead of naming a broad topic.
- Product evidence and a bounded success measure replace implementation activities.
- Stable invariant IDs give child tasks one exact shared contract.
- The task map delegates tactical acceptance instead of embedding it.
- The epic DoD verifies the strategic outcome and invariants. Merged pull requests do not establish either result.

### Example D.11 — A task with hidden classification and delegated failure behavior
Profile: task
Source: constructed
Rules applied: 4.11.2, 4.11.5, 4.11.6, 4.11.15, 4.11.18, 4.11.19, 5.9.1, 5.9.2, 5.9.3, 5.9.5, 5.9.6
Chunk types: requirement, decision, procedure
Constructs: title, declaration, user-journey, requirement, parent-link
Repair operators: state-journey-in-title, declare-both-classifications, cite-violated-contract, summarize-delegated-path, add-integrated-acceptance
Preservation notes: the five billing fields; the delegated sad path SP-2 and its owner

Before:

> # Fix expired cards
>
> Type: bug. Preserve the form if payment fails. See ST-4 for edge cases. Done
> when the frontend and backend subtasks close.

After:

> # A buyer can retry checkout after replacing an expired card
>
> **Classification.**
>
> - Outcome class: `user-journey`
> - Change reason: `defect-correction`
>
> **Parent and invariants.** Parent: E-7. Applicable invariants: INV-1 and INV-2.
>
> **Contract and deviation evidence.** Contract C-12 requires checkout to retain
> all five billing fields after payment rejection. Recording R-4 shows those
> fields become empty after the `expired_card` response in release 2026.07.
>
> **User journey.** A buyer with an expired card replaces that card and completes
> the existing order.
>
> **Happy path.** Checkout retains the order and billing fields. The buyer
> replaces the card. Checkout retries payment and confirms the order.
>
> **Sad paths.** SP-1 covers a second rejection. Checkout retains the order and
> billing fields, explains the rejection, and permits another replacement.
> SP-2 covers a timeout. Checkout retains the same state and offers retry.
> Subtask ST-4 owns SP-2 detail.
>
> **Definition of done.** CC-1 passes when test V-4 confirms that all five
> billing fields survive each covered rejection. CC-2 passes when test V-5
> confirms that one order exists after a successful retry.
>
> **Integrated acceptance.** Run the complete journey after CC-1 and CC-2 pass.
> Confirm that the retried payment uses the retained fields and existing order.

Annotation:

- The title carries the actor, trigger, and observable outcome.
- Two fields distinguish the user-journey outcome from the defect-correction reason.
- The accepted contract and recording establish a defect instead of a requested feature.
- The task retains SP-2's user-visible response, safe state, recovery, and owner.
- Named conditions and integrated acceptance replace closure based on child status.

### Example D.12 — A subtask with two parents and no parent condition
Profile: subtask
Source: constructed
Rules applied: 4.11.4, 4.11.12, 4.11.13, 4.11.14, 5.9.4
Chunk types: requirement, evidence
Constructs: title, parent-link, invariant, requirement
Repair operators: state-contribution-in-title, name-one-parent, name-one-parent-condition, replace-status-with-evidence
Preservation notes: the inherited INV-1 boundary; the field comparison that verifies CC-1

Before:

> # Checkout fix
>
> Parents: T-18 and T-21. Update the form and error message. Done when the pull
> request merges.

After:

> # Preserve billing data after an expired-card response
>
> **Parent task.** T-18.
>
> **Named completion condition.** T-18 CC-1 requires all five billing fields to
> survive each covered payment rejection.
>
> **Contribution.** Keep the five fields in form state when checkout receives
> the `expired_card` response.
>
> **Boundaries and invariants.** This subtask covers the browser form in release
> 2026.07. INV-1 applies. Server-side order retention remains in ST-5.
>
> **Delegated path details.** None. T-18 assigns no sad path to this subtask.
>
> **Definition of done.** This subtask is done when test V-4 compares all five
> fields before and after rejection and finds no change.
>
> **Verification evidence.** Test V-4 passes in Chrome 138 and Firefox 140.
> The test record links its field comparison to T-18 CC-1.

Annotation:

- One parent and one condition give the subtask a single acceptance owner.
- The contribution remains narrower than the parent user journey.
- The inherited invariant and local boundary limit the contribution.
- A verified field comparison replaces pull-request status as completion evidence.

### Example D.13 — An interface described without its bounds
Profile: design-rfc
Source: constructed
Rules applied: 2.1.4, 3.1.4, 5.1.1, 5.4.1, 7.1.2
Chunk types: requirement, mechanism, limitation
Constructs: interface, invariant, quantity, acronym
Repair operators: state-interface-bounds, expand-acronym, split-load-bearing-sentence, add-scope-of-validity
Preservation notes: the 5-megabyte payload ceiling; the at-least-once delivery guarantee

Before:

> The API is fast and accepts reasonably sized payloads. Delivery is
> guaranteed. The SLA covers all standard usage.

After:

> **Interfaces and invariants.** The submission interface accepts a payload of
> at most 5 megabytes. A larger payload is rejected with a size error.
>
> INV-1: An acknowledged submission is delivered at least once. Duplicate
> delivery remains possible.
>
> The service-level agreement (SLA) covers submissions below the size ceiling,
> at up to 200 submissions per second. It does not cover a submission that
> exceeds either bound.

Annotation:

- "Fast" and "reasonably sized" are unmeasured adjectives. Rule 5.4.1 requires the bound, so the rewrite states the ceiling and the rate.
- "Delivery is guaranteed" hides the difference between at-least-once and exactly-once. Rule 5.1.1 forbids a plain rendering that strengthens an exact item, so the invariant states the weaker true guarantee and names the residual duplicate risk.
- "SLA" appears without expansion. Rule 2.1.4 requires the expansion and the parenthesized short form at first use.
- "All standard usage" has no boundary. Rule 7.1.2 requires the scope in which the statement holds.

### Example D.14 — A decision record that omits its status and its reversal cost
Profile: decision-record
Source: constructed
Rules applied: 4.3.3, 4.4.1, 5.6.1, 7.1.3, 7.2.1
Chunk types: decision, limitation, risk
Constructs: claim, caveat, risk
Repair operators: add-required-slot, state-status, attach-caveat-to-claim, state-reversal-cost

Before:

> We are going with the managed queue. It's clearly the right call and we can
> always switch later if needed.

After:

> **Status.** Accepted on 2026-05-04 by the platform pod.
>
> **Decision.** Background jobs use the managed queue service.
>
> **Consequences.** Switching to a self-hosted queue later requires rewriting
> every handler's acknowledgement call, because the two interfaces differ.
> We estimate that rewrite at three engineer-weeks based on the 14 handlers
> in the current code base.
>
> Job payloads leave our infrastructure. The managed service holds them for
> up to 14 days.

Annotation:

- The record has no `Status` slot. Rule 4.3.3 requires every Annex E slot for the declared profile, and Rule 4.4.1 requires the skeleton's order.
- "Clearly the right call" is an uncalibrated claim. Rule 5.6.1 permits only the §5.6 table phrases, so the rewrite drops the assertion and states the decision.
- "We can always switch later" is a claim whose caveat is the switching cost. Rule 7.2.1 requires the caveat in the same chunk, so the estimate sits with the claim it qualifies.
- Payload residency is a disclosed effect under Rule 7.1.3.

### Example D.15 — A procedure whose warning arrives after the dangerous step
Profile: procedure
Source: constructed
Rules applied: 3.3.1, 4.1.1, 4.4.1, 7.1.3, 7.2.1
Chunk types: procedure, risk, limitation
Constructs: procedure-step, warning, caveat
Repair operators: move-warning-before-step, name-point-of-no-return, use-active-voice, add-verification-between-steps

Before:

> Run the migration script, then drop the old table. Note that the old table
> cannot be recovered once dropped, so it should have been backed up.

After:

> **Steps.**
>
> 1. Run the migration script.
> 2. Confirm that the row count in the new table equals the recorded count in
>    the old table.
> 3. Take a backup of the old table and record its location.
>
> **Warning.** Step 4 is the point of no return. After step 4 you cannot read
> the old table, and only the step 3 backup can restore it.
>
> 4. Drop the old table.

Annotation:

- The original states the hazard after the step that causes it. Rule 7.2.1 requires the caveat to sit with the content it qualifies, and Rule 7.1.3 requires the failure mode to be disclosed where a reader meets it.
- "It should have been backed up" states the prerequisite in the past tense, after the point where it was needed. The rewrite makes the backup an executable step before the hazard.
- "Should have been backed up" is passive with no actor. Rule 3.3.1 requires active voice here, because the reader is the actor.
- Step 2 separates the migration from the drop with an observable check, satisfying Rule 4.1.1's one purpose per chunk.

### Example D.16 — An explanation whose analogy carries the exact content
Profile: explanation
Source: constructed
Rules applied: 6.1.2, 6.3.1, 6.3.2, 6.5.4, 7.1.2
Chunk types: mechanism, limitation
Constructs: analogy, bounded-block, requirement, prohibited-phrase
Repair operators: move-exact-content-out-of-block, bound-the-intuition-block, state-analogy-breaking-point, delete-hollow-summary

Before:

> Think of the write-ahead log like a diary: you jot things down before you do
> them. Entries older than 7 days are removed. In summary, the write-ahead log
> is an important part of durability.

After:

> **Mechanism.** The service appends a record of each change to the write-ahead
> log before it applies the change. After a restart, the service replays every
> logged record that it has not yet applied.
>
> **Retention.** The service removes a log record 7 days after it writes the
> record.
>
> > **[Intuition — write-ahead log]** The log resembles a diary kept before the
> > fact rather than after it. Unlike a diary, the log is read by the service
> > and never by a person, and a replayed record changes stored data.

Annotation:

- The 7-day retention is an exact item stated only inside the analogy. Rule 6.3.2 forbids an intuition block from being the only location of exact content, so the rewrite moves the retention into main text.
- The informal explanation is now inside the bounded form Rule 6.3.1 requires.
- The diary analogy had no breaking point. Rule 6.1.2 requires the first property that does not transfer, so the block names two.
- "In summary, the write-ahead log is an important part of durability" adds nothing. Rule 6.5.4 requires the section to end on its last substantive point.

### Example D.17 — An incident report that hides impact behind an average
Profile: incident
Source: constructed
Rules applied: 5.4.1, 5.4.2, 7.1.5, 7.3.1, 7.4.1
Chunk types: evidence, interpretation, limitation
Constructs: measurement, quantity, observation, generalization
Repair operators: replace-average-with-distribution, add-change-context, state-data-limitation, name-extrapolation-target

Before:

> Average latency was only slightly elevated during the incident, so customer
> impact was minimal. Most users were unaffected.

After:

> **Impact.** Median request latency rose from 120 to 140 milliseconds. The
> 99th-percentile latency rose from 400 milliseconds to 9.2 seconds.
>
> 3,100 of 240,000 requests exceeded the 5-second client timeout and returned
> an error to the caller.
>
> **Limitations.** We record latency per region but not per account, so we
> cannot state how many distinct customers those 3,100 requests represent.

Annotation:

- The average hid the tail that produced the failures. Rule 5.4.1 requires the reporting elements that make a measurement interpretable, so the rewrite gives both the median and the tail.
- "Slightly elevated" and "minimal" are unmeasured. Rule 5.4.2 requires the change context for each figure.
- "Most users were unaffected" extends the claim from requests to users. Rule 7.4.1 requires an extrapolation to name its target setting, and the data does not support the user-level claim.
- Rule 7.1.5 requires the data limitation that blocks the user-level count.

### Example D.18 — A report that reuses one symbol for two quantities
Profile: technical-report
Source: constructed
Rules applied: 5.2.1, 5.2.2, 5.3.1
Chunk types: mechanism, evidence
Constructs: symbol, equation, table
Repair operators: rename-conflicting-symbol, define-symbol-at-first-use, add-notation-table, add-plain-reading

Before:

> We write t for the retry timeout. Throughput t is measured in requests per
> second. The relationship is t = c / t.

After:

> **Notation.** The retry timeout is *T*, measured in seconds. Throughput is
> *R*, measured in requests per second. Concurrency is *C*, a count of
> simultaneous requests.
>
> | Symbol | Meaning | Admitted in |
> |---|---|---|
> | *T* | retry timeout in seconds | §2 |
> | *R* | throughput in requests per second | §2 |
> | *C* | concurrency as a count | §2 |
>
> R = C / T
>
> Throughput equals concurrency divided by the retry timeout. Doubling the
> timeout at a fixed concurrency halves throughput.

Annotation:

- One symbol carried two meanings, which Rule 5.2.2 forbids in both directions.
- Neither symbol was defined before use. Rule 5.2.1 requires a prose definition at or before first use.
- The equation appeared without a reading. Rule 5.3.1 requires an adjacent plain-language reading, so the rewrite adds one sentence of reading and one of consequence.
- Rule 5.2.3 requires a notation table above six symbols; this report has three, so the rule is not applied here and the table is an aid rather than a requirement. Adding it early keeps the document compliant as the symbol set grows.

### Example D.19 — A research limitation that understates what was untested
Profile: research-paper
Source: constructed
Rules applied: 5.6.1, 5.6.2, 7.1.4, 7.1.6, 7.4.2
Chunk types: limitation, interpretation
Constructs: limitation, generalization, claim
Repair operators: enumerate-untested-conditions, mark-unknown-dimension, drop-strength-beyond-boundary

Before:

> Our method should generalize well to other domains. Limitations are minimal.

After:

> **Limitations.** We tested three English question-answering sets drawn from
> encyclopedia articles, product manuals, and financial filings.
>
> We did not test any other language, any generation task other than question
> answering, or any input longer than 4,000 words.
>
> Whether the reduction holds for a language with different entity morphology
> is unknown. Our checker compares entity strings exactly, and that comparison
> may behave differently under inflection.
>
> The evidence does not establish a benefit outside the three tested sets.

Annotation:

- "Should generalize well" is a claim about untested settings at observed strength. Rule 7.4.2 requires an unestablished-setting form, so the rewrite states what the evidence does not establish.
- "Limitations are minimal" names nothing. Rule 7.1.4 requires the untested conditions a reader would plausibly assume were covered.
- Rule 7.1.6 requires each plausibly relevant dimension to be marked unknown rather than omitted, so the morphology question is stated as unknown.
- The remaining strength language comes from the §5.6 table, satisfying Rules 5.6.1 and 5.6.2.

### Example D.20 — A log entry that rewrites its own history
Profile: investigation-log
Source: constructed
Rules applied: 2.1.1, 4.9.1, 4.9.3, 6.5.1, 7.3.1
Chunk types: context, evidence, interpretation
Constructs: prohibited-phrase, observation, admitted-term
Repair operators: append-correction-entry, restore-original-entry, use-established-term, separate-observation-from-correction
Preservation notes: the original count of four failing requests, which the later entry corrects rather than replaces

Before:

> **Entry 2026-07-27 E-1 (edited 2026-07-28).** Three requests failed, not four
> as previously stated. The connection pool was the culprit all along, unlike
> what we thought before.

After:

> **Entry 2026-07-27 E-1.**
>
> **Observations.** Four requests failed between 9.8 and 10.0 seconds.
>
> **Entry 2026-07-28 E-2.**
>
> **Objective.** Recount the failures recorded in entry E-1.
>
> **Observations.** A recount of the E-1 run finds three failing requests. The
> fourth record in E-1 duplicates the third request identifier.
>
> **Interpretation.** Entry E-1's count of four is superseded by this recount.
> The evidence indicates a recording defect in the harness, not a fourth
> failure.

Annotation:

- The original edits a recorded entry. The `investigation-log` skeleton declares entries append-only, so the correction becomes a new dated entry that cites the earlier one.
- "Unlike what we thought before" is a warpath marker. Rule 4.9.1 forbids it, and Rule 4.9.3 requires each path reference to delete cleanly or become a framed prior.
- "The culprit" is a causal claim in an observation position. Rule 7.3.1 keeps the observation and the interpretation in separate chunks.
- "Connection pool" replaces the admitted term used in earlier entries. Rules 2.1.1 and 6.5.1 require the established wording.

### Example D.21 — An epic whose success measure cannot fail
Profile: epic
Source: constructed
Rules applied: 4.11.10, 4.11.11, 5.9.2, 5.9.7, 5.9.8
Chunk types: requirement, claim
Constructs: requirement, measurement, invariant
Repair operators: make-measure-falsifiable, add-evaluation-window, remove-child-acceptance-detail, tie-completion-to-outcome

Before:

> **Success measures.** Improve the onboarding experience and increase
> activation.
>
> **Definition of done.** All child tasks are closed and the team agrees the
> experience is better.

After:

> **Success measures.** During a 30-day evaluation window, at least 45% of new
> accounts complete their first import within seven days of signup. The
> current figure is 31%, measured over the preceding 30 days.
>
> **Definition of done.** The epic is done when the success measure passes for
> one full evaluation window and verification confirms INV-1 and INV-2 in every
> in-scope task.

Annotation:

- "Improve" and "increase" name a direction, not a threshold. Rule 5.9.2 requires an observable pass condition and a verification method.
- The measure now carries a window and a baseline, so it can fail. A measure that cannot fail does not verify the strategic outcome that Rule 5.9.7 requires.
- "All child tasks are closed" makes completion depend on child status. Rule 5.9.8 requires every applicable completion condition to pass, and Rule 4.11.11 keeps each task independently acceptable.
- The original definition of done also carried tactical acceptance detail, which Rule 4.11.10 keeps out of an epic.

### Example D.22 — A subtask that quietly weakens an inherited invariant
Profile: subtask
Source: constructed
Rules applied: 4.11.9, 4.11.17, 5.9.4, 5.1.1, 5.1.2
Chunk types: requirement, evidence
Constructs: invariant, parent-link, requirement
Repair operators: restore-inherited-invariant, move-hint-out-of-contract, trace-evidence-to-parent-condition
Preservation notes: INV-1's prohibition on deleting entered billing data, at full strength

Before:

> **Contribution.** Keep most billing fields after a rejection where practical.
> Probably easiest to store them in session state.
>
> **Definition of done.** The form looks right after a rejection.

After:

> **Contribution.** Keep all five billing fields in form state when checkout
> receives the `expired_card` response. INV-1 applies without exception.
>
> **Technical hint.** Session state is one storage option. The hint carries no
> requirement.
>
> **Definition of done.** This subtask is done when test V-4 compares all five
> fields before and after the rejection and finds no change.
>
> **Verification evidence.** The V-4 record links its field comparison to
> CC-1 of parent task T-18.

Annotation:

- "Most billing fields where practical" weakens the inherited INV-1, which Rule 4.11.9 forbids. Rule 5.1.1 makes the same point at the sentence level: a plain rendering may not change an exact item's required behavior.
- The storage suggestion sat inside the contract. Rule 4.11.17 keeps a technical hint free of normative content, so the rewrite labels it and states that it binds nothing.
- "The form looks right" is not observable. Rule 5.9.4 requires the subtask's evidence to state how it verifies the named parent condition.
- Rule 5.1.2 requires the traceable link, which the verification-evidence chunk now supplies.

### Example D.23 — A task whose failure path leaves the buyer stranded
Profile: task
Source: constructed
Rules applied: 4.11.18, 4.11.19, 4.11.20, 4.11.21, 5.9.5
Chunk types: procedure, requirement, risk
Constructs: user-journey, requirement, warning
Repair operators: complete-happy-path-fields, add-failure-recovery, name-safe-state, add-integrated-acceptance
Preservation notes: the retained cart contents; the existing order identifier

Before:

> **Happy path.** The buyer pays and it works.
>
> **Sad paths.** If the provider is down, show an error.

After:

> **Happy or technical success path.** A buyer with a valid card submits
> payment. Checkout charges the card, confirms the order under the existing
> order identifier, and shows the confirmation page.
>
> **Sad or technical failure paths.**
>
> SP-1 covers a provider outage. Checkout retains the cart and the entered
> billing fields, states that payment could not be attempted, and offers a
> retry. No order is created, so INV-2 holds.
>
> SP-2 covers a provider timeout after the charge request was sent. Checkout
> retains the same state, states that the payment result is unknown, and
> directs the buyer to the order history page rather than offering an
> immediate retry.
>
> **Integrated acceptance.** After CC-1 and CC-2 pass, run SP-2 and confirm
> that a later reconciliation creates at most one order for the attempt.

Annotation:

- "The buyer pays and it works" states no actor path and no observable outcome. Rule 4.11.18 requires every happy-path field.
- "Show an error" names no safe state and no recovery. Rule 4.11.19 requires the user-visible response, the safe state, and the recovery for each sad path.
- SP-2 is the case the original omitted: a timeout after the charge leaves the payment result unknown, and offering an immediate retry risks a double charge. Naming the safe state is what Rule 4.11.19 buys.
- The double-charge risk appears only when both completion conditions interact, which is the behavior Rule 5.9.5 requires integrated acceptance to cover.

### Example D.24 — Machine narration that restates the code it annotates
Profile: maintenance-comment
Source: constructed
Rules applied: 4.13.1, 4.13.2, 4.13.4, 4.13.5
Chunk types: any
Constructs: comment
Repair operators: delete-restated-code, state-information-delta, replace-inferred-intent-with-basis
Preservation notes: the 250 ms retry delay; decision record DR-12 as the recorded basis

Before:

> ```python
> # Increment the retry counter and sleep for 250 milliseconds.
> # This ensures compliance with our performance requirements.
> retries += 1
> time.sleep(0.25)
> ```

After:

> ```python
> # 250 ms holds retries under the gateway's 4-per-second burst limit (DR-12).
> retries += 1
> time.sleep(0.25)
> ```

Annotation:

- "Increment the retry counter and sleep" restates the two lines below it. Rule 4.13.1 requires an information delta, and the delta here is the burst limit that the code cannot show.
- "Ensures compliance with our performance requirements" names a requirement that exists nowhere. Rule 4.13.5 forbids intent inferred from the implementation alone; the rewrite cites the decision record that actually fixed the number.
- One comment carried narration and an intent claim. Rule 4.13.2 gives the surviving comment one purpose, `rationale`.
- Rule 4.13.4 requires the rationale to carry a durable basis; DR-12 supplies it.

### Example D.25 — A bare marker with no route back to its work
Profile: maintenance-comment
Source: constructed
Rules applied: 4.13.8, 4.13.7, 4.13.4
Chunk types: any
Constructs: marker, removal-condition
Repair operators: add-work-item-reference, state-removal-condition
Preservation notes: the shim itself; the v2 totals endpoint as the replacement

Before:

> ```python
> # TODO: clean this up later.
> def totals_shim(order):
> ```

After:

> ```python
> # TODO(TASK-142): remove this shim when the v2 API returns order totals
> # directly and test T-9 passes against the v2 endpoint.
> def totals_shim(order):
> ```

Annotation:

- "Clean this up later" names no work item and no end state. Rule 4.13.8 requires the marker keyword, one durable reference, and a removal condition.
- The record declares lifecycle `temporary`, so Rule 4.13.7 requires the removal condition to be observable; a shipped v2 endpoint and a passing named test are checkable facts, "later" is not.
- TASK-142 is also the marker's durable basis under Rule 4.13.4: a future maintainer can open it and recover the context this line cannot carry.

## D.3 Coverage and next milestone

The corpus contains 25 examples. Every profile has at least two, and `research-paper` has three.

Every `Rules applied` field carries permanent rule IDs. The compiler resolves each ID against the rule set and fails on an unknown one.

Later expansion should add a third example only after every profile has two, and should widen the source mix. Candidate sources include public requests for comment, decision records, procedures, explanatory documentation, incident reports, technical reports, research papers, and investigation records.

Approved anonymized material is also eligible.

Source diversity is a quality constraint. Publication in any one venue or repository is neither required nor sufficient.

# Annex D — Examples corpus

**Status:** v0.2.1-draft. The corpus has nine paired examples. The examples cover all eight ITWS profiles.

Both original research examples remain. Seven constructed non-research examples form the initial cross-profile baseline.

The corpus provides training material for writers.

The corpus also tests acceptance of the shared core and profile overlays.

If a representative rewrite loses necessary meaning, inspect the applicable rules. Do not assume that the passage is faulty.

## D.1 Paired-example format

ITWS forks this paired-example format from STE:

```
### Example D.<n> — <one-line description of the failure mode>
Profile:       <one ITWS profile ID>
Source:        <public citation and passage location | approved anonymized source |
                "constructed" for illustrations>
Rules applied: <rule/section citations>

Before:
<the original passage, verbatim>

After:
<the conforming rewrite>

Annotation:
<what changed and which rule forced each change>
```

An entry may cite a section when the example applies a mechanism across several rules. Otherwise, cite the generated Annex C rule IDs.

Constructed examples do not assert facts about any organization or product.

An example may be an excerpt rather than a complete document. An excerpt conforms only for the jobs shown.

A complete governed document must still contain every required Annex E job.

Balance policy: the corpus shall contain at least one example for every profile before any profile receives a third example.

The next milestone is 16 examples, with at least two examples per profile. Sources should include public, approved anonymized, and constructed material.

No source venue or repository is mandatory.

## D.2 Examples

### Example D.1 — Hype vocabulary and formulaic constructions in an abstract
Profile: research-paper
Source: constructed (representative of ML-abstract register)
Rules applied: §2.6 (puffery, jargon-as-shorthand), §3.10 (negative parallelism, trailing significance participle, copula avoidance), §5.4 (no naked percentages), §2.3 (undefined terms), §5.6 (claim strength)

Before:

> Large language models have revolutionized NLP, but hallucination remains a
> pivotal challenge, underscoring the need for robust mitigation strategies. We
> introduce VeriFrame, a novel framework that serves as a crucial bridge between
> generation and verification. VeriFrame doesn't just detect hallucinations — it
> prevents them, achieving a remarkable 43% improvement and showcasing the
> transformative potential of verification-aware decoding.

After:

> Language models that generate text sometimes state facts their input does not
> support. We call these facts unsupported statements.
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
- "Doesn't just detect" and "it prevents" form negative parallelism under §3.10. The rewrite states what the system does.
- "Serves as a crucial bridge" combines an inflated copula substitute with a metaphor. Section 3.10 requires its deletion.
- "A remarkable 43% improvement" is a naked percentage under §5.4. The rewrite names the quantity, endpoints, comparison condition, and cost.
- "Showcasing the transformative potential" is a trailing significance participle under §3.10. The rewrite rejects the unsupported generalization and states the tested scope.

### Example D.2 — Vague attribution and blurred claim in a results discussion
Profile: research-paper
Source: constructed (representative of results-section register)
Rules applied: §2.6 (vague attribution, gap-speculation), §5.4 (reporting elements), §5.6 (calibrated language), §7.3 (observation vs. interpretation), §3.6 (bare "this")

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
Rules applied: §2.3 (term admission), §4.2 (main point first), §5.6 (claim strength), Annex E profile skeleton

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
Rules applied: §4.2 (main point first), §4.9 (path-agnostic prose), §5.6 (claim strength), Annex E profile skeleton

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
Rules applied: §3.7 (unambiguous reference), §4.1 (procedure chunks), §5.4 (measurable checks), Annex E profile skeleton

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
Rules applied: §2.3 (term admission), §4.1 (mechanism chunks), §6.1 (analogy boundary), §6.2 (worked examples), Annex E profile skeleton

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
Rules applied: §5.6 (claim strength), §7.2 (caveat placement), §7.3 (observation vs. interpretation), Annex E profile skeleton

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
Rules applied: §5.4 (comparison elements), §5.6 (claim strength), §7.1 (limitations), §7.3 (observation vs. interpretation), Annex E profile skeleton

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
Rules applied: §4.9 (path-agnostic prose), §5.4 (reporting elements), §7.3 (observation vs. interpretation), Annex E profile skeleton

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

## D.3 Coverage and next milestone

Current coverage includes one example for each non-research profile. Coverage also includes two retained `research-paper` examples.

Expansion should first add a second example to each profile that has one.

The next milestone is 16 examples, with at least two examples per profile.

Candidate sources include public RFCs, decision records, procedures, explanatory documentation, incident reports, technical reports, research papers, and investigation records.

Approved anonymized material is also eligible.

Source diversity is a quality constraint. Publication in any one venue or repository is neither required nor sufficient.

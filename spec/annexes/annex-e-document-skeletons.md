# Annex E — Document skeletons

**Status:** v0.2.1-draft.

This annex defines the required-section skeletons for the complete ITWS profile registry.

Every governed document has one profile ID. The registry contains exactly these IDs:

`design-rfc`, `decision-record`, `procedure`, `explanation`, `incident`, `technical-report`, `research-paper`, `investigation-log`.

Human-readable labels may vary. Label variations do not create additional IDs.

Every document also has a title. Every document must include the exact §0.4.3 declaration fields:

`ITWS version: 0.2.1-draft`, `Profile: <canonical ID>`, and `Conformance tier: <permitted tier>`.

The title and declaration fields are required document elements, not profile sections.

All slots marked *(required)* must be present.

If a job has no content, state `None` or `Not applicable`. Give the reason. Do not omit the slot.

Optional bounded blocks and appendices may be added under the shared-core rules.

### E.0.1 Rename and merge policy

- Exact skeleton headings require no section map.
- A heading may use one of the profile-specific renames listed below.
- Any other rename requires a front-matter `Section map`. The map must connect the actual heading to the canonical job.
- Only the merges expressly listed below are permitted.
- A merged section must retain separately labeled subsections for each canonical job. The subsections must follow canonical order.
- A rename or merge changes only the presentation. Required content does not change. No required job may disappear.
- Sections without explicit merge permission shall remain separate.
- Observations or evidence may share a section with causal analysis or interpretation only when the profile expressly permits that merge.
- A permitted shared section must label the observation or evidence job separately from the analysis or interpretation job.

## E.1 `design-rfc`

**Job:** specify a design that reviewers can evaluate against explicit requirements before implementation or rollout.

```
Summary                    (required) The proposed change, who or what it affects, and
                           the decision reviewers are being asked to make.
Context                    (required) The current condition, problem, and relevant
                           constraints, without decision-path history (§4.9).
Requirements               (required) Verifiable outcomes and constraints. Distinguish
                           mandatory requirements from preferences.
Proposal                   (required) The design and mechanism, ordered from the
                           assumed-reader view to exact detail.
Interfaces and invariants  (required) Inputs, outputs, boundaries, compatibility, and
                           properties that must remain true.
Alternatives               (required) Credible alternatives, including no change when
                           relevant, compared against the requirements.
Risks                      (required) Failure modes, security/reliability concerns,
                           unknowns, and mitigations with bounded claims.
Rollout                    (required) Implementation stages, validation gates, rollback,
                           and ownership or handoff points.
Open questions             (required) Unresolved decisions and the evidence or owner
                           needed to close each one.
```

Permitted renames: `Proposal` → `Proposed design`; `Interfaces and invariants` → `Contracts and invariants`; `Rollout` → `Migration and rollout`; `Open questions` → `Unresolved questions`.

Permitted merges: `Context` + `Requirements` → `Context and requirements`; `Proposal` + `Interfaces and invariants` → `Design`; `Risks` + `Rollout` → `Risks and rollout`.

## E.2 `decision-record`

**Job:** preserve one decision, the context that constrained it, and its expected consequences.

```
Status                     (required) Proposed, accepted, superseded, or another defined
                           state. Identify a superseding record when one exists.
Context                    (required) The durable facts, forces, and constraints that
                           made a decision necessary.
Alternatives               (required) The credible options considered, including no
                           change when relevant, and why they were not selected.
Decision                   (required) The selected option in direct, present-tense
                           language, including its scope.
Consequences               (required) Expected benefits, costs, trade-offs, follow-on
                           work, and conditions that would justify revisiting it.
```

Permitted renames: `Alternatives` → `Options considered`; `Decision` → `Outcome`; `Consequences` → `Consequences and trade-offs`.

Permitted merges: none. `Status` may appear as a front-matter field immediately before `Context`.

Front-matter placement satisfies the slot but does not make status optional.

## E.3 `procedure`

**Job:** enable the assumed reader to perform a bounded task safely and verify success.

The procedure supports recovery when possible. The procedure also supports escalation when recovery is unsafe or fails.

```
Goal                       (required) The end state the procedure produces.
Scope                      (required) Applicable systems, conditions, exclusions, and
                           required authority.
Prerequisites              (required) Access, tools, inputs, backups, captured state,
                           and checks completed before the first change.
Steps                      (required) Ordered actions with named objects and stop
                           conditions.
Verification               (required) Observable checks and pass criteria for the goal.
Rollback                   (required) Steps that restore the prior safe state, or an
                           explicit explanation of why rollback is unavailable.
Failure and escalation     (required) Conditions for stopping, safe state while stopped,
                           evidence to collect, and a named role or documented channel.
```

Permitted renames: `Goal` → `Outcome`; `Prerequisites` → `Before you begin`; `Failure and escalation` → `Stop conditions and escalation`.

Permitted merges: `Goal` + `Scope` → `Goal and scope`; `Rollback` + `Failure and escalation` → `Recovery and escalation`.

Verification checks may also appear beside individual steps. The required `Verification` job must still summarize the final pass criteria.

## E.4 `explanation`

**Job:** build a correct mental model of a concept or system.

The explanation must not become instructions or a design decision.

```
Summary                    (required) The idea and why it matters, in assumed-reader
                           vocabulary.
Concepts                   (required) Terms and relationships admitted in ladder order
                           (§2.3).
Mechanism                  (required) How or why the subject behaves, from plain model
                           to bounded exact detail.
Examples                   (required) Representative worked cases that exercise the
                           mechanism, not merely restate it.
Limits                     (required) Where the model stops, counterexamples, trade-offs,
                           and details intentionally left out.
```

Permitted renames: `Concepts` → `Key concepts`; `Mechanism` → `How it works`; `Limits` → `Limits and trade-offs`.

Permitted merges: `Concepts` + `Mechanism` → `Concepts and mechanism`. No other merge is permitted.

## E.5 `incident`

**Job:** record impact and chronology, distinguish observed facts from causal claims, and track restoration and prevention work.

```
Summary                    (required) What happened, current state, and the bounded
                           causal claim, if any.
Impact                     (required) Affected users or systems, duration, severity
                           measures, and known exclusions.
Timeline                   (required) Timestamped events with time zone and source when
                           the source matters.
Observations               (required) Logs, measurements, changes, and reproduced facts,
                           without causal interpretation.
Causal analysis            (required) Supported causal chain, contributing conditions,
                           confidence, and contrary evidence. State "undetermined" when
                           the evidence does not identify a cause.
Remediation                (required) Actions taken to restore or contain the incident
                           and evidence that service or process recovered.
Follow-up                  (required) Preventive and detective work, owners or roles,
                           due states, and verification of completion.
```

Permitted renames: `Causal analysis` → `Cause and contributing conditions`; `Remediation` → `Containment and recovery`; `Follow-up` → `Corrective actions`.

Permitted merges: `Summary` + `Impact` → `Summary and impact`; `Remediation` + `Follow-up` → `Remediation and follow-up`. `Timeline` or `Observations` shall not merge with `Causal analysis`.

## E.6 `technical-report`

**Job:** report a system, method, or technical finding.

The report must include enough detail for a reader to assess the evidence.

A reader must be able to reproduce the method or verify the system.

```
Summary                    (required) Main result or deliverable, scope, audience, and
                           headline evidence in assumed-reader vocabulary.
Context                    (required) Question, need, prior state, and constraints.
System or method           (required) What was built, examined, or done; interfaces,
                           configuration, and mechanism at the detail needed for audit.
Evidence                   (required) Measurements, observations, comparisons, or worked
                           cases with the reporting elements required by Part 5.
Interpretation             (required) What the evidence supports, separated from
                           observation and calibrated per §5.6.
Limitations                (required) Scope, failure modes, missing evidence, and what
                           was not tested.
Reproducibility or         (required) Use reproducibility when another reader can repeat
verification               the method. Use verification when claims are checked against
                           a system or artifact. State the steps, inputs, and pass
                           criteria. A report may include both.
```

Permitted renames: `System or method` → `System`, `Method`, or `Approach`; `Evidence` → `Results`; `Interpretation` → `Discussion`; `Reproducibility or verification` → `Reproducibility`, `Verification`, or `Reproducibility and verification`.

Permitted merges: `Evidence` + `Interpretation` → `Results and interpretation`, with separate labeled subsections. No other merge is permitted.

## E.7 `research-paper`

**Job:** report a research question, method, result, and bounded interpretation to publication standard using the IMRaD-derived ITWS structure.

The overlay assumes familiarity with research-paper navigation. The overlay assumes no knowledge of machine learning (Annex B §B.4).

```
Abstract                   (required) State the claim first in assumed-reader vocabulary.
                           Include scope, strength, and a headline comparison where
                           applicable.
Introduction               (required) Research question, importance, main claim, and
                           document map.
Background from first      (required) The ladder-seeding section: admit every
principles                 non-assumed term needed by the main line, in dependency order.
Method or what we built    (required) Procedure and mechanism, with exact detail in
                           bounded technical blocks when needed.
Experimental setup         (required) Data or materials, conditions, comparisons,
                           measures, and symbols needed to interpret the evidence.
Results                    (required) Observations and measurements. Include uncertainty
                           and self-contained figures or tables where applicable.
Discussion                 (required) Interpretation, relation to prior evidence, and
                           bounded generalization. Keep speculation labeled.
Limitations                (required) Scope of validity, known failure modes, untested
                           cases, and aggregation of claim-local caveats.
Reproducibility statement  (required) Plain-language account of what repeating the work
                           requires, distinct from an optional technical appendix.
```

Permitted renames: `Background from first principles` → a topic-specific heading that is mapped to `Background from first principles`; `Method or what we built` → `Method`, `Methods`, or `System`; `Discussion` → `Interpretation`; `Reproducibility statement` → `Reproducibility`.

Permitted merges: `Method or what we built` + `Experimental setup` → `Methods`, with separate mechanism and setup subsections.

`Results` and `Discussion` may merge as `Results and discussion` only when a publication format requires the merge.

The merged section must contain separately labeled observation and interpretation subsections.

`Background from first principles` shall not merge into `Introduction`.

Optional appendices may contain full formalism, proofs, extended tables, instruments, or configuration. An appendix does not replace any required job.

## E.8 `investigation-log`

**Job:** maintain a dated, append-only record of an investigation.

Another reader must be able to reconstruct the question, conditions, observations, interpretation, and next action.

```
Log header                 (required once for the log)
  Subject                  (required) The system, behavior, or question under investigation.
  Scope                    (required) Included and excluded environments, versions, time
                           range, and stop condition.
  Governing artifacts      (required) Links to the design, procedure, incident, issue, or
                           other source that authorizes or frames the investigation.
                           Write "None" with a reason when no such artifact exists.
  Admitted terms           (required) The log-wide admitted-term set and definition links;
                           entry-local terms are admitted inside their entry.
Entry <date> <id>          (required for each entry; include time zone when time matters)
  Objective                (required) The question this entry is intended to answer.
  Configuration or context (required) Absolute settings, inputs, environment, or
                           non-experimental context needed to interpret observations.
                           Include both configuration and context when both matter.
  Observations             (required) What happened or was found, with source and
                           measurements where available. Include no causal claim.
  Interpretation           (required) What the observations support and do not support.
                           Write "No interpretation yet" when evidence is insufficient.
  Next step                (required) The next discriminating check, decision, or stop
                           condition, stated as a plan.
```

Permitted renames: `Objective` → `Question`; `Configuration or context` → `Configuration`, `Context`, `Setup`, or `Configuration and context`; `Observations` → `Findings`; `Next step` → `Next action`.

Use `Configuration and context` when both kinds of content apply. Permitted merges: none.

`Observations` and `Interpretation` shall never merge.

The log as a whole carries the ITWS declaration. Entries do not repeat the declaration.

Entries are append-only. A correction must cite the earlier entry. Add the correction as a new dated statement.

Do not rewrite the earlier entry.

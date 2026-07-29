# Annex E §E.3 — `procedure` skeleton

**ITWS version:** 0.6.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

The procedure supports recovery when possible. The procedure also supports escalation when recovery is unsafe or fails.

## Dependency order

A `procedure` seeds prerequisites, safety conditions, permissions, and terms before the first dependent step (§4.4).

## Required sections

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

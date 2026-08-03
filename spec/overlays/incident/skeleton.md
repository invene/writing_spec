# Annex E §E.5 — `incident` skeleton

**ITWS version:** 0.10.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

## Dependency order

An `incident` supplies necessary system context and vocabulary before dependent timeline or causal analysis (§4.4).

## Required sections

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

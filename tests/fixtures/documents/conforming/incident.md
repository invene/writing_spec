# Request failures after the 14:04 configuration rollout

ITWS version: 0.6.0-draft
Profile: incident
Conformance tier: reviewed

## Summary

Requests failed for 18 minutes. The failures began three minutes after a configuration rollout. The failures ended two minutes after the rollback completed.

## Impact

From 14:07 to 14:25 Coordinated Universal Time (UTC), 12% of requests returned an error. The affected requests came from every region.

No stored record was lost. No request was charged twice.

## Timeline

The rollout completed at 14:04 UTC. The error rate crossed the alert threshold at 14:07 UTC.

The rollback started at 14:19 UTC and completed at 14:23 UTC. The error rate returned below the threshold at 14:25 UTC.

## Observations

Every failed request used the changed code path. No comparable error appears in the preceding hour.

The failing requests returned the same error code. The error count rose from 0.1% to 12% within four minutes.

## Causal analysis

The evidence indicates that the rollout contributed to the failures. The timing and the shared code path match the change.

The evidence does not identify which changed setting produced the failures. Three settings changed together in one rollout.

## Remediation

The changed configuration stays disabled. The previous configuration serves all regions.

## Follow-up

Reproduce one failed request against each changed setting in the staging environment. Record which setting triggers the error.

Split the rollout into one change per setting before the configuration is enabled again.

# Replace the worker binary on one host

ITWS version: 0.8.0-draft
Profile: procedure
Conformance tier: reviewed

## Goal

Replace the worker binary on one host. The host accepts no new work while the replacement runs.

## Scope

This procedure covers one worker host in the production environment. The procedure does not cover the scheduler, the database, or a whole-fleet replacement.

## Prerequisites

The replacement requires a drained host, a verified package, and rollback access.

1. Record the current binary version. The rollback step needs the recorded value.
2. Confirm that another host can accept the queued work.
3. Confirm that you can reach the host over the administrative network.

## Steps

The replacement drains, installs, starts, and checks one worker.

1. Disable new work on the selected host.
2. Wait until the active-job count on the host reaches zero.
3. Install the new binary.
4. Start the worker.

## Verification

Verification confirms the new binary, worker health, and job completion.

1. Confirm that the worker reports the new version.
2. Submit one test job to the host.
3. Confirm that the worker completes the test job without an error.

## Rollback

If any verification check fails, complete these steps:

1. Disable new work on the host.
2. Reinstall the version you recorded in the prerequisites.
3. Start the worker.
4. Repeat every verification check.

## Failure and escalation

Stop if the active-job count does not reach zero within 15 minutes. Stop if the recorded version cannot be restored.

Send the command output and the host identifier to the role that owns failed changes.

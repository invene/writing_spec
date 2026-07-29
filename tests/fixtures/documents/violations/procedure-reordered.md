# Replace the worker binary on one host

ITWS version: 0.8.0-draft
Profile: procedure
Conformance tier: reviewed

<!-- Risk fixture: a safety dependency is reordered. The Verification and -->
<!-- Rollback slots appear before Steps, which §4.4.1 forbids. -->

## Goal

Replace the worker binary on one host. The host accepts no new work while the replacement runs.

## Scope

This procedure covers one worker host in the production environment.

## Prerequisites

1. Record the current binary version.
2. Confirm that another host can accept the queued work.

## Verification

1. Confirm that the worker reports the new version.
2. Submit one test job and confirm that the worker completes it.

## Rollback

1. Disable new work on the host.
2. Reinstall the recorded version and start the worker.

## Steps

1. Disable new work on the selected host.
2. Wait until the active-job count reaches zero.
3. Install the new binary and start the worker.

## Failure and escalation

Stop if the active-job count does not reach zero within 15 minutes. Send the command output to the role that owns failed changes.

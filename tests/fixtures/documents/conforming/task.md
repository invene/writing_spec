# A buyer can retry checkout after replacing an expired card

ITWS version: 0.10.0-draft
Profile: task

## Summary

A buyer whose card is expired replaces the card and completes the existing order without re-entering billing data.

## Classification

- Outcome class: `user-journey`
- Change reason: `defect-correction`

## Parent and invariants

Parent: E-7. Applicable invariants: INV-1, INV-2, and INV-3.

## Context and boundaries

This task covers the web checkout form in release 2026.07. It excludes the mobile application and the support-facing order record.

## Contract and deviation evidence

Contract C-12 requires checkout to retain all five billing fields after a payment rejection. Recording R-4 shows those fields become empty after an `expired_card` response in release 2026.07.

## Journey or engineering outcome

A buyer with an expired card replaces that card and completes the existing order.

## Happy or technical success path

Checkout retains the order and the five billing fields. The buyer replaces the card. Checkout retries the payment and confirms the order under the existing order identifier.

## Sad or technical failure paths

SP-1 covers a second rejection. Checkout retains the order and the billing fields, states the rejection reason, and permits another replacement.

SP-2 covers a provider timeout. Checkout retains the same state and offers a retry. Subtask ST-4 owns the SP-2 detail.

## Definition of done

- CC-1: Test V-4 confirms that all five billing fields survive each covered rejection.
- CC-2: Test V-5 confirms that exactly one order exists after a successful retry.
- CC-3: Test V-6 confirms that the retried payment reuses the existing order identifier.

## Integrated acceptance

Run the complete journey after CC-1, CC-2, and CC-3 pass. Confirm that the retried payment uses the retained fields and the existing order.

## Subtask map

ST-4 owns the browser form state. ST-5 owns server-side order retention.

# Preserve billing data after an expired-card response

ITWS version: 0.6.0-draft
Profile: subtask
Conformance tier: core

## Summary

The browser checkout form keeps its five billing fields when the payment provider returns an `expired_card` response.

## Parent task

Parent: T-18.

## Named completion condition

CC-1 of T-18 requires all five billing fields to survive each covered payment rejection.

## Contribution

Keep the five fields in form state when checkout receives the `expired_card` response. The fields stay populated and editable.

## Boundaries and invariants

This subtask covers the browser form in release 2026.07. INV-1 applies. Server-side order retention stays in ST-5.

## Delegated path details

None. T-18 assigns no sad path to this subtask.

## Definition of done

This subtask is done when test V-4 compares all five fields before and after the rejection and finds no change.

## Verification evidence

Test V-4 passes in Chrome 138 and Firefox 140. The test record links its field comparison to CC-1 of T-18.

# Epic E-7 proposal: reduce checkout abandonment after recoverable payment failures

ITWS version: 0.10.0-draft
Profile: epic

## Summary

Epic E-7 requests approval for checkout recovery work. Buyers who hit a recoverable payment failure often abandon checkout. The epic covers the recovery path from the failure to a completed purchase.

## Strategic outcome

A buyer can recover from a rejected payment without restarting checkout.

## Problem and evidence

During the last 30 days, 580 of 1,380 buyers completed a purchase within 24 hours after a recoverable payment failure.

Session recordings R-2 through R-9 show that a rejected payment clears the entered billing fields. Every recorded buyer re-entered the fields or left.

## Users and journeys

A buyer holds a cart, submits a payment method, and receives a rejection the buyer can act on. An expired card and a network timeout are the two covered rejections.

A support agent reads the order record to answer a buyer question about a failed payment.

## Scope and non-goals

This epic covers recoverable rejections on the web checkout. It excludes the mobile application, subscription renewals, and refunds.

It excludes fraud declines, because a fraud decline is not recoverable by the buyer.

## Success measures

During the 30-day evaluation window, at least 690 of each 1,380 covered buyers complete a purchase within 24 hours.

Support contacts about failed payments fall below 40 per week, measured over the same window.

## Technical invariants

Three invariants preserve billing data, order creation, and order identity.

- INV-1: A failed payment **shall not** delete entered billing data.
- INV-2: Checkout **shall not** create an order before payment succeeds.
- INV-3: A retried payment **shall** reuse the existing order identifier.

## Task map

T-18 owns expired-card recovery. T-19 owns timeout recovery. T-20 owns the support-facing order record.

## Cross-task risks

Two tasks change the checkout form state. A change made in one task can undo the other, so both tasks share one form-state contract.

The payment provider may change its rejection codes during the window. That change would alter which rejections count as recoverable.

## Relations

This epic depends on architecture decision record ADR-41, which fixes the order-identifier format.

## Definition of done

The epic is done when the success measure passes for one full 30-day window and verification confirms INV-1, INV-2, and INV-3 across every in-scope task.

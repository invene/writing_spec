# Choose a coordinator for invoice writes

ITWS version: 0.6.0-draft
Profile: decision-record
Conformance tier: core

<!-- Risk fixture: a term is used before its definition (§2.3.1). -->

## Status

Accepted on 2026-06-02 by the storage pod.

## Context

The cluster reaches a quorum before it accepts an invoice write. A single coordinator holds the write for the duration of that agreement.

A *quorum* is the smallest number of cluster members that must agree before the cluster accepts a change.

## Alternatives

A fixed coordinator needs no agreement round. A fixed coordinator stops all writes when its host fails.

## Decision

The cluster elects one coordinator for each term of the agreement protocol.

## Consequences

A write now waits for the agreement round. The wait adds 4 to 9 milliseconds in the tested configuration.

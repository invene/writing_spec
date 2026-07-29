# Store the export retry limit in the configuration database

ITWS version: 0.6.0-draft
Profile: decision-record
Conformance tier: core

## Status

Accepted on 2026-06-14 by the platform pod.

## Context

Four processes read the export retry limit. An operator must change the limit without replacing application files. The current file-based limit changes only at process start.

The limit governs how many times an export job repeats after a transient failure. A wrong limit either drops work or holds a queue open too long.

## Alternatives

A configuration file avoids a database dependency. A change to the file reaches a running process only after a restart, and four processes must restart together.

An environment variable has the same restart cost and adds no audit record.

## Decision

The export retry limit lives in the existing configuration database. Each process reads the limit once per minute.

## Consequences

A read of the limit now depends on database availability. A process that cannot read the limit keeps the last value it read.

A change to the limit uses the existing access checks, and the existing change record names who changed the limit and when.

File-only startup no longer sets the limit. The startup path reads the database instead.

The limit applies to export jobs only. This record does not cover import retries or scheduled reconciliation.

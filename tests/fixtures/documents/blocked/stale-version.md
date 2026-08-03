# Store the export retry limit in the configuration database

ITWS version: 0.5.1-draft
Profile: decision-record

<!-- Risk fixture: the document declares an earlier ITWS version than the -->
<!-- checkout holds. Rule 8.6.2 rejects a result computed from a different -->
<!-- specification version. -->

## Status

Accepted on 2026-06-14 by the platform pod.

## Context

Four processes read the export retry limit. An operator must change the limit without replacing application files.

## Alternatives

A configuration file avoids a database dependency. A change to the file reaches a running process only after a restart.

## Decision

The export retry limit lives in the existing configuration database.

## Consequences

A read of the limit now depends on database availability. A process that cannot read the limit keeps the last value it read.

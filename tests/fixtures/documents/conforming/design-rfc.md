# A persistent queue for accepted background jobs

ITWS version: 0.6.0-draft
Profile: design-rfc
Conformance tier: reviewed

## Summary

We propose storing every accepted background job before the request returns. The change affects the job submission path and every job handler. Reviewers are asked to accept or reject the storage design.

## Context

A background job is work the system accepts now and runs later. Today the system holds accepted jobs in worker memory.

A worker restart loses every job it holds. During the last 30 days, three planned restarts lost 412 accepted jobs in total.

## Requirements

R-1: A worker restart **shall not** lose an accepted job.

R-2: A job **may** run more than once.

R-3: Each handler **shall** reject a repeated job identifier without side effects.

## Proposal

The submission path writes the job to durable storage. The path returns success only after the write completes.

A worker reads one stored job at a time. The worker records completion under the job identifier. The worker then removes the job from the queue.

## Interfaces and invariants

The submission interface accepts a job identifier, a job class, and a payload. The interface returns the stored identifier.

INV-1: A job the submission path acknowledged is present in storage until a handler records its completion.

INV-2: A completion record exists at most once for each job identifier.

## Alternatives

Holding jobs in worker memory is simpler and needs no storage dependency. A worker restart loses accepted work, which fails R-1.

Writing jobs to a local file on each worker keeps the storage dependency small. The file is unreadable after the worker's host is replaced, which also fails R-1.

## Risks

Duplicate delivery remains possible because R-2 permits it. A handler that is not repeat-safe can double-charge an account.

The submission path now depends on storage availability. A storage outage rejects new submissions instead of accepting work it cannot keep.

## Rollout

Stage 1 tests every handler with repeated job identifiers in the staging environment.

Stage 2 enables the queue for one job class in production for seven days.

Stage 3 enables the queue for the remaining job classes. Rollback at any stage restores the previous submission path and drains stored jobs through the new worker.

## Open questions

The retention period for a completed job record is undecided. The storage owner supplies the cost figure needed to close this question.

The behavior of a handler that fails after recording completion is undecided. The reliability reviewer supplies the required recovery contract.

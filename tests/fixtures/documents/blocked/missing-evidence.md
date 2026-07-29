# Completion time of the replacement job scheduler

ITWS version: 0.6.0-draft
Profile: technical-report
Conformance tier: reviewed

<!-- Risk fixture: an absent measurement stays absent. Every unknown value -->
<!-- is recorded as unknown, so validation reports `blocked` rather than -->
<!-- letting a rewrite invent a number (§8.6.2). -->

## Summary

In the test configuration, the replacement scheduler completed the workload in 51 seconds. The current scheduler's completion time is unknown, because the baseline run was not recorded.

## Context

A scheduler assigns queued jobs to workers. The platform pod asked whether the replacement scheduler reduces completion time.

## System or method

Both schedulers process the same 10,000 independent jobs on 16 workers. Only the replacement scheduler was measured.

## Evidence

Completion time for the replacement scheduler was 49 to 54 seconds across five runs.

Peak memory for the replacement scheduler was 1.8 gigabytes. Peak memory for the current scheduler is unknown.

## Interpretation

No comparison is available. The evidence establishes the replacement scheduler's completion time and nothing about the current scheduler.

## Limitations

The baseline measurement is missing. Until the baseline exists, this report supports no claim about a reduction.

We did not test dependent jobs, worker failure, or more than 16 workers.

## Reproducibility or verification

Another reader repeats the replacement measurement with the workload generator in `bench/scheduler` and the fixed 16-worker configuration file. The pass criterion is a median completion time within 10% of 51 seconds.

The baseline procedure is unknown, so no reader can yet verify the comparison this report was asked to make.

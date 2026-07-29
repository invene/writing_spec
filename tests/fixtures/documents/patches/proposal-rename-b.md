# Completion time of the replacement job scheduler

ITWS version: 0.6.0-draft
Profile: technical-report
Conformance tier: reviewed

## Summary

In the test configuration, the batch scheduler completed the workload in 51 seconds. The current scheduler completed the same workload in 103 seconds.

## Context

A scheduler assigns queued jobs to workers. The current scheduler assigns one job per polling cycle, and the cycle is fixed at 50 milliseconds.

The platform pod asked whether a batch scheduler reduces completion time enough to justify the migration cost.

## System or method

The batch scheduler assigns every runnable job at each cycle instead of one job.

Both schedulers processed the same 10,000 independent jobs on 16 workers. Each job slept for a fixed 20 milliseconds and returned. Each reported result is the median of five runs on one host.

## Evidence

Completion times were 49 to 54 seconds for the batch scheduler. Completion times were 100 to 108 seconds for the current scheduler.

Peak memory was 1.8 gigabytes for the batch scheduler. Peak memory was 1.5 gigabytes for the current scheduler.

## Interpretation

The evidence indicates a completion-time reduction for this workload. The batch scheduler used about 20% more peak memory.

The evidence does not establish a reduction for workloads with job dependencies, because every job in the test was independent.

## Limitations

We did not test dependent jobs, worker failure, or more than 16 workers. We did not vary the job duration.

We measured on one host, so the result carries no evidence about other hardware.

## Reproducibility or verification

Another reader repeats this measurement with the workload generator in `bench/scheduler`, the fixed 16-worker configuration file, and the five-run median script. The pass criterion is a median completion time within 10% of the reported value.

The host specification is recorded in the same directory. The recorded specification is the one input a reader outside the pod cannot obtain.

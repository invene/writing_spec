# Investigation log: client failures on the export path

ITWS version: 0.10.0-draft
Profile: investigation-log

## Log header

### Subject

Client requests to the export path fail at a low rate. This log records the search for the condition that ends those requests. Section "Admitted terms" defines every term this log adds.

### Scope

This log covers the export path in the staging environment, release 2026.07. The log excludes the import path and every production environment.

The log stops when one entry identifies the condition that ends a failing request.

### Governing artifacts

Issue EX-118 authorizes this investigation. No design or procedure frames the investigation.

### Admitted terms

A *service* is a running software unit that accepts requests through a defined interface. The unit returns results or performs work for another unit or user.

A *reusable database connection* is a database connection the service keeps open and hands to one request at a time.

## Entry 2026-07-27 E-1

### Objective

Determine whether a 10-second request timeout prevents the observed client failures.

### Configuration or context

Request timeout: 10 seconds. Worker count: 8. Reusable database connection count: 16. Workload: 500 requests at 20 requests per second.

### Observations

Three requests failed between 9.8 and 10.0 seconds. The other 497 requests completed in 0.2 to 3.1 seconds.

### Interpretation

Raising the timeout did not remove the failure pattern. The evidence indicates that timeout expiry ended those four requests.

The evidence does not identify why those requests stayed active until the timeout.

### Next step

Repeat the same workload with the connection wait time recorded for every request. Keep every listed setting unchanged.

## Entry 2026-07-28 E-2

### Objective

Determine whether the four failing requests waited for a reusable database connection.

### Configuration or context

Every setting matches entry E-1. The service now records the connection wait time for each request.

### Observations

Three requests waited more than 9.5 seconds for a reusable database connection. One request waited 0.1 seconds and then ran for 9.9 seconds.

### Interpretation

The evidence indicates that connection waiting ends most of the failing requests. The evidence does not cover the fourth request, whose wait was short.

### Next step

Repeat the workload with 32 reusable database connections. Record the wait time and the run time for every request.

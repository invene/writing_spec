# Annex E §E.11 — `subtask` skeleton

**ITWS version:** 0.10.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

A `subtask` is not independently acceptable. It may carry local implementation or verification detail. The parent retains the tactical outcome and integrated acceptance.

## Dependency order

A `subtask` seeds its parent condition and inherited invariants before contribution details, delegated paths, and verification (§4.4).

## Required sections

```
Summary                    (required) The contribution and the parent condition it
                           verifies, without a separate product outcome.
Parent task                (required) Exactly one authoritative parent task reference.
Named completion condition (required) Exactly one stable completion-condition ID from
                           the parent task, with its exact meaning and scope preserved.
Contribution               (required) The implementation, test, documentation, data,
                           or operational contribution this subtask supplies.
Boundaries and invariants  (required) Local scope, applicable inherited invariant IDs,
                           relevant failure limits, and excluded work.
Delegated path details     (required) Detail for each sad path delegated by the parent,
                           or "None" with a reason. The detail preserves the parent's
                           user-visible outcome.
Definition of done         (required) One local closure contract that verifies the
                           named parent completion condition.
Verification evidence      (required) Artifact, environment, inputs, method, observable
                           result, and link back to the parent condition.
```

Optional: `Technical hints`, containing only non-normative implementation information. An unverified hypothesis uses a Speculation block.

Permitted renames: `Named completion condition` → `Parent condition`; `Boundaries and invariants` → `Boundaries`; `Delegated path details` → `Delegated paths`; `Verification evidence` → `Evidence`.

Permitted merges: `Summary` + `Parent task` → `Summary and parent`; `Contribution` + `Boundaries and invariants` → `Contribution and boundaries`.

Each permitted merge must retain the canonical jobs as separately labeled subsections. `Definition of done` shall not merge with Technical hints.

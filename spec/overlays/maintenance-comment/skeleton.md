# Annex E §E.12 — `maintenance-comment` skeleton

**ITWS version:** 0.8.0-draft · **Status:** normative

The README in this directory states the profile job. Annex E states the shared slot policy and the §E.0.1 rename and merge policy.

This skeleton binds a hosted comment set, not a Markdown document. Each slot is a named field of the JSON declaration carrier (§4.3, §E.0.4). The host source file carries only the comments themselves.

## Dependency order

A `maintenance-comment` change set seeds its scope, host identity, and anchors before the comment content, bases, and lifecycle facts that depend on them (§4.4).

## Required sections

```
Change scope               (required) The change-set ID, host adapter, host file,
                           base and proposed hashes, and the change set's
                           one-sentence purpose.
Comment record             (required, for each governed comment) One governed
                           comment's complete record.
  Anchor                   (required) The host file, line span, and enclosing
                           named construct the comment attaches to.
  Comment text             (required) The exact governed comment text, with
                           comment markers stripped.
  Purpose                  (required) Exactly one closed purpose from Rule 4.13.2.
  Information delta        (required) The knowledge deleting the comment would
                           lose, stated against the anchored code.
  Basis                    (required) The durable code, test, contract, work-item,
                           or decision references that support the comment, or
                           "None" with a reason.
  Lifecycle                (required) "durable", or "temporary" with the
                           observable removal condition.
  Provenance               (required) "human-authored", or "ai-proposed" with the
                           §8.7 comment proposal record.
Boundaries                 (required) The comments, files, and conditions the
                           change set does not cover.
Conformance evidence       (required) The pinned lint run, self-check, and
                           scan-test records for the declared tier.
```

Permitted renames: none.

Permitted merges: none.

An empty required field states `None` or `Not applicable` with a reason, exactly as §E.0 requires of a document slot.

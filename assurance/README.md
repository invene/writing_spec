# ITWS assurance companion

**Status:** non-normative companion guidance

This guide describes optional ways to gain confidence in text written against
the Invene Technical Writing Specification (ITWS). It is not part of ITWS
textual conformance. A writer or rewriting agent does not load this guide
unless a request explicitly asks for assurance, review, or release work.

ITWS conformance and assurance answer different questions:

- **Textual conformance:** Does the governed text satisfy every applicable
  mandatory language rule for its declared ITWS version and profile?
- **Machine-check result:** Did the reference checker find a decidable
  violation, and what portion of the rule envelope did it evaluate?
- **Assurance:** What independent review, reader testing, release checking, or
  accepted-deviation process did an organization choose to perform?

Assurance never changes the text's conformance. In particular, accepting a
deviation does not turn violating text into conforming text.

## Optional assurance levels

Organizations may use these cumulative labels. They are not ITWS declarations
and do not belong in governed text.

### `core`

The author or rewriting agent:

1. runs a checker pinned to the text's declared ITWS version and profile;
2. reads every machine candidate and every rule outside machine coverage;
3. records unresolved facts without inventing them; and
4. performs a profile-aware self-check of vocabulary, sentences, structure,
   explanation, exactness, evidence, and boundaries.

### `reviewed`

The `core` work is complete. Two people who did not author the text review it:

- A **subject-matter owner** checks exact content, evidence, status, conditions,
  interfaces, invariants, and boundaries.
- A **reader proxy** checks the plain layer from the profile's assumed-reader
  baseline.

One person should not fill both roles for the same review.

### `publication`

The `reviewed` work is complete. A fresh representative reader completes the
reader protocol, and the release checks in this guide are complete.

## Profile-aware checklist

A checklist should be generated from the selected version's active language
rules and the declared profile. It should not be edited by hand. A practical
self-check groups applicable rules into four passes:

1. vocabulary;
2. sentences;
3. structure and explanation; and
4. technical exactness and evidence.

The checklist is an assurance artifact. Its existence is not a language
requirement, and a missing checklist does not prevent an agent from producing
a rewrite.

## Scan protocol

The normative specification defines a **scan path**, which is part of the
text. This optional protocol tests what that path leaves with a reader.

A scan key records:

1. the expected purpose and main point;
2. applicable status or strength;
3. every material boundary needed to prevent widening;
4. links to supporting exact and body items; and
5. one plausible strengthened foil for each protected status, strength, or
   boundary.

The reader views the complete scan path once, closes the text, completes a
source-independent intervening task, states the profile's shallow-model
outcome from memory, and accepts or rejects each foil. Record omissions,
widening, invented facts, and accepted foils. A change to a scan-path element
or linked source makes the result stale.

At `reviewed` and `publication`, the subject-matter owner should prepare or
approve the key before the reader proxy or participant sees it.

## Independent reader protocol

For `publication`, use a participant who matches the declared assumed-reader
baseline and has not authored, reviewed, contributed to, or previously read a
draft.

1. Complete the scan protocol before opening the full text.
2. Let the participant read the full text once, unassisted and at their pace.
3. Ask them to produce the primary outcome appropriate to the profile.
4. Record what they misstated, invented, or could not do.
5. Revise failures and retest with a different qualified participant.

## Release checks

Before applying the optional `publication` assurance label, confirm:

1. the ITWS version and profile are final and consistent;
2. machine-check output and accepted-deviation records are current;
3. the independent reviews are complete;
4. citations, links, figures, tables, alternative text, and referenced
   artifacts resolve in the release form;
5. profile-required deliverables are accessible or state their access limits;
   and
6. the reader record contains both phases, participant criteria, outcomes, and
   resulting revisions.

## Accepted deviations

An organization may accept text that does not conform to one or more mandatory
rules. Record:

- the deviated rule;
- the text and location;
- the reason;
- a compensating measure or `None`;
- the accepting person, role, and date; and
- the scope or expiry.

Call this an **accepted deviation**, not an ITWS waiver and not conformance.
Recurring deviations are evidence that the language rule may need revision.

## Machine-proposed comments

An organization may require provenance review before merging a comment proposed
by a machine. A proposal record can include:

- prompt or run provenance;
- durable code, test, contract, work-item, or decision bases;
- source, anchor, and comment hashes; and
- a human disposition of `accepted`, `revised`, or `rejected`.

A changed hash should invalidate the disposition. This is an optional merge
control, not a language rule. ITWS comment text remains subject to the same
information-delta, basis, lifecycle, exactness, and non-invention rules
regardless of authorship.

## Historical mapping

ITWS 0.9.0-draft encoded these practices as normative conformance tiers and
Rules 8.1.1–8.1.5, 8.3.1–8.3.5, 8.4.1–8.4.4, 8.5.1–8.5.2, and
8.7.1–8.7.4. ITWS 0.10.0-draft retires those process rules from the current
language specification. Their permanent identifiers remain reserved and are
not reused.

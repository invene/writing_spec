ITWS version: 1.0.0
Profile: decision-record
AI disclosure: generated — drafted every section from the STY-79 ticket and the ITWS 1.0.0 rule set; not yet reviewed

# A tabular document declares one AI disclosure for the whole workbook

## Status

Proposed. No superseding record exists.

Recorded against [STY-79](https://linear.app/inveneprod/issue/STY-79), the first
of the two questions the spreadsheet-overlay proposal left open.

## Summary

A workbook declares one `AI disclosure` value for the whole workbook. That single
declaration covers every cell in it. We propose no table-specific convention for
a later cell edit. [Decision](#decision) carries the exact statement.

## Context

A *tabular document* is a workbook of named sheets. ITWS governs it as one unit
under the `data-table` profile
(<https://github.com/invene/writing_spec/blob/1.0.0/spec/profiles/data-table.md>).
Its *Title sheet* comes first and holds the workbook's identity. The Title sheet
also holds the three ITWS declarations, as rule §4.14.1 requires.

The `AI disclosure` field records what generative tooling contributed to a
governed unit. Core §0.5 fixes three values: `none`, `assisted`, and `generated`.

The question arose because a workbook is edited differently from a prose
document. A consultant reopens a delivered workbook months later and changes four
cells. A Markdown document under the same treatment would be rewritten in
sections. Its disclosure note would then describe that rewrite. The proposal
asked whether a table needs its own convention for the smaller, later edit.

Two boundaries bound the answer below. Version: the answer is written against
ITWS 1.0.0 and its amendments of 2026-08-04. Dependencies: none, because the
disclosure is a declaration and not a computed value. Environment, capacity,
security, privacy, and data-provenance dimensions do not apply to a declaration
field.

## Alternatives

### A per-cell disclosure costs more than it returns

Each edited cell, or each edited sheet, would carry its own disclosure. The
record would then name exactly which values a tool produced.

We rejected the option on three grounds. Core §0.5 attaches the disclosure to the
governed unit, and a `data-table` is one unit. Rule §4.14.14 already treats a row
identifier, a column header, and a closed-set value as metadata. A per-cell field
would add a fourth metadata class that no rule asks for. The bookkeeping also
grows without limit: a workbook of 900 rows would carry 900 disclosures.
[STY-69](https://linear.app/inveneprod/issue/STY-69) reports that per-record cost
as unaffordable on the comment surface.

### A disclosure tied to approval would put process inside the text

The original question named post-approval cell edits. That framing would have the
disclosure annotate itself when an edit follows an approval.

We rejected the option because ITWS governs text and not process. Core §0.5
states that the declaration block is the only process artifact ITWS defines. No
rule turns on an event outside the document, and an approval is such an event.

### The workbook keeps one disclosure

The workbook carries one disclosure, updated when the tooling's contribution
changes. We selected this option.

### Reversibility differs across the three

Adding a per-cell field later would leave every existing workbook conforming.
Removing one afterwards would invalidate every workbook that had adopted it.
Neither alternative raises a capacity, security, privacy, or data-classification
concern, because a disclosure names tooling and not content.

## Decision

We propose that a `tabular-document` declares exactly one `AI disclosure` value.
The value sits on the Title sheet and covers the whole workbook. No cell, row,
column, or sheet carries a disclosure of its own.

An edit to any cell is an edit to the workbook. The writer updates the Title
sheet note to describe what the tooling did. Core §4.3.4 places that obligation
on every other governed unit already.

Where several tools contributed, the note lists each contribution in order. The
note then ends with the human review status. `AGENTS.md` already states that form
for a corpus, and the table surface adopts it unchanged.

## Consequences

The `data-table` profile keeps every rule and slot it already has. This record
assigns no rule identifier. Workbooks written against ITWS 1.0.0 stay conforming,
because the answer keeps their existing behaviour.

One cost is real, and we accept it. A workbook edited across years accumulates
one note describing a growing list of contributions. A reader cannot tell from
that note which cells any one tool produced. The workbook's version history
carries that detail, and ITWS makes no claim to replace a version history.

A second cost bounds the first. A note that grows without editing will eventually
exceed what a Title-sheet cell displays. We know of no threshold at which the
note becomes unreadable. We have not tested one, so the writer's judgment governs
the length until evidence sets a bound.

One condition would justify revisiting the decision: a reader needs per-cell
provenance often enough to build it by hand. A workbook that grows a provenance
column of its own is the observable signal. Rule §4.14.13 governs that column as
ordinary prose and not as a disclosure.

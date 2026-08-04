ITWS version: 1.0.0
Profile: decision-record
AI disclosure: generated — drafted every section from the STY-79 ticket and the ITWS 1.0.0 rule set; not yet reviewed

# A CSV set names its sheets in its filenames

## Status

Proposed. No superseding record exists.

Recorded against [STY-79](https://linear.app/inveneprod/issue/STY-79), the ticket
carrying both questions the spreadsheet-overlay proposal left open. This record
answers the second.

## Summary

A workbook delivered as separate files names each sheet in its own filename. The
pattern is `<workbook>-<sheet>.csv`. We propose the filename convention in place
of a manifest file. [Decision](#decision) carries the exact statement.

## Context

A *tabular document* is a workbook of named sheets that ITWS governs as one unit
(<https://github.com/invene/writing_spec/blob/1.0.0/spec/profiles/data-table.md>).
Three sheet kinds are required. The *Title sheet* holds the workbook's identity
and its declarations. The *Glossary sheet* defines every column and every
admitted term. A *data sheet* holds rows under one header row.

A *carrier* is the file format a workbook arrives in. Core §0.2 states that the
carrier is not a conformance surface. A workbook conforms or fails on the same
terms in every carrier.

The set of separate files is the case that needs an answer. A `.xlsx` file and a
hosted sheet both store a name for every sheet. Rules §4.14.1 through §4.14.4
read those names directly. A set of separate files stores no such name. A reader
then cannot tell which file is the Title sheet. The required-sheet rules have
nothing to read. A reader cannot settle them.

Two boundaries bound the answer. Version: the answer is written against ITWS
1.0.0 and its amendments of 2026-08-04. Dependencies: the answer assumes only
that filenames survive storage and transfer. We have surveyed no delivery format
against that assumption, which therefore stays untested. Capacity, security,
privacy, and data-provenance dimensions do not apply to a naming convention.

## Alternatives

### A manifest file drifts from what it describes

One extra file would map each filename to a sheet name and kind. A sheet name
could then hold a character a filename cannot.

We reject the option because the manifest is a second artifact describing the
first. The two drift apart on the first rename that touches only one of them.
[STY-63](https://linear.app/inveneprod/issue/STY-63) reports that failure on the
comment surface. A quarter of one corpus pointed at the wrong place. The
derived record had fallen out of step with what it described.

### A positional convention breaks without an edit

The files would be ordered, and the first would be the Title sheet. We reject
the option because file ordering is not preserved. A copy, an archive, a
download, and a listing each apply their own order.

### Silence is what produced the question

The specification would stay silent, and each delivery would invent its own
answer. We reject the option because every consumer would guess, and the
guesses would differ.

### The filename convention survives every move

We propose this option. A workbook that adopts the convention repackages as a
`.xlsx` file without loss, because the sheet names survive the move. A workbook
that later adds a manifest keeps its filenames. Anyone who ignores the manifest
still reads the set.

## Decision

We propose that a workbook delivered as separate files names each file
`<workbook>-<sheet>.csv`. One shared `<workbook>` name identifies every file in
the set.

Two suffixes are reserved. The file ending `-title.csv` is the Title sheet. The
file ending `-glossary.csv` is the Glossary sheet. Every other file in the set is
a data sheet. The text between the shared name and `.csv` is that sheet's name.

The convention assigns no rule identifier and adds no rule. Rules §4.14.1 through
§4.14.4 already require the sheets, and this record states how a set of separate
files expresses them. A workbook in any other carrier is untouched.

## Consequences

A reader can now name every sheet from a directory listing alone. The
required-sheet rules become decidable on this carrier.

Two costs follow, and we accept both. A sheet name is limited to what a filename
holds. A name containing a slash or a colon must be rewritten. We accept the
limit because a sheet name is a short label and not prose. Rule §4.14.14 already
treats a column header as metadata.

A set of files carries no enforced link between its members. A file dropped from
the set leaves a workbook that looks complete. Nothing in this record detects the
loss, and nothing in ITWS does either. A reader who looks for a Title sheet finds
it missing. We have not tested whether readers reliably notice, and we make no
claim that they do.

One condition would justify revisiting the decision: a workbook holds sheet names
that cannot survive a filename. A set that renames sheets to fit the convention
has reached that condition. A manifest becomes the better trade at that point.

# Profile: `data-table`

**ITWS version:** 1.0.0 · **Surface:** `tabular-document` · **Family:** reference

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Inventory homogeneous items as rows against a fixed column schema. Reader looks up one row, compares rows, or audits coverage.

**This profile governs a workbook, not a Markdown document.** Sustained argument, narrative, and single-decision records belong in other profiles; a `data-table` may accompany one as a companion unit. A workbook that computes is outside scope (core §0.3).

A core rule naming a document element — heading, section, figure, equation, bounded block — is inapplicable here, because the construct is absent (core §0.2).

## Shallow-model outcome (core §4.12.2)

The scan surface lets the assumed reader state **what the table inventories, what kind of claim each row makes, how to read each column, and the coverage limits of the whole table** — without opening any data row.

## Tabular vocabulary

Available without definition in this profile.

**data sheet** — one named sheet holding homogeneous rows under exactly one header row. **header row** — row 1 of a data sheet, one cell per column, holding column names. **column schema** — the ordered column set one data sheet's rows share. **registry** — the Glossary sheet: the document's complete column and term definitions. **row ID** — the stable identifier one row carries in its own column, used for every cross-row reference. **scan surface** — this profile's replacement for the core §4.12.1 scan path, defined at §4.14.18. **closed value set** — the complete list of values a column admits, stated in that column's registry entry.

## Reader overlay (genre knowledge only)

The reader recognizes a workbook separating document identity (Title sheet), column and term definitions (Glossary sheet), and data grids under one header row. Navigation only.

The overlay grants **nothing else**. No product, system, operational, or domain vocabulary enters through it. A term appearing in a cell enters through the registry (§4.14.6).

## Skeleton — required sheets, in this order

Dependency order: seed identity and definitions before the rows depending on them (core §4.4.2).

| Sheet | Required | Job |
|---|---|---|
| Title | yes | key–value rows: title, the three core §0.5 declarations including `AI disclosure`, provenance ("Built from"), last-updated date, and the table's coverage and boundary statement. ! data facts |
| Glossary | yes | the registry, sectioned `Columns` then `Terms`: one entry per column of every data sheet, one entry per admitted term |
| data sheet | 1+ | homogeneous rows under one header row; row 1 = column headers, nothing above it |

**Renames:** `Glossary` → `Definitions` or `Legend`. **Merges:** none. No section map — sheet names carry no other rename.

An empty required Title field states `None` or `Not applicable` with a reason (core §4.4).

## Boundary locations (core §7.1)

- **Title sheet coverage and boundary statement** — every applicable dimension for the table as a whole: what it inventories, what it omits, the time window and source state it reflects, and the conditions under which a row stops being true.
- **Each row's boundary column(s)** — the coverage, status, and caveat content qualifying that row, named as boundary columns in their registry entries (§4.14.5).

## §4.14 Scoped rules — tabular documents

| ID | C | D | Rule |
|---|---|---|---|
| 4.14.1 | M | L | the three core §0.5 declarations live on the Title sheet |
| 4.14.2 | M | J | Title sheet ! carry data facts |
| 4.14.3 | M | S | Title sheet carries the table's coverage and boundary statement (core §7.1) |
| 4.14.4 | M | L | every column of every data sheet has exactly one registry `Columns` entry stating what its cells hold and how to read them, including closed value sets, key conventions, and units |
| 4.14.5 | M | L | each registry `Columns` entry declares its column's §7.3 role: observation, interpretation, or metadata |
| 4.14.6 | M | J | **registry replaces ladder** — named exception to §2.3.1 and §2.3.3: a table has no linear reading order, so define-before-first-use is unsatisfiable; instead every non-baseline term used in any cell has a registry `Terms` entry |
| 4.14.7 | M | J | a registry `Terms` entry meets the §2.4 definition-quality rules |
| 4.14.8 | M | S | a registry `Terms` entry satisfies the §2.1.4 first-use expansion obligation |
| 4.14.9 | M | J | named exception to §4.8.1: the per-page admission budget does not apply; the bound is registry completeness — a term used in a cell with no registry entry is a violation |
| 4.14.10 | R | J | a cell uses ≤ 3 non-baseline terms — the per-cell reader-effort bound replacing §4.8.1's per-page bound |
| 4.14.11 | M | J | one column = one meaning across the whole workbook |
| 4.14.12 | M | J | a cell carries only its column's declared content |
| 4.14.13 | M | J | a cell holding prose is a §4.1 chunk; §2, §3, §5, and §7 apply to it unchanged |
| 4.14.14 | M | L | a cell holding a row ID, a column header, or a value from a declared closed value set is metadata, ! governed prose; §3 sentence rules do not apply to it |
| 4.14.15 | M | L | each row carries a stable row ID in its own column |
| 4.14.16 | M | S | cross-row dependence uses the row ID; ! adjacency, row order, or sheet order |
| 4.14.17 | M | L | a required column with no value for a row states `None` or `Not applicable` with a reason; ! silent blank. A systematic absence states its reason once in that column's registry entry |
| 4.14.18 | M | L | **scan surface replaces scan path** — named exception to §4.12.1: scan surface = the Title sheet, then the sheet names in workbook order, then each data sheet's header row, then the registry `Columns` section. **§4.12.2–§4.12.4 still govern it unchanged.** |
| 4.14.19 | M | J | a material claim in a cell carries the §5.4 evidence record; a source shared by many rows may live once in the Title sheet provenance field, with each row's deviation recorded in that row |
| 4.14.20 | M | J | a caveat qualifying one row lives in that row (§7.2.1); ! only in the registry or on the Title sheet |
| 4.14.21 | R | S | a data sheet groups rows by a category column rather than by sub-sheets, so one header row governs every row |

§4.14.5 and §4.14.14 are the two rules that most often bite: a column's role is declared once rather than inferred per row, and a status value is not judged as prose.

## Evidence-record additions (core §5.4)

The source, its retrieval or observation date, and its coverage for each row's reported facts.

## Applicable core rules with profile scope

**§4.2.4 does not apply** (no linear main point). **§4.4.3 does not apply** (no early-then-precise restatement).

**§4.6.2 bounded blocks cannot exist on this surface.** A cell holds no blockquote. Two consequences bind: §6.3.1 makes informal explanation available **only** inside an Intuition block, and §7.3.2 makes a statement exceeding interpretive support available **only** inside a Speculation block. With neither construct available, both are prohibited outright in a `data-table`. Exact detail that §4.6.1 would send to a bounded block or appendix goes to a companion unit under its own profile.

**§3 caps are defined over sentences.** A column header is a noun phrase, not a sentence, so §3.1 and §3.5.1 do not fire on the header row. They govern every cell holding prose.

**§7.3 applies through the column schema.** Because each cell is its own unit, a column carries one role for every row, and §4.14.5 declares it in the registry. This makes §7.3.1 checkable from the Glossary sheet rather than by reading every row.

**§5.6 still governs strength.** A status column's closed value set is a lifecycle value, not a strength phrase (core §5.6, closing). A registry entry ! define a status value so that it reads as a calibrated strength claim.

**§4.9 (path-agnostic prose) applies unchanged**, and bites hardest in free-text columns. A note recording a superseded approach passes delete-or-promote (§4.9.3) like any other prose.

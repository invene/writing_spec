# Recorded check: the pilot `data-table` fixture

**This record carries no conformance claim of its own.** It is the session record STY-78 asks for, not a governed unit. The thing it checks is the workbook beside it.

- **Unit checked:** `document-search-inventory-*.csv`, a `tabular-document` carried as a CSV set.
- **Checked against:** ITWS 1.0.0 as amended 2026-08-04, `data-table` profile.
- **Checked on:** 2026-08-04, by generative AI tooling. Not yet reviewed by a person.
- **Ticket:** [STY-78](https://linear.app/inveneprod/issue/STY-78), under [STY-72](https://linear.app/inveneprod/issue/STY-72).

The fixture is a CSV set rather than a single workbook, which exercises the naming convention [decisions/0002](../../decisions/0002-csv-set-sheet-identity.md) settles: `-title.csv` and `-glossary.csv` are reserved, and every other suffix names a data sheet.

## CC-1 — no client-identifying content

**Pass.** Every row is invented. The workbook names no client, engagement, vendor, person, or production system, and the Title sheet's `Built from` row states that nothing stands behind any cell.

The source Alex supplied was already fictional and said so on its own Title sheet. The sweep confirmed it: no proper noun in the fixture refers to a real organization, and no cell carries a measurement, date, or identifier traceable to an engagement.

## CC-3 — findings

**Zero unwaived findings remain.** Ten findings were raised against the source workbook and all ten were repaired. **Every one was a fixture defect. None was a profile defect** — the profile held on its first real unit.

| # | Rule | Finding | Repair |
|---|---|---|---|
| 1 | §4.3.1 | `Profile: data-table (proposed)` is not a canonical §0.1 profile ID | Declares `data-table`. The lifecycle word also fails the §0.5 text-not-process boundary. |
| 2 | §4.14.2, skeleton | Title sheet carried no provenance row, which the skeleton requires | Added `Built from` |
| 3 | §4.14.3, §7.1.6 | `Scope` stated what the table covers, and not what it omits, the time window, or when a row stops being true | Added `Coverage`, `Omitted`, `Time window`, and `Not applicable` rows |
| 4 | §4.14.5 | No registry `Columns` entry declared its column's §7.3 role | All nine declare one |
| 5 | §4.14.6 | Eight non-baseline terms appeared in cells with no registry `Terms` entry — among them *token boundary*, *term frequency*, *index freshness*, *search cluster*, *container job* | Registry carries 14 entries, each used in at least one cell |
| 6 | §5.6.2, §4.14.19 | Two unmarked declarative claims carried verified-tier force with no evidence behind them: "Proven parsing libraries cover the supported formats" and "An inverted index answers term queries in near-constant time per term" | Every `Why this choice` cell now carries a §5.6 phrase, almost all `we decided`, and row Q2 carries `we propose` |
| 7 | §2.7.3 | The grid said *Text normalizer*, the registry said *Normalizer* | One name throughout |
| 8 | §4.14.17 | Rows X1 and X2 said `Not applicable.` with no reason | Each states the reason: the approach was not taken |
| 9 | §0.5 | Column C8 read "pending operational review", conditioning content on an event outside the document | Reads "a design intention, not a deployed fact, because nothing in this fixture has been built" |
| 10 | §4.14.13 → §3.1.1 | Several cells ran past the sentence caps | No sentence in a governed cell exceeds 20 words |

Finding 4 is the one the profile predicts. `spec/profiles/data-table.md` names §4.14.5 as a rule that "most often bites", and it was missing from all nine columns of a workbook that otherwise looked finished.

## CC-2 — coverage

Every rule below was evaluated. `mechanical` marks a result a script decided; everything else was decided by reading.

### `data-table` scoped rules

| Rule | Result |
|---|---|
| §4.14.1 declarations on the Title sheet | pass, mechanical |
| §4.14.2 Title sheet carries no data facts | pass |
| §4.14.3 Title sheet carries coverage and boundaries | pass |
| §4.14.4 one registry `Columns` entry per column | pass, mechanical — 9 of 9 |
| §4.14.5 each `Columns` entry declares its §7.3 role | pass, mechanical |
| §4.14.6 registry replaces the ladder | pass — which terms are non-baseline is my judgment, recorded below |
| §4.14.7 `Terms` entries meet §2.4 | pass, partly mechanical — all ≤ 2 sentences and ≤ 40 words |
| §4.14.8 first-use expansion | not triggered — no acronym or initialism appears |
| §4.14.9 registry completeness replaces the page budget | pass |
| §4.14.10 (R) cell uses ≤ 3 non-baseline terms | pass, mechanical |
| §4.14.11 one column, one meaning | pass |
| §4.14.12 cell carries only its column's declared content | pass |
| §4.14.13 a prose cell is a §4.1 chunk | pass — §3.1 mechanical, §2, §5, §7 by reading |
| §4.14.14 IDs, headers, closed-set values are metadata | pass — C1 through C4 declared metadata |
| §4.14.15 stable row ID per row | pass, mechanical |
| §4.14.16 cross-row dependence uses the row ID | pass, mechanical — every `row Xn` resolves |
| §4.14.17 no silent blank | pass — the five empty `Notes` cells are covered by C9's systematic-absence statement, which §4.14.17 permits |
| §4.14.18 scan surface replaces the scan path | pass — walked, below |
| §4.14.19 material claim carries its evidence record | pass — the shared `Built from` row states that no source stands behind any cell |
| §4.14.20 a row's caveat lives in that row | pass — row Q2's caveat sits in row Q2 |
| §4.14.21 (R) group by a category column | pass |

### Core rules

| Rule | Result |
|---|---|
| §0.5 three declarations, closed values, note form | pass, mechanical |
| §2.1.1, §2.1.2 one meaning, no synonym swap | pass |
| §2.1.4 acronym expansion | not triggered |
| §2.3.1, §2.3.3 term ladder | displaced by §4.14.6 |
| §2.4.1–§2.4.5 definition quality | pass |
| §2.6.1–§2.6.11 prohibited patterns | pass, mechanical |
| §2.7.1 coined name gets a plain introduction | pass — each `Technology` name is introduced by its `Role in the stack` cell |
| §2.7.3 one name per artifact | pass |
| §2.7.4 version pin | not triggered — no external artifact is referenced |
| §3.1.1–§3.1.4 length | pass, mechanical |
| §3.2 one idea per sentence | pass |
| §3.3 voice, §3.4 tense | pass |
| §3.5 noun clusters | pass |
| §3.6.1, §3.6.2 reference | pass, mechanical |
| §3.7 ambiguity controls | pass |
| §3.8.1–§3.8.3 punctuation and connectives | pass, mechanical |
| §3.9.1, §3.9.2 hedging | pass, mechanical |
| §3.10.1–§3.10.6 formulaic constructions | pass, mechanical |
| §4.1.1 one purpose per chunk | pass |
| §4.2.4 document main point | does not apply to this profile |
| §4.3.1–§4.3.4 one job, slots, disclosure | pass, mechanical |
| §4.4.1, §4.4.2 skeleton and dependency order | pass |
| §4.4.3 plain-then-exact restatement | does not apply to this profile |
| §4.6 bounded blocks | cannot exist on this surface, so §6.3.1 and §7.3.2 bar informal explanation and beyond-interpretive statements outright. Neither appears. |
| §4.8.1 admission budget | displaced by §4.14.9 |
| §4.9.1–§4.9.3 path-agnostic prose | pass — rows X1 and X2 state rejected approaches as current facts, not as history |
| §4.10.5 emoji | pass, mechanical |
| §4.12.1 scan path | displaced by §4.14.18 |
| §4.12.2–§4.12.4 scan-path quality | pass — walked, below |
| §5.1.1, §5.1.2 exactness | pass |
| §5.4.1–§5.4.6 evidence record and locators | pass — the one external reference, STY-78, carries its URL |
| §5.6.1, §5.6.2 strength | pass, mechanical — every `Why this choice` cell carries a closed-vocabulary phrase |
| §7.1.1–§7.1.6 boundary content | pass — the Title sheet names each applicable dimension and each inapplicable one |
| §7.2.1, §7.2.2 caveat placement | pass |
| §7.3.1 observation and interpretation | pass — no column declares the observation role, and nothing is reported as observed |
| §7.4 beyond established boundaries | not triggered |

### Not checked

§5.2 notation and §5.3 equations — no symbol or equation appears. §5.5 figures and tables — the unit is the table. §6.1 through §6.5 explanatory devices — no analogy, worked example, intuition block, or diagram appears. §5.7 and §5.8 belong to other profiles.

## The scan surface (§4.14.18)

Read in order: the Title sheet, then the sheet names, then each data sheet's header row, then the registry `Columns` section. That reading gives the profile's shallow-model outcome without opening a data row.

- **What the table inventories** — the components of a fictional document search service, one per row, plus the approaches it rejected.
- **What kind of claim each row makes** — the `Columns` roles say it: C1 through C4 are metadata, C5 through C9 are interpretation, and no column is observation. Nothing here is measured.
- **How to read each column** — nine registry entries, including the closed value sets on `Category` and `Build or reuse`.
- **The coverage limits** — the Title sheet states what the table covers, what it omits, the time window, when a row stops being true, and which boundary dimensions do not apply.

Status and strength survive the scan: the Title sheet's `Built from` row says nothing stands behind any cell, so no reader can take a scan of this table for evidence about a real system.

## Missing facts

None. The fixture is fictional by declaration, and the `Built from` row records that rather than leaving a reader to infer it. No cell was filled with an invented value standing in for a real one, which is the failure core §8 obligation 2 exists to prevent.

## What this says about the profile

The profile held. Every one of the ten findings was a defect in the workbook rather than in the rules, and no rule turned out to be unsatisfiable, ambiguous, or in conflict with another on this surface.

Two mechanisms earned their keep on first use. §4.14.17's systematic-absence escape let one registry entry explain five empty cells, instead of five cells each repeating `Not applicable`. The [decisions/0002](../../decisions/0002-csv-set-sheet-identity.md) filename convention was load-bearing rather than decorative: without it nothing identifies which of three files is the Title sheet, and §4.14.1 through §4.14.4 have nothing to read.

# Invene Technical Writing Specification (ITWS)

**Version 1.0.0** · controlled English for technical documents

ITWS gives a working technical reader a **correct shallow model at low reading cost**, while the main text stays complete for the document's declared job and exact detail stays reachable. Conformance does not depend on who or what wrote the text.

One shared core plus thirteen document profiles. A governed unit declares one profile and applies the core plus that profile.

## Breaking change in 1.0.0

1.0.0 replaces the tool-backed 0.10.0-draft tree with a markdown-only specification.

**Removed:** the `itws` Python package, every `tools/` command, the test suite, the generated navigation catalog under `spec/generated/`, the numbered chapter files, Annexes A–G as separate documents, and the `spec/overlays/` directory.

**Consequence:** there is no machine `pass` / `fail` result. A document is checked by a reader or an agent citing rule IDs. Conformance claims made against 0.10.0-draft do not carry over — re-check against 1.0.0, or keep citing the older version.

**Kept:** every permanent rule ID. §2.1.1 in 1.0.0 is the rule §2.1.1 was in 0.10.0-draft. Existing citations remain valid.

## Layout

```text
spec/legend.md          notation and the voice fence — read first
spec/ontology.md        external standards ITWS borrows from, and where it forks them
spec/core.md            the shared normative core
spec/phrases.md         literal prohibited and replacement strings
spec/glossary.md        canonical admitted terms
spec/reader.md          what the assumed reader knows
spec/profiles/*.md      one file per profile
skills/itws-rewrite/    Claude skill for a consumer session
decisions/              recorded decisions about the specification
appendices/             non-normative background, outside the load set
fixtures/               worked example units, outside the load set
tools/                  optional, non-normative; outside the load set
AGENTS.md               working instructions for agent sessions
CHANGELOG.md            version history
```

Every rule carries three markers: an ID, a class (`M`/`R`/`P`), and a decidability (`D`) saying whether a machine settles it — `L` literal, `S` screened, `J` judgment. `D` allocates attention; it changes no rule's force.

`tools/itws_literal.py` screens a corpus for the `L` and `S` rules and reports what it did not evaluate. It decides no conformance question, no rule refers to it, and deleting it changes no obligation.

## Profiles

`design-rfc` · `decision-record` · `procedure` · `explanation` · `incident` · `technical-report` · `research-paper` · `investigation-log` · `epic` · `task` · `subtask` · `maintenance-comment` · `data-table`

## Using it

Load `legend` → `ontology` → `core` → `phrases` → `glossary` → `reader` → **exactly one** profile. That set is the complete applicable rule set; there is nothing else to retrieve. It runs 22,883–27,059 tokens depending on the profile.

The rules are guidance a writer applies with judgment. An `M` rule is the strong default: apply it unless applying it makes the passage worse, then report the departure. The owner of the document has final say.

A governed unit declares:

```text
ITWS version: 1.0.0
Profile: design-rfc
AI disclosure: assisted — drafted the rollout section
```

The `AI disclosure` field is `none`, `assisted`, or `generated`. It records provenance for transparency; it never affects how the rules apply.

Three obligations carry across every session: cite a rule ID for every finding, report a missing fact instead of generating one, and continue around unresolved spans — returning the best safe draft plus a missing-fact list.

**ITWS governs text, not process.** The declaration block above is the only process artifact the specification defines. The disclosure records provenance, not review. No rule records review state, approval state, or lifecycle position, and none turns on a workflow event: a review, an approval, or a lifecycle transition.

[AGENTS.md](AGENTS.md) has the full sequence.

## A note on voice

The specification is written in compressed notation for agent reading. **Governed documents are not.** Documents written against ITWS use normal professional English. [spec/legend.md](spec/legend.md) states the fence.

## Where it comes from

ITWS assembles existing standards — ASD-STE100, PlainLanguage.gov, the Google and Microsoft style guides, Diátaxis, ISO/IEC/IEEE 26514, IEC/IEEE 82079-1, RFC 2119, IPCC calibrated uncertainty language, and others. [spec/ontology.md](spec/ontology.md) names each source, says whether you need to recall it, and states exactly where ITWS forks it.

ITWS-original: the two-layer exact/plain model, the term ladder, the scan path, path-agnostic prose, the work-item hierarchy, the maintenance-comment surface, and the tabular-document surface.

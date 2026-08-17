# ITWS ontology — external standards

**ITWS version:** 1.0

ITWS is assembled from existing standards. This file names them so the rest of the specification can state **deltas only**.

## Recall policy

| Recall | Meaning |
|---|---|
| `required` | ITWS depends on this. Core states every obligation ITWS takes from it. Do not fetch. |
| `optional` | If you already know it, use it as background. If you do not, ITWS still works — core states every ITWS obligation. Fetch only if a judgment call turns on the source's own wording. |

Rule of thumb: **never block on a fetch.** Every ITWS obligation is stated in [core.md](core.md), [phrases.md](phrases.md), and the profile file. External sources explain *why* a rule exists; they never add a requirement. A source ITWS forks from is authoritative for its own content and **not** for ITWS — where they differ, ITWS wins.

These standards change on multi-year cycles. A recalled version some years stale is acceptable background.

## Anchors — general (all 16 profiles)

| Source | ITWS borrows | Recall | Where |
|---|---|---|---|
| RFC 2119 / RFC 8174 | conformance keywords (shall / should / may) | required | https://www.rfc-editor.org/rfc/rfc2119 · https://www.rfc-editor.org/rfc/rfc8174 |
| ASD-STE100 (Simplified Technical English) | rule anatomy, permanent rule IDs, sentence rules, dictionary-entry format, checker practice | optional | https://asd-ste100.org/ |
| PlainLanguage.gov | audience focus, active voice, main-point-first ordering, headings | optional | https://www.plainlanguage.gov/guidelines/ |
| Google Developer Style Guide | word use, punctuation, naming, timeless documentation, example quality | optional | https://developers.google.com/style |
| Microsoft Writing Style Guide | word use, acronyms, passive-voice exceptions | optional | https://learn.microsoft.com/style-guide/welcome/ |
| Diátaxis | one job per document; explanation ≠ instruction | optional | https://diataxis.fr/ |
| Information Mapping / DITA topic typing | chunk purpose, modular structure, metadata filtering | optional | https://en.wikipedia.org/wiki/Information_mapping |
| ISO/IEC/IEEE 26514 | audience analysis, information structure, content quality, verification | optional | https://www.iso.org/standard/80699.html |
| IEC/IEEE 82079-1 | task-oriented instruction, warning placement at the hazard, usability | optional | https://webstore.iec.ch/publication/60697 |
| ISO/IEC Directives Part 2 · ISO 704 · ISO 10241 | requirements language, precedence discipline, definitions, terminology records | optional | https://www.iso.org/directives-and-policies.html · https://www.iso.org/standard/38109.html |
| IPCC calibrated uncertainty language | claim-strength calibration mechanism | optional | https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf |
| Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup) | prohibited vocabulary, formulaic constructions, formatting tells | optional | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing |
| Semantic Versioning 2.0.0 | major and minor change categories | optional | https://semver.org/ |
| Keep a Changelog 1.1.0 | change-log format | optional | https://keepachangelog.com/ |

## Scan-path evidence

Core §4.12 rests on reading and memory research. Recall `optional`. The rules are complete on their own.

Trust your own recall of that research and your judgment of the §4.12 rules. Open the evidence appendix only when a judgment call on §4.12 genuinely turns on a citation. Never block on opening it. The appendix is outside the load set: [appendices/scan-path-evidence.md](../appendices/scan-path-evidence.md).

## ITWS deltas — where ITWS forks its sources

Do not resolve these from the source. Core is authoritative.

| Area | Source | ITWS delta |
|---|---|---|
| Vocabulary | ASD-STE100 closed dictionary | **open but gated**: any term is usable once admitted through the term ladder (§2.3) |
| Document types | Diátaxis four types | **sixteen profiles** (§0.1); one-job discipline kept, registry replaced. `role-specification` is explanation-family with a named Screening exception to explanation ≠ instruction |
| Prose layers | — | **two-layer model** (§1.2): plain wraps exact, never replaces it — ITWS-original |
| Notation | — | term ladder extended to **symbols** (§5.2) — ITWS-original |
| Context | Google timeless documentation | extended from time-relative to **decision-path-relative** prose (§4.9) — ITWS-original |
| Claim strength | IPCC calibration | vocabulary re-cut for design, decision, incident, and investigation work (§5.6) |
| Skimming | — | **scan path** with a truth-preservation contract and per-profile shallow-model outcome (§4.12) — ITWS-original |
| Detail layering | NN/g progressive disclosure | **skip-coherence test** (§4.6.3) — ITWS-original |
| Work items | general work-item convention | **hierarchy, dual classification, path ownership, DoD composition** — ITWS-original |
| Code comments | Ousterhout; Google TODO format | **information delta, host anchor, durable basis, lifecycle, conflict-report** — ITWS-original |
| Review artifacts | — | **change-request** (host title + description as one unit) and **feedback-comment** (addressed to a person, about a change, expecting a response) — ITWS-original |
| Conformance | requirements practice | **guidance applied with judgment** against one declared version + profile; `M` = strong default, departures reported; owner has final say — ITWS-original |
| Reader | ISO 26514 audience analysis | **one fixed cross-functional software-pod baseline** ([reader.md](reader.md)) — ITWS-original |
| Versioning | Semantic Versioning 2.0.0 | **commit-addressed refs** (§9): third field = 12-hex SHA-1, not a patch counter. Tag name = version string. Spec files declare the line. A governed unit copies the tag. Hash-addressed names do not sort |

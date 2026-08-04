# ITWS ontology — external standards

**ITWS version:** 1.0.0

ITWS is assembled from existing standards. This file names them so the rest of the specification can state **deltas only**.

## Recall policy

| Recall | Meaning |
|---|---|
| `required` | ITWS depends on this. Core states every obligation ITWS takes from it. Do not fetch. |
| `optional` | If you already know it, use it as background. If you do not, ITWS still works — core states every ITWS obligation. Fetch only if a judgment call turns on the source's own wording. |

Rule of thumb: **never block on a fetch.** Every ITWS obligation is stated in [core.md](core.md), [phrases.md](phrases.md), and the profile file. External sources explain *why* a rule exists; they never add a requirement. A source ITWS forks from is authoritative for its own content and **not** for ITWS — where they differ, ITWS wins.

These standards change on multi-year cycles. A recalled version some years stale is acceptable background.

## Anchors — general (all 13 profiles)

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
| Semantic Versioning 2.0.0 · Keep a Changelog 1.1.0 | version and change mechanics | optional | https://semver.org/ · https://keepachangelog.com/ |
| Ousterhout, *A Philosophy of Software Design* (2018) | comments state what code cannot | optional | ch. 12–16 |

## Anchors — research only (`research-paper`; `technical-report` where noted)

| Source | ITWS borrows | Recall | Where |
|---|---|---|---|
| IMRaD | research section order; results ≠ discussion | optional | https://en.wikipedia.org/wiki/IMRAD |
| APA JARS | method, statistical, and result-reporting disclosures | optional | https://apastyle.apa.org/jars |
| NeurIPS Paper Checklist · ML Reproducibility Checklist | reproducibility and limitations disclosure | optional | https://neurips.cc/public/guides/PaperChecklist |
| Model Cards · Datasheets for Datasets | artifact, data, and use-context disclosure | optional | https://arxiv.org/abs/1810.03993 · https://arxiv.org/abs/1803.09010 |

These four impose nothing outside `research-paper` and `technical-report`.

## Scan-path evidence

Core §4.12 (the scan path) rests on reading and memory research, not on a style tradition. Recall `optional`; the rules are complete without it.

Duggan & Payne 2009 (DOI 10.1037/a0016995) and 2011 (DOI 10.1145/1978942.1979114) — skim reading allocates attention; skimming does not deliver full comprehension. Hyönä & Lorch 2004 (DOI 10.1016/j.learninstruc.2004.01.001) — headings signal structure. Kintsch & van Dijk 1978 (DOI 10.1037/0033-295X.85.5.363) — gist vs detail. Gilbert et al. 1993 (DOI 10.1037/0022-3514.65.2.221) and Kaup et al. 2007 (DOI 10.1080/17470210600823512) — negations and late qualifications fail under constrained processing, which is why §4.12.3 requires affirmative content words. Schotter et al. 2014 (DOI 10.1177/0956797614531148) — rereading matters. Cowan 2001 (DOI 10.1017/S0140525X01003922) and Sweller 1988 (DOI 10.1016/0364-0213(88)90023-0) — working-memory limits behind the §4.8.1 admission budget.

ITWS derives no document-length target and no comprehension promise from these.

## ITWS deltas — where ITWS forks its sources

Do not resolve these from the source. Core is authoritative.

| Area | Source | ITWS delta |
|---|---|---|
| Vocabulary | ASD-STE100 closed dictionary | **open but gated**: any term is usable once admitted through the term ladder (§2.3) |
| Document types | Diátaxis four types | **thirteen profiles** (§0.1); one-job discipline kept, registry replaced |
| Prose layers | — | **two-layer model** (§1.2): plain wraps exact, never replaces it — ITWS-original |
| Notation | — | term ladder extended to **symbols** (§5.2) — ITWS-original |
| Context | Google timeless documentation | extended from time-relative to **decision-path-relative** prose (§4.9) — ITWS-original |
| Claim strength | IPCC calibration | vocabulary re-cut for design, decision, incident, and investigation work (§5.6) |
| Skimming | — | **scan path** with a truth-preservation contract and per-profile shallow-model outcome (§4.12) — ITWS-original |
| Detail layering | NN/g progressive disclosure | **skip-coherence test** (§4.6.3) — ITWS-original |
| Work items | general work-item convention | **hierarchy, dual classification, path ownership, DoD composition** — ITWS-original |
| Code comments | Ousterhout; Google TODO format | **information delta, host anchor, durable basis, lifecycle, conflict-report** — ITWS-original |
| Conformance | requirements practice | **binary textual conformance** against one declared version + profile — ITWS-original |
| Reader | ISO 26514 audience analysis | **one fixed cross-functional software-pod baseline** ([reader.md](reader.md)) — ITWS-original |

# Annex F — Mapping to source frameworks

**Status:** v0.2.1-draft. This annex is maintained at shared-core and profile granularity.

Annex C exposes generated `Source` and `Profiles` metadata for every rule. A disagreement between that metadata and this annex is a traceability defect.

This annex audits the goal of keeping the customization surface as small as possible.

The audit identifies forks, original content, and source applicability. `Original` marks content without a source framework.

A profile-specific source shall not be the sole basis for a shared-core requirement.

## F.1 General technical-writing anchors

These anchors apply across the shared core and all eight profiles:

- **ASD-STE100:** controlled-language architecture, rule anatomy, sentence rules, dictionary format, and checker practice.
- **PlainLanguage.gov, Google Developer Style Guide, and Microsoft Writing Style Guide:** audience-oriented wording, main-point-first organization, headings, naming, and usage guidance.
- **Diátaxis:** one-job-per-document discipline and separation of explanation, instruction, and other document modes. ITWS adapts Diátaxis but does not claim that Diátaxis defines all eight profiles.
- **ISO 26514 (ISO/IEC/IEEE 26514):** audience analysis, information structure, content quality, review, verification, and documentation lifecycle.
- **IEC 82079-1:** usable information for use, task-oriented instruction, warning/caveat placement, and evaluation.
- **ISO/IEC Directives Part 2, ISO 704, and ISO 10241:** requirements language, definitions, notes, and terminology records.
- **RFC 2119 / RFC 8174, Semantic Versioning, and Keep a Changelog:** conformance keywords and version/change mechanics.

Diátaxis, ISO 26514, and IEC 82079-1 are the general architecture anchors for the profile system. These anchors are not limited to research documents.

## F.2 Research-profile-specific anchors

The following sources are the basis for requirements specific to the `research-paper` profile:

- **IMRaD:** research-paper section order and the results/discussion distinction.
- **APA JARS:** research-method, statistical, and result-reporting disclosures.
- **NeurIPS Paper Checklist and the ML Reproducibility Checklist:** research reproducibility and limitations disclosures.
- **Model Cards and Datasheets for Datasets:** research artifact, data, limitation, and use-context disclosures.

These sources may inform examples or generally anchored rules in other profiles.

However, these sources do not independently impose conformance outside `research-paper`.

A similar shared-core or other-profile rule must cite a general anchor or be marked original.

## F.3 Traceability matrix (section granularity)

| ITWS area | Applicability | Source framework(s) | Nature of reuse |
| --- | --- | --- | --- |
| §0.1 Foreword | shared core | ASD-STE100 foreword structure | structural mirror |
| §0.2, 0.5, 0.6, 0.7 | shared core | ISO/IEC Directives Part 2; ISO 26514 | section and audience framework adapted |
| §0.3 Assumed reader | shared core | PlainLanguage.gov; Google audience guidance; ACM CS curriculum | format forked; working-software-engineer content pruned and original |
| §0.4 Conformance | shared core | RFC 2119 / RFC 8174 | keywords adopted; profile applicability and cumulative tier architecture **original** |
| §0.8 Versioning | shared core | SemVer 2.0.0; STE issue practice | semantics adopted; conformity mapping original |
| §1.1 Principles | shared core | PlainLanguage.gov; ASD-STE100; ISO 26514 | adapted |
| §1.2 Two-layer model | shared core | — | **original** core doctrine |
| §1.3 Rule anatomy | shared core | ASD-STE100 rule format | copied with applicability and metadata fields added |
| §1.4 Precedence | shared core | ISO/IEC Directives Part 2 | mechanism borrowed |
| §2.1–2.2 Word rules | shared core | ASD-STE100; Google/Microsoft word lists; frequency baseline | adapted; Annex B baseline original |
| §2.3 Term ladder | shared core | — | **original** core mechanism |
| §2.4 Definition quality | shared core | ISO 704; ISO 10241; ISO/IEC Directives Part 2 | adopted |
| §2.5 Glossary governance | shared core | ISO 10241 terminology-record practice | process adapted; profile metadata original |
| §2.6 Prohibited patterns | shared core | PlainLanguage.gov; Google; Wikipedia "Signs of AI writing" | adapted; exact catalog contains original items |
| §2.7 Naming | shared core | Google naming conventions | adapted |
| §3.1–3.5 Length, one idea, voice, tense, noun clusters | shared core | ASD-STE100 Parts 2–5; PlainLanguage.gov; Microsoft | forked; inline-math counting original |
| §3.6–3.8 Reference, ambiguity, punctuation | shared core | PlainLanguage.gov; Microsoft/Google; ASD-STE100 | forked |
| §3.9 Hedging | shared core | — | **original** link to claim calibration |
| §3.10 Formulaic constructions | shared core | Wikipedia "Signs of AI writing" | catalog converted to rules |
| §4.1 Chunk model | shared core | Information Mapping; DITA topic typing; ISO 26514 | mapped to an original purpose taxonomy |
| §4.2 Main point first | shared core | PlainLanguage.gov; BLUF; Minto pyramid | adopted |
| §4.3 Profile discipline | shared core + all profiles | Diátaxis; ISO 26514 | mode discipline forked; eight-profile registry original |
| §4.4 Structure and skeleton application | shared core + all profiles | Diátaxis; ISO 26514; IEC 82079-1 | general structure adapted; exact profile slots traced below |
| §4.5 Headings | shared core | PlainLanguage.gov; Google; ISO 26514 | adopted |
| §4.6 Progressive disclosure | shared core | NN/g progressive disclosure; DITA filtering | pattern adopted; skip-coherence test original |
| §4.7–4.8 Navigation and density budgets | shared core | ISO 26514 (navigation) | navigation adapted; budget values original |
| §4.9 Path-agnostic prose | shared core | Google timeless-documentation guidance | extended from time- to path-relativity; **original** |
| §4.10 Formatting | shared core | Wikipedia "Signs of AI writing"; ISO 26514 | catalog converted to rules |
| §5.1 Exactness principle | shared core | original | **original** core doctrine |
| §5.2 Notation | shared core | original; ASD-STE100 | term ladder applied to symbols; symbol reuse adapted |
| §5.3 Equations in prose | shared core | original | **original** |
| §5.4 General evidence reporting | shared core | ISO 26514; IEC 82079-1 verification practice; Wikipedia "Signs of AI writing" | reporting elements generalized; citation-integrity checks adapted |
| §5.4 Research-result additions | `research-paper` | APA JARS; NeurIPS Paper Checklist | research disclosures converted to overlay requirements |
| §5.5 Figures and tables | shared core | ISO 26514; APA/IEEE figure conventions; Nature-style figure guidance; original | general usability anchored generally; caption and research conventions additive |
| §5.6 Claim calibration | shared core | IPCC calibrated-uncertainty mechanism | mechanism forked; vocabulary adapted |
| §5.7 Statistical admission and reporting | `technical-report`, `research-paper` | original | **original**; term-ladder mechanism reused |
| §5.8 Reproducibility or verification | `technical-report`, `research-paper` | ISO 26514; IEC 82079-1; original | verification framing generalized; statement placement original |
| §5.8 Research reproducibility additions | `research-paper` | NeurIPS checklist; ML Reproducibility Checklist | research disclosures converted to overlay requirements |
| §6.1 Analogies | shared core | original | **original** operational rules; pedagogy literature informative |
| §6.2 Worked examples | shared core | Carroll minimalism; Google example guidance | forked |
| §6.3 Bounded intuition blocks | shared core | ASD-STE100 notes; ISO Directives note discipline; original | repurposed; exact-dependency rule original |
| §6.4 Diagrams | shared core | ISO 26514; IEC 82079-1; Google; original | assembled; admitted-terms constraint original |
| §6.5 Repetition | shared core | ASD-STE100; spaced-recall practice; Wikipedia "Signs of AI writing" | repetition generalized; hollow-summary prohibition adapted |
| §7.1 General limitations | shared core | ISO 26514; IEC 82079-1 | limits and warnings generalized |
| §7.1 Research-source adaptations within general rules | `research-paper` | NeurIPS checklist; Model Cards; Datasheets for Datasets | checklist fields adapted for research; general anchors govern universal applicability |
| §7.2 Caveat placement | shared core | ASD-STE100; IEC 82079-1 warning placement | caveat-as-warning mechanism forked |
| §7.3 Observation and interpretation | `incident`, `technical-report`, `research-paper`, `investigation-log` | ISO 26514; IPCC calibrated language; original | separation generalized; speculation-block mechanism original |
| §7.3 Research results/discussion | `research-paper` | IMRaD; APA JARS | research overlay formalized |
| §7.4 Generalization claims | shared core | ISO 26514 | scope discipline generalized |
| §7.4 Research additions | `research-paper` | NeurIPS checklist; APA JARS; CONSORT | research applicability disclosures adapted |
| §8.1 Checklist | shared core + profile overlays | STE checker workflows; original | generation approach adopted; pass assignment and regeneration triggers original |
| §8.2 Automated checks | shared core + profile overlays | Vale; STE checker practice; original | tooling adopted; severity and version-pin checks original |
| §8.3 Reader testing | shared core + profile overlays | PlainLanguage.gov; ISO 26514; teach-back method | adapted; pass/fail criteria original |
| §8.4 Reviewer roles | shared core | ISO 26514; IEC 82079-1; original | two-pass review adapted; finding-citation rule original |
| §8.5 Waivers | shared core | IEC 82079-1; engineering standards-deviation practice | pattern copied |
| Annex A | shared core + tagged profile entries | ASD-STE100 dictionary; ISO 704/10241 | format forked; ladder/profile fields original |
| Annex B | shared core + convention-only overlays | ACM CS curriculum; Diátaxis | base pruned; overlay boundary original |
| Annex C | shared core + profile applicability | ASD-STE100 rule summary | build artifact |
| Annex D | all profiles | ASD-STE100 paired-example convention | format forked; content original |
| Annex F | shared core + all profiles | requirements-traceability-matrix practice | format adopted |
| Annex G | shared core + all profiles | Keep a Changelog 1.1.0 | adopted |

### F.3.1 Annex E profile skeleton sources

| Profile | Source framework(s) | Nature of reuse |
| --- | --- | --- |
| `design-rfc` | Diátaxis; ISO 26514; general engineering RFC convention | one-job discipline adapted; exact required slots original assembly |
| `decision-record` | Diátaxis; ISO 26514; general decision-record convention | compact record convention adapted; exact policy original assembly |
| `procedure` | Diátaxis; IEC 82079-1; ISO 26514 | instructional sequence, verification, recovery, and warning structure adapted |
| `explanation` | Diátaxis; ISO 26514 | explanation mode adapted; ladder-seeding integration original |
| `incident` | ISO 26514; IEC 82079-1; general incident-record convention | fact/analysis and remediation structure assembled; exact slots original |
| `technical-report` | ISO 26514 | report structure, evidence, verification, and review adapted |
| `research-paper` | IMRaD; APA JARS; NeurIPS Paper Checklist; ML Reproducibility Checklist; Model Cards | IMRaD base forked; ladder-seeding and plain-language slots original |
| `investigation-log` | ISO 26514; general engineering log convention | traceable dated record adapted; append-only and path-agnostic constraints original |

## F.4 Reading the matrix

Sections marked **original** define ITWS's custom surface:

- the two-layer model;
- term ladder and governance;
- profile registry and exact slot assembly;
- path-agnostic prose;
- exactness principle;
- equations-in-prose rules;
- analogy constraints;
- ladder-seeding slots;
- density budgets; and
- Annex B's exact baseline.

All other areas assemble sourced mechanisms.

When promoting a requirement from one profile to the shared core, add a general anchor or mark the promoted mechanism original.

When narrowing a shared requirement to one profile, update its applicability metadata, Annex C, this matrix, and Annex G together.

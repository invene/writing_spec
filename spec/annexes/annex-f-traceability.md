# Annex F — Mapping to source frameworks

**Status:** v0.10.0-draft. This annex is maintained at shared-core and profile granularity.

Annex C exposes generated `Source`, `Profiles`, and `File` metadata for every rule. A disagreement between that metadata and this annex is a traceability defect.

This annex audits the goal of keeping the customization surface as small as possible.

The audit identifies forks, original content, and source applicability. `Original` marks content without a source framework.

A profile-specific source shall not be the sole basis for a shared-core requirement.

## F.1 General technical-writing anchors

These anchors apply across the shared core and all twelve profiles:

- **ASD-STE100:** controlled-language architecture, rule anatomy, sentence rules, dictionary format, and checker practice.
- **PlainLanguage.gov, Google Developer Style Guide, and Microsoft Writing Style Guide:** audience-oriented wording, main-point-first organization, headings, naming, and usage guidance.
- **Diátaxis:** one-job-per-document discipline and separation of explanation, instruction, and other document modes. ITWS adapts Diátaxis but does not claim that Diátaxis defines all twelve profiles.
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

## F.2.1 Attention, memory, and scan-path evidence

The scan-path language rules use the following peer-reviewed evidence:

- Duggan and Payne, "Text skimming: The process and effectiveness of foraging through text under time pressure," *Journal of Experimental Psychology: Applied* 15(3), 2009, 228–242, DOI 10.1037/a0016995.
- Duggan and Payne, "Skim reading by satisficing," *CHI 2011*, DOI 10.1145/1978942.1979114.
- Hyönä and Lorch, "Effects of topic headings on text processing," *Learning and Instruction* 14(2), 2004, 131–152, DOI 10.1016/j.learninstruc.2004.01.001.
- Kintsch and van Dijk, "Toward a model of text comprehension and production," *Psychological Review* 85(5), 1978, 363–394, DOI 10.1037/0033-295X.85.5.363.
- Pirolli and Card, "Information foraging," *Psychological Review* 106(4), 1999, 643–675, DOI 10.1037/0033-295X.106.4.643.
- Glenberg, Wilkinson, and Epstein, "The illusion of knowing," *Memory & Cognition* 10, 1982, 597–602, DOI 10.3758/BF03202442.
- Thiede, Anderson, and Therriault, "Accuracy of metacognitive monitoring affects learning of texts," *Journal of Educational Psychology* 95(1), 2003, 66–73, DOI 10.1037/0022-0663.95.1.66.
- Gilbert, Tafarodi, and Malone, "You can't not believe everything you read," *Journal of Personality and Social Psychology* 65(2), 1993, 221–233, DOI 10.1037/0022-3514.65.2.221.
- Kaup, Yaxley, Madden, Zwaan, and Lüdtke, "Experiential simulations of negated text information," *Quarterly Journal of Experimental Psychology* 60(7), 2007, 976–990, DOI 10.1080/17470210600823512.
- Schotter, Tran, and Rayner, "Don't believe what you read (only once)," *Psychological Science* 25(6), 2014, 1218–1226, DOI 10.1177/0956797614531148.
- Cowan, "The magical number 4 in short-term memory," *Behavioral and Brain Sciences* 24(1), 2001, 87–114, DOI 10.1017/S0140525X01003922.
- Sweller, "Cognitive load during problem solving," *Cognitive Science* 12(2), 1988, 257–285, DOI 10.1016/0364-0213(88)90023-0.

Duggan and Payne support attention allocation, not a promise of complete comprehension. Hyönä and Lorch support heading signals, not a universal heading template. Kintsch and van Dijk support a distinction between gist and detail. Glenberg and Thiede support generated checks over confidence ratings. The Thiede procedure delayed keyword generation until participants had read all six texts and set no elapsed-time threshold.

Gilbert and Kaup support review of negated or late qualifications under constrained processing. Schotter supports preserving rereading and non-linear access. Cowan and Sweller support budgeting working-memory demand under Rule 4.8.1. ITWS derives no numeric document-length target or full-comprehension promise from these sources.

## F.3 Traceability matrix (section granularity)

| ITWS area | Applicability | Source framework(s) | Nature of reuse |
| --- | --- | --- | --- |
| §0.1 Foreword | shared core | ASD-STE100 foreword structure | structural mirror |
| §0.2, 0.5, 0.6, 0.7 | shared core | ISO/IEC Directives Part 2; ISO 26514 | section and audience framework adapted |
| §0.3 Assumed reader | shared core | ISO 26514; PlainLanguage.gov; Google audience guidance | audience framework adapted; cross-functional software-pod baseline **original** |
| §0.2.1, §0.3.4 Governed surfaces and host supplement | shared core + `maintenance-comment` | original | **original**; the hosted comment set, declaration carrier, and conditional host-language supplement |
| §0.4 Conformance | shared core | RFC 2119 / RFC 8174 | keywords adopted; profile applicability and binary textual-conformance model **original** |
| §0.8 Versioning | shared core | SemVer 2.0.0; STE issue practice | semantics adopted; conformity mapping original |
| §1.1 Principles | shared core | PlainLanguage.gov; ASD-STE100; ISO 26514; Cowan; Sweller | effort optimization adapted; profile-relative completeness **original** |
| §1.2 Two-layer model | shared core | — | **original** core doctrine |
| §1.3 Rule anatomy | shared core | ASD-STE100 rule format | copied with applicability and metadata fields added |
| §1.4 Precedence | shared core | ISO/IEC Directives Part 2 | mechanism borrowed |
| §1.5 Layout and load set | shared core + all profiles | DITA topic modularity; ISO 26514 information architecture | modular separation adapted; overlay placement policy and load set **original** |
| §1.6 Rule navigation metadata | shared core + all profiles | DITA metadata and filtering; requirements-traceability practice | faceted metadata adapted; the closed value sets, the navigation/normative split, and generated precedence are **original** |
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
| §4.3 Profile discipline | shared core + all profiles | Diátaxis; ISO 26514 | mode discipline forked; twelve-profile registry original |
| §4.4 Structure and skeleton application | shared core + all profiles | Diátaxis; ISO 26514; IEC 82079-1 | general structure adapted; exact profile slots traced below |
| §4.5 Headings | shared core | PlainLanguage.gov; Google; ISO 26514 | adopted |
| §4.6 Progressive disclosure | shared core | NN/g progressive disclosure; DITA filtering | pattern adopted; skip-coherence test original |
| §4.7–4.8 Navigation and density budgets | shared core | ISO 26514; Cowan; Sweller | navigation adapted; working-memory rationale supported; budget values original |
| §4.9 Path-agnostic prose | shared core | Google timeless-documentation guidance | extended from time- to path-relativity; **original** |
| §4.10 Formatting | shared core | Wikipedia "Signs of AI writing"; ISO 26514 | catalog converted to rules |
| §4.11 Work-item hierarchy | `epic`, `task`, `subtask` | Diátaxis; ISO 26514; IEC 82079-1; original | one-job and verification principles adapted; hierarchy, classification, path ownership, and hint boundary **original** |
| §4.12 Scan path | shared core + all profiles | Duggan and Payne; Hyönä and Lorch; Kintsch and van Dijk; Gilbert et al.; Kaup et al.; Schotter et al.; original | attention and retrieval evidence adapted; exact path, truth-preservation contract, and profile outcome binding **original** |
| §4.13 Maintenance comments | `maintenance-comment` | Ousterhout 2018; Google style guides (code comments); Information Mapping; Duggan and Payne; original | information-delta and marker-format guidance adapted; anchoring, basis, lifecycle, conflict-report, and comment-set scan-path rules **original** |
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
| §5.9 Definition-of-done composition | `epic`, `task`, `subtask` | ISO 26514; IEC 82079-1; original | observable verification adapted; one-DoD and parent-child composition rules **original** |
| §6.1 Analogies | shared core | original | **original** operational rules; pedagogy literature informative |
| §6.2 Worked examples | shared core | Carroll minimalism; Google example guidance | forked |
| §6.3 Bounded intuition blocks | shared core | ASD-STE100 notes; ISO Directives note discipline; original | repurposed; exact-dependency rule original |
| §6.4 Diagrams | shared core | ISO 26514; IEC 82079-1; Google; original | assembled; admitted-terms constraint original |
| §6.5 Repetition | shared core | ASD-STE100; spaced-recall practice; Wikipedia "Signs of AI writing" | repetition generalized; hollow-summary prohibition adapted |
| §7.1 General limitations | shared core | ISO 26514; IEC 82079-1 | limits and warnings generalized |
| §7.1 Research-source adaptations within general rules | `research-paper` | NeurIPS checklist; Model Cards; Datasheets for Datasets | checklist fields adapted for research; general anchors govern universal applicability |
| §7.2 Caveat placement | shared core | ASD-STE100; IEC 82079-1 warning placement | caveat-as-warning mechanism forked |
| §7.3 Observation and interpretation | `incident`, `technical-report`, `research-paper`, `investigation-log`, `task`, `subtask` | ISO 26514; IPCC calibrated language; original | separation generalized; speculation-block mechanism original |
| §7.3 Research results/discussion | `research-paper` | IMRaD; APA JARS | research overlay formalized |
| §7.4 Generalization claims | shared core | ISO 26514 | scope discipline generalized |
| §7.4 Research additions | `research-paper` | NeurIPS checklist; APA JARS; CONSORT | research applicability disclosures adapted |
| §8.1 Textual conformance | shared core + all profiles | requirements-conformance practice; original | binary text property and separation from assurance **original** |
| §8.2 Machine checks | shared core + all profiles | STE checker practice; Google and Microsoft word-list adjudications; original | checker workflow adopted; phrase lists generated from rule-adjacent source; severity, version pinning, and coverage disclosure **original** |
| §8.3 Generated artifacts | shared core + all profiles | reproducible-build practice; requirements-traceability practice; original | content-hash pinning adapted; deterministic catalog and binary machine report **original** |
| Annex A | shared core + tagged profile entries | ASD-STE100 dictionary; ISO 704/10241 | format forked; ladder/profile fields original |
| Annex B | shared core + convention-only overlays | ISO 26514; Diátaxis | base and overlay boundary **original**; audience-analysis framework adapted |
| Annex C | shared core + profile applicability | ASD-STE100 rule summary | build artifact |
| Annex D | all profiles | ASD-STE100 paired-example convention | format forked; content original; §1.6 annotation fields **original** |
| Annex E §E.0.2 Section map | shared core + all profiles | DITA map and reltable practice | heading-to-slot mapping adapted; the closed rejection conditions are **original** |
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
| `epic` | Diátaxis; ISO 26514; general product-requirements convention | one strategic job and requirements structure adapted; exact slots and invariant inheritance original |
| `task` | ISO 26514; IEC 82079-1; general work-item convention | task orientation and verification adapted; classification, journey, path, and integrated-acceptance structure original |
| `subtask` | ISO 26514; general work-breakdown convention | traceable contribution adapted; one-parent and one-condition structure original |
| `maintenance-comment` | Google style guides (TODO format); Ousterhout 2018; original | comment-format guidance adapted; the carrier-field skeleton, anchor and provenance records, and conformance-evidence slot **original** |

## F.4 Reading the matrix

Sections marked **original** define ITWS's custom surface:

- the two-layer model;
- rule navigation metadata and generated precedence;
- the generated-artifact contract and the four validation states;
- term ladder and governance;
- profile registry and exact slot assembly;
- path-agnostic prose;
- the exact scan path, profile binding, and strengthened-foil contract;
- the overlay layout, placement policy, and load set;
- work-item hierarchy and path ownership;
- exactness principle;
- definition-of-done composition;
- equations-in-prose rules;
- analogy constraints;
- ladder-seeding slots;
- density budgets; and
- Annex B's exact baseline.

All other areas assemble sourced mechanisms.

When promoting a requirement from one profile to the shared core, add a general anchor or mark the promoted mechanism original.

When narrowing a shared requirement to one profile, update its applicability metadata, Annex C, this matrix, and Annex G together. Move the rule to the file that §1.5.2 requires for its new applicability.

## F.5 Removed dependencies

Version 0.6.0-draft removed Vale and its packaged Google and Microsoft rule sets from the toolchain. The reason is a consumption constraint, not a disagreement with those sources: the reference environment can run Python but cannot install a binary or fetch a style package, and §8.2 sets the tooling floor at what that environment can run.

The adjudications themselves remain. Parts 2 and 3 state each one, the phrase-list paragraphs of §8.2.1 make them machine readable, and the rows above still credit the Google Developer Style Guide and the Microsoft Writing Style Guide as their source. The change moved where the list lives, not where it came from.

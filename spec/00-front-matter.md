# Invene Technical Writing Specification (ITWS) — Front matter

**Version:** 0.2.1-draft · **Status:** self-conformance rewrite draft  
**Governs:** the eight technical-document profiles in §0.2

---

## 0.1 Foreword

This specification defines controlled English for technical documents. ITWS keeps content exact and usable by working technical readers who may not know the subject.

ITWS has one shared core and eight profiles. The core supplies the language, structure, exactness, explanation, and compliance rules that technical genres share. A profile supplies only the purpose, skeleton, and exceptions needed by one genre. This architecture avoids eight divergent style guides. The architecture also gives each genre distinct evidence and release obligations.

The specification adapts existing work. Its rule architecture comes from ASD-STE100 (Simplified Technical English). The architecture uses permanent numbered rules, one normative statement per rule, contrasting examples, explicit applicability, and controlled vocabulary. Existing standards and guides supply relevant content. Every rule names its source. Annex F preserves source-framework traceability.

The principal source frameworks are:

- ASD-STE100 — rule architecture, sentence rules, controlled vocabulary, and dictionary-entry format.
- PlainLanguage.gov federal plain-language guidelines — audience focus, voice, headings, and main-point-first ordering.
- Google Developer Style Guide and Microsoft Writing Style Guide — word use, punctuation, acronyms, naming, and developer-document conventions.
- Diátaxis — separation by reader need and discipline against mixing procedural and explanatory modes. ITWS generalizes that discipline across all eight profiles rather than adopting Diátaxis's four types as the profile registry.
- Information Mapping and DITA topic typing — chunk purpose, modular structure, and reusable information units.
- ISO/IEC/IEEE 26514 — software-documentation planning, audience analysis, content design, review, evaluation, and lifecycle controls.
- IEC/IEEE 82079-1 — principles for information for use, task-oriented procedures, warning placement, usability, and quality evaluation.
- ISO/IEC Directives Part 2 and ISO 704 — normative drafting, notes discipline, terms, and definitions.
- IMRaD and the pyramid principle — research structure and claim-first ordering where those mechanisms fit the selected profile.
- IPCC calibrated uncertainty language — claim-strength calibration.
- APA JARS, the NeurIPS Paper Checklist, the ML Reproducibility Checklist, Model Cards, and Datasheets for Datasets — research reporting, reproducibility, and limitations disclosure.
- RFC 2119 and RFC 8174 — conformance keywords.
- Semantic Versioning and Keep a Changelog — versioning and change records.
- Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup) — prohibited vocabulary, constructions, and formatting patterns.

The external sources are informative unless §0.5 says otherwise. Their requirements become normative only when an ITWS rule adopts them. This specification is for internal use. Annex F attributes adapted material.

## 0.2 Scope

ITWS governs prose documents that design, direct, explain, assess, or record technical work. A governed document uses the shared core and declares exactly one profile from the registry below. The profile identifier (ID) is canonical. Its label is the human-readable name.

| Canonical profile ID | Canonical label | Purpose |
|---|---|---|
| `design-rfc` | Design / RFC | Propose or specify a technical design, including requirements, interfaces, invariants, alternatives, and acceptance conditions. |
| `decision-record` | Architecture decision record | Record a decision, its context, considered alternatives, and consequences. |
| `procedure` | Runbook / how-to | Enable a reader to complete an operational or development task safely and repeatably. |
| `explanation` | Concept / explanation | Build an accurate mental model of a system, mechanism, or concept. |
| `incident` | Incident report / postmortem | Record impact, response, evidence, causes or contributing factors, and follow-up work. |
| `technical-report` | Technical report | Present a technical analysis, system, method, or result in sustained detail. |
| `research-paper` | Research paper | Report a research question, method, evidence, result, and limitations to publication standard. |
| `investigation-log` | Investigation log | Preserve dated questions, actions, observations, hypotheses, and next steps while an investigation proceeds. |

The registry contains the only ITWS 0.2 profiles. A document **shall** use one canonical ID and **shall not** combine profile IDs. A collection may contain several governed documents, but each document declares its own profile. Companion documents are preferable to a hybrid whose purpose and acceptance conditions cannot be determined.

The following are outside ITWS conformance:

- Source code and code comments.
- Standalone application programming interface (API) or command reference material. Interface definitions may appear inside an applicable governed profile.
- Slide decks, posters, and talk scripts.
- Marketing and general-audience communication.
- Chat messages, issue-tracker tickets, and review comments.

An out-of-scope document may reuse ITWS practices, but no ITWS conformance claim attaches.

## 0.3 The assumed reader (normative)

Every vocabulary, notation, and explanation rule resolves against this section and Annex B. The assumed reader has two components:

1. the **base reader**, shared by all profiles; and
2. the selected profile's **genre-knowledge overlay**.

The base reader is a **working software engineer**:

- They have roughly the knowledge of an Association for Computing Machinery (ACM) curriculum in computer science.
- They also have a few years of professional software work.
- They read and write code in their work. Common programming and software-practice concepts need no definition.
- They are not assumed to know the document's product, system, operational environment, scientific field, or other subject domain.

### 0.3.1 What may be assumed

The writer may use the following without definition, subject to Annex B's full enumeration:

- **Ordinary English:** contemporary general-purpose English used in its ordinary, nontechnical sense.
- **Programming concepts:** functions, parameters, arguments, return values, common data structures, recursion, iteration, state, caching, hashing, indexing, compilation, APIs, databases, queues, concurrency, and version control.
- **Software practice:** testing, benchmarks, regressions, profiling, logging and monitoring, debugging, latency/throughput trade-offs, configuration, dependency management, releases, and versioning.
- **General mathematics to first-year-undergraduate level:** algebraic manipulation, functions and graphs, logarithms and exponentials, summation notation, basic probability, percentages, averages, linear equations, and basic set notation.
- **Baseline notation** enumerated in §5.2 and Annex B.
- **Genre knowledge** explicitly granted by the selected profile overlay in Annex B.

Profile overlays grant only genre knowledge: the document conventions and reading strategies needed for that profile. They do not grant product, system, operational, scientific, or other domain vocabulary.

### 0.3.2 What may not be assumed

A domain term absent from the base-reader baseline **shall** enter through the term ladder (§2.3). This requirement applies even when specialists or frequent profile readers know the term. Familiarity is not operational knowledge.

The `research-paper` overlay expressly assumes **no machine-learning background**. The overlay does not assume machine-learning concepts, advanced statistics, linear algebra as manipulation, calculus, optimization, research-community shorthand, venue conventions, or dataset and benchmark names. Terms such as *model*, *training*, *loss*, *gradient*, *embedding*, *transformer*, *attention*, *fine-tuning*, and *inference* therefore require admission unless Annex B's versioned base list says otherwise.

The same rule applies outside research. A procedure does not inherit a service's internal vocabulary. An incident report does not inherit the incident team's system knowledge. A design RFC does not inherit the proposing team's architecture shorthand.

### 0.3.3 Disputes

Annex B decides whether the reader may know a concept, symbol, or genre convention. The reader does not know items absent from the base-reader list and selected overlay. A profile overlay cannot settle a domain-term dispute by adding domain knowledge. The document must admit the term. A proposal to add it to Annex B follows §0.8.

## 0.4 Conformance

### 0.4.1 Keywords

This specification gives five bold lowercase keywords the RFC 2119 meanings, as clarified by RFC 8174. The keywords are **shall**, **shall not**, **should**, **should not**, and **may**. Only these bold lowercase forms are normative. Unformatted instances carry their ordinary English meanings.

### 0.4.2 Rule classes

Every rule carries exactly one class:

- **Mandatory** — stated with **shall** or **shall not**. An unwaived violation is a conformance failure.
- **Recommended** — stated with **should** or **should not**. A deviation requires a recorded reason but is not a conformance failure.
- **Permitted** — stated with **may**. A permitted rule describes an allowed option and never creates a requirement.

### 0.4.3 Conformance statement

**Rule applicability.** A rule applies to all eight profiles by default. If a rule carries a `**Profiles:**` metadata line, it applies only to the canonical IDs on that line. Construct conditions still apply: for example, a universal equation rule is relevant only when a document contains an equation. §1.3 defines the metadata syntax.

**Conformance tiers.** ITWS has three cumulative tiers:

- **`core`** — The document satisfies every applicable mandatory shared-core and profile rule. An approved waiver covers each deviation. The author completes version-pinned linting and records a profile-aware self-check against the applicable checklist.
- **`reviewed`** — all `core` obligations, plus an independent subject-matter-owner pass over the exact layer and an independent reader-proxy pass over the plain layer. The two passes are performed by different people who are not authors of the document.
- **`publication`** — all `reviewed` obligations, plus an independent reader test and the release checks defined in Part 8. The test participant matches the base reader and profile overlay and is not an author, reviewer, or prior reader of a draft.

The profile sets the minimum tier:

| Profile | Minimum tier |
|---|---|
| `design-rfc` | `reviewed` |
| `decision-record` | `core` |
| `procedure` | `reviewed` |
| `explanation` | `core` |
| `incident` | `reviewed` |
| `technical-report` | `reviewed` |
| `research-paper` | `publication` |
| `investigation-log` | `core` |

A document **may** declare a tier above its profile minimum. The document **shall not** declare a lower tier. A higher tier adds assurance evidence. The higher tier does not remove or substitute any applicable content rule.

**Required declaration.** A conforming document **shall** declare the exact ITWS version, one canonical profile ID, and one permitted conformance tier:

```text
ITWS version: 0.2.1-draft
Profile: design-rfc
Conformance tier: reviewed
```

The human-readable profile label may accompany the ID but does not replace it. Conformance requires the declaration and complete evidence for the declared tier. The document must satisfy every applicable mandatory rule or receive a waiver under §8.5.

A partial audit may identify the parts or rules it checked, but it **shall not** claim ITWS conformance or declare a conformance tier. Cherry-picking rules does not establish conformance.

### 0.4.4 Version citation

A document is checked against its declared specification version, not the latest version. Tooling, applicability data, checklists, and reviewers **shall** use the declared version's materials. Those materials include its core, profile registry, Annexes A and B, rule metadata, and phrase lists. §0.8 guarantees that earlier versions remain checkable.

## 0.5 Normative references

The following documents are cited normatively. For dated references, only the cited edition applies.

- RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*; RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*.
- Semantic Versioning 2.0.0 — for §0.8.
- Keep a Changelog 1.1.0 — for Annex G.
- Annex A (Glossary) and Annex B (Assumed-Reader Baseline and Profile Overlays) of this specification — normative annexes, versioned with ITWS.

The standards and guides listed in §0.1 are informative sources. Annex F identifies what each ITWS rule adopts, adapts, or originates.

## 0.6 Terms and definitions

The following meta-vocabulary is available throughout ITWS without further definition.

- **governed document** — a document in §0.2's scope that declares one ITWS profile.
- **shared core** — rules and mechanisms common to all profiles unless explicit applicability metadata says otherwise.
- **profile** — one canonical genre contract from §0.2, including its purpose, skeleton, minimum tier, and profile-scoped rules.
- **profile overlay** — the selected profile's additions to the shared core, including the genre-knowledge overlay in Annex B.
- **conformance tier** — the cumulative assurance level (`core`, `reviewed`, or `publication`) declared by a governed document.
- **applicable rule** — a rule whose profile metadata and construct conditions include the document or passage under review.
- **base reader** — the working-software-engineer baseline defined in §0.3 and enumerated in Annex B.
- **assumed reader** — the base reader plus the genre-knowledge overlay for the document's declared profile.
- **genre knowledge** — knowledge of how to read and use a document genre, not knowledge of its subject domain.
- **domain term** — a technical word or phrase from a product, system, operational environment, profession, or field. The term is absent from the base-reader baseline.
- **subject-matter owner** — an independent reviewer qualified and authorized to accept the exact layer's technical correctness and completeness.
- **reader proxy** — an independent reviewer who checks the plain layer from the base reader's knowledge state plus the selected profile overlay.
- **reader test** — a direct test with a fresh representative reader, distinct from the reader-proxy review.
- **release checks** — final checks that conformance evidence, waivers, references, linked artifacts, and the released rendering are complete and resolve.
- **rule** — a permanent-ID normative unit in Parts 2–8, written in the §1.3 template.
- **admitted term** — a term defined in the current document under §2.3. When Annex A has an entry, the document uses its meaning and satisfies its prerequisites.
- **term ladder** — the §2.3 discipline of defining a term before first use with only assumed or previously admitted terms.
- **chunk** — a paragraph-level unit with exactly one purpose from the §4.1 taxonomy.
- **bounded block** — a visually delimited, labeled span whose detail the main text does not depend on (§4.6, §6.3, §7.3).
- **prior** — context deliberately introduced so later text may build on it (§4.9).
- **claim** — a proposition the document presents as true, at a strength governed by its evidence and §5.6.
- **caveat** — a statement limiting the scope, conditions, or strength of technical content (§7.2).
- **machine-checkable** — a rule property indicating that §8.2 tooling can detect a violation without human judgment.
- **waiver** — a recorded, approved deviation from a mandatory rule (§8.5).

Part 1 defines the exact and plain layers.

## 0.7 How to use this specification

**Self-application boundary.** This specification is outside §0.2 profile conformance. Its authored prose follows shared-core rules where meaningful. Quoted counterexamples, metadata, templates, tables, source names, and generated artifacts are fixtures.

**Writers.** Select the profile before drafting and select a tier no lower than that profile's minimum. Put the three required declarations in the document. Draft from the profile skeleton in Part 4 and Annex E. Resolve vocabulary against the base reader and selected overlay, not against the expected specialist audience. Before claiming `core`, run the pinned linter and complete the profile-aware self-check.

**Reviewers.** For `reviewed` and `publication`, the subject-matter owner checks the exact layer and the reader proxy checks the plain layer. Each finding cites a rule ID. A finding with no rule ID is an opinion or a candidate rule, not a conformance failure. The reader proxy is not the publication reader-test participant.

**Releasers.** For `publication`, confirm the independent reader-test record, final review state, approved waivers, version pin, references, linked artifacts, and released rendering. A green linter does not replace a human pass or reader test.

**Rule citation form:** "ITWS §3.2.1" cites a rule. "ITWS Part 3" cites a part. A bare "§3.2" cites a section. A scoped rule may also be described as "ITWS §x.y.z (`procedure`)." Rules, not sections or profile labels, are the unit of conformance.

**Precedence:** §1.4 resolves apparent collisions after §1.3 determines which rules apply. Writers and reviewers do not resolve collisions ad hoc.

## 0.8 Versioning and change policy

ITWS uses Semantic Versioning. Until 1.0, a minor version may contain breaking draft changes. The changelog **shall** identify them. The expansion from the research-only 0.1 draft to the shared-core/profile architecture is such a change. The expansion is released as 0.2.0-draft. After 1.0:

- **Major** — A change is major when it adds or tightens a mandatory rule. Upward reclassification, expanded profile applicability, and a higher profile minimum tier are also major. Adding, removing, or repurposing a canonical profile ID is major. Removing an assumed-reader baseline item is major. Any change that can make a previously conforming document non-conforming is major.
- **Minor** — A change is minor when it adds a recommended or permitted rule. Relaxation, downward reclassification, and narrower profile applicability are also minor. Adding a term to the assumed-reader baseline is minor. Adding a glossary entry or genre-knowledge item is minor unless it admits domain knowledge.
- **Patch** — wording, examples, and typographical corrections that do not change conformance, applicability, reader assumptions, or tier evidence.

**Permanent rule IDs.** A rule ID is assigned once and never reused, including across profiles. Changed wording or `Profiles` metadata does not give a rule a new ID. The version pin identifies the applicable form. New rules receive new IDs appended within their section.

**Deprecation over deletion.** A withdrawn rule, glossary entry, baseline item, profile ID, or tier mechanism remains in its historical release. Where the current text must mention a withdrawal, it marks the item *deprecated*, gives the deprecation version, and points to its replacement. A deprecated ID is never reassigned.

**Checkability guarantee.** A document citing version X **shall** remain checkable against X. Tagged releases retain the core, profile registry, Annexes A and B, Annex C applicability data, Annex F traceability, checklists, phrase lists, and compatible tooling. Rule applicability is historical data, not a property inferred from the latest text.

**Naming history.** Version 0.1 used the name *Research Writing Specification (RWS)*. That name and its four-type conformance model remain valid for documents that cite 0.1. ITWS does not retroactively rename or reinterpret the release.

**Living lists.** The prohibited-language lists, Annex A glossary, and Annex B baseline and overlays may change more often than rule text. They version with ITWS, follow §2.5 governance where applicable, and obey the compatibility rules above.

Annex G records all changes in Keep a Changelog format and identifies affected rule IDs, profiles, tiers, reader assumptions, and source mappings.

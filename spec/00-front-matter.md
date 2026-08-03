# Invene Technical Writing Specification (ITWS) — Front matter

**Version:** 0.10.0-draft · **Status:** language-process separation draft

**Governs:** the twelve technical-writing profiles in §0.2

---

## 0.1 Foreword

This specification defines controlled English for technical documents. ITWS gives working technical readers a correct shallow model at low reading cost. Main text remains complete for the document's declared purpose. Bounded blocks and appendices preserve optional resolution. Exact content remains available when the reader descends. This guarantee concerns access and orientation, not full-document learning or comprehension.

The reader may use the §0.3 baseline but need not know the document's subject. The design is especially useful for long or machine-drafted documents. Conformance does not depend on authorship.

ITWS has one shared core and twelve profiles. The core supplies the language, structure, exactness, explanation, and conformance rules that technical genres share. A profile supplies only the purpose, skeleton, and exceptions needed by one genre. This architecture avoids twelve divergent style guides without prescribing how an organization drafts, reviews, approves, or releases its text.

The specification adapts existing work. Its rule architecture comes from ASD-STE100 (Simplified Technical English). The architecture uses permanent numbered rules, one normative statement per rule, contrasting examples, explicit applicability, and controlled vocabulary. Existing standards and guides supply relevant content. Every rule names its source. Annex F preserves source-framework traceability.

The principal source frameworks are:

- ASD-STE100 — rule architecture, sentence rules, controlled vocabulary, and dictionary-entry format.
- PlainLanguage.gov federal plain-language guidelines — audience focus, voice, headings, and main-point-first ordering.
- Google Developer Style Guide and Microsoft Writing Style Guide — word use, punctuation, acronyms, naming, and developer-document conventions.
- Diátaxis — separation by reader need and discipline against mixing procedural and explanatory modes. ITWS generalizes that discipline across all twelve profiles rather than adopting Diátaxis's four types as the profile registry.
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

ITWS governs prose that designs, directs, explains, assesses, or records technical work. A governed unit uses the shared core and declares exactly one profile from the registry below. The profile identifier (ID) is canonical. Its label is the human-readable name.

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
| `epic` | Epic | Define one strategic product outcome, its scope, success measures, technical invariants, cross-task risks, and child-task boundaries. |
| `task` | Task | Specify one independently acceptable tactical outcome through a user journey or an explicit engineering-only contract. |
| `subtask` | Subtask | Verify one named completion condition under exactly one parent `task`, without creating an independent outcome. |
| `maintenance-comment` | Maintenance comment set | Preserve durable code knowledge by governing the comments one maintenance change adds, modifies, or removes. |

The registry contains the only ITWS 0.10.0-draft profiles. A governed unit **shall** use one canonical ID and **shall not** combine profile IDs. A collection may contain several governed units, but each unit declares its own profile. Companion documents are preferable to a hybrid whose purpose and acceptance conditions cannot be determined.

### 0.2.1 Governed surfaces

Each profile governs exactly one surface form:

- **`markdown-document`** — a prose Markdown document. The first eleven profiles govern this surface, and every reference to a "governed document" concerns it alone.
- **`hosted-comment-set`** — a comment change set inside a host source file, declared and recorded by a JSON declaration carrier. Only `maintenance-comment` governs this surface. The host source file itself remains outside ITWS conformance, and governed comments carry no ITWS boilerplate.

A rule that names a document element, such as a heading, a section, a figure, or an equation, is inapplicable to a hosted comment set when the construct is absent, exactly as §1.4 item 3 already provides. A hosted-surface profile states any genuine exceptions as named §1.4 layer-2 exceptions in its overlay.

The two terms are chosen, not interchangeable. A rule whose obligation holds on both surfaces names the **governed unit**, and every such rule reaches a comment change set. A rule that names the **governed document** is bounded to `markdown-document` and does not reach one. A rule **shall not** name the governed document for an obligation that reading or tooling applies to a hosted comment set, because the rule would then be enforced against a subject its own statement excludes.

An issue-tracker item is governed only when it declares `epic`, `task`, or `subtask`. The item **shall** also contain every required Annex E slot. Issue-tracker comments, status events, and unstructured tickets remain outside ITWS conformance.

The following are outside ITWS conformance:

- Source code. A code comment is governed only through a declared `maintenance-comment` comment change set; every other code comment remains outside conformance.
- Standalone application programming interface (API) or command reference material. Interface definitions may appear inside an applicable governed profile.
- Slide decks, posters, and talk scripts.
- Marketing and general-audience communication.
- Chat messages, issue-tracker comments and status events, unstructured tickets, and review comments.

An out-of-scope document may reuse ITWS practices, but no ITWS conformance claim attaches.

## 0.3 The assumed reader (normative)

Every vocabulary, notation, and explanation rule resolves against this section and Annex B. The assumed reader has two components:

1. the **base reader**, shared by all profiles; and
2. the selected profile's **genre-knowledge overlay**.

The base reader is a **working member of a software engineering pod**.

A software engineering pod is cross-functional. Its members may include software engineers, product designers, engineering managers, quality assurance (QA) specialists, product managers, and operations partners.

- They collaborate regularly on software design, delivery, testing, operation, or management.
- They can follow basic engineering discussions and artifacts common to software work.
- They know the concepts enumerated in Annex B, usually through practical exposure and proximity.
- They are not assumed to have a computer science education or write or review code.
- They are not assumed to match a seasoned software engineer's depth.
- They are not assumed to know the document's product, system, operational environment, scientific field, or other subject domain.

### 0.3.1 What may be assumed

The writer may use the following without definition, subject to Annex B's full enumeration:

- **Ordinary English:** contemporary general-purpose English used in its ordinary, nontechnical sense.
- **Basic software concepts:** functions, inputs, outputs, state, interfaces, APIs, clients and servers, requests and responses, files, databases, latency, and throughput.
- **Software delivery and quality:** requirements, acceptance criteria, bugs, tests, debugging, logs, monitoring, environments, deployments, releases, rollbacks, and version control.
- **Basic quantitative reasoning:** arithmetic, counts, ranges, percentages, ratios, rates, mean or average, median, and chance in its ordinary sense.
- **Baseline notation** enumerated in §5.2 and Annex B.
- **Genre knowledge** explicitly granted by the selected profile overlay in Annex B.

Profile overlays grant only genre knowledge: the document conventions and reading strategies needed for that profile. They do not grant product, system, operational, scientific, or other domain vocabulary.

### 0.3.2 What may not be assumed

A domain term absent from the base-reader baseline **shall** enter through the term ladder (§2.3). This requirement applies even when specialists or frequent profile readers know the term. Familiarity is not operational knowledge.

The `research-paper` overlay expressly assumes **no machine-learning background**. The overlay does not assume formal statistics, algebra beyond arithmetic, linear algebra, calculus, optimization, research-community shorthand, venue conventions, or benchmark names. Terms such as *model*, *training*, *loss*, *gradient*, *embedding*, *transformer*, *attention*, *fine-tuning*, and *inference* require admission.

The same rule applies outside research. A procedure does not inherit a service's internal vocabulary. An incident report does not inherit the incident team's system knowledge. A design RFC does not inherit the proposing team's architecture shorthand.

### 0.3.3 Disputes

Annex B decides whether the reader may know a concept, symbol, or genre convention. The reader does not know items absent from the base-reader list and selected overlay. A profile overlay cannot settle a domain-term dispute by adding domain knowledge. The document must admit the term. A proposal to add it to Annex B follows §0.8.

### 0.3.4 Host-language reader supplement

A hosted-comment-set profile adds one conditional supplement to the assumed reader. When the declaration carrier names a host adapter, the reader also has reading literacy in that host language's surface syntax and may treat an identifier visible in the anchored code as a repeatable name.

The supplement grants nothing else. The reader is not assumed to know the project's history, the product's vocabulary, the behavior of any library or service the code calls, or the author's intent. Annex B §B.4.12 states the complete supplement, and §0.3.3 governs disputes about it unchanged.

## 0.4 Conformance

### 0.4.1 Keywords

This specification gives five bold lowercase keywords the RFC 2119 meanings, as clarified by RFC 8174. The keywords are **shall**, **shall not**, **should**, **should not**, and **may**. Only these bold lowercase forms are normative. Unformatted instances carry their ordinary English meanings.

### 0.4.2 Rule classes

Every rule carries exactly one class:

- **Mandatory** — stated with **shall** or **shall not**. A violation is a conformance failure.
- **Recommended** — stated with **should** or **should not**. A deviation is not a conformance failure.
- **Permitted** — stated with **may**. A permitted rule describes an allowed option and never creates a requirement.

### 0.4.3 Conformance statement

**Rule applicability.** A rule applies to all twelve profiles by default. If a rule carries a `**Profiles:**` metadata line, it applies only to the canonical IDs on that line. Construct conditions still apply: for example, a universal equation rule is relevant only when a document contains an equation. §1.3 defines the metadata syntax. §1.5 states which file holds each rule.

**Binary result.** A governed unit either conforms or does not conform for one
declared ITWS version and profile. It conforms when it satisfies every
applicable mandatory rule and every required profile slot. Reviews, approvals,
reader tests, accepted deviations, and release checks do not alter this result.

**Required declaration.** A conforming governed unit **shall** declare the exact ITWS version and one canonical profile ID:

```text
ITWS version: 0.10.0-draft
Profile: design-rfc
```

A Markdown document carries the declaration in its front matter. A hosted comment set carries the same two fields in its declaration carrier (§0.2.1, §4.3.1). The human-readable profile label may accompany the ID but does not replace it.

A partial check may identify the parts or rules it evaluated, but it **shall not** claim full textual conformance. Cherry-picking rules does not establish conformance.

### 0.4.4 Version citation

A governed unit is checked against its declared specification version, not the latest version. Tooling and applicability data **shall** use the declared version's core, profile registry, profile overlays, Annexes A and B, rule metadata, and phrase lists. §0.8 guarantees that retained earlier versions remain checkable.

## 0.5 Normative references

The following documents are cited normatively. For dated references, only the cited edition applies.

- RFC 2119, *Key words for use in RFCs to Indicate Requirement Levels*; RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words*.
- Semantic Versioning 2.0.0 — for §0.8.
- Keep a Changelog 1.1.0 — for Annex G.
- Annex A (Glossary) and Annex B (Assumed-Reader Baseline and Profile Overlays) of this specification — normative annexes, versioned with ITWS.

The standards and guides listed in §0.1 are informative sources. Annex F identifies what each ITWS rule adopts, adapts, or originates.

## 0.6 Terms and definitions

The following meta-vocabulary is available throughout ITWS without further definition.

- **governed document** — a Markdown document in §0.2's scope that declares one ITWS profile.
- **governed surface** — the artifact form a profile governs: `markdown-document` or `hosted-comment-set` (§0.2.1).
- **governed unit** — a governed document or a governed comment change set.
- **comment change set** — the governed comments changed between one recorded base version and one recorded proposed version of a host source file, identified by one change-set ID and one declaration carrier.
- **declaration carrier** — the JSON record that holds a comment change set's declarations and comment records.
- **host adapter** — the language-specific component that extracts comment units and host anchors and applies the exclusion policy for one host language.
- **host anchor** — the host file, line span, and enclosing named construct a governed comment attaches to.
- **information delta** — the knowledge a comment adds beyond what its anchored code states to a reader with the declared host-language supplement.
- **cognitive debt** — the future reader effort created when recorded knowledge is missing, stale, or misplaced.
- **removal condition** — the observable fact whose occurrence ends a temporary comment's or marker's life.
- **work item** — a governed `epic`, `task`, or `subtask` document that directs and verifies one unit of planned work.
- **product requirements document** — a document that states a product problem, outcome, scope, measures, and constraints.
- **strategic outcome** — an outcome that requires several independently acceptable tactical outcomes.
- **tactical outcome** — an outcome accepted at one product or technical boundary.
- **technical boundary** — an interface, invariant, operational state, or artifact that engineering can verify.
- **technical invariant** — a stable property that every applicable child work item must preserve.
- **user journey** — one actor's path from a stated starting condition to an observable outcome.
- **happy path** — a user-journey path that reaches the intended outcome under expected conditions.
- **sad path** — a path that names a blocking condition, expected response, safe state, and recovery.
- **accepted behavior contract** — an approved requirement, invariant, journey, or documented behavior that defines expected behavior.
- **feature work** — work that adds or changes accepted behavior without correcting a documented deviation.
- **defect correction** — work that restores behavior required by an accepted behavior contract.
- **maintenance or enabler work** — work that preserves behavior or prepares a later independently acceptable outcome.
- **engineering-only task** — a `task` with no independently acceptable user outcome and acceptance at a named technical boundary.
- **definition of done (DoD)** — one work item's authoritative closure contract.
- **completion condition** — one observable and independently testable part of a DoD.
- **integrated acceptance** — verification of behavior that appears only when all completion conditions work together.
- **technical hint** — non-normative information about relevant components, tests, evidence, or likely implementation locations.
- **shared core** — rules and mechanisms common to all profiles unless explicit applicability metadata says otherwise.
- **profile** — one canonical genre contract from §0.2, including its purpose, skeleton, and profile-scoped rules.
- **profile overlay** — the selected profile's additions to the shared core, including the genre-knowledge overlay in Annex B.
- **applicable rule** — a rule whose profile metadata and construct conditions include the document or passage under review.
- **software engineering pod** — a cross-functional group that designs, delivers, tests, operates, manages, or supports software.
- **base reader** — the software engineering pod baseline defined in §0.3 and enumerated in Annex B.
- **assumed reader** — the base reader plus the genre-knowledge overlay for the document's declared profile.
- **genre knowledge** — knowledge of how to read and use a document genre, not knowledge of its subject domain.
- **domain term** — a technical word or phrase from a product, system, operational environment, profession, or field. The term is absent from the base-reader baseline.
- **rule** — a permanent-ID normative unit of Parts 2–8, written in the §1.3 template. A scoped rule keeps its section number and sits in the overlay file that §1.5 assigns.
- **profile family** — a group of profiles that share genre rules through one shared overlay module (§1.5).
- **load set** — the shared core, the shared annexes, one profile directory, and that directory's shared modules (§1.5.3).
- **admitted term** — a term defined in the current document under §2.3. When Annex A has an entry, the document uses its meaning and satisfies its prerequisites.
- **term ladder** — the §2.3 discipline of defining a term before first use with only assumed or previously admitted terms.
- **chunk** — a paragraph-level unit with exactly one purpose from the §4.1 taxonomy.
- **bounded block** — a visually delimited, labeled span whose detail the main text does not depend on (§4.6, §6.3, §7.3).
- **prior** — context deliberately introduced so later text may build on it (§4.9).
- **claim** — a proposition the document presents as true, at a strength governed by its evidence and §5.6.
- **caveat** — a statement limiting the scope, conditions, or strength of technical content (§7.2).
- **machine-checkable** — a rule property indicating that §8.2 tooling can detect a violation without human judgment.
- **navigation metadata** — the §1.6 fields that describe a rule so a reader or tool can find it. Only the construct condition carries normative force.
- **profile envelope** — every active rule whose applicability admits a declared profile. The envelope is the widest correct rule set for a document.
- **generated artifact** — a machine-produced file derived from this specification, pinned to one version and to source hashes (§8.6).

Part 1 defines the exact and plain layers. Section 1.6 defines the navigation metadata. Part 8 defines textual conformance and the bounded machine result.

## 0.7 How to use this specification

**Self-application boundary.** This specification is outside §0.2 profile conformance. Its authored prose follows shared-core rules where meaningful. Quoted counterexamples, metadata, templates, tables, source names, and generated artifacts are fixtures. The §1.6 navigation metadata lines, the §8.2.1 phrase-list paragraphs, and the skeleton and section-map blocks are metadata in that sense: they are machine-readable records, not governed prose.

**Writers and rewriting agents.** Select the profile before drafting. Load the §1.5.3 load set for that profile and ignore every other overlay. Put the two required declarations in the governed unit. Draft from the profile skeleton and resolve vocabulary against the base reader plus the selected overlay. Preserve exact facts, continue around unresolved spans, and report missing facts instead of inventing them.

**Machine checks.** Run the checker against the declared version and profile. Treat `pass` as a result for the disclosed machine coverage, not as certification of every semantic rule. Candidates and untested rules remain available for a reader or agent to evaluate without blocking an otherwise safe rewrite.

**Rule citation form:** "ITWS §3.2.1" cites a rule. "ITWS Part 3" cites a part. A bare "§3.2" cites a section. A scoped rule may also be described as "ITWS §x.y.z (`procedure`)." Rules, not sections or profile labels, are the unit of conformance.

**Precedence:** §1.4 resolves apparent collisions after §1.3 determines which rules apply. Writers and reviewers do not resolve collisions ad hoc.

## 0.8 Versioning and change policy

ITWS uses Semantic Versioning. Until 1.0, a minor version may contain breaking draft changes. The changelog **shall** identify them. The expansion from the research-only 0.1 draft to the shared-core/profile architecture is such a change. The expansion is released as 0.2.0-draft. After 1.0:

- **Major** — A change is major when it adds or tightens a mandatory rule. Upward reclassification and expanded profile applicability are also major. Adding, removing, or repurposing a canonical profile ID is major. Removing an assumed-reader baseline item is major. Any change that can make a previously conforming document non-conforming is major.
- **Minor** — A change is minor when it adds a recommended or permitted rule. Relaxation, downward reclassification, and narrower profile applicability are also minor. Adding a term to the assumed-reader baseline is minor. Adding a glossary entry or genre-knowledge item is minor unless it admits domain knowledge.
- **Patch** — wording, examples, and typographical corrections that do not change conformance, applicability, or reader assumptions.

**Permanent rule IDs.** A rule ID is assigned once and never reused, including across profiles. Changed wording or `Profiles` metadata does not give a rule a new ID. The version pin identifies the applicable form. New rules receive new IDs appended within their section.

**Retirement without reuse.** A withdrawn rule remains in its retained historical release, and its permanent ID remains reserved. The current source may omit retired rule text when retaining it would import a contract outside the current specification's scope. A retired-ID ledger records the version and replacement or `none`. A retired or deprecated ID is never reassigned.

**Checkability guarantee.** A document citing a **retained** version **shall** remain checkable against that version. A retained version keeps the core, profile registry, profile overlays, Annexes A and B, Annex C applicability data, Annex F traceability, phrase lists, and compatible tooling at one recoverable revision. Rule applicability is historical data, not a property inferred from the latest text.

Annex G marks every released version as retained or unavailable, and §0.8 makes no promise about an unavailable one. Before 1.0 a draft may be released without a retained revision; the guarantee then does not reach it, and a document citing it is re-pinned to a retained version before its conformance is recorded. From 1.0 onward every released version is retained.

**Naming history.** Version 0.1 used the name *Research Writing Specification (RWS)*. That name and its four-type conformance model remain valid for documents that cite 0.1. ITWS does not retroactively rename or reinterpret the release.

**Living lists.** The prohibited-language lists, Annex A glossary, and Annex B baseline and overlays may change more often than rule text. They version with ITWS, follow §2.5 governance where applicable, and obey the compatibility rules above.

Annex G records all changes in Keep a Changelog format and identifies affected rule IDs, profiles, reader assumptions, and source mappings.

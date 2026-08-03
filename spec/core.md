# ITWS core

**ITWS version:** 1.0.0 · **Status:** normative

Shared core. Applies to every profile unless a rule says otherwise. Read [legend.md](legend.md) first — it fixes the `ID | C | Rule` notation and the voice fence.

ITWS = controlled English for technical documents. Goal: give a working technical reader a **correct shallow model at low reading cost**, while main text stays complete for the document's declared job and exact detail stays reachable. Access and orientation, not full comprehension.

Conformance does not depend on who or what wrote the text.

---

## 0. Scope and conformance

### 0.1 Profile registry (closed)

Governed unit = shared core + **exactly one** profile ID. ID is canonical; label is cosmetic.

| ID | Job |
|---|---|
| `design-rfc` | propose/specify a design: requirements, interfaces, invariants, alternatives, acceptance |
| `decision-record` | record one decision + context + alternatives + consequences |
| `procedure` | let reader complete an operational task safely + repeatably |
| `explanation` | build accurate mental model of a system, mechanism, concept |
| `incident` | record impact, response, evidence, causes, follow-up |
| `technical-report` | present analysis / system / method / result in sustained detail |
| `research-paper` | report question, method, evidence, result, limitations to publication standard |
| `investigation-log` | preserve dated questions, actions, observations, hypotheses, next steps |
| `epic` | define one strategic outcome + measures + invariants + child-task boundaries |
| `task` | specify one independently acceptable tactical outcome |
| `subtask` | verify one named completion condition under exactly one parent `task` |
| `maintenance-comment` | govern comments one maintenance change adds, modifies, removes |
| `data-table` | inventory homogeneous items as rows against a fixed column schema, for lookup, comparison, delivery tracking |

One ID per unit. Never combine. Companion documents > hybrid. A collection may hold many units, each declaring its own profile.

### 0.2 Governed surfaces

- `markdown-document` — prose Markdown. First 11 profiles. "governed document" = this alone.
- `hosted-comment-set` — comment change set inside a host source file, declared by a JSON carrier. Only `maintenance-comment`. Host file itself = outside conformance; governed comments carry no ITWS boilerplate.
- `tabular-document` — workbook of named sheets: one Title sheet, one Glossary sheet, 1+ data grids of homogeneous rows. Only `data-table`. Cells hold governed prose. Rendering (fill, font, frozen panes, merged cells, column width) = outside conformance, as Markdown rendering is. File format (`.xlsx`, CSV set, hosted sheet) = carrier, ! conformance surface.

**governed unit** = any surface. A rule naming the *governed unit* reaches all three. A rule naming the *governed document* is bounded to Markdown. A rule naming a document element (heading, section, figure, equation) is inapplicable where that construct is absent.

### 0.3 Outside scope

Source code (except a declared `maintenance-comment` set) · standalone API/command reference · slide decks, posters, talk scripts · marketing and general-audience writing · chat, issue-tracker comments, status events, unstructured tickets, review comments.

**Computational workbook** — assumptions, formula graph, derived outputs — is outside scope. A `data-table` inventories rows; it does not govern a workbook that computes. A workbook mixing both is governed only over its `data-table` sheets, and the computational sheets carry no conformance claim.

Issue-tracker item is governed only when it declares `epic` | `task` | `subtask` **and** carries every required slot.

Out-of-scope work may reuse ITWS practice; no conformance claim attaches.

### 0.4 The assumed reader

assumed reader = **base reader** (all profiles) + **genre overlay** (declared profile).

Base reader = working member of a cross-functional software engineering pod: engineers, designers, EMs, QA, PMs, ops partners. They follow basic engineering discussion. They are **not** assumed to have a CS education, to write or review code, to match a seasoned engineer's depth, or to know this document's product, system, environment, field, or subject.

Full enumeration: [reader.md](reader.md). That file decides disputes. **Item absent from the list = not assumed.**

Profile overlays grant **genre knowledge only** — how to read the document type. Never product, system, operational, scientific, or domain vocabulary. Familiarity ≠ operational knowledge: a domain term specialists know still enters through the term ladder (§2.3).

### 0.5 Conformance

**Binary.** A governed unit conforms, or does not, for **one declared version + one declared profile**. It conforms when it satisfies every applicable mandatory (`M`) rule and every required profile slot. Reviews, approvals, reader tests, and accepted deviations do not change this result.

**Applicability.** A core rule applies to all thirteen profiles. A profile file's rules apply to that profile only. Construct triggers still gate: an equation rule is irrelevant to a document with no equation.

**Required declaration.** Every conforming unit declares three fields:

```text
ITWS version: 1.0.0
Profile: design-rfc
AI disclosure: assisted — drafted the rollout section and rewrote the summary; reviewed by the platform pod
```

Markdown document → front matter. Hosted comment set → declaration carrier. Tabular document → Title sheet.

A unit is checked against **its declared version**, not the newest one.

Declaration fields are metadata, not governed prose. §3 sentence rules do not apply to them.

**`AI disclosure` values (closed):**

| Value | Meaning |
|---|---|
| `none` | no generative AI tooling contributed content to this unit |
| `assisted` | generative AI tooling contributed part of the content |
| `generated` | generative AI tooling produced the substantial majority of the content |

Form: `<value>` alone for `none`; otherwise `<value> — <what the tooling did>; reviewed by <who>`. The note states scope and human review, because a bare value tells the reader nothing they can act on (P5, P6).

Where review has not happened, say so — `not yet reviewed` — rather than naming a reviewer. Never record a review that did not occur.

**The disclosure records provenance. It does not affect the conformance result.** Conformance is a property of the text (§0.5, opening). A `generated` unit satisfying every applicable mandatory rule conforms. An `assisted` unit that does not, does not. The field exists so a reader knows how the text came to exist, not so they can discount it.

A partial check may name what it evaluated. It **shall not** claim full conformance. Cherry-picking rules establishes nothing.

### 0.6 Meta-vocabulary

Available throughout ITWS without definition.

**chunk** — paragraph-level unit with exactly one §4.1 purpose. **bounded block** — visually delimited labeled span whose detail main text does not depend on. **prior** — context deliberately introduced so later text may build on it. **claim** — proposition presented as true at a strength governed by §5.6. **caveat** — statement limiting scope, conditions, or strength. **admitted term** — term defined in the current document under §2.3. **term ladder** — §2.3 discipline: define before first use, using only assumed or already-admitted terms. **load set** — legend + ontology + core + phrases + glossary + reader + one profile.

Work-item vocabulary (`epic`, `task`, `subtask`), hosted-comment vocabulary (`maintenance-comment`), and tabular vocabulary (`data-table`) live in those profile files.

---

## 1. Architecture

### 1.1 Principles

Each is enforced by concrete rules; cite the rule, not the principle.

- **P1 — optimize reader effort, not word count.** Add words that prevent rereading. Layer or remove words that do not. → §3.1, §4.6, §6.5
- **P2 — one word, one meaning.** Elegant variation prohibited. → §2.1, §2.3, §5.2, §6.5
- **P3 — exactness survives plain prose.** Simplification may drop nonessential explanation detail. It may never change a claim, definition, requirement, interface, invariant, procedure, observation, or measurement. → §1.2, §5.1, §5.6
- **P4 — reader effort is budgeted by depth.** Scan path = correct shallow model. Main text = the declared job, complete. Bounded blocks + appendices = optional resolution. → §2.3, §4.6, §4.8, §4.12
- **P5 — specific over generic.** Every sentence should say something that could not describe a different subject. Loss of specificity is the central failure. → §2.6, §3.10, §4.10, §5.4, §6.5, §7.4
- **P6 — assertions carry their basis.** Claim → evidence, conditions, units, comparison, uncertainty. Requirement → acceptance condition. Interface/invariant → bounds. Procedure → prerequisites, hazards, outcomes, verification. → §5.4, §5.6, §7.2, §7.3
- **P7 — enforceable or not a rule.** Point at the rule + the passage, be done. → §1.3, §8
- **P8 — common stays common, differences stay explicit.** Profile files hold genuine genre differences only; they never duplicate core or smuggle in domain knowledge.

### 1.2 Two-layer model (normative)

Every governed document carries two layers. They interleave in the rendering; their obligations differ.

- **exact layer** — claims, definitions, requirements, interfaces + invariants, procedures, observations + measurements. Includes the mathematics, data, conditions, bounds, warnings, uncertainty, and evidence precision needs. Governed by §4, §5, §7 + the profile.
- **plain layer** — the prose and explanatory structure carrying the exact layer to the assumed reader. Governed by §2, §3, §4, §6.

Plain **wraps** exact. Plain **never replaces** exact.

1. Each exact item has the precision its profile requires.
2. A plain rendering preserves the exact item's meaning, scope, strength, conditions, and normative force, and stays traceable (§5.1.2).
3. Simplification may omit detail from an **explanation** only. It may not weaken a requirement, alter an interface or invariant, drop a procedure prerequisite / hazard / step / verification, or detach an observation from its interpretive conditions.
4. A bounded block may carry high-resolution detail when the main line stays accurate without it. Required operational or safety information is **never** skippable.

Three acceptance questions:

- **exactness** — is the exact layer correct, complete for the job, consistent, precise enough to act on?
- **scan utility** — does the §4.12 scan path give the assumed reader the profile's shallow-model outcome, preserving status, strength, and material boundaries?
- **main-path utility** — can the assumed reader follow the declared purpose from the baseline alone, without inventing missing domain knowledge?

A document can be precise but unusable, scannable but false, or fluent but untrustworthy.

### 1.3 Precedence

Determine applicability first (§0.5). A rule outside the applicable set cannot conflict. When two applicable rules collide on one passage, this order is **fixed** — never resolve a collision ad hoc:

1. **Exactness and safety over style.** A length cap never justifies blurring a claim, weakening a requirement, changing an invariant, or dropping a warning or verification step. Split, restructure, or layer instead.
2. **Explicit profile exception over its named general rule.** A profile rule overrides a core rule only when its statement expressly names the displaced rule. To narrow a mandatory rule the exception must itself be mandatory. Cannot override (1).
3. **Structure over sentence.** §4 + the profile skeleton beat §3.
4. **Mandatory over recommended**, subject to (1)–(3).
5. **Normative text over notes.** Rationales, examples, and intuition blocks create no requirement.
6. **Specific over general**, subject to (1)–(5).

Known collisions, resolved:

- exact content vs §3.1 caps → (1): split or layer, never blur.
- procedure prerequisites/warnings vs claim-first ordering → (1)+(3): safe task order wins.
- §6.5 deliberate redundancy vs §2.1 no-variation → not a collision. Redundancy repeats **verbatim**; §2.1 prohibits *varied* wording.
- §4.2 claim-first vs §2.3 define-before-use → (3): summary states the point in base-reader words; the exact restatement waits for its terms; both linked under §5.1.2.
- profile exception vs core rule → (2) **only** when the exception names the rule. Listing a profile creates no implied exception.

---

## 2. Words and vocabulary

ITWS replaces the ASD-STE100 closed dictionary with an **open but gated** vocabulary. Baseline + profile overlay supply some words ([reader.md](reader.md)). Everything else is admitted through the ladder before first use.

### 2.1 General word rules

| ID | C | Rule |
|---|---|---|
| 2.1.1 | M | word/term carries exactly one meaning throughout a document |
| 2.1.2 | M | later reference to a named concept uses the established term; ! synonym swap for variety |
| 2.1.3 | R | use the plain-verb replacements in [phrases.md](phrases.md) §2.1.3 |
| 2.1.4 | M | acronym/initialism not in [reader.md](reader.md) → first use gives expansion + parenthesized short form |
| 2.1.5 | M | after introduction, use short form **or** expanded form consistently, ! both interchangeably |

### 2.2 Permitted general vocabulary

| ID | C | Rule |
|---|---|---|
| 2.2.1 | M | every specialized term or sense is assumed under [reader.md](reader.md) **or** admitted under §2.3 before first use |

### 2.3 Term ladder (ITWS-original core mechanism)

Document builds vocabulary as a program builds state: nothing referenced before initialization. Each admitted term becomes a rung for the next definition. §5.2 applies it to symbols; §4.9 applies it to context.

| ID | C | Rule |
|---|---|---|
| 2.3.1 | M | term outside §2.2.1 permitted vocabulary → defined before first body use (glossary terms included) |
| 2.3.2 | M | a definition uses only assumed vocabulary + terms already admitted in this document |
| 2.3.3 | M | ! use a term on a promise to define it later — see [phrases.md](phrases.md) §2.3.3 |
| 2.3.4 | M | definition states what the thing **is or does** — inputs, outputs, distinguishing properties; ! merely relate it to other terms |

Valid chain, worked — each rung stands on assumed vocabulary or an earlier rung:

> A *replica* is a copy of a service or its stored data. A *health check* is a repeated test that reports whether a replica can accept requests. *Failover* is sending requests to a healthy replica after another replica stops accepting them.

Broken chain — no rung reaches the ground:

> We use Raft for leader election after a quorum failure. Consensus, described in §5, preserves linearizability.

*Raft*, *leader election*, *quorum*, *linearizability* unadmitted; *consensus* forward-referenced.

### 2.4 Definition quality

| ID | C | Rule |
|---|---|---|
| 2.4.1 | M | definition substitutes for the term in every sentence of the document without changing meaning |
| 2.4.2 | M | ! circular — definition uses neither the term, its derivative, nor anything depending on it |
| 2.4.3 | R | genus + differentia: name the nearest familiar category, then what distinguishes it |
| 2.4.4 | M | definition ≤ 2 sentences **and** ≤ 40 words; further explanation goes in separate prose |
| 2.4.5 | M | ! definition by synonym alone, by other jargon, or by citation alone |

### 2.5 Glossary governance

Two levels: per-document definitions (§2.3–2.4) and canonical entries in [glossary.md](glossary.md).

| ID | C | Rule |
|---|---|---|
| 2.5.1 | M | governed unit ! contradict a glossary term's meaning, in definition or in use |
| 2.5.2 | R | at definitional first use, quote the glossary wording verbatim |
| 2.5.3 | R | second writer to define a term proposes it for the glossary |

Flow: **draft** (define in-document; nothing else required) → **propose** (recurring term, with drafted entry + ladder prerequisites) → **admit** (maintainer checks against §2.3–2.4, records prerequisites and version) → **revise/deprecate** (never delete; deprecate and retain).

### 2.6 Prohibited usage patterns

Most of these are P5 failures: generic prose displacing specific prose. Literal strings for every "listed" rule are in [phrases.md](phrases.md).

| ID | C | Rule |
|---|---|---|
| 2.6.1 | M | ! field jargon as a compression device when permitted vocabulary states the same thing |
| 2.6.2 | M | named technology, model, method, tool, standard, or system → plain-language introduction before bare use |
| 2.6.3 | M | listed superlative appears only if the same sentence states the measurement earning it |
| 2.6.4 | M | ! listed prohibited word, except in quotation or discussion of the word |
| 2.6.5 | M | ! listed agency verb for software/models/automated systems before its operational definition |
| 2.6.6 | M | ! listed warpath marker or equivalent (structural parent: §4.9) |
| 2.6.7 | M | ! listed editorializing aside |
| 2.6.8 | M | claims name and cite their sources; ! listed vague-authority phrase; plural attribution ! imply more sources than the citations provide |
| 2.6.9 | M | ! replace absent evidence with speculation — report the absence; ! listed gap-speculation phrase |
| 2.6.10 | M | ! stack listed connectives as padding; each connective marks a §3.8 relation |
| 2.6.11 | M | ! listed chat phrase, unfilled placeholder, or tool-leakage artifact |

### 2.7 Naming

Covers organization-coined names for artifacts, components, services, experiments, datasets, methods.

| ID | C | Rule |
|---|---|---|
| 2.7.1 | M | coined name gets the §2.3 plain-language introduction before bare use |
| 2.7.2 | R | descriptive name > allusive name |
| 2.7.3 | M | exactly one name per artifact throughout; ! nicknames, shortenings, or renaming mid-document |
| 2.7.4 | M | reference to an external artifact carries a version pin |

---

## 3. Sentences

§5 exactness beats any §3 rule (§1.3 item 1). Split or layer. Never blur.

### 3.1 Length

**load-bearing sentence** = admits a term, or states a claim, requirement, decision, instruction, warning, or operational outcome. **descriptive sentence** = any other.

| ID | C | Rule |
|---|---|---|
| 3.1.1 | M | descriptive sentence ≤ 25 words |
| 3.1.2 | M | load-bearing sentence ≤ 20 words |
| 3.1.3 | M | counting: one math symbol = 1 word; an inline expression containing any operator = 3 words |
| 3.1.4 | M | over cap → split, or move non-action-critical detail to display math or a bounded block; ! drop precision to fit |

### 3.2 One idea

| ID | C | Rule |
|---|---|---|
| 3.2.1 | M | one idea per sentence |
| 3.2.2 | M | ≤ 1 independently reviewable claim, requirement, decision, instruction, risk, or outcome per sentence |

### 3.3 Voice

| ID | C | Rule |
|---|---|---|
| 3.3.1 | M | active voice, unless a listed exception applies |
| 3.3.2 | M | "we" = the document's authors or named reporting team only; ! include the reader |

Passive permitted only when: (a) actor unknown or genuinely irrelevant; (b) the object is the chunk's established topic and fronting it preserves continuity; (c) the previous sentence named the actor and the passive stays unambiguous.

### 3.4 Tense and mood

| ID | C | Rule |
|---|---|---|
| 3.4.1 | M | tense follows the table below |
| 3.4.2 | M | listed conditional forms appear only in allowed contexts; ! report an observation, requirement, decision, or committed plan |

| Context | Tense |
|---|---|
| properties of a system, method, policy, artifact | present |
| general truths, definitions | present |
| completed actions, observations | past |
| governing decisions, current requirements | present or direct requirement form |
| procedure steps | imperative |
| proposed or committed future behavior | explicit future or requirement form |
| the document referring to itself | present |
| untested predictions | future/conditional, **inside a §7.3 speculation block** |

### 3.5 Noun clusters

| ID | C | Rule |
|---|---|---|
| 3.5.1 | M | ≤ 3 nouns per cluster; longer stacks use prepositions or clauses |
| 3.5.2 | P | an admitted multiword term may count as one noun under 3.5.1 |

### 3.6 Reference

| ID | C | Rule |
|---|---|---|
| 3.6.1 | M | every pronoun has exactly one grammatically plausible antecedent, in the same sentence or the one before |
| 3.6.2 | M | ! open a sentence with bare "this / that / these / those / it" — name the referent with a following noun |

### 3.7 Ambiguity controls

| ID | C | Rule |
|---|---|---|
| 3.7.1 | M | "only" immediately precedes what it modifies |
| 3.7.2 | M | "respectively" pairs ≤ 2 items; 3+ → direct or tabular |
| 3.7.3 | M | ≤ 1 negation per clause, counting negative affixes ("un-", "non-") that interact with "not" |
| 3.7.4 | M | two quantifiers in one sentence → scope order unambiguous; use per-item statements when needed |

### 3.8 Punctuation and connectives

| ID | C | Rule |
|---|---|---|
| 3.8.1 | M | ! semicolon joining independent clauses — use two sentences |
| 3.8.2 | M | serial comma before the final conjunction in a list of 3+ |
| 3.8.3 | M | each connective expresses only its reserved relation; "since" and "while" = **time only** |

| Relation | Permitted connectives |
|---|---|
| contrast | but, however, whereas |
| cause / consequence | because, so, therefore |
| sequence | first / second / then, after, before (ordinals, ! "firstly") |
| addition | and, also — plus moreover / furthermore / additionally, subject to §2.6.10 |
| concession | although, even though (one per sentence) |
| example | for example (! "e.g." in running prose) |

### 3.9 Hedging

Certainty language has exactly one source: §5.6.

| ID | C | Rule |
|---|---|---|
| 3.9.1 | M | ! listed vague hedge modifying a claim, risk, prediction, or reported outcome |
| 3.9.2 | M | every expression of confidence or claim strength uses a §5.6 phrase; no other certainty phrasing permitted |

### 3.10 Formulaic constructions

Prohibited on their merits: each adds filler, inflates significance, or blurs a claim, regardless of author. Vocabulary-level signs → §2.5. Formatting-level → §4.10. Hollow summaries → §6.5.

| ID | C | Rule |
|---|---|---|
| 3.10.1 | M | ! pad a list or series to three for rhythm; each item carries distinct information |
| 3.10.2 | M | ! listed contrast-reframe template ("not just X but Y") — state the positive content directly |
| 3.10.3 | M | em dash marks only a genuine interruption or reversal; ! replace an equivalent comma, colon, or parenthesis |
| 3.10.4 | M | ! listed trailing present-participle clause asserting significance |
| 3.10.5 | M | "ranges from X to Y" describes only endpoints of a measured or defined range; ! spread rhetorical examples |
| 3.10.6 | M | ! listed inflated copula substitute where a plain verb states the fact; ! open a definition with "refers to" |

---

## 4. Chunks, structure, and the scan path

### 4.1 Chunk model — one purpose per chunk

| ID | C | Rule |
|---|---|---|
| 4.1.1 | M | each chunk serves exactly one purpose from the taxonomy below |

A reviewer who cannot classify a paragraph has found mixed or missing purpose. Profiles need not use every type.

| Type | Job | Review test |
|---|---|---|
| context / prior | supply a fact, constraint, event, or prior later content needs; introduces no requirement, choice, or conclusion | what must the reader know before the next point makes sense? |
| definition | admit a term to the ladder with an operational meaning | can the reader now use the term correctly in an unseen sentence? |
| requirement | state a condition the work must satisfy, with explicit testable force | could a reviewer turn this into an acceptance check without inventing a threshold or actor? |
| claim | state a conclusion or finding at a §5.6 strength | if deleted, would the document assert less? |
| decision | record one selected course of action, its status, its governing scope | can the reader state what was chosen without reconstructing it from the alternatives? |
| mechanism / explanation | explain how or why something works, asserting no new result | does it answer "how does this happen?" and stay true if measured results change? |
| procedure / instruction | ordered actions to perform or audit, not their interpretation | could the assumed reader follow or repeat them in this order? |
| evidence / observation | report measurements, events, counts, comparisons, uninterpreted | could two people who disagree about the conclusion still accept every sentence? |
| interpretation | state what evidence means, at a §5.6 strength, labeled where §7.3 requires | could a reasonable person accept the evidence but dispute this paragraph? |
| risk | uncertain condition + its consequence, calibrated per §5.6 and §7.3 | what could go wrong, under what condition, with what consequence? |
| limitation / boundary | bound a claim, decision, procedure, or explanation (§7.1) | does it reduce the reach of content stated elsewhere? |

Deciding which type a passage carries is a **reader's judgment**. It is never derived mechanically.

### 4.2 Main point first, at four levels

| ID | C | Rule |
|---|---|---|
| 4.2.1 | R | sentence states its main point in the main clause, before subordinate qualification |
| 4.2.2 | M | chunk states its point in its first sentence; remaining sentences support, elaborate, or bound it |
| 4.2.3 | M | section states its takeaway or operational purpose in its opening chunk, before supporting material |
| 4.2.4 | M | *(all profiles except `investigation-log`, `subtask`, `maintenance-comment`, `data-table`)* document states its profile-specific main point in the earliest applicable slot, before supporting detail |

Main point may be a requirement, proposal, decision, instruction goal, explanatory takeaway, incident outcome, or evidential claim. The reader should never hold unexplained machinery while waiting to learn why it matters.

### 4.3 One job per document

| ID | C | Rule |
|---|---|---|
| 4.3.1 | M | governed unit declares exactly one canonical §0.1 profile ID on its declaration surface (front matter, or the carrier) |
| 4.3.2 | M | ! independently perform another profile's primary job; required subordinate content stays inside the declared profile |
| 4.3.3 | M | every required slot for the profile is present, in the profile's stated order |
| 4.3.4 | M | a governed unit declares one `AI disclosure` value from the §0.5 closed set, on the same surface as its other declarations; any value other than `none` carries the scope-and-review note |

### 4.4 Applying the skeleton

| ID | C | Rule |
|---|---|---|
| 4.4.1 | M | apply the declared profile's skeleton, on its declared surface |
| 4.4.2 | M | introduce each prerequisite before the first load-bearing detail depending on it |
| 4.4.3 | M | *(`design-rfc`, `decision-record`, `procedure`, `incident`, `technical-report`, `research-paper`, `epic`, `task`)* state the main outcome early in assumed-reader vocabulary, restate it precisely after admitting all dependencies, and link both under §5.1.2 |

**Empty slots.** A required job with no content stays present as `None` or `Not applicable` **with a reason**. Never omit the slot. Optional bounded blocks and appendices may be omitted.

**Renames and merges.** Exact skeleton headings need nothing. A profile file lists its permitted renames and merges; any other rename needs a front-matter section map. A merged section keeps separately labeled subsections for each canonical job, in canonical order. A rename or merge changes presentation only — no required job disappears. Sections without express merge permission stay separate. Observation/evidence may share a section with analysis/interpretation only where the profile expressly permits it, and then only with the two jobs separately labeled.

**Section map** (optional; only for a rename the profile file does not list). Fenced block in the front matter, tagged `itws-section-map`, one heading → one canonical slot per line:

```text
"Why we are doing this" -> Context
"What must hold" -> Requirements
```

Invalid if a heading repeats, a slot repeats, a named slot is absent from the profile, a named slot belongs to another profile, or a mapped heading is absent from the document. **front-matter region** = first line through the last line before the first `##` heading.

### 4.5 Headings

| ID | C | Rule |
|---|---|---|
| 4.5.1 | M | below required top-level slot names, a heading states its section's point or operational purpose; ! merely name the topic |

Required slot names are navigational landmarks and are exempt. Lower-level headings are not. "Two replicas preserve write availability" > "Design details".

### 4.6 Progressive disclosure

Three layers: plain main text → bounded blocks → appendix formalism. Each deeper layer adds resolution and does not restate a shallower one without a recall or verification purpose (§6.5).

| ID | C | Rule |
|---|---|---|
| 4.6.1 | M | exact detail unnecessary to the assumed reader's main line goes in a bounded block or appendix, ! in main text |
| 4.6.2 | M | bounded block = blockquote whose first line carries exactly one bold bracketed label: **[Detail — &lt;topic&gt;]**, **[Intuition — &lt;topic&gt;]**, or **[Speculation — &lt;topic&gt;]**; block ends where the quotation ends |
| 4.6.3 | M | **skip test**: main text stays coherent with every bounded block removed — no dangling reference, no broken argument |

### 4.7 Transitions and navigation

| ID | C | Rule |
|---|---|---|
| 4.7.1 | M | a section's first chunk states its function and its connection to preceding content |
| 4.7.2 | R | ≤ 2 forward pointers per section; each names a numbered section and does not depend on unread content |
| 4.7.3 | M | cross-references cite a numbered section, figure, or table; ! "above", "below", "as previously discussed" |

### 4.8 Density budgets

Ladder makes rigor possible; budgets make it manageable.

| ID | C | Rule |
|---|---|---|
| 4.8.1 | M | ≤ 3 new terms or symbols admitted per page (page = consecutive non-overlapping 500-word window; remainder = final page) |
| 4.8.2 | R | section ≤ 1,500 words |
| 4.8.3 | R | subsection ≤ 600 words |

### 4.9 Path-agnostic prose (no warpath)

Prose states current facts without relying on the decision path that produced them. "...instead of the old approach", "previously we tried X and it failed, so..." force the reader to infer a history they do not share. Extends Google's timeless-documentation rule from time-relativity to **path**-relativity. Lintable marker strings live at §2.6.6.

| ID | C | Rule |
|---|---|---|
| 4.9.1 | M | ! residual-history aside referring to superseded approaches, prior drafts, or abandoned states, outside a §4.9.2 framed prior or an identified chronological event |
| 4.9.2 | M | necessary path information appears as a **prior** in the concept's framing chunk, in path-agnostic terms |
| 4.9.3 | M | every clause about a superseded state or abandoned approach passes **delete-or-promote**: it deletes cleanly, or it takes §4.9.2 promotion |

Investigation logs and incident timelines legitimately record history — as identified dated events, not path-relative phrasing.

### 4.10 Formatting

| ID | C | Rule |
|---|---|---|
| 4.10.1 | M | headings use sentence case |
| 4.10.2 | M | body boldface only for term admissions (§2.3) and template-required labels; ! emphasize selected running words |
| 4.10.3 | M | prose content uses prose; ! a vertical "**Term**: description" list substituting for prose |
| 4.10.4 | R | ! table where a sentence states 2–4 facts equally well; tables hold genuinely tabular data (§5.5) |
| 4.10.5 | M | ! emoji |
| 4.10.6 | M | ! a section that could apply unchanged to another subject; ! listed boilerplate outline |

### 4.11 Work items

§4.11 rules apply to `epic`, `task`, and `subtask` only. They live in those profile files.

### 4.12 Scan path

Scan path = the governed unit's cheapest correct reading. Access and orientation, not comprehension.

| ID | C | Rule |
|---|---|---|
| 4.12.1 | M | Markdown scan path = document title, then in document order each main-text heading + the first sentence of that section's opening chunk; excludes bounded blocks and appendix content. *(`maintenance-comment` and `data-table` each replace this path — see their profile files.)* |
| 4.12.2 | M | scan path lets the assumed reader produce the declared profile's shallow-model outcome, preserving each applicable status, strength, and material boundary; the title ! frame a wider or stronger outcome |
| 4.12.3 | M | a material assertion on the scan path carries every truth-preserving qualification **in its own sentence**, using affirmative content words wherever a bare negation or trailing hedge could leave a stronger reading |
| 4.12.4 | M | each scan-path element states its subject without depending on adjacent prose or reading order; a dependency uses a local noun or an explicit numbered reference |

**main-text section** = headed section outside a bounded block or appendix. **opening chunk** = first chunk under a heading, before any child heading. **material boundary** = a §7.1 boundary whose omission would widen or strengthen the scan path's main point. **truth-preserving qualification** = an applicable status, strength, condition, or material boundary needed to keep a scan assertion true.

Heading identifies the topic. Opening sentence states the point about it.

### 4.13 Maintenance comments

§4.13 rules apply to `maintenance-comment` only. They live in that profile file.

### 4.14 Tabular documents

§4.14 rules apply to `data-table` only. They live in that profile file.

---

## 5. Exactness and evidence

By §1.3 these override §2, §3, §4, §6 wherever they collide.

### 5.1 Exactness principle

| ID | C | Rule |
|---|---|---|
| 5.1.1 | M | a plain rendering ! change the scope, status, strength, conditions, or required behavior of the exact statement it renders |
| 5.1.2 | M | every simplified rendering of a claim, decision, requirement, condition, or outcome explicitly references the exact statement it renders |

### 5.2 Notation

Notation is vocabulary — the §2.3 ladder applies to symbols unchanged.

| ID | C | Rule |
|---|---|---|
| 5.2.1 | M | symbol outside the baseline set is defined in prose at or before first use, using only baseline notation, admitted symbols, and admitted terms |
| 5.2.2 | M | one symbol = one meaning within a document; one meaning = one symbol |
| 5.2.3 | M | > 6 non-baseline symbols defined → notation table listing every defined symbol, its meaning, and its admission section |

Baseline (free): arithmetic `+ − × /` and parentheses · `=` `≠` `<` `≤` `>` `≥` · percent and plain ratios (`3:1`) · plain numeric ranges (`1–5`). **Everything else requires admission**, including any letter naming a quantity. Full list: [reader.md](reader.md).

### 5.3 Equations in prose

An equation the reader cannot read aloud is an image, not a statement.

| ID | C | Rule |
|---|---|---|
| 5.3.1 | M | every displayed equation carries an adjacent plain-language reading stating what it computes and why it appears there |
| 5.3.2 | M | inline math stays atomic — single symbols, function applications, single binary relations; anything containing a summation, product, fraction, or nested subexpression is displayed |

### 5.4 Reporting claims, decisions, and outcomes

A statement is **material** when changing or omitting it could change an implementation, action, approval decision, risk judgment, conclusion, or evaluation of the profile job. Supporting color and non-load-bearing examples are not material.

| ID | C | Rule |
|---|---|---|
| 5.4.1 | M | every material exact item carries the complete evidence record — from the item, its immediate context, or an explicit link |
| 5.4.2 | M | ! naked percentage or improvement figure — state base values and an absolute-or-relative marker |
| 5.4.3 | M | every citation resolves: DOI resolves to the referenced publication, URL is live or archived, book citation carries page numbers |
| 5.4.4 | M | the cited page or section states or directly supports the claim it is cited for |
| 5.4.5 | M | plural attribution ("several studies") is backed by at least that many distinct cited sources |

**Complete evidence record** = these six shared fields + every profile-specific field the profile file lists:

1. **exact item** — the claim, decision, requirement, interface, invariant, procedure control, observation, measurement, or outcome.
2. **context** — environment, version, dependency state, data, population, operating condition, time window: where the statement holds.
3. **baseline or alternatives** — previous state, expected state, comparison point, rejected options, or an explicit statement that no meaningful baseline exists.
4. **evidence** — measurements, tests, logs, traces, sources, proofs, or decision rationale.
5. **evidential strength and uncertainty** — the applicable §5.6 strength, plus quantified or bounded uncertainty when evidence is sampled, variable, incomplete, or inferential; otherwise state that none applies.
6. **lifecycle or authority status** — the applicable approval, verification, adoption, release, or investigation state, so an unsettled item does not read as settled; otherwise state that none applies.

Fields take the form the item needs. A field need not appear in every sentence — an item may link to one section- or document-level record supplying it.

Citation-integrity rules apply in **every** profile: fabricated-but-plausible references are a realistic failure mode in any machine-drafted text.

### 5.5 Figures and tables

| ID | C | Rule |
|---|---|---|
| 5.5.1 | M | every quantitative figure labels quantity + unit for each axis, every plotted series, and any nonlinear scale |
| 5.5.2 | M | caption states the claim, decision, or outcome the artifact supports; ! only what it depicts |
| 5.5.3 | M | every term and symbol in a figure, its caption, or its legend is assumed or previously admitted, with admission **preceding** the figure |

### 5.6 Evidential strength and authority (closed vocabulary)

Single source of phrasing for evidential strength and decision authority. §3.9 and §7.3–§7.4 defer to it. Grammatical inflection that preserves the phrase is fine. **These strings are exact — do not paraphrase them.**

| ID | C | Rule |
|---|---|---|
| 5.6.1 | M | signal strength or authority using **only** a phrase from the table below; ! unsupported modifier |
| 5.6.2 | M | each calibrated statement's strength matches the document's evidence and approval status |

| Tier | Phrases | Standard |
|---|---|---|
| verified | **the record shows** · **verification confirms** · **we show** | cited evidence, a stated verification, or a proof directly establishes the statement over its full stated scope |
| observed | **we observed** · **we find** | the document directly records the observation in a stated context, claiming no general fact beyond it |
| interpretive | **the evidence indicates** · **this suggests** | consistent with the evidence, but material alternatives remain or no direct test separates them |
| adopted | **we decided** · **this document requires** | records an adopted choice or normative constraint; authority from decision or approval status, not from empirical fact |
| proposed | **we propose** | choice, design, or requirement pending approval or implementation |
| speculative | **we hypothesize** · **we speculate** | goes beyond the available evidence; permitted **only** inside a marked §7.3 speculation block |

**Unsupported modifiers** (prohibited): any unsupported certainty or significance modifier, including "clearly", "obviously", "importantly", "dramatic", "we believe".

An **unmarked declarative material claim carries verified-tier force** — and must meet the verified-tier standard under 5.6.2.

**Lifecycle values** (`proposed`, `accepted`, `superseded`, `mitigated`, `resolved`, `open`, `closed`) describe artifact or workflow state. They are **not** strength.

### 5.7–5.9 Profile-scoped exactness

§5.7 (statistical admission) and §5.8 (checkability statements) apply to `technical-report` and `research-paper` only. §5.9 (definition-of-done composition) applies to `epic`, `task`, and `subtask` only. Each lives in its profile file.

---

## 6. Explanatory devices

These carry the plain layer. They never carry the exact layer: an analogy, intuition block, or explanatory diagram alone cannot establish a requirement, invariant, procedure condition, decision, finding, or research claim.

### 6.1 Analogies

| ID | C | Rule |
|---|---|---|
| 6.1.1 | M | every analogy maps its concept onto an anchor from the assumed-reader baseline or a previously admitted term |
| 6.1.2 | M | every analogy states its **breaking point** — the first anchor property that does not transfer |
| 6.1.3 | M | ≤ 1 analogy per concept per document, and exactly one anchor per analogy |

### 6.2 Worked examples

| ID | C | Rule |
|---|---|---|
| 6.2.1 | M | every **central mechanism** (one the document's primary outcome depends on) gets one worked example tracing concrete inputs through the mechanism to concrete outputs, states, or decisions |
| 6.2.2 | M | worked example ! carry detail the point being shown does not need |
| 6.2.3 | R | example values drawn from the reported task, data, or system, even when simplified in scale |

### 6.3 Intuition blocks

The sanctioned place for "roughly speaking". Notes inform; no requirement lives in a note.

| ID | C | Rule |
|---|---|---|
| 6.3.1 | M | informal explanation appears only as a **[Intuition — &lt;topic&gt;]** bounded block (§4.6.2) |
| 6.3.2 | M | an intuition block ! be the only location of a requirement, decision, precondition, verification, rollback condition, finding, measurement, comparison, or other exact statement |
| 6.3.3 | M | main text stays coherent and complete with every intuition block removed |

### 6.4 Diagrams

§5.5 governs figures presenting evidence; §6.4 governs diagrams explaining structure, sequence, state, or causality. Both apply when a diagram does both.

| ID | C | Rule |
|---|---|---|
| 6.4.1 | R | 3+ interacting components the primary outcome depends on → show as a diagram, ! prose alone |
| 6.4.2 | M | every diagram is referenced from main text by number, at the point the reader needs it |
| 6.4.3 | M | diagram labels, node names, edge annotations, and legend entries use only assumed or previously admitted terms, admitted **before** the diagram's first reference |
| 6.4.4 | R | every diagram carries alt text stating what it shows, in the same admitted terms as its labels |

### 6.5 Repetition

Elegant variation is prohibited (P2). Repetition that restores distant information is permitted. Moving from scan path to main text does not by itself justify repetition.

| ID | C | Rule |
|---|---|---|
| 6.5.1 | M | repeated definitions, claims, and admitted terms use wording **identical** to the original in every load-bearing element |
| 6.5.2 | R | an admitted term reused after more than 2,500 intervening words gets a verbatim definition recall or a section reference |
| 6.5.3 | P | a major section may open with a "Recall:" boundary recap giving each depended-on admitted term and its verbatim definition |
| 6.5.4 | M | ! end a section with a paragraph restating content without adding information — end on the last substantive point |

---

## 7. Limitations, caveats, interpretation

### 7.1 Required boundary content

Boundary dimensions (shared inventory):

- **environment** — deployment, region, topology, hardware, OS, runtime, physical conditions.
- **version and dependencies** — software, schema, protocol, model, configuration, external service, compatibility ranges.
- **capacity and duration** — load, scale, rate, storage, resource, concurrency, time window, exhaustion limits.
- **failure and recovery** — known failure modes, partial-failure behavior, detection gaps, rollback boundaries, irreversible effects.
- **security and privacy** — trust assumptions, privileges, threat boundaries, secret handling, data classification, exposure, consent, retention.
- **data** — provenance, collection conditions, coverage, quality, missing cases, transformations, known errors.
- **untested or unverified conditions** — plausible conditions the primary outcome invites the reader to assume are covered but are not.

Not every dimension applies to every document. Each profile file names which slots carry which dimensions.

| ID | C | Rule |
|---|---|---|
| 7.1.1 | M | every governed unit carries clearly identified boundary material in every boundary location its profile lists |
| 7.1.2 | M | boundary material states each applicable dimension within which the primary outcome is valid |
| 7.1.3 | M | boundary material describes known failure modes + their operational, security, privacy, data-integrity, or safety effects |
| 7.1.4 | M | boundary material identifies the untested or unverified conditions a reader would most plausibly assume are covered |
| 7.1.5 | M | central reliance on collected, generated, sampled, or logged data → state provenance, collection conditions, coverage gaps, transformations, retention limits, and known quality errors |
| 7.1.6 | M | each plausibly relevant dimension that is unknown, untested, unverified, or not applicable is **named as such**, not silently omitted |

### 7.2 Caveat placement

Warning goes at the hazard, not only in a general chapter. Here the hazard is a reader acting on an exact statement without its boundary.

| ID | C | Rule |
|---|---|---|
| 7.2.1 | M | every caveat shares a chunk with the material claim, decision, requirement, procedure step, or outcome it qualifies, at **every** load-bearing statement of that content |
| 7.2.2 | M | boundary material **aggregates** the document's caveats; it ! be the only place a caveat appears |

### 7.3 Interpretation discipline

*(Mandatory for `incident`, `technical-report`, `research-paper`, `investigation-log`, `task`, `subtask`. Other profiles may use the split.)*

| ID | C | Rule |
|---|---|---|
| 7.3.1 | M | a chunk recording an observation or measurement ! include an interpretive addition (cause, meaning, recommendation, broader conclusion) |
| 7.3.2 | M | every statement exceeding interpretive-tier support appears only inside a **[Speculation — &lt;topic&gt;]** bounded block that stays removable under §4.6.3 |
| 7.3.3 | M | a speculation block uses only speculative-tier phrases ("we hypothesize", "we speculate"); ! a verified, observed, interpretive, adopted, or proposed phrase |

Worked split — one fused paragraph at three strengths:

> Connection use reached 100% at 09:14 UTC, demonstrating that the client upgrade leaked connections, and a credential refresh probably triggered the first leak.

becomes:

> We observed connection use reach the configured maximum of 800 at 09:14:22 UTC on all three affected hosts. Trace links and clock bounds are in Timeline events I-17 through I-20.
>
> The evidence indicates that connection exhaustion caused request failures: failures begin after the pool reaches 800 and stop after capacity is restored. The evidence does not establish what began the connection growth.
>
> > **[Speculation — first connection failure]** We speculate that a credential refresh began the growth, but authentication logs for that interval had expired.

### 7.4 Beyond established boundaries

A statement beyond an established boundary is a different, weaker statement.

| ID | C | Rule |
|---|---|---|
| 7.4.1 | M | every statement extending a claim, decision rationale, verified procedure, incident conclusion, or result beyond its established boundary names its extrapolation target — environment, version, dependency, capacity, population, data source, or time period |
| 7.4.2 | M | a statement about a setting the document's evidence does not establish uses the interpretive tier, the proposed tier, or a marked speculation block; ! a verified or observed phrase |

---

## 8. Checking conformance

ITWS 1.0.0 has **no linter and no validator**. A reader or agent checks the text against the rules above.

**Self-check obligations.** After writing or rewriting a governed unit:

1. **Cite the rule.** Every finding and every material semantic judgment names a rule ID: "ITWS §4.12.3". A finding without an ID is not a finding.
2. **Report, never invent.** A missing fact is reported as missing. Never generate a value, citation, timestamp, owner, or measurement to fill a slot. This obligation outranks completing the draft.
3. **Continue around blocks.** An unresolved span does not stop work on independent spans. Return the best safe draft plus an explicit missing-fact list.
4. **Check the scan path last.** Read title + headings + opening sentences alone (§4.12). Confirm the profile's shallow-model outcome survives, with its status, strength, and material boundaries intact.
5. **State coverage honestly.** Say which rules you checked and which you did not. There is no `pass` result to report — a clean self-check is a disclosed-coverage statement, not a certification.

**Precedence when repairing.** §1.3 governs. Exact content is never edited to satisfy a style rule; repair the surrounding text and report the local limitation instead.

**Self-application.** This specification is outside §0.1 profile conformance. Its own prose follows core rules where meaningful; quoted counterexamples, tables, templates, and skeleton blocks are fixtures.

---

## 9. Versioning

Semantic Versioning.

- **major** — adds or tightens a mandatory rule; upward reclassification; wider profile applicability; adding, removing, or repurposing a profile ID; removing a reader-baseline item. Any change that can make a conforming document non-conforming.
- **minor** — adds a recommended or permitted rule; relaxation; downward reclassification; narrower applicability; adding a baseline item, glossary entry, or genre-knowledge item.
- **patch** — wording, examples, typography; no change to conformance, applicability, or reader assumptions.

**Permanent rule IDs.** Assigned once, never reused — including across profiles. Changed wording or applicability does not give a rule a new ID. A withdrawn ID stays reserved and is never reassigned.

A governed unit is checked against its **declared** version.

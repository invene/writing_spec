# Part 1 — Foundations and principles

Part 1 defines the architecture behind Parts 2–8. Part 1 covers one shared core, twelve profiles, two prose layers, tiered evidence, fixed rule anatomy, deterministic precedence, the file layout that separates each overlay from the core, and the navigation metadata that indexes every rule. The architecture serves every profile in §0.2. Research is one overlay, not the default document model.

## 1.1 Purpose and design principles

Concrete rules elsewhere in the specification enforce each principle below. Each principle lists its trace, and Annex F records it.

**P1 — Optimize reader effort, not word count.** Use the most economical form that preserves comprehension, exactness, safety, and profile completeness. Add words when they prevent inference or rereading. Remove or layer words that do not serve those needs.
*Enforced by:* §3.1 (length caps exist to serve clarity, not concision), §6.5 (deliberate redundancy is permitted), §4.6 (detail is layered, not deleted).

**P2 — One word, one meaning.** A term means one thing everywhere in a document, and one thing across all governed documents once it enters the glossary. Synonym variation for style is prohibited.
*Enforced by:* §2.1, §2.3, §5.2 (one symbol, one meaning), §6.5.

**P3 — Exactness preserved under plain prose.** Plain language carries technical content. Plain language never replaces or weakens that content. A simplification may omit nonessential detail from an explanation. A simplification may not change a claim, definition, requirement, interface, invariant, procedure, observation, or measurement.
*Enforced by:* §1.2 (the two-layer model), §5.1 (traceability of simplified statements), §5.6 (calibrated claim strength), and profile-specific exact-content rules.

**P4 — Reader effort is budgeted by reading depth.** The scan path gives a correct shallow model. Main text completes the declared profile job. Bounded blocks and appendices add optional resolution. The base reader plus the selected genre-knowledge overlay (§0.3) gets a defined budget of new concepts. The document spends this budget explicitly. Profile completeness requires every fact needed for the profile's purpose. It does not require every relevant fact about the subject.
*Enforced by:* §2.3, §4.6, §4.8, §4.12.

**P5 — Specific over generic.** Every sentence should convey information that could not describe a different subject. The central failure is loss of specificity. Specific, verifiable facts become generic significance claims that fit any subject. Machine-generated prose often shows this failure. Most prohibitions in §§2.6, 3.10, 4.10, and 6.5 address this failure.
*Enforced by:* §2.6 (hype vocabulary and vague attribution), §3.10 (formulaic constructions), and §4.10 (canned section formulas).
*Also enforced by:* §5.4 (no naked percentages), §6.5 (hollow summaries), and §7.4 (bounded generalization).

**P6 — Technical assertions carry their basis.** A claim or observation carries its evidence, conditions, units, comparison, and uncertainty. A requirement carries its acceptance condition. An interface or invariant carries its bounds. A procedure carries its prerequisites, hazards, expected outcomes, and verification. The relevant basis appears where the assertion is made or is linked unambiguously.
*Enforced by:* §5.4, §5.6, §7.2, §7.3, Part 4 profile structures, and profile-specific rules.

**P7 — Rules are enforceable or they are not rules.** Every rule is written so a reviewer can point at the rule and a violating passage and be done. Preferences that cannot be applied that way do not become rules.
*Enforced by:* §1.3 (rule anatomy), §8.1–8.2 (checklist and lint), Annex C (every rule indexed with its machine-checkability).

**P8 — Common rules stay common, and differences stay explicit.** A rule applies to every profile unless a `Profiles` line says otherwise. A profile overlay contains only genuine genre differences. The overlay does not duplicate the shared core or smuggle in domain knowledge.
*Enforced by:* §0.2 (profile registry), §0.3 (reader overlays), §0.4.3 (applicability), §1.3 (metadata), §1.5 (layout and placement), and Annex C.

## 1.2 The two-layer model (normative)

A governed document has two logical layers. They may be interleaved in the rendered document, but each has a distinct obligation:

- The **exact layer** consists of **claims, definitions, requirements, interfaces and invariants, procedures, observations and measurements**. The layer includes any mathematics, data, conditions, bounds, warnings, uncertainty, and evidence needed for precision. Parts 4, 5, and 7 and the selected profile govern this layer.
- The **plain layer** is the prose and explanatory structure that carries the exact layer to the base reader plus the selected profile overlay. Parts 2–4 and 6 govern this layer.

The plain layer **wraps** the exact layer. The plain layer **shall not replace** the exact layer. The following conditions apply:

1. Each exact-layer item **shall** have the precision required by the selected profile. A design RFC states enforceable requirements and interface bounds. A procedure states executable steps and checks. An investigation log distinguishes observations from hypotheses. A research paper matches each claim's strength to its evidence.
2. A plain-language rendering **shall** preserve the exact item's meaning, scope, strength, conditions, and normative force. The rendering **shall** remain traceable under §5.1.
3. Simplification **may** omit detail only from an explanation when the omission does not change an exact item. Simplification **shall not** weaken a requirement or alter an interface or invariant. Simplification **shall not** omit a procedure prerequisite, hazard, step, or verification condition. Simplification **shall not** detach an observation or measurement from necessary interpretive conditions.
4. A bounded block **may** carry high-resolution detail when the main line remains accurate without that detail. The selected profile must also permit the reader to skip it (§4.6). Required operational or safety information is never skippable.

### 1.2.1 Acceptance questions

The two layers create three acceptance questions:

- **Exactness and ownership:** Is the exact layer correct, complete for the profile's purpose, internally consistent, and precise enough to verify or act on?
- **Scan utility:** Does the §4.12 scan path give the assumed reader the profile's correct shallow model? Does that model preserve applicable status, strength, and material boundaries?
- **Main-path utility:** Can the assumed reader follow the declared purpose from the §0.3 baseline and selected overlay? Can the reader proceed without inventing missing domain knowledge?

A document can be precise but unusable, scannable but false, or fluent but untrustworthy. Every tier addresses all three questions. The required evidence remains proportional to the tier.

### 1.2.2 Tier-proportional evidence

The declared conformance tier determines who performs the acceptance work:

1. At **`core`**, the author runs the version-pinned linter and records a profile-aware self-check of both layers. Independent review and reader testing are not required.
2. At **`reviewed`**, the `core` evidence remains. An independent subject-matter owner answers the exactness-and-ownership question. An independent reader proxy answers the reader-utility question. The two checks are review passes, not direct reader testing.
3. At **`publication`**, the `reviewed` evidence remains, and a fresh representative reader completes the independent reader test before release checks close the document.

A higher tier adds independent evidence. The higher tier does not change either layer's meaning. The profile minimums in §0.4.3 determine the least evidence permitted. The architecture does not force a reader test on a `core` document.

## 1.3 Rule anatomy

Every rule uses the following template, adapted from ASD-STE100's rule format. The template applies in Parts 2–8 and in every overlay file (§1.5). The template is mandatory for rule authors. A rule drafted outside the template is a specification defect.

```
#### Rule <part>.<section>.<n> — <short name>
**Class:** mandatory | recommended | permitted · **Machine-checkable:** yes | partial | no · **Source:** <framework or "original">
**Profiles:** <comma-separated canonical profile IDs; omit this line when universal>
**Constructs:** <comma-separated §1.6 construct conditions, or "any">
**Navigation:** target: <unit> · chunks: <§4.1 types or "any"> · slots: <Annex E slots or "any"> · layers: exact | plain | both · context: <scope> · rewrite: <guidance>
**Resources:** reads: <resources> · writes: <resources or "none">
**Relations:** <typed edges to other rules, or "none">
**Status:** deprecated since <version>; replacement <rule ID | none> (omit this line when active)

> <Normative statement using a §0.4 keyword. One requirement per rule.>

**Rationale:** <why the rule exists; which §1.1 principle it serves>

**Compliant:** <example that follows the rule>
**Non-compliant:** <minimal contrasting example that violates it>

**Cross-references:** <related rules, or "none">
```

Conventions:

- **One independently testable outcome per rule.** A rule may use multiple normative verbs only when the clauses express one invariant. Examples include positive and prohibited forms or both directions of a one-to-one mapping. Clauses that can pass or fail independently are separate rules with separate permanent IDs.
- **Universal by default.** A rule with no `**Profiles:**` line applies to all twelve profiles. The universal form is the normal shared-core form.
- **Explicit profile scope.** Any rule that does not apply to all profiles carries a `**Profiles:**` line. This requirement includes profile additions and exceptions. The line lists every applicable profile. The list uses canonical IDs from §0.2 in registry order. Labels, aliases, `all`, wildcards, and negative forms such as `except` are invalid.
- **Scoped rules live with their profile.** A rule that carries a `Profiles` line moves to the overlay file that §1.5 assigns. The move changes the rule's location only. The rule keeps its permanent ID, its section number, and its applicability.
- **Construct scope is not profile scope.** A rule about equations can remain universal even though only equations trigger it. The equation rule receives no `Profiles` line unless some profiles treat equations differently.
- **Exceptions name what they displace.** A profile-scoped exception identifies the general rule it modifies in its normative statement and cross-references. A `Profiles` line alone narrows applicability. The line does not silently override another rule.
- **Tiers are not profile metadata.** `Profiles` determines content-rule applicability. The conformance tier determines assurance evidence under §0.4.3 and §1.2.2.
- **Active is the default status.** Active rules omit `Status`. A withdrawn rule remains with `**Status:** deprecated since <version>; replacement <rule ID | none>`. Annex C retains its permanent ID.
- **The example pair is not optional.** A rule without a contrasting pair is not enforceable (P7). Examples use governed technical prose, not aerospace or generic filler.
- **Rule numbers are permanent** (§0.8). Numbers are assigned per section in drafting order and never reused.
- **Examples match applicability.** A universal rule may use any governed profile. A scoped rule's compliant and non-compliant examples use one of the listed profiles. The corpus as a whole represents all twelve profiles rather than defaulting to research prose.
- **Source traceability is mandatory.** `Source` names the adopted or adapted framework, or it names `original`. Framework examples include Diátaxis, ISO/IEC/IEEE 26514, and IEC/IEEE 82079-1. Annex F records the nature of reuse. A profile scope does not erase the source.
- **Machine-checkable** feeds §8.2. `yes` means a linter can flag violations without human judgment. `partial` means a linter can flag candidates for human confirmation.
- **Navigation metadata is mandatory and closed.** Every active rule carries the four §1.6 lines. Section 1.6 fixes their permitted values. An unknown value is a specification defect.

Applicability metadata examples:

```text
**Class:** mandatory · **Machine-checkable:** partial · **Source:** PlainLanguage.gov
```

With no `Profiles` line, this rule applies to all twelve profiles.

```text
**Class:** mandatory · **Machine-checkable:** yes · **Source:** IEC/IEEE 82079-1
**Profiles:** procedure, incident
```

This rule applies only to `procedure` and `incident`. A document in any other profile does not evaluate it. Omitting the line from a rule intended only for those profiles would make the rule universal and is therefore a specification defect.

## 1.4 Conflict resolution

Determine applicability before resolving a conflict:

1. A rule with no `Profiles` line enters the applicable set for every profile.
2. A rule with a `Profiles` line enters the set only when the document's declared profile is listed.
3. A construct-scoped rule enters the set only when its construct is present.

A rule outside the applicable set cannot conflict with an applicable rule. When two applicable rules conflict for one passage, the following precedence is fixed. Writers and reviewers **shall not** resolve the collision ad hoc. This order follows the normative-drafting discipline of ISO/IEC Directives Part 2:

1. **Exactness and safety over style.** Exact-layer obligations override sentence and presentation preferences. A length cap never justifies blurring a claim, weakening a requirement, changing an invariant, or omitting a procedural warning or verification step. Split, restructure, or layer the passage instead.
2. **Explicit profile exception over its named general rule.** A profile-scoped rule overrides a universal rule only when its normative statement expressly names the displaced rule and defines the exception. To narrow a mandatory rule, the exception must itself be mandatory. The exception cannot override (1).
3. **Structure over sentence.** Part 4 and the selected profile skeleton override Part 3 where they collide. Chunk integrity, required order, and task safety remain intact even where a sentence-level rewrite would be smoother.
4. **Mandatory over recommended.** Subject to items (1)–(3), a mandatory applicable rule wins against a recommended applicable rule, regardless of source.
5. **Normative text over notes.** Rule statements outrank rationales, examples, informative notes, and intuition blocks. Nothing outside a normative statement creates a requirement. The requirement follows ISO/IEC and IEC/IEEE 82079-1 discipline against hiding requirements or safety information in notes.
6. **Specific over general.** A rule scoped to a construct, profile element, or document location overrides a general rule for that construct, element, or location, subject to (1)–(5).

Known collisions resolved by this ordering:

- *Exact content vs. §3.1 sentence caps* — resolved by (1): split or layer, never blur. The same resolution applies to requirements, interface contracts, procedure steps, and measurements.
- *Procedure prerequisites and warnings vs. generic claim-first ordering* — resolved by (1) and (3): the profile's safe task order takes precedence. IEC/IEEE 82079-1 warning placement is not rearranged for rhetorical effect.
- *§6.5 deliberate redundancy vs. §2.1 no-variation* — not a collision. Redundancy repeats identical wording. §2.1 prohibits varied wording. Repetition is compliant only when verbatim-consistent.
- *§4.2 claim-first vs. §2.3 define-before-use* — resolved by (3) and the selected profile skeleton. A summary may state the point early in base-reader vocabulary. The exact restatement appears only after its domain terms are admitted. The two statements remain traceable under §5.1.
- *A profile-scoped exception vs. a universal rule* — resolved by (2) only when the exception names the universal rule. Merely listing a profile does not create an implied waiver.

Unresolved collisions found during drafting or review are specification defects. Record them in Annex G's `Unreleased` section. Resolve them by amending this section, not locally.

## 1.5 Specification layout and the load set

ITWS separates the shared core from twelve profile overlays. The separation lets a reader, writer, or tool load one profile without loading unrelated genres. A profile's overlay also declares its governed surface (§0.2.1); `maintenance-comment` is the only hosted-surface profile.

### 1.5.1 Layout

| Location | Contents |
|---|---|
| `spec/00-front-matter.md` through `spec/08-review-compliance-tooling.md` | the shared core, including every universal rule |
| `spec/annexes/` | the shared annexes A–G |
| `spec/overlays/<profile ID>/` | one profile's job, reader overlay, skeleton, and scoped rules |
| `spec/overlays/shared/<family>.md` | the rules that one profile family shares |

A profile family groups profiles that share genre rules. ITWS declares two families. The work-item family contains `epic`, `task`, and `subtask`. The report family contains `technical-report` and `research-paper`.

Each profile directory holds four files. `README.md` states the job, minimum tier, load set, assurance focus, and example pointers. `reader.md` states the Annex B genre-knowledge overlay. `skeleton.md` states the Annex E required sections. `rules.md` holds the rules scoped to that profile alone.

### 1.5.2 Rule placement

Every rule appears in exactly one file. Its `Profiles` metadata determines that file:

1. A rule with no `Profiles` line is shared core and stays in Parts 2–8.
2. A rule scoped to one profile goes in that profile's `rules.md`.
3. A rule scoped to several profiles of one family goes in that family's shared module.
4. A rule scoped to several profiles across families stays in Parts 2–8, where its `Profiles` line records the narrowing.

Placement never changes applicability, permanent IDs, or section numbers. Rule 4.11.1 keeps its ID and its §4.11 section although its text is in an overlay file. A core section whose rules all moved keeps its number and points to the files that hold them.

An overlay never repeats a shared-core rule (P8). A shared module never repeats a profile's scoped rule.

### 1.5.3 The load set

The load set for one governed document is the shared core, the shared annexes, exactly one profile directory, and the shared modules that the directory lists. A document loads no other overlay.

The registry in `spec/overlays/README.md` maps each profile to its directory and its modules. Each profile `README.md` states the same load set for one profile.

### 1.5.4 Enforcement

`tools/itws_index.py` fails when a rule sits outside the file that §1.5.2 requires. `tools/itws_overlays.py` fails when a profile directory, a registry row, or a declared minimum tier is missing or inconsistent. `tools/itws_compile.py` fails when a profile manifest and the generated checklist resolve different rule sets. Annex C records each rule's file, and `python3 tools/itws_check_all.py` runs every check in one command.

## 1.6 Rule navigation metadata (normative)

Sections 1.3 and 1.5 tell a reader which rules apply and where those rules live. Section 1.6 adds the metadata that lets a reader or tool find a rule from a passage instead of reading every part in order. The metadata describes the rule. The metadata never describes a governed document's prose.

### 1.6.1 What the metadata does and does not decide

The `Constructs` line is the only navigation field with normative force. It records the construct condition that the rule's own normative statement states, so §1.4 item 3 can be applied without re-reading the statement. A construct absent from a document removes the rule from that document's applicable set, exactly as §1.4 already provides.

Every field of the `Navigation`, `Resources`, and `Relations` lines is a navigation aid. A navigation field **shall not** narrow the profile envelope. The profile envelope is every active rule whose `Profiles` metadata admits the declared profile. A tool **shall** make the whole envelope available before it offers any narrower result.

A tool **shall not** decide which construct, chunk type, prose layer, skeleton slot, or claim a passage contains. A reader or an artificial-intelligence agent makes that judgment from the specification text. A tool may check that the judgment cites known identifiers and available rules. A tool cannot check that the judgment is correct.

### 1.6.2 Closed values

**Target** names the unit the rule judges. One rule names exactly one target: `document`, `collection`, `section`, `heading`, `chunk`, `sentence`, `list`, `word`, `term`, `symbol`, `equation`, `citation`, `figure`, `table`, `bounded-block`, `procedure-step`, `declaration`, `conformance-record`, `comment`, or `comment-set`.

**Constructs** names the conditions the rule states. The permitted values are `any`, `acronym`, `admitted-term`, `analogy`, `bounded-block`, `caveat`, `citation`, `claim`, `comment`, `comparison`, `connective`, `cross-reference`, `declaration`, `definition`, `diagram`, `domain-term`, `equation`, `figure`, `generalization`, `heading`, `hedge`, `host-anchor`, `interface`, `invariant`, `limitation`, `list`, `marker`, `measurement`, `name`, `noun-cluster`, `number`, `observation`, `parent-link`, `procedure-step`, `prohibited-phrase`, `pronoun`, `proposal-record`, `quantity`, `removal-condition`, `requirement`, `risk`, `section`, `speculation`, `statistic`, `symbol`, `table`, `title`, `tool-artifact`, `user-journey`, `verb`, `waiver`, `warning`, `word`, and `worked-example`. The value `any` **shall not** appear beside another value.

**Chunks** lists the §4.1 purposes the rule can reach, or `any`.

**Slots** lists the Annex E slots the rule targets, or `any`. Every named slot **shall** appear in at least one profile skeleton.

**Layers** is `exact`, `plain`, or `both`, matching §1.2.

**Context** states how much surrounding material a reviewer must hold: `local`, `neighboring`, `section`, `document`, or `collection`.

**Rewrite** states what a repair may attempt:

- `mechanical` — the violation and its repair are both determinate.
- `candidate` — a repair can be proposed, and a reader must accept it.
- `review` — a reader must decide the repair.
- `prohibited` — no repair may change the governed content on tooling authority alone.

**Resources** names what the rule reads and writes: `none`, `chunk-text`, `heading`, `declaration-block`, `term-ledger`, `symbol-ledger`, `exact-item-ledger`, `claim-ledger`, `evidence-ledger`, `cross-reference-ledger`, `skeleton-order`, `figure-ledger`, `citation-ledger`, `conformance-record`, `waiver-record`, `comment-text`, `host-anchor-ledger`, or `proposal-record`. Two repairs that write one resource can collide. Section 8.6 states the check.

**Relations** lists typed edges to other rules, separated by semicolons, or `none`. The permitted types are `requires`, `constrains`, `overrides`, `pairs-with`, and `validates`. A generated `exemplified-by` edge links a rule to its Annex D examples; an author never writes that edge. Every edge **shall** name an existing permanent rule ID.

### 1.6.3 Generated precedence

The §1.4 order is generated as a machine relation. Each rule receives one precedence layer:

| Layer | Name | Membership |
|---|---|---|
| 1 | exactness and safety | every rule of Parts 5 and 7 |
| 2 | profile exception | a profile-scoped rule that carries an `overrides` relation |
| 3 | structure | every rule of Parts 4 and 6 |
| 4 | class comparison | every remaining rule |

The generated layer is a restatement of §1.4, not a new rule. Section 1.4 remains authoritative when the two disagree, and the disagreement is a specification defect.

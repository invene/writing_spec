# Part 1 — Foundations and principles

Part 1 defines the architecture behind Parts 2–8. Part 1 covers one shared core, eight profiles, two prose layers, tiered evidence, fixed rule anatomy, and deterministic precedence. The architecture serves every profile in §0.2. Research is one overlay, not the default document model.

## 1.1 Purpose and design principles

Concrete rules elsewhere in the specification enforce each principle below. Each principle lists its trace, and Annex F records it.

**P1 — Clarity over brevity.** When a shorter sentence costs comprehension, the longer sentence wins. Compression is never a goal. The document spends the reader's effort.
*Enforced by:* §3.1 (length caps exist to serve clarity, not concision), §6.5 (deliberate redundancy is permitted), §4.6 (detail is layered, not deleted).

**P2 — One word, one meaning.** A term means one thing everywhere in a document, and one thing across all governed documents once it enters the glossary. Synonym variation for style is prohibited.
*Enforced by:* §2.1, §2.3, §5.2 (one symbol, one meaning), §6.5.

**P3 — Exactness preserved under plain prose.** Plain language carries technical content. Plain language never replaces or weakens that content. A simplification may omit nonessential detail from an explanation. A simplification may not change a claim, definition, requirement, interface, invariant, procedure, observation, or measurement.
*Enforced by:* §1.2 (the two-layer model), §5.1 (traceability of simplified statements), §5.6 (calibrated claim strength), and profile-specific exact-content rules.

**P4 — Reader effort is spent deliberately.** The base reader plus the selected genre-knowledge overlay (§0.3) gets a defined budget of new concepts. The document spends this budget explicitly. The document admits domain terms in order (§2.3), caps density (§4.8), and bounds skippable detail (§4.6).
*Enforced by:* §2.3, §4.6, §4.8.

**P5 — Specific over generic.** Every sentence should convey information that could not describe a different subject. The central failure is loss of specificity. Specific, verifiable facts become generic significance claims that fit any subject. Machine-generated prose often shows this failure. Most prohibitions in §§2.6, 3.10, 4.10, and 6.5 address this failure.
*Enforced by:* §2.6 (hype vocabulary and vague attribution), §3.10 (formulaic constructions), and §4.10 (canned section formulas).
*Also enforced by:* §5.4 (no naked percentages), §6.5 (hollow summaries), and §7.4 (bounded generalization).

**P6 — Technical assertions carry their basis.** A claim or observation carries its evidence, conditions, units, comparison, and uncertainty. A requirement carries its acceptance condition. An interface or invariant carries its bounds. A procedure carries its prerequisites, hazards, expected outcomes, and verification. The relevant basis appears where the assertion is made or is linked unambiguously.
*Enforced by:* §5.4, §5.6, §7.2, §7.3, Part 4 profile structures, and profile-specific rules.

**P7 — Rules are enforceable or they are not rules.** Every rule is written so a reviewer can point at the rule and a violating passage and be done. Preferences that cannot be applied that way do not become rules.
*Enforced by:* §1.3 (rule anatomy), §8.1–8.2 (checklist and lint), Annex C (every rule indexed with its machine-checkability).

**P8 — Common rules stay common, and differences stay explicit.** A rule applies to every profile unless a `Profiles` line says otherwise. A profile overlay contains only genuine genre differences. The overlay does not duplicate the shared core or smuggle in domain knowledge.
*Enforced by:* §0.2 (profile registry), §0.3 (reader overlays), §0.4.3 (applicability), §1.3 (metadata), and Annex C.

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

The two layers create two acceptance questions:

- **Exactness and ownership:** Is the exact layer correct, complete for the profile's purpose, internally consistent, and precise enough to verify or act on?
- **Reader utility:** Can the intended reader follow the declared purpose from the §0.3 baseline and selected overlay? Can the reader proceed without inventing missing domain knowledge?

A document that answers only the first question is precise but unusable. A document that answers only the second is fluent but untrustworthy. Every tier addresses both questions, but the required evidence is proportional to the tier.

### 1.2.2 Tier-proportional evidence

The declared conformance tier determines who performs the acceptance work:

1. At **`core`**, the author runs the version-pinned linter and records a profile-aware self-check of both layers. Independent review and reader testing are not required.
2. At **`reviewed`**, the `core` evidence remains. An independent subject-matter owner answers the exactness-and-ownership question. An independent reader proxy answers the reader-utility question. The two checks are review passes, not direct reader testing.
3. At **`publication`**, the `reviewed` evidence remains, and a fresh representative reader completes the independent reader test before release checks close the document.

A higher tier adds independent evidence. The higher tier does not change either layer's meaning. The profile minimums in §0.4.3 determine the least evidence permitted. The architecture does not force a reader test on a `core` document.

## 1.3 Rule anatomy

Every rule in Parts 2–8 uses the following template, adapted from ASD-STE100's rule format. The template is mandatory for rule authors. A rule drafted outside the template is a specification defect.

```
#### Rule <part>.<section>.<n> — <short name>
**Class:** mandatory | recommended | permitted · **Machine-checkable:** yes | partial | no · **Source:** <framework or "original">
**Profiles:** <comma-separated canonical profile IDs; omit this line when universal>
**Status:** deprecated since <version>; replacement <rule ID | none> (omit this line when active)

> <Normative statement using a §0.4 keyword. One requirement per rule.>

**Rationale:** <why the rule exists; which §1.1 principle it serves>

**Compliant:** <example that follows the rule>
**Non-compliant:** <minimal contrasting example that violates it>

**Cross-references:** <related rules, or "none">
```

Conventions:

- **One independently testable outcome per rule.** A rule may use multiple normative verbs only when the clauses express one invariant. Examples include positive and prohibited forms or both directions of a one-to-one mapping. Clauses that can pass or fail independently are separate rules with separate permanent IDs.
- **Universal by default.** A rule with no `**Profiles:**` line applies to all eight profiles. The universal form is the normal shared-core form.
- **Explicit profile scope.** Any rule that does not apply to all profiles carries a `**Profiles:**` line. This requirement includes profile additions and exceptions. The line lists every applicable profile. The list uses canonical IDs from §0.2 in registry order. Labels, aliases, `all`, wildcards, and negative forms such as `except` are invalid.
- **Construct scope is not profile scope.** A rule about equations can remain universal even though only equations trigger it. The equation rule receives no `Profiles` line unless some profiles treat equations differently.
- **Exceptions name what they displace.** A profile-scoped exception identifies the general rule it modifies in its normative statement and cross-references. A `Profiles` line alone narrows applicability. The line does not silently override another rule.
- **Tiers are not profile metadata.** `Profiles` determines content-rule applicability. The conformance tier determines assurance evidence under §0.4.3 and §1.2.2.
- **Active is the default status.** Active rules omit `Status`. A withdrawn rule remains with `**Status:** deprecated since <version>; replacement <rule ID | none>`. Annex C retains its permanent ID.
- **The example pair is not optional.** A rule without a contrasting pair is not enforceable (P7). Examples use governed technical prose, not aerospace or generic filler.
- **Rule numbers are permanent** (§0.8). Numbers are assigned per section in drafting order and never reused.
- **Examples match applicability.** A universal rule may use any governed profile. A scoped rule's compliant and non-compliant examples use one of the listed profiles. The corpus as a whole represents all eight profiles rather than defaulting to research prose.
- **Source traceability is mandatory.** `Source` names the adopted or adapted framework, or it names `original`. Framework examples include Diátaxis, ISO/IEC/IEEE 26514, and IEC/IEEE 82079-1. Annex F records the nature of reuse. A profile scope does not erase the source.
- **Machine-checkable** feeds §8.2. `yes` means a linter can flag violations without human judgment. `partial` means a linter can flag candidates for human confirmation.

Applicability metadata examples:

```text
**Class:** mandatory · **Machine-checkable:** partial · **Source:** PlainLanguage.gov
```

With no `Profiles` line, this rule applies to all eight profiles.

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

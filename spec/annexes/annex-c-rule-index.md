# Annex C — Rule index (generated)

**Status:** generated 2026-07-28 from ITWS 0.2.1-draft. Do not edit this annex by hand.

## C.1 Generation contract

For each rule in Parts 2–8, this annex records:

| Field | Source |
| --- | --- |
| Rule number | `#### Rule <n>` header; permanent under §0.8 |
| Short name | rule-header title |
| Class | `Class` metadata |
| Machine-checkable | `Machine-checkable` metadata |
| Profiles | `Profiles` metadata; absence means all profiles |
| Status | optional `Status` metadata; absence means active |
| Source framework | `Source` metadata; feeds Annex F |

The index is sorted numerically by rule number. It is the input to the §8.1 checklist generator, which filters rules by declared ITWS version and profile before grouping them into the four self-check passes. Tier obligations come from §0.4.3 and Part 8; they are not rule-profile metadata.

## C.2 Generation command

Regenerate this index after changing rule metadata:

```text
python3 tools/itws_index.py \
  --spec-dir spec \
  --out spec/annexes/annex-c-rule-index.md
```

After approving a new permanent rule ID, add `--update-registry` once to append it to `spec/rule-ids.txt`.

The generator validates rule IDs against `spec/rule-ids.txt` independently of the output path. It fails on a duplicate or removed rule number, an unregistered new ID without `--update-registry`, malformed metadata, an unknown profile ID, or a profile list outside canonical registry order. A deprecated rule remains in its source file with `**Status:** deprecated since <version>; replacement <rule ID | none>`; generation never drops its permanent ID.

Generate a document's §8.1 checklist from this annex:

```text
python3 tools/itws_checklist.py \
  --spec-version 0.2.1-draft \
  --profile <canonical profile ID> \
  --tier <core | reviewed | publication> \
  --out <document-checklist.md>
```

## C.3 Index

**Rule count:** 161

| Rule | Short name | Class | Machine-checkable | Profiles | Status | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 2.1.1 | One word, one meaning | mandatory | partial | all profiles | active | ASD-STE100 |
| 2.1.2 | No synonym variation | mandatory | partial | all profiles | active | ASD-STE100 |
| 2.1.3 | Prefer the plain verb | recommended | yes | all profiles | active | Google/Microsoft word lists, ASD-STE100 |
| 2.1.4 | Expand every acronym at first use | mandatory | yes | all profiles | active | Google/Microsoft style guides |
| 2.1.5 | One form per acronym after introduction | mandatory | yes | all profiles | active | Google/Microsoft style guides |
| 2.2.1 | The permitted-vocabulary test | mandatory | partial | all profiles | active | original (baseline enumerated in Annex B) |
| 2.3.1 | Define before first use | mandatory | yes | all profiles | active | original |
| 2.3.2 | Definitions stand only on lower rungs | mandatory | yes | all profiles | active | original |
| 2.3.3 | No forward references | mandatory | yes | all profiles | active | original |
| 2.3.4 | Definitions are operational | mandatory | no | all profiles | active | original |
| 2.4.1 | Substitutability | mandatory | no | all profiles | active | ISO 704 |
| 2.4.2 | No circular definitions | mandatory | partial | all profiles | active | ISO 704 |
| 2.4.3 | Genus and differentia | recommended | no | all profiles | active | ISO 704 |
| 2.4.4 | Definition length cap | mandatory | yes | all profiles | active | original (per ISO 704 single-phrase convention, relaxed) |
| 2.4.5 | No definition by synonym or citation alone | mandatory | partial | all profiles | active | ISO 704, original |
| 2.5.1 | Documents do not contradict the glossary | mandatory | partial | all profiles | active | original |
| 2.5.2 | Use canonical wording at definitional first use | recommended | partial | all profiles | active | original |
| 2.5.3 | Recurring terms are proposed to the glossary | recommended | no | all profiles | active | original |
| 2.6.1 | No jargon as shorthand | mandatory | partial | all profiles | active | PlainLanguage.gov |
| 2.6.2 | No opaque named artifacts | mandatory | partial | all profiles | active | Google style guide, original |
| 2.6.3 | No unearned superlatives | mandatory | yes | all profiles | active | Google style guide, PlainLanguage.gov |
| 2.6.4 | The prohibited-word list (living) | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" |
| 2.6.5 | Agency language requires an operational definition | mandatory | partial | all profiles | active | original (extends Google's anthropomorphism guidance) |
| 2.6.6 | No warpath markers | mandatory | yes | all profiles | active | original (phrase-level enforcement of §4.9) |
| 2.6.7 | No editorializing asides | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" |
| 2.6.8 | No vague attribution or source-count inflation | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 2.6.9 | No gap-speculation phrasing | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 2.6.10 | Connectives earn their place | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" |
| 2.6.11 | No conversational or template artifacts | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" |
| 2.7.1 | Names are admitted like terms | mandatory | partial | all profiles | active | original (extends §2.3) |
| 2.7.2 | Descriptive names over allusive names | recommended | no | all profiles | active | Google naming conventions |
| 2.7.3 | One name per artifact | mandatory | partial | all profiles | active | Google naming conventions, ASD-STE100 |
| 2.7.4 | References to external artifacts are version-pinned | mandatory | partial | all profiles | active | Google style guide, ML Reproducibility Checklist |
| 3.1.1 | Descriptive sentence cap | mandatory | yes | all profiles | active | ASD-STE100 (adapted) |
| 3.1.2 | Load-bearing sentence cap | mandatory | partial | all profiles | active | ASD-STE100 (adapted) |
| 3.1.3 | Inline-math word counting | mandatory | yes | all profiles | active | original |
| 3.1.4 | Split, never blur | mandatory | no | all profiles | active | original |
| 3.2.1 | One idea per sentence | mandatory | no | all profiles | active | ASD-STE100 |
| 3.2.2 | One reviewable assertion per sentence | mandatory | no | all profiles | active | original (extends ASD-STE100) |
| 3.3.1 | Active voice by default | mandatory | partial | all profiles | active | ASD-STE100 + PlainLanguage.gov + Microsoft |
| 3.3.2 | "We" names the reporting actors | mandatory | partial | all profiles | active | original |
| 3.4.1 | Tense follows the table | mandatory | no | all profiles | active | ASD-STE100 + Google (adapted) |
| 3.4.2 | No ambiguous conditionals | mandatory | partial | all profiles | active | original |
| 3.5.1 | Three-noun cap | mandatory | yes | all profiles | active | ASD-STE100 |
| 3.5.2 | Admitted terms count as one noun | permitted | yes | all profiles | active | original |
| 3.6.1 | Unambiguous antecedents | mandatory | no | all profiles | active | ASD-STE100 + PlainLanguage.gov |
| 3.6.2 | No bare "this," "that," or "it" openers | mandatory | yes | all profiles | active | Google + Microsoft (adapted) |
| 3.7.1 | "Only" sits next to what it modifies | mandatory | partial | all profiles | active | Microsoft + Google |
| 3.7.2 | "Respectively" restricted | mandatory | yes | all profiles | active | Google + Microsoft (adapted) |
| 3.7.3 | One negation per clause | mandatory | partial | all profiles | active | ASD-STE100 + PlainLanguage.gov |
| 3.7.4 | Explicit quantifier scope | mandatory | no | all profiles | active | original (seeded by STE ambiguity rules) |
| 3.8.1 | No semicolon between independent clauses | mandatory | yes | all profiles | active | Google (tightened) |
| 3.8.2 | Serial comma | mandatory | yes | all profiles | active | Google |
| 3.8.3 | Connectives keep their reserved meaning | mandatory | partial | all profiles | active | ASD-STE100 + Google (adapted) |
| 3.9.1 | No vague hedges | mandatory | yes | all profiles | active | original (list seeded from PlainLanguage.gov and Wikipedia "Signs of AI writing") |
| 3.9.2 | Certainty language comes from §5.6 only | mandatory | partial | all profiles | active | original (mechanism forked from IPCC calibrated language) |
| 3.10.1 | No rule-of-three padding | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 3.10.2 | No negative parallelism | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" |
| 3.10.3 | No formulaic em dashes | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 3.10.4 | No trailing significance participles | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" |
| 3.10.5 | No false ranges | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 3.10.6 | No copula avoidance | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" + ASD-STE100 (simple verbs) |
| 4.1.1 | One purpose per chunk | mandatory | partial | all profiles | active | Information Mapping |
| 4.2.1 | Main point before qualification in a sentence | recommended | no | all profiles | active | PlainLanguage.gov |
| 4.2.2 | Chunk opens with its point | mandatory | partial | all profiles | active | PlainLanguage.gov / pyramid principle |
| 4.2.3 | Section opens with its takeaway or purpose | mandatory | no | all profiles | active | pyramid principle |
| 4.2.4 | Document states its main point before detail | mandatory | no | `design-rfc`, `decision-record`, `procedure`, `explanation`, `incident`, `technical-report`, `research-paper` | active | PlainLanguage.gov / IMRaD (adapted) |
| 4.3.1 | Declare the profile | mandatory | yes | all profiles | active | Diátaxis (adapted) |
| 4.3.2 | Stay in the profile job | mandatory | no | all profiles | active | Diátaxis |
| 4.3.3 | Annex E required sections are present | mandatory | yes | all profiles | active | ISO/IEC/IEEE 26514 (adapted) |
| 4.4.1 | Use the declared profile skeleton | mandatory | yes | all profiles | active | Diátaxis / IMRaD (adapted) |
| 4.4.2 | Seed prerequisites before load-bearing detail | mandatory | partial | all profiles | active | original |
| 4.4.3 | State the main outcome plainly, then exactly | mandatory | no | `design-rfc`, `decision-record`, `procedure`, `incident`, `technical-report`, `research-paper` | active | original |
| 4.5.1 | Headings are informative | mandatory | partial | all profiles | active | PlainLanguage.gov / Google Developer Style Guide |
| 4.6.1 | Exact detail beyond the plain layer goes in a bounded block or appendix | mandatory | no | all profiles | active | original |
| 4.6.2 | Bounded blocks use the standard markup | mandatory | yes | all profiles | active | original |
| 4.6.3 | Main text passes the skip test | mandatory | no | all profiles | active | original |
| 4.7.1 | A section opens by locating itself | mandatory | no | all profiles | active | original |
| 4.7.2 | Forward pointers are few and explicit | recommended | partial | all profiles | active | original |
| 4.7.3 | Cross-references cite numbers, not positions | mandatory | yes | all profiles | active | Google Developer Style Guide |
| 4.8.1 | At most three term admissions per page | mandatory | yes | all profiles | active | original |
| 4.8.2 | Sections stay under the length ceiling | recommended | yes | all profiles | active | original |
| 4.8.3 | Subsections stay under the length ceiling | recommended | yes | all profiles | active | original |
| 4.9.1 | No residual-history asides | mandatory | partial | all profiles | active | Google Developer Style Guide (timeless documentation, extended) |
| 4.9.2 | Necessary path information is promoted to a framed prior | mandatory | no | all profiles | active | original |
| 4.9.3 | Every path reference passes delete-or-promote | mandatory | no | all profiles | active | original |
| 4.10.1 | Headings use sentence case | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" / Google Developer Style Guide |
| 4.10.2 | Boldface is earned and rare | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 4.10.3 | No inline-header lists in place of prose | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 4.10.4 | No tables for what a sentence says better | recommended | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 4.10.5 | No emoji | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" |
| 4.10.6 | No canned section formulas | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 5.1.1 | Simplification preserves exact meaning | mandatory | no | all profiles | active | original |
| 5.1.2 | Simplified statements trace to exact statements | mandatory | partial | all profiles | active | original |
| 5.2.1 | Define every non-baseline symbol at first use | mandatory | partial | all profiles | active | original (mechanism from §2.3) |
| 5.2.2 | One symbol, one meaning | mandatory | yes | all profiles | active | ASD-STE100 (adapted) |
| 5.2.3 | Notation table above six symbols | mandatory | yes | all profiles | active | original |
| 5.3.1 | Every displayed equation gets a plain-language reading | mandatory | partial | all profiles | active | original |
| 5.3.2 | Keep inline math atomic | mandatory | partial | all profiles | active | original |
| 5.4.1 | Material statements carry a complete evidence record | mandatory | partial | all profiles | active | ISO/IEC/IEEE 26514; IEC 82079-1; APA JARS / NeurIPS checklist (research adaptation) |
| 5.4.2 | No naked percentages | mandatory | partial | all profiles | active | ISO/IEC/IEEE 26514; APA JARS (effect size + uncertainty, restated) |
| 5.4.3 | Every citation resolves | mandatory | yes | all profiles | active | Wikipedia "Signs of AI writing" (citations) |
| 5.4.4 | Cited sources support the claim | mandatory | no | all profiles | active | Wikipedia "Signs of AI writing" (citations) |
| 5.4.5 | Source counts are accurate | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" (source-count inflation) |
| 5.5.1 | Label axes, units, and series completely | mandatory | partial | all profiles | active | APA / IEEE figure conventions |
| 5.5.2 | The caption states the takeaway | mandatory | no | all profiles | active | ISO/IEC/IEEE 26514; Nature-style figure guidance |
| 5.5.3 | Figures stand alone for the assumed reader | mandatory | partial | all profiles | active | original |
| 5.6.1 | Strength and authority language comes from the table only | mandatory | partial | all profiles | active | IPCC calibrated language (mechanism) |
| 5.6.2 | Strength matches the evidential standard | mandatory | no | all profiles | active | IPCC calibrated language (mechanism) |
| 5.7.1 | Admit ladder-required statistical concepts before use | mandatory | partial | `technical-report`, `research-paper` | active | original (mechanism from §2.3) |
| 5.7.2 | Headline statistical results use bare concepts | mandatory | no | `technical-report`, `research-paper` | active | original |
| 5.8.1 | Reports include the applicable checkability statement | mandatory | yes | `technical-report`, `research-paper` | active | ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS checklist / ML Reproducibility Checklist (research adaptation) |
| 5.8.2 | The statement reads in assumed-reader vocabulary | mandatory | partial | `technical-report`, `research-paper` | active | original |
| 6.1.1 | Anchor analogies in assumed-reader vocabulary | mandatory | no | all profiles | active | original |
| 6.1.2 | State the breaking point | mandatory | partial | all profiles | active | original |
| 6.1.3 | At most one analogy per concept | mandatory | partial | all profiles | active | original |
| 6.2.1 | Central mechanisms get a worked example | mandatory | no | all profiles | active | Carroll minimalism |
| 6.2.2 | Examples carry no incidental complexity | mandatory | no | all profiles | active | Carroll minimalism / Google style guide |
| 6.2.3 | Examples use realistic values | recommended | no | all profiles | active | Google style guide |
| 6.3.1 | Intuition is bounded and labeled | mandatory | yes | all profiles | active | ASD-STE100 (note blocks) |
| 6.3.2 | Exact content does not live only in intuition blocks | mandatory | partial | all profiles | active | ISO/IEC Directives Part 2 |
| 6.3.3 | Main text survives block removal | mandatory | no | all profiles | active | original |
| 6.4.1 | Diagram structures that prose cannot carry | recommended | no | all profiles | active | ISO/IEC/IEEE 26514 / IEC 82079-1 |
| 6.4.2 | Every diagram is referenced from the text | mandatory | yes | all profiles | active | ISO/IEC/IEEE 26514 |
| 6.4.3 | Diagram labels use admitted terms only | mandatory | yes | all profiles | active | original |
| 6.4.4 | Diagrams carry alt text | recommended | yes | all profiles | active | Google style guide |
| 6.5.1 | Repeat verbatim or not at all | mandatory | partial | all profiles | active | ASD-STE100 |
| 6.5.2 | Recall distant definitions at reuse | recommended | yes | all profiles | active | original (instructional-design spaced recall) |
| 6.5.3 | Recap the ladder at part boundaries | permitted | yes | all profiles | active | original |
| 6.5.4 | No hollow summaries | mandatory | partial | all profiles | active | Wikipedia "Signs of AI writing" |
| 7.1.1 | Boundary material is required | mandatory | partial | all profiles | active | ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS Paper Checklist (research adaptation) |
| 7.1.2 | State the scope of validity | mandatory | no | all profiles | active | ISO/IEC/IEEE 26514; IEC 82079-1; NeurIPS Paper Checklist / Model Cards (research adaptation) |
| 7.1.3 | Disclose known failure modes and adverse effects | mandatory | no | all profiles | active | ISO/IEC/IEEE 26514; IEC 82079-1; Model Cards (research adaptation) |
| 7.1.4 | Disclose what was not tested or verified | mandatory | no | all profiles | active | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / Datasheets for Datasets (research adaptation) |
| 7.1.5 | Disclose data limitations | mandatory | no | all profiles | active | ISO/IEC/IEEE 26514; Datasheets for Datasets (research adaptation) |
| 7.1.6 | Plausible boundary gaps are explicit | mandatory | partial | all profiles | active | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist (research adaptation) |
| 7.2.1 | Caveats attach to their claims | mandatory | no | all profiles | active | IEC 82079-1 / ASD-STE100 (warning placement) |
| 7.2.2 | Boundary material aggregates, it does not replace | mandatory | no | all profiles | active | IEC 82079-1 |
| 7.3.1 | Separate observation from interpretation | mandatory | partial | `incident`, `technical-report`, `research-paper`, `investigation-log` | active | ISO/IEC/IEEE 26514; IMRaD / APA JARS (research adaptation) |
| 7.3.2 | Speculation only in marked blocks | mandatory | yes | `incident`, `technical-report`, `research-paper`, `investigation-log` | active | original (§6.3 mechanism) |
| 7.3.3 | Speculation uses the speculative tier | mandatory | partial | `incident`, `technical-report`, `research-paper`, `investigation-log` | active | IPCC calibrated language (via §5.6) |
| 7.4.1 | Extrapolations name the target setting | mandatory | no | all profiles | active | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / APA JARS (research adaptation) |
| 7.4.2 | Beyond the boundary, drop evidential strength | mandatory | partial | all profiles | active | ISO/IEC/IEEE 26514; NeurIPS Paper Checklist / CONSORT (research adaptation) |
| 8.1.1 | Checklist is generated, not authored | mandatory | yes | all profiles | active | STE checker workflows |
| 8.1.2 | Four self-check passes | mandatory | yes | all profiles | active | original |
| 8.1.3 | Regeneration on rule change | mandatory | yes | all profiles | active | original |
| 8.2.1 | Lint gate | mandatory | yes | all profiles | active | Vale / STE checker practice |
| 8.2.2 | Severity maps to rule class | mandatory | yes | all profiles | active | original |
| 8.2.3 | Version-pinned checking | mandatory | yes | all profiles | active | original |
| 8.2.4 | Machine checks do not close human gates | mandatory | no | all profiles | active | original |
| 8.3.1 | Publication gate | mandatory | no | all profiles | active | ISO 26514 / plain-language testing practice |
| 8.3.2 | Participant sampling | mandatory | no | all profiles | active | plain-language testing practice |
| 8.3.3 | Protocol and pass criteria | mandatory | no | all profiles | active | teach-back method, adapted |
| 8.3.4 | Reader-test failures are recorded | mandatory | no | all profiles | active | original |
| 8.3.5 | Failed documents are revised and independently retested | mandatory | no | all profiles | active | original |
| 8.4.1 | Reviewed tiers use two independent roles | mandatory | no | all profiles | active | ISO 26514 / IEC 82079-1 review process |
| 8.4.2 | Subject-matter-owner scope | mandatory | no | all profiles | active | ISO 26514, renamed to §1.2 |
| 8.4.3 | Assumed-reader proxy scope | mandatory | no | all profiles | active | ISO 26514, renamed to §1.2 |
| 8.4.4 | Findings cite rules | mandatory | partial | all profiles | active | original |
| 8.5.1 | Deviation requires a recorded waiver | mandatory | partial | all profiles | active | IEC 82079-1 / engineering-standard practice |
| 8.5.2 | Waiver content | mandatory | yes | all profiles | active | engineering-standard practice |

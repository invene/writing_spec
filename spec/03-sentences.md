# Part 3 — Sentences

Part 3 is shared core. Every rule in this part applies to every ITWS profile. Part 3 governs sentence length, load, voice, tense, reference, punctuation, and prohibited formulaic constructions.

ASD-STE100 supplies the base rules. PlainLanguage.gov and Microsoft supply passive-voice exceptions. The Google Developer Style Guide supplies punctuation guidance. Wikipedia's "Signs of AI writing" seeds §3.10.

Two sections are custom. Section 3.1 counts inline mathematics. Section 3.9 makes §5.6 the only source of permitted certainty language.

Part 5 exactness wins any collision with a sentence rule (§1.4). Split or layer the sentence. Never blur a claim, requirement, decision, or operational fact.

## 3.1 Sentence length

Two caps apply, following STE's two-tier structure. A *load-bearing sentence* admits a term or states a claim, requirement, decision, instruction, warning, or operational outcome. A *descriptive sentence* is any other sentence. Load-bearing sentences get the tighter cap because readers must retain or act on them exactly.

#### Rule 3.1.1 — Descriptive sentence cap
**Class:** mandatory · **Machine-checkable:** yes · **Source:** ASD-STE100 (adapted)
**Constructs:** any
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 3.1.3; constrains 3.1.4

> A descriptive sentence **shall not** exceed 25 words, counted per Rule 3.1.3.

**Rationale:** Long sentences force the reader to hold unresolved structure in memory. STE's cap has decades of use across technical documentation. ITWS allows scoped qualifications but not a paragraph disguised as a sentence. Serves P1 and P4.

**Compliant:** "The gateway stayed available in eight of nine failure tests. In the ninth, both replicas restarted together."
**Non-compliant:** "The gateway stayed available in eight of the nine failure tests while in the ninth test both replicas restarted together after receiving the same invalid configuration."

**Cross-references:** Rule 3.1.2, Rule 3.1.4, Rule 3.2.1.

#### Rule 3.1.2 — Load-bearing sentence cap
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100 (adapted)
**Constructs:** claim
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 3.1.3; constrains 3.1.4

> A load-bearing sentence **shall not** exceed 20 words, counted per Rule 3.1.3.

**Rationale:** These are the sentences readers must retain, verify, implement, or act on exactly. A load-bearing sentence too long to hold in mind fails regardless of its correctness. Serves P4 and supports §2.4's definition-quality rules.

**Compliant:** "The migration shall keep write unavailability below 30 seconds."
**Non-compliant:** "The migration shall, during all planned production phases and under the expected request load, keep write unavailability below a total duration of 30 seconds."

**Cross-references:** §2.3, §2.4, §5.6.

#### Rule 3.1.3 — Inline-math word counting
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** equation
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: none
**Relations:** validates 3.1.1; validates 3.1.2

> Under Rules 3.1.1 and 3.1.2, one mathematical symbol **shall** count as one word. An inline expression containing any operator **shall** count as three words.

**Rationale:** Symbols are not free because the reader decodes each one. Three words reflect a composite expression's reading cost. The count moves heavy expressions toward display math. Section 5.3 also requires a plain-language reading. Serves P4.

**Compliant:** "The loss L decreases for the first 10,000 steps." L counts as one word. The sentence counts as nine.
**Non-compliant:** Treating "the quantity L(θ) − L(θ′) over successive checkpoints" as adding two words to the count. (The expression contains operators and counts as three; writers who need several such expressions in one sentence must split or move to display math.)

**Cross-references:** §5.3, §1.4 collision list.

#### Rule 3.1.4 — Split, never blur
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** claim
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: chunk-text, exact-item-ledger · writes: chunk-text
**Relations:** constrains 3.1.1; constrains 3.1.2; requires 5.1.1

> When an exact statement exceeds a cap, the writer **shall** split it or move only non-action-critical detail. Moved detail **shall** use display math or a bounded block. The writer **shall not** remove precision to meet a cap.

**Rationale:** This rule applies §1.4. Exactness and safety override sentence length. Claims, requirements, stop conditions, warnings, and verification criteria keep their precision. Action-critical content also stays in the main flow. Serves P3.

**Compliant:** "The cache reduced median latency in every region tested. The reduction ranged from 18 ms to 31 ms."
**Non-compliant:** Rewriting that pair as "The cache broadly improved latency" to fit one sentence.

**Cross-references:** §1.4, §5.1, §4.6.

## 3.2 One idea, one reviewable assertion

#### Rule 3.2.1 — One idea per sentence
**Class:** mandatory · **Machine-checkable:** no · **Source:** ASD-STE100
**Constructs:** any
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 4.1.1

> A sentence **shall** express exactly one idea.

**Rationale:** A sentence carrying two ideas forces the reader to split them, and readers split them differently. STE's core rule transfers to every ITWS profile unchanged. Serves P1.

**Compliant:** "The worker drains its queue before shutdown. Draining prevents unfinished writes."
**Non-compliant:** "The worker drains its queue before shutdown, which prevents unfinished writes and also simplifies recovery."

**Cross-references:** Rule 3.2.2, §4.1 (one purpose per chunk).

#### Rule 3.2.2 — One reviewable assertion per sentence
**Class:** mandatory · **Machine-checkable:** no · **Source:** original (extends ASD-STE100)
**Constructs:** claim
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: chunk-text, claim-ledger · writes: chunk-text
**Relations:** requires 3.2.1

> A sentence **shall not** state more than one independently reviewable claim, requirement, decision, instruction, risk, or outcome.

**Rationale:** These assertions are the units that reviewers verify, teams trace, and readers cite. Two assertions in one sentence can share scope, evidence, or force accidentally, so at least one becomes harder to review correctly. Serves P6 and P7.

**Compliant:** "The API shall accept the old token format for 30 days. The API shall log each old-format request."
**Non-compliant:** "The API shall accept the old token format for 30 days and log each request so migration progress remains visible."

**Cross-references:** §5.6, §7.3.

## 3.3 Voice

Rule 3.3.1 permits passive voice only under these exceptions:

1. The actor is unknown or genuinely irrelevant.
2. The grammatical object is the chunk's established topic, and fronting it preserves continuity.
3. The preceding sentence names the actor, and the passive construction remains unambiguous.

#### Rule 3.3.1 — Active voice by default
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100 + PlainLanguage.gov + Microsoft
**Constructs:** verb
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 3.3.2

> A sentence **shall** use active voice unless an exception listed immediately above applies.

**Rationale:** Passive voice can hide the actor. The actor is often load-bearing in decisions, configuration changes, tests, and incident observations. The exception list merges the legitimate cases from PlainLanguage.gov and Microsoft. Serves P1.

**Compliant:** "The on-call engineer disabled the faulty rule." Also compliant under exception 1: "The rack was installed in 2019." (The installer is unknown and irrelevant.)
**Non-compliant:** "The faulty rule was disabled." (The responder is known, and the action belongs in the incident record.)

**Cross-references:** Rule 3.3.2, §5.8 (reproducibility and verification statements name actors for method steps).

#### Rule 3.3.2 — "We" names the reporting actors
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** pronoun
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 3.3.1

> "We" **shall** name only the document's authors or named reporting team as actors or claimants. "We" **shall not** include the reader.

**Rationale:** Reader-inclusive "we" blurs who observed, decided, or acted. "We can see a clear trend" asserts agreement before the reader has judged. The reporting actor owns the statement. The text must earn the reader's agreement. Serves P6.

**Compliant:** "We restarted the gateway at 14:32 UTC."
**Non-compliant:** "As we can see in Figure 3, the error spike is clear."

**Cross-references:** §5.5 (figures state their own takeaway), §7.3.

## 3.4 Tense and mood

Tense and mood follow one table. A governed document distinguishes stable facts, completed actions, instructions, proposals, and unresolved possibilities.

| Context | Tense | Example |
| --- | --- | --- |
| Properties of a system, method, policy, or artifact | present | "The gateway validates each token." |
| General truths and definitions | present | "A hash function maps inputs of any size to fixed-size outputs." |
| Completed actions and observations | past | "We restarted the worker. Errors stopped at 14:36 UTC." |
| Governing decisions and current requirements | present or direct requirement form | "Invoice writes use three regional replicas." |
| Procedure steps | imperative | "Stop the worker. Verify that its queue is empty." |
| Proposed or committed future behavior | explicit future or requirement form | "The gateway will reject the old token format after 30 days." |
| The document referring to itself | present | "Section 5 reports the latency results." |
| Untested predictions | future or conditional, inside a §7.3 block | "We hypothesize that the queue will grow during a longer outage." |

#### Rule 3.4.1 — Tense follows the table
**Class:** mandatory · **Machine-checkable:** no · **Source:** ASD-STE100 + Google (adapted)
**Constructs:** verb
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 3.4.2

> A sentence **shall** use the tense assigned by the §3.4 table for its context.

**Rationale:** Mixed tense and mood make the reader guess whether a sentence states current behavior, an observed event, an instruction, or a proposal. Those distinctions control implementation and preserve the observation/interpretation boundary (§7.3). Serves P6.

**Compliant:** "The gateway rejects expired tokens. During the incident, it accepted 214 expired tokens."
**Non-compliant:** "The gateway rejected expired tokens, and during the incident it accepts 214 expired tokens."

**Cross-references:** §7.3, Rule 3.4.2.

Allowed contexts for "would," "could," and "might" are marked risks, hypotheticals, counterfactuals, and speculation blocks (§7.3).

#### Rule 3.4.2 — No ambiguous conditionals
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original
**Constructs:** verb, hedge
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 3.4.1; pairs-with 5.6.1

> The covered forms **shall** appear only in the allowed contexts. They **shall not** report an observation, requirement, decision, or committed plan.

**Rationale:** "A second replica would prevent the outage" leaves its status unclear. The statement may describe a test, decision, or proposal. Observations take past tense. Requirements and decisions use direct forms. Untested projections use marked speculation with §5.6 calibration. Serves P6.

**Compliant:** "A second replica prevented interruption in all six failure tests." Or, in a marked speculation block: "We hypothesize that a region failure would still interrupt writes. We did not test that condition."
**Non-compliant:** "A second replica would likely prevent the remaining outage."

**Cross-references:** §5.6, §7.3, §2.6 (gap-speculation phrasing).

## 3.5 Noun clusters

#### Rule 3.5.1 — Three-noun cap
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100
**Constructs:** noun-cluster
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 3.5.2

> A noun cluster **shall not** contain more than three nouns. Longer stacks **shall** use prepositions or clauses.

**Rationale:** English noun stacks parse right-to-left without marked structure. Each added noun multiplies the possible groupings. Domain specialists apply parsing habits that the assumed reader may not share. Serves P1. Counting nouns needs a part-of-speech reading that §8.2 tooling cannot produce, so the linter reports a candidate and a reader confirms it.

**Compliant:** "the timeout for requests from the account service"
**Non-compliant:** "the account service request timeout setting"

**Cross-references:** Rule 3.5.2, §2.3.

#### Rule 3.5.2 — Admitted terms count as one noun
**Class:** permitted · **Machine-checkable:** partial · **Source:** original
**Constructs:** noun-cluster, admitted-term
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: document · rewrite: mechanical
**Resources:** reads: chunk-text, term-ledger · writes: none
**Relations:** requires 3.5.1

> An admitted multiword term **may** count as one noun under Rule 3.5.1.

**Rationale:** Once "attention head" is admitted, the term is one concept to the reader. The cap should measure concepts, not whitespace. The single-noun count keeps the cap from punishing the ladder it depends on. Serves P4. The count inherits Rule 3.5.1's part-of-speech limit, so it is `partial` for the same reason.

**Compliant:** "the deployment ring health threshold" where "deployment ring" is admitted (three countable nouns: deployment-ring, health, threshold).
**Non-compliant:** Counting "deployment ring" as one noun before the term has been admitted.

**Cross-references:** §2.3, Rule 3.5.1.

## 3.6 Pronouns and reference

#### Rule 3.6.1 — Unambiguous antecedents
**Class:** mandatory · **Machine-checkable:** no · **Source:** ASD-STE100 + PlainLanguage.gov
**Constructs:** pronoun
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: neighboring · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 3.6.2

> Every pronoun **shall** have exactly one grammatically plausible antecedent, located in the same sentence or the sentence before.

**Rationale:** "The gateway replaced the proxy because it failed under load" has two readings. The wrong reading inverts the decision record. Repeating the noun costs one word. Ambiguity costs the fact. Serves P1. Section 6.5 makes repetition compliant.

**Compliant:** "The gateway replaced the proxy because the proxy failed under load."
**Non-compliant:** "The gateway replaced the proxy because it failed under load."

**Cross-references:** Rule 3.6.2, §6.5.

**Phrase list 3.6.2 — bare openers (opener):** "this"; "that"; "these"; "those"; "it".

A covered opener is compliant when a noun follows it in the same noun phrase. "This queue" names its referent; bare "This" does not.

#### Rule 3.6.2 — No bare "this," "that," or "it" openers
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google + Microsoft (adapted)
**Constructs:** pronoun
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 3.6.1

> A sentence **shall not** open with a covered bare opener. The opener **shall** name its referent through a following noun.

**Rationale:** A bare "This shows..." can point at the last sentence, paragraph, or figure. Only the writer knows which referent applies. "This latency increase shows..." makes the writer name the referent. Naming can expose an unclear referent. Serves P1. The sentence-opener pattern is lintable.

**Compliant:** "This latency increase suggests the cache is saturated."
**Non-compliant:** "This suggests the cache is saturated."

**Cross-references:** Rule 3.6.1.

## 3.7 Ambiguity controls

#### Rule 3.7.1 — "Only" sits next to what it modifies
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Microsoft + Google
**Constructs:** word
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 3.7.4

> The word "only" **shall** immediately precede the word or phrase it modifies.

**Rationale:** "We only restarted the gateway in region A" has at least three readings. Each reading places "only" differently and records a different action. Serves P6.

**Compliant:** "We restarted the gateway only in region A."
**Non-compliant:** "We only restarted the gateway in region A."

**Cross-references:** Rule 3.7.4.

#### Rule 3.7.2 — "Respectively" restricted
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google + Microsoft (adapted)
**Constructs:** list
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 5.5.1

> "Respectively" **shall not** pair lists longer than two items. Pairings of three or more items **shall** be direct or tabular.

**Rationale:** "Respectively" makes the reader join two lists by index while suspending comprehension of both. Two items impose a tolerable cost. Beyond two items, the sentence becomes a lookup table in prose form. Section 5.5 governs tables. Serves P1.

**Compliant:** "Region A recovered in 12 minutes, and region B recovered in 18 minutes."
**Non-compliant:** "Regions A, B, and C recovered in 12, 18, and 31 minutes, respectively."

**Cross-references:** §5.5.

#### Rule 3.7.3 — One negation per clause
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100 + PlainLanguage.gov
**Constructs:** word
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 3.9.1

> A clause **shall not** contain more than one negation, including negative affixes ("un-," "non-") that interact with "not."

**Rationale:** Stacked negations require the reader to compute parity. "The effect is not inconsistent with our hypothesis" also hedges without calibration. Section 5.6 prohibits that hedge by other means. A positive statement forces the writer to choose a calibrated strength. Serves P1 and P6.

**Compliant:** "The evidence indicates that the observed effect matches our hypothesis."
**Non-compliant:** "The effect is not inconsistent with our hypothesis."

**Cross-references:** §3.9, §5.6.

Covered quantifiers are "all," "some," "every," "no," and "most."

#### Rule 3.7.4 — Explicit quantifier scope
**Class:** mandatory · **Machine-checkable:** no · **Source:** original (seeded by STE ambiguity rules)
**Constructs:** generalization
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 7.4.1

> A sentence with two covered quantifiers **shall** make their scope order unambiguous. The writer **shall** use per-item statements when needed.

**Rationale:** "Every region loses some requests" and "some requests fail in every region" are different incident findings. Compact phrasing lets the reader choose the stronger statement. Serves P6.

**Compliant:** "Each region lost at least one request class. No request class failed in every region."
**Non-compliant:** "All regions lost some request classes."

**Cross-references:** §7.4, Rule 3.7.1.

## 3.8 Punctuation and connectives

Punctuation follows the Google Developer Style Guide except where a rule below tightens it. Connectives are signals, and a signal that can mean anything means nothing: each connective is reserved for one relation.

| Relation | Permitted connectives | Notes |
| --- | --- | --- |
| contrast | but, however, whereas | "while" is temporal only; see Rule 3.8.3 |
| cause / consequence | because, so, therefore | "since" is temporal only; see Rule 3.8.3 |
| sequence | first / second / then, after, before | ordinal words, not "firstly" |
| addition | and, also, moreover, furthermore, additionally | covered connective padding: see §2.6 |
| concession | although, even though | one per sentence |
| example | for example | not "e.g." in running prose |

#### Rule 3.8.1 — No semicolon between independent clauses
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google (tightened)
**Constructs:** any
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 3.2.1

> A semicolon **shall not** join independent clauses. The writer **shall** use two sentences.

**Rationale:** A semicolon between clauses is a soft claim that the two ideas are one, which Rule 3.2.1 already prohibits. The only permitted semicolon use is separating list items that contain internal commas. Serves P1.

**Compliant:** "The test covered four queue sizes. Only the smallest avoided timeouts."
**Non-compliant:** "The test covered four queue sizes; only the smallest avoided timeouts."

**Cross-references:** Rule 3.2.1.

#### Rule 3.8.2 — Serial comma
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google
**Constructs:** list
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** none

> A list of three or more items **shall** use a comma before the final conjunction.

**Rationale:** Without the serial comma, the final two items can read as one compound item. In lists of conditions, systems, or evidence, that reading changes the record. Serves P6.

**Compliant:** "We tested the gateway, worker, and database."
**Non-compliant:** "We tested the gateway, worker and database."

**Cross-references:** none.

#### Rule 3.8.3 — Connectives keep their reserved meaning
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100 + Google (adapted)
**Constructs:** connective
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** constrains 2.6.10

> A connective **shall** express only its §3.8 relation. In particular, "since" and "while" **shall** express only time.

**Rationale:** "Since the queue filled" is causal or temporal depending on the reader's guess, and the two readings assign different roles to the event. Reserving each connective for one relation makes logic mechanically recoverable. Serves P1.

**Compliant:** "Because the queue filled, we rejected new jobs."
**Non-compliant:** "Since the queue filled, we rejected new jobs."

**Cross-references:** §2.6 (hollow connective inflation).

## 3.9 Hedging

Certainty language has one governing source: the calibrated vocabulary of §5.6. This section prohibits uncalibrated hedges. Section 3.9 defines no permitted alternatives.

**Phrase list 3.9.1 — vague hedges (word):** "somewhat"; "fairly"; "relatively"; "quite"; "arguably"; "rather"; "largely"; "generally" (prohibited for an assessment, permitted for a stated scope); "to some extent".

#### Rule 3.9.1 — No vague hedges
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original (list seeded from PlainLanguage.gov and Wikipedia "Signs of AI writing")
**Constructs:** hedge
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 5.6.1

> A covered hedge **shall not** modify a claim, risk, prediction, or reported outcome.

**Rationale:** Each covered word reduces a claim's strength without measuring the reduction. The reader must reconstruct the authors' actual confidence. Section 5.6 provides calibrated replacements. This list makes the uncalibrated forms lintable. Serves P6. The list remains under §2.5 governance.

**Compliant:** "Median latency rose 21 ms, from 68 ms to 89 ms." Or, calibrated: "The evidence indicates that sustained load weakens the cache."
**Non-compliant:** "Latency rose somewhat under load."

**Cross-references:** §5.6, §2.6, Rule 3.9.2.

#### Rule 3.9.2 — Certainty language comes from §5.6 only
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (mechanism forked from IPCC calibrated language)
**Constructs:** hedge, claim
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text, claim-ledger · writes: chunk-text
**Relations:** requires 5.6.1

> Every expression of confidence or claim strength **shall** use a §5.6 phrase. No other certainty phrasing is permitted.

**Rationale:** Two tables of permitted hedges would drift apart. One table cannot. Every certainty phrase maps through §5.6 to a defined evidential standard. A reader can convert the phrasing back into evidence. Serves P3 and P6.

**Compliant:** "We find that the new index halves median query time." ("We find" carries the §5.6 evidential standard for direct empirical support.)
**Non-compliant:** "It seems fairly safe to say that the new index improves query time."

**Cross-references:** §5.6, §7.3, §7.4.

## 3.10 Formulaic constructions (machine-generated-writing signs, sentence level)

The patterns below are prohibited on their merits. Each pattern adds filler, inflates significance, or blurs a claim, regardless of its author. The catalog comes from Wikipedia's "Signs of AI writing" guide. WikiProject AI Cleanup built the guide from thousands of flagged submissions. Conforming documents also avoid machine-generated phrasing. Vocabulary-level signs live in §2.6. Formatting-level signs live in §4.10. Hollow summaries live in §6.5.

#### Rule 3.10.1 — No rule-of-three padding
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** list
**Navigation:** target: list · chunks: any · slots: any · layers: plain · context: local · rewrite: review
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 2.6.4

> A list or series **shall not** be padded to three items for rhythm. Each item **shall** carry distinct information.

**Rationale:** The triplet is a rhetorical cadence, not an information structure. "Clear, concise, and compelling" repeats one idea in three words. The reader must inspect all three words to find one idea. A complete two-item list is better than a padded three-item list. Serves P5.

**Compliant:** "The method is simple to implement and cheap to run."
**Non-compliant:** "The method is simple, efficient, and effective."

**Cross-references:** §2.6 (puffery vocabulary).

**Phrase list 3.10.2 — contrast-reframe templates (pattern):** "\bis(?:n't| not)? just\b"; "\bnot only\b[^.]{0,60}\bbut also\b"; "\bnot merely\b"; "\bmore than just\b".

Rule 3.10.2 also covers "X rather than Y" when Y adds no information. A reader decides that case; the patterns above do not detect it.

#### Rule 3.10.2 — No negative parallelism
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** prohibited-phrase
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 2.6.4

> A document **shall not** use a covered contrast-reframe template. The writer **shall** state the positive content directly.

**Rationale:** Negative parallelism spends half the sentence denying a claim nobody made, purely to inflate the half that remains. The construction is lintable as a phrase pattern, and the rewrite is always available: delete the denial, keep the content. Serves P5.

**Compliant:** "The queue protects the database by limiting concurrent writes."
**Non-compliant:** "The queue isn't just a buffer — it's a control plane for resilience."

**Cross-references:** §2.6.

#### Rule 3.10.3 — No formulaic em dashes
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** any
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 3.8.3

> An em dash **shall not** replace an equivalent comma, colon, or parenthesis. An em dash **shall** mark only a genuine interruption or reversal.

**Rationale:** The em dash has become a default rhythm marker: statement — elaboration, statement — punchline. Each formulaic dash is a connective that refuses to name its relation, and Rule 3.8.3 requires relations to be named. Serves P1.

**Compliant:** "The deployment failed for one reason: the manifest named the wrong image."
**Non-compliant:** "The deployment failed for one reason — the manifest named the wrong image."

**Cross-references:** Rule 3.8.3.

**Phrase list 3.10.4 — trailing significance participles (phrase):** "highlighting the need for"; "underscoring the importance of"; "underlining the importance of"; "reflecting a broader trend"; "demonstrating the potential of"; "showcasing the"; "marking a significant".

#### Rule 3.10.4 — No trailing significance participles
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** prohibited-phrase
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 2.6.4

> A sentence **shall not** append a covered present-participle clause that asserts significance.

**Rationale:** The trailing participle puts an interpretation in the same sentence as an observation. The interpretation then appears to have the observation's evidential standing. A real significance claim needs its own sentence and §5.6 calibration. The claim also needs an interpretation chunk under §7.3. Serves P5 and P6. The phrase family is lintable.

**Compliant:** "The gateway failed all four region-loss tests. The evidence indicates that replication alone does not provide regional failover." (The second sentence is a calibrated interpretation chunk.)
**Non-compliant:** "The gateway failed all four region-loss tests, underscoring the importance of resilient architecture."

**Cross-references:** §5.6, §7.3.

#### Rule 3.10.5 — No false ranges
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"
**Constructs:** quantity
**Navigation:** target: sentence · chunks: any · slots: any · layers: exact · context: local · rewrite: candidate
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** requires 5.4.2

> "Ranges from X to Y" **shall** describe only endpoints of a measured or defined range. The phrase **shall not** spread rhetorical examples.

**Rationale:** "Applications range from healthcare to finance" sounds quantitative but says nothing. The examples are not endpoints, and the dimension does not exist. A real range informs. A false range decorates. Serves P5.

**Compliant:** "Latency ranged from 12 ms to 340 ms across the nine regions."
**Non-compliant:** "The system supports uses ranging from billing to scientific discovery."

**Cross-references:** §5.4.

Plain alternatives are "is," "has," and other direct verbs.

**Phrase list 3.10.6 — inflated copula substitutes (phrase):** "serves as" → "is"; "stands as" → "is"; "functions as" → "is"; "acts as" → "is"; "boasts" → "has"; "features" → "has"; "maintains" → "has"; "refers to" → "is" (prohibited only as a definition opener).

#### Rule 3.10.6 — No copula avoidance
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing" + ASD-STE100 (simple verbs)
**Constructs:** prohibited-phrase, verb
**Navigation:** target: sentence · chunks: any · slots: any · layers: plain · context: local · rewrite: mechanical
**Resources:** reads: chunk-text · writes: chunk-text
**Relations:** pairs-with 2.1.3

> When a plain verb states the fact, a writer **shall not** substitute a covered inflated form. A definition **shall not** open with "refers to."

**Rationale:** Machine-generated text often avoids plain "is" and "are." The substitutes add syllables and an implied claim of importance. "X refers to Y" defines a term when the sentence meant to describe its subject. STE's simple-verb discipline has the same purpose. Use "wrote," not "authored." Use "used," not "utilized." Serves P5.

**Compliant:** "The router is a two-process service. The router has four worker threads."
**Non-compliant:** "The router serves as a two-process service and boasts four worker threads."

**Cross-references:** §2.6 (puffery list), §2.4 (definition form).

# Part 2 — Words and vocabulary

Part 2 is shared core. Every rule in this part applies to every Invene Technical Writing Specification (ITWS) profile. Part 2 governs words and term admission.

Part 2 replaces ASD-STE100's closed dictionary with an open-but-gated vocabulary. The base reader and declared profile overlay supply some words and genre conventions (§0.3, Annex B). A document admits other terms through the term ladder (§2.3) before first use. Profile overlays grant genre knowledge, never product, system, operational, scientific, or other domain vocabulary.

Sections 2.1–2.2 give the general word rules and permitted baseline. Sections 2.3–2.5 define term admission, definition quality, and glossary governance. Sections 2.6–2.7 prohibit specific usage patterns and govern names.

## 2.1 General word rules

#### Rule 2.1.1 — One word, one meaning
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100

> A word or term **shall** carry exactly one meaning throughout a document.

**Rationale:** A reader who must re-derive a word's sense from context pays twice for the same word (P2). Engineering prose is dense with overloaded words such as "port," "node," "weight," and "state." A document that switches senses forces the reader to guess which sense is active.

**Compliant:** "A *node* is one running member of the storage cluster. The cluster has five nodes." (*node* has one meaning throughout.)
**Non-compliant:** "The cluster has five nodes. Each syntax-tree node stores a token." (*node* first means a running member, then a tree element.)

**Cross-references:** §2.3.1, §5.2 (one symbol, one meaning)

#### Rule 2.1.2 — No synonym variation
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ASD-STE100

> Later references to a named concept **shall** use the established term. They **shall not** substitute synonyms for variety.

**Rationale:** Elegant variation makes the reader ask whether "the gateway," "the service," and "the component" are three things or one (P2). Identical wording for identical meaning lets the reader stop checking.

**Compliant:** "The gateway validates each request. The gateway rejects requests without a token."
**Non-compliant:** "The gateway validates each request. The service rejects requests without a token. The component also records failures." (One concept, three names.)

**Cross-references:** §2.1.1, §6.5 (deliberate redundancy uses verbatim wording)

Rule 2.1.3 uses these plain-verb replacements:

- *use*, not *utilize*.
- *do*, not *perform*.
- *show*, not *demonstrate*, when the verb means *exhibit*.
- *wrote*, not *authored*.
- *is* or *has*, not *serves as* or *boasts*.

#### Rule 2.1.3 — Prefer the plain verb
**Class:** recommended · **Machine-checkable:** yes · **Source:** Google/Microsoft word lists, ASD-STE100

> A document **should** use the plain-verb replacements listed immediately above.

**Rationale:** Inflated verbs add syllables, not meaning, and displace the plain copula (P1, P5). The Google and Microsoft word lists supply ready adjudications. The §8.2 linter inherits them.

**Compliant:** "We used the same timeout for every request."
**Non-compliant:** "We utilized an identical timeout across the entirety of request-processing operations."

**Cross-references:** §3.10.6 (copula avoidance), §2.6.4

#### Rule 2.1.4 — Expand every acronym at first use
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google/Microsoft style guides

> At first use, an acronym or initialism not assumed by Annex B **shall** include its expansion and parenthesized short form.

**Rationale:** An unexpanded acronym is an undefined term with worse ergonomics: the reader cannot even guess it (P4). Expansion alone is not admission. Section 2.3 also applies when the expanded phrase contains non-assumed terms.

**Compliant:** "A service-level objective (SLO) is a measurable target for service behavior. This service's SLO is 99.9% availability."
**Non-compliant:** "The service meets its SLO."

**Cross-references:** §2.3.1, §2.6.2

#### Rule 2.1.5 — One form per acronym after introduction
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google/Microsoft style guides

> After introduction, a document **shall** use either the short form or the expanded form consistently, not both interchangeably.

**Rationale:** Alternating forms applies Rule 2.1.2's synonym variation to abbreviations. The reader must keep matching the pair again.

**Compliant:** "…service-level objective (SLO). The SLO permits 43 minutes of unavailability per month. The SLO applies to successful API requests."
**Non-compliant:** "…service-level objective (SLO). The service-level objective permits 43 minutes of unavailability. The SLO applies to successful API requests."

**Cross-references:** §2.1.2

## 2.2 The permitted general vocabulary

#### Rule 2.2.1 — The permitted-vocabulary test
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (baseline enumerated in Annex B)

> Every specialized term or sense **shall** be assumed under Annex B or admitted under §2.3 before first use.

**Rationale:** This rule is the open-but-gated replacement for a closed technical dictionary (P4). Ordinary English in its general sense is available under Annex B §B.1. Ask one question about a potentially specialized use. *Would the base reader plus this profile overlay define the sense or recognize the convention without help?* If not, the document must admit the sense. A profile may supply familiarity with "Timeline" or "Decision" as a section job. The profile cannot supply a system term such as *lease*. Disputes resolve against Annex B (§0.3.3).

**Compliant:** "The service switches to a replica when the active instance stops answering." (After *replica* is admitted.)
**Non-compliant:** "The leader renews its lease after reaching quorum." (*leader*, *lease*, and *quorum* are not assumed and have not been admitted.)

**Cross-references:** §0.3, §2.3.1, Annex B

## 2.3 Term admission — the term ladder

The ladder is this specification's core original mechanism. A document builds vocabulary as a program builds state: nothing is referenced before initialization. Each admitted term becomes a rung for the next definition. Section 5.2 applies the mechanism to mathematical symbols. Section 4.9 applies the same discipline to context.

#### Rule 2.3.1 — Define before first use
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original

> A term outside Rule 2.2.1's permitted vocabulary **shall** be defined before first body use, including Annex A terms.

**Rationale:** The reader climbs the ladder in reading order (P4). Use before definition forces the assumed reader to stall or continue with a gap. Every later sentence that uses the term inherits the gap.

**Compliant:** "A *quorum* is the smallest number of members that must agree before the cluster accepts a change. This cluster requires a quorum of three."
**Non-compliant:** "The cluster requires a quorum of three. (Quorum is defined in §4.)"

**Cross-references:** §2.2.1, §4.4 (where the ladder is seeded), §5.2

#### Rule 2.3.2 — Definitions stand only on lower rungs
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original

> A definition **shall** use only assumed vocabulary and terms already admitted in the document.

**Rationale:** A definition written in undefined terms defines nothing. Such a definition moves the gap one step back (P4). This rule makes the structure a ladder instead of a pile.

**Compliant:** "*Failover* is sending requests to a healthy replica after the active replica stops answering." The document admitted *replica* earlier. The other words are assumed.
**Non-compliant:** "*Failover* is leader promotion after consensus failure." (*leader promotion* and *consensus* are unadmitted.)

**Cross-references:** §2.3.1, §2.4.2

Forbidden promises under Rule 2.3.3 include "see §5," "defined below," and "as we will describe."

#### Rule 2.3.3 — No forward references
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original

> A document **shall not** use a term through a promise to define it later.

**Rationale:** A forward reference borrows against the reader's patience (P4). A term needed here also needs its definition here or earlier. If the definition cannot come earlier, the text using the term belongs later.

**Compliant:** "§4 explains how the cluster chooses one member to coordinate writes. Until then, this section describes only the write interface."
**Non-compliant:** "Leader election (see §4) prevents conflicting writes."

**Cross-references:** §2.3.1, §4.7

#### Rule 2.3.4 — Definitions are operational
**Class:** mandatory · **Machine-checkable:** no · **Source:** original

> A definition **shall** state what the thing is or does. The definition **shall** explain applicable inputs, outputs, or distinguishing properties. The definition **shall not** merely relate the term to other terms.

**Rationale:** The assumed reader needs a definition they can *run*: one that lets them predict what the term does in the next sentence (P3, P4). A relational gloss ("a transformer is a kind of neural architecture") is circular in effect even when not in form.

**Compliant:** "A *circuit breaker* is a control that temporarily stops calls to a failing service after too many calls fail."
**Non-compliant:** "A *circuit breaker* is a resilience primitive for fault-domain isolation."

**Cross-references:** §2.4.1, §2.4.2, §6.1

### A valid admission chain, worked

The following three-sentence chain admits *replica*, *health check*, and *failover*. Each rung stands only on assumed vocabulary and earlier rungs:

> A *replica* is a copy of a service or its stored data. A *health check* is a repeated test that reports whether a replica can accept requests. *Failover* is sending requests to a healthy replica after another replica stops accepting them.

*Replica* uses only assumed vocabulary. *Health check* stands on *replica*. *Failover* stands on both earlier terms. After these sentences, the document may use all three terms freely, and later definitions may stand on them.

### A non-compliant chain, for contrast

> We use Raft for leader election after a quorum failure. Consensus, described in §5, preserves linearizability.

The first sentence uses three unadmitted terms: *Raft*, *leader election*, and *quorum*. The second sentence uses *consensus* through a forward reference and defines nothing. *Linearizability* is also unadmitted. No rung reaches the ground.

## 2.4 Definition quality

#### Rule 2.4.1 — Substitutability
**Class:** mandatory · **Machine-checkable:** no · **Source:** ISO 704

> A definition **shall** replace the term in every document sentence without changing that sentence's meaning.

**Rationale:** Substitutability is the mechanical test that a definition actually covers the term's use (P7). If substitution produces nonsense somewhere, the definition and the usage have diverged.

**Compliant:** "A *retry limit* is the greatest number of times a client sends the same request again." Substitution in "the retry limit is three" preserves the meaning.
**Non-compliant:** "A *retry limit* is how we avoid overload." Substitution in "the retry limit is three" produces nonsense.

**Cross-references:** §2.3.4

#### Rule 2.4.2 — No circular definitions
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO 704

> A definition **shall not** use the defined term, its derivative, or any term that depends on it.

**Rationale:** A circular definition consumes a rung without adding one (P4). Cycles across entries ("training adjusts weights; weights are what training adjusts") are the two-step form of the same defect and equally prohibited.

**Compliant:** "*Overfitting* is when a model performs well on its training examples but poorly on new examples."
**Non-compliant:** "*Overfitting* is when a model fits the training data too well." (*fits* is the term's own root doing the defining.)

**Cross-references:** §2.3.2

#### Rule 2.4.3 — Genus and differentia
**Class:** recommended · **Machine-checkable:** no · **Source:** ISO 704

> A definition **should** name the nearest familiar category the thing belongs to, then state what distinguishes it within that category.

**Rationale:** "A kind of X that differs by Y" hands the reader an anchor before asking them to hold something new (P4). The genus must itself be assumed or admitted vocabulary.

**Compliant:** "A *deployment ring* is a group of systems that receives a release at the same time, before the next group receives it."
**Non-compliant:** "A *deployment ring* is a rollout cohort."

**Cross-references:** §2.3.4, §6.1 (analogies extend the same anchoring move)

#### Rule 2.4.4 — Definition length cap
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original (per ISO 704 single-phrase convention, relaxed)

> A definition **shall not** exceed two sentences or 40 words. Further explanation **shall** appear as separate prose.

**Rationale:** A definition is a rung, not a lecture (P4). Detail beyond the cap belongs in an explanation chunk or bounded block, where §4.6 lets the reader manage it.

**Compliant:** "A *lease* is permission to control a resource until a stated time."
**Non-compliant:** A ten-sentence paragraph that defines *lease*, compares coordination algorithms, explains clock drift, and recommends a library, all labeled as the definition.

**Cross-references:** §2.4.5, §4.8 (density budgets)

#### Rule 2.4.5 — No definition by synonym or citation alone
**Class:** mandatory · **Machine-checkable:** partial · **Source:** ISO 704, original

> A definition **shall not** consist only of a synonym, a translation into other jargon, or a citation.

**Rationale:** "Backpressure, i.e., flow control [12]" spends a rung and admits nothing. The synonym may be as unfamiliar as the term. The citation moves the ladder into another document that the assumed reader may not open (P4). Citations may accompany a definition. A citation cannot replace the definition.

**Compliant:** "*Backpressure* is a receiver's signal that makes a sender slow or stop until the receiver has capacity [12]."
**Non-compliant:** "We use backpressure (i.e., flow control; see [12])."

**Cross-references:** §2.3.2, §5.4 (citation integrity)

## 2.5 Glossary governance

Definitions live at two levels: per-document definitions written under §2.3–2.4, and canonical entries in the living glossary (Annex A). The flow between them:

1. **Draft** — a writer defines a term in a document under §2.3–2.4. Nothing else is required to use the term in that document.
2. **Propose** — The writer proposes a term for Annex A when it recurs across documents or is expected to recur. The proposal includes the drafted entry, its ladder prerequisites, relevant profiles, and a descriptive domain tag.
3. **Admit** — The glossary maintainer checks the entry against §2.3–2.4. The maintainer records prerequisites, profile relevance, domain tag, and version, then merges it. Profile and domain metadata describe expected use. They do not make the term assumed or prohibit its use in another profile. Admission is a minor version change (§0.8).
4. **Revise / deprecate** — Entry changes follow §0.8. Revisions carry version history. Superseded entries are deprecated and never deleted.

#### Rule 2.5.1 — Documents do not contradict the glossary
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original

> A governed document **shall not** contradict an Annex A term's meaning in its definition or use.

**Rationale:** The glossary is one-word-one-meaning (P2) lifted from document scope to organization scope. A document that quietly redefines a canonical term breaks every reader who carries the canonical meaning between documents.

**Compliant:** "We use *failover* as defined in the glossary: sending requests to a healthy replica after the active replica stops answering."
**Non-compliant:** "In this procedure, *failover* means restarting the active instance." (Annex A defines it otherwise.)

**Cross-references:** §2.3.1, Annex A

#### Rule 2.5.2 — Use canonical wording at definitional first use
**Class:** recommended · **Machine-checkable:** partial · **Source:** original

> At definitional first use, a document **should** quote the term's Annex A wording verbatim.

**Rationale:** Verbatim canonical wording helps readers recognize a term from another governed document (P2, §6.5). Readers need not compare two phrasings. Adaptation reinforces the term but does not carry its first definition.

**Compliant:** First use quotes the Annex A wording. A later recall says, "Recall that failover sends requests to a healthy replica."
**Non-compliant:** First use improvises a new phrasing while Annex A's differs in substance, leaving two competing definitions in circulation.

**Cross-references:** §2.5.1, §6.5

#### Rule 2.5.3 — Recurring terms are proposed to the glossary
**Class:** recommended · **Machine-checkable:** no · **Source:** original

> The second writer to define a term **should** propose it for Annex A.

**Rationale:** The glossary grows from real use, not speculation about possible needs. A second definition signals that a canonical entry will repay its cost.

**Compliant:** The second document to define *deployment ring* proposes the entry with its prerequisites.
**Non-compliant:** Five design documents each carry a different private definition of *deployment ring*, and none proposes a canonical entry.

**Cross-references:** §2.5.1, §0.8 (living lists), Annex A

## 2.6 Prohibited usage patterns

The rules in this section prohibit specific vocabulary-level patterns. Most show generic prose displacing specific prose (P5). Several make a structural rule lintable at the phrase level. Those rules cite their structural parent.

#### Rule 2.6.1 — No jargon as shorthand
**Class:** mandatory · **Machine-checkable:** partial · **Source:** PlainLanguage.gov

> A document **shall not** use field jargon as a compression device when permitted vocabulary can state the same thing.

**Rationale:** Jargon is a cache shared by insiders. The assumed reader has a cold cache (P4). Jargon that names a genuinely new concept enters through the ladder. Plain action language replaces jargon that only compresses an action.

**Compliant:** "We sent 5% of production requests to the new release and measured its error rate."
**Non-compliant:** "We canaried the release."

**Cross-references:** §2.2.1, §2.3.1

#### Rule 2.6.2 — No opaque named artifacts
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Google style guide, original

> A named technology, model, method, tool, standard, or system **shall** receive a plain-language introduction before bare use.

**Rationale:** "Raft," "Envoy," and "AdamW" can read as opaque product codes to the assumed reader. The name is a handle. The introduction supplies the object that the handle identifies.

**Compliant:** "The cluster uses Raft, a method for choosing one coordinator and agreeing on ordered changes."
**Non-compliant:** "The cluster uses Raft."

**Cross-references:** §2.1.4, §2.7.1

Rule 2.6.3 covers *state-of-the-art*, *novel*, *breakthrough*, *dramatic*, and *significant* outside its statistical sense.

#### Rule 2.6.3 — No unearned superlatives
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Google style guide, PlainLanguage.gov

> A covered term **shall not** appear unless the same sentence states the measurement that earns it.

**Rationale:** An adjective is a claim (P6). "State-of-the-art" backed by a table is a finding. Without evidence, it is marketing. Section 5.7 reserves the statistical sense of *significant*.

**Compliant:** "The new index cuts median query time from 82 ms to 41 ms, the lowest value among the four indexes tested."
**Non-compliant:** "Our novel index delivers a dramatic, state-of-the-art improvement."

**Cross-references:** §5.4, §5.6, §2.6.4

Seed list (ITWS 0.2): *delve, underscore(s) (as rhetorical emphasis), tapestry, testament, pivotal, crucial, robust (outside its statistical sense), showcase, intricate, fostering, garner, meticulous, vibrant, landscape (abstract), interplay (abstract), boasts, align with, bolstered.*

#### Rule 2.6.4 — The prohibited-word list (living)
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing"

> Except in quotations or discussion, a governed document **shall not** use an item on the prohibited-word list.

**Rationale:** These words commonly carry generic significance instead of specific information (P5). Their source does not affect the prohibition. Conforming documents also avoid machine-generated phrasing. The list is **era-specific and living** because model-era vocabulary changes. For example, the 2023 list differs from the 2025 list. The list remains a versioned artifact under §2.5 and §0.8. The rule does not freeze the enumeration.

**Compliant:** "The migration completed on all three clusters we tested."
**Non-compliant:** "This underscores the pivotal role of robust planning across the evolving infrastructure landscape."

**Cross-references:** §2.6.3, §3.10, §8.2 (the list ships as a linter asset)

Covered agency verbs are "wants," "believes," "knows," "understands," "thinks," "decides," and "tries."

#### Rule 2.6.5 — Agency language requires an operational definition
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (extends Google's anthropomorphism guidance)

> Software, models, and other automated systems **shall not** receive a covered agency verb before its operational definition.

**Rationale:** The assumed reader cannot tell how literally to take "the scheduler decides" or "the model knows." Specialists use these verbs as shorthand. Their operational definition often remains implicit (P3). State the observable behavior that the verb denotes. The verb then enters the document like any other term.

**Compliant:** "We say the scheduler *decides* when it selects the highest-priority runnable task. The scheduler decides once per cycle."
**Non-compliant:** "The scheduler decides that the worker wants more tasks."

**Cross-references:** §2.3.4, §7.3

Covered markers include "instead of the old approach," "unlike what we did before," "previously we," "as before," and "our earlier attempt."

#### Rule 2.6.6 — No warpath markers
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original (phrase-level enforcement of §4.9)

> A governed document **shall not** use a covered marker or equivalent.

**Rationale:** These phrases expose prose written relative to a history the reader does not share. Section 4.9 owns the structural rule. That rule requires deletion or promotion to a framed prior. Rule 2.6.6 owns the phrase list so §8.2 can lint it.

**Compliant:** "The gateway validates tokens before forwarding requests. Validation at the gateway prevents unauthenticated traffic from reaching internal services."
**Non-compliant:** "Unlike our earlier design, the gateway now validates tokens instead of using the old service check."

**Cross-references:** §4.9, §8.2

Covered importance-announcing asides are "it's important to note," "it should be emphasized," "notably," "interestingly," and "no discussion would be complete without."

#### Rule 2.6.7 — No editorializing asides
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing"

> A document **shall not** use the covered importance-announcing asides.

**Rationale:** Under claim-first ordering (§4.2), position and content signal importance. An importance-announcing aside admits that the structure failed (P5). A material point leads its chunk.

**Compliant:** "The error rate triples after the cache reaches capacity: 0.4% rises to 1.2%."
**Non-compliant:** "It is important to note that, interestingly, the error rate triples after the cache reaches capacity."

**Cross-references:** §4.2, §3.10

Covered authority phrases include "experts say," "studies show," "widely regarded as," and equivalents. The rule also covers plural attributions backed by fewer sources, such as "several publications" with one citation.

#### Rule 2.6.8 — No vague attribution or source-count inflation
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"

> Claims **shall** name and cite their sources. A document **shall not** use a covered authority phrase. A plural attribution **shall not** imply more sources than its citations provide.

**Rationale:** Vague attribution borrows authority without lending accountability (P6). The source count is part of the claim: "several studies" citing one study is a false statement about the evidence.

**Compliant:** "Two evaluations report the same failure mode [4, 11]."
**Non-compliant:** "Numerous studies have widely established this failure mode [4]."

**Cross-references:** §5.4 (citation integrity), §2.6.4

Covered gap phrases include "while specific details are limited, it is likely that" and "although not widely documented."

#### Rule 2.6.9 — No gap-speculation phrasing
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Wikipedia "Signs of AI writing"

> A document **shall not** replace absent evidence with speculation. The document **shall** report the absence.

**Rationale:** This pattern turns "we do not know" into a plausible guess presented as fact. The pattern violates the observation and interpretation separation (§7.3). The document reports unknown information as unknown. Warranted speculation belongs in a marked speculation block at §5.6-calibrated strength.

**Compliant:** "We did not measure memory use. The logs do not record it."
**Non-compliant:** "While memory figures are not documented, the method likely uses substantially less memory in practice."

**Cross-references:** §7.3, §5.6

Covered formulaic connectives are "moreover," "furthermore," and "additionally" when chained across consecutive sentences or paragraph openings.

#### Rule 2.6.10 — Connectives earn their place
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing"

> A document **shall not** stack covered connectives as padding. Each connective **shall** mark a §3.8 relation.

**Rationale:** A connective asserts a logical relation between sentences. Chained "furthermore"s assert relations that do not exist. The pattern teaches the reader to ignore every connective, including material ones (P5).

**Compliant:** "The service fails under sustained load. The failure rises with request rate: 12% at 1,000 requests per second and 31% at 8,000."
**Non-compliant:** "The service fails under load. Moreover, the failure is notable. Furthermore, request rate matters. Additionally, we measured this."

**Cross-references:** §3.8

Covered chat phrases include "I hope this helps," "certainly," "let's explore," and "would you like." Covered placeholders include "[Your Name]," "INSERT_URL," and "2025-XX-XX."

#### Rule 2.6.11 — No conversational or template artifacts
**Class:** mandatory · **Machine-checkable:** yes · **Source:** Wikipedia "Signs of AI writing"

> A governed document **shall not** contain a covered chat phrase or unfilled placeholder.

**Rationale:** These are tool-leakage artifacts: text addressed to a chat user or slots a template left empty. Their presence means the document was not read end-to-end by its author, which is a review failure before it is a style failure.

**Compliant:** (Their absence.)
**Non-compliant:** "Certainly! Let's explore the results below. Contact [Your Name] for the raw data."

**Cross-references:** §8.2 (mechanical artifact regexes)

## 2.7 Naming

Rule 2.7.1 covers organization-coined names for artifacts, components, services, experiments, datasets, and methods.

#### Rule 2.7.1 — Names are admitted like terms
**Class:** mandatory · **Machine-checkable:** partial · **Source:** original (extends §2.3)

> Before bare use, a covered name **shall** receive the plain-language introduction required by §2.3.

**Rationale:** An internal codename is a term with a private definition (P4). The ladder does not distinguish between vocabulary we inherited and vocabulary we invented.

**Compliant:** "We call the production request replay set EDGE-24: the sampled gateway requests from 2024 with credentials removed."
**Non-compliant:** "All load tests use EDGE-24 unless noted."

**Cross-references:** §2.3.1, §2.6.2

Rule 2.7.2 covers new artifacts, components, services, experiments, datasets, and methods. After the Rule 2.7.1 introduction, a document can use an allusive codename.

#### Rule 2.7.2 — Descriptive names over allusive names
**Class:** recommended · **Machine-checkable:** no · **Source:** Google naming conventions

> A covered item **should** receive a descriptive name.

**Rationale:** A descriptive name carries its own recall. "The production-request replay set" explains itself at every use. A reader must look up an allusive name such as "Project NIGHTJAR." Descriptive names spend less of the reader's budget (P4).

**Compliant:** "the production-request replay set"
**Non-compliant:** "NIGHTJAR-2 (successor to NIGHTJAR)" with no statement of what either is.

**Cross-references:** §2.7.1

Rule 2.7.3 covers named artifacts, components, services, experiments, datasets, and methods.

#### Rule 2.7.3 — One name per artifact
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Google naming conventions, ASD-STE100

> A covered item **shall** have exactly one name throughout a document. The document **shall not** add nicknames, shortened names, or renamings mid-document.

**Rationale:** Rule 2.1.2 applies to artifacts. "The edge gateway," "the proxy," and "the request service" may name one artifact or three. The reader should never maintain that mapping.

**Compliant:** "EDGE-GATEWAY" at every mention.
**Non-compliant:** "EDGE-GATEWAY" in §2, "the proxy" in §4, and "the request service" in §5, all denoting the same artifact.

**Cross-references:** §2.1.2, §5.2 (same discipline for symbols)

Covered external artifacts include libraries, tools, services, standards, models, datasets, and benchmarks. Accepted pins include a version, snapshot date, access date, digest, or equivalent identifier.

#### Rule 2.7.4 — References to external artifacts are version-pinned
**Class:** mandatory · **Machine-checkable:** partial · **Source:** Google style guide, ML Reproducibility Checklist

> A reference to a covered external artifact **shall** include an accepted pin.

**Rationale:** External artifacts change under stable names. "Kubernetes," "GPT-4," and "the Wikipedia dump" can denote different objects in different months. An unpinned name makes requirements, procedures, and claims unverifiable (P6, §5.8).

**Compliant:** "PostgreSQL 17.2 (container digest `sha256:…`)"
**Non-compliant:** "the latest PostgreSQL"

**Cross-references:** §5.4, §5.8

---

> **Drafting note (ITWS 0.2):** The prohibited-word seed list in Rule 2.6.4 is a versioned linter asset. The inline list above is the ITWS 0.2 snapshot. Organization-specific naming conventions belong in a separately versioned policy layered on this shared core.

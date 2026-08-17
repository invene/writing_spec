# Profile: `role-specification`

**ITWS version:** 1.0 · **Surface:** `markdown-document`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Specify a role for an operator running a hiring screen.

Explanation-family. Concepts and Mechanism build the model. Screening directs the operator. The unit is not `explanation`: no required Examples, and Screening is a slot. The unit is not `procedure`: the screen is this role's, not a general instruction set. Overlay cannot carry the forks: each changes a slot or displaces a core rule (core §0.4).

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the role, its mechanism, the screening signals and ramp set, and the role's boundaries.**

## Screening vocabulary

Available without definition in this profile.

**screening signal** — one numbered pair: an ask imperative and a listen-for imperative. **ramp set** — topics the screen does not filter on, because the role ramps them on the job.

## Reader overlay (genre knowledge only)

The reader recognizes a role specification: Concepts, Mechanism, and Screening (ask, listen-for, ramp set) that directs an operator. Navigation only.

The overlay grants **nothing else**. Hiring-method terms still enter through core §2.3. The actual audience is an operator running a screen. That narrowing does not change the baseline ([reader.md](../reader.md) §4).

## Skeleton

Dependency order: admit the domain vocabulary before the mechanism and screening steps that use it (core §4.4.2).

No `Examples` slot. A worked example of the role's mechanism, when present, lives in Mechanism (§4.17.10).

| Slot | Required | Job |
|---|---|---|
| Summary | yes | the role and why it exists, in assumed-reader vocabulary |
| Concepts | yes | domain terms and relationships admitted in ladder order (§2.3). Naming that vocabulary is this slot's job |
| Mechanism | yes | how the role works: responsibilities, operating mode, what success looks like |
| Screening | yes | numbered screening signals plus the ramp set |
| Limits | yes | role boundaries, trade-offs, and every applicable §7.1 dimension |

**Renames:** `Concepts` → `Key concepts` · `Mechanism` → `How the role works` · `Limits` → `Limits and trade-offs`.

**Merges:** `Concepts` + `Mechanism` → `Concepts and mechanism`, with the canonical jobs as separately labeled subsections. Screening stays its own top-level slot. No other merge.

## Boundary locations (core §7.1)

- **Limits** — role boundaries (what the role is not, what it does not own, hire-versus-ramp) and every applicable core §7.1 dimension. §7.1.4–§7.1.6 apply unchanged.

Role boundary is always applicable. A Limits slot that names only role boundaries and drops unverified conditions or data provenance without naming them as such fails §7.1.6.

## Evidence-record additions (core §5.4)

Screening signals, the ramp set, and any anonymized-client or internal-confidential evidence together with its confidentiality basis.

## §4.17 Scoped rules — role specifications

| ID | C | D | Rule |
|---|---|---|---|
| 4.17.1 | M | S | `Screening` is a numbered list of screening signals — each item an ask imperative paired with a listen-for imperative |
| 4.17.2 | M | S | `Screening` names the ramp set and states that those topics ramp on the job |
| 4.17.3 | M | J | named exception to §4.3.2: Screening and other operator-directed instructions may carry procedure-shaped content whose job is running this role's screen. The document ! independently perform `procedure`'s primary job |
| 4.17.4 | M | J | named exception to §3.4.1: operator-directed instructions in this profile (Screening signals, weighting instructions, filter instructions) use imperative mood. Other prose follows the §3.4 table |
| 4.17.5 | M | J | named exception to §4.8.1: the per-page admission budget does not apply; the bound is Concepts completeness — every non-baseline term used in the document has a Concepts entry |
| 4.17.6 | M | J | Concepts is the only admission home; Summary, Mechanism, Screening, and Limits introduce no new terms |
| 4.17.7 | R | S | the document admits ≤ 30 non-baseline terms — the document-level reader-effort bound replacing §4.8.1's per-page bound |
| 4.17.8 | M | J | named exception to §5.4.6 and to §2.6.8's cite-the-source clause: a material claim whose source is an anonymized client or an internal measurement the reader cannot be given may omit a resolvable locator when the claim's sentence or immediate context states the confidentiality basis that prevents one. The §5.4.1 evidence field records the class (anonymized client or internal measurement) plus that basis. ! invent a source. Listed vague-authority phrases stay prohibited. The exception makes a limitation visible and licenses no unsupported claim |
| 4.17.9 | M | J | a material claim whose evidence is anonymized-client or internal-confidential takes at most the observed tier. Unmarked it carries verified-tier force (§5.6) and fails §5.6.2. An internal measurement nobody can check is not verified-tier |
| 4.17.10 | M | J | named exception to §6.2.1: a worked example of the role's mechanism is not required; when present it lives in Mechanism |

Illustrative screening signal, not a quotation from a shipped document: "Ask the candidate how they would split a late-arriving fact table. Listen for a partition-and-backfill answer."

## Applicable core rules with profile scope

§4.2.4 applies. **§4.4.3 does not apply.** §7.3 is optional here.

§6 still applies as in `explanation`, except §6.2.1 as narrowed by §4.17.10.

**§5.6 still governs strength.** No profile exception. §4.17.9 states how the rule lands on confidential evidence.

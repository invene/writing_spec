# Profile: `research-paper`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document` · **Family:** report

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Report a research question, method, evidence, result, and limitations to publication standard.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **the research question, main result, evidential strength, uncertainty, and scope.**

## Reader overlay (genre knowledge only)

The reader recognizes IMRaD-derived navigation, treats citations as source pointers, and distinguishes results from discussion.

**This overlay expressly assumes no machine-learning knowledge.** Every ML term, method, benchmark, dataset, metric, convention, or symbol absent from [reader.md](../reader.md) §1–§2 requires admission — including *model*, *training*, *loss*, *gradient*, *embedding*, *transformer*, *attention*, *fine-tuning*, and *inference*. [glossary.md](../glossary.md) supplies canonical wording for many of them; an entry does not make a term assumed.

The overlay also assumes no formal statistics, algebra beyond arithmetic, linear algebra, calculus, optimization, research-community shorthand, venue conventions, or benchmark names.

## Skeleton

Dependency order: seed prerequisites before the methods, evidence, and claims that use them (core §4.4.2).

| Slot | Required | Job |
|---|---|---|
| Abstract | yes | state the claim first in assumed-reader vocabulary; include scope, strength, and a headline comparison where applicable |
| Introduction | yes | research question, importance, main claim, document map |
| Background from first principles | yes | the ladder-seeding section: admit every non-assumed term the main line needs, in dependency order |
| Method or what we built | yes | procedure and mechanism, with exact detail in bounded blocks where needed |
| Experimental setup | yes | data or materials, conditions, comparisons, measures, and symbols needed to interpret the evidence |
| Results | yes | observations and measurements, with uncertainty and self-contained figures or tables where applicable |
| Discussion | yes | interpretation, relation to prior evidence, bounded generalization; speculation stays labeled |
| Limitations | yes | scope of validity, known failure modes, untested cases, aggregation of claim-local caveats |
| Reproducibility statement | yes | plain-language account of what repeating the work requires, distinct from any technical appendix |

**Renames:** `Background from first principles` → a topic-specific heading, mapped via a section map · `Method or what we built` → `Method`, `Methods`, or `System` · `Discussion` → `Interpretation` · `Reproducibility statement` → `Reproducibility`.

**Merges:** `Method or what we built` + `Experimental setup` → `Methods`, with separate mechanism and setup subsections. `Results` + `Discussion` → `Results and discussion` **only when a publication format requires it**, and then with separately labeled observation and interpretation subsections. **`Background from first principles` shall not merge into `Introduction`.**

Optional appendices may hold full formalism, proofs, extended tables, instruments, or configuration. An appendix replaces no required job.

## Boundary locations (core §7.1)

- **Limitations** — every applicable dimension.
- **Reproducibility statement** — data, dependency, resource, and unavailable-input bounds on repeating the work.

## Evidence-record additions (core §5.4)

The statistical and reproducibility detail required by §5.7 and §5.8 below.

## §5.7 Statistical evidence

The reader has only [reader.md](../reader.md) §1 basic quantitative knowledge unless this document admits more.

**Bare** — usable without definition: count, minimum, maximum, range, mean or average, median, percentage, ratio, rate.

**Ladder-required** — admit under core §2.3 before use: mode and percentiles (including p50, p99) · standard deviation, variance, standard error · confidence interval, p-value, statistical significance · any named distribution, including "normal" and "power law" · correlation, regression, effect size · formal probability, expected value, sampling error, statistical power · every hypothesis-testing concept.

| ID | C | Rule |
|---|---|---|
| 5.7.1 | M | a ladder-required concept, or "significant" in its statistical sense, ! appear before §2.3 admission; admitting "significant" includes its underlying test |
| 5.7.2 | M | every headline statistical result includes a statement using **only bare concepts**; a ladder-required formulation may accompany it but ! replace it |

## §5.8 Reproducibility statement

The statement identifies what another person needs to repeat the work: data or materials, code or procedure, compute or other resources, and key settings. It also identifies any unavailable input or component.

| ID | C | Rule |
|---|---|---|
| 5.8.1 | M | the paper includes its reproducibility statement, containing every element listed above |
| 5.8.2 | M | the statement uses only assumed or previously admitted terms, and ! delegate required statement content entirely to a technical appendix or external artifact |

## Applicable core rules with profile scope

§4.2.4 and §4.4.3 both apply. **§7.3 is mandatory for this profile.** §7.4 (bounded generalization) does the most work in `Discussion`: name the extrapolation target and drop to interpretive, proposed, or speculative strength beyond established evidence.

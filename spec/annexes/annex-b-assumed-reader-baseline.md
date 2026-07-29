# Annex B — Assumed-reader baseline (normative)

**Status:** v0.8.0-draft. Members across software engineering pod roles have not yet validated this annex.

Until that review, treat borderline items as not assumed (§0.3.3).

This annex enumerates the baseline behind §0.3. The annex is normative.

The policy in §0.8 classifies baseline changes separately from prose changes. Removing an item from §B.1 or §B.2 is a major change.

Adding an item is a minor change.

The baseline represents knowledge shared across a cross-functional software engineering pod.

It does not use a software engineer's education, coding fluency, or professional depth as its floor.

A base reader gains familiarity through regular work near software design, delivery, testing, operation, or management.

Role-specific expertise remains unavailable unless §B.1 lists it.

The shared core uses one base reader for every profile. A profile overlay may add familiar document conventions.

For example, a reader may know that a decision record has a decision section. A reader of `research-paper` documents may expect a results section.

An overlay does not add subject-matter knowledge.

Domain jargon, organization-local shorthand, and specialized notation still require admission through §2.3.

This annex has four main content sections.

§B.1 lists what the base reader knows. §B.2 lists notation that needs no explanation.

§B.3 lists explicit exclusions. §B.4 lists the limited genre conventions that each profile adds.

§B.3 is not the complement of §B.1. Its explicit exclusion list resolves recurring disputes under §0.3.3.

## B.1 Assumed concepts

The writer may use these without definition.

Ordinary English:

- Contemporary general-purpose English in its ordinary, nontechnical senses

The baseline does not admit a specialized sense merely because the term uses a familiar word.

For example, *lease*, *control*, *model*, and *significance* still require admission as domain terms.

Basic software concepts:

- Software, source code, configuration, applications, systems, components, and processes understood as running programs
- Frontends and backends at the level of user-facing and server-side software
- Inputs, outputs, state, errors, failures, and dependencies
- Functions as named software units that accept inputs and produce outputs or effects
- Parameters as named inputs to functions or APIs, and arguments as supplied values
- Interfaces and application programming interfaces (APIs) as defined boundaries between software units
- Clients and servers, requests and responses, and HTTP as a common request protocol
- Files and databases, including tables, rows, and queries at a conceptual level
- Latency as delay, throughput as work per unit of time, capacity, and availability

Software delivery and quality:

- Requirements, acceptance criteria, features, bugs or defects, and regressions
- Manual and automated tests, including unit, integration, end-to-end, and regression tests at a purpose level
- Reproduction steps and debugging at the level of finding the cause of a failure
- Logs, metrics, monitoring, and alerts
- Development, test, staging, and production environments
- Builds, deployments, releases, versions, and rollbacks
- Version control, commits, branches, diffs, pull requests, and code review at a purpose level
- Continuous integration at the level of automated checks on a proposed change

Basic quantitative reasoning:

- Arithmetic with whole numbers, decimals, negative numbers, and fractions
- Counts, minimums, maximums, and ranges
- Percentages, ratios, and rates
- Mean or average and median
- Chance in its ordinary, informal sense
- Values presented in simple tables, line charts, and bar charts

## B.2 Assumed notation

The reader parses the following notation without a definition. This list is the §5.2 baseline notation set.

Writers must define every symbol not on this list in prose at first use.

Included:

- Arithmetic: `+ − × /` and parentheses.
- Equality and comparison: `=`, `≠`, `<`, `≤`, `>`, and `≥`.
- Percent `%` and plain ratios such as `3:1`.
- Plain numeric ranges such as `1–5`.

Every letter or symbol that names a quantity requires a prose definition at first use.

The following notation is not in the baseline. Writers define the notation at first use, even when the notation looks standard.

- Variables, named constants, function application, and subscripted indexing
- Approximation `≈`, powers, absolute value, scientific notation, and interval notation such as `[0, 1]`
- Summation `Σ`, product `Π`, logarithms, exponentials, factorial, and Big-O notation
- Set notation, including membership, subsets, unions, intersections, and set-builder notation
- Binomial coefficients `C(n, k)` / `(n choose k)`
- Vector/matrix notation: bold symbols, `Ax`, transpose, norms `‖x‖`, and dot products.
- Calculus notation: `d/dx`, `∂`, `∫`, `∇`, and limits.
- Probability/statistics notation: `P(X | Y)` as formal notation, `E[·]`, `Var`, `σ`, and distribution names and symbols (`N(μ, σ²)`).
- `argmax` / `argmin`, `∝`, `∀` / `∃`, and Greek letters carrying conventional meanings (θ for parameters, α for rates).

## B.3 Explicitly not assumed

The writer shall not use these concepts without admitting them through the §2.3 ladder. Familiarity is not knowledge (§0.3.2).

Recognition does not establish operational knowledge.

Role and education:

The baseline does not assume a computer science education or a software engineering job title.

The baseline does not assume professional coding experience or the depth of a seasoned software engineer.

The reader need not parse or write source code, shell commands, SQL, configuration syntax, or regular expressions.

Programming implementation:

Admit programming-language syntax and implementation concepts not listed in §B.1.

Examples include types, scope, control flow, iteration, recursion, exceptions, classes, objects, and closures.

Other examples include immutability, side effects, serialization, parsing, pseudorandom seeding, and string manipulation.

Admit data structures and algorithms beyond ordinary lists and tables.

Examples include maps, sets, stacks, queues, trees, graphs, hash tables, linked structures, sorting algorithms, and binary search.

Complexity analysis, Big-O notation, divide and conquer, dynamic programming, and intractability remain unassumed.

Systems and data infrastructure:

Admit threads, concurrency, race conditions, memory hierarchy, caching, compilation, and floating-point behavior.

Admit CPU/GPU execution models, file-system internals, timeouts, retries, load balancing, and scaling models.

Eventual consistency, database schemas, indexes, transactions, joins, key-value stores, and SQL behavior remain unassumed.

Domain and organization-specific concepts:

A profile does not grant subject expertise.

Admit specialized reliability, platform, security, governance, legal, financial, scientific, or product terms unless §B.1 lists the intended sense.

Examples include service-level indicator, service-level objective, error budget, blast radius, threat model, residual risk, control objective, policy exception, internal component names, and organization-local acronyms.

Annex A supplies canonical ladder entries for some terms. Those entries do not make the terms assumed.

Machine-learning concepts:

The following concepts remain unassumed:

- Model (in the machine-learning sense), training, loss, gradient, neural network, layer, weight, activation, embedding, token, attention, and transformer
- Parameter (in the stored-numeric-setting sense), pre-training, fine-tuning, prompt, context window, and inference (in the machine-learning sense)
- Overfitting, regularization, hyperparameter, checkpoint, sampling (in the generation sense), reinforcement learning, reward, agent (in the machine-learning sense), alignment, and hallucination
- Benchmark suites by name (MMLU, GSM8K, …) and dataset names as shorthand (ImageNet, C4, …)

Statistics beyond basic quantitative reasoning:

The following concepts remain unassumed:

- Mode, percentiles, named distributions, standard deviation, variance, standard error, hypothesis testing, p-values, and statistical significance
- Confidence intervals, effect sizes, correlation, regression, sampling error, statistical power, expected value, and formal probability

Technical reports and research papers admit these concepts under §5.7.

Other profiles admit them under §2.3.

Mathematics beyond basic quantitative reasoning:

The following concepts remain unassumed:

- Algebraic manipulation, mathematical functions, function graphs, linear equations, slopes, and polynomials
- Exponentials, logarithms, summation, products, factorials, combinatorics, formal set operations, and coordinate geometry

Linear algebra as manipulation:

The following concepts remain unassumed:

- Matrix multiplication as an operation with meaning
- Vectors as directions or points in high-dimensional space
- Dot products as similarity
- Eigenvalues and eigenvectors, matrix decompositions, and high-dimensional geometry

Calculus and optimization:

- Derivatives, partial derivatives, gradients (formal sense), integrals, limits, continuity as a formal property, convexity, optimization as a field, and convergence guarantees

Community and process shorthand:

A familiar section pattern does not admit its community's jargon.

Examples that remain unassumed include venue prestige as evidence, "SOTA," "camera-ready," "rebuttal," "SEV-1," "five whys," "two-person rule," and unexplained status labels or approval gates.

## B.4 Profile overlays: conventions only

Each overlay adds only navigation or document conventions. Each overlay states its own conventions in the `reader.md` file of its overlay directory. Section 1.5 defines that layout.

The following table is the complete profile registry for ITWS 0.8.0-draft. Each row is normative through the file it names.

| Overlay | Profile | File |
|---|---|---|
| §B.4.1 | `design-rfc` | [../overlays/design-rfc/reader.md](../overlays/design-rfc/reader.md) |
| §B.4.2 | `decision-record` | [../overlays/decision-record/reader.md](../overlays/decision-record/reader.md) |
| §B.4.3 | `procedure` | [../overlays/procedure/reader.md](../overlays/procedure/reader.md) |
| §B.4.4 | `explanation` | [../overlays/explanation/reader.md](../overlays/explanation/reader.md) |
| §B.4.5 | `incident` | [../overlays/incident/reader.md](../overlays/incident/reader.md) |
| §B.4.6 | `technical-report` | [../overlays/technical-report/reader.md](../overlays/technical-report/reader.md) |
| §B.4.7 | `research-paper` | [../overlays/research-paper/reader.md](../overlays/research-paper/reader.md) |
| §B.4.8 | `investigation-log` | [../overlays/investigation-log/reader.md](../overlays/investigation-log/reader.md) |
| §B.4.9 | `epic` | [../overlays/epic/reader.md](../overlays/epic/reader.md) |
| §B.4.10 | `task` | [../overlays/task/reader.md](../overlays/task/reader.md) |
| §B.4.11 | `subtask` | [../overlays/subtask/reader.md](../overlays/subtask/reader.md) |
| §B.4.12 | `maintenance-comment` | [../overlays/maintenance-comment/reader.md](../overlays/maintenance-comment/reader.md) |

These conventions let the writer use the corresponding section functions without teaching the genre. The conventions do not permit unexplained domain terms within those sections.

The `maintenance-comment` overlay additionally carries the §0.3.4 host-language reader supplement. The supplement is conditional on the declared host adapter. It grants reading literacy in the host language's surface syntax and the use of identifiers visible in the anchored code. It grants no project history, product vocabulary, library behavior, or author intent.

The `research-paper` overlay expressly assumes no machine-learning knowledge. Its file states that boundary and what remains ladder-required.

A profile-specific audience declaration may narrow the actual audience. The declaration does not change ITWS conformance unless Annex B changes.

## B.5 Change process

Disputes resolve under §0.3.3: an item not listed is not assumed.

Additions and removals follow §0.8. Annex G records each addition and removal.

Removing an item from §B.1 or §B.2 is breaking.

Adding an item is a minor change.

Each change names its evidence. Typical evidence is a failed or contested §8.3 reader test or a recurring §8.4 proxy finding.

A profile overlay change must state whether it adds only a convention. Subject-matter knowledge belongs in §B.1, not in an overlay.

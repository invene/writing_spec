# Annex B — Assumed-reader baseline (normative)

**Status:** v0.2.1-draft. Working software engineers who match the §0.3 base reader have not yet validated this annex.

Until that review, treat borderline items as not assumed (§0.3.3).

This annex enumerates the baseline behind §0.3. The annex is normative.

The policy in §0.8 classifies baseline changes separately from prose changes. Removing an item from §B.1 or §B.2 is a major change.

Adding an item is a minor change.

The baseline begins with the core of the Association for Computing Machinery's computer science curriculum.

The baseline keeps knowledge that working software engineers retain. The baseline also adds professional-practice knowledge that the curriculum does not cover.

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

Programming:

- Variables, types, functions, parameters and arguments, return values, scope, control flow, iteration, recursion, exceptions, and interfaces
- Classes and objects, immutability, side effects, pure functions, closures, serialization, parsing, regular expressions, and string manipulation
- Randomness and seeding pseudorandom generators

Data structures:

- Arrays, lists, maps/dictionaries, sets, stacks, and queues
- Trees, graphs, hash tables and hashing, and linked structures
- Matrices as two-dimensional arrays of numbers

The baseline assumes only matrix storage and indexing. §B.3 excludes the algebraic sense.

Algorithms and complexity:

- Searching and sorting, big-O notation and growth rates, and time/space trade-offs
- Greedy versus exhaustive search, binary search, and divide and conquer
- Dynamic programming at the level of "cache subproblem results" and graph traversal
- The idea that some problems are intractable at scale

Systems:

- Processes, threads, concurrency, and race conditions
- Memory hierarchy and caching
- CPUs versus GPUs at the level of "GPUs run many simple operations in parallel"
- Compilation and interpretation
- Floating-point numbers and their finite precision
- File systems and operating-system basics

Networking and distributed systems:

- Client/server, HTTP, and APIs
- Latency versus throughput and bandwidth
- Timeouts, retries, and load balancing
- Horizontal versus vertical scaling
- Eventual consistency at the level of "replicas can briefly disagree"

Databases:

- Tables, rows, schemas, queries, indexes, transactions, joins at the working SQL level, and key-value stores

Software practice:

- Version control (commits, branches, and diffs), code review, and testing (unit, integration, and regression)
- Continuous integration, benchmarks and profiling, logging and monitoring, and debugging
- Configuration and environment variables, dependency management, releases and versioning, and technical debt
- A/B testing at the level of "compare two variants on live traffic"

Mathematics (first-year-undergraduate working level):

- Algebraic manipulation
- Functions and their graphs, linear equations and slopes, and polynomials
- Exponentials and logarithms, including log scales and "logarithmic growth"
- Percentages, ratios, and rates
- Averages (mean, median, and mode) and a distribution's spread at the level of "min/max/percentiles"
- Basic probability, including independent events, coin flips and dice, and informal conditional probability ("the chance of X given Y")
- Expected value at the level of "long-run average"
- Basic set operations
- Factorial and simple counting arguments
- Basic two-dimensional geometry and coordinates

## B.2 Assumed notation

The reader parses the following notation without a definition. This list is the §5.2 baseline notation set.

Writers must define every symbol not on this list in prose at first use.

Included:

- Function application: `f(x)`, `g(x, y)`, and named functions used as values.
- Variables and named constants; subscripts as indices (`xᵢ`, "the i-th example").
- Arithmetic: `+ − × / ^`, parentheses, `=`, `≈`, and `≠`.
- Inequalities and ranges: `< ≤ > ≥`, intervals like `[0, 1]`.
- Absolute value `|x|`, percent `%`, and scientific notation (`3 × 10⁸`).
- Summation `Σ` over an indexed set, read as a loop; product `Π` by analogy, if introduced with a reading.
- Logarithms and exponentials: `log`, `ln`, `exp`, `2ⁿ`, and `10ᵏ`.
- Set notation: `{…}`, `∈`, `∉`, `⊆`, `∪`, `∩`, and `∅`; set-builder notation read aloud at first use.
- Factorial `n!`.
- Big-O: `O(n log n)`.

The following notation is not in the baseline. Writers define the notation at first use, even when the notation looks standard.

- Binomial coefficients `C(n, k)` / `(n choose k)`. The baseline assumes the counting idea (§B.1), but not the notation.
- Vector/matrix notation: bold symbols, `Ax`, transpose, norms `‖x‖`, and dot products.
- Calculus notation: `d/dx`, `∂`, `∫`, `∇`, and limits.
- Probability/statistics notation: `P(X | Y)` as formal notation, `E[·]`, `Var`, `σ`, and distribution names and symbols (`N(μ, σ²)`).
- `argmax` / `argmin`, `∝`, `∀` / `∃`, and Greek letters carrying conventional meanings (θ for parameters, α for rates).

## B.3 Explicitly not assumed

The writer shall not use these concepts without admitting them through the §2.3 ladder. Familiarity is not knowledge (§0.3.2).

Recognition does not establish operational knowledge.

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

Statistics beyond basic probability:

The following concepts remain unassumed:

- Named distributions (normal, binomial, …), standard deviation and variance as formal quantities, hypothesis testing, p-values, and statistical significance
- Confidence intervals, effect sizes, correlation coefficients, regression (statistical sense), sampling error, and statistical power

Admit every concept in this list under §5.7.

Linear algebra as manipulation:

The following concepts remain unassumed:

- Matrix multiplication as an operation with meaning
- Vectors as directions or points in high-dimensional space
- Dot products as similarity
- Eigenvalues and eigenvectors, matrix decompositions, and high-dimensional geometry

The baseline assumes matrices as two-dimensional storage (§B.1).

Calculus and optimization:

- Derivatives, partial derivatives, gradients (formal sense), integrals, limits, continuity as a formal property, convexity, optimization as a field, and convergence guarantees

Community and process shorthand:

A familiar section pattern does not admit its community's jargon.

Examples that remain unassumed include venue prestige as evidence, "SOTA," "camera-ready," "rebuttal," "SEV-1," "five whys," "two-person rule," and unexplained status labels or approval gates.

## B.4 Profile overlays: conventions only

The following list is the complete profile registry for ITWS 0.2.1-draft. Each overlay adds only the listed navigation or document convention.

- `design-rfc`. The reader recognizes a proposal organized around context, requirements, a proposed design, alternatives, risks, rollout, and unresolved questions.
- `decision-record`. The reader recognizes a compact record of status, context, decision, and consequences. The reader expects an explicit recorded decision.
- `procedure`. The reader recognizes prerequisites, ordered steps, verification, recovery, and escalation as instruction-document conventions.
- `explanation`. The reader recognizes a concept-to-mechanism explanation supported by examples and bounded by limits.
- `incident`. The reader recognizes impact and timeline as factual records. The reader treats causal analysis as a separate interpretation. The reader treats remediation and follow-up as separate jobs.
- `technical-report`. The reader recognizes a report that separates system or method, evidence, interpretation, limitations, and reproducibility or verification.
- `research-paper`. The reader recognizes navigation derived from introduction, methods, results, and discussion (IMRaD). The reader treats citations as source pointers and distinguishes results from discussion. This overlay expressly assumes no machine-learning knowledge. Every machine-learning term, method, benchmark, dataset, metric, convention, or symbol absent from §B.1 and §B.2 requires admission.
- `investigation-log`. The reader recognizes dated, append-only entries that separate objective, configuration or context, observations, interpretation, and next step.

These conventions let the writer use the corresponding section functions without teaching the genre. The conventions do not permit unexplained domain terms within those sections.

A profile-specific audience declaration may narrow the actual audience. The declaration does not change ITWS conformance unless Annex B changes.

## B.5 Change process

Disputes resolve under §0.3.3: an item not listed is not assumed.

Additions and removals follow §0.8. Annex G records each addition and removal.

Removing an item from §B.1 or §B.2 is breaking.

Adding an item is a minor change.

Each change names its evidence. Typical evidence is a failed or contested §8.3 reader test or a recurring §8.4 proxy finding.

A profile overlay change must state whether it adds only a convention. Subject-matter knowledge belongs in §B.1, not in an overlay.

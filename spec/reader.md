# ITWS assumed reader

**ITWS version:** 1.0.0 · **Status:** normative

Every vocabulary, notation, and explanation rule resolves against this file.

**assumed reader = base reader (below) + the genre overlay in the declared profile file.**

## The decision rule

**An item absent from §1 or §2 is not assumed.** It enters through the term ladder (core §2.3).

This settles every dispute. Familiarity is not operational knowledge: a term specialists recognize, or that frequent readers of this profile see weekly, still needs admission. Borderline item → treat as not assumed.

A profile overlay cannot settle a domain-term dispute by adding domain knowledge. The document admits the term.

## Who the base reader is

A working member of a **cross-functional software engineering pod** — software engineers, product designers, engineering managers, QA specialists, product managers, operations partners.

They collaborate regularly on software design, delivery, testing, operation, or management. They follow basic engineering discussion and artifacts. They know §1 through practical exposure and proximity.

They are **not** assumed to have a computer science education, to hold a software engineering title, to write or review code, to match a seasoned engineer's depth, or to know the document's product, system, operational environment, scientific field, or any other subject domain.

---

## 1. Assumed concepts

Usable without definition.

**Ordinary English** — contemporary general-purpose English in its ordinary, nontechnical senses.

A familiar word does not carry a specialized sense for free: *lease*, *control*, *model*, *significance* still require admission as domain terms.

**Basic software** — software, source code, configuration, applications, systems, components, processes as running programs · frontends and backends as user-facing and server-side software · inputs, outputs, state, errors, failures, dependencies · functions as named units taking inputs and producing outputs or effects · parameters as named function/API inputs, arguments as supplied values · interfaces and APIs as defined boundaries · clients and servers, requests and responses, HTTP as a common request protocol · files and databases, including tables, rows, queries conceptually · latency as delay, throughput as work per unit time, capacity, availability.

**Delivery and quality** — requirements, acceptance criteria, features, bugs/defects, regressions · manual and automated tests (unit, integration, end-to-end, regression) at a purpose level · reproduction steps and debugging as finding a failure's cause · logs, metrics, monitoring, alerts · development, test, staging, production environments · builds, deployments, releases, versions, rollbacks · version control, commits, branches, diffs, pull requests, code review at a purpose level · continuous integration as automated checks on a proposed change.

**Basic quantitative reasoning** — arithmetic with whole numbers, decimals, negatives, fractions · counts, minimums, maximums, ranges · percentages, ratios, rates · mean/average and median · chance in its ordinary informal sense · values in simple tables, line charts, bar charts.

## 2. Assumed notation

Parsed without definition. This is the core §5.2 baseline notation set.

- Arithmetic `+ − × /` and parentheses
- Equality and comparison `=` `≠` `<` `≤` `>` `≥`
- Percent `%` and plain ratios (`3:1`)
- Plain numeric ranges (`1–5`)

**Every letter or symbol naming a quantity needs a prose definition at first use.**

Not baseline — define at first use even when it looks standard: variables, named constants, function application, subscripted indexing · `≈`, powers, absolute value, scientific notation, interval notation `[0, 1]` · `Σ`, `Π`, logarithms, exponentials, factorial, Big-O · set notation (membership, subsets, unions, intersections, set-builder) · binomial coefficients `C(n, k)` · vector/matrix notation (bold symbols, `Ax`, transpose, norms `‖x‖`, dot products) · calculus (`d/dx`, `∂`, `∫`, `∇`, limits) · probability/statistics (`P(X | Y)`, `E[·]`, `Var`, `σ`, distribution names and symbols such as `N(μ, σ²)`) · `argmax` / `argmin`, `∝`, `∀` / `∃` · Greek letters carrying conventional meanings (θ for parameters, α for rates).

## 3. Explicitly not assumed

This list is not the complement of §1 — it resolves recurring disputes. Everything here requires ladder admission.

**Role and education** — no CS education, no software engineering title, no professional coding experience, no seasoned-engineer depth. The reader need not parse or write source code, shell commands, SQL, configuration syntax, or regular expressions.

**Programming and implementation** — language syntax; types, scope, control flow, iteration, recursion, exceptions, classes, objects, closures; immutability, side effects, serialization, parsing, pseudorandom seeding, string manipulation. Data structures and algorithms beyond ordinary lists and tables: maps, sets, stacks, queues, trees, graphs, hash tables, linked structures, sorting, binary search. Complexity analysis, Big-O, divide and conquer, dynamic programming, intractability.

**Systems and data infrastructure** — threads, concurrency, race conditions, memory hierarchy, caching, compilation, floating-point behavior; CPU/GPU execution models, file-system internals, timeouts, retries, load balancing, scaling models; eventual consistency, database schemas, indexes, transactions, joins, key-value stores, SQL behavior.

**Domain and organization-specific** — a profile grants no subject expertise. Specialized reliability, platform, security, governance, legal, financial, scientific, or product terms need admission: service-level indicator, service-level objective, error budget, blast radius, threat model, residual risk, control objective, policy exception, internal component names, organization-local acronyms. [glossary.md](glossary.md) supplies canonical wording for some of these; an entry does not make the term assumed.

**Machine learning** — model (ML sense), training, loss, gradient, neural network, layer, weight, activation, embedding, token, attention, transformer · parameter (stored-setting sense), pre-training, fine-tuning, prompt, context window, inference (ML sense) · overfitting, regularization, hyperparameter, checkpoint, sampling (generation sense), reinforcement learning, reward, agent (ML sense), alignment, hallucination · benchmark suites by name (MMLU, GSM8K, …) and dataset names as shorthand (ImageNet, C4, …).

**Statistics beyond basic quantitative reasoning** — mode, percentiles, named distributions, standard deviation, variance, standard error, hypothesis testing, p-values, statistical significance · confidence intervals, effect sizes, correlation, regression, sampling error, statistical power, expected value, formal probability. `technical-report` and `research-paper` admit these under §5.7; other profiles under §2.3.

**Mathematics beyond basic quantitative reasoning** — algebraic manipulation, mathematical functions, function graphs, linear equations, slopes, polynomials · exponentials, logarithms, summation, products, factorials, combinatorics, formal set operations, coordinate geometry.

**Linear algebra as manipulation** — matrix multiplication as a meaningful operation, vectors as directions or points in high-dimensional space, dot products as similarity, eigenvalues and eigenvectors, matrix decompositions, high-dimensional geometry.

**Calculus and optimization** — derivatives, partial derivatives, gradients (formal sense), integrals, limits, continuity as a formal property, convexity, optimization as a field, convergence guarantees.

**Community and process shorthand** — a familiar section pattern does not admit its community's jargon. Unassumed: venue prestige as evidence, "SOTA", "camera-ready", "rebuttal", "SEV-1", "five whys", "two-person rule", unexplained status labels and approval gates.

## 4. Profile overlays

Each profile file states its genre-knowledge overlay: the navigation conventions that profile's reader recognizes. An overlay lets the writer use those section functions without teaching the genre. **An overlay never admits a domain term inside those sections.**

`research-paper` expressly assumes **no machine-learning knowledge**.

`maintenance-comment` additionally carries a conditional host-language supplement — see its profile file.

A profile-specific audience declaration may narrow the actual audience. It does not change ITWS conformance.

## 5. Changing this file

Removing an item from §1 or §2 is a **major** change. Adding one is **minor** (core §9). Each change names its evidence: repeated reader confusion, recurring rewrite findings, or documented use the current baseline misclassifies. A profile overlay change states whether it adds only a convention — subject-matter knowledge belongs in §1, never in an overlay.

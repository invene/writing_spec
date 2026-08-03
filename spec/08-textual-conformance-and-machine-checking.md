# Part 8 — Textual conformance and machine checking

Parts 2–7 and the selected profile define conforming text. Part 8 defines the
binary textual-conformance model and the reference machine report. It assigns
no work to an author, reviewer, approver, or releaser.

Assurance practices such as independent review, reader testing, accepted
deviations, and release checks are outside ITWS conformance. The repository's
non-normative `assurance/` companion records optional practices. A rewriting
agent does not load that companion unless its request expressly asks for
assurance work.

## 8.1 Textual conformance

A governed unit is either conforming or nonconforming for one declared ITWS
version and profile.

A governed unit conforms when:

1. it declares an available ITWS version and one canonical profile;
2. every applicable mandatory language rule is satisfied; and
3. every required profile slot is present.

A recommended-rule deviation does not make the text nonconforming. An accepted
deviation outside this specification does not change whether the text
conforms.

Textual conformance is a property of the text. Machine checking has bounded
coverage and therefore does not, by itself, certify every semantic rule.

## 8.2 Machine checking

`itws-lint` checks the decidable portion of the profile envelope. It uses only
the Python standard library and needs no network access for its default run.
Optional network resolution changes reported coverage, not the applicable
language rules.

### 8.2.1 Phrase-list input

A phrase-list paragraph is a machine-readable list and the linter's only
word- and phrase-level input. The paragraph sits beside the language rule it
supports and has this form:

```text
**Phrase list <rule ID> — <label> (<kind>[, case-sensitive]):** "<item>" (<note>); "<item>"; …
```

The kind is `word`, `phrase`, `opener`, or `pattern`. A `word` item matches on
word boundaries. A `phrase` item matches a literal span. An `opener` item
matches only at the start of a sentence. A `pattern` item is a regular
expression. A parenthesized note states an exclusion that a reader or agent
applies; the machine finding repeats the note.

#### Rule 8.2.1 — Error violations fail the machine check
**Class:** mandatory · **Machine-checkable:** yes · **Source:** STE checker practice
**Constructs:** tool-artifact
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: mechanical
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** requires 8.2.2; pairs-with 8.6.6

> A machine check **shall** report `fail` when at least one error-severity violation remains and **shall** otherwise report `pass`.

**Rationale:** Binary machine results make decidable failures usable in editors
and continuous integration. Candidates and rules outside machine coverage
remain visible through Rule 8.2.5 without being mislabeled as failures.

**Compliant:** Rule 3.10.6 produces an error violation, so the machine result is
`fail`.
**Non-compliant:** The run reports `pass` while an error violation remains.

**Cross-references:** Rules 8.2.2, 8.2.5, 8.6.6

**Severity map:**

- Mandatory rule: error.
- Recommended rule: warning.
- Permitted-practice hint: suggestion.

#### Rule 8.2.2 — Severity maps to rule class
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** tool-artifact
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: mechanical
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** validates 8.2.1

> Each machine finding **shall** carry the severity assigned by the severity map.

**Rationale:** Rule classes lose their meaning when tooling flattens them. A
mandatory-rule violation must remain distinguishable from a recommendation or
hint.

**Compliant:** A mandatory prohibited-phrase rule reports an error.
**Non-compliant:** Every finding reports a warning regardless of rule class.

**Cross-references:** §0.4.2, Rule 8.2.1

**Version-pinned check inputs:**

- The governed unit's declared ITWS version.
- Its declared canonical profile.
- That version's rule applicability, baseline, glossary, and phrase lists.

#### Rule 8.2.3 — Version- and profile-pinned checking
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** declaration
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: mechanical
**Resources:** reads: declaration-block, conformance-record · writes: conformance-record
**Relations:** requires 4.3.1; pairs-with 8.6.2

> A machine check **shall** use every version-pinned check input.

**Rationale:** Checking against the latest lists or a guessed profile evaluates
a different language contract from the one the text declares.

**Compliant:** A `procedure` declaring ITWS 0.10.0-draft is checked with that
version's `procedure` envelope.
**Non-compliant:** A tool infers `research-paper` from citations and checks the
latest phrase lists.

**Cross-references:** §0.4.3, §0.4.4, Rule 4.3.1

#### Rule 8.2.5 — Machine reports disclose coverage
**Class:** mandatory · **Machine-checkable:** no · **Source:** original
**Constructs:** tool-artifact
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: mechanical
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** constrains 8.2.1; pairs-with 8.6.6

> A machine report **shall** list the applicable rules it checked fully, checked partially, and did not check.
>
> A machine `pass` **shall not** be described as certification of full textual conformance.

**Rationale:** Many language rules require semantic judgment. Coverage
disclosure keeps a useful machine result without turning an unperformed
judgment into a pass or a reason to refuse a rewrite.

**Compliant:** The report says `pass`, lists 87 fully checked rules, 24 partial
rules, and 31 untested rules, and labels the result `machine`.
**Non-compliant:** The report says "ITWS certified" after running phrase checks
alone.

**Cross-references:** §8.1, Rules 8.2.1, 8.6.6

## 8.3 Generated artifacts

The Markdown under `spec/` is authoritative. The generated navigation catalog
derives from that source and is an implementation aid, not assurance evidence.

**Generation-contract conditions:**

1. Record the ITWS version, artifact schema version, and generation command.
2. Record a content hash for each governed source and generated file except
   the inventory itself.
3. Produce byte-identical output from an unchanged source tree.
4. Preserve every normative order.
5. Contain every active rule exactly once.

#### Rule 8.6.1 — Generated artifacts satisfy the generation contract
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** tool-artifact
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: collection · rewrite: mechanical
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** pairs-with 8.6.2

> A published ITWS artifact set **shall** satisfy every generation-contract condition.

**Rationale:** Deterministic, source-pinned artifacts let an agent navigate the
language rules without trusting stale or reordered output.

**Compliant:** Regeneration from one source tree produces identical bytes and
matching source hashes.
**Non-compliant:** `rules.jsonl` names an older ITWS version and no command
reproduces it.

**Cross-references:** §0.4.4, Annex C

**Stale-artifact conditions:**

- A recorded source hash differs from the current source.
- A generated artifact records a different ITWS version.

#### Rule 8.6.2 — Stale artifacts are rejected
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** tool-artifact
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: collection · rewrite: mechanical
**Resources:** reads: conformance-record · writes: none
**Relations:** requires 8.6.1; pairs-with 8.2.3

> A tool **shall not** report a machine result computed from an artifact set that meets a stale-artifact condition.

**Rationale:** A stale catalog checks a different language contract. Rejecting
it prevents a plausible but invalid result.

**Compliant:** The validator reports the changed source hash and produces no
result.
**Non-compliant:** The validator prints a warning and reports `pass`.

**Cross-references:** Rule 8.2.3, Rule 8.6.1

**Machine-report fields:**

- result: `pass` or `fail`;
- checked rules;
- partially checked rules;
- untested rules;
- candidates and unresolved facts;
- structural problems; and
- readability metrics.

#### Rule 8.6.6 — Machine validation is binary and coverage-aware
**Class:** mandatory · **Machine-checkable:** yes · **Source:** original
**Constructs:** tool-artifact
**Navigation:** target: conformance-record · chunks: any · slots: any · layers: both · context: document · rewrite: mechanical
**Resources:** reads: conformance-record · writes: conformance-record
**Relations:** requires 8.2.1; requires 8.2.5

> A machine validation report **shall** contain every machine-report field and exactly one result, `pass` or `fail`.

**Rationale:** One binary machine result supports automation. Separate coverage
and candidate fields preserve what the machine did not decide without creating
an approval queue or a global rewrite blocker.

**Compliant:** A run reports `pass`, its checked/partial/untested rule IDs, two
candidates, and no structural problems.
**Non-compliant:** A run reports `needs_review`, or reports `pass` without its
coverage.

**Cross-references:** Rules 8.2.1, 8.2.5

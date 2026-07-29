# ITWS agent entry point

**ITWS version:** 0.8.0-draft

You are reading this because you were asked to rewrite a document so it conforms to the Invene Technical Writing Specification (ITWS). This file is the entry point. Read it once, then follow the sequence in §A.3.

The Markdown files under `spec/` are the specification. Everything else in this repository derives from them or helps you read them.

## A.1 What this repository gives you, and what it does not

The repository gives you four things:

1. **The specification itself**, in `spec/`. It is authoritative. When a generated file and the Markdown disagree, the Markdown wins and the disagreement is a defect.
2. **A committed navigation catalog**, in `spec/generated/agent/`. It holds one JSON record per rule, a typed rule graph, the glossary ladder, the reader baseline, the profile envelopes, the skeletons, and the linter's phrase lists. You can load it without running a build.
3. **Python helpers**, in `itws/`, with command-line entry points in `tools/`. They use only the Python standard library. Add the repository root to `sys.path` and import them, or run the scripts directly.
4. **Copyable examples**, in `examples/agent-scripts/`. Each one is short and states which part you are expected to replace with your own reasoning.

The repository does not give you a judgment about a governed document. No tool here decides a passage's §4.1 chunk type, its prose layer, whether a statement is exact or plain, what an evidence relationship is, or which rewrite is best. Section 1.6.1 reserves those decisions for a reader or an agent. You are that agent.

The division is deliberate. Deterministic code preserves structure and checks mechanical conditions. You make semantic judgments and cite the rules behind them.

## A.2 Before you start

Confirm three things.

**Python.** Run `python3 --version`. Any Python 3.11 or later works. No package installation is needed, and no network access is needed.

**The catalog is current.** Run `python3 tools/itws_compile.py --check`. A clean result means the committed catalog matches the Markdown. A stale result means you should regenerate before trusting a lookup.

**The profile.** Every governed document declares exactly one profile from the twelve in §0.2. If the document already declares one, use it. If it does not, choose from the registry in `spec/overlays/README.md` and say which one you chose and why. If two profiles fit the request equally, ask the person who gave you the document; a wrong profile produces a document with the wrong acceptance conditions.

## A.3 The sequence

### Step 1 — Load the profile envelope

```text
python3 tools/itws_retrieve.py get-profile <profile> --json
```

The envelope is every active rule the profile admits. It is the widest correct rule set for the document. Every later step narrows what you are *looking at*; nothing narrows what *applies*.

### Step 2 — Index the document's structure

```text
python3 tools/itws_document.py index --input <document>.md --out structure.json
python3 tools/itws_document.py scan-path --input <document>.md --json
```

The manifest reports headings, paragraphs, lists, tables, code fences, quotations, links, and source spans. It links a heading to a skeleton slot only when the heading matches a canonical name, a permitted rename, or an authored section map (§E.0.2). Every other heading is yours to classify.

The scan-path command extracts the Rule 4.12.1 surface. It reports a missing opening chunk but never decides whether the path preserves the profile's shallow model. Compare the extracted path with the profile's `scan_test_outcome` and the exact items you identify in Step 3. Record missing information or widening as a judgment. This comparison does not replace a required human scan test.

### Step 3 — Read the document and classify it yourself

Read the whole document. For each passage, decide its §4.1 chunk type, its layer, and the constructs it contains. Record each decision with the span it covers and the rule or section that supports it, as Rule 8.6.4 requires. `itws.analysis.AgentAnalysis` gives you a shape for that record; you may use your own instead.

Keep an uncertain reading as `proposed` or `unresolved`. Do not force a choice you cannot defend. If a rewrite would need a fact the document does not contain, record an open question and let validation report `blocked`.

### Step 4 — Navigate to the rules each passage triggers

```text
python3 tools/itws_retrieve.py search-rules "<what you see>" --profile <profile>
python3 tools/itws_retrieve.py expand-relations <rule id> --depth 2
python3 tools/itws_retrieve.py get-examples --rule <rule id>
python3 tools/itws_retrieve.py get-glossary-entry "<term>"
```

Search ranking is convenience, not applicability. Keep several readings alive, expand relations from the ones that look load-bearing, and return to earlier branches when a later rule changes your reading.

Read each rule's `rewrite` field before you plan a repair:

| Value | What you may do |
|---|---|
| `mechanical` | Apply the repair. The violation and its fix are both determinate. |
| `candidate` | Propose the repair and say why a reader should accept it. |
| `review` | Describe the problem and the options. Do not choose alone. |
| `prohibited` | Do not change the governed content on your own authority. Report it. |

### Step 5 — Plan the work

For a small document, work directly. For a document you will change in several places, build work slices with `itws.work`, declare which resources each slice writes, and check for cycles and collisions:

```text
python3 tools/itws_work.py validate --plan plan.json --document <document>.md
```

Two slices that write one resource collide. Rule 8.6.5 says the tool reports the collision and you resolve it.

### Step 6 — Rewrite

Preserve every exact item. Rule 5.1.1 forbids changing the scope, status, strength, conditions, or required behavior of an exact statement, and it is `prohibited` for a reason: a plain rewrite that widens a claim is the most common way this work goes wrong.

Never invent a threshold, a measurement, a source, or an acceptance condition. If one is missing, say it is missing.

### Step 7 — Guard the patch

```text
python3 tools/itws_patch.py check --base <document>.md --proposed <rewritten>.md
python3 tools/itws_patch.py combine --base <document>.md --proposed a.md b.md
```

`check` reports changed ranges, affected spans, stale hashes, and edits outside a declared slice. `combine` reports collisions among several proposals. Neither applies anything.

### Step 8 — Lint and validate

```text
python3 tools/itws_lint.py --input <rewritten>.md
python3 tools/itws_validate.py --input <rewritten>.md
```

Validation reports one of four states (§8.6.2):

- `pass` — every machine check passed, nothing required was skipped, and every human gate for the tier is recorded.
- `fail` — an unwaived error-severity finding remains.
- `needs_review` — the machine checks are clean and a reader still has work to do.
- `blocked` — a required input is missing.

A clean lint run is not conformance. Rule 8.2.4 says so, and the four states exist so a tool can say so too. Report the state you got, not the state you wanted.

## A.3.1 The comment-change-set sequence

The sequence above governs a Markdown document. A `maintenance-comment` unit is a hosted comment set (§0.2.1): the governed comments changed between a base and a proposed version of one host source file, declared by a JSON carrier. One tool covers the mechanical steps:

```text
python3 tools/itws_retrieve.py get-profile maintenance-comment --json
python3 tools/itws_comment.py index --carrier <set>.json
python3 tools/itws_comment.py scan-path --carrier <set>.json
python3 tools/itws_comment.py lint --carrier <set>.json
python3 tools/itws_comment.py stale --carrier <set>.json
python3 tools/itws_comment.py validate --carrier <set>.json
```

What changes, and what does not:

- **The carrier is the declaration surface.** It holds the §0.4.3 declarations, the change-set ID, the host adapter, the base and proposed hashes, and one record per governed comment (Annex E §E.12). The host file carries no ITWS boilerplate.
- **The governed set is explicit.** Changed `TODO` and `FIXME` markers are always governed. A natural-language comment is governed only when the carrier records it. Never mark a comment `ai-proposed` or `human-authored` from its style; provenance is declared or it is missing.
- **Your judgments are the same judgments.** Information delta (Rule 4.13.1), inferred intent (Rule 4.13.5), basis durability (Rule 4.13.4), and a code-comment conflict (Rule 4.13.6) are semantic readings. Record each with its comment ID and rule, exactly as Rule 8.6.4 requires. A conflict is reported, never silently reconciled.
- **Machine-proposed comments carry a gate.** If you drafted a comment, its record needs a §8.7 proposal record: prompt provenance, durable bases beyond the prompt, pinned hashes, and a human disposition. Validation stays short of `pass` until a person records `accepted` or `revised`, and a stale pinned hash voids the disposition (Rules 8.7.1–8.7.4).
- **The scan path changes shape.** It is the change-set ID, then each anchor and complete governed comment (Rule 4.13.9). Rules 4.12.2–4.12.4 still govern what it must preserve.

## A.4 Working from Python instead

Every command above is a thin wrapper. The library is often easier:

```python
import sys
sys.path.insert(0, "<repository root>")

from pathlib import Path
from itws.catalog import Catalog
from itws.document import parse_document
from itws.parser import parse_specification

catalog = Catalog.from_repo(Path.cwd())
spec = parse_specification(Path("spec"))

profile = catalog.get_profile("design-rfc")
matches = catalog.search_rules("interface invariant", profile="design-rfc")
neighbors = catalog.expand_relations(["5.1.1"], depth=2)

manifest = parse_document(Path("proposal.md"), skeleton=spec.skeleton("design-rfc"))
```

Write your own scripts freely. The supplied records are scaffolds, not a protocol: use all of them, some of them, or none.

## A.5 What you owe

- Cite a rule for every finding and every semantic judgment (Rules 8.4.4 and 8.6.4).
- Preserve every exact item, or stop and report why you cannot.
- Report a missing fact as missing. Do not generate one.
- Report the validation state you reached, including `needs_review` and `blocked`.
- Treat a scan-to-body comparison as agent analysis, not human scan-test evidence.
- Never edit `spec/` while rewriting somebody else's document. See `AGENTS.md` for the maintainer session that may.

## A.6 Pilot status

The 0.8.0-draft release verified the machine path end to end. `python3 tools/itws_check_all.py` parses the specification, regenerates every artifact, runs the unit tests, and validates twelve conforming profile fixtures to `pass` plus seven risk fixtures to their expected non-passing states.

The release did not verify the cold start: whether a fresh session that receives only a repository URL, a raw document, and one sentence of instruction reaches this sequence without further help. Four pilots remain open, and Annex G records them as pending:

| Pilot | Profile | What it tests |
|---|---|---|
| Compact cold start | `decision-record` | Can a fresh session find this file, run the scripts, write a small helper, classify passages, and produce a guarded rewrite unaided? |
| Structural stress | `design-rfc` | Can a coordinator identify requirements, exact and plain links, alternatives, risks, and rollout dependencies through navigation alone? |
| Mutation policy | `investigation-log` | Does the append-only policy stop a rewrite of a recorded entry? |
| Vocabulary and evidence | `research-paper` | Do the term ladder, symbols, equations, evidence, claim strength, limitations, and human review state all hold together? |

If you are running one of these, record what you had to guess. A guess you had to make is a defect in this file.

## A.7 Where to read next

| Question | File |
|---|---|
| What are the profiles, tiers, and layout? | `spec/README.md` |
| What does a rule look like, and what is navigation metadata? | `spec/01-foundations.md` (§1.3, §1.6) |
| What must my profile contain? | `spec/overlays/<profile>/skeleton.md` |
| What may I assume the reader knows? | `spec/annexes/annex-b-assumed-reader-baseline.md` |
| What does a conforming rewrite look like? | `spec/annexes/annex-d-examples-corpus.md` |
| What do the generated artifacts contain? | §8.6 and `spec/generated/agent/manifest.json` |
| How do I run everything at once? | `python3 tools/itws_check_all.py` |

# ITWS agent entry point

**ITWS version:** 0.10.0-draft

Use this sequence when asked to write, review, or rewrite a governed unit
against the Invene Technical Writing Specification (ITWS). The goal is the
best safe draft the available facts support.

The Markdown under `spec/` is authoritative. The non-normative `assurance/`
directory is not part of this sequence. Do not load it unless the request
explicitly asks for assurance, approval, reader testing, or release work.

## A.1 Division of work

The repository provides:

1. the language specification under `spec/`;
2. a generated navigation catalog under `spec/generated/agent/`;
3. standard-library Python helpers under `itws/` and `tools/`; and
4. copyable scripts under `examples/agent-scripts/`.

Tools decide syntax and other deterministic conditions. They do not decide a
passage's chunk type, prose layer, evidence relationship, information delta,
or best wording. Make those semantic judgments from the source and cite the
applicable rule.

Machine validation reports `pass` or `fail` for disclosed coverage. It lists
fully checked, partially checked, and untested rules. A machine `pass` is not
full semantic certification and is never an approval gate.

## A.2 Before the rewrite

Confirm the catalog is current:

```text
python3 tools/itws_compile.py --check
```

Resolve exactly one profile. Use the declared canonical profile when it fits
the requested job. If the declaration is missing, choose from
`spec/overlays/README.md`, state the choice, and add the declaration. Ask only
when the request leaves two materially different jobs equally plausible.

## A.3 Rewrite sequence

### Step 1 — Load the language envelope

```text
python3 tools/itws_retrieve.py get-profile <profile> --json
```

The envelope is every active language rule admitted by the profile. Its load
set contains no assurance path.

### Step 2 — Index the governed unit

For a Markdown document:

```text
python3 tools/itws_document.py index --input <document>.md --out structure.json
python3 tools/itws_document.py scan-path --input <document>.md --json
```

The structural manifest supplies source spans, headings, links, and exact
skeleton matches. The scan path is the title, headings, and opening sentences.
Compare it with the profile's `shallow_model_outcome`; record missing or widened
information as a semantic finding.

### Step 3 — Read and classify

Read the complete governed unit. Identify each passage's §4.1 purpose, exact or
plain layer, and triggered constructs. `itws.analysis.AgentAnalysis` is an
optional record shape; use it only when it helps.

Keep uncertainty explicit. A missing fact is not a reason to abandon the
rewrite:

1. preserve the affected exact span or use a clearly marked unresolved value
   that the source already permits;
2. rewrite every independent span that can be repaired safely;
3. do not invent a threshold, measurement, source, status, requirement, or
   acceptance condition; and
4. return a concise missing-fact list with the draft.

### Step 4 — Retrieve triggered rules

```text
python3 tools/itws_retrieve.py search-rules "<what you see>" --profile <profile>
python3 tools/itws_retrieve.py expand-relations <rule-id> --depth 2
python3 tools/itws_retrieve.py get-examples --rule <rule-id>
python3 tools/itws_retrieve.py get-glossary-entry "<term>"
```

Search order is navigation only. The full profile envelope remains applicable.

Interpret the `rewrite` field locally:

| Value | Repair behavior |
|---|---|
| `mechanical` | Apply the determinate repair. |
| `candidate` | Propose a source-supported repair and state the basis. |
| `review` | Make a conservative semantic choice or present alternatives. |
| `prohibited` | Preserve the protected exact content; repair around it and report the local limitation. |

No value requires external authority before a draft may be proposed. No value
blocks repairs to unrelated spans.

### Step 5 — Rewrite

Preserve every exact item's meaning, scope, strength, status, conditions, and
normative force. Split or restructure prose instead of weakening it. Follow the
profile skeleton, term ladder, scan-path rules, and profile-specific rules.

Produce the rewritten governed unit even when unresolved facts remain. Keep
known facts precise and attach the unresolved list separately.

### Step 6 — Guard the patch

```text
python3 tools/itws_patch.py check --base <document>.md --proposed <rewritten>.md
python3 tools/itws_patch.py combine --base <document>.md --proposed a.md b.md
```

`check` reports widened changes and stale spans. `combine` reports collisions.
Resolve a collision from the source facts; do not use it as a reason to discard
independent repairs.

### Step 7 — Lint and validate

```text
python3 tools/itws_lint.py --input <rewritten>.md
python3 tools/itws_validate.py --input <rewritten>.md
```

- `fail` means an error-severity machine violation or structural problem was
  found.
- `pass` means no such violation was found within the disclosed coverage.
- Candidates, skipped network checks, untested semantic rules, and unresolved
  source facts are reported separately. They do not become `needs_review` or
  `blocked` states.

Report the machine result and its coverage honestly.

## A.3.1 Hosted comment sets

A `maintenance-comment` unit is the selected comments changed between a base
and proposed host source, declared by a JSON carrier:

```text
python3 tools/itws_retrieve.py get-profile maintenance-comment --json
python3 tools/itws_comment.py index --carrier <set>.json
python3 tools/itws_comment.py scan-path --carrier <set>.json
python3 tools/itws_comment.py lint --carrier <set>.json
python3 tools/itws_comment.py stale --carrier <set>.json
python3 tools/itws_comment.py validate --carrier <set>.json
```

The carrier declares the ITWS version, profile, change scope, host adapter,
base and proposed sources, boundaries, and one record per governed comment.
It has no tier, conformance-evidence, provenance, proposal, or disposition
field.

Apply the information-delta, anchor, purpose, basis, lifecycle, marker, and
unsupported-intent rules regardless of who proposed the comment. If code and
comment conflict, preserve both, report the local conflict, and continue with
other comments.

## A.4 Python API

The commands are thin wrappers:

```python
from pathlib import Path

from itws.catalog import Catalog
from itws.document import parse_document
from itws.parser import parse_specification

catalog = Catalog.from_repo(Path.cwd())
spec = parse_specification(Path("spec"))
profile = catalog.get_profile("design-rfc")
matches = catalog.search_rules("interface invariant", profile="design-rfc")
manifest = parse_document(
    Path("proposal.md"),
    skeleton=spec.skeleton("design-rfc"),
)
```

Write a small script when that is clearer than a command sequence. The
scaffolds are optional, not a workflow requirement.

## A.5 Deliverables

Return:

- the best safe rewritten unit;
- rule-cited findings and material semantic judgments;
- a list of unresolved facts or locally preserved conflicts;
- the machine `pass` or `fail` result; and
- the report's full/partial/untested coverage summary.

Never fabricate a missing fact. Never refuse the entire rewrite merely because
one span cannot be repaired safely.

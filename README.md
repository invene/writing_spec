# writing_spec

## For an AI agent

You were probably given this repository and a document to rewrite. Read [spec/agent/README.md](spec/agent/README.md) and follow the sequence there. That file is the entry point; nothing else is required reading first.

Everything runs from a clone with the Python standard library. There is nothing to install and no network call to make.

## Invene Technical Writing Specification (ITWS)

`spec/` contains **ITWS 0.8.0-draft**. ITWS is a controlled-language specification for technical writing.

The specification combines a shared core with twelve profiles. The profiles cover sustained technical documents, governed work items, and governed code-comment changes.

The work-item profiles are `epic`, `task`, and `subtask`. The `maintenance-comment` profile governs a comment change set inside a host source file through a JSON declaration carrier; the source code itself stays outside conformance (§0.2.1).

Each profile keeps its overlay in its own directory under [spec/overlays/](spec/overlays/). A reader, writer, or tool loads the shared core, the shared annexes, one profile directory, and the shared modules that directory lists. No other overlay is needed.

The base reader is any working member of a software engineering pod. Annex B defines the shared technical baseline, and each overlay defines its own reader conventions.

See [spec/README.md](spec/README.md) for the profile registry, conformance tiers, and contents.

## The application path for a writer

1. Choose a profile from the registry in [spec/README.md](spec/README.md) and a tier no lower than that profile's minimum.
2. Read Part 1 once. Load the profile's overlay directory and draft from its skeleton.
3. Generate your checklist and complete the four self-check passes:

   ```text
   python3 tools/itws_checklist.py \
     --spec-version 0.8.0-draft \
     --profile design-rfc \
     --tier reviewed \
     --out design-rfc-checklist.md
   ```

4. Run the linter and read every finding:

   ```text
   python3 tools/itws_lint.py --input your-document.md
   ```

5. Validate, and read the state it reports:

   ```text
   python3 tools/itws_validate.py --input your-document.md
   ```

A clean linter run is not conformance. Rule 8.2.4 says so, and the validator reports `needs_review` rather than `pass` until a reader has done their part.

For a comment change set, the same path runs through one tool: `python3 tools/itws_comment.py index | scan-path | lint | validate --carrier <set>.json`. The carrier declares the change set, one record per governed comment, and — for machine-proposed comments — the §8.7 proposal record and human disposition.

## The application path for a tool author

The Markdown under `spec/` is authoritative. Everything else derives from it.

| Layer | Where | What it does |
|---|---|---|
| Model | `itws/model.py`, `itws/parser.py` | one typed model of the whole specification |
| Compiler | `itws/compile.py` | writes the deterministic catalog under `spec/generated/agent/` |
| Catalog | `itws/catalog.py` | rule lookup, search, facets, relation traversal, context packets |
| Structure | `itws/document.py` | syntactic indexing of a governed document |
| Comments | `itws/comments/` | the hosted comment-set surface: carrier records, host adapters, extraction |
| Scaffolds | `itws/analysis.py`, `itws/work.py`, `itws/patch.py` | optional records for agent-authored analysis, plans, and patch guards |
| Checks | `itws/lint/`, `itws/validate.py` | the repository-local linter and four-state validation |

Regenerate and verify everything with one command:

```text
python3 tools/itws_check_all.py
```

The individual commands are listed in [spec/README.md](spec/README.md), so a failure can be isolated.

## A kickoff prompt you can copy

Give an agent the repository and this message:

```text
Clone or open <repository URL>. Read spec/agent/README.md and follow the
sequence it describes. Rewrite <document> so it conforms to ITWS.

The intended audience is <audience>, so the profile is probably <profile>.
If you disagree with that profile, say which one you chose and why.

Cite a rule for every change you propose. If a rewrite would need a fact the
document does not contain, stop and tell me what is missing instead of
supplying it. Report the validation state you reach, including
needs_review or blocked.
```

The same instruction is available as an installable skill in [skills/itws-rewrite/SKILL.md](skills/itws-rewrite/SKILL.md). Both are optional. The entry-point README alone is enough.

## Lineage

Annex G records the Research Writing Specification (RWS) 0.1 lineage. This repository does not contain a checkable 0.1 snapshot.

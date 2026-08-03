# writing_spec

## For an AI agent

If you were given this repository and a governed unit to rewrite, start at
[spec/agent/README.md](spec/agent/README.md). It tells you how to produce the
best safe draft, continue around missing facts, and report machine coverage.

Everything runs from a clone with the Python standard library. No installation
or network call is required.

## Invene Technical Writing Specification

`spec/` contains ITWS 0.10.0-draft, a controlled-language specification for
technical writing. It combines one shared core with twelve profiles. Eleven
profiles govern Markdown documents; `maintenance-comment` governs selected
comment changes through a JSON declaration carrier.

A governed unit declares only:

```text
ITWS version: 0.10.0-draft
Profile: <canonical profile ID>
```

Textual conformance is binary for that version and profile. There is no
conformance tier, reviewer, waiver, reader-test, release, evidence, or
machine-proposal-disposition requirement in the language specification.

Optional organizational review and release practices live in
[assurance/](assurance/README.md). Rewrite agents do not load that directory
unless a request explicitly asks for assurance work.

## Rewrite path

```text
python3 tools/itws_compile.py --check
python3 tools/itws_retrieve.py get-profile <profile>
python3 tools/itws_document.py index --input <document>.md --out structure.json
# read and classify; preserve exact facts; rewrite every safe span
python3 tools/itws_patch.py check --base <document>.md --proposed <rewrite>.md
python3 tools/itws_lint.py --input <rewrite>.md
python3 tools/itws_validate.py --input <rewrite>.md
```

Validation reports machine `pass` or `fail` plus fully checked, partially
checked, and untested rule IDs. Candidates and missing source facts remain
separate. A machine pass is not full semantic certification.

For hosted comment sets:

```text
python3 tools/itws_comment.py index     --carrier <set>.json
python3 tools/itws_comment.py scan-path --carrier <set>.json
python3 tools/itws_comment.py lint      --carrier <set>.json
python3 tools/itws_comment.py stale     --carrier <set>.json
python3 tools/itws_comment.py validate  --carrier <set>.json
```

Comment rules apply regardless of authorship. The carrier needs no provenance,
proposal, disposition, tier, or conformance-evidence field.

## Repository map

| Path | Contents |
|---|---|
| `spec/` | authoritative language specification |
| `spec/overlays/` | one directory per profile plus shared family modules |
| `spec/generated/agent/` | deterministic language-navigation catalog |
| `spec/agent/README.md` | rewrite-agent entry point |
| `itws/` | parser, model, catalog, linter, validator, and rewrite scaffolds |
| `itws/assurance/` | optional assurance helpers, isolated from default validation |
| `assurance/` | non-normative assurance companion |
| `tools/` | command-line entry points |
| `tests/` | unit tests and governed-unit fixtures |

Verify the repository:

```text
python3 tools/itws_check_all.py
```

This default check creates no `.itws-check` bundle and loads no assurance
record.

## Copyable kickoff prompt

```text
Open <repository>. Read spec/agent/README.md. Rewrite <document> against ITWS
using profile <profile>. Preserve exact facts and do not invent missing ones.
Continue around any unresolved span, return the best safe draft plus a concise
missing-fact list, and report machine pass/fail with its coverage summary.
```

The same flow is available as
[skills/itws-rewrite/SKILL.md](skills/itws-rewrite/SKILL.md).

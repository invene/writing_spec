# Agent instructions

This repository serves two kinds of session. Decide which one you are in before you change anything. Getting this wrong is the most expensive mistake available here.

## Which session am I in?

**You are a consumer session** if you were asked to write, review, or rewrite a document *against* ITWS. This is the common case.

- Do not modify anything under `spec/`, `itws/`, or `tools/`.
- Do not add a changelog entry, and do not increment the version.
- Read [spec/agent/README.md](spec/agent/README.md) and follow the sequence there.

**You are a maintainer session** if you were asked to change ITWS itself: a rule, an annex, a profile overlay, the tooling, or the tests.

- Every edit to this specification follows the rules in the specification.
- Every edit includes a changelog entry in [spec/annexes/annex-g-changelog.md](spec/annexes/annex-g-changelog.md).
- Every edit includes a version increment under §0.8.
- You may create tools to help modify the specification.

If the request is ambiguous, ask. A consumer session that edits `spec/` corrupts the specification for every other reader.

## Consumer session

Everything you need is in [spec/agent/README.md](spec/agent/README.md). In short:

```text
python3 tools/itws_compile.py --check
python3 tools/itws_retrieve.py get-profile <profile>
python3 tools/itws_document.py index --input <document>.md --out structure.json
# read, classify, and navigate; write your own scripts as needed
python3 tools/itws_patch.py check --base <document>.md --proposed <rewritten>.md
python3 tools/itws_validate.py --input <rewritten>.md
```

Two obligations carry across every step. Cite a rule for every finding and every semantic judgment. Report a missing fact as missing instead of generating one.

## Maintainer session

### Before you edit

Run the full check so you know the tree was clean when you started:

```text
python3 tools/itws_check_all.py
```

### While you edit

A new or changed rule needs the complete §1.3 template, including the four §1.6 navigation lines. `itws/annotations.py` holds the curated metadata, and `tools/itws_annotate.py` writes it into the Markdown:

```text
python3 tools/itws_annotate.py --spec-dir spec
```

A new permanent rule ID needs one approving pass before it enters the registry:

```text
python3 tools/itws_index.py --spec-dir spec --update-registry
```

A rule marked `Machine-checkable: yes` needs a registered checker in `itws/lint/`. The compiler fails without one. If no standard-library checker can decide the rule, change the metadata to `partial` and record the reason in the rule's rationale and in the changelog.

A phrase list lives in exactly one place: the phrase-list paragraph beside its rule (§8.2.1). Never copy a list into the linter.

### After you edit

Regenerate every artifact and rerun everything:

```text
python3 tools/itws_index.py --spec-dir spec
python3 tools/itws_compile.py --spec-dir spec
python3 tools/itws_check_all.py
```

### What a complete change contains

- The Markdown edit.
- Navigation metadata for any new or changed rule.
- A regenerated Annex C and a regenerated catalog under `spec/generated/agent/`.
- An Annex F row when the source framework or applicability changed.
- An Annex G entry naming every affected rule ID, profile, tier, and reader assumption.
- A version increment in `spec/00-front-matter.md` and in every current-version declaration.
- A passing `python3 tools/itws_check_all.py`.

## Repository map

| Path | Contents |
|---|---|
| `spec/` | the authoritative specification |
| `spec/overlays/` | one directory per profile, plus shared family modules |
| `spec/annexes/` | Annexes A–G |
| `spec/agent/README.md` | the consumer-session entry point |
| `spec/generated/agent/` | the committed navigation catalog (generated) |
| `itws/` | the parser, model, compiler, catalog, linter, and scaffolds |
| `tools/` | command-line entry points |
| `examples/agent-scripts/` | copyable scripts for a consumer session |
| `tests/` | the unit tests and the document fixtures |

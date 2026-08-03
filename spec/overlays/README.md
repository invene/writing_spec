# Profile overlays

**ITWS version:** 0.10.0-draft

This directory holds one subdirectory for each canonical profile in §0.2. A subdirectory holds only that profile's overlay material.

A writer, rewriting agent, or tool loads the shared core, the shared annexes, and exactly one profile directory. A profile directory loads a shared overlay module only when the registry below lists that module.

Section 1.5 defines this layout, the rule-placement policy, and the load set.

## Overlay registry

| Profile | Directory | Shared modules |
|---|---|---|
| `design-rfc` | [design-rfc/](design-rfc/) | none |
| `decision-record` | [decision-record/](decision-record/) | none |
| `procedure` | [procedure/](procedure/) | none |
| `explanation` | [explanation/](explanation/) | none |
| `incident` | [incident/](incident/) | none |
| `technical-report` | [technical-report/](technical-report/) | [shared/report.md](shared/report.md) |
| `research-paper` | [research-paper/](research-paper/) | [shared/report.md](shared/report.md) |
| `investigation-log` | [investigation-log/](investigation-log/) | none |
| `epic` | [epic/](epic/) | [shared/work-item.md](shared/work-item.md) |
| `task` | [task/](task/) | [shared/work-item.md](shared/work-item.md) |
| `subtask` | [subtask/](subtask/) | [shared/work-item.md](shared/work-item.md) |
| `maintenance-comment` | [maintenance-comment/](maintenance-comment/) | none |

Every profile above governs the `markdown-document` surface except `maintenance-comment`, which governs a `hosted-comment-set`: a comment change set declared by a JSON carrier beside its host source file (§0.2.1). Its skeleton binds carrier fields instead of headings (§E.0.4).

## Directory contents

Every profile directory holds these four files:

| File | Contents |
|---|---|
| `README.md` | job, shallow-model outcome, load set, and example pointers |
| `reader.md` | the genre-knowledge overlay cited as Annex B §B.4.*n* |
| `skeleton.md` | the required-section skeleton cited as Annex E §E.*n* |
| `rules.md` | every rule scoped to this profile alone |

A profile that adds no scoped rule keeps `rules.md` and records that the file lists none.

## Shared overlay modules

The [shared/](shared/) directory holds rules scoped to several profiles in one profile family. A rule appears in exactly one file. No overlay repeats a shared-core rule.

| Module | Family | Profiles |
|---|---|---|
| [shared/work-item.md](shared/work-item.md) | work item | `epic`, `task`, `subtask` |
| [shared/report.md](shared/report.md) | report | `technical-report`, `research-paper` |

## Validation

Check the layout, the registry, and rule placement:

```text
python3 tools/itws_overlays.py --spec-dir spec
python3 tools/itws_index.py --spec-dir spec --out spec/annexes/annex-c-rule-index.md
python3 tools/itws_compile.py --spec-dir spec
```

The rule index reads the core parts and this directory. It fails when a rule sits outside the location its `Profiles` metadata requires.

The compiler writes one profile manifest and one skeleton record for each directory above, under `spec/generated/agent/`. It fails when a profile manifest and the specification resolve different rule sets.

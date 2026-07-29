# Shared overlay modules

**ITWS version:** 0.8.0-draft

A shared overlay module holds rules that apply to several profiles in one profile family. Section 1.5 defines the placement policy that assigns a rule to this directory.

| Module | Family | Profiles | Loaded by |
|---|---|---|---|
| [work-item.md](work-item.md) | work item | `epic`, `task`, `subtask` | the three work-item overlays |
| [report.md](report.md) | report | `technical-report`, `research-paper` | the two report overlays |

A module rule keeps its `Profiles` metadata. A document evaluates a module rule only when the rule lists the document's declared profile.

A profile directory loads a module only when its README lists the module in the load set. No profile outside a module's family loads that module.

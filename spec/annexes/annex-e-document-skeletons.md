# Annex E — Document skeletons

**Status:** v0.6.0-draft.

This annex defines the shared slot policy and registers the required-section skeleton of every profile.

Every governed document has one profile ID. The registry contains exactly these IDs:

`design-rfc`, `decision-record`, `procedure`, `explanation`, `incident`, `technical-report`, `research-paper`, `investigation-log`, `epic`, `task`, `subtask`.

Human-readable labels may vary. Label variations do not create additional IDs.

Every document also has a title. Every document must include the exact §0.4.3 declaration fields:

`ITWS version: 0.6.0-draft`, `Profile: <canonical ID>`, and `Conformance tier: <permitted tier>`.

The title and declaration fields are required document elements, not profile sections.

All slots marked *(required)* must be present.

If a job has no content, state `None` or `Not applicable`. Give the reason. Do not omit the slot.

Optional bounded blocks and appendices may be added under the shared-core rules.

### E.0.1 Rename and merge policy

- Exact skeleton headings require no section map.
- A heading may use one of the renames listed in the profile's skeleton file.
- Any other rename requires a front-matter `Section map`. The map must connect the actual heading to the canonical job.
- Only the merges expressly listed in that file are permitted.
- A merged section must retain separately labeled subsections for each canonical job. The subsections must follow canonical order.
- A rename or merge changes only the presentation. Required content does not change. No required job may disappear.
- Sections without explicit merge permission shall remain separate.
- Observations or evidence may share a section with causal analysis or interpretation only when the profile expressly permits that merge.
- A permitted shared section must label the observation or evidence job separately from the analysis or interpretation job.

### E.0.2 Section map syntax

A `Section map` connects one actual heading to one canonical slot of the declared profile. The map is optional. A document needs it only for a rename that the profile's skeleton file does not list.

The map is a fenced block in the front-matter region, tagged `itws-section-map`. Each line maps one heading to one slot:

```text
```itws-section-map
"Why we are doing this" -> Context
"What must hold" -> Requirements
```
```

A heading containing a double quotation mark uses the unquoted form. Leading and trailing spaces are not significant. A blank line and a line beginning with `#` are ignored.

A parser **shall** reject a map that meets any of these conditions:

- A heading appears twice.
- A slot appears twice.
- A named slot is absent from the declared profile's skeleton.
- A named slot belongs to another profile.
- A mapped heading is absent from the document.

A section map changes presentation only. It does not remove a required job, reorder the skeleton, or grant a merge. Section E.0.1 continues to govern renames and merges.

### E.0.3 Mutation policy declarations

A skeleton file **may** declare a limit on rewriting content that already exists. The declaration has this form:

```text
**Mutation policy:** <scope> · <policy> · rule <rule ID> · <note>
```

The policy value is `append-only`, `replace-permitted`, or `owner-approval`. A tool reads the declaration and refuses a rewrite that the policy forbids. A skeleton without a declaration permits ordinary revision under the shared core.

## E.1–E.11 Profile skeleton registry

Each profile keeps its skeleton in the `skeleton.md` file of its overlay directory. Section 1.5 defines that layout. Each file states the profile's dependency order, required sections, permitted renames, and permitted merges.

The following table is the complete skeleton registry for ITWS 0.6.0-draft. Each row is normative through the file it names.

| Skeleton | Profile | File |
|---|---|---|
| §E.1 | `design-rfc` | [../overlays/design-rfc/skeleton.md](../overlays/design-rfc/skeleton.md) |
| §E.2 | `decision-record` | [../overlays/decision-record/skeleton.md](../overlays/decision-record/skeleton.md) |
| §E.3 | `procedure` | [../overlays/procedure/skeleton.md](../overlays/procedure/skeleton.md) |
| §E.4 | `explanation` | [../overlays/explanation/skeleton.md](../overlays/explanation/skeleton.md) |
| §E.5 | `incident` | [../overlays/incident/skeleton.md](../overlays/incident/skeleton.md) |
| §E.6 | `technical-report` | [../overlays/technical-report/skeleton.md](../overlays/technical-report/skeleton.md) |
| §E.7 | `research-paper` | [../overlays/research-paper/skeleton.md](../overlays/research-paper/skeleton.md) |
| §E.8 | `investigation-log` | [../overlays/investigation-log/skeleton.md](../overlays/investigation-log/skeleton.md) |
| §E.9 | `epic` | [../overlays/epic/skeleton.md](../overlays/epic/skeleton.md) |
| §E.10 | `task` | [../overlays/task/skeleton.md](../overlays/task/skeleton.md) |
| §E.11 | `subtask` | [../overlays/subtask/skeleton.md](../overlays/subtask/skeleton.md) |

A citation of the form "Annex E §E.9" resolves to the row above and to the file it names. The section numbers are stable across the reorganization in 0.6.0-draft.

The rename and merge policy in §E.0.1 governs every skeleton. A skeleton file adds only the renames and merges permitted for its profile.

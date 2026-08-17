# Profile: `change-request`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document` · **Family:** review-time

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Describe a proposed change so a reviewer can see what changed, what could break, and what to read first.

Host-neutral. A GitHub pull request, a GitLab merge request, and a Gerrit change are the same job.

A review comment on this change is [`feedback-comment`](feedback-comment.md). A durable code comment is `maintenance-comment`. A design proposal is `design-rfc`. This profile describes the change under review.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **what changed, what could break, and what to read first.**

## Reader overlay (genre knowledge only)

The reader recognizes a change description whose title names the change, then risk, review path, and verification. The host title and the body are one unit. Navigation only.

### Named-in-the-change supplement (conditional)

The host attaches this description to a proposed change. An identifier, path, or suite name in that change may be repeated as a name without admission.

The supplement grants **nothing else**. A domain term still enters through core §2.3.

## Skeleton

Dependency order: state what changed before the risk, review path, and verification that depend on it (core §4.4.2).

The host title is in scope. The host title is the document title under §4.15.1. A body heading is not required to carry it.

A one-line dependency bump and a large migration are both this profile. Fill every required slot.

| Slot | Required | Job |
|---|---|---|
| Summary | yes | what changed, in assumed-reader vocabulary |
| Risk | yes | what could break: failure modes, compatibility, and the bound of the change |
| Review path | yes | what to read first, named so a reviewer can open it |
| Verification | yes | the named suite that ran and the commit it ran against, or `None` with the reason no suite ran |

**Renames:** `Risk` → `What could break` · `Review path` → `What to read first` · `Verification` → `Checks`.

**Merges:** `Summary` + `Risk` → `Summary and risk` · `Review path` + `Verification` → `Review and verification`. Each merge keeps the canonical jobs as separately labeled subsections.

## Boundary locations (core §7.1)

- **Risk** — failure modes, compatibility, recovery, what the change could break.
- **Verification** — environment, version, dependency, and checks that did not run.

## Evidence-record additions (core §5.4)

The named suite, the commit, and the risk bound.

## §4.15 Scoped rules — change requests

The title and the description are one unit. The scan path starts at the title. An ungoverned host title breaks core §4.12.1 at that first element.

| ID | C | D | Rule |
|---|---|---|---|
| 4.15.1 | M | J | the host title is the document title for core §4.12.1 |
| 4.15.2 | M | J | a `change-request` title states the observable change |
| 4.15.3 | M | S | `Verification` names the suite that ran and the commit it ran against, or records `None` with the reason no suite ran |

§4.15.3 is this profile's checkability form. Core §5.8 does not apply. The `Verification` slot promises that a named suite passed at a named commit. The slot does not promise reproducibility of a method or verification of a system.

## Applicable core rules with profile scope

§4.2.4 applies. **§4.4.3 does not apply.** §7.3 is optional here.

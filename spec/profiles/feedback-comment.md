# Profile: `feedback-comment`

**ITWS version:** 1.0.0 · **Surface:** `markdown-document` · **Family:** review-time

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Address a person about a change with a request, observation, or question that expects a response.

A `feedback-comment` is a different job from a `maintenance-comment`. A `maintenance-comment` records a durable information delta about code for every future reader. A feedback comment is addressed to a person, about a change, and expects a response.

The change's description and title are [`change-request`](change-request.md). ! reuse `maintenance-comment` machinery: no comment hash, no host-anchor triple, no declaration carrier. The host already attaches the comment to the change.

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **what the comment asks the author to do or consider, about which part of the change.**

## Reader overlay (genre knowledge only)

The reader recognizes a comment addressed to a person about a change, expecting a response. Navigation only.

### Named-in-the-change supplement (conditional)

The host attaches this comment to a change. An identifier, path, or suite name in that change may be repeated as a name without admission.

The supplement grants **nothing else**. A domain term still enters through core §2.3.

## Skeleton

The shortest instance is one sentence. Size the unit to that instance.

The three core §0.5 declarations occupy the start of the body. Every line after them is governed prose. Without this placement, core's front-matter region swallows a heading-less body.

| Slot | Required | Job |
|---|---|---|
| Comment | yes | the request, observation, or question about the attached change |

The slot may be the whole body with no heading. Same pattern as `decision-record` `Status` as a front-matter field.

**Renames:** none. **Merges:** none.

## Boundary locations (core §7.1)

- The comment body — the part of the change the comment does not cover, when that bound is load-bearing.

A one-sentence comment whose whole point is the request carries no extra boundary sentence.

## Evidence-record additions (core §5.4)

The host's attachment of the comment to the change supplies context. The comment body is the exact item.

## §4.16 Scoped rules — feedback comments

| ID | C | D | Rule |
|---|---|---|---|
| 4.16.1 | M | L | scan path = the comment body in source order. Headings, when present, follow core §4.12.1's heading-plus-opening-sentence rule. No title element. **This replaces core §4.12.1.** §4.12.2–§4.12.4 still govern it unchanged |
| 4.16.2 | M | L | the three §0.5 declarations occupy the start of the body. Every line after them is governed prose |

## Applicable core rules with profile scope

**§4.2.4 does not apply** (no document-level slot ordering). **§4.4.3 does not apply.** §7.3 is optional here.

A core rule naming a document element — heading, section, figure, equation — is inapplicable when the construct is absent (core §0.2).

**§5.6 still governs strength.** A request and a question are not material claims — "Rename this to `batch_size`" · "Does this handle an empty page?" carry no strength; §5.6 does not reach them. Most comments here are one of those two. An observation is a material claim. Unmarked it takes verified-tier force. A reviewer who has read a diff has usually not verified, so the honest tier is `observed` (`we observed` · `we find`). A writer who states it flat because that is how the comment reads best **departs and reports it** (core §0.5). The flat form is a departure, not a violation to hide.

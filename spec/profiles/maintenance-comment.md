# Profile: `maintenance-comment`

**ITWS version:** 1.0.0 · **Surface:** `hosted-comment-set`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Preserve durable code knowledge by governing the comments one maintenance change adds, modifies, or removes.

**This profile governs a comment change set, not a Markdown document.** The host source file stays outside ITWS conformance. Governed comments carry no ITWS boilerplate. Declarations and slots live in a JSON **declaration carrier**, not in headings.

A core rule naming a document element — heading, section, figure, equation — is inapplicable here, because the construct is absent (core §0.2).

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **what knowledge each governed comment preserves, where it applies, its basis, and any removal trigger.**

## Hosted-comment vocabulary

Available without definition in this profile.

**comment change set** — the governed comments changed between one recorded base version and one recorded proposed version of a host source file, identified by one change-set ID and one declaration carrier. **declaration carrier** — the JSON record holding a change set's declarations and comment records. **host adapter** — the language-specific component that extracts comment units and host anchors and applies the exclusion policy for one host language. **host anchor** — the host file, line span, and enclosing named construct a governed comment attaches to. **information delta** — the knowledge a comment adds beyond what its anchored code states to a reader with the declared host-language supplement. **cognitive debt** — the future reader effort created when recorded knowledge is missing, stale, or misplaced. **removal condition** — the observable fact whose occurrence ends a temporary comment's or marker's life.

## Reader overlay (genre knowledge only)

The reader recognizes one comment change set with its change scope, repeated comment records, and boundaries.

### Host-language supplement (conditional)

When the declaration carrier names a host adapter, the assumed reader **additionally** has:

- reading literacy in that host language's surface syntax — comment markers, string and docstring delimiters, and the shape of a function, class, or block;
- the ability to treat an identifier appearing in the anchored code as a name the comment may repeat without admission.

The supplement grants **nothing else**. The reader is not assumed to know the project's history, prior versions, or removed behavior; the product's vocabulary or any domain term absent from [reader.md](../reader.md); the behavior of any library, framework, or service the code calls; or the author's intent.

Two limits keep the supplement inside core rather than beside it:

- A domain term inside a governed comment enters through the core §2.3 ladder. A cited basis records where the term's meaning is fixed and satisfies §4.13.4 — it does not admit the term (§2.4.5: a citation accompanies a definition, never replaces one).
- A granted identifier is a name repeated from the code the anchor names, and nothing more. §2.7.1 still governs an organization-coined name, including a codename or internal component name appearing in the anchored code.

This profile declares **no exception** to any core rule. It displaces nothing in §2.

## Comment purposes (closed)

| Purpose | Meaning |
|---|---|
| `rationale` | why the code takes this form |
| `invariant` | a property the anchored code must preserve |
| `caution` | a hazard, ordering constraint, or unsafe edit |
| `history` | a recorded past state that still constrains the present |
| `reference` | a pointer to a durable external contract or record |
| `marker` | a `TODO` or `FIXME` work marker |

## Skeleton — declaration carrier fields

Dependency order: seed scope, host identity, and anchors before the comment content, bases, and lifecycle facts depending on them (core §4.4.2).

Field names are **fixed**. No rename, no merge, no section map. An empty required field states `None` or `Not applicable` with a reason.

| Slot | Required | Job |
|---|---|---|
| Change scope | yes | change-set ID, host adapter, host file, base and proposed hashes, the change set's one-sentence purpose, and the three core §0.5 declarations including `AI disclosure` |
| Comment record | yes, per governed comment | one governed comment's complete record — fields below |
| → Change kind | yes | exactly one of `added`, `modified`, `removed`; selects the source the Anchor resolves against |
| → Anchor | yes | host file, line span, enclosing named construct: in the **proposed** source for `added`/`modified`, in the **base** source for `removed` |
| → Comment text | yes | the exact governed comment text, comment markers stripped; a removed comment records the text as it stood in the base source |
| → Purpose | yes | exactly one purpose from the closed list above |
| → Information delta | yes | the knowledge deleting the comment would lose, stated against the anchored code |
| → Basis | yes | the durable code, test, contract, work-item, or decision references supporting the comment, or `None` with a reason |
| → Lifecycle | yes | `durable`, or `temporary` with its observable removal condition |
| Boundaries | yes | the comments, files, and conditions the change set does not cover |

## Boundary locations (core §7.1)

- **Boundaries** — the comments, files, and conditions the change set does not cover, plus the environment, version, and dependency bounds within which each governed comment stays true.
- Each record's **Lifecycle** — the removal condition of a temporary comment (§4.13.7).
- Each record's **Basis** — the evidence limits of a comment whose basis is `None`.

## §4.13 Scoped rules — maintenance comments

| ID | C | Rule |
|---|---|---|
| 4.13.1 | M | a governed comment adds information its anchored code does not state to a reader with the declared host-language supplement |
| 4.13.2 | M | a governed comment record declares exactly one purpose from the closed list |
| 4.13.3 | M | a governed comment attaches to exactly one host anchor resolving to one construct span in the source its change kind names |
| 4.13.4 | M | a comment whose purpose is `rationale`, `invariant`, or `history` names a durable basis, or records `None` with the reason no durable basis exists |
| 4.13.5 | M | a governed comment ! present an intent, purpose, or requirement claim whose only support is the current implementation's behavior |
| 4.13.6 | M | a writer or agent finding a governed comment that contradicts its anchored code **records the conflict as a finding** and ! silently edit either side into agreement |
| 4.13.7 | M | a comment with lifecycle `temporary` records an observable removal condition |
| 4.13.8 | M | a `TODO` or `FIXME` marker the change set adds or modifies contains the marker keyword, one durable work-item or issue reference, and a removal condition |
| 4.13.9 | M | the scan path of a comment change set = the change-set ID, then in host order each host anchor and its complete governed comment. **This replaces the core §4.12.1 title-and-headings path.** §4.12.2–§4.12.4 still govern it unchanged. |

§4.13.5 and §4.13.6 are the two rules that most often bite: a comment may not infer intent from the code alone, and a code/comment disagreement is reported, never quietly reconciled.

## Applicable core rules with profile scope

**§4.2.4 does not apply** (no document-level slot ordering). **§4.4.3 does not apply.** §7.3 is optional here.

§4.9 (path-agnostic prose) still applies: a `history` comment records a past state that **still constrains the present**, framed as a prior — not as a warpath aside.

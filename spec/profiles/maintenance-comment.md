# Profile: `maintenance-comment`

**ITWS version:** 1.0.0 · **Surface:** `hosted-comment-set`

Load set: [legend](../legend.md) + [ontology](../ontology.md) + [core](../core.md) + [phrases](../phrases.md) + [glossary](../glossary.md) + [reader](../reader.md) + this file. Load no other profile.

## Job

Preserve durable code knowledge by governing comments. Two cases: those one maintenance change adds, modifies, or removes · those already present across a repository.

**This profile governs comments, not a Markdown document.** The host source file stays outside ITWS conformance. Governed comments carry no ITWS boilerplate. Declarations and slots live in a JSON **declaration carrier**, not in headings.

Two carrier shapes, and a carrier is one or the other:

- **change set** — the comments one maintenance change adds, modifies, or removes in one host file. Primary unit: the reviewer of a diff needs each comment decision beside it.
- **corpus at rest** — the comments already present across a **declaration boundary**, brought under the profile in a first conversion. One declaration covers the whole boundary.

A core rule naming a document element — heading, section, figure, equation — is inapplicable here, because the construct is absent (core §0.2).

## Shallow-model outcome (core §4.12.2)

The scan path lets the assumed reader state **what knowledge each governed comment preserves, where it applies, its basis, and any removal trigger.**

## Hosted-comment vocabulary

Available without definition in this profile.

**comment change set** — the governed comments changed between one recorded base version and one recorded proposed version of a host source file, identified by one change-set ID and one declaration carrier. **declaration carrier** — the JSON record holding one carrier's declarations and any comment records. **declaration boundary** — a named repository, package, or directory tree one carrier's declarations cover. **corpus at rest** — the governed comments already present across a declaration boundary, changed by no pending edit. **conversion** — the first pass bringing a corpus at rest under this profile, whose base is the boundary's pre-conversion state. **host adapter** — the language-specific component that extracts comment units and host anchors and applies the exclusion policy for one host language. **host anchor** — the host file, enclosing named construct, and comment hash a governed comment attaches to. **comment hash** — a hash of one governed comment's own text, comment markers stripped, that identifies the comment independently of its position in the host file. **information delta** — the knowledge a comment adds beyond what its anchored code states to a reader with the declared host-language supplement. **cognitive debt** — the future reader effort created when recorded knowledge is missing, stale, or misplaced. **removal condition** — the observable fact whose occurrence ends a temporary comment's or marker's life.

## Reader overlay (genre knowledge only)

The reader recognizes one carrier with its change scope, its repeated comment records where it has them, and its boundaries.

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
| Change scope | yes | the carrier shape — `change-set` or `corpus-at-rest` — the host adapter, the carrier's one-sentence purpose, and the three core §0.5 declarations including `AI disclosure`. A `change-set` adds its change-set ID, host file, and base and proposed hashes. A `corpus-at-rest` adds its declaration boundary and the boundary's pre-conversion state. |
| Comment record | `change-set`: yes, per governed comment · `corpus-at-rest`: optional (§4.13.16) | one governed comment's complete record — fields below |
| → Change kind | yes | exactly one of `added`, `modified`, `removed`, `converted`; selects the source the Anchor resolves against |
| → Anchor | yes | host file, enclosing named construct, and comment hash: in the **proposed** source for `added`, `modified`, and `converted`, in the **base** source for `removed` |
| → Line span | no | a cached position for navigation, marked derived (§4.13.11) |
| → Comment text | yes | the exact governed comment text, comment markers stripped; a removed comment records the text as it stood in the base source |
| → Purpose | yes | exactly one purpose from the closed list above |
| → Information delta | yes | the knowledge deleting the comment would lose, stated against the anchored code |
| → Basis | yes | the durable code, test, contract, work-item, or decision references supporting the comment, or `None` with a reason |
| → Lifecycle | yes | `durable`, or `temporary` with its observable removal condition |
| Boundaries | yes | the comments, files, and conditions the carrier does not cover |

## Boundary locations (core §7.1)

- **Boundaries** — the comments, files, and conditions the carrier does not cover, plus the environment, version, and dependency bounds within which each governed comment stays true.
- Each record's **Lifecycle** — the removal condition of a temporary comment (§4.13.7).
- Each record's **Basis** — the evidence limits of a comment whose basis is `None`.

## §4.13 Scoped rules — maintenance comments

| ID | C | D | Rule |
|---|---|---|---|
| 4.13.1 | M | J | a governed comment adds information its anchored code does not state to a reader with the declared host-language supplement |
| 4.13.2 | M | L | a governed comment record declares exactly one purpose from the closed list |
| 4.13.3 | M | L | a governed comment attaches to exactly one host anchor — host file, enclosing named construct, and comment hash — in the source its change kind names |
| 4.13.4 | M | S | a comment whose purpose is `rationale`, `invariant`, or `history` names a durable basis, or records `None` with the reason no durable basis exists |
| 4.13.5 | M | J | a governed comment ! present an intent, purpose, or requirement claim whose only support is the current implementation's behavior |
| 4.13.6 | M | J | a writer or agent finding a governed comment that contradicts its anchored code **records the conflict as a finding** and ! silently edit either side into agreement |
| 4.13.7 | M | S | a comment with lifecycle `temporary` records an observable removal condition |
| 4.13.8 | M | L | a `TODO` or `FIXME` marker the change set adds or modifies contains the marker keyword, one durable work-item or issue reference, and a removal condition |
| 4.13.9 | M | L | the scan path of a carrier = its change-set ID or declaration boundary, then in host order each host anchor and its complete governed comment. **This replaces the core §4.12.1 title-and-headings path.** §4.12.2–§4.12.4 still govern it unchanged. |
| 4.13.10 | M | L | an anchor **resolves** when exactly one comment in the named source matches its comment hash. Zero matches = the comment is gone or edited and the record needs a second reading. Two matches = the ambiguity §4.13.3 forbids. |
| 4.13.11 | P | L | a carrier may cache a `line span` for navigation, marked derived. It is derived data: nothing resolves an anchor through it, and a cached span whose text does not match the comment hash is a finding **against the carrier**, ! against the host file. |
| 4.13.12 | M | S | a `converted` record's base = the boundary's pre-conversion state. In a conversion `Change kind` is constant and carries no editorial signal; the base is a version boundary rather than a maintenance edit. |
| 4.13.13 | M | J | a `converted` record for a comment with no information delta states the empty delta and records it as a §4.13.6 finding. Conversion ! compel the comment's removal — the finding goes to the owner. |
| 4.13.14 | R | J | audit before converting: a read-only pass recording §4.13.1 gaps and §4.13.6 conflicts, editing nothing |
| 4.13.15 | P | J | one carrier's declarations may cover a **declaration boundary** — a repository, package, or directory tree — rather than one host file |
| 4.13.16 | M | L | a `change-set` carrier carries one `Comment record` per governed comment. A `corpus-at-rest` carrier may omit the records; conformance then rests on the comment text alone, which core §0.5 already makes the test. |

§4.13.5 and §4.13.6 are the two rules that most often bite: a comment may not infer intent from the code alone, and a code/comment disagreement is reported, never quietly reconciled.

**Why the anchor is content-addressed (§4.13.3, §4.13.10, §4.13.11).** A line span moves on three events: the carrier's own edits above it · a formatter reflow · a repair round. A drifted span still satisfies every check a span can satisfy, because fitting inside the file proves nothing. The hash ties the anchor to its own text, so a stale anchor announces itself instead of pointing a reader at unrelated code. `enclosing named construct` stays mandatory as the stable human pointer. One construct often carries several governed comments.

**Adopting the profile is not adopting a conversion (§4.13.14, §4.13.16).** A repository governing only its future changes conforms. Where a conversion is worth doing, the read-only audit delivers most of its value first.

## Applicable core rules with profile scope

**§4.2.4 does not apply** (no document-level slot ordering). **§4.4.3 does not apply.** §7.3 is optional here.

§4.9 (path-agnostic prose) still applies: a `history` comment records a past state that **still constrains the present**, framed as a prior — not as a warpath aside.

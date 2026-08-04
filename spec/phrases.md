# ITWS phrase lists

**ITWS version:** 1.0.0 · **Status:** normative

Literal strings for the [core.md](core.md) rules that prohibit or replace specific wording. **Match these exactly.** Do not paraphrase, expand, or "modernize" an entry — the string is the rule.

Matching is case-insensitive unless an entry says otherwise. A `pattern` list holds regular expressions; every other list holds literal words or phrases. `opener` means the item is prohibited only in sentence-initial position.

Every list is a closed set for its rule. A phrase resembling a listed item but absent from the list is judged under the rule's statement, not banned by this file.

---

## §2.1.3 — plain-verb replacements (word) · `R`

| Avoid | Use | Note |
|---|---|---|
| utilize | use | |
| perform | do | |
| demonstrate | show | only when the verb means "exhibit" |
| authored | wrote | |
| serves as | is | |
| boasts | has | |

## §2.3.3 — forward-reference promises (phrase) · `M`

"defined below" · "defined later" · "described below" · "as we will describe" · "as we will see" · "we define this later" · "more on this below" · "see below"

## §2.6.3 — unearned superlatives (word) · `M`

"state-of-the-art" · "novel" · "breakthrough" · "dramatic" · "significant" *(permitted in the statistical sense once admitted under §5.7)*

## §2.6.4 — prohibited words (word) · `M`

"delve" · "underscore" / "underscores" *(permitted for a physical mark; prohibited as rhetorical emphasis)* · "tapestry" · "testament" · "pivotal" · "crucial" · "robust" *(permitted in the statistical sense once admitted under §5.7)* · "showcase" · "intricate" · "fostering" · "garner" · "meticulous" · "vibrant" · "landscape" *(permitted for physical terrain; prohibited as an abstract field)* · "interplay" *(prohibited as an abstract relation)* · "boasts" · "align with" · "bolstered"

## §2.6.5 — agency verbs (word) · `M`

"wants" · "believes" · "knows" · "understands" · "thinks" · "decides" · "tries"

Prohibited for software, models, and automated systems **before** an operational definition of the verb.

## §2.6.6 — warpath markers (phrase) · `M`

"instead of the old approach" · "unlike what we did before" · "unlike our earlier" · "previously we" · "as before" · "our earlier attempt" · "the old approach" · "we used to"

## §2.6.7 — editorializing asides (phrase) · `M`

"it's important to note" · "it is important to note" · "it should be emphasized" · "it is worth noting" · "notably" · "interestingly" · "no discussion would be complete without"

## §2.6.8 — vague-authority phrases (phrase) · `M`

"experts say" · "studies show" · "research shows" · "widely regarded as" · "it is widely known" · "it is generally accepted" · "many believe"

## §2.6.9 — gap-speculation phrases (phrase) · `M`

"while specific details are limited" · "although not widely documented" · "not widely documented" · "while exact figures are unavailable" · "though details remain scarce"

## §2.6.10 — formulaic connectives (opener) · `M`

"moreover" · "furthermore" · "additionally" · "in addition"

Prohibited as **stacked padding**. A single connective marking a genuine §3.8 addition relation is permitted.

## §2.6.11 — conversational artifacts (phrase) · `M`

"I hope this helps" · "certainly!" · "let's explore" · "let's dive in" · "would you like" · "as an AI"

## §2.6.11 — unfilled placeholders (pattern) · `M`

`\[Your Name\]` · `\[Insert [^\]]*\]` · `INSERT_[A-Z_]+` · `\b\d{4}-XX-XX\b` · `\bTBD\b` · `<[A-Z_]{3,}>`

## §2.6.11 — tool-leakage patterns (pattern) · `M`

`oaicite` · `contentReference` · `turn\d+search\d*` · `\[cite: ?\d+\]` · `grok_card` · `grok_render_citation` · `\[span_\d+\]\(start_span\)` · `attached_file` · `【\d+†[^】]*】` · `utm_source=chatgpt\.com` · `utm_source=openai` · `utm_source=copilot\.com` · `referrer=grok\.com`

## §3.6.2 — bare openers (opener) · `M`

"this" · "that" · "these" · "those" · "it"

Prohibited as a bare sentence opener. Permitted when followed by the noun naming the referent ("This replica…").

## §3.9.1 — vague hedges (word) · `M`

"somewhat" · "fairly" · "relatively" · "quite" · "arguably" · "rather" · "largely" · "generally" *(prohibited for an assessment; permitted for a stated scope)* · "to some extent"

## §3.10.2 — contrast-reframe templates (pattern) · `M`

`\bis(?:n't| not)? just\b` · `\bnot only\b[^.]{0,60}\bbut also\b` · `\bnot merely\b` · `\bmore than just\b`

## §3.10.4 — trailing significance participles (phrase) · `M`

"highlighting the need for" · "underscoring the importance of" · "underlining the importance of" · "reflecting a broader trend" · "demonstrating the potential of" · "showcasing the" · "marking a significant"

## §3.10.6 — inflated copula substitutes (phrase) · `M`

| Avoid | Use |
|---|---|
| serves as | is |
| stands as | is |
| functions as | is |
| acts as | is |
| boasts | has |
| features | has |
| maintains | has |
| refers to | is *(prohibited only as a definition opener)* |

## §4.10.5 — emoji code points (pattern) · `M`

`[\U0001F300-\U0001FAFF]` · `[\U00002600-\U000027BF]` · `[\U0001F000-\U0001F0FF]` · `[\U0001F1E6-\U0001F1FF]` · `[\uFE0F]`

## §4.12.3 — scan-qualification candidates (pattern) · `M`

`\b(?:not|no|never|without)\b` *(candidate only — a canonical negative fact may be valid)* · `[,;]\s*(?:although|though|however|but)\b` · `\b(?:may|might|could)\b[^.!?]{0,80}\b(?:unverified|unknown|untested)\b`

These flag a scan-path sentence for review under §4.12.3, which requires affirmative content words wherever a bare negation or trailing hedge could leave a stronger reading. A match is not automatically a violation.

## §5.6.1 — unsupported modifiers (word) · `M`

"clearly" · "obviously" · "importantly" · "dramatic" · "we believe"

Any unsupported certainty or significance modifier is prohibited; these are the named instances. The **permitted** strength phrases are the closed table in core §5.6.

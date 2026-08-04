# tools — outside the specification

Nothing here is part of ITWS. No rule refers to it, it is outside the load set,
and deleting the directory changes no obligation. Read `spec/` for the rules and
`AGENTS.md` for how to work with them.

## Why this exists at all

ITWS 1.0.0 removed the 0.x tool suite because agents used the tools to *navigate*
the specification instead of loading it, then applied only the retrieved subset of
rules. That failure is what the roughly 22,000-token load set exists to prevent:
loading the whole specification has to stay affordable, so that nothing competes
with loading it.

A checker that points at the **corpus being edited** does not have that problem.
It never becomes a query surface for `spec/`, and it never answers "what does ITWS
require here?" — it answers "which strings in this document match a list the
specification already publishes."

So the constraint on anything added here is one sentence:

> A tool replaces **reading for** the literal rules. It never replaces loading them.

## `itws_literal.py`

Screens a corpus for the rules `spec/legend.md` marks `D = L` (a match, a count, or
a closed-set test settles it) and `D = S` (a match finds every candidate; a reader
decides each one).

```bash
python3 tools/itws_literal.py docs/**/*.md      # screen a corpus
python3 tools/itws_literal.py --json FILE       # machine-readable findings
python3 tools/itws_literal.py --self-test       # run the fixture
```

It carries no copy of any rule string. Every phrase list, profile ID, disclosure
value, and strength phrase is parsed out of `spec/phrases.md` and `spec/core.md`
at run time, so the tool cannot drift from the specification it screens. Adding a
phrase list to `spec/phrases.md` makes it screenable without touching the code.

**What a run does not tell you.** It decides no conformance question — ITWS §0.5
keeps that binary and textual, and §8 states what a checker may establish. Every
run ends with its own coverage statement naming what it did not evaluate, which is
every rule marked `D = J` and most of what a reader actually has to judge. A clean
run means the literal rules are clean. It means nothing else.

Exit status is 0 whenever the run completed. A finding is not an error, because
the exit code must never read as a verdict.

## `fixtures/phrase-list-fixture.md`

A deliberate violation corpus carrying at least one instance of every phrase list
the checker screens. `--self-test` fails when a list stops producing a finding,
which catches a phrase list added to `spec/phrases.md` without a matching fixture
line. The fixture carries no conformance claim.

# Annex B §B.4.12 — `maintenance-comment` reader overlay

**ITWS version:** 0.10.0-draft · **Status:** normative

This overlay adds one navigation convention and one host-language supplement to the §B.1 base reader.

The reader recognizes one comment change set with its change scope, repeated comment records, and boundaries.

The host-language supplement is conditional and narrow. When the declaration carrier names a host adapter, the assumed reader also has:

- Reading literacy in the declared host language's surface syntax: comment markers, string and docstring delimiters, and the shape of a function, class, or block.
- The ability to treat an identifier that appears in the anchored code as a name the comment may repeat without admission.

The supplement grants nothing else. The reader is not assumed to know:

- The project's history, prior versions, or removed behavior.
- The product's vocabulary or any domain term absent from Annex B.
- The behavior of any library, framework, or service the code calls.
- The author's intent, or any fact stated nowhere in the anchored code, the comment, or its cited basis.

Section B.4 states the convention-only boundary that governs this overlay. The supplement admits declared host syntax and visible identifiers, never subject-domain knowledge.

Two limits keep the supplement inside the shared core rather than beside it.

A domain term inside a governed comment enters through the §2.3 term ladder. A cited basis records where the term's meaning is fixed and satisfies Rule 4.13.4; it does not admit the term. Rule 2.4.5 states the reason: a citation moves the ladder into another document the assumed reader may not open, so a citation accompanies a definition and never replaces one.

An identifier the supplement grants is a name the comment repeats from the code its anchor names, and nothing more. Rule 2.7.1 continues to govern an organization-coined name, including a codename or an internal component name that appears in the anchored code. This overlay declares no §1.4 layer-2 exception, so it displaces no rule of Part 2.

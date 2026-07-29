---
name: itws-rewrite
description: Rewrite a document so it conforms to the Invene Technical Writing Specification (ITWS). Use when asked to make a design RFC, decision record, runbook, explanation, incident report, technical report, research paper, investigation log, epic, task, or subtask conform to ITWS, or when asked to review a document against ITWS rules.
---

# Rewrite a document to conform to ITWS

## What this skill does

It points you at one repository and one entry point. The repository holds the specification, a committed navigation catalog, and standard-library Python helpers. The entry point tells you the order to use them in. The public repository is located at: https://github.com/invene/writing_spec

## Steps

1. **Get the repository.** Clone or open the `writing_spec` repository. Everything runs from the checkout with the Python standard library; there is nothing to install.

2. **Read the entry point.** Open `spec/agent/README.md` and follow the sequence it describes. Do not skip it: it states the division between what the tools decide and what you decide, and getting that wrong produces confident, wrong rewrites.

3. **Confirm the catalog is current.**

   ```text
   python3 tools/itws_compile.py --check
   ```

4. **Pick the profile.** If the document declares one, use it. If not, choose from `spec/overlays/README.md`, and say which one you chose and why. Ask if two profiles fit equally.

5. **Work through the sequence in the entry point.** Load the profile envelope, index the document's structure, read and classify it yourself, navigate to the rules each passage triggers, rewrite, guard the patch, and validate.

## What you must not do

- Do not edit anything under `spec/`, `itws/`, or `tools/`. Those belong to a maintainer session; see `AGENTS.md`.
- Do not invent a threshold, a measurement, a source, or an acceptance condition. If one is missing, report it as missing.
- Do not weaken or widen an exact statement to make a sentence shorter. Rule 3.1.4 requires a split; Rule 5.1.1 forbids the change.
- Do not report `pass` when the validator reported `needs_review` or `blocked`.

## What you owe

- A rule citation for every finding and every semantic judgment.
- The validation state you actually reached.
- A named list of anything you could not resolve.

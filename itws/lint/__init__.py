"""The repository-local ITWS lint engine.

The engine uses only the Python standard library (§8.2). Its word- and
phrase-level inputs are generated from the specification's phrase-list
paragraphs; its structural checks read the model in :mod:`itws.parser` and
the structural manifest in :mod:`itws.document`.

A check reports what deterministic code can establish. A `partial` rule
produces a candidate, which is a navigation lead for a reader, never a
confirmed violation.
"""

from __future__ import annotations

from itws.lint.model import Finding, LintReport, LintContext
from itws.lint.engine import run_lint

__all__ = ["Finding", "LintReport", "LintContext", "run_lint"]

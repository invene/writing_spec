"""ITWS specification model, compiler, and agent-navigation scaffolds.

The Markdown files under ``spec/`` remain the authoritative specification.
Every module here derives from that source. Nothing in this package assigns a
semantic classification to a governed document's prose: an agent makes those
judgments and records them in the optional analysis records of
:mod:`itws.analysis`.

The package uses only the Python standard library. A checkout of the
repository is enough to import it::

    import sys
    sys.path.insert(0, "<repository root>")
    from itws.catalog import Catalog
"""

from __future__ import annotations

__all__ = ["SCHEMA_VERSION"]

#: Version of the generated-artifact schema under ``spec/generated/agent/``.
#: The schema version advances independently of the ITWS version.
SCHEMA_VERSION = "1.0.0"

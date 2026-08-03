"""The hosted comment-set surface of the `maintenance-comment` profile.

The package extracts comment units from a host source file, matches them
against a JSON declaration carrier, and reports mechanical facts: spans,
hashes, anchors, coverage, marker grammar, and staleness.

Nothing here decides what a comment means. Information delta, basis
sufficiency, inferred intent, and code-comment conflict are semantic
judgments that a reader or agent may record separately.
"""

from itws.comments.adapter import HostAdapter, PythonAdapter, get_adapter
from itws.comments.changeset import (
    CommentSetManifest,
    comment_scan_path,
    load_comment_set,
    structural_manifest,
)
from itws.comments.records import (
    CommentRecord,
    CommentSetDeclarations,
    HostAnchor,
)

__all__ = [
    "CommentRecord",
    "CommentSetDeclarations",
    "CommentSetManifest",
    "HostAdapter",
    "HostAnchor",
    "PythonAdapter",
    "comment_scan_path",
    "get_adapter",
    "load_comment_set",
    "structural_manifest",
]

#!/usr/bin/env python3
"""Rebuild the comment-fixture declaration carriers.

Run after editing a fixture host file, from the repository root:

    python3 tests/fixtures/comments/rebuild.py

Each carrier pins real content hashes, so an edit to a host file without a
rerun turns the fixture stale. Re-run this script whenever you change
``retry_base.py`` or ``retry_proposed.py`` in a fixture directory.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
REPO_ROOT = FIXTURES.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from itws.comments.adapter import PythonAdapter
from itws.model import SourceSpan, content_hash

ADAPTER = PythonAdapter()
ITWS_VERSION = "0.10.0-draft"

RATIONALE_TEXT = (
    "The 250 ms pause keeps retries under the gateway burst limit (DR-12)."
)
MARKER_TEXT = (
    "TODO(TASK-142): remove this shim when the v2 totals endpoint is live and\n"
    "test T-9 passes against it."
)


def find_span(source: str, first_line_text: str, line_count: int) -> dict[str, int]:
    for number, line in enumerate(source.splitlines(), start=1):
        if line.strip().lstrip("# ").startswith(first_line_text[:40]):
            return {"start_line": number, "end_line": number + line_count - 1}
    raise SystemExit(f"fixture text not found: {first_line_text[:40]!r}")


def anchor_for(source: str, path: str, span: dict[str, int]) -> dict[str, object]:
    resolved = ADAPTER.resolve_anchor(
        source, path, SourceSpan(path, span["start_line"], span["end_line"])
    )
    return resolved.to_json()


def declarations(directory: Path, change_set_id: str, scope: str) -> dict[str, object]:
    base = (directory / "retry_base.py").read_text(encoding="utf-8")
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    return {
        "itws_version": ITWS_VERSION,
        "profile": "maintenance-comment",
        "change_set_id": change_set_id,
        "host_adapter": "python",
        "base_path": "retry_base.py",
        "base_hash": content_hash(base),
        "proposed_path": "retry_proposed.py",
        "proposed_hash": content_hash(proposed),
        "change_scope": scope,
        "boundaries": (
            "The module docstring and the function docstrings stay outside "
            "this change set."
        ),
    }


def rationale_record(
    proposed: str, *, text: str = RATIONALE_TEXT, basis: list[str] | None = None
) -> dict[str, object]:
    span = find_span(proposed, text.split("\n")[0], text.count("\n") + 1)
    anchor = anchor_for(proposed, "retry_proposed.py", span)
    if basis is None:
        basis = ["decision record DR-12"]
    record: dict[str, object] = {
        "comment_id": "C-1",
        "change": "added",
        "anchor": anchor,
        "span": span,
        "text": text,
        "purpose": "rationale",
        "information_delta": (
            "The code shows the pause length; the burst limit that fixes it "
            "is recorded only here and in DR-12."
        ),
        "basis": basis,
        "lifecycle": "durable",
    }
    return record


def marker_record(proposed: str, *, text: str = MARKER_TEXT) -> dict[str, object]:
    span = find_span(proposed, text.split("\n")[0], text.count("\n") + 1)
    return {
        "comment_id": "C-2",
        "change": "added",
        "anchor": anchor_for(proposed, "retry_proposed.py", span),
        "span": span,
        "text": text,
        "purpose": "marker",
        "information_delta": (
            "The marker records the planned removal and its trigger; the "
            "code cannot state either."
        ),
        "basis": ["work item TASK-142"],
        "lifecycle": "temporary",
        "removal_condition": (
            "The v2 totals endpoint is live and test T-9 passes against it."
        ),
    }


def write_conforming_pair(directory: Path, change_set_id: str, scope: str) -> None:
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    write(
        directory,
        {
            **declarations(directory, change_set_id, scope),
            "comments": [
                rationale_record(proposed),
                marker_record(proposed),
            ],
        },
    )


def write(directory: Path, payload: dict[str, object]) -> None:
    payload.setdefault("judgments", [])
    payload.setdefault("open_questions", [])
    payload.setdefault(
        "conformance_evidence",
        {"lint_run_version": ITWS_VERSION, "self_check_recorded": True},
    )
    target = directory / "carrier.json"
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {target.relative_to(REPO_ROOT)}")


def main() -> None:
    directory = FIXTURES / "conforming"
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    write(
        directory,
        {
            **declarations(
                directory,
                "CS-2026-014",
                "Add the retry-pause rationale and complete the totals-shim "
                "marker in the gateway client.",
            ),
            "comments": [
                rationale_record(proposed),
                marker_record(proposed),
            ],
            "judgments": [
                {
                    "kind": "information_delta",
                    "value": "states the burst limit the code cannot show",
                    "span_ids": ["C-1"],
                    "support": ["4.13.1"],
                    "state": "accepted_for_run",
                }
            ],
        },
    )

    directory = FIXTURES / "conforming-removal"
    base = (directory / "retry_base.py").read_text(encoding="utf-8")
    removed = "TODO: clean this up."
    span = find_span(base, removed, 1)
    write(
        directory,
        {
            **declarations(
                directory,
                "CS-2026-019",
                "Remove the bare totals-shim marker now that TASK-142 is closed.",
            ),
            "comments": [
                {
                    "comment_id": "C-1",
                    "change": "removed",
                    "anchor": anchor_for(base, "retry_base.py", span),
                    "span": span,
                    "text": removed,
                    "purpose": "marker",
                    "information_delta": (
                        "None; the marker named no work item and no removal "
                        "condition, so its deletion loses no recorded knowledge."
                    ),
                    "basis": ["work item TASK-142"],
                    "lifecycle": "temporary",
                    "removal_condition": "TASK-142 is closed.",
                }
            ],
        },
    )

    directory = FIXTURES / "violations" / "bare-marker"
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    bare = "TODO: clean this up later."
    record = marker_record(proposed, text=bare)
    record["removal_condition"] = ""
    record["basis"] = []
    record["information_delta"] = "None; the marker names no work."
    write(
        directory,
        {
            **declarations(
                directory, "CS-2026-015", "Add a work marker to the totals shim."
            ),
            "comments": [record],
        },
    )

    directory = FIXTURES / "violations" / "unsupported-rationale"
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    text = "The 250 ms pause keeps the gateway happy under load."
    record = rationale_record(proposed, text=text, basis=[])
    record["basis_none_reason"] = "The generation prompt is the only source."
    record["information_delta"] = "Asserted intent with no recorded support."
    write(
        directory,
        {
            **declarations(
                directory, "CS-2026-016", "Add a machine-drafted retry rationale."
            ),
            "comments": [record],
        },
    )

    write_conforming_pair(
        FIXTURES / "violations" / "stale-proposal",
        "CS-2026-017",
        "Record the retry-pause rationale and totals-shim marker.",
    )

    write_conforming_pair(
        FIXTURES / "blocked" / "pending-disposition",
        "CS-2026-018",
        "Record the retry-pause rationale and totals-shim marker.",
    )


if __name__ == "__main__":
    main()

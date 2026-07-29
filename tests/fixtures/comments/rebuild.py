#!/usr/bin/env python3
"""Rebuild the comment-fixture declaration carriers.

Run after editing a fixture host file, from the repository root:

    python3 tests/fixtures/comments/rebuild.py

Each carrier pins real hashes, so an edit to a host file without a rerun
turns the fixture stale, exactly as Rule 8.7.4 intends. The stale-proposal
fixture deliberately keeps hashes from the conforming carrier's text with
one character changed; the loop below never rewrites its broken pins.
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
        "itws_version": "0.8.0-draft",
        "profile": "maintenance-comment",
        "conformance_tier": "core",
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
    proposed: str, *, provenance: str, disposition: str, bases: list[str],
    text: str = RATIONALE_TEXT,
) -> dict[str, object]:
    span = find_span(proposed, text.split("\n")[0], text.count("\n") + 1)
    anchor = anchor_for(proposed, "retry_proposed.py", span)
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
        "basis": ["decision record DR-12"],
        "lifecycle": "durable",
        "provenance": provenance,
    }
    if provenance == "ai-proposed":
        record["proposal"] = {
            "prompt_provenance": (
                "Prompt recorded in the change request: state why the retry "
                "pause is 250 ms."
            ),
            "bases": bases,
            "source_hash": content_hash(proposed),
            "anchor_hash": anchor["anchor_hash"],
            "comment_hash": content_hash(text),
            "disposition": disposition,
            "disposed_by": "R. Alvarez" if disposition != "pending" else "",
            "disposed_on": "2026-07-29" if disposition != "pending" else "",
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
        "provenance": "human-authored",
    }


def write(directory: Path, payload: dict[str, object]) -> None:
    payload.setdefault("judgments", [])
    payload.setdefault("open_questions", [])
    payload.setdefault(
        "conformance_evidence",
        {"lint_run_version": "0.8.0-draft", "self_check_recorded": True},
    )
    target = directory / "carrier.json"
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {target.relative_to(REPO_ROOT)}")


def main() -> None:
    # Conforming: one accepted machine proposal, one complete human marker.
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
                rationale_record(
                    proposed,
                    provenance="ai-proposed",
                    disposition="accepted",
                    bases=["decision record DR-12", "test T-7"],
                ),
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

    # Bare marker: the marker violates the Rule 4.13.8 grammar, and its
    # record declares temporary with no removal condition (Rule 4.13.7).
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

    # Unsupported machine rationale: the proposal cites only its prompt.
    directory = FIXTURES / "violations" / "unsupported-rationale"
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    text = "The 250 ms pause keeps the gateway happy under load."
    record = rationale_record(
        proposed,
        provenance="ai-proposed",
        disposition="accepted",
        bases=[],
        text=text,
    )
    record["basis"] = []
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

    # Stale proposal: the pinned hashes describe text this carrier does not
    # hold, so the recorded disposition no longer covers the comment.
    directory = FIXTURES / "violations" / "stale-proposal"
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    record = rationale_record(
        proposed,
        provenance="ai-proposed",
        disposition="accepted",
        bases=["decision record DR-12"],
    )
    record["proposal"]["comment_hash"] = content_hash(
        RATIONALE_TEXT.replace("250", "500")
    )
    record["proposal"]["anchor_hash"] = content_hash("an earlier function body")
    write(
        directory,
        {
            **declarations(
                directory, "CS-2026-017", "Re-approve the retry-pause rationale."
            ),
            "comments": [record, marker_record(proposed)],
        },
    )

    # Pending disposition: mechanically sound, but no person has disposed
    # of the machine proposal, so validation blocks (Rule 8.7.3).
    directory = FIXTURES / "blocked" / "pending-disposition"
    proposed = (directory / "retry_proposed.py").read_text(encoding="utf-8")
    write(
        directory,
        {
            **declarations(
                directory, "CS-2026-018", "Propose the retry-pause rationale."
            ),
            "comments": [
                rationale_record(
                    proposed,
                    provenance="ai-proposed",
                    disposition="pending",
                    bases=["decision record DR-12"],
                ),
                marker_record(proposed),
            ],
        },
    )


if __name__ == "__main__":
    main()

"""Byte-deterministic JSON serialization for generated artifacts.

Two runs over one unchanged source tree must produce identical bytes
(Rule 8.6.1). Every writer here fixes the separators, the indent, the escape
policy, and the trailing newline. No writer sorts object keys: the record
classes already emit their fields in a fixed, meaningful order.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from itws.model import content_hash


def dumps(payload: object) -> str:
    """Render one JSON document with the repository's fixed formatting."""
    return (
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            separators=(",", ": "),
            sort_keys=False,
        )
        + "\n"
    )


def dumps_lines(records: Iterable[object]) -> str:
    """Render JSON Lines: one compact record per line, order preserved."""
    return "".join(
        json.dumps(record, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
        + "\n"
        for record in records
    )


def write(path: Path, text: str) -> str:
    """Write ``text`` and return its content hash."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return content_hash(text)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[object]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

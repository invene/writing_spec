"""Shared fixtures and paths for the test suite."""

from __future__ import annotations

import functools
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SPEC_DIR = REPO_ROOT / "spec"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "documents"
CONFORMING = FIXTURES / "conforming"
VIOLATIONS = FIXTURES / "violations"
BLOCKED = FIXTURES / "blocked"
PATCHES = FIXTURES / "patches"
TOOLS = REPO_ROOT / "tools"

from itws.catalog import Catalog  # noqa: E402
from itws.parser import parse_specification  # noqa: E402


@functools.lru_cache(maxsize=1)
def spec():
    """Parse the specification once for the whole suite."""
    return parse_specification(SPEC_DIR)


@functools.lru_cache(maxsize=1)
def catalog() -> Catalog:
    """Load the committed catalog once for the whole suite."""
    return Catalog.from_repo(REPO_ROOT)


def conforming_documents() -> list[Path]:
    return sorted(CONFORMING.glob("*.md"))


def rule_registry_ids() -> set[str]:
    """Permanent rule IDs from the source-controlled registry."""
    path = SPEC_DIR / "rule-ids.txt"
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def retired_rule_ids() -> set[str]:
    """IDs reserved after process-rule retirement."""
    path = SPEC_DIR / "retired-rule-ids.txt"
    ids: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        ids.add(stripped.split()[0])
    return ids


def registry_matches_spec() -> bool:
    """True when the permanent registry equals active rules ∪ retired IDs."""
    current = {rule.number for rule in spec().rules}
    registry = rule_registry_ids()
    retired = retired_rule_ids()
    return (
        registry == current | retired
        and not (current & retired)
    )

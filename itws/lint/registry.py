"""The checker registry.

Every rule marked ``Machine-checkable: yes`` must appear here, and the
compiler fails when one does not (Rule 8.6.1 support). A ``partial`` rule may
also register a checker; its findings are candidates, never violations.

A checker declares a scope so the runner supplies the right input:

``document``
    Reads the structural manifest and the specification model.
``evidence``
    Reads the conformance evidence a run supplies. Absent evidence produces
    a ``blocked`` finding, never a pass (Rule 8.6.3).
``tooling``
    Checks the toolchain itself, such as the §8.2 severity map.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from itws.lint.model import Finding, LintContext

Checker = Callable[[LintContext], Iterable[Finding]]

SCOPES = ("document", "evidence", "tooling")


@dataclass(frozen=True)
class Registration:
    rule: str
    scope: str
    name: str
    checker: Checker
    network: bool = False


_REGISTRY: dict[str, list[Registration]] = {}


def register(rule: str, *, scope: str = "document", name: str = "", network: bool = False):
    """Register one checker for one rule."""
    if scope not in SCOPES:
        raise ValueError(f"unknown checker scope {scope!r}")

    def decorate(function: Checker) -> Checker:
        _REGISTRY.setdefault(rule, []).append(
            Registration(
                rule=rule,
                scope=scope,
                name=name or function.__name__,
                checker=function,
                network=network,
            )
        )
        return function

    return decorate


def registrations() -> dict[str, tuple[Registration, ...]]:
    _load()
    return {rule: tuple(items) for rule, items in sorted(_REGISTRY.items())}


def registered_rule_ids() -> frozenset[str]:
    _load()
    return frozenset(_REGISTRY)


_loaded = False


def _load() -> None:
    global _loaded
    if _loaded:
        return
    _loaded = True
    # Importing the check modules populates the registry.
    from itws.lint import checks_phrase  # noqa: F401
    from itws.lint import checks_vocabulary  # noqa: F401
    from itws.lint import checks_sentences  # noqa: F401
    from itws.lint import checks_structure  # noqa: F401
    from itws.lint import checks_exactness  # noqa: F401
    from itws.lint import checks_process  # noqa: F401

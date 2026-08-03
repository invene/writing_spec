"""Typed records for the non-normative assurance companion."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ASSURANCE_LEVELS = ("core", "reviewed", "publication")


@dataclass(frozen=True)
class AcceptedDeviation:
    """One organizational decision to accept nonconforming text."""

    rule: str
    location: str
    reason: str
    compensating_measure: str
    accepted_by: str
    accepted_on: str
    scope: str

    @classmethod
    def from_json(cls, payload: object) -> "AcceptedDeviation":
        if not isinstance(payload, dict):
            raise ValueError("accepted deviation must be an object")

        def required(name: str) -> str:
            value = payload.get(name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"accepted deviation requires non-empty {name!r}"
                )
            return value.strip()

        return cls(
            rule=required("rule"),
            location=required("location"),
            reason=required("reason"),
            compensating_measure=required("compensating_measure"),
            accepted_by=required("accepted_by"),
            accepted_on=required("accepted_on"),
            scope=required("scope"),
        )

    def to_json(self) -> dict[str, str]:
        return {
            "rule": self.rule,
            "location": self.location,
            "reason": self.reason,
            "compensating_measure": self.compensating_measure,
            "accepted_by": self.accepted_by,
            "accepted_on": self.accepted_on,
            "scope": self.scope,
        }


@dataclass(frozen=True)
class AssuranceRecord:
    """Optional organizational evidence, separate from ITWS declarations."""

    level: str
    checklist_path: str = ""
    self_check_recorded: bool = False
    owner_review_recorded: bool = False
    proxy_review_recorded: bool = False
    reader_test_recorded: bool = False
    release_checks_recorded: bool = False
    accepted_deviations: tuple[AcceptedDeviation, ...] = ()

    @classmethod
    def from_json(cls, payload: object) -> "AssuranceRecord":
        if not isinstance(payload, dict):
            raise ValueError("assurance record must be an object")
        level = payload.get("level")
        if level not in ASSURANCE_LEVELS:
            raise ValueError(
                "assurance level must be one of "
                + ", ".join(ASSURANCE_LEVELS)
            )
        raw_deviations = payload.get("accepted_deviations", ())
        if not isinstance(raw_deviations, (list, tuple)):
            raise ValueError("accepted_deviations must be a list")
        return cls(
            level=level,
            checklist_path=str(payload.get("checklist_path") or ""),
            self_check_recorded=payload.get("self_check_recorded") is True,
            owner_review_recorded=payload.get("owner_review_recorded") is True,
            proxy_review_recorded=payload.get("proxy_review_recorded") is True,
            reader_test_recorded=payload.get("reader_test_recorded") is True,
            release_checks_recorded=(
                payload.get("release_checks_recorded") is True
            ),
            accepted_deviations=tuple(
                AcceptedDeviation.from_json(item)
                for item in raw_deviations
            ),
        )

    @property
    def missing(self) -> tuple[str, ...]:
        required = ["self_check_recorded"]
        if self.level in {"reviewed", "publication"}:
            required.extend(
                ["owner_review_recorded", "proxy_review_recorded"]
            )
        if self.level == "publication":
            required.extend(
                ["reader_test_recorded", "release_checks_recorded"]
            )
        return tuple(name for name in required if not getattr(self, name))

    def to_json(self) -> dict[str, object]:
        return {
            "level": self.level,
            "checklist_path": self.checklist_path,
            "self_check_recorded": self.self_check_recorded,
            "owner_review_recorded": self.owner_review_recorded,
            "proxy_review_recorded": self.proxy_review_recorded,
            "reader_test_recorded": self.reader_test_recorded,
            "release_checks_recorded": self.release_checks_recorded,
            "accepted_deviations": [
                deviation.to_json()
                for deviation in self.accepted_deviations
            ],
            "missing": list(self.missing),
        }


def load_assurance_record(path: Path) -> AssuranceRecord:
    """Load one optional assurance record from JSON."""
    return AssuranceRecord.from_json(
        json.loads(path.read_text(encoding="utf-8"))
    )

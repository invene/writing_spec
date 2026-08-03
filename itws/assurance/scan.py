"""Optional scan-protocol records from the assurance companion."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable

from itws.document import ScanPath, StructuralManifest
from itws.model import content_hash

SCAN_KEY_FIELDS = (
    "purpose",
    "main_point",
    "status_or_strength",
    "material_boundaries",
)
SCAN_TEST_ROLES = ("author", "reader_proxy", "publication_participant")
SCAN_TEST_RESULTS = ("pass", "fail", "blocked")


@dataclass(frozen=True)
class ScanKeyField:
    name: str
    expected: str
    span_ids: tuple[str, ...]
    support: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "expected": self.expected,
            "span_ids": list(self.span_ids),
            "support": list(self.support),
        }


@dataclass(frozen=True)
class StrengthenedFoil:
    id: str
    protected_field: str
    text: str
    span_ids: tuple[str, ...]
    support: tuple[str, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "protected_field": self.protected_field,
            "text": self.text,
            "span_ids": list(self.span_ids),
            "support": list(self.support),
        }


@dataclass(frozen=True)
class ScanTestKey:
    document_path: str
    document_hash: str
    profile: str
    scan_path_hash: str
    fields: tuple[ScanKeyField, ...]
    foils: tuple[StrengthenedFoil, ...]

    def _content_json(self) -> dict[str, object]:
        return {
            "document_path": self.document_path,
            "document_hash": self.document_hash,
            "profile": self.profile,
            "scan_path_hash": self.scan_path_hash,
            "fields": [item.to_json() for item in self.fields],
            "foils": [item.to_json() for item in self.foils],
        }

    @property
    def key_hash(self) -> str:
        rendered = json.dumps(
            self._content_json(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return content_hash(rendered)

    def to_json(self) -> dict[str, object]:
        return {**self._content_json(), "key_hash": self.key_hash}


@dataclass(frozen=True)
class FoilResponse:
    foil_id: str
    accepted: bool

    def to_json(self) -> dict[str, object]:
        return {"foil_id": self.foil_id, "accepted": self.accepted}


@dataclass(frozen=True)
class ScanTestRecord:
    role: str
    profile: str
    document_hash: str
    scan_path_hash: str
    key_hash: str
    linked_source_hashes: tuple[tuple[str, str], ...]
    intervening_task: str
    elapsed_seconds: float
    response_fields: tuple[tuple[str, str], ...]
    foil_responses: tuple[FoilResponse, ...]
    result: str
    findings: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "role": self.role,
            "profile": self.profile,
            "document_hash": self.document_hash,
            "scan_path_hash": self.scan_path_hash,
            "key_hash": self.key_hash,
            "linked_source_hashes": [
                {"span_id": span_id, "source_hash": source_hash}
                for span_id, source_hash in self.linked_source_hashes
            ],
            "intervening_task": self.intervening_task,
            "elapsed_seconds": self.elapsed_seconds,
            "response_fields": dict(self.response_fields),
            "foil_responses": [
                item.to_json() for item in self.foil_responses
            ],
            "result": self.result,
            "findings": list(self.findings),
        }


def validate_scan_test(
    key: ScanTestKey,
    record: ScanTestRecord,
    manifest: StructuralManifest,
    path: ScanPath,
    *,
    known_rules: Iterable[str] = (),
) -> list[str]:
    """Check record shape and staleness without judging response meaning."""
    del known_rules
    problems: list[str] = []
    units = {unit.id: unit for unit in manifest.units}
    if key.document_path != manifest.path:
        problems.append("the scan key names a different document")
    if key.document_hash != manifest.document_hash:
        problems.append("the scan key names a different document hash")
    if key.scan_path_hash != path.scan_path_hash:
        problems.append("the scan key names a different scan path")
    if manifest.declarations and key.profile != manifest.declarations.profile:
        problems.append("the scan key names a different profile")

    field_names = [item.name for item in key.fields]
    if len(field_names) != len(set(field_names)):
        problems.append("the scan key repeats a field")
    for required in SCAN_KEY_FIELDS:
        if required not in field_names:
            problems.append(f"the scan key omits {required!r}")
    for item in key.fields:
        if item.name not in SCAN_KEY_FIELDS:
            problems.append(f"the scan key has unknown field {item.name!r}")
        if not item.expected.strip():
            problems.append(f"scan-key field {item.name!r} is empty")
        for span_id in item.span_ids:
            if span_id not in units:
                problems.append(f"unknown scan-key span {span_id!r}")

    foil_ids = [foil.id for foil in key.foils]
    if len(foil_ids) != len(set(foil_ids)):
        problems.append("the scan key repeats a foil ID")
    for foil in key.foils:
        if foil.protected_field not in {
            "status_or_strength",
            "material_boundaries",
        }:
            problems.append(
                f"foil {foil.id!r} protects an unknown field"
            )
        for span_id in foil.span_ids:
            if span_id not in units:
                problems.append(f"foil {foil.id!r} names unknown span")

    if record.role not in SCAN_TEST_ROLES:
        problems.append(f"unknown scan role {record.role!r}")
    if record.result not in SCAN_TEST_RESULTS:
        problems.append(f"unknown scan result {record.result!r}")
    if record.profile != key.profile:
        problems.append("the scan record names a different profile")
    if record.document_hash != manifest.document_hash:
        problems.append("the scan record is stale for the document")
    if record.scan_path_hash != path.scan_path_hash:
        problems.append("the scan record is stale for the scan path")
    if record.key_hash != key.key_hash:
        problems.append("the scan record is stale for the answer key")

    linked = dict(record.linked_source_hashes)
    for span_id in {
        span_id
        for item in key.fields
        for span_id in item.span_ids
    } | {
        span_id for foil in key.foils for span_id in foil.span_ids
    }:
        unit = units.get(span_id)
        if unit and linked.get(span_id) != unit.source_hash:
            problems.append(f"linked source {span_id!r} is missing or stale")

    responses = {item.foil_id: item for item in record.foil_responses}
    for foil_id in foil_ids:
        if foil_id not in responses:
            problems.append(f"the scan response omits foil {foil_id!r}")
        elif responses[foil_id].accepted:
            problems.append(f"the scan response accepts foil {foil_id!r}")
    for foil_id in responses:
        if foil_id not in foil_ids:
            problems.append(f"the scan response names unknown foil {foil_id!r}")
    return problems

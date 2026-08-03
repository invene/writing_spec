"""Optional assurance helpers.

Nothing in :mod:`itws.lint`, :mod:`itws.validate`, or the generated language
catalog imports this package. Callers opt in when they need organizational
review, release, or accepted-deviation records.
"""

from itws.assurance.model import (
    AcceptedDeviation,
    AssuranceRecord,
    load_assurance_record,
)
from itws.assurance.scan import (
    FoilResponse,
    ScanKeyField,
    ScanTestKey,
    ScanTestRecord,
    StrengthenedFoil,
    validate_scan_test,
)

__all__ = [
    "AcceptedDeviation",
    "AssuranceRecord",
    "load_assurance_record",
    "FoilResponse",
    "ScanKeyField",
    "ScanTestKey",
    "ScanTestRecord",
    "StrengthenedFoil",
    "validate_scan_test",
]

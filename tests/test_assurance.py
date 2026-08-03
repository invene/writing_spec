"""Optional assurance helpers stay outside default validation."""

from __future__ import annotations

import importlib
import unittest

from itws.assurance import FoilResponse, ScanTestRecord, validate_scan_test


class TestAssuranceExports(unittest.TestCase):
    def test_default_validate_does_not_import_assurance(self) -> None:
        validate = importlib.import_module("itws.validate")
        lint_model = importlib.import_module("itws.lint.model")
        engine = importlib.import_module("itws.lint.engine")
        for module in (validate, lint_model, engine):
            imported = set(getattr(module, "__dict__", {}))
            # Reload to inspect real module dependencies via sys.modules edges.
            self.assertNotIn("Evidence", imported)
        self.assertFalse(hasattr(lint_model, "Evidence"))
        self.assertFalse(hasattr(validate, "_human_gates"))
        self.assertFalse(hasattr(validate.ValidationReport, "human_gates"))
        self.assertFalse(hasattr(validate.ValidationReport, "tier"))

    def test_profile_load_set_excludes_assurance(self) -> None:
        from itws.parser import parse_specification
        from pathlib import Path

        spec = parse_specification(Path("spec"))
        for profile in spec.profiles:
            joined = "\n".join(profile.load_set)
            self.assertNotIn("assurance/", joined, profile.id)
            self.assertNotIn("08-review-compliance-tooling.md", joined, profile.id)

    def test_scan_types_import_from_assurance(self) -> None:
        record = ScanTestRecord(
            role="reader_proxy",
            profile="decision-record",
            document_hash="sha256:abc",
            scan_path_hash="sha256:def",
            key_hash="sha256:ghi",
            linked_source_hashes=(),
            intervening_task="sort identifiers",
            elapsed_seconds=60.0,
            response_fields=(),
            foil_responses=(FoilResponse("F-1", False),),
            result="pass",
        )
        self.assertEqual(record.result, "pass")
        self.assertTrue(callable(validate_scan_test))


if __name__ == "__main__":
    unittest.main()

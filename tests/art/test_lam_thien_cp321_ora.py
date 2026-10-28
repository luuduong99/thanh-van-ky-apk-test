"""CP321 ORA template quality gates: structural success is not production approval."""
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "cp321", ROOT / "tools/validate_lam_thien_cp321_ora.py"
)
cp321 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cp321)


class CP321AuditTests(unittest.TestCase):
    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            errors, pending = cp321.audit(Path(temp) / "missing.ora")
            self.assertTrue(any("Missing ORA" in s for s in errors))
            self.assertEqual(pending, [])

    def test_non_ora_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fake.ora"
            path.write_bytes(b"not an ORA")
            errors, pending = cp321.audit(path)
            self.assertTrue(errors)
            self.assertEqual(pending, [])

    def test_template_must_not_pass_strict_gate(self):
        # An archive with an empty layer stack is not rig-ready. The actual
        # CP321 template is Library-backed and not checked into GitHub.
        # For a missing source the strict validation must fail as well.
        with tempfile.TemporaryDirectory() as temp:
            errors, _ = cp321.audit(Path(temp) / "not_production_ready.ora", strict=True)
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()

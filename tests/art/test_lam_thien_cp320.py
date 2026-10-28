"""Unit tests for CP320 input integrity and conservative art readiness."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("cp320", ROOT / "tools/check_lam_thien_cp320.py")
cp320 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cp320)


class CP320Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "docs/art/LAM_THIEN_CP320_VIEW_CALIBRATION.json").read_text(encoding="utf-8"))

    def test_manifest_is_valid_but_pending(self):
        errors, pending = cp320.validate_manifest(self.data)
        self.assertEqual([], errors)
        self.assertGreater(len(pending), 0)

    def test_strict_mode_blocks_unfinished_art(self):
        errors, pending = cp320.validate_manifest(self.data, strict=True)
        self.assertGreater(len(errors), 0)
        self.assertEqual(len(errors), len(pending))

    def test_rejects_faked_landmarks(self):
        x = json.loads(json.dumps(self.data))
        x["views"][0]["landmarks_normalized"] = {"head_top": [1.3, 0.2]}
        errors, _ = cp320.validate_manifest(x)
        self.assertTrue(any("seven named" in e for e in errors))

    def test_rejects_duplicate_percent_application(self):
        x = json.loads(json.dumps(self.data))
        x["canon"]["historical_plus_17_already_included"] = False
        errors, _ = cp320.validate_manifest(x)
        self.assertTrue(any("+17%" in e for e in errors))

    def test_poster_crops_are_reference_only(self):
        refs = self.data["poster_reference_crops"]
        self.assertEqual(len(refs["items"]), 12)
        errors, pending = cp320.validate_manifest(self.data)
        self.assertEqual(errors, [])
        self.assertTrue(pending, "Poster crop extraction is not production art")

    def test_poster_crop_cannot_be_promoted_to_rig_ready(self):
        x = json.loads(json.dumps(self.data))
        x["poster_reference_crops"]["items"][0]["status"] = "production_ready"
        errors, _ = cp320.validate_manifest(x)
        self.assertTrue(any("cannot promote poster crop" in e for e in errors))

    def test_source_header_rejects_non_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "fake.png"
            fake.write_bytes(b"THIS IS NOT PNG")
            self.assertTrue(cp320.verify_png(fake))


if __name__ == "__main__":
    unittest.main()

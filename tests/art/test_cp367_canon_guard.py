"""CP367 tests. Run with approved CANON PNG next to this test to enable real-source checks."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "art" / "cp367_canon_guard.py"
spec = importlib.util.spec_from_file_location("cp367", SCRIPT)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
CANON = Path(__file__).with_name("LAM_THIEN_CANON_V2_1_FINAL_20261029.png")

class Cp367CanonGuardTest(unittest.TestCase):
    def test_invariants_and_blocked_release(self):
        self.assertEqual(g.CANON_SIZE, (941, 1672))
        self.assertEqual(g.FRONT_SIZE, (217, 458))
        self.assertEqual(len(g.TOES), 2)
        self.assertEqual(g.CANON_SHA, "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a")

    def test_wrong_canon_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            fake = Path(folder) / "wrong.png"
            Image.new("RGBA", g.CANON_SIZE, "white").save(fake)
            with self.assertRaisesRegex(ValueError, "CANON_SHA_MISMATCH"):
                g.get_reference(fake)

    @unittest.skipUnless(CANON.exists(), "User-approved image only in private artifact storage")
    def test_both_original_toes_present(self):
        result = g.evaluate(CANON)
        self.assertEqual(result["technical_status"], "SOURCE_TOE_COLOR_COVERAGE_OK")
        self.assertTrue(all(x["pass"] for x in result["toe_results"].values()))
        self.assertFalse(result["apk_approved"])
        self.assertFalse(result["rig_or_spine_ready"])

    @unittest.skipUnless(CANON.exists(), "User-approved image only in private artifact storage")
    def test_missing_left_toe_is_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            image = g.get_reference(CANON)
            image.paste((0, 0, 0, 0), g.TOES["image_left_toe"])
            dest = Path(folder) / "left.png"
            image.save(dest)
            result = g.evaluate(CANON, dest)
            self.assertEqual(result["technical_status"], "TOE_REGRESSION_FOUND")
            self.assertTrue(result["toe_results"]["image_right_toe"]["pass"])

    @unittest.skipUnless(CANON.exists(), "User-approved image only in private artifact storage")
    def test_missing_right_toe_is_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            image = g.get_reference(CANON)
            image.paste((0, 0, 0, 0), g.TOES["image_right_toe"])
            dest = Path(folder) / "right.png"
            image.save(dest)
            result = g.evaluate(CANON, dest)
            self.assertEqual(result["technical_status"], "TOE_REGRESSION_FOUND")
            self.assertTrue(result["toe_results"]["image_left_toe"]["pass"])

    @unittest.skipUnless(CANON.exists(), "User-approved image only in private artifact storage")
    def test_unaligned_crop_is_not_passed(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / "bad-size.png"
            g.get_reference(CANON).crop((0, 0, 215, 449)).save(dest)
            self.assertEqual(g.evaluate(CANON, dest)["technical_status"], "REVIEW_ALIGNMENT")

if __name__ == "__main__":
    unittest.main()

"""CP361 art-study safety contract. Does not certify image quality."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "tools/art/cp361_four_shoulder_underlay_study.py"


class Cp361ArtSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code = BUILDER.read_text(encoding="utf8")

    def test_all_four_independent_vector_regions_exist(self):
        for name in (
            "01_hidden_shoulder_skin", "02_hidden_bodice_inner_fabric",
            "03_rear_silk_underarm", "04_rear_hair_overlap",
        ):
            self.assertIn(name, self.code)

    def test_source_provenance_fails_closed(self):
        self.assertIn("assert hashlib.sha256(CANON.read_bytes()).hexdigest()==CANON_SHA", self.code)
        self.assertIn("assert hashlib.sha256(CP348.read_bytes()).hexdigest()==CP348_SHA", self.code)

    def test_original_idle_pixel_lock(self):
        self.assertIn("np.array_equal(x[:,:,3],y[:,:,3])", self.code)
        self.assertIn("np.array_equal(x[x[:,:,3]>0],y[y[:,:,3]>0])", self.code)

    def test_no_art_runtime_or_rig_approval(self):
        self.assertIn("'complete_highres_character_semantic_art':False", self.code)
        self.assertIn("'approved_sprite':False", self.code)
        self.assertIn("'spine_ready':False", self.code)
        self.assertIn("'production_release':'blocked_pending_art'", self.code)

    def test_two_pose_outputs_are_rigless_diagnostics(self):
        self.assertIn("for deg in (0,-2,-4,-7)", self.code)
        self.assertIn("rigless grouped-arm raster rotation", self.code)

if __name__ == "__main__":
    unittest.main()

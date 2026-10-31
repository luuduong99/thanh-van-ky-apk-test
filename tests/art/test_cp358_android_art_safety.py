"""CP358: actual repository guard for legacy-art status and Android motion diagnostics.

These tests check metadata/source wiring, NOT approved art or measured phone FPS.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "app/src/main/java/vn/thanhvanky/prototype"

class Cp358AndroidArtSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.motion = (SOURCE / "TVKCharacterMotionView.kt").read_text(encoding="utf-8")
        cls.activity = (SOURCE / "CharacterInteractionActivity.kt").read_text(encoding="utf-8")
        cls.resolver = (SOURCE / "CharacterExpressionCatalog.kt").read_text(encoding="utf-8")
        cls.catalog = json.loads((ROOT / "app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))

    def test_debug_motion_metrics_exist(self):
        self.assertIn('Log.d("TVKMotion"', self.motion)
        self.assertIn('canvas_draw_fps=', self.motion)
        self.assertIn('slow_intervals_over_33ms=', self.motion)
        self.assertIn('debug_only_not_display_fps', self.motion)

    def test_motion_metrics_only_on_debuggable_builds(self):
        self.assertIn("ApplicationInfo.FLAG_DEBUGGABLE", self.motion)
        self.assertIn("if (!collectFrameStats || !animate || !isShown) return", self.motion)

    def test_vsync_remains_and_old_25fps_timer_not_returned(self):
        self.assertIn("postInvalidateOnAnimation()", self.motion)
        self.assertNotIn("postInvalidateDelayed(40L)", self.motion)

    def test_blocked_lam_thien_art_is_labelled_in_runtime(self):
        self.assertIn('selectedId == "lin_qian"', self.activity)
        self.assertIn("ẢNH TEST / LEGACY", self.activity)
        self.assertIn("hasApprovedLamThienSprite = CharacterExpressionCatalog.hasRuntimeArtApproval(", self.activity)
        self.assertIn('if (selectedId == "lin_qian" && !hasApprovedLamThienSprite)', self.activity)

    def test_approval_requires_verified_release(self):
        self.assertIn("approvedSpriteRelease(approved) != null", self.resolver)
        self.assertIn("sprite_paths", self.resolver)
        lam = next(c for c in self.catalog["characters"] if c["id"] == "lin_qian")
        self.assertEqual(lam["production_release"]["status"], "blocked_pending_art")
        self.assertEqual(lam["sprite_paths"], {})

if __name__ == "__main__":
    unittest.main()

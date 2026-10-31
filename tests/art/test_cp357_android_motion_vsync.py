"""CP357 frame-pacing contract: test source behavior, not device FPS.

The runtime method postInvalidateOnAnimation() schedules redraw at display
VSYNC. A green test does NOT prove a stable 60 FPS on an actual Android phone.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
VIEW = ROOT / "app/src/main/java/vn/thanhvanky/prototype/TVKCharacterMotionView.kt"

class MotionVsyncContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.code = VIEW.read_text(encoding="utf-8")

    def test_motion_view_uses_vsync_redraw(self):
        self.assertIn("postInvalidateOnAnimation()", self.code)

    def test_old_fixed_40ms_25fps_timer_removed(self):
        self.assertNotIn("postInvalidateDelayed(40L)", self.code)

    def test_respects_animation_toggle(self):
        self.assertIn("fun setMotionEnabled(enabled: Boolean)", self.code)
        self.assertIn("if ((animate || reactAmplitude > 0f) && isAttachedToWindow)", self.code)

    def test_retains_preview_not_rig_disclaimer(self):
        self.assertIn("NOT a skeletal Spine/Live2D rig", self.code)

if __name__ == "__main__":
    unittest.main()

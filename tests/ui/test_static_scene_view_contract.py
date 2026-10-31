"""Static-first scene viewer: contracts for disabled body touch and preserved controls.

These are source-level regression checks. Android runtime/device QA remains separate.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
VIEW = ROOT / "app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt"
MAP = ROOT / "app/src/main/java/vn/thanhvanky/prototype/MainActivity.kt"
POLICY = ROOT / "docs/team/STATIC_FIRST_SCENE_MODE.md"


class ViewOnlySceneContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.viewer = VIEW.read_text(encoding="utf-8")
        cls.map = MAP.read_text(encoding="utf-8")

    def test_body_hitboxes_unwired(self):
        for old in ("touchPortrait(", "respondToTouch(", "setOnTouchListener",
                    "MotionEvent.ACTION_DOWN", "touchFeedbackView"):
            with self.subTest(old=old):
                self.assertNotIn(old, self.viewer)

    def test_portrait_not_mesh_or_warped(self):
        self.assertIn("ImageView(this)", self.viewer)
        self.assertIn("ImageView.ScaleType.FIT_CENTER", self.viewer)
        self.assertNotIn("TVKCharacterMotionView(", self.viewer)
        self.assertNotIn("interactive = true", self.viewer)
        self.assertNotIn("drawBitmapMesh(", self.viewer)

    def test_pose_wardrobe_character_and_scene_controls_preserved(self):
        for required in ("CharacterAppearanceState.setPose(",
                         "CharacterAppearanceState.setWardrobe(",
                         "CharacterAppearanceState.setExpression(",
                         'getJSONArray("controls")',
                         'getJSONArray("scenes")',
                         "selectScene(heroine, control)",
                         "openWardrobe(character)",
                         'btn("TRÒ CHUYỆN")',
                         'btn("← Bản đồ")'):
            with self.subTest(required=required):
                self.assertIn(required, self.viewer)

    def test_missing_art_cannot_silently_substitute(self):
        self.assertIn("CharacterAppearanceState.resolveArt(", self.viewer)
        self.assertIn("safeHeroineImage", self.viewer)
        self.assertIn('portrait("Nam chính"', self.viewer)
        self.assertIn("chưa có trong APK", self.viewer)

    def test_scene_tap_explains_mode(self):
        self.assertIn("Chạm trực tiếp lên cơ thể không kích hoạt tương tác", self.viewer)
        self.assertIn("XEM CẢNH NHÂN VẬT · STATIC-FIRST", self.viewer)
        self.assertIn("CHỌN CẢNH / TƯ THẾ / TRANG PHỤC BẰNG NÚT", self.viewer)

    def test_map_dialogue_tap_still_exists(self):
        self.assertIn("override fun onTouchEvent", self.map)
        self.assertIn('getSharedPreferences("tvk_chapter_1"', self.map)

    def test_policy_mentions_release_gate(self):
        text = POLICY.read_text(encoding="utf-8")
        for key in ("VIEW-01", "VIEW-08", "không dùng", "FIT_CENTER",
                    "TVK-01", "TVK-02", "TVK-03", "TVK-04"):
            with self.subTest(key=key):
                self.assertIn(key, text)


if __name__ == "__main__":
    unittest.main()

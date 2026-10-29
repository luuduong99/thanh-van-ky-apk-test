"""CP324: approved expression metadata/runtime safety without claiming sprite art exists."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSET = ROOT / "app/src/main/assets/character_expression_profiles.json"
APP = ROOT / "app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt"
CATALOGUE = ROOT / "app/src/main/java/vn/thanhvanky/prototype/CharacterExpressionCatalog.kt"
STATE = ROOT / "app/src/main/java/vn/thanhvanky/prototype/CharacterAppearanceState.kt"
APPROVED = ROOT / "docs/art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json"
GLOBAL = ROOT / "docs/art/GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.json"
MODEL = ROOT / "docs/art/LAM_THIEN_MODEL_CARD_V2.json"
EXPECTED = ["shy", "angry", "pain", "embarrassed", "alluring"]


class CP324ExpressionRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = json.loads(ASSET.read_text(encoding="utf-8"))
        cls.approved = json.loads(APPROVED.read_text(encoding="utf-8"))
        cls.global_standard = json.loads(GLOBAL.read_text(encoding="utf-8"))
        cls.model = json.loads(MODEL.read_text(encoding="utf-8"))
        cls.app_src = APP.read_text(encoding="utf-8")
        cls.resolver_src = CATALOGUE.read_text(encoding="utf-8")
        cls.state_src = STATE.read_text(encoding="utf-8")

    def test_exactly_five_explicitly_approved_lam_thien_expressions(self):
        chars = {c["id"]: c for c in self.catalogue["characters"]}
        lam = chars["lin_qian"]
        self.assertEqual([e["id"] for e in lam["approved_expressions"]], EXPECTED)
        self.assertEqual([e["id"] for e in self.approved["approved_expressions"]], EXPECTED)
        self.assertEqual(lam["approval_status"], "approved_reference_sprite_pending")
        self.assertEqual(lam["approved_profile_id"], self.approved["expression_profile_id"])

    def test_body_and_expression_reference_ids_cannot_be_confused(self):
        lam = next(x for x in self.catalogue["characters"] if x["id"] == "lin_qian")
        self.assertEqual(lam["canonical_body_visual_id"], self.model["canonical_visual_id"])
        self.assertEqual(lam["canonical_body_sha256"], self.model["source"]["sha256"])
        self.assertEqual(lam["expression_preview_sha256"], self.approved["source"]["sha256"])
        self.assertNotEqual(lam["canonical_body_sha256"], lam["expression_preview_sha256"])

    def test_other_character_has_no_reused_approved_face(self):
        ly = next(x for x in self.catalogue["characters"] if x["id"] == "to_nguyet_ly")
        self.assertEqual(ly["approval_status"], "individual_preview_required")
        self.assertIsNone(ly["approved_profile_id"])
        self.assertEqual(ly["approved_expressions"], [])
        self.assertEqual(ly["sprite_paths"], {})
        self.assertTrue(self.global_standard["per_character_requirements"]["requires_individual_preview_approval"])

    def test_no_sprite_fabricated_from_flat_approved_sheet(self):
        for c in self.catalogue["characters"]:
            self.assertEqual(c["sprite_paths"], {})
            self.assertEqual(c["sprite_status"], "not_created")
            self.assertEqual(c["spine_status"], "not_created")
        self.assertFalse(self.approved["art_qa"]["facial_layer_sprites_complete"])
        self.assertFalse(self.approved["art_qa"]["spine_animation_complete"])

    def test_switching_pose_does_not_reset_selected_expression(self):
        pose_handler = self.app_src.split('val poseButton = btn(option.optString("label")) {', 1)[1]
        pose_handler = pose_handler.split('poseButton.setBackgroundDrawable', 1)[0]
        self.assertIn("CharacterAppearanceState.setPose(this, selectedId, poseId)", pose_handler)
        self.assertNotIn("CharacterAppearanceState.setExpression(", pose_handler)
        self.assertIn('prefKey(id, "expression")', self.state_src)

    def test_expression_button_does_not_change_wardrobe_integrity_or_pose(self):
        btn = self.app_src.split("val chooseExpression = btn(option.label) {", 1)[1]
        btn = btn.split("chooseExpression.setBackgroundDrawable", 1)[0]
        self.assertIn("CharacterAppearanceState.setExpression(this, selectedId, option.id)", btn)
        for forbidden in ("setWardrobe(", "setIntegrity(", "setPose(", "setAction("):
            self.assertNotIn(forbidden, btn)

    def test_missing_expression_sprite_has_no_silent_neutral_fallback(self):
        self.assertIn("if (requiresExpressionArt) expressionArt.orEmpty()", self.app_src)
        self.assertIn("CharacterExpressionCatalog.resolveSprite(", self.app_src)
        self.assertIn("!path.startsWith(\"characters/\" + characterId + \"/\")", self.resolver_src)
        for marker in ("state.expression", "state.wardrobe", "state.integrity.toString()", "state.pose"):
            self.assertIn(marker, self.resolver_src)

    def test_wardrobe_dialog_does_not_reset_expression(self):
        self.assertIn('if (sceneKind != "wardrobe")', self.app_src)
        self.assertIn('CharacterAppearanceState.setExpression(this, characterId, expression)', self.app_src)


if __name__ == "__main__":
    unittest.main()

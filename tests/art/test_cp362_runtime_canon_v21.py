"""CP362 active V2.1 runtime release contract. Checks metadata, not sprite art."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANON_ID = "LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29"
CANON_SHA = "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
OLD_ID = "LT_CANON_BODY_REF_2026-10-28_V2"

class Cp362RuntimeCanonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = json.loads((ROOT / "app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))
        cls.registry = json.loads((ROOT / "docs/art/LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
        cls.guard = (ROOT / "app/src/main/java/vn/thanhvanky/prototype/CharacterExpressionCatalog.kt").read_text(encoding="utf-8")
        cls.lam = next(x for x in cls.catalogue["characters"] if x["id"] == "lin_qian")

    def test_active_canon_source_is_exact_user_approved_v21(self):
        current = self.registry["latest_user_approved_design"]
        self.assertEqual((current["id"], current["visual_reference_sha256"]), (CANON_ID, CANON_SHA))
        self.assertEqual(self.lam["canonical_body_visual_id"], CANON_ID)
        self.assertEqual(self.lam["canonical_body_sha256"], CANON_SHA)

    def test_runtime_release_metadata_locked_to_v21(self):
        release = self.lam["production_release"]
        self.assertEqual(release["canonical_body_visual_id"], CANON_ID)
        self.assertEqual(release["canonical_body_sha256"], CANON_SHA)
        self.assertEqual(self.lam["active_user_approved_art_reference"]["sha256"], CANON_SHA)
        self.assertIn('release.optString("canonical_body_sha256") != canonSha', self.guard)
        self.assertIn('active.optString("sha256") != canonSha', self.guard)

    def test_older_body_reference_preserved_only_as_history(self):
        self.assertEqual(self.lam["archived_body_release_metadata"]["id"], OLD_ID)
        self.assertNotEqual(self.lam["archived_body_release_metadata"]["sha256"], CANON_SHA)

    def test_game_art_release_still_blocked(self):
        self.assertEqual(self.lam["production_release"]["status"], "blocked_pending_art")
        self.assertEqual(self.lam["sprite_paths"], {})
        self.assertFalse(self.lam["production_release"]["artist_qa_passed"])
        self.assertFalse(self.lam["production_release"]["runtime_qa_passed"])

    def test_release_build_does_not_fallback_to_legacy_flat_portrait(self):
        activity = (ROOT / "app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt").read_text(encoding="utf-8")
        self.assertIn("ApplicationInfo.FLAG_DEBUGGABLE", activity)
        self.assertIn('selectedId == "lin_qian" && !hasApprovedLamThienSprite && !debugArtPreview', activity)
        self.assertIn('val safeHeroineImage', activity)
        self.assertEqual(activity.count('portrait(heroine.optString("name"), safeHeroineImage,'), 2)
        self.assertNotIn('portrait(heroine.optString("name"), heroineImage,', activity)

    def test_expression_approval_remains_independent(self):
        self.assertEqual(len(self.lam["approved_expressions"]),5)
        self.assertEqual(self.lam["approved_profile_id"], "LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED")

if __name__ == "__main__":
    unittest.main()

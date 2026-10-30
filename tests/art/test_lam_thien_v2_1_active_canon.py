"""Protect the user-approved Lâm Thiển V2.1 visual reference against reverting to older sheets.

Only text manifest and registry are held in this GitHub repo. The original
PNG was SHA-256 verified locally and stored in persistent ChatGPT Library.
"""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
HASH="f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
ID="LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29"
MAN=json.loads((ART/"LAM_THIEN_CANON_V2_1_FINAL_MANIFEST.json").read_text(encoding="utf-8"))
REG=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
MODEL=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2_1_FINAL.json").read_text(encoding="utf-8"))
LEGACY=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2.json").read_text(encoding="utf-8"))
PROFILES=json.loads((ROOT/"app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))

class ActiveCanonV21(unittest.TestCase):
    def test_original_approved_hash_is_pinned(self):
        self.assertEqual(MAN["canonical_id"],ID)
        self.assertEqual(MAN["sha256"],HASH)
        self.assertEqual(REG["latest_user_approved_design"]["visual_reference_sha256"],HASH)
        self.assertEqual(REG["latest_user_approved_design"]["id"],ID)
        self.assertEqual(MODEL["source"]["sha256"],HASH)
        self.assertEqual(MODEL["active_canonical_visual_id"],ID)

    def test_approved_visual_is_exact_9_by_16_board(self):
        self.assertEqual([MAN["width"],MAN["height"]],[941,1672])
        self.assertEqual(MAN["mode"],"RGBA")
        self.assertEqual(MODEL["source"]["filename"],"LAM_THIEN_CANON_V2_1_FINAL_20261029.png")
        self.assertIn("Approved References/Lam_Thien_CANON_V2_1_FINAL_20261029",MODEL["source"]["library_path"])

    def test_user_decisions_not_accidentally_revised(self):
        self.assertEqual(MAN["approved_details"]["expressions"],["shy","angry","pain","embarrassed","alluring"])
        self.assertEqual(sorted(int(x) for x in MAN["approved_details"]["garment_integrity_states"]),[30,50,70,100])
        self.assertEqual(MAN["approved_details"]["body_plus_17_percent"],"already baked in; do not reapply")
        self.assertTrue(MODEL["locked"]["damage_30_not_exaggerated"])

    def test_outdated_visuals_are_archived(self):
        self.assertEqual(LEGACY["superseded_by_canonical_id"],ID)
        self.assertNotEqual(LEGACY["source"]["sha256"],HASH)
        self.assertTrue(REG["previous_approval_sources_archived"]["not_authoritative_for_new_art"])
        self.assertEqual(REG["active_final_canonic_sheet_id"],ID)

    def test_reference_approval_does_not_unlock_runtime(self):
        self.assertFalse(MAN["production_safety"]["artist_drawn_layered_source_complete"])
        self.assertFalse(MAN["production_safety"]["spine_ready"])
        self.assertFalse(MAN["production_safety"]["apk_build_verified"])
        self.assertEqual(MAN["production_safety"]["android_production_release"],"blocked_pending_art")
        lam=next(c for c in PROFILES["characters"] if c["id"]=="lin_qian")
        self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
        self.assertFalse(lam["sprite_paths"])

    def test_spec_and_plan_visible(self):
        spec=(ROOT/"docs/PROJECT_SPEC.md").read_text(encoding="utf-8")
        self.assertIn(HASH,spec[:2000])
        # The project file prepends checkpoints; the plan remains authoritative
        # even when its link moves beyond a brittle fixed-length prefix.
        self.assertIn("LAM_THIEN_PLAN_AFTER_CANON_V2_1.md",spec)
        self.assertIn("P1", (ART/"LAM_THIEN_PLAN_AFTER_CANON_V2_1.md").read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()

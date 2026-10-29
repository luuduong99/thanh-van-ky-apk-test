"""CP342 metadata contract; 13 binary PNG/ORA tests run locally against the Library package."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
M=json.loads((ART/"LAM_THIEN_CP342_SHADOW_CLEANUP_MANIFEST.json").read_text())
CAN=json.loads((ART/"LAM_THIEN_CANON_V2_1_FINAL_MANIFEST.json").read_text())
REG=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text())
MODEL=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2_1_FINAL.json").read_text())
ASSETS=json.loads((ROOT/"app/src/main/assets/character_expression_profiles.json").read_text())

class CP342SourceLock(unittest.TestCase):
    def test_source_canon_is_final_user_approved(self):
        self.assertEqual(M["canon_id"],CAN["canonical_id"])
        self.assertEqual(M["canon_sha256"],CAN["sha256"])
        self.assertEqual(M["canon_sha256"],MODEL["source"]["sha256"])
        self.assertEqual(M["canon_id"],REG["latest_user_approved_design"]["id"])
    def test_nondeceptive_flat_cutout(self):
        self.assertEqual(M["native_front_px"],[215,449])
        self.assertTrue(M["rgb_unchanged"])
        self.assertTrue(M["upper_410_scanlines_alpha_unchanged"])
        self.assertTrue(M["still_single_flat_character_foreground"])
        self.assertTrue(M["not_artist_clean_semantic_layers"])
    def test_floor_shadow_change_localized(self):
        q=M["pixel_qa"]
        self.assertEqual(q["upper_body_untouched_pixels"],410*215)
        self.assertEqual(q["upper_torso_delta"],0)
        self.assertEqual(q["center_shoe_delta"],0)
        self.assertGreater(q["floor_zone_delta"],100000)
        self.assertGreater(q["alpha_pixels_changed"],1000)
        self.assertGreater(q["before_alpha_gt_128"],q["after_alpha_gt_128"])
    def test_files_have_real_hashes(self):
        self.assertGreaterEqual(len(M["output_files"]),9)
        for item in M["output_files"].values():
            self.assertEqual(len(item["sha256"]),64)
    def test_runtime_cannot_use_unapproved_art(self):
        g=M["production_gate"]
        for x in ["manual_artist_edge_clean_approved","face_underpaint_complete","independent_hair_body_garment_parts_created","riggable_layers_ready","spine_verified","apk_built_and_tested"]:
            self.assertFalse(g[x],x)
        self.assertEqual(g["runtime_release"],"blocked_pending_art")
        lam=next(c for c in ASSETS["characters"] if c["id"]=="lin_qian")
        self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
        self.assertFalse(lam["sprite_paths"])

if __name__=="__main__":unittest.main()

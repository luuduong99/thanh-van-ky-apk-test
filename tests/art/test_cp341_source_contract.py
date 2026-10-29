"""CP341 CI: metadata only. Real PNG + OpenRaster tests are local from Library ZIP."""
import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[2];A=R/"docs/art"
M=json.loads((A/"LAM_THIEN_CP341_MATTE_MANIFEST.json").read_text(encoding="utf-8"))
CAN=json.loads((A/"LAM_THIEN_CANON_V2_1_FINAL_MANIFEST.json").read_text(encoding="utf-8"))
REG=json.loads((A/"LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
PROFILE=json.loads((R/"app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))
class SourceAndQualityGate(unittest.TestCase):
 def test_active_canon_not_older_reference(self):
  self.assertEqual(M["canonical_id"],CAN["canonical_id"])
  self.assertEqual(M["canonical_sha256"],CAN["sha256"])
  self.assertEqual(REG["latest_user_approved_design"]["id"],CAN["canonical_id"])
 def test_native_crop_and_real_source_pixels_protected(self):
  self.assertEqual(M["front_source_bbox_xyxy"],[13,177,228,626])
  self.assertEqual(M["front_native_px"],[215,449])
  self.assertTrue(M["front_rgb_exact_original"])
  self.assertTrue(M["flat_source_only"])
 def test_mask_contains_more_hair_and_fabric(self):
  self.assertGreater(M["opaque_px_gain"],18000)
  self.assertEqual(M["refined_cutout_opaque_px"]-M["old_cutout_opaque_px"],M["opaque_px_gain"])
  self.assertEqual(len(M["region_checks"]),4)
  self.assertTrue(all(item["delta_opaque_px"]>2000 for item in M["region_checks"].values()))
 def test_editable_layer_files_are_not_spine_rig(self):
  self.assertIn("ora",M["output_files"])
  self.assertIn("alpha_mask",M["output_files"])
  self.assertTrue(M["not_artist_semantic_layers"])
  self.assertFalse(M["production_gate"]["separate_character_parts_completed"])
  self.assertFalse(M["production_gate"]["artist_clean_edges_approved"])
 def test_runtime_release_stays_blocked(self):
  self.assertFalse(M["production_gate"]["spine_verified"])
  self.assertFalse(M["production_gate"]["apk_verified"])
  self.assertEqual(M["production_gate"]["android_production_release"],"blocked_pending_art")
  lam=next(c for c in PROFILE["characters"] if c["id"]=="lin_qian")
  self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
  self.assertFalse(lam["sprite_paths"])
if __name__=="__main__":unittest.main()

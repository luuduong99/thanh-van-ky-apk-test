"""Metadata only. Binary ORA and PNG test suite runs locally against CP343 Library ZIP."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
M=json.loads((ART/"LAM_THIEN_CP343_REGION_LAYER_MANIFEST.json").read_text(encoding="utf-8"))
CAN=json.loads((ART/"LAM_THIEN_CANON_V2_1_FINAL_MANIFEST.json").read_text(encoding="utf-8"))
REG=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
P=json.loads((ROOT/"app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))
class CP343Metadata(unittest.TestCase):
 def test_source_locked(self):
  self.assertEqual(M["approved_canon_id"],CAN["canonical_id"])
  self.assertEqual(M["approved_source_sha256"],CAN["sha256"])
  self.assertEqual(M["approved_canon_id"],REG["latest_user_approved_design"]["id"])
 def test_ten_distinct_real_regions(self):
  self.assertEqual(M["region_count"],10)
  self.assertEqual(len(M["region_assignments"]),10)
  self.assertEqual(sum(x["visible_pixels"] for x in M["region_assignments"]),M["visible_source_pixels"])
  self.assertTrue(all(len(x["png_sha256"])==64 and x["visible_pixels"]>0 for x in M["region_assignments"]))
 def test_source_rest_is_preserved_not_riggable(self):
  self.assertEqual(M["native_cutout_size"],[215,449])
  self.assertTrue(M["visible_recomposition_is_pixel_exact"])
  for k in ("underpaint_for_motion_exists","semantic_borders_artist_verified","high_resolution_repaint_exists","riggable_layers_ready","spine_verified","apk_verified"):
   self.assertFalse(M[k],k)
 def test_movement_artifact_is_reported_as_failure(self):
  trial=M["arm_motion_stress_test"]
  self.assertEqual(trial["result"],"FAIL_no_hidden_underpaint")
  self.assertGreater(trial["missing_source_pixels"],1000)
  self.assertGreater(trial["new_protruding_pixels"],500)
 def test_game_remains_blocked(self):
  self.assertEqual(M["android_production_release"],"blocked_pending_art")
  self.assertEqual(M["game_sprite_paths_registered"],0)
  lam=next(x for x in P["characters"] if x["id"]=="lin_qian")
  self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
  self.assertFalse(lam["sprite_paths"])
if __name__=="__main__":unittest.main()

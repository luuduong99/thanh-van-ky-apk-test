"""CP340: metadata contract only. Binary PNG/ORA QA is local in Library package."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];A=ROOT/"docs/art"
M=json.loads((A/"LAM_THIEN_CP340_ALPHA_TRIAL_MANIFEST.json").read_text())
REG=json.loads((A/"LAM_THIEN_DESIGN_REGISTRY.json").read_text())
V21=json.loads((A/"LAM_THIEN_CANON_V2_1_FINAL_MANIFEST.json").read_text())
PROFILE=json.loads((ROOT/"app/src/main/assets/character_expression_profiles.json").read_text())
class CP340SourceLock(unittest.TestCase):
 def test_real_source_is_latest_approved(self):
  self.assertEqual(M["source_sha256"],V21["sha256"])
  self.assertEqual(M["source_id"],REG["latest_user_approved_design"]["id"])
  self.assertEqual(M["source_sha256"],REG["latest_user_approved_design"]["visual_reference_sha256"])
 def test_fourteen_references_same_source_and_native(self):
  self.assertEqual(len(M["reference_crops"]),14)
  self.assertEqual(sum(x["id"].startswith("view_") for x in M["reference_crops"]),5)
  self.assertEqual(sum(x["id"].startswith("emotion_") for x in M["reference_crops"]),5)
  self.assertEqual(sum(x["id"].startswith("damage_") for x in M["reference_crops"]),4)
  self.assertTrue(all(x["exact_source_pixels"] for x in M["reference_crops"]))
 def test_one_front_cutout_is_not_sprite_art(self):
  self.assertEqual(M["first_alpha_trial"]["native_size"],[215,449])
  self.assertTrue(M["first_alpha_trial"]["source_rgb_pixels_unchanged"])
  self.assertFalse(M["first_alpha_trial"]["approved"])
  for x in ("spine_ready","clean_underpaint_done","facial_attachments_independent","real_artist_native_highres_layers_complete"):
   self.assertFalse(M["production"][x])
 def test_runtime_remains_blocked(self):
  lam=next(c for c in PROFILE["characters"] if c["id"]=="lin_qian")
  self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
  self.assertFalse(lam["sprite_paths"])
  self.assertEqual(REG["latest_user_approved_design"]["id"],"LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29")
if __name__=="__main__":unittest.main()

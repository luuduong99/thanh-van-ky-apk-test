"""CP331 metadata gate — not a replacement for Library-backed ORA binary QA."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
DATA=json.loads((ART/"LAM_THIEN_CP331_SHARED_FACE_TRIAL_MANIFEST.json").read_text(encoding="utf-8"))
MODEL=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2.json").read_text(encoding="utf-8"))
EXP=json.loads((ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json").read_text(encoding="utf-8"))
REG=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
IDS=["shy","angry","pain","embarrassed","alluring"]
PARTS={"brow_image_left","brow_image_right","eye_image_left","eye_image_right","mouth","blush_image_left","blush_image_right"}

class CP331Contract(unittest.TestCase):
    def test_visual_authority_unchanged(self):
        self.assertEqual(DATA["canonical_visual_id"],MODEL["canonical_visual_id"])
        self.assertEqual(DATA["canonical_sha256"],MODEL["source"]["sha256"])
        self.assertEqual(DATA["canonical_visual_id"],REG["latest_user_approved_design"]["id"])
        self.assertEqual(DATA["approved_expression_profile"],EXP["expression_profile_id"])
        self.assertEqual(DATA["approved_expression_sha256"],EXP["source"]["sha256"])
        self.assertEqual(REG["approved_expression_profile"]["id"],EXP["expression_profile_id"])

    def test_all_five_emotions_and_seven_regions(self):
        self.assertEqual([r["id"] for r in DATA["results"]],IDS)
        self.assertEqual(set(DATA["target_region_boxes"]),PARTS)
        self.assertEqual(DATA["layer_count_total"],35)
        self.assertEqual(DATA["orafiles"],5)
        self.assertTrue(all(r["source_patch_layers_nonempty"]==7 for r in DATA["results"]))

    def test_only_one_flat_underpaint_reference(self):
        self.assertEqual(len(set(x["underpaint_sha256"] for x in DATA["results"])),1)
        self.assertTrue(DATA["outside_face_region_pixel_identical"])
        self.assertEqual(DATA["base_source_panel"],"angry")

    def test_technical_trial_not_approved_new_face(self):
        self.assertEqual(DATA["status"],"shared_face_master_technical_trial_unapproved_not_spine_ready")
        self.assertNotEqual(DATA["new_sheet_sha256"],DATA["canonical_sha256"])
        self.assertNotEqual(DATA["new_sheet_sha256"],DATA["approved_expression_sha256"])
        self.assertEqual(DATA["new_sheet_source_kind"],"AI_generated_flat_unapproved")
        for key in ("shared_master_art_production_ready","new_generated_face_visual_approved",
                    "shared_underpaint_artist_approved","source_is_true_high_resolution",
                    "spine_ready","apk_verified","asset_registration_allowed"):
            self.assertFalse(DATA[key],key)

    def test_baked_in_features_and_hidden_inpaint_must_be_disclosed(self):
        self.assertTrue(DATA["flat_master_contains_baked_facial_features"])
        self.assertTrue(DATA["shared_underpaint_is_hidden_draft_only"])
        self.assertIn("not_independent_rig_attachments",DATA["face_attachment_semantics"])

    def test_raw_size_has_not_been_falsified(self):
        self.assertEqual(DATA["native_source_dimensions_px"],[258,364])
        for r in DATA["results"]:
            self.assertEqual(r["native_dimensions_px"],[258,364])
            self.assertIs(r["production_approved"],False)

    def test_ora_hashes_unique_and_nonblank(self):
        values=[x["ora_sha256"] for x in DATA["results"]]
        self.assertEqual(len(values),len(set(values)))
        self.assertTrue(all(len(x)==64 for x in values))

if __name__=="__main__":
    unittest.main()

"""CP325: guard metadata of editable facial-reference patches.

This does NOT test the binary ORAs, which are backed up in ChatGPT Library.
Run tools/cp325/test_cp325_face_proxies.py against the extracted Library ZIP
for real alpha/CRC/source-pixel verification.
"""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
MANIFEST=ART/"LAM_THIEN_CP325_FACE_REGION_PROXY_MANIFEST.json"
APPROVED=ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json"
MODEL=ART/"LAM_THIEN_MODEL_CARD_V2.json"
ASSET=ROOT/"app/src/main/assets/character_expression_profiles.json"
EMOTIONS=["shy","angry","pain","embarrassed","alluring"]
REGIONS={
  "brow_image_left","brow_image_right","eye_image_left","eye_image_right",
  "mouth","blush_image_left","blush_image_right"
}


class CP325ReferenceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.approved=json.loads(APPROVED.read_text(encoding="utf-8"))
        cls.model=json.loads(MODEL.read_text(encoding="utf-8"))
        cls.asset=json.loads(ASSET.read_text(encoding="utf-8"))

    def test_only_five_approved_reference_emotions(self):
        self.assertEqual([x["emotion_id"] for x in self.manifest["items"]],EMOTIONS)
        self.assertEqual(
            [e["id"] for e in self.approved["approved_expressions"]],EMOTIONS
        )

    def test_never_change_body_canon_or_expression_preview(self):
        self.assertEqual(self.manifest["canonical_body_visual_id"],self.model["canonical_visual_id"])
        self.assertEqual(self.manifest["canonical_body_sha256"],self.model["source"]["sha256"])
        self.assertEqual(self.manifest["approved_expression_sheet_sha256"],
                         self.approved["source"]["sha256"])
        self.assertEqual(self.manifest["approved_expression_profile_id"],
                         self.approved["expression_profile_id"])

    def test_seven_facial_regions_per_emotion_with_native_dimensions(self):
        self.assertEqual(len(self.manifest["items"]),5)
        for item in self.manifest["items"]:
            self.assertEqual(set(x["name"] for x in item["regions"]),REGIONS)
            self.assertEqual(len(item["regions"]),7)
            width,height=item["native_size_px"]
            self.assertLess(width,400,"Do not misrepresent native low-resolution poster as HD")
            self.assertEqual(height,385)
            for region in item["regions"]:
                x0,y0,x1,y1=region["source_bbox_xyxy"]
                self.assertTrue(0<=x0<x1<=width and 0<=y0<y1<=height)
                self.assertGreater(region["alpha_nonzero"],0)

    def test_art_proxy_is_not_registered_as_game_asset(self):
        self.assertFalse(self.manifest["asset_registration_allowed"])
        self.assertFalse(self.manifest["spine_ready"])
        self.assertFalse(self.manifest["apk_ready"])
        self.assertEqual(self.manifest["status"],
                         "REFERENCE_REGION_EDITABLE_POC_NOT_GAME_ART")
        for character in self.asset["characters"]:
            self.assertEqual(character["sprite_paths"],{})
            self.assertEqual(character["sprite_status"],"not_created")

    def test_no_false_claim_of_independent_face_layers(self):
        for item in self.manifest["items"]:
            self.assertTrue(item["patches_feathered_from_flat_reference"])
            self.assertTrue(item["reference_hidden"])
            self.assertEqual(item["status"],"PROTOTYPE_ART_REGION_NOT_FACE_RIG")


if __name__=="__main__":
    unittest.main()

"""CP326 contract: prototype preserves approved face/body decisions and blocks game promotion."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
MANIFEST=ART/"LAM_THIEN_CP326_VECTOR_FACE_MANIFEST.json"
APPROVED=ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json"
CANON=ART/"LAM_THIEN_MODEL_CARD_V2.json"
PROFILES=ROOT/"app/src/main/assets/character_expression_profiles.json"
EMOTIONS=["shy","angry","pain","embarrassed","alluring"]
PARTS={"blush_image_left","blush_image_right","eye_image_left","eye_image_right",
       "brow_image_left","brow_image_right","mouth"}

class CP326VectorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.approved=json.loads(APPROVED.read_text(encoding="utf-8"))
        cls.model=json.loads(CANON.read_text(encoding="utf-8"))
        cls.profiles=json.loads(PROFILES.read_text(encoding="utf-8"))

    def test_v2_and_five_expressions_source_immutable(self):
        d=self.data
        self.assertEqual(d["canonical_body_visual_id"],self.model["canonical_visual_id"])
        self.assertEqual(d["canonical_body_sha256"],self.model["source"]["sha256"])
        self.assertEqual(d["approved_five_expression_sheet_sha256"],
                         self.approved["source"]["sha256"])

    def test_five_distinct_ora_with_seven_independently_drawn_layers_each(self):
        d=self.data
        self.assertEqual(d["expression_ids"],EMOTIONS)
        self.assertEqual([i["id"] for i in d["items"]],EMOTIONS)
        self.assertEqual(len(set(i["ora_sha256"] for i in d["items"])),5)
        self.assertEqual(sum(i["alpha_independent_layers"] for i in d["items"]),35)
        for item in d["items"]:
            self.assertEqual(set(item["parts"]),PARTS)
            for layer in item["parts"].values():
                self.assertGreater(layer["alpha_nonzero_pixels"],0)
                self.assertEqual(layer["rgba_mode"],"RGBA")
                self.assertIs(layer["native_source_pixels_used"],False)

    def test_native_resolution_accurately_disclosed(self):
        self.assertEqual(self.data["native_source_size_px"],[230,114])
        self.assertEqual(self.data["rendered_canvas_px"],[920,456])
        self.assertEqual(self.data["enlargement_factor"],4)
        self.assertEqual(self.data["art_mode"],"independent_alpha_vector_render_with_source_canon_guide")

    def test_underpaint_draft_must_never_be_registered_to_apk(self):
        self.assertEqual(self.data["created_files"],5)
        for item in self.data["items"]:
            self.assertEqual(item["underpaint_status"],"algorithmic_placeholder")
            self.assertEqual(item["guide_status"],"original_canon_source_hidden")
        self.assertFalse(self.data["production_ready"])
        self.assertFalse(self.data["spine_ready"])
        self.assertFalse(self.data["apk_ready"])
        self.assertFalse(self.data["asset_registration_allowed"])
        for character in self.profiles["characters"]:
            self.assertEqual(character["sprite_paths"],{})
            self.assertEqual(character["sprite_status"],"not_created")

    def test_draft_must_not_replace_approved_expression_reference(self):
        self.assertEqual(self.data["status"],
            "new_vector_facial_parts_on_canon_v2_inpaint_prototype_not_approved_for_game")
        self.assertEqual(self.approved["approval_status"],
            "explicit_user_approved_expression_preview")
        self.assertEqual(self.approved["art_qa"]["facial_layer_sprites_complete"],False)

if __name__=="__main__":unittest.main()

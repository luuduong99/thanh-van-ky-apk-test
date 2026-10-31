"""CP334 art-direction metadata contract.

Only metadata and original approved source SHA are in this repository. The
actual generated flat portraits and review ORA are in Library, audited
separately with tools/cp334/verify_cp334.py after extracting the ZIP.
"""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
MAN=json.loads((ART/"LAM_THIEN_CP334_ART_REVIEW_MANIFEST.json").read_text(encoding="utf-8"))
BODY=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2.json").read_text(encoding="utf-8"))
EXP=json.loads((ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json").read_text(encoding="utf-8"))
REG=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
IDS=["shy","angry","pain","embarrassed","alluring"]


class CP334ReviewMetadataTests(unittest.TestCase):
    def test_ref_identity_is_immutable(self):
        self.assertEqual(MAN["canonical_visual_id"],BODY["canonical_visual_id"])
        self.assertEqual(MAN["canonical_sha256"],BODY["source"]["sha256"])
        self.assertEqual(MAN["canonical_visual_id"],next(x for x in REG["archived_approved_designs"] if x["id"]=="LT_CANON_BODY_REF_2026-10-28_V2")["id"])
        self.assertEqual(MAN["approved_expression_id"],EXP["expression_profile_id"])
        self.assertEqual(MAN["approved_expression_sha256"],EXP["source"]["sha256"])

    def test_exactly_five_candidate_reference_crops(self):
        self.assertEqual(MAN["expression_ids"],IDS)
        self.assertEqual([x["expression_id"] for x in MAN["candidate_pieces"]],IDS)
        self.assertEqual(len(set(x["sha256"] for x in MAN["candidate_pieces"])),5)
        w,h=MAN["cp334_generated_sheet_dimensions"]
        for x in MAN["candidate_pieces"]:
            left,top,right,bottom=x["source_box_xyxy"]
            self.assertTrue(0<=left<right<=w and 0<=top<bottom<=h)
            self.assertEqual(x["size_px"],[right-left,bottom-top])
            self.assertEqual(len(x["sha256"]),64)

    def test_poster_is_not_sprite_art(self):
        self.assertEqual(MAN["status"],"VISUAL_CONCEPT_REVIEW_PENDING_ART_ACCEPTANCE")
        self.assertTrue(MAN["visual_review_workspace_is_not_sprite_rig"])
        self.assertNotEqual(MAN["cp334_generated_flat_sheet_sha256"],MAN["canonical_sha256"])
        self.assertNotEqual(MAN["cp334_generated_flat_sheet_sha256"],MAN["approved_expression_sha256"])
        for key in (
            "new_portrait_style_artist_approved",
            "single_native_face_master_across_five",
            "clean_independent_facial_attachments",
            "clean_underpaint_verified",
            "front_three_quarter_production_art",
            "spine_rig_verified",
            "apk_built_tested"
        ):
            self.assertIs(MAN["qa_gates"][key],False,key)
        self.assertEqual(MAN["qa_gates"]["android_sprite_paths_registered"],0)

    def test_explicit_not_production_statement(self):
        self.assertIn("NOT actual face layers",MAN["warning"])
        self.assertTrue(MAN["qa_gates"]["canon_body_unchanged"])
        self.assertTrue(MAN["qa_gates"]["five_emotion_directions_unchanged"])


if __name__=="__main__":
    unittest.main()

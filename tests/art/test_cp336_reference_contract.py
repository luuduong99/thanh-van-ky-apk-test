"""CP336 manifest/approved-reference contract (no private binary refs on CI)."""
import json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
REF=json.loads((ART/"LAM_THIEN_CP336_SOURCE_MASTER_MANIFEST.json").read_text(encoding="utf-8"))
MODEL=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2.json").read_text(encoding="utf-8"))
EXPR=json.loads((ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json").read_text(encoding="utf-8"))
REG=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
PROFILE=json.loads((ROOT/"app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))
EXPECTED=["shy","angry","pain","embarrassed","alluring"]

class CP336SourceContract(unittest.TestCase):
    def test_canon_and_emotions_still_approved_source(self):
        self.assertEqual(REF["canonical_visual_id"],MODEL["canonical_visual_id"])
        self.assertEqual(REF["canonical_sha256"],MODEL["source"]["sha256"])
        self.assertEqual(REF["canonical_visual_id"],REG["latest_user_approved_design"]["id"])
        self.assertEqual(REF["approved_expression_profile"],EXPR["expression_profile_id"])
        self.assertEqual(REF["approved_expression_sha256"],EXPR["source"]["sha256"])

    def test_face_native_pixels_truthfully_reported(self):
        self.assertEqual(REF["canonical_original_size_px"],[1672,941])
        self.assertEqual([x["id"] for x in REF["source_angle_crops"]],
                         ["front","three_quarter","closeup"])
        for x in REF["source_angle_crops"]:
            x0,y0,x1,y1=x["source_box_xyxy"]
            self.assertEqual(x["native_size_px"],[x1-x0,y1-y0])
            self.assertLess(max(x["native_size_px"]),512)

    def test_approved_five_expression_reference_crops(self):
        self.assertEqual([x["id"] for x in REF["emotion_crops"]],EXPECTED)
        self.assertEqual(len(set(x["sha256"] for x in REF["emotion_crops"])),5)
        for crop in REF["emotion_crops"]:
            self.assertEqual(len(crop["sha256"]),64)

    def test_do_not_claim_production_art_or_rig(self):
        for key in ["native_high_res_front_face_master_ready",
                    "native_high_res_three_quarter_face_master_ready",
                    "clean_underpaint_completed",
                    "five_expressions_semantic_layers_completed",
                    "spine_verified","apk_verified",
                    "real_ora_psd_source_recovered",
                    "new_flat_cp336_candidate_approved",
                    "renderer_layered_animation_integrated"]:
            self.assertIs(REF[key],False,key)
        self.assertEqual(REF["sprite_paths_registered"],0)
        self.assertEqual(REF["real_production_png_layers_created"],0)

    def test_production_face_sprite_stays_locked_in_android(self):
        characters={c["id"]:c for c in PROFILE["characters"]}
        lam=characters["lin_qian"]
        self.assertEqual([x["id"] for x in lam["approved_expressions"]],EXPECTED)
        self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
        self.assertFalse(lam["production_release"]["artist_qa_passed"])
        self.assertEqual(lam["sprite_paths"],{})
        self.assertEqual(characters["to_nguyet_ly"]["approval_status"],"individual_preview_required")
        self.assertEqual(characters["to_nguyet_ly"]["sprite_paths"],{})

if __name__=="__main__":unittest.main()

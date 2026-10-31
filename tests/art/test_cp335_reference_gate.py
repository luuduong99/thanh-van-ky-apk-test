"""CP335 review-only candidate cannot overwrite approved source or become game sprite."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
REF=json.loads((ART/"LAM_THIEN_CP335_VISUAL_GATE_MANIFEST.json").read_text(encoding="utf-8"))
MODEL=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2.json").read_text(encoding="utf-8"))
APPROVED=json.loads((ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json").read_text(encoding="utf-8"))
REG=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text(encoding="utf-8"))
ASSET=json.loads((ROOT/"app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))

class CP335ReferenceContract(unittest.TestCase):
    def test_canonical_body_and_emotion_references_are_unchanged(self):
        self.assertEqual(REF["canonical_body_sha256"],MODEL["source"]["sha256"])
        self.assertEqual(REF["approved_emotions_sha256"],APPROVED["source"]["sha256"])
        self.assertEqual(next(x for x in REG["archived_approved_designs"] if x["id"]=="LT_CANON_BODY_REF_2026-10-28_V2")["id"],MODEL["canonical_visual_id"])
        self.assertEqual(REG["approved_expression_profile"]["id"],APPROVED["expression_profile_id"])

    def test_cp335_sheet_is_a_draft_not_rig(self):
        self.assertEqual(REF["status"],"visual_candidate_only_not_approved")
        self.assertFalse(REF["candidate_has_actual_rig_layers"])
        self.assertFalse(REF["candidate_art_user_approved"])
        self.assertNotEqual(REF["new_flat_candidate_sha256"],REF["canonical_body_sha256"])
        self.assertNotEqual(REF["new_flat_candidate_sha256"],REF["approved_emotions_sha256"])
        self.assertEqual(REF["candidate_dimensions"],[1536,1024])
        self.assertEqual(len(REF["source_crop_boxes_xyxy"]),5)

    def test_sprite_release_is_explicitly_blocked_even_for_approved_lam_thien_expressions(self):
        chars={c["id"]:c for c in ASSET["characters"]}
        lam=chars["lin_qian"]
        self.assertEqual(lam["approval_status"],"explicit_user_approved_expression_preview")
        self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
        self.assertFalse(lam["production_release"]["artist_qa_passed"])
        self.assertFalse(lam["production_release"]["runtime_qa_passed"])
        self.assertIsNone(lam["production_release"]["user_asset_approval_id"])
        self.assertEqual(lam["sprite_paths"],{})
        self.assertEqual(lam["expression_preview_sha256"],APPROVED["source"]["sha256"])
        # CP335's V2 expression-reference archive stays immutable, but new
        # runtime sprite release must follow the subsequently approved V2.1.
        self.assertEqual(lam["canonical_body_visual_id"], REG["latest_user_approved_design"]["id"])
        self.assertEqual(lam["canonical_body_sha256"],REG["latest_user_approved_design"]["visual_reference_sha256"])
        self.assertEqual(lam["archived_body_release_metadata"]["sha256"],MODEL["source"]["sha256"])

    def test_other_character_is_not_auto_approved(self):
        ly=next(c for c in ASSET["characters"] if c["id"]=="to_nguyet_ly")
        self.assertEqual(ly["approval_status"],"individual_preview_required")
        self.assertEqual(ly["sprite_paths"],{})
        self.assertEqual(ly["production_release"]["status"],"blocked_pending_art")

if __name__=="__main__":
    unittest.main()

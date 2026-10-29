"""CP338: exact V2 reference IDs and safe fringe-trim boundaries (metadata only)."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
MAN=json.loads((ART/"LAM_THIEN_CP338_CANON_TRIM_MANIFEST.json").read_text(encoding="utf-8"))
MODEL=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2.json").read_text(encoding="utf-8"))
EXP=json.loads((ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json").read_text(encoding="utf-8"))
PROFILES=json.loads((ROOT/"app/src/main/assets/character_expression_profiles.json").read_text(encoding="utf-8"))

class CP338CanonTrimContract(unittest.TestCase):
    def test_source_bodies_are_immutable(self):
        self.assertEqual(MAN["canonical_visual_id"],MODEL["canonical_visual_id"])
        self.assertEqual(MAN["canonical_sha256"],MODEL["source"]["sha256"])
        self.assertEqual(MAN["approved_expression_profile"],EXP["expression_profile_id"])
        self.assertEqual(MAN["approved_expression_sha256"],EXP["source"]["sha256"])
        self.assertEqual(MAN["body_percent_adjustment_already_in_canon"],17)
    def test_all_references_keep_native_dimensions_and_sha(self):
        self.assertEqual(MAN["native_reference_png_count"],22)
        self.assertEqual(len(MAN["references"]),22)
        self.assertEqual(len({i["id"] for i in MAN["references"]}),22)
        self.assertEqual(len([i for i in MAN["references"] if i["category"]=="emotion"]),5)
        self.assertTrue(all(len(i["sha256"])==64 for i in MAN["references"]))
        self.assertTrue(all(i["native_px"][0]>0 and i["native_px"][1]>0 for i in MAN["references"]))
    def test_only_minor_tassels_can_be_removed(self):
        trim=MAN["costume_detail_simplification"]
        self.assertEqual(trim["status"],"allowed_conditionally_no_modification_committed")
        self.assertGreater(len(trim["trim_allowed_only_if_minor"]),0)
        self.assertTrue(any("coverage" in v for v in trim["do_not_trim"]))
        self.assertTrue(any("flowers" in v or "flower" in v for v in trim["do_not_trim"]))
        self.assertEqual(trim["qa_decisions"],["PASS","PASS_WITH_MINOR_NOTES","REVISE"])
    def test_no_false_production_release(self):
        self.assertTrue(MAN["not_production_art"])
        for key in ["production_face_master_ready","semantic_face_sprites_ready","spine_verified","apk_verified"]:
            self.assertFalse(MAN[key])
        self.assertEqual(MAN["sprite_paths_registered"],0)
        lam=next(x for x in PROFILES["characters"] if x["id"]=="lin_qian")
        self.assertEqual(lam["production_release"]["status"],"blocked_pending_art")
        self.assertEqual(lam["sprite_paths"],{})
        self.assertEqual(MAN["garment_integrity_states"],[100,70,50,30])

if __name__=="__main__":unittest.main()

"""CP328 safeguards: V2 iris color and user-approved expression direction stay locked.

Synthetic CI checks only. The 230x114 approved V2 crop and artist binaries
live outside GitHub; local full-source SHA/pixel audit is separately recorded.
"""
import importlib.util
import json
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
MODULE=ROOT/"tools/cp328/cp328_face_color_gate.py"
spec=importlib.util.spec_from_file_location("cp328_gate",MODULE)
cp=importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
MANIFEST=ROOT/"docs/art/LAM_THIEN_CP328_FACE_MASTER_GATE.json"
MODEL=ROOT/"docs/art/LAM_THIEN_MODEL_CARD_V2.json"
EXP=ROOT/"docs/art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json"
EXPECTED=["shy","angry","pain","embarrassed","alluring"]

class CP328ColorGateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.model=json.loads(MODEL.read_text(encoding="utf-8"))
        cls.approved=json.loads(EXP.read_text(encoding="utf-8"))

    def test_canon_sha_and_approved_expression_direction_remain_immutable(self):
        a=self.manifest
        self.assertEqual(a["canonical_body_visual_id"],self.model["canonical_visual_id"])
        self.assertEqual(a["canonical_body_sha256"],cp.CANON_SHA)
        self.assertEqual(a["canonical_body_sha256"],self.model["source"]["sha256"])
        self.assertEqual(a["approved_expression_sha256"],self.approved["source"]["sha256"])
        self.assertEqual(a["approved_expression_sha256"],cp.EMOTION_SHA)
        self.assertEqual(a["approved_expression_ids"],EXPECTED)

    def test_production_art_is_still_unapproved(self):
        a=self.manifest
        for key in ("new_generated_cp328_illustrations_approved",
                    "production_high_resolution_face_master_ready",
                    "clean_underpaint_artist_approved",
                    "five_expression_independent_face_sprites_ready",
                    "spine_animation_verified","android_apk_verified"):
            self.assertIs(a[key],False,key)
        self.assertEqual(a["registered_android_asset_paths"],0)

    def test_native_source_dimensions_not_misrepresented(self):
        a=self.manifest
        self.assertEqual(a["native_face_size_px"],[230,114])
        self.assertEqual(a["source_roi_original_poster_xyxy"],[1160,0,1390,114])
        self.assertEqual(a["v2_iris_color_audit"]["native_crop_px"],[230,114])
        self.assertTrue(all(v["heuristic_pass"] for v in a["v2_iris_color_audit"]["eyes"]))

    def test_blue_iris_candidate_fails_even_when_other_iris_is_amber(self):
        img=Image.new("RGB",(512,512),(242,224,211))
        draw=ImageDraw.Draw(img)
        draw.rectangle((70,90,110,130),fill=(207,128,55))
        draw.rectangle((350,90,390,130),fill=(44,121,231))
        report=cp.evaluate_candidate_iris_patches(img,{
            "left_iris":[70,90,110,130],"right_iris":[350,90,390,130]})
        self.assertEqual(report["status"],"heuristic_fail")

    def test_artists_must_annotate_both_irises(self):
        img=Image.new("RGB",(512,512))
        with self.assertRaises(ValueError):
            cp.evaluate_candidate_iris_patches(img,{"left_iris":[70,90,110,130]})

    def test_amber_candidate_with_two_annotated_irises_passes_heuristic(self):
        img=Image.new("RGB",(512,512),(242,224,211))
        draw=ImageDraw.Draw(img)
        for a in [(70,90,110,130),(350,90,390,130)]:
            draw.rectangle(a,fill=(206,128,52))
        report=cp.evaluate_candidate_iris_patches(img,{
            "left_iris":[70,90,110,130],"right_iris":[350,90,390,130]})
        self.assertEqual(report["status"],"heuristic_pass")

if __name__=="__main__":unittest.main()

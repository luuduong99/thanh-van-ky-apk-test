"""CP330 GitHub metadata & synthetic painting-gate tests.

The real ORA binary files remain Library-backed. Passing CI must never
promote the five *new unapproved* candidates to canonical art or Spine.
"""
import importlib.util
import json
import unittest
from pathlib import Path
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/"docs/art"
SPEC=importlib.util.spec_from_file_location("cp330_paint",ROOT/"tools/cp330/build_cp330.py")
cp=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(cp)
MAN=json.loads((ART/"LAM_THIEN_CP330_ART_TRIAL_MANIFEST.json").read_text())
PACKAGE=json.loads((ART/"LAM_THIEN_CP330_PACKAGE_MANIFEST.json").read_text())
MODEL=json.loads((ART/"LAM_THIEN_MODEL_CARD_V2.json").read_text())
APPROVED=json.loads((ART/"LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json").read_text())
REGISTRY=json.loads((ART/"LAM_THIEN_DESIGN_REGISTRY.json").read_text())

class CP330TechnicalContractTests(unittest.TestCase):
    def test_canonical_sources_unchanged(self):
        self.assertEqual(MAN["canonical_visual_id"],MODEL["canonical_visual_id"])
        self.assertEqual(MAN["canonical_sha256"],MODEL["source"]["sha256"])
        self.assertEqual(MAN["approved_expression_profile"],APPROVED["expression_profile_id"])
        self.assertEqual(MAN["approved_expression_sha256"],APPROVED["source"]["sha256"])

    def test_new_generated_candidate_is_not_approved_canon(self):
        self.assertNotEqual(MAN["source_unapproved_generated_sheet_sha256"],MAN["canonical_sha256"])
        self.assertNotEqual(MAN["source_unapproved_generated_sheet_sha256"],MAN["approved_expression_sha256"])
        self.assertEqual(MAN["status"],"candidate_flat_art_decomposed_technical_only_NOT_CANON")
        self.assertFalse(MAN["production_asset_allowed"])
        self.assertFalse(MAN["same_canonical_face_master"])

    def test_all_five_candidate_expressions_and_native_resolution(self):
        self.assertEqual([r["expression_id"] for r in MAN["results"]],list(cp.NAMES))
        self.assertEqual(sum(r["independent_alpha_layers"] for r in MAN["results"]),35)
        for result in MAN["results"]:
            w,h=result["native_dimensions_px"]
            self.assertTrue(250<=w<=261 and h==370)
            self.assertTrue(result["default_composite_pixel_exact"])
            self.assertTrue(result["shift_test_no_alpha_holes"])
            self.assertEqual(result["underpaint"],"cv2_telea_auto_not_approved")

    def test_no_premature_game_or_spine_registration(self):
        self.assertFalse(PACKAGE["spine_ready"])
        self.assertFalse(PACKAGE["apk_ready"])
        self.assertFalse(PACKAGE["clean_artist_underpaint"])
        self.assertEqual(PACKAGE["sprite_paths_registered"],0)
        self.assertEqual(REGISTRY["approved_expression_profile"]["id"],MAN["approved_expression_profile"])
        self.assertEqual(next(x for x in REGISTRY["archived_approved_designs"] if x["id"]=="LT_CANON_BODY_REF_2026-10-28_V2")["id"],MAN["canonical_visual_id"])

    def test_source_reference_does_not_claim_original_high_resolution(self):
        self.assertFalse(PACKAGE["art_native_resolution_adequate"])
        self.assertFalse(PACKAGE["art_is_shared_face_master"])
        self.assertFalse(MAN["new_artist_redraw_complete"])
        self.assertTrue(MAN["art_preview_needs_review"])

    def test_masks_exactly_seven_and_nonoverlapping(self):
        for entry in MAN["results"]:
            m,union=cp.create_masks(tuple(entry["native_dimensions_px"]),entry["region_bounds"])
            self.assertEqual(set(m),set(cp.PARTS))
            occupied=Image.new("L",union.size)
            for mask in m.values():
                self.assertIsNotNone(mask.getbbox())
                self.assertIsNone(ImageChops.multiply(occupied,mask).getbbox())
                occupied=ImageChops.lighter(occupied,mask)
            self.assertIsNone(ImageChops.difference(occupied,union).getbbox())

    def test_synthetic_roundtrip_decomposes_without_double_painted_pixels(self):
        im=Image.new("RGB",(250,370),(205,134,61))
        m,union=cp.create_masks(im.size,MAN["results"][0]["region_bounds"])
        face=im.convert("RGBA");face.putalpha(ImageChops.invert(union))
        parts=[cp.rgba_from_mask(im,m[p]) for p in cp.PARTS]
        composite=cp.compose([im.convert("RGBA"),face]+parts,im.size)
        self.assertIsNone(ImageChops.difference(composite.convert("RGB"),im).getbbox())

if __name__=="__main__":
    unittest.main()

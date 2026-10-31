"""CP327: CI contract checks do not require Library-backed ORA binaries.

The real byte-exact image comparison is performed separately using
tools/cp327/validate_cp327_atlas.py with the CP326 ORA source files.
"""
import json
import unittest
from pathlib import Path
from PIL import Image
from tools.cp327.export_cp327_atlas import layout_atlas, PARTS, EXPRESSIONS

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/art/LAM_THIEN_CP327_ART_GATE_MANIFEST.json"
ATLAS = ROOT / "docs/art/LAM_THIEN_CP327_TECH_ATLAS.json"
APPROVED = ROOT / "docs/art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json"
MODEL = ROOT / "docs/art/LAM_THIEN_MODEL_CARD_V2.json"

class CP327ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gate=json.loads(DOC.read_text(encoding="utf-8"))
        cls.atlas=json.loads(ATLAS.read_text(encoding="utf-8"))
        cls.approved=json.loads(APPROVED.read_text(encoding="utf-8"))
        cls.model=json.loads(MODEL.read_text(encoding="utf-8"))

    def test_immutable_visual_references(self):
        d=self.gate
        self.assertEqual(d["canonical_body_visual_id"],self.model["canonical_visual_id"])
        self.assertEqual(d["canonical_body_source_sha256"],self.model["source"]["sha256"])
        self.assertEqual(d["approved_expression_profile_id"],self.approved["expression_profile_id"])
        self.assertEqual(d["approved_expression_sheet_sha256"],self.approved["source"]["sha256"])

    def test_atlas_exactly_35_valid_regions(self):
        a=self.atlas
        self.assertEqual(a["regions_count"],35)
        self.assertEqual(len(a["regions"]),35)
        self.assertEqual(set(r["expression"] for r in a["regions"]),set(EXPRESSIONS))
        for expression in EXPRESSIONS:
            slots={r["slot"] for r in a["regions"] if r["expression"]==expression}
            self.assertEqual(slots,set(PARTS))

    def test_overlaps_outside_canvas_are_forbidden(self):
        regions=self.atlas["regions"]
        bbox=[]
        for r in regions:
            x,y,w,h=r["atlas_rect_xywh"]
            self.assertTrue(0<=x and 0<=y and w>0 and h>0)
            self.assertLessEqual(x+w,2048);self.assertLessEqual(y+h,2048)
            bbox.append((x,y,x+w,y+h))
        for i,a in enumerate(bbox):
            for b in bbox[i+1:]:
                self.assertFalse(a[0]<b[2] and b[0]<a[2] and
                                 a[1]<b[3] and b[1]<a[3])

    def test_atlas_sha_matches_manifest(self):
        self.assertEqual(self.gate["atlas_sha256"],self.atlas["atlas_sha256"])
        self.assertEqual(self.gate["atlas_resolution_px"],[2048,2048])
        self.assertTrue(self.gate["pixel_exact_vs_source_oras"])

    def test_never_promote_draft_to_production(self):
        d=self.gate;a=self.atlas
        for key in ("artist_approved_high_resolution_face","production_sprite_accepted",
                    "spine_rig_verified","android_apk_verified","eligible_for_android_asset_registration"):
            self.assertIs(d[key],False)
        for key in ("production_ready","spine_ready","android_asset_registration_allowed"):
            self.assertIs(a[key],False)

    def test_synthetic_atlas_packer_is_deterministic_and_safe(self):
        items=[{"id":str(i),"image":Image.new("RGBA",(25+i*4,17+i*5))}
               for i in range(18)]
        a=layout_atlas(items,size=512)
        b=layout_atlas([{"id":str(i),"image":Image.new("RGBA",(25+i*4,17+i*5))}
                       for i in range(18)],size=512)
        self.assertEqual([(i["id"],i["atlas_origin"]) for i in a],
                         [(i["id"],i["atlas_origin"]) for i in b])

if __name__=="__main__":
    unittest.main()

"""CP332 CI: contract and independent vector SVG rendering.

Actual six OpenRaster binaries are in ChatGPT Library; their compositing and
CRC are verified by local binary tests, NOT the GitHub workflow.
"""
import importlib.util
import json
import unittest
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location("cp332",ROOT/"tools/cp332/build_cp332.py")
cp=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cp)
MAN=json.loads((ROOT/"docs/art/LAM_THIEN_CP332_SEMANTIC_STUDY_MANIFEST.json").read_text())
MODEL=json.loads((ROOT/"docs/art/LAM_THIEN_MODEL_CARD_V2.json").read_text())
EXP=json.loads((ROOT/"docs/art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json").read_text())
REG=json.loads((ROOT/"docs/art/LAM_THIEN_DESIGN_REGISTRY.json").read_text())

class CP332SemanticFaceTests(unittest.TestCase):
    def test_canon_and_user_approved_expression_unchanged(self):
        self.assertEqual(MAN["canonical_visual_id"],MODEL["canonical_visual_id"])
        self.assertEqual(MAN["canonical_source_sha256"],MODEL["source"]["sha256"])
        self.assertEqual(MAN["approved_expression_profile_id"],EXP["expression_profile_id"])
        self.assertEqual(MAN["approved_expression_source_sha256"],EXP["source"]["sha256"])
        self.assertEqual(next(x for x in REG["archived_approved_designs"] if x["id"]=="LT_CANON_BODY_REF_2026-10-28_V2")["id"],MODEL["canonical_visual_id"])

    def test_five_emotions_thirteen_parts_each(self):
        ids=["shy","angry","pain","embarrassed","alluring"]
        self.assertEqual([e["id"] for e in MAN["emotions"]],ids)
        self.assertEqual(cp.EMOTIONS,ids)
        self.assertEqual(len(MAN["base_layer_names"]),10)
        self.assertEqual(MAN["base_layer_names"],cp.BASE_SLOTS)
        self.assertEqual(MAN["semantic_expression_layers"],cp.FACE_SLOTS)
        self.assertEqual(MAN["total_independent_emotion_slots"],65)
        for e in MAN["emotions"]:
            self.assertEqual(set(e["slots"]),set(cp.FACE_SLOTS))
            for part in e["slots"].values():
                self.assertGreater(part["alpha_nonzero_px"],0)

    def test_clean_underpaint_has_no_baked_eyes_or_lips(self):
        self.assertIs(MAN["base_baked_eyes_brows_mouth"],False)
        self.assertFalse(any(k in cp.base_art() for k in ("iris_left","mouth","eye_white_left","eyelashes_left")))
        # Actual SVG: skin is a standalone anatomical shape, without face crops.
        skin=cp.render_svg(cp.base_art()["face_underpaint"])
        self.assertEqual(skin.mode,"RGBA")
        for xy in ((417,503),(607,503),(510,638)):
            self.assertGreaterEqual(skin.getchannel("A").getpixel(xy),240)

    def test_face_slots_render_independently_with_alpha(self):
        parts=cp.expression_art("shy")
        self.assertEqual(set(parts),set(cp.FACE_SLOTS))
        for key in cp.FACE_SLOTS:
            im=cp.render_svg(parts[key])
            self.assertEqual(im.mode,"RGBA")
            self.assertIsNotNone(im.getchannel("A").getbbox())

    def test_amber_iris_palette_and_identity_not_copied_from_flat_source(self):
        self.assertEqual(cp.AMBER,"#d58b35")
        self.assertEqual(MAN["iris_color_reference"],"amber_not_blue")
        self.assertIs(MAN["pixel_sources_cut_from_flat_posters"],False)
        self.assertEqual(MAN["vector_native_canvas"],[1024,1024])

    def test_art_still_unapproved_unregistered_and_not_rigged(self):
        for key in ("asset_registration_allowed","production_face_master_approved",
                    "production_face_sprites_approved","spine_rig_complete","apk_verified"):
            self.assertIs(MAN[key],False,key)
        self.assertTrue(MAN["requires_artist_visual_approval"])
        self.assertFalse(MAN["side_three_quarter_completed"])

if __name__=="__main__":
    unittest.main()

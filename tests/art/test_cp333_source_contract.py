"""CP333 source-only CI: protects approved identities and nonproduction state.

Does not replace byte-level QA of Library-backed 6 ORA binaries.
"""
import json, unittest
from pathlib import Path
import cairosvg
from PIL import Image
import io
from tools.cp333 import build_cp333 as cp

ROOT=Path(__file__).resolve().parents[2]
MAN=ROOT/'docs/art/LAM_THIEN_CP333_ART_HANDOFF_MANIFEST.json'
MODEL=ROOT/'docs/art/LAM_THIEN_MODEL_CARD_V2.json'
APPROVED=ROOT/'docs/art/LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json'

class CP333SourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.man=json.loads(MAN.read_text());cls.model=json.loads(MODEL.read_text());cls.approved=json.loads(APPROVED.read_text())
 def test_canon_body_and_approved_face_emotions_locked(self):
  self.assertEqual(self.man['canonical_visual_id'],self.model['canonical_visual_id'])
  self.assertEqual(self.man['canonical_sha256'],self.model['source']['sha256'])
  self.assertEqual(self.man['approved_expression_profile_id'],self.approved['expression_profile_id'])
  self.assertEqual(self.man['approved_expression_sha256'],self.approved['source']['sha256'])
 def test_five_expression_ids_are_exact(self):
  self.assertEqual(self.man['approved_emotions'],['shy','angry','pain','embarrassed','alluring'])
 def test_semantic_slot_count_unchanged(self):
  self.assertEqual(len(cp.base.BASE_SLOTS),10)
  self.assertEqual(len(cp.base.FACE_SLOTS),13)
  self.assertEqual(self.man['face_layer_count_total'],65)
 def test_genuine_vector_edits_were_made(self):
  for part in ('hair_front','flower_gold','face_underpaint'):
   self.assertNotEqual(cp.BASE_ORIGINAL()[part],cp.base_art_refined()[part])
  for part in ('iris_left','eyelashes_left','mouth','brow_right'):
   self.assertNotEqual(cp.EXPR_ORIGINAL('shy')[part],cp.expression_refined('shy')[part])
 def test_skin_base_does_not_bake_eye_or_mouth_layers(self):
  base=cp.base_art_refined()
  self.assertEqual(set(base),set(cp.base.BASE_SLOTS))
  self.assertNotIn('iris_left',base)
  self.assertFalse(self.man['underpaint_has_baked_face_features'])
 def test_each_svg_attachment_is_alpha_and_nonempty(self):
  for eid in cp.base.EMOTIONS:
   parts=cp.expression_refined(eid)
   self.assertEqual(set(parts),set(cp.base.FACE_SLOTS))
   for k in ('iris_left','brow_left','mouth'):
    im=cp.base.render_svg(parts[k])
    self.assertEqual(im.mode,'RGBA');self.assertIsNotNone(im.getchannel('A').getbbox())
 def test_iris_hue_is_warm_not_blue(self):
  import cv2,numpy as np
  im=np.array(cp.base.render_svg(cp.expression_refined('shy')['iris_left']))
  hsv=cv2.cvtColor(im[:,:,:3],cv2.COLOR_RGB2HSV)
  mask=im[:,:,3]>160
  amber=np.count_nonzero(mask&(hsv[:,:,0]>=5)&(hsv[:,:,0]<=30)&(hsv[:,:,1]>=50))
  blue=np.count_nonzero(mask&(hsv[:,:,0]>=80)&(hsv[:,:,0]<=135)&(hsv[:,:,1]>=75))
  self.assertGreater(amber,100);self.assertLess(blue,amber//20)
 def test_production_eligibility_must_remain_false(self):
  for key in ('new_production_face_master_ready','spine_ready','apk_ready'):
   self.assertIs(self.man[key],False)
  self.assertEqual(self.man['registered_game_sprites'],0)
  self.assertEqual(self.man['status'],'VECTOR_LAYER_DETAIL_RND_NOT_APPROVED')
 def test_inherited_approved_reference_files_are_not_modified(self):
  self.assertEqual(self.man['canonical_visual_id'],'LT_CANON_BODY_REF_2026-10-28_V2')
  self.assertTrue(self.man['visual_art_is_NOT_same_as_CANON_V2'])

if __name__=='__main__':unittest.main()
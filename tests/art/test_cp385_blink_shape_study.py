"""CP385 source-locked tests. Private CANON required for visual-source tests.
A test pass never implies artist review, rig or game release.
"""
from pathlib import Path
import tempfile, importlib.util, json, unittest, zipfile, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
MODULE=HERE/'cp385_blink_shape_study.py'
if not MODULE.exists(): MODULE=HERE.parents[1]/'tools'/'art'/'cp385_blink_shape_study.py'
spec=importlib.util.spec_from_file_location('cp385_blink',MODULE)
cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)
DATA=HERE/'previous'/'OUTPUT'
CANON=DATA/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
OLD=DATA/'art_layers'/'00_technical_inpaint_underpaint_NOT_APPROVED.png'
HAVE_ASSETS=CANON.exists() and OLD.exists()

class StaticContracts(unittest.TestCase):
 def test_canonic_source_metadata(self):
  self.assertEqual(cp.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
  self.assertEqual(cp.SIZE,(168,197))
  self.assertEqual(cp.BBOX,(25,684,193,881))
 def test_separate_lid_geometry_and_no_spine_claim(self):
  self.assertNotEqual(cp.EYES['left_eye'],cp.EYES['right_eye'])
  for side in ['left','right']:
   self.assertIsNotNone(cp.lid_layer(side,1).getchannel('A').getbbox())
 def test_must_not_auto_approve_blink(self):
  code=MODULE.read_text()
  self.assertIn("'visual_qa':'NOT_PASSED'",code)
  self.assertIn("'production_release':'blocked_pending_art'",code)

@unittest.skipUnless(HAVE_ASSETS,'Exact private source not checked into GitHub')
class PrivateSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory()
  cls.root=Path(cls.tmp.name)/'out'
  cls.report=cp.make(CANON,OLD,cls.root)
  cls.source=Image.open(cls.root/'source'/'SHY_CANON_168x197_EXACT.png').convert('RGBA')
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_static_recomposition_is_exact(self):
  target=Image.open(self.root/'CP385_CANON_PIXEL_EXACT_STATIC_FACE.png')
  self.assertTrue(np.array_equal(np.asarray(target),np.asarray(self.source)))
 def test_eyebrow_outside_masks_untouched(self):
  self.assertEqual(self.report['new_changes_outside_eye_and_mouth_masks'],0)
 def test_five_frames_are_distinct_and_bookended_by_canon(self):
  frames=[np.asarray(Image.open(self.root/'frames'/f'CP385_BLINK_FRAME_{i:02}_DRAFT.png')) for i in range(5)]
  self.assertTrue(np.array_equal(frames[0],np.asarray(self.source)))
  self.assertTrue(np.array_equal(frames[4],np.asarray(self.source)))
  self.assertFalse(np.array_equal(frames[2],frames[0]))
  self.assertTrue(np.array_equal(frames[1],frames[3]))
 def test_ora_layers_crc_and_visible_source(self):
  with zipfile.ZipFile(self.root/'CP385_SHY_SOURCE_AND_BLINK_DRAFT_NOT_RIG.ora') as z:
   self.assertIsNone(z.testzip())
   root=ET.fromstring(z.read('stack.xml'))
   layers=list(root.find('stack'))
   self.assertEqual(len(layers),7)
   self.assertEqual(sum(layer.get('visibility')=='hidden' for layer in layers),3)
   merged=np.asarray(Image.open(z.open('mergedimage.png')).convert('RGBA'))
  self.assertTrue(np.array_equal(merged,np.asarray(self.source)))
 def test_no_unapproved_source_ships(self):
  r=self.report
  self.assertFalse(r['blink_artist_approved'])
  self.assertFalse(r['background_transparent'])
  self.assertEqual(r['production_release'],'blocked_pending_art')
  self.assertEqual(r['sprite_paths'],{})
  self.assertFalse(r['apk_ready'])
 def test_preserves_exact_canon_file_bytes(self):
  import hashlib
  self.assertEqual(hashlib.sha256((self.root/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes()).hexdigest(),cp.CANON_SHA)
 def test_wrong_source_has_no_side_effect(self):
  with tempfile.TemporaryDirectory() as tmp:
   wrong=Path(tmp)/'wrong.png';Image.new('RGBA',cp.CANON_SIZE,'white').save(wrong)
   output=Path(tmp)/'should_not_exist'
   with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
    cp.make(wrong,OLD,output)
   self.assertFalse(output.exists())

if __name__=='__main__':unittest.main()
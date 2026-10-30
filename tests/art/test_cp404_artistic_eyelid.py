"""CP404: technical checks do not constitute visual approval."""
import os, sys, json, zipfile, unittest, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cp404_artistic_eyelid as m

CANON=Path(os.getenv('TVK_CP404_CANON',''))
PREV=Path(os.getenv('TVK_CP404_PREV',''))
HAS_SOURCES=CANON.is_file() and PREV.is_file()

class StaticPolicy(unittest.TestCase):
 def test_canon_hash_pinned(self):self.assertEqual(m.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
 def test_crop_shape(self):self.assertEqual(m.SIZE,(168,197));self.assertEqual(m.base.CROP,(25,684,193,881))
 def test_roi_bounds_nonoverlap(self):
  a,b=m.ROIS.values();self.assertLess(a[2],b[0]);self.assertTrue(all(0<=p<=197 for p in (a[1],a[3],b[1],b[3])))
 def test_approved_release_never_auto_unlocked(self):
  s=Path(m.__file__).read_text();self.assertIn("'closed_eye_art_user_approved':False",s);self.assertIn("'production_sprite_paths':{}",s)
 def test_refuse_unknown_variant(self):
  with self.assertRaises(ValueError):m.compose_study(Image.new('RGBA',m.SIZE),'unexpected')

@unittest.skipUnless(HAS_SOURCES,'Private CANON and CP402 PNG not present in public CI')
class PrivateImageQA(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=m.base.exact_source(CANON);cls.prev=Image.open(PREV).convert('RGBA')
  cls.feather,cls.layers,cls.repaired,cls.mask=m.compose_study(cls.src,'feather')
  cls.defined,*_=m.compose_study(cls.src,'defined')
  cls.balanced=Image.blend(cls.prev,cls.defined,.32)
 def test_reference_exact_source(self):self.assertEqual(m.sha(CANON),m.SHA)
 def test_two_eye_only(self):
  for a in (self.feather,self.defined,self.balanced):self.assertEqual(m.base.valid_pixels_only(self.src,a),0)
 def test_draft_does_not_modify_alpha(self):
  aa=np.asarray(self.src)[:,:,3]
  for a in (self.feather,self.defined,self.balanced):np.testing.assert_array_equal(np.asarray(a)[:,:,3],aa)
 def test_local_skin_repaint(self):self.assertGreater(np.count_nonzero(self.mask),100)
 def test_layers_have_alpha(self):
  self.assertEqual(len(self.layers),4)
  for layer in self.layers.values():self.assertTrue(np.any(np.asarray(layer)[:,:,3]>0))
 def test_closure_changes_pixels(self):
  self.assertGreater(np.count_nonzero(np.any(np.asarray(self.feather)!=np.asarray(self.src),axis=2)),100)
 def test_same_frame_guards(self):
  for pos in [0,.15,.30,.6,.9,1]:
   im=m.base.eyelid_position(self.src,self.balanced,pos)
   self.assertEqual(m.base.valid_pixels_only(self.src,im),0)
  self.assertTrue(np.array_equal(np.asarray(self.src),np.asarray(m.base.eyelid_position(self.src,self.balanced,0))))
 def test_ora_only_source_visible(self):
  with tempfile.TemporaryDirectory() as t:
   dst=Path(t)/'art.ora';m.make_ora(self.src,self.balanced,self.prev,self.layers,self.repaired,dst)
   with zipfile.ZipFile(dst) as z:
    self.assertIsNone(z.testzip());root=ET.fromstring(z.read('stack.xml'));layers=root.findall('./stack/layer')
    self.assertEqual(len(layers),8)
    self.assertEqual(sum(v.get('visibility')=='visible' for v in layers),1)
    self.assertTrue(np.array_equal(np.asarray(Image.open(z.open('mergedimage.png'))),np.asarray(self.src)))
 def test_deterministic_candidates(self):
  x,*_=m.compose_study(self.src,'feather');np.testing.assert_array_equal(np.asarray(x),np.asarray(self.feather))
 def test_tampered_canon_fails(self):
  with tempfile.TemporaryDirectory() as t:
   fp=Path(t)/'changed.png';self.src.save(fp)
   with self.assertRaises(ValueError):m.base.exact_source(fp)

if __name__=='__main__':unittest.main()
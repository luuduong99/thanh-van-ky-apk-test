"""CP394 exact source QA. Public checkout intentionally skips private art checks."""
from __future__ import annotations
import io,os,sys,tempfile,unittest,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cp394_source_lash_underpaint as m
CANON=Path(os.getenv('TVK_CANON_PATH','/mnt/data/CP393/OUTPUT/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
PRIOR=Path(os.getenv('TVK_CP393_CLOSED_PATH','/mnt/data/CP393/OUTPUT/CP393_FULL_CLOSED_PAINT_STUDY_NOT_APPROVED.png'))
class PublicStatic(unittest.TestCase):
 def test_exact_locked_source(self):
  self.assertEqual(len(m.CANON_SHA),64);self.assertEqual(m.SIZE,(168,197));self.assertEqual(m.CROP,(25,684,193,881))
 def test_both_eyes_have_separate_geometry(self):
  self.assertEqual(set(m.ROIS),{'LEFT','RIGHT'});self.assertEqual(set(m.GEOM),set(m.ROIS))
  self.assertLess(m.ROIS['LEFT'][2],m.ROIS['RIGHT'][0])
 def test_explicit_art_gate(self):
  self.assertEqual(m.RELEASE['status'],'blocked_pending_art');self.assertEqual(m.RELEASE['sprite_paths'],{})
  self.assertFalse(m.RELEASE['apk_ready']);self.assertFalse(m.RELEASE['spine_ready'])
 def test_editable_layer_organization(self):
  for side in m.GEOM:
   self.assertEqual(set(m.GEOM[side]),{'upper','lower','lash'})
  self.assertTrue(callable(m.ora));self.assertTrue(callable(m.make_layers))
@unittest.skipUnless(CANON.is_file() and PRIOR.is_file(),'Private CANON and prior art are absent')
class PrivateExactSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=m.checked_canon(CANON);cls.layers={side:m.make_layers(cls.src,side) for side in m.ROIS}
  cls.closed=m.composite(cls.src,cls.layers,'closed');cls.soft=m.composite(cls.src,cls.layers,'soft')
 def test_exact_source_bytes(self):self.assertEqual(m.sha(CANON),m.CANON_SHA)
 def test_source_crop_exact(self):
  self.assertTrue(np.array_equal(np.asarray(Image.open(CANON).crop(m.CROP)),np.asarray(self.src)))
 def test_six_nonempty_layers(self):
  for side in m.ROIS:
   self.assertEqual(set(self.layers[side]),{'SKIN','CANON_LASH','CREASE'})
   for name,layer in self.layers[side].items():self.assertGreater(np.count_nonzero(np.asarray(layer)[:,:,3]),2,(side,name))
 def test_candidate_modifies_only_eye_roi(self):
  for target in (self.closed,self.soft):
   self.assertEqual(m.outside_changes(self.src,target),0)
   self.assertGreater(m.diff_count(self.src,target),300)
 def test_ora_has_only_original_visible(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'test.ora';self.assertEqual(m.ora(self.src,self.layers,self.closed,self.soft,p),10)
   with zipfile.ZipFile(p) as z:
    self.assertIsNone(z.testzip());root=ET.fromstring(z.read('stack.xml'));ls=list(root.find('stack'))
    self.assertEqual(len(ls),10);self.assertEqual(sum(x.attrib.get('visibility')=='visible' for x in ls),1)
    merged=Image.open(io.BytesIO(z.read('mergedimage.png')))
    self.assertTrue(np.array_equal(np.asarray(merged),np.asarray(self.src)))
 def test_wrong_sha_refuses_before_directory_created(self):
  with tempfile.TemporaryDirectory() as tmp:
   wrong=Path(tmp)/'wrong.png';out=Path(tmp)/'out';raw=bytearray(CANON.read_bytes());raw[100]^=1;wrong.write_bytes(raw)
   with self.assertRaises(ValueError):m.create(wrong,PRIOR,out)
   self.assertFalse(out.exists())
 def test_changes_have_real_eye_structure(self):
  for side in m.ROIS:
   a=np.asarray(self.layers[side]['CANON_LASH']);skin=np.asarray(self.layers[side]['SKIN'])
   self.assertGreater(np.count_nonzero(a[...,3]),20)
   self.assertGreater(np.count_nonzero(skin[...,3]),20)
if __name__=='__main__':unittest.main(verbosity=2)
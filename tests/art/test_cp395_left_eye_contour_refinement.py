"""CP395 exact CANON source tests; private-art tests intentionally SKIP in public GitHub."""
import io,os,sys,tempfile,unittest,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cp395_left_eye_contour_refinement as m
CANON=Path(os.getenv('TVK_CANON_PATH','/mnt/data/CP394/OUTPUT/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
PRIOR=Path(os.getenv('TVK_CP394_CLOSED_PATH','/mnt/data/CP394/OUTPUT/CP394_CLOSED_EYE_SOURCE_LASH_STUDY_NOT_APPROVED.png'))
class StaticPublicContract(unittest.TestCase):
 def test_source_lock(self):self.assertEqual(len(m.CANON_SHA),64);self.assertEqual(len(m.PREVIOUS_SHA),64)
 def test_native_size(self):self.assertEqual(m.SIZE,(168,197));self.assertEqual(m.CROP,(25,684,193,881))
 def test_release_guard(self):
  self.assertEqual(m.RELEASE['status'],'blocked_pending_art');self.assertEqual(m.RELEASE['sprite_paths'],{})
  self.assertFalse(m.RELEASE['apk_ready']);self.assertFalse(m.RELEASE['spine_ready'])
 def test_left_only_geometry(self):
  self.assertLess(m.LEFT_ROI[2],m.RIGHT_ROI[0]);self.assertTrue(callable(m.masks))
@unittest.skipUnless(CANON.is_file() and PRIOR.is_file(), 'Private source CANON / CP394 assets absent')
class PrivateSourceContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source,cls.previous=m.checked_inputs(CANON,PRIOR)
  cls.layers={v:m.masks(cls.source,v) for v in ('tight','soft')}
  cls.candidates={v:m.apply(cls.previous,cls.layers[v]) for v in cls.layers}
 def test_source_hash_and_dimensions(self):
  self.assertEqual(m.sha(CANON),m.CANON_SHA)
  self.assertEqual(m.sha(PRIOR),m.PREVIOUS_SHA)
  self.assertTrue(np.array_equal(np.asarray(Image.open(CANON).crop(m.CROP)),np.asarray(self.source)))
 def test_four_editable_layers_nonempty(self):
  for name,parts in self.layers.items():
   self.assertEqual(set(parts),{'SKIN_LOCAL','LASH_LOCAL'})
   for k,img in parts.items(): self.assertGreater(np.count_nonzero(np.asarray(img)[:,:,3]),10,(name,k))
 def test_no_modification_outside_left_eye(self):
  for target in self.candidates.values():
   self.assertEqual(m.left_only_change(self.previous,target),0)
   self.assertEqual(m.cp394.outside_changes(self.source,target),0)
 def test_both_drafts_independent(self):
  self.assertGreater(m.diff(self.candidates['tight'],self.candidates['soft']),20)
  for draft in self.candidates.values():self.assertGreater(m.diff(self.previous,draft),20)
 def test_original_visible_in_ora(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'eyes.ora';n=m.save_ora(self.source,self.previous,self.layers,self.candidates,p)
   self.assertEqual(n,9)
   with zipfile.ZipFile(p) as z:
    self.assertIsNone(z.testzip())
    root=ET.fromstring(z.read('stack.xml'))
    ls=list(root.find('stack'))
    self.assertEqual(len(ls),9)
    self.assertEqual(sum(l.attrib.get('visibility')=='visible' for l in ls),1)
    merged=np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png'))))
    self.assertTrue(np.array_equal(merged,np.asarray(self.source)))
 def test_tampered_canon_refused_before_output(self):
  with tempfile.TemporaryDirectory() as td:
   wrong=Path(td)/'tampered.png';out=Path(td)/'artifact'
   b=bytearray(CANON.read_bytes());b[123]^=1;wrong.write_bytes(b)
   with self.assertRaises(ValueError):m.build(wrong,PRIOR,out)
   self.assertFalse(out.exists())
 def test_wrong_previous_refused_before_output(self):
  with tempfile.TemporaryDirectory() as td:
   wrong=Path(td)/'wrong.png';out=Path(td)/'artifact'
   b=bytearray(PRIOR.read_bytes());b[75]^=1;wrong.write_bytes(b)
   with self.assertRaises(ValueError):m.build(CANON,wrong,out)
   self.assertFalse(out.exists())
if __name__=='__main__':unittest.main(verbosity=2)
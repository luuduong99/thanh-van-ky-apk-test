"""CP400 source-fidelity / export contract. Technical pass is NOT aesthetic approval."""
import os,sys,json,io,zipfile,tempfile,unittest
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cp400_blink_pipeline as m
CANON=Path(os.getenv('TVK_CANON_PATH','/mnt/data/tvk_cp396/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
PRIOR=Path(os.getenv('TVK_CP398_SOFT_PATH','/mnt/data/tvk_cp398/OUTPUT/CP398_CLOSED_EYE_SOFT_DRAFT_NOT_APPROVED.png'))
class StaticContract(unittest.TestCase):
 def test_lock(self):self.assertEqual(len(m.CANON_HASH),64);self.assertEqual(len(m.CP398_SOFT_SHA),64)
 def test_crop(self):self.assertEqual(m.CROP,(25,684,193,881));self.assertEqual(m.NATIVE,(168,197))
 def test_mask_bounds(self):
  for roi in m.ROIS.values(): self.assertTrue(0<=roi[0]<roi[2]<=m.NATIVE[0] and 0<=roi[1]<roi[3]<=m.NATIVE[1])
 def test_source_only_release(self):
  import inspect
  source=inspect.getsource(m.build)
  self.assertIn('CANON_SHA',inspect.getsource(m.load_canon))
  self.assertIn('CP398_SOFT_SHA',source)
  self.assertIn('PENDING_USER_APPROVAL',source)
  self.assertIn("'ready_for_apk':False",source)
@unittest.skipUnless(CANON.is_file() and PRIOR.is_file(),'private CANON and CP398 draft assets absent')
class PrivateExactArtTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=m.load_canon(CANON)
  if m.sha(PRIOR)!=m.CP398_SOFT_SHA:raise ValueError('PRIOR_SHA_BAD')
  cls.old=Image.open(PRIOR).convert('RGBA')
  cls.closed,cls.layers,_=m.paint_eyes(cls.src,cls.old)
  cls.frames=m.sequence(cls.src,cls.closed)
 def test_canon_sha_and_crop(self):
  self.assertEqual(m.sha(CANON),m.CANON_HASH)
  self.assertTrue(np.array_equal(np.asarray(Image.open(CANON).crop(m.CROP)),np.asarray(self.src)))
 def test_prior_source_hash(self):self.assertEqual(m.sha(PRIOR),m.CP398_SOFT_SHA)
 def test_art_layers_alpha_nonempty(self):
  self.assertEqual(set(self.layers),{'UNDERPAINT','SHADOW','CREASE','LASH','CANON_LASH_ROOT'})
  for img in self.layers.values(): self.assertGreater(np.count_nonzero(np.asarray(img)[:,:,3]),5)
 def test_outside_eye_pixel_exact(self):
  self.assertEqual(m.limit_check(self.src,self.closed),0)
  for frame in self.frames:self.assertEqual(m.limit_check(self.src,frame),0)
 def test_frames_count_dimensions(self):
  self.assertEqual(len(self.frames),9)
  for frame in self.frames:self.assertEqual(frame.size,m.NATIVE)
 def test_open_endpoints_exact(self):
  self.assertTrue(np.array_equal(np.asarray(self.src),np.asarray(self.frames[0])))
  self.assertTrue(np.array_equal(np.asarray(self.src),np.asarray(self.frames[-1])))
 def test_closed_really_differs(self):
  self.assertGreater(np.any(np.asarray(self.src)!=np.asarray(self.closed),axis=2).sum(),500)
  self.assertTrue(np.array_equal(np.asarray(self.closed),np.asarray(self.frames[4])))
 def test_ora_source_only_visible(self):
  with tempfile.TemporaryDirectory() as td:
   f=Path(td)/'eyes.ora';count=m.openraster(self.src,self.closed,self.layers,f)
   self.assertEqual(count,7)
   with zipfile.ZipFile(f) as z:
    self.assertIsNone(z.testzip())
    root=ET.fromstring(z.read('stack.xml'))
    names=list(root.find('stack'))
    self.assertEqual(sum(i.attrib['visibility']=='visible' for i in names),1)
    px=np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png'))))
    self.assertTrue(np.array_equal(px,np.asarray(self.src)))
 def test_tampered_sources_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   dst=Path(td)/'output';wrong=Path(td)/'wrong.png'
   a=bytearray(CANON.read_bytes());a[140]^=1;wrong.write_bytes(a)
   with self.assertRaises(ValueError):m.build(wrong,PRIOR,dst)
   self.assertFalse(dst.exists())
   a=bytearray(PRIOR.read_bytes());a[60]^=1;wrong.write_bytes(a)
   with self.assertRaises(ValueError):m.build(CANON,wrong,dst)
   self.assertFalse(dst.exists())
 def test_exports_gif_apng_atlas(self):
  with tempfile.TemporaryDirectory() as td:
   report=m.build(CANON,PRIOR,td)
   self.assertFalse(report['ready_for_apk'])
   self.assertEqual(report['changed_outside_eyes'],0)
   for name in ('CP400_BLINK_PREVIEW.gif','CP400_BLINK_PREVIEW.png'):
    with Image.open(Path(td)/name) as im:
     self.assertEqual(im.n_frames,9)
   with Image.open(Path(td)/'CP400_BLINK_FRAMES_ATLAS_DRAFT.png') as atlas:
    self.assertEqual(atlas.size,(9*168,197))
if __name__=='__main__':unittest.main(verbosity=2)
"""CP398 source-locked tests — technical pixel guarantees, not aesthetic acceptance."""
import os,sys,io,json,tempfile,unittest,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'/'art'))
import cp398_eyelid_refinement as m

CANON=Path(os.getenv('TVK_CANON_PATH','/mnt/data/tvk_cp396/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
PRIOR=Path(os.getenv('TVK_CP397_PATH','/mnt/data/tvk_cp397/OUTPUT/CP397_CLOSED_EYE_PAINT_STUDY_DRAFT_NOT_APPROVED.png'))
class PublicSourceGuard(unittest.TestCase):
 def test_canon_sha_lock_shape(self):self.assertEqual(len(m.CANON_SHA),64)
 def test_previous_sha_lock_shape(self):self.assertEqual(len(m.PREVIOUS_SHA),64)
 def test_eye_geometry_disjoint(self):self.assertLess(m.ROIS['LEFT'][2],m.ROIS['RIGHT'][0])
 def test_release_blocked(self):
  self.assertFalse(m.RELEASE['apk_ready']);self.assertFalse(m.RELEASE['spine_ready']);self.assertEqual(m.RELEASE['sprite_paths'],{})

@unittest.skipUnless(CANON.is_file() and PRIOR.is_file(), 'Private CANON/CP397 source files are intentionally not in public GitHub')
class Contract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source,cls.prior=m.checked(CANON,PRIOR)
  cls.layers={x:m.make_layers(cls.source,x) for x in ('natural','soft')}
  cls.images={k:m.make_candidate(cls.prior,v) for k,v in cls.layers.items()}
 def test_01_source_sha_exact(self):self.assertEqual(m.sha(CANON),m.CANON_SHA)
 def test_02_prior_sha_exact(self):self.assertEqual(m.sha(PRIOR),m.PREVIOUS_SHA)
 def test_03_crop_pixel_exact_native(self):
  with Image.open(CANON) as big:self.assertTrue(np.array_equal(np.asarray(big.crop(m.CROP)),np.asarray(self.source)))
  self.assertEqual(self.source.size,(168,197))
 def test_04_variants_both_differ_from_cp397(self):
  for pic in self.images.values():self.assertGreater(m.diff(self.prior,pic),30)
  self.assertGreater(m.diff(self.images['natural'],self.images['soft']),12)
 def test_05_only_exact_eyes_changed(self):
  for img in self.images.values():self.assertEqual(m.outside_diff(self.source,img),0)
 def test_06_eight_editable_layers_each_variant(self):
  for variant in self.layers.values():
   self.assertEqual(sum(map(len,variant.values())),8)
   for side,layer in variant.items():
    self.assertEqual(set(layer),{'SKIN_RETOUCH','LID_SHADOW','SKIN_HIGHLIGHT','FINE_LASH'})
    for kind,img in layer.items():self.assertGreater(np.count_nonzero(np.asarray(img)[:,:,3]),1,(side,kind))
 def test_07_all_mask_alpha_inside_correct_roi(self):
  for variant in self.layers.values():
   for side,parts in variant.items():
    x1,y1,x2,y2=m.ROIS[side]
    for im in parts.values():
     alpha=np.asarray(im)[:,:,3];mask=np.ones(alpha.shape,bool);mask[y1:y2,x1:x2]=False
     self.assertFalse(alpha[mask].any())
 def test_08_two_eye_rois_disjoint(self):
  x1,y1,x2,y2=m.ROIS['LEFT']; a,b,c,d=m.ROIS['RIGHT']
  self.assertLess(x2,a)
 def test_09_curves_in_roi(self):
  for side in m.ROIS:
   x1,y1,x2,y2=m.ROIS[side]
   for t in np.linspace(0,1,21):
    x,y=m.bez(m.LID[side],t)
    self.assertTrue(x1<=x<=x2 and y1<=y<=y2,(side,x,y))
 def test_10_ora_13_layers_single_canon_visible(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'o.ora';self.assertEqual(m.save_ora(self.source,self.prior,self.layers['natural'],self.images,path),13)
   with zipfile.ZipFile(path) as z:
    self.assertIsNone(z.testzip())
    root=ET.fromstring(z.read('stack.xml'));layers=list(root.find('stack'))
    self.assertEqual(len(layers),13)
    self.assertEqual(sum(x.attrib['visibility']=='visible' for x in layers),1)
    self.assertEqual(layers[0].attrib['visibility'],'visible')
    self.assertTrue(np.array_equal(np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png')))),np.asarray(self.source)))
 def test_11_tampered_canon_rejected_before_artifacts(self):
  with tempfile.TemporaryDirectory() as td:
   bad=Path(td)/'bad.png';bad.write_bytes(CANON.read_bytes()[:-77]);dest=Path(td)/'out'
   with self.assertRaises(ValueError):m.build(bad,PRIOR,dest)
   self.assertFalse(dest.exists())
 def test_12_tampered_prior_rejected_before_artifacts(self):
  with tempfile.TemporaryDirectory() as td:
   bad=Path(td)/'bad.png';bad.write_bytes(PRIOR.read_bytes()[:-77]);dest=Path(td)/'out'
   with self.assertRaises(ValueError):m.build(CANON,bad,dest)
   self.assertFalse(dest.exists())
 def test_13_release_remains_blocked(self):
  self.assertFalse(m.RELEASE['apk_ready']);self.assertFalse(m.RELEASE['spine_ready']);self.assertEqual(m.RELEASE['sprite_paths'],{})
 def test_14_output_source_sha_lock_and_qa(self):
  with tempfile.TemporaryDirectory() as td:
   result=m.build(CANON,PRIOR,Path(td)/'out')
   self.assertEqual(result['visual_qa'],'NOT_PASSED_PENDING_HUMAN_REVIEW')
   self.assertEqual(result['openraster_layers'],13)
   self.assertEqual(result['outside_eyes_changed_from_canon'],{'natural':0,'soft':0})
   self.assertEqual(m.sha(Path(td)/'out'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'),m.CANON_SHA)
 def test_15_source_exact_mergedimage_in_artifact(self):
  out=Path('/mnt/data/tvk_cp398/OUTPUT/CP398_CANON_EYELID_REFINEMENT_13_LAYER_NOT_APPROVED.ora')
  if not out.is_file():self.skipTest('Local generated artifact not present')
  with zipfile.ZipFile(out) as z:self.assertEqual(m.png(self.source),z.read('mergedimage.png'))

if __name__=='__main__':unittest.main(verbosity=2)
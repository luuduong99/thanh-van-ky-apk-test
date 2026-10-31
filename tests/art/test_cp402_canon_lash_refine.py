"""CP402 no-CANON-leak test suite. Tests source lock and ROI protection.
True art acceptance requires direct artist review; no green test is art QA.
"""
import hashlib, os, sys, unittest, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cp402_canon_lash_refine as m
import cp401_occlusion_blink as cp401

SOURCE = Path(os.getenv('TVK_CANON_V21','/mnt/data/tvk_cp396/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))

class StaticContract(unittest.TestCase):
 def test_locked_source_sha(self):self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
 def test_regions_inside_face(self):
  self.assertEqual(m.SIZE,(168,197))
  for a,b,c,d in m.ROIS.values():self.assertTrue(0<=a<c<=168 and 0<=b<d<=197)
 def test_bad_variant_rejected(self):
  with self.assertRaises(ValueError):m.draw_refined_closed(Image.new('RGBA',m.SIZE),'madeup')
 def test_release_has_no_asset_paths(self):self.assertEqual(cp401.RELEASE['sprite_paths'],{})

@unittest.skipUnless(SOURCE.is_file(),'Private CANON file absent; never replace with another face')
class SourceLockedContract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.src=cp401.exact_source(SOURCE)
 def test_sha(self):self.assertEqual(m.hashed(SOURCE),m.CANON_SHA)
 def test_closed_both_variants(self):
  for variant in ('root','soft'):
   art=m.draw_refined_closed(self.src,variant)
   self.assertEqual(art.mode,'RGBA');self.assertEqual(art.size,m.SIZE)
 def test_outside_eye_no_modification(self):
  for var in ('root','soft'):
   art=m.draw_refined_closed(self.src,var)
   self.assertEqual(cp401.valid_pixels_only(self.src,art),0)
 def test_source_alpha_unchanged(self):
  for var in ('root','soft'):
   art=m.draw_refined_closed(self.src,var)
   np.testing.assert_array_equal(np.asarray(self.src)[:,:,3],np.asarray(art)[:,:,3])
 def test_source_root_from_original_only(self):
  for side in m.ROIS:
   x=int((m.ROIS[side][0]+m.ROIS[side][2])/2)
   self.assertEqual(len(m.source_lash_color(self.src,side,x)),3)
 def test_both_variants_are_distinct(self):
  a=m.draw_refined_closed(self.src,'root');b=m.draw_refined_closed(self.src,'soft')
  self.assertGreater(np.count_nonzero(np.any(np.asarray(a)!=np.asarray(b),axis=2)),0)
 def test_stored_reference_exact_crop(self):
  self.assertEqual(cp401.exact_source(SOURCE).tobytes(),self.src.tobytes())
 def test_all_blink_frames_keep_protected_pixels(self):
  a=m.draw_refined_closed(self.src,'root')
  for f in cp401.render_sequence(self.src,a,72):self.assertEqual(cp401.valid_pixels_only(self.src,f),0)
 def test_invalid_source_fails_before_output(self):
  with tempfile.TemporaryDirectory() as root:
   p=Path(root)/'impostor.png';q=Path(root)/'OUT'
   Image.new('RGBA',(941,1672),(1,2,3,255)).save(p)
   with self.assertRaises(ValueError):m.run(p,q)
   self.assertFalse(q.exists())
 def test_outputs_are_review_only(self):
  with tempfile.TemporaryDirectory() as td:
   r=m.run(SOURCE,Path(td)/'out')
   self.assertEqual(r['visual_qa'],'NOT_APPROVED')
   self.assertFalse(r['android_runtime_tested'])
   self.assertEqual(r['sprite_paths'],{})
   self.assertEqual(r['outside_roi_changed'],0)
   with Image.open(Path(td)/'out'/'CP402_ATLAS_ROOT_DRAFT_15.png') as atlas:
    self.assertEqual(atlas.size,(2520,197))

if __name__=='__main__':unittest.main()
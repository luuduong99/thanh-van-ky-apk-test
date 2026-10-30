"""CP401 checks image provenance/occlusion, not visual painter approval."""
import hashlib, sys, tempfile, unittest, os, json
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cp401_occlusion_blink as m
CANON=Path(os.getenv('TVK_CANON_PATH','/mnt/data/tvk_cp396/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
class Static(unittest.TestCase):
 def test_canon_pin(self):self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
 def test_crop_and_eye_regions(self):
  self.assertEqual(m.CROP,(25,684,193,881)); self.assertEqual(m.SIZE,(168,197))
  for x1,y1,x2,y2 in m.ROIS.values():self.assertTrue(0<=x1<x2<=168 and 0<=y1<y2<=197)
 def test_release_blocked(self):
  self.assertFalse(m.RELEASE['apk_ready']);self.assertEqual(m.RELEASE['sprite_paths'],{})
  self.assertEqual(m.RELEASE['status'],'blocked_pending_painter_approval')
 def test_timeline(self):
  self.assertEqual(m.frame_progress(0),0.)
  self.assertGreater(m.frame_progress(.35),.9)
  self.assertEqual(m.frame_progress(.37),1.)
  self.assertEqual(m.frame_progress(.6),0.)
 def test_source_rejects_missing_and_invalid(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'wrong.png';path.write_bytes(b'not canon')
   with self.assertRaises(ValueError):m.exact_source(path)
@unittest.skipUnless(CANON.is_file(),'Exact private CANON unavailable: public CI cannot approve art')
class SourceChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=m.exact_source(CANON);cls.closed=m.eyelid_art(cls.src)
 def test_verified_source_and_native_crop(self):
  self.assertEqual(m.sha(CANON),m.CANON_SHA)
  self.assertTrue(np.array_equal(np.asarray(Image.open(CANON).crop(m.CROP)),np.asarray(self.src)))
 def test_exact_canonic_outside_pixels(self):
  self.assertEqual(m.valid_pixels_only(self.src,self.closed),0)
  for p in [.01,.11,.3,.5,.7,.85,.96,1.]:
   self.assertEqual(m.valid_pixels_only(self.src,m.eyelid_position(self.src,self.closed,p)),0)
 def test_endpoints_exact(self):
  self.assertTrue(np.array_equal(np.asarray(self.src),np.asarray(m.eyelid_position(self.src,self.closed,0))))
  self.assertTrue(np.array_equal(np.asarray(self.closed),np.asarray(m.eyelid_position(self.src,self.closed,1))))
 def test_partial_frames_not_same_as_linear_crossfade(self):
  src=np.asarray(self.src).astype(float);dst=np.asarray(self.closed).astype(float)
  for p in [.35,.60,.80]:
   shaped=np.asarray(m.eyelid_position(self.src,self.closed,p))
   naive=np.uint8(np.rint(src*(1-p)+dst*p))
   self.assertGreater(np.any(shaped!=naive,axis=2).sum(),70)
 def test_protected_hair_and_skin(self):
  a=np.asarray(self.src);z=np.asarray(self.closed)
  protected=[(10,90),(140,100),(80,130),(50,150),(30,60)]
  for x,y in protected:self.assertTrue(np.array_equal(a[y,x],z[y,x]))
 def test_animation_72fps_positions(self):
  frames=m.render_sequence(self.src,self.closed)
  self.assertEqual(len(frames),72)
  self.assertTrue(all(frame.size==m.SIZE for frame in frames))
  self.assertTrue(np.array_equal(np.asarray(frames[0]),np.asarray(self.src)))
  self.assertGreater(max(np.any(np.asarray(frame)!=np.asarray(self.src),axis=2).sum() for frame in frames),1000)
 def test_build_outputs_and_gif_apng(self):
  with tempfile.TemporaryDirectory() as td:
   manifest=m.build(CANON,td)
   self.assertFalse(manifest['production_release']['apk_ready'])
   self.assertEqual(manifest['outside_eye_changes'],0)
   with Image.open(Path(td)/'CP401_BLINK_PREVIEW.gif') as f:self.assertGreaterEqual(f.n_frames,5)  # Pillow merges duplicate hold frames
   with Image.open(Path(td)/'CP401_BLINK_PREVIEW.apng.png') as f:self.assertGreaterEqual(f.n_frames,8)  # optimized duplicate frames
   with Image.open(Path(td)/'CP401_POSE_ATLAS_DRAFT.png') as f:self.assertEqual(f.size,(15*168,197))
   self.assertEqual(len(list((Path(td)/'video_frames').glob('*.png'))),72)
 def test_tampered_source_failfast_before_output(self):
  with tempfile.TemporaryDirectory() as td:
   orig=bytearray(CANON.read_bytes()); orig[300]^=1
   fake=Path(td)/'fake.png';fake.write_bytes(orig);dest=Path(td)/'out'
   with self.assertRaises(ValueError):m.build(fake,dest)
   self.assertFalse(dest.exists())
if __name__=='__main__':unittest.main(verbosity=2)
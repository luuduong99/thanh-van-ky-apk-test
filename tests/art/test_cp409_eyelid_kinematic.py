"""CP409: exact user-approved CANON + geometric moving eyelid source-only tests."""
from pathlib import Path
import json,sys,unittest,hashlib
import numpy as np
from PIL import Image
THIS=(Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name=='art' else Path(__file__).resolve().parents[1])
SCRIPT_DIR=(THIS/'tools'/'art' if (THIS/'tools'/'art'/'cp409_eyelid_kinematic.py').exists() else THIS)
sys.path.insert(0,str(SCRIPT_DIR))
import cp409_eyelid_kinematic as cp
CANON=THIS/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
OUT=THIS/'OUTPUT'

class CP409SourceContract(unittest.TestCase):
 def test_release_guard(self):
  self.assertFalse(cp.PRODUCTION['artist_approved'])
  self.assertFalse(cp.PRODUCTION['blink_runtime_released'])
  self.assertFalse(cp.PRODUCTION['physical_device_tested'])
  self.assertEqual(cp.PRODUCTION['sprite_paths'],{})
 def test_sha_string(self):self.assertEqual(cp.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
 def test_motion_logic(self):
  self.assertEqual(cp.loop_progress(0),0)
  self.assertEqual(cp.loop_progress(.36),1)
  self.assertEqual(cp.loop_progress(.60),0)
  self.assertGreater(cp.loop_progress(.333),.1)
 def test_shape(self):
  self.assertEqual(cp.FACE_SIZE,(168,197))
  self.assertEqual(cp.CROP,(25,684,193,881))
  self.assertEqual(set(cp.ROIS),{'left','right'})
 def test_no_foreign_image_fetch_or_bitmap_overlay(self):
  code=(SCRIPT_DIR/'cp409_eyelid_kinematic.py').read_text(encoding='utf8')
  self.assertIn('upper_new=',code)
  self.assertIn('lower_new=',code)
  self.assertIn('y_source=',code)
  self.assertNotIn('CP402_CLOSED',code)
  self.assertNotIn('requests.get',code)
 def test_debug_viewer_pin_and_nonproduction_gate(self):
  viewer=THIS/'app/src/main/java/vn/thanhvanky/prototype/TVKBlinkAtlasPreviewActivity.kt'
  if not viewer.exists():self.skipTest('Android project source absent in local artist handoff')
  code=viewer.read_text(encoding='utf8')
  self.assertIn('cp409_review',code)
  self.assertIn('d9234630eab9e13ec07527e2c7b6fbbacd849117bf2e4983bf35ac4bcf73a07e',code)
  self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',code)
  self.assertIn('digest == pinnedAtlasSha',code)
 def test_absent_private_source_failure(self):
  with self.assertRaises(ValueError):cp.source(SCRIPT_DIR/'cp409_eyelid_kinematic.py')

@unittest.skipUnless(CANON.exists(),'private approved CANON source not checked into public GitHub')
class CP409ArtworkGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=cp.source(CANON)
  cls.cache=cp.masks_and_base(cls.source,4)
  cls.reference=np.asarray(cls.source.resize((672,788),Image.Resampling.BICUBIC))
  cls.outside=cls.cache[2]==0
 def test_approved_png_hash(self):self.assertEqual(cp.sha(CANON),cp.CANON_SHA)
 def test_native_crop_exact(self):
  with Image.open(CANON) as im: self.assertTrue(np.array_equal(np.asarray(im.crop(cp.CROP)),np.asarray(self.source)))
 def test_atlas_has_expected_dimensions_and_framing(self):
  a=Image.open(OUT/'CP409_15_POSE_NATIVE_SHA_LOCKED_DRAFT.png').convert('RGBA')
  self.assertEqual(a.size,(2520,197))
  self.assertTrue(np.array_equal(np.asarray(a.crop((0,0,168,197))),np.asarray(self.source)))
  self.assertTrue(np.array_equal(np.asarray(a.crop((14*168,0,15*168,197))),np.asarray(self.source)))
 def test_each_pose_preserves_background_and_alpha(self):
  for i in range(15):
   im=np.asarray(Image.open(OUT/f'pose_{i:02}.png'))
   self.assertTrue(np.array_equal(im[self.outside],self.reference[self.outside]),f'pose {i} changed background')
   self.assertTrue(np.array_equal(im[:,:,3],self.reference[:,:,3]))
 def test_native_atlas_preserves_face_around_both_eyes(self):
  atlas=np.asarray(Image.open(OUT/'CP409_15_POSE_NATIVE_SHA_LOCKED_DRAFT.png'))
  keep=np.ones((197,168),bool)
  for x1,y1,x2,y2 in cp.ROIS.values(): keep[y1:y2,x1:x2]=False
  original=np.asarray(self.source)
  for i in range(15):self.assertTrue(np.array_equal(atlas[:,i*168:(i+1)*168,:][keep],original[keep]))
 def test_pupils_do_not_crossfade_or_ghost(self):
  src=np.asarray(self.source.resize((672,788),Image.Resampling.BICUBIC))
  closed=np.asarray(cp.lid_frame(self.source,1,4,self.cache))
  self.assertGreater(int(np.any(src!=closed,axis=2).sum()),100)
  half=np.asarray(cp.lid_frame(self.source,.5,4,self.cache))
  self.assertFalse(np.array_equal(half,closed))
  self.assertFalse(np.array_equal(half,src))
 def test_smooth_motion_distinct_stages(self):
  a=np.asarray(cp.lid_frame(self.source,.24,4,self.cache))
  b=np.asarray(cp.lid_frame(self.source,.52,4,self.cache))
  c=np.asarray(cp.lid_frame(self.source,.79,4,self.cache))
  self.assertFalse(np.array_equal(a,b))
  self.assertFalse(np.array_equal(b,c))
 def test_wrong_source_fails_closed(self):
  fake=THIS/'OUTPUT'/'test_wrong_canon.png'
  self.source.save(fake)
  try:
   with self.assertRaises(ValueError):cp.source(fake)
  finally:fake.unlink(missing_ok=True)
 def test_qa_report_draft(self):
  report=json.loads((OUT/'CP409_REPORT.json').read_text())
  self.assertEqual(report['visual_qa'],'NOT_APPROVED')
  self.assertFalse(report['release']['blink_runtime_released'])
  self.assertEqual(report['native_atlas_sha256'],cp.sha(OUT/'CP409_15_POSE_NATIVE_SHA_LOCKED_DRAFT.png'))

if __name__=='__main__':unittest.main()
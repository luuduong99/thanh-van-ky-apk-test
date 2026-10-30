"""CP403 exact source/atlas and Android debug visual-review contract tests."""
import hashlib,os,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
import numpy as np
BASE=Path(__file__).resolve().parents[1]
ROOT=Path(__file__).resolve().parents[2]
if not (ROOT/'app/src/main/java/vn/thanhvanky/prototype/TVKBlinkAtlasPreviewActivity.kt').exists():ROOT=BASE
sys.path.insert(0,str(BASE))
try:import cp403_review_qa as qa
except ImportError:
 # In GitHub, the source module is inside tools/art.
 sys.path.insert(0,str(ROOT/'tools/art'))
 import cp403_review_qa as qa

class CP403Static(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.kotlin=(ROOT/'app/src/main/java/vn/thanhvanky/prototype/TVKBlinkAtlasPreviewActivity.kt')
  if not cls.kotlin.exists():cls.kotlin=BASE/'TVKBlinkAtlasPreviewActivity.kt'
  cls.source=cls.kotlin.read_text(encoding='utf8')
 def test_01_hashes_are_locked(self):
  self.assertEqual(len(qa.SOURCE_SHA),64);self.assertEqual(len(qa.ATLAS_SHA),64)
  self.assertIn(qa.ATLAS_SHA,self.source)
 def test_02_source_crop_lock(self):
  self.assertEqual(qa.CROP,(25,684,193,881));self.assertEqual((qa.W,qa.H),(168,197))
 def test_03_loop_positions_have_open_endpoints(self):
  self.assertEqual(len(qa.POSITIONS),15)
  self.assertEqual(qa.POSITIONS[0],0);self.assertEqual(qa.POSITIONS[-1],0)
  self.assertEqual(qa.POSITIONS[7],1)
 def test_04_debug_runtime_gate(self):
  self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',self.source)
  self.assertIn('finish(); return',self.source)
 def test_05_picker_digest_and_dimensions(self):
  for token in ('Intent.ACTION_OPEN_DOCUMENT','MessageDigest.getInstance("SHA-256")',
                'image.width == 2520 && image.height == 197','8 * 1024 * 1024'):
   self.assertIn(token,self.source)
 def test_06_source_vs_blink_comparison(self):
  self.assertIn('"MỞ / CANON"',self.source)
  self.assertIn('"CP402 / DRAFT"',self.source)
  self.assertIn('drawPanel(canvas, image, 0,',self.source)
  self.assertIn('drawPanel(canvas, image, index,',self.source)
 def test_07_frame_controls(self):
  for token in ('fun step()','fun togglePlaying()','fun toggleFiltering()',
                'fun pause()','postInvalidateOnAnimation()'):
   self.assertIn(token,self.source)
 def test_08_nearest_neighbor_mode(self):
  self.assertIn('picture.isFilterBitmap = !isSharp',self.source)
 def test_09_no_silent_production_asset(self):
  self.assertNotIn('assets.open(',self.source)
  self.assertIn('KHÔNG PHẢI ẢNH GAME ĐÃ DUYỆT',self.source)
 def test_10_non_exported_manifest(self):
  manifest=ROOT/'app/src/main/AndroidManifest.xml'
  if not manifest.exists():manifest=BASE/'AndroidManifest.xml'
  if not manifest.exists():self.skipTest('Android manifest is only available in repository')
  data=manifest.read_text(encoding='utf8')
  self.assertIn('.TVKBlinkAtlasPreviewActivity',data)
  start=data.index('android:name=".TVKBlinkAtlasPreviewActivity"')
  self.assertIn('android:exported="false"',data[start:start+100])

class CP403PrivateSource(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.canon=Path(os.environ.get('TVK_CP403_CANON',''))
  cls.atlas=Path(os.environ.get('TVK_CP403_ATLAS',''))
  if not os.environ.get('TVK_CP403_CANON') or not os.environ.get('TVK_CP403_ATLAS'):
   raise unittest.SkipTest('Private approved CANON/atlas omitted from public repository')
  if not cls.canon.is_file() or not cls.atlas.is_file():
   raise unittest.SkipTest('Approved source paths not mounted')
 def test_11_full_exact_contract(self):
  r=qa.verify(self.canon,self.atlas)
  self.assertEqual(r['outside_roi_changed'],0)
 def test_12_full_size(self):
  with Image.open(self.atlas) as i:self.assertEqual(i.size,(2520,197))
 def test_13_source_and_atlas_sha(self):
  self.assertEqual(qa.digest(self.canon),qa.SOURCE_SHA)
  self.assertEqual(qa.digest(self.atlas),qa.ATLAS_SHA)
 def test_14_unique_and_reversal(self):
  r=qa.verify(self.canon,self.atlas)
  self.assertEqual(r['unique_frame_count'],8)
  self.assertEqual(r['changed_pixels_by_pose'],list(reversed(r['changed_pixels_by_pose'])))
 def test_15_reject_modified_atlas(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.png';p.write_bytes(self.atlas.read_bytes()+b'bad')
   with self.assertRaisesRegex(ValueError,'WRONG_CP402_ATLAS_SHA256'):qa.verify(self.canon,p)
 def test_16_reject_modified_canon(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.png';p.write_bytes(self.canon.read_bytes()+b'bad')
   with self.assertRaisesRegex(ValueError,'WRONG_CANON_SOURCE_SHA256'):qa.verify(p,self.atlas)
 def test_17_source_alpha_preserved(self):
  self.assertTrue(qa.verify(self.canon,self.atlas)['source_alpha_unchanged'])
 def test_18_contact_sheet_generated(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'board.png';qa.board(self.atlas,p)
   with Image.open(p) as i:self.assertGreater(i.width,1600)
 def test_19_draft_gate(self):
  r=qa.verify(self.canon,self.atlas)
  self.assertEqual(r['release'],'DRAFT_NOT_APPROVED')
  self.assertEqual(r['production_sprite_paths'],{})

if __name__=='__main__':unittest.main()
"""CP417 CANON exact and Android debug gates; do not equate technical PASS with art approval."""
from pathlib import Path
import importlib.util, json, hashlib, zipfile, unittest, os
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[0]
REPO=Path(__file__).resolve().parents[2]
TOOL=REPO/'tools/art/cp417_source_lash_blink.py'
if not TOOL.exists(): TOOL=ROOT/'cp417_source_lash_blink.py'
CANON=Path(os.environ.get('TVK_CP417_PRIVATE_CANON', '/mnt/data/tvk_cp416_work/original/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
ANDROID=REPO/'app/src/main/java/vn/thanhvanky/prototype/TVKCP417SamePoseBlinkActivity.kt'
if not ANDROID.exists(): ANDROID=ROOT/'TVKCP417SamePoseBlinkActivity.kt'
OUTPUT=Path(os.environ.get('TVK_CP417_OUTPUT','/mnt/data/tvk_cp417_work/outputs'))
spec=importlib.util.spec_from_file_location('cp417',TOOL)
cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)
class PublicContract(unittest.TestCase):
 def test_source_identity(self):
  self.assertEqual(cp.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
  self.assertEqual(cp.FRONT,(16,180,224,623));self.assertEqual(cp.SIZE,(208,443))
 def test_frame_count_and_source_lashes(self):
  self.assertEqual(cp.FRAMES,5);self.assertEqual(cp.ROIS['L'],(88,50,104,56));self.assertEqual(cp.ROIS['R'],(107,50,124,57))
 def test_android_debug_source_guards(self):
  k=ANDROID.read_text()
  for needle in ['FLAG_DEBUGGABLE','CANON_SHA', 'ATLAS_SHA', 'sameAs(source)','inLeft','inRight','Intent.ACTION_OPEN_DOCUMENT','PICK_ATLAS']:
   self.assertIn(needle,k)
 def test_art_not_promoted(self):
  script=TOOL.read_text()
  for needle in ["'artist_quality_approved':False","'spine_ready':False","'sprite_paths':{}","'android_device_verified':False"]:
   self.assertIn(needle,script)
 def test_no_foreign_poses(self):
  self.assertNotIn('(25,684,193,881)',TOOL.read_text())

@unittest.skipUnless(CANON.exists(),'Private CANON unavailable in public checkout')
class PrivateArt(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.im=cp.source(CANON);cls.front=cls.im.crop(cp.FRONT);cls.frames=[cp.draw_frame(cls.front,i/4) for i in range(5)]
 def test_raw_sha(self):self.assertEqual(cp.sha(CANON),cp.SHA)
 def test_neutral_exact(self):self.assertTrue(np.array_equal(np.array(self.frames[0]),np.array(self.front)))
 def test_all_changes_limited_to_eye_rois(self):
  for f in self.frames:
   changed,outside=cp.roi_diff(self.front,f)
   self.assertEqual(outside,0)
 def test_frames_different(self):
  self.assertEqual(len({f.tobytes() for f in self.frames}),5)
 def test_upper_source_lash_kept(self):
  a=np.array(self.front)
  for f in self.frames:
   b=np.array(f)
   for x0,y0,x1,y1 in cp.ROIS.values():
    self.assertTrue(np.array_equal(a[y0:52,x0:x1],b[y0:52,x0:x1]))
 def test_atlas_identity_and_size(self):
  a=Image.open(OUTPUT/'CP417_SAME_POSE_5FRAME_ATLAS_DRAFT.png')
  self.assertEqual(a.size,(1040,443))
  self.assertTrue(np.array_equal(np.array(a.crop((0,0,208,443))),np.array(self.front)))
 def test_ora_visible_canon_and_crc(self):
  with zipfile.ZipFile(OUTPUT/'CP417_SOURCE_LASH_EDITABLE_DRAFT.ora') as z:
   self.assertIsNone(z.testzip())
   import xml.etree.ElementTree as ET
   root=ET.fromstring(z.read('stack.xml'))
   layers=root.find('stack').findall('layer')
   self.assertEqual(len(layers),5)
   self.assertEqual(sum(x.attrib.get('visibility')=='visible' for x in layers),1)
   self.assertTrue(np.array_equal(np.array(Image.open(z.open('mergedimage.png'))),np.array(self.front)))
 def test_manifest_gate_and_exact_atlas_sha(self):
  d=json.loads((OUTPUT/'CP417_REPORT.json').read_text())
  self.assertEqual(d['atlas_sha256'],cp.sha(OUTPUT/'CP417_SAME_POSE_5FRAME_ATLAS_DRAFT.png'))
  self.assertFalse(d['artist_quality_approved']);self.assertEqual(d['sprite_paths'],{})
 def test_fail_closed_on_wrong_source(self):
  from tempfile import TemporaryDirectory
  with TemporaryDirectory() as tmp:
   bad=Path(tmp)/'bad.png';bad.write_bytes(b'bad')
   with self.assertRaises(ValueError):cp.source(bad)

if __name__=='__main__':unittest.main()
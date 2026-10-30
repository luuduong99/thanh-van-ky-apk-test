"""CP386 source integrity tests; tests requiring private CANON intentionally skipped on public CI."""
import importlib.util
import hashlib
import tempfile
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
import zipfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
TOOL=HERE/'cp386_painted_blink_draft.py'
if not TOOL.exists():TOOL=HERE.parent.parent/'tools'/'art'/'cp386_painted_blink_draft.py'
spec=importlib.util.spec_from_file_location('cp386',TOOL)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
CANON=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
OUT=HERE/'OUTPUT'
HAS_PRIVATE=CANON.exists() and OUT.exists()

class TestCP386(unittest.TestCase):
 def test_source_constants_and_release_gate(self):
  self.assertEqual(mod.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
  self.assertEqual(mod.BBOX,(25,684,193,881))
  self.assertEqual(mod.SIZE,(168,197))
 def test_eye_paths_and_seven_stages(self):
  self.assertEqual(set(mod.EYES),{'left','right'})
  self.assertGreater(len(mod.EYES['left']),8)
  self.assertGreater(len(mod.EYES['right']),8)
  for side in mod.EYES:
   self.assertIsNotNone(mod.eyelid(side,1).getbbox())
 def test_bad_source_refused_before_any_output(self):
  with tempfile.TemporaryDirectory() as d:
   wrong=Path(d)/'bad.png'
   Image.new('RGBA',(941,1672),'white').save(wrong)
   out=Path(d)/'no-art-created'
   with self.assertRaisesRegex(ValueError,'WRONG_CANON_SHA'):mod.run(wrong,out)
   self.assertFalse(out.exists())
 @unittest.skipUnless(HAS_PRIVATE,'private exact CANON and output unavailable')
 def test_canon_bytes(self):
  self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),mod.CANON_SHA)
  self.assertEqual((OUT/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes(),CANON.read_bytes())
 @unittest.skipUnless(HAS_PRIVATE,'private art unavailable')
 def test_static_merged_identical(self):
  src=mod.check(CANON)
  exact=Image.open(OUT/'CP386_CANON_SOURCE_EXACT_OPEN.png').convert('RGBA')
  self.assertTrue(np.array_equal(np.array(src),np.array(exact)))
 @unittest.skipUnless(HAS_PRIVATE,'private art unavailable')
 def test_eyes_only_changed_underpaint(self):
  src=np.array(mod.check(CANON));under=np.array(Image.open(OUT/'layers'/'CP386_CHEEK_BASE_TECH_NOT_APPROVED.png'))
  mask=(np.asarray(mod.mask_polygon(mod.EYES['left']))>0)|(np.asarray(mod.mask_polygon(mod.EYES['right']))>0)
  dif=np.any(src[:,:,:3]!=under[:,:,:3],axis=2)
  self.assertEqual(int(np.count_nonzero(dif&~mask)),0)
  self.assertGreater(np.count_nonzero(dif),0)
 @unittest.skipUnless(HAS_PRIVATE,'private art unavailable')
 def test_ora_crc_and_source_guide_hidden(self):
  with zipfile.ZipFile(OUT/'ora'/'CP386_SOURCE_EXACT_AND_EYELIDS_DRAFT_NOT_RIG.ora') as z:
   self.assertIsNone(z.testzip())
   layers=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
   self.assertEqual(len(layers),7)
   self.assertEqual(sum(l.attrib['visibility']=='hidden' for l in layers),3)
 @unittest.skipUnless(HAS_PRIVATE,'private art unavailable')
 def test_both_closed_lid_paths_are_visible_drafts(self):
  for side in ['left','right']:
   im=Image.open(OUT/'layers'/f'{side}_closed_eyelid_DRAFT.png')
   self.assertIsNotNone(im.getchannel('A').getbbox())
 @unittest.skipUnless(HAS_PRIVATE,'private art unavailable')
 def test_seven_frames_preserve_endpoints(self):
  src=np.array(mod.check(CANON))
  frames=list(sorted((OUT/'frames').glob('CP386_FRAME_*_TECH_ONLY.png')))
  self.assertEqual(len(frames),7)
  self.assertTrue(np.array_equal(src,np.array(Image.open(frames[0]))))
  self.assertTrue(np.array_equal(src,np.array(Image.open(frames[-1]))))
 @unittest.skipUnless(HAS_PRIVATE,'private art unavailable')
 def test_release_stays_blocked(self):
  import json
  r=json.loads((OUT/'CP386_REPORT.json').read_text())
  self.assertEqual(r['visual_qa'],'NOT_PASSED')
  self.assertEqual(r['production_release'],'blocked_pending_art')
  self.assertEqual(r['sprite_paths'],{})
  self.assertFalse(r['apk_ready'])
  self.assertFalse(r['closed_eye_artist_approved'])

if __name__=='__main__':unittest.main(verbosity=2)
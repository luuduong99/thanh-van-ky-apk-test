import os,sys,unittest,tempfile
from pathlib import Path
from PIL import Image
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cp399_closed_eye_art_review as m
ROOT=Path(os.environ.get('TVK_CP398_OUTPUT','/mnt/data/tvk_cp398/OUTPUT'))
CANON=ROOT/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'; CP397=ROOT/'CP397_PREVIOUS_CLOSED_EYE_DRAFT_NOT_APPROVED.png'
NAT=ROOT/'CP398_CLOSED_EYE_NATURAL_DRAFT_NOT_APPROVED.png';SOFT=ROOT/'CP398_CLOSED_EYE_SOFT_DRAFT_NOT_APPROVED.png'
EXISTS=all(x.is_file() for x in (CANON,CP397,NAT,SOFT))
class PublicStatic(unittest.TestCase):
 def test_source_hash_shape(self):
  for val in (m.CANON_SHA,m.CP397_SHA,m.CP398_NATURAL_SHA,m.CP398_SOFT_SHA):self.assertEqual(len(val),64)
 def test_eyes_nonoverlap(self):
  l,r=m.ROIS['LEFT'],m.ROIS['RIGHT'];self.assertLess(l[2],r[0]);self.assertLess(l[0],l[2])
 def test_production_blocked(self):
  self.assertFalse(m.PRODUCTION['apk_ready']);self.assertFalse(m.PRODUCTION['spine_ready']);self.assertEqual(m.PRODUCTION['sprite_paths'],{})
  self.assertFalse(m.release_allowed({'status':'APPROVED','approved_by_user':True}))
 def test_no_false_authorization(self):self.assertEqual(m.ART_APPROVAL,'PENDING_HUMAN_VISUAL_REVIEW')
@unittest.skipUnless(EXISTS,'Private CANON / CP398 inputs absent from public repo')
class OriginalSourceChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.orig,cls.prev,cls.opts=m.validate(CANON,CP397,NAT,SOFT)
 def test_original_sha_locked(self):self.assertEqual(m.sha(CANON),m.CANON_SHA)
 def test_prior_sha_locked(self):self.assertEqual(m.sha(CP397),m.CP397_SHA)
 def test_both_variants_sha_locked(self):
  self.assertEqual(m.sha(NAT),m.CP398_NATURAL_SHA);self.assertEqual(m.sha(SOFT),m.CP398_SOFT_SHA)
 def test_pixel_exact_canon_crop(self):
  with Image.open(CANON) as im:self.assertTrue(np.array_equal(np.asarray(im.crop(m.CROP)),np.asarray(self.orig)))
 def test_all_outside_eye_pixels_zero_changed(self):
  for v in (self.prev,*self.opts.values()):self.assertEqual(m.outside_changes(self.orig,v),0)
 def test_two_drafts_distinct(self):self.assertGreater(m.changed(*self.opts.values()),5)
 def test_report_never_claims_approval(self):
  with tempfile.TemporaryDirectory() as d:
   report=m.build(CANON,CP397,NAT,SOFT,d)
   self.assertNotEqual(report['review']['choice'],'APPROVED')
   self.assertFalse(report['production_release']['apk_ready'])
   self.assertTrue((Path(d)/'CP399_CANON_NATURAL_SOFT_REVIEW_16x9.png').is_file())
   self.assertTrue((Path(d)/'CP399_EYES_EXACT_NATIVE_ZOOM.png').is_file())
 def test_corrupt_source_rejected_before_output(self):
  with tempfile.TemporaryDirectory() as d:
   can=Path(d)/'broken.png';raw=bytearray(CANON.read_bytes());raw[123]^=1;can.write_bytes(raw)
   out=Path(d)/'output'
   with self.assertRaises(ValueError):m.build(can,CP397,NAT,SOFT,out)
   self.assertFalse(out.exists())
 def test_corrupt_draft_rejected_before_output(self):
  with tempfile.TemporaryDirectory() as d:
   wrong=Path(d)/'wrong.png';raw=bytearray(NAT.read_bytes());raw[40]^=1;wrong.write_bytes(raw)
   out=Path(d)/'output'
   with self.assertRaises(ValueError):m.build(CANON,CP397,wrong,SOFT,out)
   self.assertFalse(out.exists())
if __name__=='__main__':unittest.main(verbosity=2)
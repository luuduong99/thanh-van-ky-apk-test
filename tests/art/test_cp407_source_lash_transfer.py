#!/usr/bin/env python3
"""CP407 exact-source and release gate tests (private image tests skip on GitHub)."""
import sys,unittest,hashlib,zipfile,io,json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import cp407_source_lash_transfer as tr
import cp407_make_review as mr
import cp401_occlusion_blink as cp

class StaticSourceContract(unittest.TestCase):
 def test_original_canon_sha_locked(self): self.assertEqual(cp.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
 def test_baseline_sha_locked(self):self.assertEqual(tr.EXPECTED_BASELINE_SHA,'0391ba0cb906bf5334f176ac28a508cad4afa700fe6cb7c2deb52affaf1ac5f6')
 def test_roi_is_bounded(self):
  mask=tr.roi_mask();self.assertEqual(mask.shape,(788,672));self.assertTrue(0<mask.sum()<mask.size//3)
 def test_geometric_blink_progress_starts_and_ends_open(self):
  self.assertEqual(mr.PROGRESS[0],0);self.assertEqual(mr.PROGRESS[-1],0);self.assertEqual(mr.PROGRESS[7],1);self.assertEqual(len(mr.PROGRESS),15)
 def test_production_not_marked_approved(self):
  code=Path(tr.__file__).read_text();self.assertIn('NOT_APPROVED',code);self.assertNotIn('approved_for_runtime',code)

@unittest.skipUnless((ROOT/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').is_file() and (ROOT/'CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png').is_file(),"Approved private CANON and CP402 root art are absent from public GitHub")
class ActualCanonPixels(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.original,cls.close=tr.source(ROOT)
  cls.open_4=np.asarray(cls.original.resize(tr.DISPLAY,Image.Resampling.LANCZOS))
  cls.mask=tr.roi_mask()
  cls.a,cls.paint=tr.new_candidate(cls.original,cls.close,.75)
  cls.variants=[cls.a,tr.new_candidate(cls.original,cls.close,1.15)[0]]
 def test_sha_matches_private_bitmap(self): self.assertEqual(tr.sha(ROOT/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'),cp.CANON_SHA)
 def test_closed_root_source_matches_approved_checkpoint_sha(self): self.assertEqual(tr.sha(ROOT/'CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png'),tr.EXPECTED_BASELINE_SHA)
 def test_source_size_maintained(self): self.assertEqual(self.original.size,(168,197))
 def test_distinct_variants(self):self.assertFalse(np.array_equal(np.asarray(self.variants[0]),np.asarray(self.variants[1])))
 def test_no_outside_eye_changed(self):
  for img in self.variants:self.assertTrue(np.array_equal(np.asarray(img)[~self.mask],self.open_4[~self.mask]))
 def test_alpha_canon_preserved(self):
  for img in self.variants:self.assertTrue(np.array_equal(np.asarray(img)[:,:,3],self.open_4[:,:,3]))
 def test_transferred_lash_layer_only_inside_eyes(self):
  paint=np.asarray(self.paint);self.assertTrue(np.all(paint[~self.mask]==0));self.assertGreater(np.count_nonzero(paint[:,:,3]),0)
 def test_ora_unapproved_and_source_only_visible(self):
  p=ROOT/'outputs/CP407_SOURCE_LASH_WARP_EDITABLE_NOT_APPROVED.ora'
  if not p.is_file():self.skipTest('Run builder before checking ORA artifact')
  from xml.etree import ElementTree
  with zipfile.ZipFile(p) as z:
   root=ElementTree.fromstring(z.read('stack.xml'));layers=root.findall('stack/layer')
   self.assertEqual(len(layers),6)
   self.assertEqual(sum(x.attrib.get('visibility')=='visible' for x in layers),1)
   self.assertIn('CANON',next(x.attrib['name'] for x in layers if x.attrib['visibility']=='visible'))
   merged=np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA'))
   self.assertTrue(np.array_equal(merged,self.open_4))
 def test_art_release_is_blocked(self):
  rep=ROOT/'outputs/CP407_BLINK_REPORT.json'
  if not rep.exists():self.skipTest('Run animation first')
  data=json.loads(rep.read_text());self.assertFalse(data['user_approval']);self.assertFalse(data['production_art_approval']);self.assertFalse(data['apk_integrated'])
 def test_exact_source_rejects_modified_bytes(self):
  from tempfile import TemporaryDirectory
  with TemporaryDirectory() as t:
   d=Path(t);img=np.asarray(Image.open(ROOT/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')).copy();img[0,0,0]^=1
   Image.fromarray(img).save(d/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
   (d/'CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png').write_bytes((ROOT/'CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png').read_bytes())
   with self.assertRaises(ValueError):tr.source(d)
if __name__=='__main__':unittest.main(verbosity=2)
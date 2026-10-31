#!/usr/bin/env python3
"""Actual PNG/ORA verification. Run from package folder with: python -m unittest discover -s tests -v."""
import unittest,hashlib,json,zipfile,io,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/'CP342_MANIFEST.json').read_text())
def read_png(rel):return Image.open(ROOT/rel)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
class CP342RealFileTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src=read_png(MAN['output_files']['canonical_original']['path']).convert('RGBA')
  cls.crop=read_png(MAN['output_files']['front_native']['path']).convert('RGBA')
  cls.prev=read_png(MAN['output_files']['cp341_previous']['path']).convert('RGBA')
  cls.new=read_png(MAN['output_files']['cp342_refined']['path']).convert('RGBA')
  cls.a=np.array(cls.prev);cls.b=np.array(cls.new)
 def test_01_exact_canon_source_sha(self):self.assertEqual(sha(ROOT/MAN['output_files']['canonical_original']['path']),MAN['canon_sha256'])
 def test_02_source_native_pixels_are_exact(self):self.assertTrue(np.array_equal(np.array(self.src.crop(tuple(MAN['source_bbox_xyxy']))),np.array(self.crop)))
 def test_03_no_generated_rgb_or_costume_changes(self):
  self.assertTrue(np.array_equal(self.a[:,:,:3],self.b[:,:,:3]));self.assertTrue(np.array_equal(self.b[:,:,:3],np.array(self.crop)[:,:,:3]))
 def test_04_upper_body_alpha_is_byte_identical(self):self.assertTrue(np.array_equal(self.a[:410,:,3],self.b[:410,:,3]))
 def test_05_alpha_is_only_reduced(self):
  self.assertTrue(np.all(self.b[:,:,3]<=self.a[:,:,3]));self.assertGreater(np.count_nonzero(self.b[:,:,3]!=self.a[:,:,3]),1300)
 def test_06_floor_bluegray_shadow_is_attenuated(self):
  old=self.a[421:438,32:184,3].astype(np.int64).sum();new=self.b[421:438,32:184,3].astype(np.int64).sum()
  self.assertGreater(old-new,100000)
 def test_07_shoe_core_alpha_preserved(self):self.assertTrue(np.array_equal(self.a[398:435,85:120,3],self.b[398:435,85:120,3]))
 def test_08_drape_alpha_still_present(self):
  self.assertGreater(np.count_nonzero(self.b[275:410,:35,3]>128),1900)
  self.assertGreater(np.count_nonzero(self.b[275:410,180:,3]>128),1100)
 def test_09_mask_matches_png(self):self.assertTrue(np.array_equal(np.array(read_png(MAN['output_files']['cp342_mask']['path']).convert('L')),self.b[:,:,3]))
 def test_10_removed_alpha_diagnostic_matches_difference(self):
  removed=np.array(read_png(MAN['output_files']['cp342_delta']['path']).convert('L'))
  self.assertTrue(np.array_equal(removed,self.a[:,:,3].astype('int16')-self.b[:,:,3].astype('int16')))
 def test_11_all_declared_output_hashes(self):
  for name,item in MAN['output_files'].items():self.assertEqual(sha(ROOT/item['path']),item['sha256'],name)
 def test_12_ora_real_4_layers_crc_and_merge(self):
  path=ROOT/MAN['output_files']['ora']['path']
  with zipfile.ZipFile(path) as z:
   self.assertIsNone(z.testzip());self.assertEqual(z.read('mimetype'),b'image/openraster')
   stack=ET.fromstring(z.read('stack.xml'))
   layers=stack.findall('.//layer')
   self.assertEqual(len(layers),4)
   self.assertEqual(sum(el.attrib['visibility']=='visible' for el in layers),1)
   self.assertTrue(np.array_equal(np.array(Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA')),self.b))
 def test_13_not_artist_approved_or_spine(self):
  p=MAN['production_gate'];self.assertFalse(p['manual_artist_edge_clean_approved']);self.assertFalse(p['riggable_layers_ready'])
  self.assertFalse(p['face_underpaint_complete']);self.assertFalse(p['spine_verified']);self.assertFalse(p['apk_built_and_tested'])
  self.assertEqual(p['runtime_release'],'blocked_pending_art');self.assertEqual(p['sprite_paths_registered'],0)
if __name__=='__main__':unittest.main()
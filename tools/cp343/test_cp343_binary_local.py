"""Run from the unpacked CP343 archive; checks actual PNGs and ORA binaries."""
from pathlib import Path
from PIL import Image
import numpy as np,hashlib,json,unittest,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/'CP343_MANIFEST.json').read_text())
SRC=np.array(Image.open(ROOT/'source/FRONT_CP342_SOURCE_LOCKED.png').convert('RGBA'))
CAN=Path('/mnt/data/TVK_LamThien_CANON_V2_1_20261029/LAM_THIEN_CANON_V2_1_FINAL_20261029.png')

class BinaryContract(unittest.TestCase):
 def test_01_final_canon_hash_is_locked(self):
  self.assertEqual(MAN['approved_source_sha256'],'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
  if CAN.exists():self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),MAN['approved_source_sha256'])
 def test_02_native_size(self):self.assertEqual(list(SRC.shape[:2][::-1]),[215,449])
 def test_03_ten_distinct_nonempty_regions(self):
  self.assertEqual(len(MAN['region_assignments']),10)
  self.assertTrue(all(x['visible_pixels']>0 for x in MAN['region_assignments']))
  self.assertEqual(len(set(x['name'] for x in MAN['region_assignments'])),10)
 def test_04_all_layer_hashes(self):
  for x in MAN['region_assignments']:
   p=ROOT/x['png'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['png_sha256'])
 def test_05_disjoint_alpha_and_pixel_exact_reconstruction(self):
  reconstructed=np.zeros_like(SRC)
  for item in MAN['region_assignments']:
   ar=np.array(Image.open(ROOT/item['png']).convert('RGBA'))
   active=ar[:,:,3]>0
   self.assertFalse(np.any((reconstructed[:,:,3]>0)&active))
   reconstructed[active]=ar[active]
  self.assertTrue(np.array_equal(reconstructed[:,:,3],SRC[:,:,3]))
  idx=SRC[:,:,3]>0;self.assertTrue(np.array_equal(reconstructed[idx],SRC[idx]))
 def test_06_mask_matches_actual_layer(self):
  for item in MAN['region_assignments']:
   mask=np.array(Image.open(ROOT/item['mask']).convert('L'))>0
   pixels=np.array(Image.open(ROOT/item['png']).convert('RGBA'))[:,:,3]>0
   self.assertTrue(np.array_equal(mask,pixels))
 def test_07_region_coverage_and_counts(self):
  self.assertEqual(sum(x['visible_pixels'] for x in MAN['region_assignments']),MAN['visible_source_pixels'])
  self.assertEqual(MAN['visible_source_pixels'],int(np.count_nonzero(SRC[:,:,3]>0)))
 def test_08_ora_is_valid_and_n_layers(self):
  ora=ROOT/MAN['ora'];z=zipfile.ZipFile(ora)
  self.assertIsNone(z.testzip())
  self.assertEqual(z.read('mimetype'),b'image/openraster')
  xml=ET.fromstring(z.read('stack.xml'))
  self.assertEqual(len(xml.find('stack').findall('layer')),10)
  self.assertEqual(np.array(Image.open(z.open('mergedimage.png')).convert('RGBA'))[:,:,3].shape,(449,215))
 def test_09_pixel_recomposition_output(self):
  ar=np.array(Image.open(ROOT/'source/FRONT_CP343_AT_REST_EXACT_RECOMPOSITION.png').convert('RGBA'))
  self.assertTrue(np.array_equal(ar[:,:,3],SRC[:,:,3]))
  self.assertTrue(np.array_equal(ar[SRC[:,:,3]>0],SRC[SRC[:,:,3]>0]))
 def test_10_motion_stress_detects_missing_underpaint(self):
  x=MAN['arm_motion_stress_test'];self.assertEqual(x['result'],'FAIL_no_hidden_underpaint')
  self.assertGreater(x['missing_source_pixels'],1000)
  self.assertGreater(x['new_protruding_pixels'],500)
  self.assertTrue((ROOT/x['diagnostic_preview']).is_file())
 def test_11_explicitly_not_production(self):
  for key in ['underpaint_for_motion_exists','semantic_borders_artist_verified','high_resolution_repaint_exists','riggable_layers_ready','spine_verified','apk_verified']:
   self.assertIs(MAN[key],False,key)
  self.assertEqual(MAN['android_production_release'],'blocked_pending_art')
  self.assertEqual(MAN['game_sprite_paths_registered'],0)
 def test_12_full_qa_previews_and_guide(self):
  self.assertTrue((ROOT/'preview/CP343_CANON_SOURCE_EXACT_LAYER_MAP_QA.png').exists())
  self.assertTrue((ROOT/'preview/CP343_LAYER_REGION_LEGEND.png').exists())
  self.assertTrue((ROOT/'ARTIST_TASKS.md').exists())
if __name__=='__main__':unittest.main()
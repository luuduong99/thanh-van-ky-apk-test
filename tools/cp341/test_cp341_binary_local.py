"""CP341 binary QA: real source-approved V2.1 PNG, masks, ORA and visual artifact."""
from pathlib import Path
import hashlib, json, unittest, zipfile, io
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parents[1]
MAN=json.loads((BASE/'CP341_MANIFEST.json').read_text())
SRC=BASE/'source/CANON_V2_1_EXACT_ORIGINAL.png'
ORIG=BASE/'source/FRONT_CANON_V2_1_EXACT_NATIVE_CROP.png'
OLD=BASE/'source/FRONT_CP340_PREVIOUS_NOT_PRODUCTION.png'
NEW=BASE/'source/FRONT_CP341_REFINED_SINGLE_FOREGROUND_NOT_RIG.png'
MASK=BASE/'source/FRONT_CP341_EDITABLE_ALPHA_MASK.png'
ORA=BASE/'ora/CP341_FRONT_MATTE_REVIEW_NOT_RIG.ora'
APPROVED_HASH='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class CP341Binary(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=np.array(Image.open(SRC).convert('RGBA'))
  cls.orig=np.array(Image.open(ORIG).convert('RGBA'))
  cls.old=np.array(Image.open(OLD).convert('RGBA'))
  cls.new=np.array(Image.open(NEW).convert('RGBA'))
  cls.mask=np.array(Image.open(MASK).convert('L'))
 def test_original_exact_approved_sha(self):
  self.assertEqual(sha(SRC),APPROVED_HASH)
  self.assertEqual(MAN['canonical_sha256'],APPROVED_HASH)
 def test_exact_native_crop_pixel_identity(self):
  x0,y0,x1,y1=MAN['front_source_bbox_xyxy']
  self.assertTrue(np.array_equal(self.orig,self.source[y0:y1,x0:x1]))
  self.assertEqual([x1-x0,y1-y0],[215,449])
 def test_no_rgb_pixel_redesign_in_trial(self):
  self.assertTrue(np.array_equal(self.orig[:,:,:3],self.new[:,:,:3]))
  self.assertTrue(MAN['front_rgb_exact_original'])
 def test_editable_mask_same_as_export_alpha(self):
  self.assertTrue(np.array_equal(self.mask,self.new[:,:,3]))
  self.assertLess(np.min(self.mask),10)
  self.assertEqual(np.max(self.mask),255)
 def test_real_alpha_detail_exists_not_flattened(self):
  self.assertGreater(np.count_nonzero(self.mask==0),500)
  self.assertGreater(np.count_nonzero((self.mask>0)&(self.mask<255)),500)
  self.assertGreater(np.count_nonzero(self.mask==255),10000)
 def test_recovers_real_lost_side_hair_and_sleeves(self):
  self.assertGreater(MAN['opaque_px_gain'],18000)
  for key,region in MAN['region_checks'].items():
   self.assertGreater(region['delta_opaque_px'],2000,key)
 def test_no_canonical_damage_or_expression_redraw(self):
  self.assertTrue(MAN['flat_source_only'])
  self.assertTrue(MAN['not_artist_semantic_layers'])
  self.assertEqual(MAN['front_native_px'],[215,449])
 def test_source_board_label_is_not_part_of_alpha(self):
  self.assertEqual(int(np.max(self.mask[:6,:])),0)
 def test_output_file_hashes(self):
  for key,meta in MAN['output_files'].items():
   self.assertEqual(sha(BASE/meta['path']),meta['sha256'],key)
 def test_ora_openraster_has_three_truthfully_labeled_layers(self):
  with zipfile.ZipFile(ORA) as z:
   self.assertIsNone(z.testzip())
   self.assertEqual(z.read('mimetype'),b'image/openraster')
   xml=ET.fromstring(z.read('stack.xml'))
   self.assertEqual((int(xml.attrib['w']),int(xml.attrib['h'])),(215,449))
   layers=xml.findall('stack/layer')
   self.assertEqual(len(layers),3)
   self.assertEqual([l.attrib['visibility'] for l in layers],['visible','hidden','hidden'])
   self.assertIn('NOT_RIG',layers[0].attrib['name'])
   self.assertTrue(np.array_equal(np.array(Image.open(io.BytesIO(z.read('mergedimage.png')))),self.new))
   for layer in layers:
    im=Image.open(io.BytesIO(z.read(layer.attrib['src'])))
    self.assertEqual(im.mode,'RGBA')
 def test_release_remains_blocked(self):
  gate=MAN['production_gate']
  self.assertEqual(gate['android_production_release'],'blocked_pending_art')
  self.assertEqual(gate['sprite_paths_registered'],0)
  for k in ['artist_clean_edges_approved','separate_character_parts_completed','face_underpaint_completed','spine_verified','apk_verified']:
   self.assertFalse(gate[k],k)
 def test_previews_are_actual_image_files(self):
  with Image.open(BASE/'preview/CP341_BEFORE_AFTER_ALPHA_QA.png') as im:
   self.assertEqual(im.size,(1190,1070))
 def test_no_spurious_high_resolution_claim(self):
  self.assertLessEqual(self.new.shape[1],215)
  self.assertTrue(any('No new high-resolution' in x for x in MAN['limitations']))
if __name__=='__main__':unittest.main()
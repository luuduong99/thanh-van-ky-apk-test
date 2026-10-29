"""Unit tests CP331 real ORA structure and canonical source policy."""
import json, unittest, importlib.util, pathlib, zipfile, io, hashlib
import numpy as np
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('audit_cp331',ROOT/'audit_cp331.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
DATA=json.loads((ROOT/'manifest.json').read_text())

class CP331(unittest.TestCase):
 def test_approved_source_hash_pinned(self):
  self.assertEqual(DATA['canonical_sha256'],mod.CANON_SHA)
  self.assertEqual(DATA['approved_expression_sha256'],mod.EXPR_SHA)
 def test_five_expressions(self):
  self.assertEqual([r['id'] for r in DATA['results']],list(mod.IDS))
 def test_single_base_sha(self):
  self.assertEqual(len(set(x['underpaint_sha256'] for x in DATA['results'])),1)
  self.assertTrue(DATA['outside_face_region_pixel_identical'])
 def test_art_quality_gate_stays_pending(self):
  for key in ('shared_master_art_production_ready','new_generated_face_visual_approved', 'spine_ready','apk_verified','asset_registration_allowed'):
   self.assertFalse(DATA[key],key)
  self.assertTrue(DATA['flat_master_contains_baked_facial_features'])
 def test_exactly_35_nonempty_alpha_patches(self):
  self.assertEqual(sum(x['source_patch_layers_nonempty'] for x in DATA['results']),35)
  self.assertTrue(all(x['alpha_pixels_across_layers']>1000 for x in DATA['results']))
 def test_native_size_not_fake_highres(self):
  self.assertEqual(DATA['native_source_dimensions_px'],[258,364])
  self.assertFalse(DATA['source_is_true_high_resolution'])
 def test_real_oras_recompose_without_drift(self):
  errors,notes=mod.audit(ROOT)
  self.assertEqual(errors,[], '\n'.join(errors))
 def test_guides_are_hidden(self):
  for item in DATA['results']:
   p=ROOT/'ora'/f"CP331_{item['id']}_SHARED_FACE_TECH_TRIAL_NOT_GAME_ART.ora"
   with zipfile.ZipFile(p) as z:
    self.assertEqual(z.testzip(),None)
    self.assertIn(b'visibility="hidden"',z.read('stack.xml'))
 def test_five_images_differ_inside_roi(self):
  a=[]
  for item in DATA['results']:
   im=Image.open(ROOT/'preview'/f"{item['id']}_FIXED_FACE_COMPOSITE.png").convert('RGB')
   a.append(hashlib.sha256(im.tobytes()).hexdigest())
  self.assertEqual(len(set(a)),5)
if __name__=='__main__':unittest.main()
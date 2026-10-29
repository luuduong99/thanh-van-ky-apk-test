import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from verify_cp334 import audit, IDS, CANON_SHA, EXPRESSION_SHA
M=json.loads((ROOT/'CP334_ART_REVIEW_MANIFEST.json').read_text())
class CP334ReviewTests(unittest.TestCase):
 def test_real_package(self): self.assertEqual(audit(ROOT),[])
 def test_five_emotions_only(self): self.assertEqual([v['expression_id'] for v in M['candidate_pieces']],IDS)
 def test_canon_sha(self): self.assertEqual(M['canonical_sha256'],CANON_SHA)
 def test_approved_sha(self):self.assertEqual(M['approved_expression_sha256'],EXPRESSION_SHA)
 def test_exact_cropped_source(self):
  src=Image.open(ROOT/'source/CP334_GENERATED_FLAT_SHEET_NOT_APPROVED.png').convert('RGB')
  for item in M['candidate_pieces']:
   got=Image.open(ROOT/item['path']).convert('RGB')
   self.assertEqual(got.tobytes(),src.crop(tuple(item['source_box_xyxy'])).tobytes())
 def test_no_fake_spine_or_apk(self):
  for key in ('spine_rig_verified','apk_built_tested','new_portrait_style_artist_approved','clean_independent_facial_attachments'):
   self.assertIs(M['qa_gates'][key],False)
 def test_flat_image_dimensions_declared(self):
  image=Image.open(ROOT/'source/CP334_GENERATED_FLAT_SHEET_NOT_APPROVED.png')
  self.assertEqual(list(image.size),M['cp334_generated_sheet_dimensions'])
 def test_oras_is_review_not_rig(self):self.assertIs(M['visual_review_workspace_is_not_sprite_rig'],True)
if __name__=='__main__':unittest.main()
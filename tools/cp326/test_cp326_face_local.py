import copy, json, tempfile, unittest
from pathlib import Path
from validate_cp326_face import audit,EMOTIONS

HERE=Path(__file__).resolve().parent
CANON=Path('/mnt/data/TVK_LamThien_CANON_BodyCostume_V2_20261028.png')

class CP326Tests(unittest.TestCase):
  def test_five_prototype_ora_layers_are_real_and_composites_match(self):
    errors,pending=audit(HERE,canon=CANON)
    self.assertEqual(errors,[])
    self.assertTrue(pending)
  def test_production_gate_stays_closed(self):
    errors,_=audit(HERE,strict=True)
    self.assertTrue(any('Underpaint' in x for x in errors))
  def test_manifest_has_five_approved_emotion_ids(self):
    data=json.loads((HERE/'manifest.json').read_text())
    self.assertEqual(data['expression_ids'],EMOTIONS)
    self.assertEqual([x['id'] for x in data['items']],EMOTIONS)
  def test_manifest_cannot_claim_sprite_ready(self):
    data=json.loads((HERE/'manifest.json').read_text())
    for state in ('production_ready','spine_ready','apk_ready','asset_registration_allowed'):
      self.assertFalse(data[state])
  def test_wrong_reference_checksum_is_rejected(self):
    with tempfile.TemporaryDirectory() as d:
      p=Path(d); data=json.loads((HERE/'manifest.json').read_text())
      data['approved_five_expression_sheet_sha256']='0'*64
      (p/'manifest.json').write_text(json.dumps(data))
      errors,_=audit(p)
      self.assertTrue(any('approved visual reference SHA' in x for x in errors))
  def test_missing_source_binary_cannot_pass(self):
    with tempfile.TemporaryDirectory() as d:
      p=Path(d);(p/'manifest.json').write_bytes((HERE/'manifest.json').read_bytes())
      errors,_=audit(p)
      self.assertTrue(any('file read error' in x for x in errors))

if __name__=='__main__':unittest.main()
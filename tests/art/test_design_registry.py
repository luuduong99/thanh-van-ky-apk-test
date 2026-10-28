import copy
import json
import unittest
from pathlib import Path
from tools.art.validate_design_registry import validate

ROOT=Path(__file__).resolve().parents[2]
DATA=json.loads((ROOT/'docs/art/LAM_THIEN_DESIGN_REGISTRY.json').read_text(encoding='utf8'))

class RegistryGateTests(unittest.TestCase):
    def test_current_registry_valid(self):
        self.assertEqual(validate(DATA),[])

    def test_pending_preview_cannot_be_production_reference(self):
        d=copy.deepcopy(DATA)
        d['implementation']['design_reference_id']=d['latest_pending_preview']['id']
        self.assertTrue(validate(d))

    def test_previous_proxy_cannot_be_production_reference(self):
        d=copy.deepcopy(DATA)
        d['implementation']['design_reference_id']='CP317_proxy'
        self.assertTrue(validate(d))

    def test_prevent_fake_rig_and_apk_complete_flags(self):
        d=copy.deepcopy(DATA)
        d['implementation']['apk_integrated']=True
        self.assertTrue(validate(d))

    def test_approved_design_must_have_confirmed_traits(self):
        d=copy.deepcopy(DATA)
        d['latest_user_approved_design']['required_traits']=[]
        self.assertTrue(validate(d))

if __name__=='__main__':unittest.main()
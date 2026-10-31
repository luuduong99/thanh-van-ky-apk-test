"""Checks real CP325 ORA proxy files, including deliberate production rejection.

This suite uses local archive files extracted beside it. On GitHub CI, only
metadata/static contracts can be tested because binary ORAs live in Library.
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from validate_cp325_face_proxies import audit, audit_ora

ROOT=Path(__file__).resolve().parent

class CP325Tests(unittest.TestCase):
    def setUp(self):
        self.manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))

    def test_five_files_pass_reference_structure(self):
        self.assertEqual(audit(ROOT), [])

    def test_strict_gate_blocks_proxy(self):
        problems=audit(ROOT,strict=True)
        self.assertEqual(len(problems),1)
        self.assertIn('not CANON V2',problems[0])

    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as dirname:
            dest=Path(dirname)
            (dest/'manifest.json').write_text((ROOT/'manifest.json').read_text())
            self.assertTrue(any('Missing ORA' in x for x in audit(dest)))

    def test_wrong_region_hash_rejected(self):
        it=copy.deepcopy(self.manifest['items'][0])
        it['regions'][0]['sha256']='0'*64
        problems=audit_ora(ROOT/it['ora_filename'],it)
        self.assertTrue(any('Patch SHA mismatch' in x for x in problems))

    def test_flat_ref_not_spine_asset(self):
        self.assertFalse(self.manifest['asset_registration_allowed'])
        self.assertFalse(self.manifest['spine_ready'])
        self.assertFalse(self.manifest['apk_ready'])

if __name__=='__main__': unittest.main()
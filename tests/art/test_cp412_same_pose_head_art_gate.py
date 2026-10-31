"""CP412 guards: exact source, honest art gate, repeatable technician-only preview."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import unittest
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

REPO=Path(__file__).resolve().parents[2]
SCRIPT=REPO/'tools/art/cp412_same_pose_head_art_gate.py'
if not SCRIPT.exists():SCRIPT=Path(__file__).resolve().parents[2]/'tools/art/cp412_same_pose_head_art_gate.py'
spec=importlib.util.spec_from_file_location('cp412',SCRIPT)
cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)
CANON=Path(os.getenv('TVK_CP412_PRIVATE_CANON','/NO_PRIVATE_ART_IN_GITHUB.png'))
OUTPUT=Path(os.getenv('TVK_CP412_PRIVATE_OUTPUT','/NO_CP412_OUTPUT'))

class PublicChecks(unittest.TestCase):
    def test_exact_source_and_crop_locked(self):
        self.assertEqual(cp.CANON_SIZE,(941,1672));self.assertEqual(cp.FRONT_BOX,(16,180,224,623))
        self.assertEqual(cp.CANON_HASH,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
    def test_front_pose_not_expression_pose(self):
        self.assertEqual(cp.FRONT_SIZE,(208,443));self.assertEqual(cp.HEAD_PIVOT,(104,77))
        self.assertEqual(cp.ANGLES,(-4,-2,0,2,4))
    def test_artist_layers_all_explicitly_blank(self):
        self.assertEqual(len(cp.REQUIRED_LAYERS),8)
        self.assertIn('03_closed_eyelids_same_pose',cp.REQUIRED_LAYERS)
        self.assertIn('05_neck_scalp_underpaint',cp.REQUIRED_LAYERS)
        self.assertIn('07_hair_underpaint',cp.REQUIRED_LAYERS)
    def test_polygon_mask_not_full_image(self):
        m=np.array(cp.matte())
        self.assertEqual(m.shape,(443,208));self.assertEqual(set(np.unique(m).tolist()),{0,255})
    def test_reject_wrong_source_before_creation(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            bad=Path(td)/'wrong.png'; bad.write_bytes(b'Not CANON')
            out=Path(td)/'created_outputs'
            with self.assertRaises(ValueError):cp.run(bad,out)
            self.assertFalse(out.exists())

@unittest.skipUnless(CANON.is_file(),'Original CANON is private, not shipped in public repo')
class PrivateExactSourceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front=cp.load_canon(CANON).crop(cp.FRONT_BOX)
        cls.plate,cls.head=cp.derive_diagnostic(cls.front)
    def test_source_hash_actual(self):
        self.assertEqual(cp.sha(CANON),cp.CANON_HASH)
    def test_source_exact_neutral(self):
        neutral,count=cp.rotate_diagnostic(self.front,self.plate,self.head,0)
        self.assertEqual(count,0)
        self.assertTrue(np.array_equal(np.array(neutral),np.array(self.front)))
    def test_nonzero_angles_reveal_underpaint_deficiency(self):
        for a in (-4,-2,2,4):
            _,count=cp.rotate_diagnostic(self.front,self.plate,self.head,a)
            self.assertGreater(count,0)
    def test_ora_is_blank_paint_layers_and_exact_source(self):
        p=OUTPUT/'CP412_ARTIST_INTAKE_BLANK_LAYERS.ora'
        if not p.exists():self.skipTest('No generated output in this job')
        with zipfile.ZipFile(p) as z:
            self.assertIsNone(z.testzip())
            root=ET.fromstring(z.read('stack.xml'))
            ll=root.find('stack').findall('layer')
            self.assertEqual(len(ll),9)
            self.assertEqual(sum(l.attrib['visibility']=='visible' for l in ll),1)
            self.assertTrue(np.array_equal(np.array(Image.open(z.open('mergedimage.png')).convert('RGBA')),np.array(self.front)))
            for l in ll[:-1]:
                self.assertFalse(np.any(np.array(Image.open(z.open(l.attrib['src'])).convert('RGBA'))[:,:,3]))
    def test_report_art_not_falsely_approved(self):
        p=OUTPUT/'CP412_MANIFEST.json'
        if not p.exists():self.skipTest('No generated output in this job')
        m=json.loads(p.read_text(encoding='utf-8'))
        self.assertFalse(m['human_paint_complete'])
        self.assertFalse(m['art_approved'])
        self.assertFalse(m['apk_production_ready'])
        self.assertEqual(m['sprite_paths'],{})
        self.assertTrue(m['technical_placeholder_exposed_pixels']['4']>0)

if __name__=='__main__':unittest.main()
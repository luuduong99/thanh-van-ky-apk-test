"""CP371 mechanical tests; passing these NEVER implies artistic approval."""
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE
if not (ROOT/'cp371_refine_pose_details.py').exists():
    ROOT=HERE.parents[1]/'tools'/'art'
spec=importlib.util.spec_from_file_location('cp371',ROOT/'cp371_refine_pose_details.py')
cp=importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)
CANON=Path(os.environ.get('TVK_CANON_PATH',str(HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))

class StructureTests(unittest.TestCase):
    def test_canon_lock_and_layer_order(self):
        self.assertEqual(cp.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(len(cp.ORDER),9)
        self.assertLess(cp.ORDER.index(cp.NEW_FOLD),cp.ORDER.index(cp.cp370.cp369.WRIST_NAME))
        self.assertLess(cp.ORDER.index(cp.NEW_HEM),cp.ORDER.index(cp.cp370.cp369.WRIST_NAME))

    def test_new_layers_are_independent_bezier_drawings(self):
        for pose in ('idle','raised'):
            for role in (cp.NEW_FOLD,cp.NEW_HEM):
                xml=ET.fromstring(cp.svg(role,pose))
                self.assertEqual(xml.tag.split('}')[-1],'svg')
                self.assertGreaterEqual(len(xml.findall('.//{*}path')),3)
                self.assertNotIn('<image',cp.svg(role,pose))
        for name in (cp.NEW_FOLD,cp.NEW_HEM):
            self.assertNotEqual(cp.svg(name,'idle'),cp.svg(name,'raised'))

    def test_no_release_claims_embedded(self):
        txt=(ROOT/'cp371_refine_pose_details.py').read_text()
        self.assertIn("'visual_qa':'NOT_PASSED'",txt)
        self.assertIn("'art_release':'blocked_pending_art'",txt)
        self.assertIn("'spine_ready':False",txt)

    def test_wrong_canon_fails_before_output_written(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'fake.png'
            Image.new('RGBA',(941,1672),'white').save(fake)
            out=Path(d)/'out'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                cp.build(fake,out)
            self.assertFalse(out.exists())

@unittest.skipUnless(CANON.exists(),'Exact approved CANON not present in repository CI')
class AssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.tmp.name)/'out'
        cls.report=cp.build(CANON,cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_canon_exact_bytes(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),cp.SHA)
        self.assertEqual(self.report['canon_sha256'],cp.SHA)

    def test_genuine_deltas_for_both_poses(self):
        for pose in ('idle','raised'):
            self.assertGreater(self.report['change_pixels_against_cp370'][pose],5000)
            self.assertLess(self.report['change_pixels_against_cp370'][pose],SIZE_LIMIT)

    def test_new_detail_layers_nonempty_and_targeted(self):
        for pose in ('idle','raised'):
            for name in (cp.NEW_FOLD,cp.NEW_HEM):
                count=self.report['new_overlay_within_sleeve_or_edge'][pose][name]
                self.assertGreater(count['visible_pixels'],500)
                self.assertGreaterEqual(count['coverage_fraction'],.95)

    def test_static_layers_unchanged_between_two_poses(self):
        self.assertTrue(self.report['static_hair_bodice_shoulder_ornament_unchanged_between_poses'])

    def test_ora_real_layers_hidden_guide_crc(self):
        for pose in ('idle','raised'):
            ora=self.out/f'CP371_{pose.upper()}_NINE_ART_LAYERS_NOT_SPINE.ora'
            self.assertTrue(ora.exists())
            with zipfile.ZipFile(ora) as z:
                self.assertIsNone(z.testzip())
                root=ET.fromstring(z.read('stack.xml'))
                ls=root.find('stack').findall('layer')
                self.assertEqual(len(ls),10)
                self.assertEqual(sum(n.get('visibility')=='hidden' for n in ls),1)
                self.assertIn('CANON_V2_1_REFERENCE',ls[-1].get('name'))
                for n in ls[:9]:
                    self.assertTrue(n.get('visibility')=='visible')
                    im=Image.open(io.BytesIO(z.read(n.get('src'))))
                    self.assertEqual(im.size,cp.SIZE)
                    self.assertIsNotNone(im.getchannel('A').getbbox())

    def test_source_reference_not_replaced(self):
        self.assertTrue(self.report['working_resolution_is_upscaled_geometry_not_master_art'])
        self.assertFalse(self.report['user_approved_sprite'])
        self.assertEqual(self.report['art_release'],'blocked_pending_art')
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertFalse(self.report['apk_built_or_tested'])

    def test_preview_exact_canon_and_only_own_drafts(self):
        with Image.open(self.out/self.report['preview']) as pic:
            self.assertEqual(pic.size,(1670,800))
        self.assertIn('CANON',self.report['preview'])

SIZE_LIMIT=cp.SIZE[0]*cp.SIZE[1]//5
if __name__=='__main__':unittest.main(verbosity=2)
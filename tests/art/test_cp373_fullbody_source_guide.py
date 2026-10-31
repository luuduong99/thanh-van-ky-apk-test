"""Real-source CP373 reproducible checks. No visual-art approval is implied."""
import importlib.util
import json
import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ROOT=HERE
SCRIPT=HERE/'cp373_fullbody_source_guide.py'
if not SCRIPT.exists():
    ROOT=HERE.parents[1] # repo/tests/art => repo
    SCRIPT=ROOT/'tools'/'art'/'cp373_fullbody_source_guide.py'
spec=importlib.util.spec_from_file_location('cp373',SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
if not CAN.exists(): CAN=ROOT/'art_assets'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
HAS_SOURCE=CAN.exists()

class BasicContract(unittest.TestCase):
    def test_fixed_canon_geometry_and_roles(self):
        self.assertEqual(m.SIZE,(941,1672))
        self.assertEqual(m.BBOX,(13,172,230,630))
        self.assertEqual(m.FRONT_SIZE,(217,458))
        self.assertEqual(len(m.NAMES),19)

    def test_wrong_source_rejected_before_creating_output(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'fake.png';Image.new('RGBA',(941,1672),'white').save(fake)
            dest=Path(d)/'SHOULD_NOT_EXIST'
            with self.assertRaisesRegex(ValueError,'Wrong CANON'):
                m.create(fake,dest)
            self.assertFalse(dest.exists())

@unittest.skipUnless(HAS_SOURCE,'Private user-approved CANON bytes unavailable on CI')
class RealSourceArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.tmp.name)/'generated'
        cls.report=m.create(CAN,cls.out)
        cls.mask=np.array(Image.open(cls.out/'masks'/'foreground_alpha_editable.png'))
        cls.ref=np.asarray(Image.open(cls.out/'source'/'FRONT_EXACT_CROP_WITH_BACKGROUND.png').convert('RGBA'))

    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()

    def test_sha_and_dimensions(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.SHA)
        self.assertEqual(self.ref.shape,(458,217,4))

    def test_rgb_never_repainted(self):
        cut=np.asarray(Image.open(self.out/'source'/'FRONT_MATTE_DRAFT_NOT_ART.png'))
        self.assertTrue(np.array_equal(cut[:,:,:3],self.ref[:,:,:3]))
        self.assertTrue(np.array_equal(cut[:,:,3],self.mask))

    def test_19_parts_partition_source_alpha_without_loss(self):
        parts=[np.asarray(Image.open(self.out/'masks'/(n+'_mask.png'))) for n in m.NAMES]
        count=np.sum([p>0 for p in parts],axis=0)
        self.assertTrue(np.all(count[self.mask>0]==1))
        self.assertTrue(np.all(count[self.mask==0]==0))
        self.assertTrue(np.array_equal(np.maximum.reduce(parts),self.mask))

    def test_ora_crc_layers_guide_hidden(self):
        with zipfile.ZipFile(self.out/'ora'/'CP373_FRONT_19_SOURCE_REGION_GUIDES_NOT_RIG.ora') as z:
            self.assertIsNone(z.testzip())
            xml=ET.fromstring(z.read('stack.xml'))
            ls=xml.find('stack').findall('layer')
            self.assertEqual(len(ls),20)
            self.assertEqual(sum(x.get('visibility')=='hidden' for x in ls),1)
            self.assertTrue('CANON_EXACT' in ls[-1].get('name'))
            merged=np.asarray(Image.open(z.open('mergedimage.png')).convert('RGBA'))
            self.assertTrue(np.array_equal(merged[:,:,3],self.mask))

    def test_shoe_toes_image_left_and_right_preserved(self):
        for key,v in self.report['toe_blue_color_checks'].items():
            with self.subTest(key=key):
                self.assertTrue(v['pass'])
                self.assertGreaterEqual(v['retained_visible_blue_px'],int(v['reference_blue_px']*0.8))

    def test_motion_still_missing_underpaint(self):
        self.assertGreater(self.report['technical_motion_missing_underpaint_px'],0)
        self.assertFalse(self.report['true_semantic_occluded_layers'])
        self.assertFalse(self.report['rig_spine_ready'])

    def test_no_production_release_and_manual_cleanup(self):
        self.assertEqual(self.report['visual_qa'],'NOT_PASSED')
        self.assertEqual(self.report['production_release'],'blocked_pending_art')
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertTrue(self.report['alpha_manual_cleanup_required'])
        self.assertTrue(self.report['floor_shadow_contamination_possible'])
        self.assertFalse(self.report['native_painted_full_body'])

    def test_preview_provenance_and_19_file_masks(self):
        self.assertTrue((self.out/'qa'/'CP373_CANON_FRONT_MATTE_19REGION_COMPARISON.png').exists())
        self.assertEqual(len(list((self.out/'layers').glob('*.png'))),19)
        self.assertTrue(self.report['static_ora_recompose_exact'])

if __name__=='__main__':unittest.main(verbosity=2)
"""CP374 source-locked conservative floor removal; structural QA, not art approval."""
import hashlib, io, sys, unittest, tempfile, json, zipfile, importlib.util
from pathlib import Path
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT/'cp374_floor_cleanup.py'
if not SCRIPT.exists(): SCRIPT=ROOT.parents[1]/'tools'/'art'/'cp374_floor_cleanup.py'
spec=importlib.util.spec_from_file_location('cp374_floor_cleanup',SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CAN=ROOT/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
if not CAN.exists():CAN=ROOT.parents[1]/'art_assets'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
CP373=ROOT/'CP373_SOURCE'
if not CP373.exists(): CP373=ROOT.parents[1]/'art_assets'/'CP373_SOURCE' 
# On GitHub CI, the private PNG and CP373 output are absent. Two safety tests still run.
class SourceContract(unittest.TestCase):
    def test_source_geometry_and_release_gate_constants(self):
        self.assertEqual(m.SIZE,(941,1672))
        self.assertEqual(m.BBOX,(13,172,230,630))
        self.assertEqual(m.FRONT,(217,458))
        self.assertEqual(len(m.TOES),2)
    def test_fake_source_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'fake.png';Image.new('RGBA',m.SIZE,'white').save(fake)
            output=Path(d)/'should_not_exist'
            with self.assertRaisesRegex(ValueError,'CANON_V2_1_SHA_MISMATCH'):
                m.make(fake,output,output)
            self.assertFalse(output.exists())

@unittest.skipUnless(CAN.is_file() and (CP373/'source'/'FRONT_EXACT_CROP_WITH_BACKGROUND.png').exists(),
                     'Private CANON/CP373 pixels not available on CI')
class RealSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.tmp.name)/'cp374'
        cls.report=m.make(CAN,CP373,cls.out)
        cls.old=np.asarray(Image.open(cls.out/'source'/'CP373_BEFORE_TRANSPARENT_SOURCE_MATTE.png'))
        cls.new=np.asarray(Image.open(cls.out/'source'/'CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png'))
        cls.floor=np.asarray(Image.open(cls.out/'masks'/'CP374_REMOVED_FLOOR_CANDIDATES.png').convert('L'))>0
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_source_sha_and_native_dimensions(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.SHA)
        self.assertEqual(self.old.shape,(458,217,4))
    def test_rgb_exact_and_alpha_changes_only_flagged_floor(self):
        self.assertTrue(np.array_equal(self.old[:,:,:3],self.new[:,:,:3]))
        diff=self.old[:,:,3]!=self.new[:,:,3]
        self.assertTrue(np.array_equal(diff,self.floor))
        self.assertTrue(np.all(self.new[self.floor,3]==0))
    def test_small_safe_floor_zone_and_no_toe_area_change(self):
        yy,xx=np.where(self.floor)
        self.assertGreater(len(yy),200)
        self.assertTrue((yy>=431).all() and (yy<=451).all())
        self.assertTrue((xx>=37).all() and (xx<=164).all())
        self.assertTrue(np.array_equal(self.old[410:458,76:127,3],self.new[410:458,76:127,3]))
        self.assertTrue(np.array_equal(self.old[:431,:,3],self.new[:431,:,3]))
    def test_both_blue_toes_preserved(self):
        a=self.report['blue_shoe_tip_checks']
        self.assertEqual(a['left']['preserved_blue_px'],163)
        self.assertEqual(a['right']['preserved_blue_px'],146)
        self.assertTrue(all(v['pass'] for v in a.values()))
    def test_ora_has_19_visible_and_two_hidden_review_layers(self):
        ora=self.out/'ora'/'CP374_FRONT_19_REVISED_SOURCE_MASKS_NOT_RIG.ora'
        with zipfile.ZipFile(ora) as z:
            self.assertIsNone(z.testzip())
            layers=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
            self.assertEqual(len(layers),21)
            self.assertEqual(sum(x.get('visibility')=='visible' for x in layers),19)
            self.assertEqual(sum(x.get('visibility')=='hidden' for x in layers),2)
            merged=np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA'))
            self.assertTrue(np.array_equal(merged[:,:,3],self.new[:,:,3]))
    def test_source_regions_are_still_disjoint(self):
        masks=list((self.out/'masks').glob('*_source_mask.png'))+list((self.out/'masks').glob('*_guide_mask.png'))
        # More robustly use all numbered role masks.
        masks=sorted(p for p in (self.out/'masks').glob('*.png') if p.name[:2].isdigit())
        self.assertEqual(len(masks),19)
        arr=np.array([np.asarray(Image.open(x).convert('L'))>0 for x in masks])
        self.assertTrue(np.all(arr.sum(axis=0)<=1))
        self.assertTrue(np.array_equal(arr.any(axis=0),self.new[:,:,3]>0))
    def test_release_gate_stays_closed_and_background_known_incomplete(self):
        r=self.report
        self.assertEqual(r['visual_qa'],'NOT_PASSED')
        self.assertEqual(r['production_release'],'blocked_pending_art')
        self.assertFalse(r['spine_ready'])
        self.assertFalse(r['apk_ready'])
        self.assertFalse(r['full_motion_gap_free'])
        self.assertTrue(r['manual_floor_cleanup_still_needed'])
        self.assertFalse(r['native_painted_hd_fullbody'])
    def test_canon_only_preview_exists(self):
        self.assertTrue((self.out/'qa'/'CP374_CANON_FLOOR_BEFORE_AFTER_NOT_APPROVED.png').is_file())
if __name__=='__main__':unittest.main(verbosity=2)
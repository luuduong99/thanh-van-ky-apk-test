"""CP376 tests of source provenance, reversible geometry, gap diagnostics and release gate.
Passing these tests is *not* visual acceptance or a full-motion/game-ready claim.
"""
import hashlib, importlib.util, io, json, tempfile, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image
import numpy as np

HERE=Path(__file__).resolve().parent
SRC=HERE/'cp376_local_wrist_refinement.py'
if not SRC.exists():SRC=HERE.parents[1]/'tools'/'art'/'cp376_local_wrist_refinement.py'
spec=importlib.util.spec_from_file_location('tvk_cp376',SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
MATTE=HERE/'CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png'
HAND=HERE/'14_left_hand_source.png'
HAS_SOURCE=CAN.exists() and MATTE.exists() and HAND.exists()

class StaticContracts(unittest.TestCase):
    def test_canon_lock_and_dimensions(self):
        self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.SIZE,(217,458));self.assertEqual(m.SIZE6,(1302,2748))
    def test_three_actual_new_vector_sources(self):
        self.assertEqual(len(m.NEW_ART),3)
        for name in m.NEW_ART:
            xml=m.svg(name)
            ET.fromstring(xml)
            self.assertIn('<path',xml)
            self.assertNotIn('<image',xml)
            self.assertNotIn('data:image',xml)
    def test_invalid_canon_cannot_create_output(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'fake.png';Image.new('RGBA',(941,1672),'white').save(fake)
            dest=Path(d)/'does-not-exist'
            with self.assertRaisesRegex(ValueError,'Wrong CANON'):
                m.make(fake,fake,fake,dest)
            self.assertFalse(dest.exists())
    def test_rig_release_is_explicitly_blocked(self):
        source=SRC.read_text('utf-8')
        self.assertIn("'production_release':'blocked_pending_art'",source)
        self.assertIn("'full_motion_gap_free':False",source)
        self.assertIn("'native_painted_full_body':False",source)

@unittest.skipUnless(HAS_SOURCE,'Private CANON/CP374/CP375 source files unavailable in public CI')
class RealSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=tempfile.TemporaryDirectory();cls.out=Path(cls.folder.name)/'art'
        cls.result=m.make(CAN,MATTE,HAND,cls.out)
    @classmethod
    def tearDownClass(cls):cls.folder.cleanup()
    def test_source_hash_and_preserved_images(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.CANON_SHA)
        self.assertEqual(self.result['source_sha256'],m.CANON_SHA)
        img,mat,arm=m.validate_source(CAN,MATTE,HAND)
        a=np.asarray(mat);b=np.asarray(img.crop(m.FRONT))
        self.assertTrue(np.array_equal(a[:,:,:3],b[:,:,:3]))
    def test_diagnostic_reference_case(self):
        self.assertEqual(self.result['old_exposed_px'],204)
        self.assertEqual(self.result['cp375_missing_px'],90)
        self.assertGreater(self.result['cp376_missing_px'],0)
        self.assertLess(self.result['cp376_missing_px'],self.result['cp375_missing_px'])
        self.assertEqual(sum(c['pixels'] for c in self.result['gap_clusters_before']),90)
    def test_no_blind_fingertip_filling(self):
        z=self.result['diagnostic_rois']
        self.assertEqual(z['finger_silhouette_motion']['before'],15)
        self.assertEqual(z['finger_silhouette_motion']['after'],15)
        self.assertEqual(z['wrist_cuff_seam']['after'],0)
        self.assertLess(z['rear_ribbon_boundary']['after'],z['rear_ribbon_boundary']['before'])
        self.assertFalse(self.result['full_motion_gap_free'])
    def test_original_and_draft_parts_editable_and_nonempty(self):
        art=list((self.out/'layers').glob('*.png'))
        self.assertEqual(len(art),7)
        self.assertEqual(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in art}),7)
        self.assertEqual(len(list((self.out/'svg').glob('*.svg'))),7)
        for x in art:self.assertIsNotNone(Image.open(x).getchannel('A').getbbox())
    def test_ora_crc_seven_visible_one_hidden_canon(self):
        with zipfile.ZipFile(self.out/'ora'/self.result['ora_name']) as z:
            self.assertIsNone(z.testzip())
            ls=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
            self.assertEqual(len(ls),8)
            self.assertEqual(sum(n.attrib['visibility']=='visible' for n in ls),7)
            self.assertEqual(sum(n.attrib['visibility']=='hidden' for n in ls),1)
            self.assertIn('CANON',ls[-1].attrib['name'])
            self.assertEqual(Image.open(io.BytesIO(z.read('mergedimage.png'))).size,m.SIZE6)
    def test_blue_toes_in_source_not_touched(self):
        img,mat,_=m.validate_source(CAN,MATTE,HAND)
        src=np.asarray(img.crop(m.FRONT));out=np.asarray(mat)
        for roi,expected in [((79,432,102,458),163),((109,414,122,446),146)]:
            x1,y1,x2,y2=roi;a=src[y1:y2,x1:x2];b=out[y1:y2,x1:x2]
            blue=(a[:,:,2]>a[:,:,0]*1.14)&(a[:,:,2]>a[:,:,1]*1.09)&(a[:,:,2]>90)
            ret=blue&(b[:,:,3]>=128)&(b[:,:,2]>b[:,:,0]*1.14)&(b[:,:,2]>b[:,:,1]*1.09)
            self.assertEqual(int(blue.sum()),expected)
            self.assertEqual(int(ret.sum()),expected)
    def test_extra_offsets_and_art_approval_blocked(self):
        self.assertEqual(len(self.result['multi_offset_diagnostics_not_animation_test']),4)
        for k,v in self.result['multi_offset_diagnostics_not_animation_test'].items():
            self.assertGreater(v['source_exposed_px'],0)
            self.assertLessEqual(v['cp376_residual_px'],v['cp375_residual_px'])
        self.assertFalse(self.result['apk_ready'])
        self.assertFalse(self.result['spine_ready'])
        self.assertEqual(self.result['visual_qa'],'NOT_PASSED')
        self.assertEqual(self.result['sprite_paths'],{})
        self.assertTrue((self.out/'qa'/self.result['preview_name']).exists())

if __name__=='__main__':unittest.main(verbosity=2)
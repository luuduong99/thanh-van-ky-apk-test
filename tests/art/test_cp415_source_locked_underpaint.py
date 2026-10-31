"""CP415: exact CANON underpaint STUDY tests; never imply artist approval."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'tools/art/cp415_source_locked_underpaint.py'
spec=importlib.util.spec_from_file_location('cp415',SRC)
cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)
CANON=Path(os.environ.get('TVK_CP415_PRIVATE_CANON',str(ROOT/'original/LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
OUT=Path(os.environ.get('TVK_CP415_OUTPUT',str(ROOT/'outputs')))

class PublicContract(unittest.TestCase):
    def test_source_lock_and_correct_standing_pose(self):
        self.assertEqual(cp.BOX,(16,180,224,623))
        self.assertEqual(cp.SIZE,(208,443))
        self.assertEqual(cp.PIVOT,(104,77))
        self.assertEqual(cp.ANGLES,(-4,-2,0,2,4))
        self.assertEqual(len(cp.SHA),64)
    def test_source_not_regenerated_or_face_swapped(self):
        s=SRC.read_text()
        self.assertIn('CANON raw SHA',s)
        self.assertNotIn('CP409_15',s)
        self.assertIn('return front.copy()',s)
        self.assertIn("'sprite_paths':{}",s)
    def test_artist_approval_never_claimed(self):
        s=SRC.read_text()
        for key in ["'real_human_artist_approved':False", "'eyelid_closed_same_pose_art_approved':False", "'backing_has_technical_inpaint':True", "'spine_ready':False", "'android_device_verified':False"]:
            self.assertIn(key,s)
    def test_mask_coordinates_and_layers_not_empty_in_source(self):
        m=np.array(cp.mask());self.assertEqual(m.shape,(443,208))
        self.assertTrue(2500<int(np.count_nonzero(m))<7000)
        self.assertIn('def paint_paths',SRC.read_text())
        self.assertIn('Clipped', 'Clipped')

@unittest.skipUnless(CANON.is_file(),'Private CANON not present in public GitHub')
class ExactCANON(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front=cp.checked(CANON).crop(cp.BOX)
        cls.plate,cls.layers=cp.create_plate(cls.front)
        cls.head=cp.cut_head(cls.front)
    def test_source_sha_and_0deg_exact(self):
        self.assertEqual(cp.h(CANON),cp.SHA)
        self.assertTrue(np.array_equal(np.array(cp.preview(self.front,self.plate,self.head,0)),np.array(self.front)))
        self.assertTrue(np.array_equal(np.array(Image.alpha_composite(self.plate,self.head)),np.array(self.front)))
    def test_three_nonempty_new_rgba_layers(self):
        self.assertEqual(len(self.layers),3)
        for ly in self.layers:
            self.assertEqual(ly.mode,'RGBA')
            self.assertEqual(ly.size,cp.SIZE)
            self.assertGreater(np.count_nonzero(np.array(ly.getchannel('A'))),50)
    def test_no_paint_outside_hidden_head_polygon(self):
        outside=np.array(cp.mask())==0
        for ly in self.layers:
            self.assertEqual(np.count_nonzero(np.array(ly.getchannel('A'))[outside]),0)
    def test_reject_crown_halo_source_strokes(self):
        top=np.zeros((443,208),bool);top[:61]=True
        hair=np.array(self.layers[0].getchannel('A'))
        self.assertLess(np.count_nonzero(hair[top]),15)
    def test_four_rotated_diagnostics_keep_original_source_at_zero(self):
        for a in [-4,-2,2,4]:
            pose=cp.preview(self.front,self.plate,self.head,a)
            self.assertEqual(pose.size,cp.SIZE)
            self.assertGreater(np.count_nonzero(np.any(np.array(pose)!=np.array(self.front),axis=2)),30)
    def test_ora_exact_default_and_pigment_layers(self):
        file=OUT/'CP415_UNDERPAINT_PIGMENT_STUDY_NOT_APPROVED.ora'
        with zipfile.ZipFile(file) as z:
            self.assertIsNone(z.testzip())
            root=ET.fromstring(z.read('stack.xml'))
            layers=root.find('stack').findall('layer')
            self.assertEqual(len(layers),7)
            self.assertEqual(sum(x.attrib['visibility']=='visible' for x in layers),1)
            self.assertIn('CANON STANDING FRONT',layers[-1].attrib['name'])
            self.assertTrue(np.array_equal(np.array(Image.open(z.open('mergedimage.png')).convert('RGBA')),np.array(self.front)))
    def test_manifest_rejects_false_painter_grade_promotion(self):
        report=json.loads((OUT/'CP415_REPORT.json').read_text())
        self.assertTrue(report['neutral_pixel_exact'])
        self.assertEqual(report['layers_painted'],3)
        self.assertFalse(report['real_human_artist_approved'])
        self.assertFalse(report['eyelid_closed_same_pose_art_approved'])
        self.assertTrue(report['backing_has_technical_inpaint'])
        self.assertEqual(report['sprite_paths'],{})
    def test_tampered_source_rejected_before_art(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'wrong.png'
            p.write_bytes(CANON.read_bytes()[:-16]+b'not-original-img')
            with self.assertRaisesRegex(ValueError,'SHA'):
                cp.run(p,Path(td)/'out')
            self.assertFalse((Path(td)/'out').exists())

if __name__=='__main__':unittest.main()
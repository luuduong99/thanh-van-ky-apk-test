"""CP416 exact-CANON source and art gate checks: no false visual approval."""
from __future__ import annotations
import importlib.util,hashlib,json,os,sys,tempfile,unittest,zipfile
from pathlib import Path
import numpy as np
from PIL import Image

REPO=Path(__file__).resolve().parents[2]
SCRIPT=REPO/'tools/art/cp416_front_pose_eyelid_art.py'
spec=importlib.util.spec_from_file_location('cp416',SCRIPT)
cp=importlib.util.module_from_spec(spec);sys.modules['cp416']=cp;spec.loader.exec_module(cp)
# By design original is private and not in the public repository.
SOURCE=Path(os.environ.get('TVK_CP416_PRIVATE_CANON',str(REPO/'private/LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
OUT=Path(os.environ.get('TVK_CP416_TEST_OUTPUT',str(REPO/'output_cp416')))

class Static(unittest.TestCase):
    def test_expected_hash_and_pose(self):
        self.assertEqual(cp.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(cp.BOX,(16,180,224,623))
        self.assertEqual(cp.SIZE,(208,443))
    def test_only_same_pose_eye_boxes(self):
        self.assertEqual(set(cp.ROIS),{'viewer_left','viewer_right'})
        for x0,y0,x1,y1 in cp.ROIS.values():
            self.assertTrue(80<x0<x1<130 and 40<y0<y1<65)
    def test_editors_only_never_promoted(self):
        t=SCRIPT.read_text()
        for marker in ["'visual_approval':'PENDING_USER'","'spine_ready':False","'sprite_paths':{}","'apk_art_ready':False","'production_release_status':'blocked_pending_art'"]:
            self.assertIn(marker,t)
    def test_bad_bytes_fail_closed_before_write(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'wrong.png';path.write_bytes(b'bad bytes')
            with self.assertRaises(ValueError):cp.run(path,Path(d)/'out')
            self.assertFalse((Path(d)/'out').exists())
    def test_curve_endpoints(self):
        p=cp.bezier((1,1),(3,2),(4,2),(6,1))
        self.assertEqual(p[0],(12,12));self.assertEqual(p[-1],(72,12))

@unittest.skipUnless(SOURCE.exists(),'Original CANON is private; not shipped to public GitHub')
class WithCanon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=cp.checked(SOURCE)
        cls.front=cls.src.crop(cp.BOX)
        OUT.mkdir(parents=True,exist_ok=True)
        cls.report=cp.run(SOURCE,OUT)
    def test_original_source_exact(self):
        self.assertEqual(cp.checksum(SOURCE),cp.SHA)
        self.assertTrue(np.array_equal(np.array(self.front),np.array(Image.open(OUT/'CP416_SOURCE_CANON_FRONT_208x443.png'))))
    def test_closed_states_change_only_eyes(self):
        allowed=np.zeros((443,208),bool)
        for x0,y0,x1,y1 in cp.ROIS.values():allowed[y0:y1,x0:x1]=True
        for v in ['RESTFUL','COMPLETE']:
            im=Image.open(OUT/f'CP416_{v}_CLOSED_EYE_DRAFT.png').convert('RGBA')
            diff=np.any(np.array(im)!=np.array(self.front),axis=2)
            self.assertGreater(int(diff.sum()),80)
            self.assertFalse(np.any(diff & ~allowed))
    def test_all_six_paint_layers_nonempty_and_bounded(self):
        allowed=np.zeros((443,208),bool)
        for x0,y0,x1,y1 in cp.ROIS.values():allowed[y0:y1,x0:x1]=True
        for v in ['RESTFUL','COMPLETE']:
            for name in ['SKIN','CREASE','LASH']:
                im=Image.open(OUT/f'CP416_{v}_{name}_LAYER.png').convert('RGBA')
                alpha=np.array(im.getchannel('A'))>0
                self.assertGreater(int(alpha.sum()),0)
                self.assertFalse(np.any(alpha&~allowed))
    def test_visual_states_are_distinct(self):
        a=np.asarray(Image.open(OUT/'CP416_RESTFUL_CLOSED_EYE_DRAFT.png'))
        b=np.asarray(Image.open(OUT/'CP416_COMPLETE_CLOSED_EYE_DRAFT.png'))
        self.assertTrue(np.any(a!=b))
    def test_atlas_frame_zero_identical(self):
        atlas=Image.open(OUT/'CP416_OPEN_SOFT_CLOSED_ATLAS_DRAFT.png').convert('RGBA')
        self.assertEqual(atlas.size,(624,443))
        self.assertTrue(np.array_equal(np.array(atlas.crop((0,0,208,443))),np.array(self.front)))
    def test_ora_source_visible_and_merged_exact(self):
        with zipfile.ZipFile(OUT/'CP416_SAME_POSE_CLOSED_EYE_EDITABLE_NOT_APPROVED.ora') as z:
            self.assertIsNone(z.testzip())
            import xml.etree.ElementTree as ET
            root=ET.fromstring(z.read('stack.xml'));layers=root.find('stack').findall('layer')
            self.assertEqual(len(layers),9)
            self.assertEqual([e.attrib['visibility'] for e in layers],['hidden']*8+['visible'])
            merged=Image.open(z.open('mergedimage.png')).convert('RGBA')
            self.assertTrue(np.array_equal(np.array(merged),np.array(self.front)))
    def test_report_release_gates_remain_blocked(self):
        self.assertEqual(self.report['visual_approval'],'PENDING_USER')
        self.assertFalse(self.report['eyelid_closed_same_pose_art_approved'])
        self.assertFalse(self.report['neck_hair_underpaint_artist_approved'])
        self.assertFalse(self.report['spine_ready'])
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertEqual(self.report['production_release_status'],'blocked_pending_art')

if __name__=='__main__':unittest.main()
"""CP378 fidelity/provenance and five frame source tests, NOT art acceptance."""
import hashlib,importlib.util,io,json,tempfile,unittest,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE
SCRIPT=HERE/'cp378_five_pose_vector_study.py'
if not SCRIPT.exists():
    ROOT=HERE.parents[1] # repo/tests/art => repo
    SCRIPT=ROOT/'tools'/'art'/'cp378_five_pose_vector_study.py'
spec=importlib.util.spec_from_file_location('cp378five',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
MAT=HERE/'CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png'
HAND=HERE/'14_left_hand_source.png'
HAS_ART=all(p.exists() for p in (CAN,MAT,HAND))
OUT=HERE/'OUTPUT'

class StaticContracts(unittest.TestCase):
    def test_strict_canon_sha_and_geometry(self):
        self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.SIZE,(217,458));self.assertEqual(m.SIZE6,(1302,2748))
    def test_exactly_five_unique_geometry_steps(self):
        self.assertEqual(len(m.POSES),5)
        self.assertEqual([t for name,t in m.POSES],[0.,.25,.5,.75,1.])
        paths=[]
        for name,t in m.POSES:
            art=m.drawn_pose_svgs(t)
            self.assertEqual(set(art),set(m.POSE_LAYER_KEYS))
            for markup in art.values():
                doc=m.wrap_svg(markup)
                ET.fromstring(doc)
                self.assertNotIn('<image',doc)
                self.assertNotIn('data:image',doc)
            paths.append(art['08_hand_contour_parametric'])
        self.assertEqual(len(set(paths)),5)
    def test_no_raster_double_hand_crossover(self):
        src=SCRIPT.read_text(encoding='utf8')
        self.assertIn('from authored landmark geometry',src)
        self.assertNotIn('Image.blend(',src)
        self.assertNotIn('ImageChops.blend(',src)
        self.assertTrue(all('M' in m.drawn_pose_svgs(t)['08_hand_contour_parametric'] for name,t in m.POSES))
    def test_bad_source_fails_before_writing(self):
        with tempfile.TemporaryDirectory() as td:
            fake=Path(td)/'invalid.png'
            Image.new('RGBA',(941,1672),'white').save(fake)
            out=Path(td)/'no-draft-should-appear'
            with self.assertRaisesRegex(ValueError,'Wrong CANON'):
                m.make(fake,fake,fake,out)
            self.assertFalse(out.exists())

@unittest.skipUnless(HAS_ART,'Private approved CANON and source matte/hand not available to public CI')
class RealSourceQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if (OUT/'CP378_REPORT.json').exists():
            cls.root=OUT;cls.tmp=None
        else:
            cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name)/'generated'
            m.make(CAN,MAT,HAND,cls.root)
        cls.report=json.loads((cls.root/'CP378_REPORT.json').read_text())
    @classmethod
    def tearDownClass(cls):
        if cls.tmp is not None:cls.tmp.cleanup()
    def test_source_sha_pixels_and_immutable_reference(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.CANON_SHA)
        src,mat,hand=m.cp376.validate_source(CAN,MAT,HAND)
        exact=np.asarray(src.crop(m.FRONT))
        ref=np.asarray(Image.open(self.root/'CANON_EXACT_FRONT_REFERENCE_217x458.png'))
        self.assertTrue(np.array_equal(ref,exact))
        self.assertTrue(np.array_equal(np.asarray(mat)[:,:,:3],exact[:,:,:3]))
    def test_five_ora_files_valid_and_canon_guide_hidden(self):
        for pose,t in m.POSES:
            path=self.root/'ora'/f'CP378_{pose.upper()}_TEN_ART_LAYERS_NOT_RIG.ora'
            with zipfile.ZipFile(path) as z:
                self.assertIsNone(z.testzip())
                ls=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
                self.assertEqual(len(ls),11)
                self.assertEqual(sum(x.get('visibility')=='visible' for x in ls),10)
                self.assertEqual(sum(x.get('visibility')=='hidden' for x in ls),1)
                self.assertIn('CANON_V2_1',ls[-1].get('name'))
                self.assertEqual(Image.open(io.BytesIO(z.read('mergedimage.png'))).size,m.SIZE6)
    def test_seven_shared_layers_and_three_dynamic_per_pose(self):
        self.assertEqual(len(list((self.root/'svg').glob('shared__*.svg'))),7)
        self.assertEqual(len(list((self.root/'svg').glob('*.svg'))),22)
        self.assertEqual(len(list((self.root/'png').glob('*.png'))),22)
        for pose,t in m.POSES:
            for layer in m.POSE_LAYER_KEYS:
                name=f'{pose}__{layer}'
                self.assertTrue((self.root/'svg'/(name+'.svg')).exists())
                self.assertIsNotNone(Image.open(self.root/'png'/(name+'.png')).getchannel('A').getbbox())
    def test_five_distinct_hand_alpha_masks_no_duplication(self):
        masks=[]
        for pose,t in m.POSES:
            x=np.asarray(Image.open(self.root/'png'/f'{pose}__08_hand_contour_parametric.png').getchannel('A'))>128
            masks.append(x)
        self.assertEqual(len({m.tobytes() for m in masks}),5)
    def test_centroid_steps_small_and_roughly_even(self):
        steps=np.asarray(self.report['hand_centroid_step_px_6x'])
        self.assertTrue(np.all(steps>1))
        self.assertTrue(np.all(steps<34))
        self.assertLess(float(steps.max()-steps.min()),4.)
        self.assertEqual(self.report['hand_motion_step_qa'],'PASS_TECHNICAL_ONLY')
    def test_diagnostic_gap_baseline_unchanged(self):
        self.assertEqual(self.report['motion_gap_diagnostic_from_cp376_not_rescored'],{'-6,3':18,'-4,2':21,'3,-2':98,'-8,5':26})
        self.assertFalse(self.report['full_motion_gap_free'])
    def test_preview_uses_only_canon_and_local_art(self):
        self.assertTrue((self.root/'qa'/'CP378_CANON_FIVE_HAND_POSES_NOT_APPROVED.png').exists())
        with Image.open(self.root/'qa'/'CP378_FIVE_POSE_FLIPBOOK_QA_ONLY.gif') as gif:
            self.assertGreaterEqual(gif.n_frames,8)
        self.assertTrue(self.report['exact_canon_source_unchanged'])
    def test_game_release_remains_blocked(self):
        self.assertEqual(self.report['visual_qa'],'NOT_PASSED')
        self.assertEqual(self.report['production_release'],'blocked_pending_art')
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertFalse(self.report['spine_ready'])
        self.assertFalse(self.report['apk_ready'])
        self.assertFalse(self.report['full_body_semantic_art_ready'])
        self.assertFalse(self.report['animated_game_fps_measured'])

if __name__=='__main__':unittest.main(verbosity=2)
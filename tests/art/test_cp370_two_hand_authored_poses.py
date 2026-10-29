"""CP370 technical tests on actual user-approved CANON and new editable SVG keyframes.
No test constitutes aesthetic acceptance, Spine validation, or APK approval.
"""
from pathlib import Path
import unittest, tempfile, json, sys, io, zipfile, hashlib
import xml.etree.ElementTree as ET
from PIL import Image, ImageChops
import numpy as np

HERE=Path(__file__).resolve().parent
SCRIPT_ROOT=HERE if (HERE/'cp370_two_hand_authored_poses.py').exists() else HERE.parents[1]/'tools'/'art'
sys.path.insert(0,str(SCRIPT_ROOT))
import cp370_two_hand_authored_poses as cp370

CANON=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
@unittest.skipUnless(CANON.exists(), "Exact CANON artwork is Library-only: asset integration checks must run locally")
class CP370Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.tmp.name)
        cls.before=hashlib.sha256(CANON.read_bytes()).hexdigest()
        cls.result=cp370.build(CANON,cls.out)
    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_01_source_exact_and_not_mutated(self):
        self.assertEqual(self.before,cp370.SHA)
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),self.before)
        self.assertEqual(self.result['source_dimensions'],[941,1672])

    def test_02_new_pose_has_independent_authored_geometry(self):
        self.assertEqual(set(cp370.RAISED),set(cp370.KEYFRAME_NAMES))
        for name in cp370.RAISED:
            s=cp370.svg(name,'raised')
            ET.fromstring(s)
            self.assertIn('<path',s)
            self.assertNotIn('transform="rotate',s)
            self.assertNotIn('<image',s)
            self.assertNotEqual(s,cp370.svg(name,'idle'))

    def test_03_all_seven_layers_have_visible_art(self):
        for pose in ('idle','raised'):
            for name in cp370.ORDER:
                image=cp370.png(name,pose)
                self.assertEqual(image.size,cp370.SIZE)
                self.assertIsNotNone(image.getchannel('A').getbbox())

    def test_04_stationary_shoulder_and_moving_wrist(self):
        self.assertTrue(self.result['fixed_vs_moving_diagnostic']['shoulder_gold_exactly_unchanged'])
        self.assertTrue(self.result['fixed_vs_moving_diagnostic']['wrist_relocated'])
        self.assertLess(self.result['fixed_vs_moving_diagnostic']['wrist_raised_bbox'][1],self.result['fixed_vs_moving_diagnostic']['wrist_idle_bbox'][1])

    def test_05_local_hidden_shoulder_underpaint(self):
        m=self.result['fixed_vs_moving_diagnostic']
        self.assertGreater(m['shoulder_joint_roi_newly_exposed_px'],0)
        self.assertEqual(m['joint_exposed_without_underpaint_px'],0)

    def test_06_both_ora_stacks_real_and_guide_hidden(self):
        for pose in ('idle','raised'):
            target=self.out/f'CP370_{pose.upper()}_SEVEN_LAYER_DRAFT_NOT_SPINE.ora'
            with zipfile.ZipFile(target) as z:
                self.assertIsNone(z.testzip())
                root=ET.fromstring(z.read('stack.xml'))
                layers=root.find('stack').findall('layer')
                self.assertEqual(len(layers),8)
                self.assertEqual(sum(n.get('visibility')=='hidden' for n in layers),1)
                self.assertIn('CANON',layers[-1].get('name'))
                for layer in layers[:7]:
                    img=Image.open(io.BytesIO(z.read(layer.get('src'))))
                    self.assertEqual(img.size,cp370.SIZE)
                    self.assertIsNotNone(img.getchannel('A').getbbox())

    def test_07_no_fake_game_asset_release(self):
        self.assertEqual(self.result['visual_qa'],'NOT_PASSED')
        self.assertEqual(self.result['production_release'],'blocked_pending_art')
        self.assertEqual(self.result['sprite_paths'],{})
        self.assertFalse(self.result['spine_ready'])
        self.assertFalse(self.result['apk_ready'])

    def test_08_wrong_reference_refused(self):
        bad=self.out/'fake.png'
        Image.new('RGBA',(941,1672),'white').save(bad)
        with self.assertRaisesRegex(ValueError,'CANON SHA'):
            cp370.build(bad,self.out/'badresult')
        self.assertFalse((self.out/'badresult').exists())

class CP370StaticContract(unittest.TestCase):
    def test_archived_reference_sha_and_pose_path_differences(self):
        self.assertEqual(cp370.SHA, "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a")
        self.assertEqual(cp370.SIZE, (1302, 2748))
        self.assertEqual(set(cp370.RAISED), set(cp370.KEYFRAME_NAMES))
        for part in cp370.KEYFRAME_NAMES:
            ET.fromstring(cp370.svg(part, 'raised'))
            self.assertNotEqual(cp370.svg(part, 'idle'), cp370.svg(part, 'raised'))

if __name__=='__main__':unittest.main(verbosity=2)
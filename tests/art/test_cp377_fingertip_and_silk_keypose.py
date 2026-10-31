"""CP377 local source and OpenRaster QA. No claim of visual or APK approval."""
import hashlib, importlib.util, io, json, tempfile, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
SRC=HERE/'cp377_fingertip_and_silk_keypose.py'
if not SRC.exists():
    SRC=HERE.parents[1]/'tools'/'art'/'cp377_fingertip_and_silk_keypose.py'
spec=importlib.util.spec_from_file_location('tvkcp377', SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
MAT=HERE/'CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png'
HAND=HERE/'14_left_hand_source.png'
OUT=HERE/'OUTPUT'
HAS_ART=all(p.exists() for p in [CAN,MAT,HAND])

class StaticTests(unittest.TestCase):
    def test_source_contract(self):
        self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.SIZE,(217,458));self.assertEqual(m.SIZE6,(1302,2748))
    def test_four_distinct_original_svg_pose_paths(self):
        self.assertEqual(len(m.POSE_ART),2)
        self.assertEqual(sum(len(p) for p in m.POSE_ART.values()),4)
        for p in m.POSE_ART.values():
            for name,content in p.items():
                self.assertIn('<path',content)
                s=m.svg(name,content)
                ET.fromstring(s)
                self.assertNotIn('<image',s)
                self.assertNotIn('data:image',s)
    def test_pose_shapes_are_different(self):
        idle=list(m.POSE_ART['idle'].values())
        raised=list(m.POSE_ART['raised'].values())
        self.assertNotEqual(idle[0],raised[0]);self.assertNotEqual(idle[1],raised[1])
    def test_bad_source_rejected_no_files(self):
        with tempfile.TemporaryDirectory() as folder:
            fake=Path(folder)/'incorrect.png'
            Image.new('RGBA',(941,1672),'white').save(fake)
            out=Path(folder)/'should_not_exist'
            with self.assertRaisesRegex(ValueError,'Wrong CANON'):
                m.make(fake,fake,fake,out)
            self.assertFalse(out.exists())

@unittest.skipUnless(HAS_ART,'Exact private CANON + CP374 hand/matte not in GitHub CI')
class AssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Prefer generated files verified during local handoff; otherwise regenerate once.
        if (OUT/'CP377_REPORT.json').exists():
            cls.output=OUT
            cls.report=json.loads((OUT/'CP377_REPORT.json').read_text())
            cls.tmp=None
        else:
            cls.tmp=tempfile.TemporaryDirectory()
            cls.output=Path(cls.tmp.name)/'rebuild'
            cls.report=m.make(CAN,MAT,HAND,cls.output)
    @classmethod
    def tearDownClass(cls):
        if cls.tmp is not None:cls.tmp.cleanup()
    def test_exact_source_sha_and_rgb(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.CANON_SHA)
        source,mat,arm=m.validate(CAN,MAT,HAND)
        self.assertTrue(np.array_equal(np.asarray(source.crop(m.FRONT))[:,:,:3],np.asarray(mat)[:,:,:3]))
        self.assertEqual(source.size,(941,1672))
    def test_two_ora_files_valid_9_visible_one_hidden(self):
        for pose in ('IDLE','RAISED'):
            fn=self.output/'ora'/f'CP377_{pose}_NINE_DRAWN_LAYERS_DRAFT_NOT_SPINE.ora'
            with zipfile.ZipFile(fn) as z:
                self.assertIsNone(z.testzip())
                nodes=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
                self.assertEqual(len(nodes),10)
                self.assertEqual(sum(v.get('visibility')=='visible' for v in nodes),9)
                self.assertEqual(sum(v.get('visibility')=='hidden' for v in nodes),1)
                self.assertIn('CANON_V2_1',nodes[-1].get('name'))
                self.assertEqual(Image.open(io.BytesIO(z.read('mergedimage.png'))).size,m.SIZE6)
    def test_finger_and_silk_independent_alpha_and_compositions(self):
        self.assertEqual(len(list((self.output/'png').glob('*.png'))),18)
        for pose in ('idle','raised'):
            names=list(m.POSE_ART[pose])
            self.assertEqual(len(names),2)
            for name in names:
                img=Image.open(self.output/'png'/f'{pose}__{name}.png').convert('RGBA')
                self.assertIsNotNone(img.getchannel('A').getbbox())
                self.assertGreater(np.count_nonzero(np.asarray(img.getchannel('A'))>128),2000)
        self.assertGreater(self.report['different_pose_pixels_6x'],10000)
    def test_carryover_seven_layers_unchanged_between_poses(self):
        for name in list(m.cp376.cp375.ART)+list(m.cp376.NEW_ART):
            a=(self.output/'png'/f'idle__{name}.png').read_bytes()
            b=(self.output/'png'/f'raised__{name}.png').read_bytes()
            self.assertEqual(hashlib.sha256(a).digest(),hashlib.sha256(b).digest())
    def test_cp376_baseline_not_blindly_zeroed(self):
        d=self.report['baseline_motion_diagnostics_unchanged']
        self.assertEqual([d[k]['cp376_baseline_uncovered_source_px'] for k in ['-6,3','-4,2','3,-2','-8,5']],[18,21,98,26])
        self.assertTrue(all(d[k]['cp377_silhouette_ignored_for_underpaint'] for k in d))
    def test_toes_reference_are_preserved_and_blocked_release(self):
        source,mat,_=m.validate(CAN,MAT,HAND)
        for box,expected in [((79,432,102,458),163),((109,414,122,446),146)]:
            a=np.asarray(source.crop(m.FRONT).crop(box))
            b=np.asarray(mat.crop(box))
            blue=(a[:,:,2]>a[:,:,0]*1.14)&(a[:,:,2]>a[:,:,1]*1.09)&(a[:,:,2]>90)
            visible=blue&(b[:,:,3]>=128)&(b[:,:,2]>b[:,:,0]*1.14)&(b[:,:,2]>b[:,:,1]*1.09)
            self.assertEqual(int(blue.sum()),expected)
            self.assertEqual(int(visible.sum()),expected)
        self.assertEqual(self.report['visual_qa'],'NOT_PASSED')
        self.assertEqual(self.report['production_release'],'blocked_pending_art')
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertFalse(self.report['full_motion_gap_free'])
        self.assertFalse(self.report['apk_ready'])

if __name__=='__main__':unittest.main(verbosity=2)
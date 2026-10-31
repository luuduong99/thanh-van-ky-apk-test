"""CP375 partial left wrist source-locked art tests, not aesthetic acceptance."""
import hashlib, importlib.util, io, json, tempfile, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE
SCRIPT=HERE/'cp375_hidden_wrist_art.py'
if not SCRIPT.exists():
    ROOT=HERE.parents[1]
    SCRIPT=ROOT/'tools'/'art'/'cp375_hidden_wrist_art.py'
spec=importlib.util.spec_from_file_location('cp375_art',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
MATTE=HERE/'CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png'
HAND=HERE/'14_left_hand_source.png'
if not CAN.exists():CAN=ROOT/'art_assets'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
HAS_ART=CAN.exists() and MATTE.exists() and HAND.exists()

class StaticContracts(unittest.TestCase):
    def test_canon_lock(self):
        self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.FRONT,(13,172,230,630))
        self.assertEqual(m.SIZE,(217,458))
        self.assertEqual(m.SIZE6,(1302,2748))
    def test_four_new_semantic_svg_paths(self):
        self.assertEqual(len(m.ART),4)
        for name in m.ART:
            svg=m.svg(name)
            ET.fromstring(svg)
            self.assertIn('<path',svg)
            self.assertNotIn('<image',svg)
            self.assertNotIn('data:image',svg)
    def test_invalid_canon_fails_before_output_created(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'fake.png';Image.new('RGBA',(941,1672),'white').save(fake)
            dest=Path(d)/'no_output'
            with self.assertRaisesRegex(ValueError,'Wrong CANON'):
                m.make(fake,fake,fake,dest)
            self.assertFalse(dest.exists())
    def test_release_stays_blocked_in_source(self):
        src=SCRIPT.read_text(encoding='utf8')
        self.assertIn("'visual_qa':'NOT_PASSED'",src)
        self.assertIn("'production_release':'blocked_pending_art'",src)
        self.assertIn("'full_motion_gap_free':False",src)
        self.assertIn("'full_character_redraw_complete':False",src)

@unittest.skipUnless(HAS_ART,'Private CANON/CP374 raster assets absent from CI')
class RealArtworkChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=tempfile.TemporaryDirectory()
        cls.out=Path(cls.folder.name)/'CP375'
        cls.report=m.make(CAN,MATTE,HAND,cls.out)
    @classmethod
    def tearDownClass(cls):cls.folder.cleanup()
    def test_source_sha_and_canvas(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.CANON_SHA)
        self.assertEqual(self.report['canvas_6x_for_drawn_svg'],[1302,2748])
    def test_new_art_layers_are_nonempty_independent(self):
        layers=list((self.out/'layers').glob('*.png'))
        self.assertEqual(len(layers),4)
        self.assertEqual(len({hashlib.sha256(x.read_bytes()).hexdigest() for x in layers}),4)
        for layer in layers:self.assertIsNotNone(Image.open(layer).getchannel('A').getbbox())
    def test_partial_gap_reduction_but_never_full_claim(self):
        self.assertEqual(self.report['underpaint_motion_local_gap_before_px'],204)
        self.assertGreater(self.report['underpaint_new_svg_alpha_coverage_of_old_gap_px'],0)
        self.assertLess(self.report['underpaint_motion_local_gap_remaining_px'],204)
        self.assertGreater(self.report['underpaint_motion_local_gap_remaining_px'],0)
        self.assertFalse(self.report['full_motion_gap_free'])
    def test_ora_real_4_visible_hidden_canon_and_crc(self):
        with zipfile.ZipFile(self.out/self.report['file_ora']) as z:
            self.assertIsNone(z.testzip())
            root=ET.fromstring(z.read('stack.xml'))
            layers=root.find('stack').findall('layer')
            self.assertEqual(len(layers),5)
            self.assertEqual(sum(x.get('visibility')=='visible' for x in layers),4)
            self.assertEqual(sum(x.get('visibility')=='hidden' for x in layers),1)
            self.assertIn('CANON',layers[-1].get('name',''))
            self.assertEqual(Image.open(io.BytesIO(z.read('mergedimage.png'))).size,(1302,2748))
    def test_source_toes_unaffected_and_preview_source_only(self):
        ref=m.validate_canon(CAN).crop(m.FRONT)
        original=Image.open(MATTE).convert('RGBA')
        source=np.asarray(ref); after=np.asarray(original)
        for roi,expected in [((79,432,102,458),163),((109,414,122,446),146)]:
            x1,y1,x2,y2=roi
            a=source[y1:y2,x1:x2]; b=after[y1:y2,x1:x2]
            blue=(a[:,:,2]>a[:,:,0]*1.14)&(a[:,:,2]>a[:,:,1]*1.09)&(a[:,:,2]>90)
            retained=blue&(b[:,:,3]>=128)&(b[:,:,2]>b[:,:,0]*1.14)&(b[:,:,2]>b[:,:,1]*1.09)
            self.assertEqual(int(blue.sum()),expected)
            self.assertEqual(int(retained.sum()),expected)
        self.assertTrue((self.out/'qa'/'CP375_CANON_V2_1_PARTIAL_PAINT_COMPARISON_NOT_APPROVED.png').exists())
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertFalse(self.report['spine_ready'])
        self.assertFalse(self.report['apk_ready'])

if __name__=='__main__':unittest.main(verbosity=2)
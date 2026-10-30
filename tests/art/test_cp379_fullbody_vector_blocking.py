"""CP379 reproducible contracts. Green structure tests do NOT approve character art."""
import hashlib, importlib.util, json, tempfile, unittest, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import numpy as np

HERE=Path(__file__).resolve().parent
MODULE=HERE/'cp379_fullbody_vector_blocking.py'
if not MODULE.exists(): MODULE=HERE.parents[1]/'tools'/'art'/'cp379_fullbody_vector_blocking.py'
spec=importlib.util.spec_from_file_location('cp379',MODULE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
MATTE=HERE/'CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png'
SOURCE=HERE/'CP374_SOURCE_LAYERS'
OUT=HERE/'OUTPUT'
HAS_SOURCE=CAN.exists() and MATTE.exists() and SOURCE.is_dir() and len(list(SOURCE.glob('*.png')))==19

class StaticContract(unittest.TestCase):
    def test_authorized_source_lock(self):
        self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.CANON_SIZE,(941,1672));self.assertEqual(m.FRONT,(13,172,230,630))
        self.assertEqual(m.CANVAS,(1302,2748))

    def test_new_semantic_fullbody_path_shapes_are_real_svg(self):
        self.assertEqual(len(m.ART),21)
        self.assertEqual(len({k for k,_ in m.ART}),21)
        for name,content in m.ART:
            with self.subTest(name=name):
                svg=m.svg_for(name)
                ET.fromstring(svg)
                self.assertIn('<path',content)
                self.assertNotIn('<image',svg)
                self.assertNotIn('href=',svg)
        for item in ['face','hair','bodice','leg','shoe','silk','arm','head']:
            self.assertTrue(any(item in name for name,_ in m.ART))

    def test_must_not_accept_wrong_canon_and_create_artifact(self):
        with tempfile.TemporaryDirectory() as root:
            fake=Path(root)/'fake.png';Image.new('RGBA',m.CANON_SIZE,'white').save(fake)
            out=Path(root)/'DO_NOT_CREATE'
            with self.assertRaisesRegex(ValueError,'CANON'):
                m.build(fake,'wrong.png','wrong',out)
            self.assertFalse(out.exists())

    def test_release_flags_are_explicitly_blocked_in_builder(self):
        s=MODULE.read_text(encoding='utf8')
        for mandatory in ["'visual_qa':'NOT_PASSED'", "'production_release':'blocked_pending_art'", "'sprite_paths':{}", "'spine_ready':False", "'apk_ready':False"]:
            self.assertIn(mandatory,s)

@unittest.skipUnless(HAS_SOURCE,'Private user-approved CANON and source layers are not available in public CI')
class RealArtworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.path=Path(cls.tmp.name)/'generated'
        cls.report=m.build(CAN,MATTE,SOURCE,cls.path)

    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()

    def test_real_approved_source_sha(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.CANON_SHA)
        with Image.open(CAN) as approved: self.assertEqual(approved.size,m.CANON_SIZE)

    def test_two_independent_ora_formats_layers_and_crc(self):
        for filename,n in [('CP379_SOURCE_19_PARTS_NOT_RIG.ora',20),('CP379_21_AUTHORED_FULLBODY_BLOCKING_DRAFT_NOT_RIG.ora',22)]:
            with self.subTest(filename=filename):
                with zipfile.ZipFile(self.path/'ora'/filename) as z:
                    self.assertIsNone(z.testzip())
                    ls=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
                    self.assertEqual(len(ls),n)
                    self.assertEqual(sum(x.get('visibility')=='hidden' for x in ls),1)
                    self.assertIn('CANON_EXACT',ls[-1].get('name'))

    def test_each_of_21_drawn_layers_has_visible_independent_alpha(self):
        layers=list((self.path/'painted').glob('*.png'))
        self.assertEqual(len(layers),21)
        sigs=[]
        for f in layers:
            with Image.open(f) as im:
                self.assertEqual(im.size,m.CANVAS)
                alpha=im.getchannel('A')
                self.assertIsNotNone(alpha.getbbox())
                sigs.append(hashlib.sha256(alpha.tobytes()).hexdigest())
        self.assertGreaterEqual(len(set(sigs)),20)

    def test_source_guide_is_exact_cp374_matte_without_claiming_repaint(self):
        self.assertTrue(self.report['source_trace_matches_cp374_matte_at_rest'])
        self.assertFalse(self.report['true_native_painted_highdetail_fullbody'])
        self.assertEqual(len(list((self.path/'guide_regions').glob('*.png'))),19)

    def test_both_blue_shoes_preserved_in_source_not_claimed_in_runtime(self):
        checks=self.report['toe_source_checks']
        self.assertEqual(checks['image_left']['blue_visible_px'],163)
        self.assertEqual(checks['image_right']['blue_visible_px'],146)
        self.assertTrue(all(x['pass'] for x in checks.values()))

    def test_rendered_fullbody_draft_has_head_torso_and_feet(self):
        merged=np.asarray(Image.open(self.path/'qa'/'CP379_FULLBODY_VECTOR_BLOCKING_TRANSPARENT_NOT_APPROVED.png').convert('RGBA'))
        alpha=merged[:,:,3]>128
        # Ensure actual broad full-body geometry across head, torso, legs and toes.
        self.assertGreater(int(alpha[20*6:90*6].sum()),1000)
        self.assertGreater(int(alpha[100*6:220*6].sum()),1000)
        self.assertGreater(int(alpha[230*6:448*6].sum()),1000)

    def test_release_is_blocked_even_if_tests_pass(self):
        r=self.report
        self.assertEqual(r['visual_qa'],'NOT_PASSED')
        self.assertEqual(r['production_release'],'blocked_pending_art')
        self.assertEqual(r['sprite_paths'],{})
        self.assertFalse(r['semantic_hidden_underpaint_complete'])
        self.assertFalse(r['motion_approved'])
        self.assertFalse(r['apk_ready'])

    def test_comparison_uses_only_approved_canon_and_same_character_draft(self):
        self.assertTrue((self.path/'qa'/'CP379_CANON_FULLBODY_VECTOR_COMPARISON_NOT_APPROVED.png').exists())
        self.assertTrue((self.path/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').exists())
        self.assertEqual(hashlib.sha256((self.path/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes()).hexdigest(),m.CANON_SHA)

if __name__=='__main__':unittest.main(verbosity=2)
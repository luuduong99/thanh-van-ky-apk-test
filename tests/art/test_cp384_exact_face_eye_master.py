"""CP384 source-exact static portrait structure checks; no approval of blink or high-res painting."""
import importlib.util, json, tempfile, unittest, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
SCRIPT=HERE/'cp384_exact_face_eye_master.py'
if not SCRIPT.exists():SCRIPT=HERE.parents[1]/'tools/art/cp384_exact_face_eye_master.py'
spec=importlib.util.spec_from_file_location('cp384',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CANON=HERE/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
if not CANON.exists():CANON=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
HAS_CANON=CANON.exists()

class StaticContract(unittest.TestCase):
    def test_locked_source_and_regions(self):
        self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.PORTRAIT_BBOX,(25,684,193,881))
        self.assertEqual(len(m.EYE_ROIS),2)
    def test_invalid_canon_rejected_before_output_creation(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'wrong.png';Image.new('RGBA',m.CANON_SIZE,(255,255,255,255)).save(fake)
            target=Path(d)/'should_not_exist'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                m.create(fake,target)
            self.assertFalse(target.exists())
    def test_painter_release_gates_remain_explicit(self):
        import inspect
        code=inspect.getsource(m.create)
        self.assertIn('blocked_pending_art',code)
        self.assertIn("'face_painting_approved':False",code)
        self.assertIn("'blink_animation_verified':False",code)

@unittest.skipUnless(HAS_CANON,'Private user-approved CANON must not be committed to GitHub')
class VerifiedSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.tmp.name)/'generated'
        cls.result=m.create(CANON,cls.root)
        cls.orig=np.array(Image.open(CANON).crop(m.PORTRAIT_BBOX).convert('RGBA'))
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_canon_static_exact_recomposition(self):
        merged=np.array(Image.open(self.root/'CP384_STATIC_SOURCE_EXACT_MASTER.png'))
        self.assertTrue(np.array_equal(merged,self.orig))
    def test_exact_reference_unchanged(self):
        with Image.open(self.root/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png') as im:
            self.assertEqual(im.size,m.CANON_SIZE)
        self.assertEqual((self.root/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes(), CANON.read_bytes())
    def test_eyes_mouth_masks_non_overlapping(self):
        masks=[np.array(Image.open(self.root/'art_layers'/f'{x}_editable_mask.png'))>0 for x in ['left_eye','right_eye','mouth']]
        count=sum(m.astype('uint8') for m in masks)
        self.assertLessEqual(count.max(),1)
        self.assertGreater(int((count>0).sum()),100)
    def test_underpaint_preserves_all_rgb_outside_regions(self):
        base=np.array(Image.open(self.root/'art_layers'/'00_technical_inpaint_underpaint_NOT_APPROVED.png'))
        masks=np.maximum.reduce([np.array(Image.open(self.root/'art_layers'/f'{x}_editable_mask.png')) for x in ['left_eye','right_eye','mouth']])>0
        self.assertTrue(np.array_equal(base[:,:,:3][~masks],self.orig[:,:,:3][~masks]))
        self.assertTrue(np.array_equal(base[:,:,3],self.orig[:,:,3]))
    def test_ora_crc_and_flags(self):
        p=self.root/'CP384_CANON_EXACT_FACE_EDITABLE_EYES_TECH_NOT_RIG.ora'
        with zipfile.ZipFile(p) as z:
            self.assertIsNone(z.testzip())
            node=ET.fromstring(z.read('stack.xml'))
            ls=node.find('stack').findall('layer')
            self.assertEqual(len(ls),7)
            self.assertEqual(sum(l.attrib['visibility']=='hidden' for l in ls),3)
            self.assertTrue(np.array_equal(np.array(Image.open(z.open('mergedimage.png')).convert('RGBA')),self.orig))
    def test_blink_is_draft_not_accepted(self):
        output=np.array(Image.open(self.root/'qa'/'CP384_BLINK_TECHNICAL_DRAFT_NOT_APPROVED.png'))
        self.assertGreater(int(np.count_nonzero(np.any(output!=self.orig,axis=2))),50)
        self.assertFalse(self.result['face_painting_approved'])
        self.assertFalse(self.result['blink_animation_verified'])
    def test_release_blocked_and_canvas_small(self):
        self.assertEqual(self.result['production_release'],'blocked_pending_art')
        self.assertEqual(self.result['sprite_paths'],{})
        self.assertFalse(self.result['portrait_background_transparent'])
        self.assertEqual(self.result['portrait_native_size'],[168,197])

if __name__=='__main__':unittest.main(verbosity=2)
import importlib.util, hashlib, json, tempfile, unittest
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
SCRIPT=HERE/'cp383_canon_portrait_staging.py'
if not SCRIPT.exists(): SCRIPT=HERE.parents[1]/'tools'/'art'/'cp383_canon_portrait_staging.py'
spec=importlib.util.spec_from_file_location('cp383',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=HERE/'previous'/'inputs'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
if not CAN.exists(): CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
HAS_SOURCE=CAN.exists()
class Static(unittest.TestCase):
    def test_source_contract_geometry(self):
        self.assertEqual(len(m.CROPS),5)
        self.assertEqual(m.CANON_DIM,(941,1672))
        self.assertEqual(m.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
    def test_wrong_source_has_no_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'fake.png';Image.new('RGBA',m.CANON_DIM,'red').save(fake)
            dest=Path(d)/'must_not_exist'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                m.build(fake,dest)
            self.assertFalse(dest.exists())
    def test_exact_expression_coordinate_roles(self):
        self.assertEqual(m.CROPS[3][2],(561,681,737,884))
        self.assertTrue(all((b[3]-b[1])==203 for _,_,b in m.CROPS))
        self.assertEqual(len(set(n for n,_,_ in m.CROPS)),5)

@unittest.skipUnless(HAS_SOURCE,'Private exact CANON V2.1 is not available on public CI')
class RealSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=tempfile.TemporaryDirectory();cls.root=Path(cls.d.name)/'generated'
        cls.report=m.build(CAN,cls.root);cls.sheet=np.asarray(m.validate(CAN))
    @classmethod
    def tearDownClass(cls): cls.d.cleanup()
    def test_five_exact_crops_source_pixels(self):
        for name,label,(x1,y1,x2,y2) in m.CROPS:
            crop=np.asarray(Image.open(self.root/'portraits'/f'{name}_CANON_EXACT.png').convert('RGBA'))
            np.testing.assert_array_equal(crop,self.sheet[y1:y2,x1:x2])
    def test_inner_ui_crops_are_only_source_pixels(self):
        for name,_,(x1,y1,x2,y2) in m.CROPS:
            inner=np.asarray(Image.open(self.root/'portraits'/f'{name}_INNER_CROP_SOURCE_ONLY.png'))
            np.testing.assert_array_equal(inner,self.sheet[y1+3:y2-3,x1+3:x2-3])
    def test_atlas_source_pixel_equivalence(self):
        atlas=np.asarray(Image.open(self.root/'PORTRAIT_ATLAS_EXACT_SOURCE_ONLY.png'))
        for rec in self.report['assets']:
            x,y,w,h=rec['atlas_rect_px'];src=np.asarray(Image.open(self.root/rec['exact_crop_filename']))
            np.testing.assert_array_equal(atlas[y:y+h,x:x+w],src)
    def test_gaps_in_atlas_transparent(self):
        atlas=np.asarray(Image.open(self.root/'PORTRAIT_ATLAS_EXACT_SOURCE_ONLY.png'))
        self.assertTrue(np.all(atlas[:,:12,3]==0))
        self.assertTrue(np.all(atlas[:, -12:,3]==0))
    def test_previews_use_only_source_character(self):
        for name in ['CP383_CANON_ONLY_PORTRAIT_PREVIEW.png','CP383_LANDSCAPE_DIALOGUE_CANON_STATIC_PREVIEW.png']:
            self.assertTrue((self.root/'qa'/name).exists())
            with Image.open(self.root/'qa'/name) as check:
                self.assertGreaterEqual(check.width,1500)
    def test_release_and_semantic_art_remain_blocked(self):
        self.assertEqual(self.report['production_release'],'blocked_pending_art')
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertFalse(self.report['rig_or_spine_ready'])
        self.assertTrue(self.report['not_an_artist_painted_new_face'])
        self.assertFalse(self.report['apk_ready'])
        self.assertEqual(len(self.report['assets']),5)
if __name__=='__main__': unittest.main(verbosity=2)
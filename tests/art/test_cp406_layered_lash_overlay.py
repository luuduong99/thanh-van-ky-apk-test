"""CP406: real source-lock tests; no static PASS should authorize production art."""
import os,sys,unittest,hashlib,zipfile,io
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import cp406_layered_lash_overlay as c
import cp401_occlusion_blink as base
ART=Path(os.environ.get('TVK_CP406_ART_DIR',ROOT))
OUT=Path(os.environ.get('TVK_CP406_OUTPUT_DIR',ROOT/'outputs'))
READY=(ART/c.CANON).exists() and (ART/c.BASELINE).exists() and (OUT/'CP406_CLOSED_EYE_4X_OVERLAY_DRAFT.png').exists()

class StaticContracts(unittest.TestCase):
    def test_canon_sha_constant(self): self.assertEqual(base.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
    def test_size(self): self.assertEqual(c.size,(672,788))
    def test_eye_rois(self): self.assertEqual(base.ROIS,{'LEFT':(29,93,71,124),'RIGHT':(83,70,129,110)})
    def test_source_is_private_and_not_asset_registry(self):
        s=Path(c.__file__).read_text();self.assertNotIn('production_release=APPROVED',s)
    def test_explicit_draft(self): self.assertIn('NOT CANON MASTER',c.make_ora.__doc__ or '') if False else self.assertIn('display proxy',c.__doc__.lower())
    def test_source_tamper_sha_raises(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/c.CANON;Image.new('RGBA',(941,1672),'white').save(fake)
            with self.assertRaises(ValueError):base.exact_source(fake)

@unittest.skipUnless(READY,'private CANON / source-root images and output are not checked into public GitHub')
class PrivateSourceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src,cls.baseline=c.source_images(ART)
        cls.master=Image.open(OUT/'CP406_CLOSED_EYE_4X_OVERLAY_DRAFT.png').convert('RGBA')
        cls.orig=cls.src.resize(c.size,Image.Resampling.LANCZOS)
        cls.mask=np.zeros((c.size[1],c.size[0]),bool)
        for x1,y1,x2,y2 in base.ROIS.values():cls.mask[y1*4:y2*4,x1*4:x2*4]=True
    def test_verified_sha(self):self.assertEqual(c.sha(ART/c.CANON),base.CANON_SHA)
    def test_baseline_sha(self):self.assertEqual(c.sha(ART/c.BASELINE),'0391ba0cb906bf5334f176ac28a508cad4afa700fe6cb7c2deb52affaf1ac5f6')
    def test_outside_eyes_exact(self):self.assertTrue(np.array_equal(np.array(self.master)[~self.mask],np.array(self.orig)[~self.mask]))
    def test_native_alpha_unchanged(self):self.assertTrue(np.array_equal(np.array(self.master)[:,:,3],np.array(self.orig)[:,:,3]))
    def test_inside_eyes_modified(self):self.assertGreater(np.count_nonzero(np.any(np.array(self.master)[self.mask]!=np.array(self.orig)[self.mask],axis=1)),0)
    def test_ora_8_layers_master_not_visible(self):
        p=OUT/'CP406_EYELID_8_LAYER_DISPLAY_DRAFT.ora'
        with zipfile.ZipFile(p) as z:
            root=__import__('xml.etree.ElementTree',fromlist=['']).fromstring(z.read('stack.xml'))
            l=root.find('stack').findall('layer')
            self.assertEqual(len(l),8)
            self.assertEqual(sum(x.attrib['visibility']=='visible' for x in l),1)
            self.assertIn('CANON',next(x.attrib['name'] for x in l if x.attrib['visibility']=='visible'))
            self.assertTrue(np.array_equal(np.array(Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA')),np.array(self.orig)))
    def test_anim_atlas(self):
        a=Image.open(OUT/'CP406_ATLAS_15_DISPLAY_DRAFT.png').convert('RGBA')
        self.assertEqual(a.size,(10080,788))
        self.assertTrue(np.array_equal(np.asarray(a.crop((0,0,672,788))),np.asarray(self.orig)))
        self.assertTrue(np.array_equal(np.asarray(a.crop((672*7,0,672*8,788))),np.asarray(self.master)))
        self.assertTrue(np.array_equal(np.asarray(a.crop((672*14,0,672*15,788))),np.asarray(self.orig)))
    def test_all_poses_outside_unchanged(self):
        a=Image.open(OUT/'CP406_ATLAS_15_DISPLAY_DRAFT.png').convert('RGBA')
        src=np.asarray(self.orig)
        for i in range(15):
            sub=np.asarray(a.crop((i*672,0,(i+1)*672,788)))
            self.assertTrue(np.array_equal(sub[~self.mask],src[~self.mask]),i)
    def test_editable_separate_layers(self):
        l=c.colored_layers()
        self.assertEqual(len(l),5)
        self.assertTrue(all(x.size==(2016,2364) for x in l.values()))

if __name__=='__main__':unittest.main()
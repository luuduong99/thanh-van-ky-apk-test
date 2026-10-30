"""CP414 artist handoff technical guards. Not evidence of art approval."""
import importlib.util, json, os, unittest, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image

REPO=Path(__file__).resolve().parents[2]
SCRIPT=REPO/'tools/art/cp414_canon_semantic_layers.py'
SOURCE=Path(os.environ.get('TVK_CANON_V21_FILE',str(REPO/'original/LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
OUT=REPO/'outputs'
spec=importlib.util.spec_from_file_location('cp414',SCRIPT)
cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)

class PublicSourceContract(unittest.TestCase):
    def test_static_canon_lock(self):
        self.assertEqual(cp.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(cp.CANON_DIMS,(941,1672))
        self.assertEqual(cp.FRONT_RECT,(16,180,224,623))
    def test_regions_constrained_to_real_front(self):
        self.assertEqual(len(cp.REGIONS),11)
        self.assertTrue(all(0<=x<208 and 0<=y<443 for pts in cp.REGIONS.values() for x,y in pts))
    def test_face_and_eyes_have_same_pose_coords(self):
        self.assertIn('02_face_cheeks',cp.REGIONS)
        self.assertIn('03_left_open_eye_source',cp.REGIONS)
        self.assertIn('04_right_open_eye_source',cp.REGIONS)
        self.assertNotEqual(cp.FRONT_RECT,(25,684,193,881))
    def test_underpaint_and_closed_eyes_explicitly_empty(self):
        self.assertEqual(len(cp.ARTIST_EMPTY),2)
        self.assertIn('UNDERPAINT_EMPTY',cp.ARTIST_EMPTY[0])
        self.assertIn('EYELIDS',cp.ARTIST_EMPTY[1])
    def test_extracted_polygon_makes_alpha_honestly(self):
        source=Image.new('RGBA',cp.FRONT_SIZE,(16,32,64,255))
        result=cp.extract(source,[(9,9),(20,9),(20,20),(9,20)])
        array=np.asarray(result)
        self.assertTrue((array[:,:,0]==16).all())
        self.assertGreater((array[:,:,3]>0).sum(),100)
        self.assertEqual(int(array[0,0,3]),0)
    def test_no_production_spine_claim(self):
        txt=SCRIPT.read_text(encoding='utf-8')
        self.assertIn("'rig_ready':False",txt)
        self.assertIn("'has_new_painter_art':False",txt)
        self.assertIn("'android_device_verified':False",txt)

@unittest.skipUnless(SOURCE.is_file(),'Private exact CANON not present in public GitHub repo')
class PrivateArtSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full=cp.load(SOURCE)
        cls.front=cls.full.crop(cp.FRONT_RECT)
    def test_source_sha(self):
        self.assertEqual(cp.sha(SOURCE),cp.CANON_SHA)
    def test_corrupt_hash_fail_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'tampered.png'
            b=SOURCE.read_bytes()
            f.write_bytes(b[:-1]+bytes([b[-1]^1]))
            with self.assertRaisesRegex(ValueError,'raw sha256'):cp.load(f)
    def test_each_source_sample_keeps_original_rgb_exact(self):
        original=np.asarray(self.front)
        for name,polygon in cp.REGIONS.items():
            p=np.asarray(cp.extract(self.front,polygon))
            mask=p[:,:,3]>0
            self.assertGreater(int(mask.sum()),20,name)
            self.assertTrue(np.array_equal(p[mask,:3],original[mask,:3]),name)
    def test_ora_source_visible_only_and_pixel_exact(self):
        path=OUT/'CP414_SOURCE_PIXEL_LAYERS_NOT_RIG_READY.ora'
        with zipfile.ZipFile(path) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(z.read('mimetype'),b'image/openraster')
            root=ET.fromstring(z.read('stack.xml'))
            layers=root.find('stack').findall('layer')
            self.assertEqual(len(layers),14)
            self.assertEqual(sum(k.attrib['visibility']=='visible' for k in layers),1)
            self.assertTrue(layers[-1].attrib['name'].startswith('00 EXACT CANON'))
            merged=np.asarray(Image.open(z.open('mergedimage.png')).convert('RGBA'))
            self.assertTrue(np.array_equal(merged,np.asarray(self.front)))
            for k in layers[-3:-1]:
                x=np.asarray(Image.open(z.open(k.attrib['src'])).convert('RGBA'))
                self.assertEqual(int(np.count_nonzero(x[:,:,3])),0)
    def test_report_not_promoted_to_runtime(self):
        j=json.loads((OUT/'CP414_REPORT.json').read_text())
        self.assertEqual(j['layers_nonempty_source_sampled'],11)
        self.assertEqual(j['layers_blank_artist_required'],2)
        self.assertFalse(j['has_artist_neck_underpaint'])
        self.assertFalse(j['has_artist_correct_pose_eyes_closed'])
        self.assertFalse(j['rig_ready'])
        self.assertEqual(j['production_release']['sprite_paths'],{})
        self.assertEqual(j['production_release']['status'],'blocked_pending_art')
if __name__=='__main__':unittest.main()
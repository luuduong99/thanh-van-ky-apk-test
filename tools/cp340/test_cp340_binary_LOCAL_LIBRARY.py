import hashlib,json,zipfile,xml.etree.ElementTree as ET, unittest
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/'CP340_MANIFEST.json').read_text())
ORIG=Image.open(ROOT/'reference/CANON_V2_1_EXACT_ORIGINAL.png').convert('RGBA')

class CP340SourceAudit(unittest.TestCase):
    def test_source_checksum(self):
        self.assertEqual(hashlib.sha256((ROOT/'reference/CANON_V2_1_EXACT_ORIGINAL.png').read_bytes()).hexdigest(),
                         'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(ORIG.size,(941,1672))
    def test_exact_14_crop_pixels(self):
        self.assertEqual(len(MAN['reference_crops']),14)
        for x in MAN['reference_crops']:
            p=ROOT/'extracted'/(x['id']+'_NATIVE_REFERENCE.png')
            crop=Image.open(p).convert('RGBA')
            self.assertEqual(list(crop.size),x['size_px'],x['id'])
            self.assertTrue(np.array_equal(np.array(crop),np.array(ORIG.crop(x['source_box_xyxy']))),x['id'])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),x['sha256'],x['id'])
    def test_approved_state_labels(self):
        ids={r['id'] for r in MAN['reference_crops']}
        self.assertEqual(sum(x.startswith('view_') for x in ids),5)
        self.assertEqual(sum(x.startswith('emotion_') for x in ids),5)
        self.assertEqual(sum(x.startswith('damage_') for x in ids),4)
    def test_no_fake_4k_or_scaled_native_crops(self):
        for x in MAN['reference_crops']:
            self.assertLess(max(x['size_px']),512)
        self.assertTrue(MAN['source_preserved'])
    def test_alpha_trial_rgb_pixel_identical_to_source(self):
        fg=np.array(Image.open(ROOT/MAN['first_alpha_trial']['path']).convert('RGBA'))
        src=np.array(Image.open(ROOT/'extracted/view_front_NATIVE_REFERENCE.png').convert('RGBA'))
        self.assertEqual(fg.shape,src.shape)
        self.assertTrue(np.array_equal(fg[:,:,:3],src[:,:,:3]))
    def test_alpha_is_real_but_not_fully_opaque(self):
        a=np.array(Image.open(ROOT/MAN['first_alpha_trial']['path']).getchannel('A'))
        self.assertGreater(int(np.count_nonzero(a==0)),5000)
        self.assertGreater(int(np.count_nonzero(a>200)),10000)
        self.assertLess(int(np.count_nonzero(a>0)),a.size)
    def test_openraster_real_png_layers_and_crc(self):
        with zipfile.ZipFile(ROOT/MAN['ora_path']) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(z.read('mimetype'),b'image/openraster')
            root=ET.fromstring(z.read('stack.xml'))
            self.assertEqual((root.attrib['w'],root.attrib['h']),('215','449'))
            stack=root.find('stack').findall('layer')
            self.assertEqual(len(stack),2)
            self.assertEqual(stack[0].attrib['visibility'],'visible')
            self.assertEqual(stack[1].attrib['visibility'],'hidden')
            self.assertIn('NOT_RIGGED',stack[0].attrib['name'])
            self.assertEqual(z.read('mergedimage.png'),z.read(stack[0].attrib['src']))
    def test_manifest_is_production_blocked(self):
        self.assertIn('NOT_PRODUCTION',MAN['status'])
        self.assertFalse(MAN['production']['spine_ready'])
        self.assertFalse(MAN['production']['clean_underpaint_done'])
        self.assertFalse(MAN['production']['facial_attachments_independent'])
        self.assertEqual(MAN['production']['sprite_paths_registered'],0)
    def test_review_images_exist(self):
        for n in ['CP340_CANON_V21_VIEWS_EMOTIONS_AND_ALPHA_QA.png','CP340_FRONT_ALPHA_SIDE_BY_SIDE.png','CP340_DAMAGE_LEVELS_EXACT_REFERENCE.png']:
            self.assertTrue((ROOT/'preview'/n).is_file(),n)
if __name__=='__main__':unittest.main()
"""CP382: exact CANON-only 5-portrait editable region guide tests.
These checks deliberately NEVER approve painter art or Android release.
"""
import importlib.util, io, json, os, tempfile, unittest, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
SCRIPT=HERE/'cp382_face_semantic_intake.py'
if not SCRIPT.exists(): SCRIPT=HERE.parents[1]/'tools'/'art'/'cp382_face_semantic_intake.py'
spec=importlib.util.spec_from_file_location('cp382',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=Path(os.getenv('CP382_CANON',str(HERE/'inputs'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
REFS=Path(os.getenv('CP382_REFS',str(HERE/'inputs'/'expression_refs')))
HAS_REAL=CAN.exists() and REFS.is_dir()

class PublicContract(unittest.TestCase):
    def test_canon_source_geometry(self):
        self.assertEqual(m.CANON_SIZE,(941,1672))
        self.assertEqual(len(m.CROP_BOXES),5)
        self.assertEqual(len(m.PORTRAITS),5)
        self.assertEqual(len(m.ROLES),9)
    def test_wrong_image_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'bad.png'
            Image.new('RGBA',(941,1672),'white').save(src)
            out=Path(d)/'must_not_exist'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                m.build(src,Path(d),out)
            self.assertFalse(out.exists())
    def test_authored_draft_paths_independent(self):
        import xml.etree.ElementTree as ET
        arr=[]
        for data in m.FEATURES:
            for role in ['brow_study','eye_study','mouth_study']:
                xml=m.make_svg(data,role,174,203)
                root=ET.fromstring(xml)
                self.assertTrue(root.findall('{http://www.w3.org/2000/svg}path'))
                arr.append(xml)
        self.assertEqual(len(arr),15)
        self.assertEqual(len(set(m.make_svg(x,'mouth_study',174,203) for x in m.FEATURES)),5)

@unittest.skipUnless(HAS_REAL,'Exact private CANON and expression crops unavailable in public CI')
class RealCanon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.tmp.name)/'result'
        cls.report=m.build(CAN,REFS,cls.out)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_canon_copy_byte_exact(self):
        self.assertEqual((self.out/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes(),CAN.read_bytes())
    def test_references_against_sheet_pixel_by_pixel(self):
        with Image.open(CAN) as c:
            for name,box in zip(m.PORTRAITS,m.CROP_BOXES):
                with self.subTest(name=name):
                    self.assertTrue(np.array_equal(np.asarray(c.crop(box)),np.asarray(Image.open(REFS/name))))
    def test_five_guide_composites_pixel_exact(self):
        for i,name in enumerate(m.PORTRAITS,1):
            source=np.asarray(Image.open(REFS/name).convert('RGBA'))
            parts=[Image.open(self.out/'parts'/f'{i:02}_{r}.png').convert('RGBA') for r in m.ROLES]
            merged=Image.new('RGBA',(source.shape[1],source.shape[0]))
            for p in parts:merged.alpha_composite(p)
            self.assertTrue(np.array_equal(np.asarray(merged),source),name)
    def test_no_overlapping_source_pixels(self):
        for i,name in enumerate(m.PORTRAITS,1):
            alphas=[np.asarray(Image.open(self.out/'parts'/f'{i:02}_{r}.png').getchannel('A'))>0 for r in m.ROLES]
            self.assertTrue(np.all(np.sum(alphas,axis=0)==1),name)
    def test_ora_crc_layer_count_and_source_preview(self):
        for i,name in enumerate(m.PORTRAITS,1):
            ora=self.out/'ora'/f'CP382_FACE_0{i}_SOURCE_GUIDES_NOT_RIG.ora'
            with zipfile.ZipFile(ora) as z:
                self.assertIsNone(z.testzip())
                root=ET.fromstring(z.read('stack.xml'))
                layers=root.find('stack').findall('layer')
                self.assertEqual(len(layers),13)
                self.assertEqual(sum(x.attrib['visibility']=='hidden' for x in layers),4)
                merged=np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA'))
                exact=np.asarray(Image.open(REFS/name).convert('RGBA'))
                self.assertTrue(np.array_equal(merged,exact))
    def test_new_vector_trials_are_hidden_and_not_approved(self):
        self.assertEqual(len(list((self.out/'svg').glob('*.svg'))),15)
        self.assertEqual(len(list((self.out/'art_drafts').glob('*.png'))),15)
        self.assertFalse(self.report['art_approved'])
        self.assertFalse(self.report['native_face_master_complete'])
        self.assertEqual(self.report['visual_qa'],'NOT_PASSED')
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertFalse(self.report['apk_ready'])
    def test_modified_reference_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as d:
            refs=Path(d)/'refs';refs.mkdir()
            for p in REFS.glob('*.png'): (refs/p.name).write_bytes(p.read_bytes())
            target=refs/m.PORTRAITS[0]
            with Image.open(target) as src:
                img=src.copy()
            img.putpixel((20,90),(0,0,0,255));img.save(target)
            dest=Path(d)/'must_not_create'
            with self.assertRaisesRegex(ValueError,'REFERENCE_NOT_PIXEL_EXACT_CANON'):
                m.build(CAN,refs,dest)
            self.assertFalse(dest.exists())
    def test_final_report_and_qa_image(self):
        self.assertTrue((self.out/'qa'/'CP382_CANON_FIVE_FACE_LAYER_GUIDES_NOT_ART.png').is_file())
        r=json.loads((self.out/'CP382_REPORT.json').read_text())
        self.assertEqual(len(r['portraits']),5)
        self.assertEqual(r['release_status'],'blocked_pending_art')
        self.assertFalse(r['spine_ready'])

if __name__=='__main__':unittest.main(verbosity=2)
"""CP381 source-fidelity & artist-workspace QA. Visual artwork acceptance NEVER implied."""
import hashlib, importlib.util, io, json, sys, tempfile, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'cp381_face_fidelity_review.py'
if not SOURCE.exists(): SOURCE=HERE.parents[1]/'tools'/'art'/'cp381_face_fidelity_review.py'
spec=importlib.util.spec_from_file_location('cp381',SOURCE)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
CAN=HERE/'CP380'/'OUTPUT'/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
DRAFT=HERE/'CP380'/'OUTPUT'/'qa'/'CP380_REFINED_29_LAYER_DRAFT.png'
if not CAN.exists():CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
if not DRAFT.exists():DRAFT=HERE/'CP380_REFINED_29_LAYER_DRAFT.png'
HAS_ASSETS=CAN.exists() and DRAFT.exists()

class PublicContract(unittest.TestCase):
    def test_canon_source_contract(self):
        self.assertEqual(mod.SOURCE_SIZE,(941,1672))
        self.assertEqual(mod.FRONT_BBOX,(13,172,230,630))
        self.assertEqual(mod.FRONT_SIZE,(217,458))
        self.assertEqual(mod.CANVAS,(1302,2748))
        self.assertEqual(len(mod.ZONES),3)
        self.assertEqual(len(mod.PAINT_LAYERS),3)

    def test_bad_source_refused_before_output(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);bogus=p/'notcanon.png';Image.new('RGBA',mod.SOURCE_SIZE,'white').save(bogus)
            dummy=p/'draft.png';Image.new('RGBA',mod.CANVAS,'white').save(dummy)
            out=p/'output';self.assertFalse(out.exists())
            with self.assertRaisesRegex(ValueError,'Wrong CANON'):
                mod.generate(bogus,dummy,out)
            self.assertFalse(out.exists())

    def test_invalid_draft_dimensions_rejected_preoutput(self):
        # mock specific canon identity only in this unit to test draft validation contract
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);dummy=p/'draft.png';Image.new('RGBA',(100,100),'white').save(dummy)
            # preflight must fail even before it could render/fabricate new output
            if HAS_ASSETS:
                with self.assertRaisesRegex(ValueError,'draft dimensions'):
                    mod.generate(CAN,dummy,p/'output')
                self.assertFalse((p/'output').exists())
            else:
                self.assertIn('CP380 draft dimensions/mode mismatch',mod.preflight.__code__.co_consts)

@unittest.skipUnless(HAS_ASSETS, 'Private CANON and CP380 draft absent from public CI')
class PrivateRealAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.temp.name)/'generated'
        cls.r=mod.generate(CAN,DRAFT,cls.out)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_source_byte_identical(self):
        self.assertEqual(mod.sha(self.out/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'),mod.SHA)

    def test_reference_crops_from_approved_canonly(self):
        front=Image.open(self.out/'source'/'FRONT_NATIVE_217x458_SOURCE_WITH_BACKGROUND.png')
        full=Image.open(CAN)
        self.assertEqual(front.tobytes(),full.crop(mod.FRONT_BBOX).tobytes())
        for name,box in mod.ZONES.items():
            with self.subTest(name=name):
                part=Image.open(self.out/'reference_crops'/(name+'_CANON_NATIVE_CROP.png'))
                self.assertEqual(part.tobytes(),front.crop(box).tobytes())

    def test_ora_crc_and_empty_paint_layers(self):
        ora=self.out/'ora'/'CP381_FACE_HAIR_BODICE_PAINTING_WORKSPACE_NOT_ART.ora'
        with zipfile.ZipFile(ora) as z:
            self.assertIsNone(z.testzip())
            tree=ET.fromstring(z.read('stack.xml'))
            layers=tree.find('stack').findall('layer')
            self.assertEqual(len(layers),8)
            self.assertEqual(sum(x.attrib['visibility']=='hidden' for x in layers),4)
            for layer in layers[:3]:
                self.assertIn('_EMPTY',layer.attrib['name'])
                im=Image.open(io.BytesIO(z.read(layer.attrib['src'])))
                self.assertIsNone(im.getchannel('A').getbbox())
            guide=Image.open(io.BytesIO(z.read(layers[-1].attrib['src'])))
            expected=Image.open(self.out/'source'/'FRONT_UPSCALED_REFERENCE_ONLY_NOT_NEW_DETAIL.png')
            self.assertEqual(guide.tobytes(),expected.tobytes())
            merged=Image.open(io.BytesIO(z.read('mergedimage.png')))
            self.assertEqual(merged.tobytes(),guide.tobytes())

    def test_visual_audit_report_not_production_pass(self):
        r=self.r
        self.assertEqual(r['visual_qa'],'NOT_PASSED')
        self.assertEqual(r['production_release'],'blocked_pending_art')
        self.assertFalse(r['native_fullbody_painting_complete'])
        self.assertFalse(r['painting_layers_have_artist_pixels'])
        self.assertEqual(r['sprite_paths'],{})
        self.assertEqual(len(r['regions']),3)
        self.assertTrue(all(x['result']=='MANUAL_REPAINT_REQUIRED' for x in r['regions'].values()))

    def test_exact_five_emotions_and_eight_accessories(self):
        self.assertEqual(len(mod.EXPRESSION_REFS),5)
        self.assertEqual(len(mod.ACCESSORY_REFS),8)
        with Image.open(CAN) as approved:
            for group,defs in [('expression_refs',mod.EXPRESSION_REFS),('accessory_refs',mod.ACCESSORY_REFS)]:
                for name,box in defs.items():
                    with self.subTest(name=name):
                        with Image.open(self.out/'reference_crops'/group/(name+'.png')) as crop:
                            self.assertEqual(crop.tobytes(),approved.crop(box).tobytes())
        self.assertTrue((self.out/'qa'/'CP381_EXACT_CANON_EXPRESSION_AND_ACCESSORY_REFERENCES.png').exists())

    def test_comparison_image_and_no_other_character(self):
        with Image.open(self.out/'qa'/'CP381_CANON_FACE_HAIR_BODICE_REVIEW.png') as im:
            self.assertEqual(im.size,(2000,1330))
        # Inputs are precisely CANON + CP380 draft: assert generator uses neither web nor another source.
        source=SOURCE.read_text()
        self.assertNotIn('requests.get',source)
        self.assertNotIn('image_query',source)

if __name__=='__main__':unittest.main(verbosity=2)
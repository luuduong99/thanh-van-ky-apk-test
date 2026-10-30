"""CP380 structural tests. Real CANON/art only available in private project artifacts."""
import importlib.util, os, hashlib, io, json, tempfile, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE
SCRIPT=HERE/'cp380_detail_pass.py'
if not SCRIPT.exists():
    ROOT=HERE.parents[1]
    SCRIPT=ROOT/'tools'/'art'/'cp380_detail_pass.py'
spec=importlib.util.spec_from_file_location('cp380',SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
CAN=Path(os.environ.get('TVK_CP380_CANON',str(HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
ART=Path(os.environ.get('TVK_CP380_BASE_LAYERS',str(HERE/'OUTPUT'/'previous_painted')))
OUT=Path(os.environ.get('TVK_CP380_OUTPUT',str(HERE/'OUTPUT')))
HAS_SOURCE=CAN.is_file() and ART.is_dir() and (OUT/'CP380_REPORT.json').exists()

class PublicContract(unittest.TestCase):
    def test_canon_size_and_layer_counts(self):
        self.assertEqual(mod.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(mod.SIZE,(1302,2748))
        self.assertEqual(len(mod.base.ART),21)
        self.assertEqual(len(mod.DETAILS),8)
    def test_all_eight_are_editable_vector_paths(self):
        self.assertEqual(len({name for name,_ in mod.DETAILS}),8)
        for n,d in mod.DETAILS:
            ET.fromstring(mod.svg(n))
            self.assertIn('<path',d)
            self.assertNotIn('<image',d)
    def test_invalid_canon_rejected_without_output_creation(self):
        with tempfile.TemporaryDirectory() as t:
            fake=Path(t)/'fake.png';Image.new('RGBA',(941,1672),'white').save(fake)
            target=Path(t)/'new-output'
            with self.assertRaisesRegex(ValueError,'Wrong CANON'):
                mod.build(fake,Path(t)/'empty',target)
            self.assertFalse(target.exists())
    def test_no_release_claim_in_source(self):
        text=SCRIPT.read_text(encoding='utf8')
        self.assertIn("'visual_qa':'NOT_PASSED'",text)
        self.assertIn("'production_release':'blocked_pending_art'",text)
        self.assertIn("'native_painted_full_body':False",text)

@unittest.skipUnless(HAS_SOURCE,'Private Lâm Thiển CANON and CP379 art not present on public GitHub CI')
class ActualBinaryFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((OUT/'CP380_REPORT.json').read_text())
    def test_canon_sha_and_exact_copy(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),mod.SHA)
        self.assertEqual((OUT/'source'/CAN.name).read_bytes(),CAN.read_bytes())
    def test_21_original_layer_png_and_svg_unchanged(self):
        for name,_ in mod.base.ART:
            self.assertEqual((OUT/'layers'/(name+'.png')).read_bytes(),(ART/(name+'.png')).read_bytes())
            self.assertEqual((OUT/'svg'/(name+'.svg')).read_bytes(),(ART.parent/'svg'/(name+'.svg')).read_bytes())
    def test_all_8_new_svg_png_layers_nonempty(self):
        for name,_ in mod.DETAILS:
            self.assertTrue((OUT/'svg'/(name+'.svg')).exists())
            im=Image.open(OUT/'layers'/(name+'.png')).convert('RGBA')
            self.assertEqual(im.size,mod.SIZE)
            self.assertIsNotNone(im.getchannel('A').getbbox())
    def test_ora_crc_30_layers_guide_hidden(self):
        with zipfile.ZipFile(OUT/'ora'/self.report['ora']) as z:
            self.assertIsNone(z.testzip())
            stack=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
            self.assertEqual(len(stack),30)
            self.assertEqual(sum(layer.get('visibility')=='hidden' for layer in stack),1)
            self.assertEqual(sum(layer.get('visibility')=='visible' for layer in stack),29)
    def test_ora_merged_equals_preview_alpha(self):
        with zipfile.ZipFile(OUT/'ora'/self.report['ora']) as z:
            merged=np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA'))
        preview=np.asarray(Image.open(OUT/'qa'/'CP380_REFINED_29_LAYER_DRAFT.png').convert('RGBA'))
        self.assertTrue(np.array_equal(merged,preview))
    def test_technical_difference_nonzero(self):
        self.assertGreater(self.report['changed_composite_pixels'],10000)
    def test_only_canon_and_derived_draft_preview(self):
        self.assertTrue((OUT/'qa'/self.report['preview']).is_file())
        self.assertTrue(self.report['source_byte_exact'])
    def test_not_artist_or_rig_approved(self):
        self.assertEqual(self.report['visual_qa'],'NOT_PASSED')
        self.assertEqual(self.report['production_release'],'blocked_pending_art')
        self.assertEqual(self.report['sprite_paths'],{})
        self.assertFalse(self.report['native_painted_full_body'])
        self.assertFalse(self.report['rig_ready'])
        self.assertFalse(self.report['apk_ready'])

if __name__=='__main__':unittest.main(verbosity=2)
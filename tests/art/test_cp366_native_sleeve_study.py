"""CP366 structural checks: genuine SVG art fragments, NOT visual acceptance."""
import hashlib, importlib.util, io, os, sys, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

LOCAL=Path(__file__).resolve().parent
SRC=(Path(__file__).resolve().parents[2]/'tools/art/cp366_build_vector_sleeve.py')
if not SRC.exists():SRC=LOCAL/'cp366_build_vector_sleeve.py'
spec=importlib.util.spec_from_file_location('cp366',SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class Cp366PaintedVectorFragments(unittest.TestCase):
    def test_six_distinct_real_svg_drawings(self):
        self.assertEqual(len(m.LAYER_CONTENT),6)
        for key,source in m.LAYER_CONTENT.items():
            with self.subTest(key=key):
                ET.fromstring(m.svg(key))
                self.assertIn('<path',source)
                self.assertTrue('stroke=' in source or 'fill=' in source)
                self.assertNotIn('image href=',source)

    def test_exact_master_sha_provenance(self):
        self.assertEqual(m.SOURCE_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.BBOX,(13,172,230,630))
        self.assertEqual(m.CANVAS,(1302,2748))

    def test_sources_keep_visual_qa_not_passed(self):
        source=SRC.read_text(encoding='utf8')
        self.assertIn("'visual_qa':'NOT_PASSED'",source)
        self.assertIn("'production_release':'blocked_pending_art'",source)
        self.assertIn("'usable_same_camera_arm_raise_art':False",source)
        self.assertIn('NOT_APPROVED',source)

    def test_can_render_svg_alpha_independently(self):
        import cairosvg
        name='06_gold_shoulder_cuff_trim'
        data=cairosvg.svg2png(bytestring=m.svg(name).encode(),output_width=217,output_height=458)
        im=Image.open(io.BytesIO(data)).convert('RGBA')
        self.assertIsNotNone(im.getchannel('A').getbbox())
        self.assertLess(im.getchannel('A').getbbox()[2],217)

    @unittest.skipUnless((LOCAL/'cp366_out'/'CP366_PARTIAL_SIX_LAYER_SLEEVE_ART_STUDY_NOT_SPINE.ora').exists(),
                         'private editable art asset not in public CI')
    def test_real_ora_layers_and_hidden_reference(self):
        art=LOCAL/'cp366_out'/'CP366_PARTIAL_SIX_LAYER_SLEEVE_ART_STUDY_NOT_SPINE.ora'
        with zipfile.ZipFile(art) as z:
            self.assertIsNone(z.testzip())
            root=ET.fromstring(z.read('stack.xml'))
            ls=root.find('stack').findall('layer')
            self.assertEqual(len(ls),7)
            self.assertEqual(sum('CP366_STUDY__' in node.attrib['name'] for node in ls),6)
            self.assertEqual(sum(node.get('visibility')=='hidden' for node in ls),1)
            self.assertIn('REFERENCE_ONLY_HIDDEN',ls[-1].attrib['name'])
            for node in ls[:6]:
                im=Image.open(io.BytesIO(z.read(node.get('src')))).convert('RGBA')
                self.assertEqual(im.size,m.CANVAS)
                self.assertIsNotNone(im.getchannel('A').getbbox())
            merged=Image.open(io.BytesIO(z.read('mergedimage.png')))
            self.assertEqual(merged.size,m.CANVAS)

if __name__ == '__main__':unittest.main()
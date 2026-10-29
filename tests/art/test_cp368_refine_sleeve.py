"""CP368 source/structure regression tests; do NOT imply aesthetic approval."""
import hashlib, importlib.util, io, tempfile, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cp368', ROOT/'cp368_refine_sleeve.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CANON=ROOT/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
OUT=ROOT/'CP368_OUT'

class CP368Tests(unittest.TestCase):
    def test_original_exact_user_canon(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),m.CANON_SHA)
        with Image.open(CANON) as im:self.assertEqual((im.size,im.mode),((941,1672),'RGBA'))

    def test_all_six_svg_sources_are_real_independent_paths(self):
        self.assertEqual(len(m.DETAILS),6)
        for name in m.DETAILS:
            with self.subTest(name=name):
                source=m.svg_for_layer(name)
                tree=ET.fromstring(source)
                self.assertIn('<path',source)
                self.assertNotIn('<image',source)
                self.assertEqual(tree.attrib['viewBox'],'0 0 217 458')

    def test_ora_layers_and_hidden_canon_reference(self):
        with zipfile.ZipFile(OUT/'CP368_REFINED_SIX_LAYER_SLEEVE_DRAFT_NOT_SPINE.ora') as z:
            self.assertIsNone(z.testzip())
            root=ET.fromstring(z.read('stack.xml'))
            layers=root.find('stack').findall('layer')
            self.assertEqual(len(layers),7)
            self.assertEqual(sum(node.attrib.get('visibility')=='hidden' for node in layers),1)
            self.assertEqual(sum('CP368_DRAFT' in node.attrib.get('name','') for node in layers),6)
            self.assertTrue(layers[-1].attrib['name'].startswith('CANON_V2_1_REFERENCE_ONLY_HIDE'))
            for node in layers[:6]:
                with Image.open(io.BytesIO(z.read(node.attrib['src']))) as im:
                    self.assertEqual(im.size,(1302,2748))
                    self.assertIsNotNone(im.convert('RGBA').getchannel('A').getbbox())

    def test_provenance_rejects_wrong_canon(self):
        with tempfile.TemporaryDirectory() as d:
            wrong=Path(d)/'wrong.png'
            Image.new('RGBA',(941,1672),'#ffffff').save(wrong)
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                m.make(wrong,Path(d)/'out')

    def test_underpaint_rotations_are_technical_only(self):
        import json
        r=json.loads((OUT/'CP368_REPORT.json').read_text())
        self.assertEqual(r['source_sha256'],m.CANON_SHA)
        self.assertEqual(r['production_release'],'blocked_pending_art')
        self.assertFalse(r['rig_ready'])
        self.assertFalse(r['apk_ready'])
        self.assertEqual(r['visual_qa'],'NOT_PASSED')
        self.assertTrue(all(v['overlap_nonzero'] for v in r['technical_motion_overlap'].values()))

    def test_preview_source_only_and_pngs(self):
        self.assertEqual(len(list(OUT.glob('0[1-6]_*.svg'))),6)
        self.assertEqual(len(list(OUT.glob('0[1-6]_*.png'))),6)
        with Image.open(OUT/'CP368_CANON_V2_1_vs_CP366_vs_CP368_UNAPPROVED.png') as im:
            self.assertEqual(im.size,(1510,850))
        with Image.open(OUT/'CP368_LEFT_SLEEVE_REFINED_DRAFT_TRANSPARENT.png') as im:
            self.assertEqual(im.size,(1302,2748))

if __name__=='__main__':unittest.main(verbosity=2)
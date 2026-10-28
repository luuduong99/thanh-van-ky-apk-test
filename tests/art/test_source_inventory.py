"""CP316 source recovery tests. All generated files are synthetic, not CP313 art."""
import io
import json
import sys
import tempfile
from pathlib import Path
import unittest
import zipfile
from xml.etree import ElementTree as ET
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'art'))
import source_inventory as inv


def ora_bytes(layers=10, nonempty=10, dummy_names=False, missing_layer=False):
    root = ET.Element('image', {'w':'24','h':'24'})
    stack = ET.SubElement(root, 'stack')
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        for i in range(layers):
            nm=f'placeholder_{i}' if dummy_names else f'real_style_layer_{i}'
            src=f'data/layer_{i}.png'
            ET.SubElement(stack, 'layer', {'name':nm,'src':src})
            if missing_layer and i == layers - 1:
                continue
            im=Image.new('RGBA',(24,24), (255,50,100,255) if i < nonempty else (0,0,0,0))
            out=io.BytesIO(); im.save(out, 'PNG')
            z.writestr(src, out.getvalue())
        z.writestr('stack.xml', ET.tostring(root))
        z.writestr('mergedimage.png', b'not-important-for-this-test')
    return b.getvalue()


class SourceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.base = Path(self.t.name)

    def test_nested_source_found_as_unverified_candidate(self):
        with zipfile.ZipFile(self.base/'nested.zip','w') as z:
            z.writestr('nested/CP313.ora', ora_bytes())
        report=inv.scan([self.base])
        self.assertEqual(report['candidate_count'],1)
        self.assertIn('NEEDS_ART_REVIEW',report['ora_candidates'][0]['status'])
        self.assertIn('!nested/CP313.ora',report['ora_candidates'][0]['locator'])

    def test_ten_layers_but_eight_empty_are_rejected(self):
        (self.base/'fake.ora').write_bytes(ora_bytes(nonempty=2))
        report=inv.scan([self.base])
        self.assertEqual(report['candidate_count'],0)
        self.assertIn('nonempty', ' '.join(report['ora_candidates'][0]['errors']))

    def test_placeholder_names_rejected(self):
        (self.base/'placeholder.ora').write_bytes(ora_bytes(dummy_names=True))
        report=inv.scan([self.base])
        self.assertEqual(report['candidate_count'],0)
        self.assertIn('placeholder-like', ' '.join(report['ora_candidates'][0]['errors']))

    def test_missing_layer_rejected(self):
        (self.base/'missing.ora').write_bytes(ora_bytes(missing_layer=True))
        report=inv.scan([self.base])
        self.assertEqual(report['candidate_count'],0)
        self.assertIn('missing layer', ' '.join(report['ora_candidates'][0]['errors']))

    def test_no_source_reports_missing_not_success(self):
        with zipfile.ZipFile(self.base/'only_png.zip','w') as z:
            z.writestr('flat.png', b'flat image')
        report=inv.scan([self.base])
        self.assertEqual(report['status'],'NO_QUALIFYING_ORA_SOURCE')
        self.assertEqual(report['candidate_count'],0)
        self.assertEqual(len(report['examined_archives']),1)


if __name__=='__main__':
    unittest.main(verbosity=2)
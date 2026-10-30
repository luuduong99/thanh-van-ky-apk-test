import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1] if (HERE.parents[1]/'tools/art/cp388_manual_eyelid_guides.py').exists() else HERE
SCRIPT=(ROOT/'tools/art/cp388_manual_eyelid_guides.py') if (ROOT/'tools/art/cp388_manual_eyelid_guides.py').exists() else HERE/'cp388_manual_eyelid_guides.py'
spec=importlib.util.spec_from_file_location('cp388', SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CANON=Path(os.getenv('CP388_CANON',HERE/'source/OUTPUT/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
HAS_CANON=CANON.exists()

class CP388Tests(unittest.TestCase):
    def test_static_source_contract(self):
        self.assertEqual(g.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(g.SIZE,(168,197));self.assertEqual(g.BBOX,(25,684,193,881))
        self.assertEqual(len(g.PATHS),6)
    def test_vector_paths_have_independent_geometry(self):
        for name,(path,color,width) in g.PATHS.items():
            self.assertIn('M ',path);self.assertIn('C ',path)
            self.assertGreater(width,0)
            self.assertGreater(len(g.parse_and_sample(path)),100)
        self.assertNotEqual(g.PATHS['left_upper_lash'][0],g.PATHS['right_upper_lash'][0])
    def test_wrong_canon_fails_before_writing(self):
        with tempfile.TemporaryDirectory() as td:
            fake=Path(td)/'fake.png';Image.new('RGBA',(941,1672),'white').save(fake)
            out=Path(td)/'output'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                g.run(fake,out)
            self.assertFalse(out.exists())
    @unittest.skipUnless(HAS_CANON,'private CANON intentionally absent')
    def test_output_preserves_source_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            g.run(CANON,td)
            self.assertEqual(Path(td,'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes(),CANON.read_bytes())
    @unittest.skipUnless(HAS_CANON,'private CANON intentionally absent')
    def test_new_drawn_layers_clipped_to_two_eye_rois(self):
        rects=g.ROIS
        for name,(path,color,width) in g.PATHS.items():
            mask=np.array(g.draw_layer(path,color,width))[:,:,3]>0
            self.assertGreater(mask.sum(),10)
            roi=rects['left' if name.startswith('left') else 'right']
            allowed=np.zeros((197,168),dtype=bool)
            x0,y0,x1,y1=roi;allowed[y0:y1,x0:x1]=True
            self.assertEqual(int((mask & ~allowed).sum()),0,name)
    @unittest.skipUnless(HAS_CANON,'private CANON intentionally absent')
    def test_ora_exact_static_and_hidden_unapproved(self):
        with tempfile.TemporaryDirectory() as td:
            g.run(CANON,td)
            with zipfile.ZipFile(Path(td,'CP388_EDITABLE_EYELID_LINEWORK_ONLY_NOT_RIG.ora')) as z:
                self.assertIsNone(z.testzip())
                tree=ET.fromstring(z.read('stack.xml'));layers=list(tree.findall('.//layer'))
                self.assertEqual(len(layers),8)
                self.assertEqual([q.attrib['visibility'] for q in layers].count('visible'),1)
                ref=np.asarray(g.verify_canon(CANON))
                merged=np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA'))
                self.assertTrue(np.array_equal(ref,merged))
                self.assertTrue(any('EMPTY' in q.attrib['name'] for q in layers))
    @unittest.skipUnless(HAS_CANON,'private CANON intentionally absent')
    def test_report_release_gate(self):
        with tempfile.TemporaryDirectory() as td:
            r=g.run(CANON,td)
            self.assertEqual(r['visual_qa'],'NOT_PASSED')
            self.assertFalse(r['closed_eye_master_approved'])
            self.assertEqual(r['new_skin_underpaint'],'EMPTY/NOT_PAINTED')
            self.assertEqual(r['production_release']['sprite_paths'],{})
            self.assertEqual(r['production_release']['status'],'blocked_pending_art')
            self.assertFalse(r['frames_ready'])
    @unittest.skipUnless(HAS_CANON,'private CANON intentionally absent')
    def test_exported_svg_png_count(self):
        with tempfile.TemporaryDirectory() as td:
            g.run(CANON,td)
            self.assertEqual(len(list(Path(td,'layers').glob('*.svg'))),6)
            self.assertEqual(len(list(Path(td,'layers').glob('*.png'))),6)
            self.assertTrue(Path(td,'qa/CP388_CANON_AND_MANUAL_EYELID_LINEWORK_DRAFT.png').exists())

if __name__=='__main__':unittest.main()
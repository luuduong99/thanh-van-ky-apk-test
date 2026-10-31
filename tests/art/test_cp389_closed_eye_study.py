"""CP389 regression tests: exact CANON original protected, closed-eye art stays draft.

Private reference missing from public CI => static tests run and source tests SKIP.
"""
from __future__ import annotations
import hashlib, importlib.util, json, os, tempfile, unittest, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
CANDIDATES=[HERE/'cp389_closed_eye_study.py', HERE.parent.parent/'tools/art/cp389_closed_eye_study.py']
CODE=next((p for p in CANDIDATES if p.exists()),CANDIDATES[0]);assert CODE.exists(),CODE
spec=importlib.util.spec_from_file_location('cp389_closed',CODE)
cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)
CANON=Path(os.environ.get('TVK_CP389_CANON',str(HERE/'source/OUTPUT/LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
HAS_CANON=CANON.is_file() and hashlib.sha256(CANON.read_bytes()).hexdigest()==cp.CANON_SHA

class CP389QA(unittest.TestCase):
    def test_static_source_identity(self):
        self.assertEqual(cp.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(cp.BBOX,(25,684,193,881))
        self.assertEqual(cp.SIZE,(168,197))

    def test_static_eyes_in_source_canvas(self):
        for roi in (cp.LEFT,cp.RIGHT):
            x0,y0,x1,y1=roi
            self.assertTrue(0<x0<x1<168 and 0<y0<y1<197)
        self.assertTrue(cp.RIGHT[0]>cp.LEFT[2])

    def test_static_output_contract(self):
        src=CODE.read_text(encoding='utf8')
        self.assertIn('blocked_pending_art',src)
        self.assertIn('NOT_PASSED',src)
        self.assertIn('closed_eye_artist_approval=False',src)
        self.assertIn('mergedimage.png',src)

    @unittest.skipUnless(HAS_CANON,'Exact private user CANON not available on public CI')
    def test_locked_source_and_copy_exact(self):
        with tempfile.TemporaryDirectory() as d:
            result=cp.generate(CANON,Path(d)/'out')
            self.assertEqual(result['source_sha256'],cp.CANON_SHA)
            self.assertEqual(hashlib.sha256((Path(d)/'out/LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes()).hexdigest(),cp.CANON_SHA)

    @unittest.skipUnless(HAS_CANON,'Exact private user CANON not available on public CI')
    def test_wrong_canon_rejected_before_any_output(self):
        with tempfile.TemporaryDirectory() as d:
            fake=Path(d)/'bad.png';Image.new('RGBA',(941,1672),(250,150,200,255)).save(fake)
            out=Path(d)/'must_not_exist'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):cp.generate(fake,out)
            self.assertFalse(out.exists())

    @unittest.skipUnless(HAS_CANON,'Exact private user CANON not available on public CI')
    def test_pixel_exact_open_face_and_roi_only_draft(self):
        with tempfile.TemporaryDirectory() as d:
            cp.generate(CANON,Path(d))
            canon=np.asarray(cp.verify(CANON));draft=np.asarray(Image.open(Path(d)/'CP389_CLOSED_EYE_DRAFT_NOT_APPROVED.png'))
            changed=np.any(canon!=draft,axis=2)
            permit=np.zeros(changed.shape,bool)
            for x0,y0,x1,y1 in ((31,94,69,122),(85,70,130,105)):permit[y0:y1,x0:x1]=True
            self.assertEqual(int((changed&~permit).sum()),0)
            self.assertGreater(int(changed.sum()),1000)
            self.assertTrue(np.array_equal(np.asarray(Image.open(Path(d)/'CANON_SHY_EXACT.png')),canon))

    @unittest.skipUnless(HAS_CANON,'Exact private user CANON not available on public CI')
    def test_four_editable_nonempty_layers(self):
        with tempfile.TemporaryDirectory() as d:
            report=cp.generate(CANON,Path(d))
            self.assertEqual(len(report['independent_new_layers']),4)
            for name in report['independent_new_layers']:
                im=np.asarray(Image.open(Path(d)/'art'/f'{name}_DRAFT.png'))
                self.assertEqual(im.shape,(197,168,4))
                self.assertGreater(int(np.count_nonzero(im[:,:,3])),10)

    @unittest.skipUnless(HAS_CANON,'Exact private user CANON not available on public CI')
    def test_ora_crc_layer_visibility_and_source_merged(self):
        with tempfile.TemporaryDirectory() as d:
            cp.generate(CANON,Path(d))
            with zipfile.ZipFile(Path(d)/'CP389_CANON_EXACT_CLOSED_EYE_EDITABLE_STUDY_NOT_APPROVED.ora') as z:
                self.assertIsNone(z.testzip())
                root=ET.fromstring(z.read('stack.xml'))
                layers=root.find('stack').findall('layer')
                self.assertEqual(len(layers),6)
                self.assertEqual([x.get('visibility') for x in layers].count('visible'),1)
                self.assertIn('CANON',layers[0].get('name'))
                merged=np.asarray(Image.open(__import__('io').BytesIO(z.read('mergedimage.png'))))
                self.assertTrue(np.array_equal(merged,np.asarray(cp.verify(CANON))))

    @unittest.skipUnless(HAS_CANON,'Exact private user CANON not available on public CI')
    def test_draft_is_explicitly_unapproved(self):
        with tempfile.TemporaryDirectory() as d:
            r=cp.generate(CANON,Path(d))
            self.assertEqual(r['visual_qa'],'NOT_PASSED')
            self.assertFalse(r['closed_eye_artist_approval'])
            self.assertFalse(r['production_release']['spine_ready'])
            self.assertFalse(r['production_release']['apk_ready'])
            self.assertEqual(r['production_release']['sprite_paths'],{})

if __name__=='__main__':unittest.main()
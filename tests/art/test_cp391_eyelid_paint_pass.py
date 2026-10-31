#!/usr/bin/env python3
"""CP391 source-only CI contracts + private exact-CANON art integrity tests."""
import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
import zipfile

import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
SRC=HERE/'cp391_eyelid_paint_pass.py'
if not SRC.exists():
    SRC=HERE.parents[1]/'tools'/'art'/'cp391_eyelid_paint_pass.py'
assert SRC.exists(), f'Cannot locate CP391 art tool from {HERE}'
spec=importlib.util.spec_from_file_location('cp391tool',SRC)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
ROOT=Path(os.getenv('CP391_TEST_ROOT','/mnt/data'))
CANON=Path(os.getenv('CP391_CANON',ROOT/'CP390'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
PRIOR=Path(os.getenv('CP391_BASE',ROOT/'CP390'/'OUTPUT'/'CP390_CLOSED_EYES_CANDIDATE_NOT_APPROVED.png'))
NEED_PRIVATE=not (CANON.is_file() and PRIOR.is_file())

class PublicStaticContracts(unittest.TestCase):
    def test_required_source_sha_and_roi(self):
        self.assertEqual(len(mod.CANON_SHA),64)
        self.assertEqual(mod.WH,(168,197))
        self.assertEqual(len(mod.ROIS),2)
        self.assertEqual(len(mod.ART_NAMES),6)

    def test_release_is_not_artist_approved(self):
        code=SRC.read_text(encoding='utf8')
        self.assertIn('blocked_pending_art',code)
        self.assertIn("'visual_qa':'NOT_PASSED'",code)
        self.assertIn("'sprite_paths':{}",code)

    def test_no_generated_concept_is_accepted_as_canon(self):
        code=SRC.read_text(encoding='utf8')
        self.assertIn('CANON_SHA_MISMATCH',code)
        self.assertIn('no_unverified_generated_concept_art_in_artifact',code)
        self.assertNotIn('a_detailed_comparison_analysis_infographic_poster',code)

@unittest.skipIf(NEED_PRIVATE,'Private CANON V2.1 and CP390 draft are not bundled in public GitHub')
class PrivateArtworkContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.out=Path(cls.temp.name)/'result'
        cls.report=mod.generate(CANON,PRIOR,cls.out)
        cls.src=mod.load_canon(CANON)
        cls.prior=mod.load_prev(PRIOR)
        cls.candidate=Image.open(cls.out/'CP391_CLOSED_EYE_ART_DRAFT_NOT_APPROVED.png').convert('RGBA')
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_exact_canon_sha(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),mod.CANON_SHA)
        self.assertEqual(hashlib.sha256((self.out/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes()).hexdigest(),mod.CANON_SHA)

    def test_fake_canon_rejected_before_write(self):
        wrong=Path(self.temp.name)/'wrong.png'
        im=Image.open(CANON).convert('RGBA');im.putpixel((20,20),(0,0,0,255));im.save(wrong)
        dest=Path(self.temp.name)/'should_not_exist'
        with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
            mod.generate(wrong,PRIOR,dest)
        self.assertFalse(dest.exists())

    def test_all_six_new_layers_are_nonempty_and_roi_bounded(self):
        for name in mod.ART_NAMES:
            im=Image.open(self.out/'art'/f'{name}_CP391_DRAFT.png').convert('RGBA')
            self.assertEqual(im.size,mod.WH)
            self.assertIsNotNone(im.getchannel('A').getbbox(),name)
            self.assertTrue(mod.in_roi(im,name.split('_')[0]),name)

    def test_closed_eye_candidate_changes_only_eye_regions(self):
        a=np.asarray(self.src);b=np.asarray(self.candidate)
        outside=np.ones((mod.WH[1],mod.WH[0]),dtype=bool)
        for x1,y1,x2,y2 in mod.ROIS.values():outside[y1:y2,x1:x2]=False
        self.assertEqual(int(np.count_nonzero(np.any(a[outside]!=b[outside],axis=1))),0)
        self.assertGreater(int(np.count_nonzero(np.any(a[~outside]!=b[~outside],axis=1))),0)

    def test_ora_source_visible_and_new_paint_hidden(self):
        p=self.out/'CP391_EYELID_PAINTER_STUDY_CANON_VISIBLE_NOT_APPROVED.ora'
        with zipfile.ZipFile(p) as z:
            self.assertIsNone(z.testzip())
            root=ET.fromstring(z.read('stack.xml'))
            layers=list(root.find('stack'))
            self.assertEqual(len(layers),9)
            self.assertEqual(sum(x.get('visibility')=='visible' for x in layers),1)
            self.assertTrue(layers[0].get('visibility')=='visible')
            image=Image.open(z.open('mergedimage.png')).convert('RGBA')
            self.assertTrue(np.array_equal(np.asarray(image),np.asarray(self.src)))

    def test_report_not_claiming_visual_approval(self):
        r=json.loads((self.out/'CP391_REPORT.json').read_text('utf8'))
        self.assertEqual(r['visual_qa'],'NOT_PASSED')
        self.assertFalse(r['artist_approval'])
        self.assertEqual(r['changed_pixels_outside_eye_roi'],0)
        self.assertEqual(r['release']['status'],'blocked_pending_art')
        self.assertEqual(r['release']['sprite_paths'],{})

    def test_canvas_and_previews_exist(self):
        p=self.out/'qa'/'CP391_CANON_CP390_CP391_ACTUAL_SOURCE_COMPARE.png'
        with Image.open(p) as im:
            self.assertEqual(im.size,(1540,845))
        self.assertEqual(self.prior.size,mod.WH)

if __name__=='__main__':unittest.main(verbosity=2)
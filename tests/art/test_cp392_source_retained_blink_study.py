#!/usr/bin/env python3
"""CP392 static public-source and private-CANON pixel integrity checks."""
import hashlib, importlib.util, json, os, tempfile, unittest, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'cp392_source_retained_blink_study.py'
if not SOURCE.exists(): SOURCE=ROOT.parents[1]/'tools'/'art'/'cp392_source_retained_blink_study.py'
spec=importlib.util.spec_from_file_location('cp392',SOURCE);cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)
CANON=Path(os.environ.get('CP392_CANON', '/mnt/data/CP391/OUTPUT/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
OLD=Path(os.environ.get('CP392_CP391', '/mnt/data/CP391/OUTPUT/CP391_CLOSED_EYE_ART_DRAFT_NOT_APPROVED.png'))
PRIVATE=CANON.exists() and OLD.exists()

class StaticContract(unittest.TestCase):
    def test_locked_source_identity(self):
        self.assertEqual(len(cp.CANON_SHA),64)
        self.assertEqual(len(cp.CP391_SHA),64)
        self.assertEqual(cp.SIZE,(168,197))
    def test_near_closed_is_not_marked_approved(self):
        code=SOURCE.read_text('utf8')
        self.assertIn('NOT_PASSED',code)
        self.assertIn('blocked_pending_art',code)
        self.assertIn('sprite_paths',code)
    def test_two_distinct_source_sampled_poses(self):
        self.assertEqual(set(cp.VARIANTS),{'gentle','near_closed'})
        self.assertEqual(set(cp.LIDS),{'LEFT','RIGHT'})
        self.assertIn('CANON_SHA_MISMATCH',SOURCE.read_text('utf8'))
    def test_no_external_generated_character_art(self):
        code=SOURCE.read_text('utf8')
        self.assertIn('same original portrait',code)
        self.assertNotIn('image_gen',code)
        self.assertNotIn('TO_NGUYET_LY',code)

@unittest.skipUnless(PRIVATE,'Private exact CANON image and CP391 raster unavailable in public CI')
class PrivateArtistSourceAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.output=Path(cls.tmp.name)/'out'
        cls.report=cp.generate(CANON,OLD,cls.output)
        cls.src=Image.open(cls.output/'CANON_SHY_SOURCE_PIXEL_EXACT.png').convert('RGBA')
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_input_source_sha_and_copy_byte_exact(self):
        self.assertEqual(cp.sha256(CANON),cp.CANON_SHA)
        self.assertEqual(cp.sha256(self.output/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'),cp.CANON_SHA)
    def test_tamper_guard_before_any_writes(self):
        wrong=Path(self.tmp.name)/'wrong.png'
        im=Image.open(CANON).convert('RGBA');im.putpixel((15,15),(0,0,0,255));im.save(wrong)
        p=Path(self.tmp.name)/'should-not-exist'
        with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):cp.generate(wrong,OLD,p)
        self.assertFalse(p.exists())
    def test_both_variants_are_distinct_and_nonempty(self):
        self.assertGreater(self.report['pixels_differ_between_variants'],100)
        for variant in cp.VARIANTS:
            self.assertGreater(self.report['pixels_changed_from_source'][variant],100)
            for side in cp.LIDS:
                im=Image.open(self.output/'art'/f'{variant}_{side}_CHEEK_SAMPLE_PATCH.png').convert('RGBA')
                self.assertIsNotNone(im.getchannel('A').getbbox())
    def test_unchanged_pixels_outside_two_eyes(self):
        for variant in cp.VARIANTS:
            im=Image.open(self.output/f'CP392_{variant.upper()}_DRAFT_NOT_APPROVED.png').convert('RGBA')
            self.assertEqual(cp.changed_outside(self.src,im),0)
    def test_ora_crc_and_original_only_visible(self):
        path=self.output/'CP392_EYELASH_RETAINED_SKIN_PATCH_EDITABLE_NOT_APPROVED.ora'
        with zipfile.ZipFile(path) as z:
            self.assertIsNone(z.testzip())
            layers=list(ET.fromstring(z.read('stack.xml')).find('stack'))
            self.assertEqual(len(layers),8)
            self.assertEqual(sum(x.get('visibility')=='visible' for x in layers),1)
            source=Image.open(z.open('mergedimage.png')).convert('RGBA')
            self.assertTrue(np.array_equal(np.asarray(source),np.asarray(self.src)))
    def test_release_remains_blocked(self):
        self.assertEqual(self.report['visual_qa'],'NOT_PASSED')
        self.assertFalse(self.report['artist_approval'])
        self.assertEqual(self.report['release']['status'],'blocked_pending_art')
        self.assertEqual(self.report['release']['sprite_paths'],{})
    def test_preview_is_source_only(self):
        path=self.output/'qa'/'CP392_SOURCE_REAL_CANON_AND_TWO_BLINK_VARIANTS.png'
        with Image.open(path) as im:self.assertEqual(im.size,(2096,760))

if __name__=='__main__':unittest.main(verbosity=2)
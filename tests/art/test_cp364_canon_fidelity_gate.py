"""CP364 tests use synthetic colored blocks, NOT real approved art.

The genuine reference was independently audited in the production work session.
"""
import sys
import unittest
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'/'art')
                 if (Path(__file__).resolve().parents[2]/'tools'/'art').exists()
                 else str(Path(__file__).resolve().parent))
from cp364_canon_fidelity_gate import analyze_candidate


def fake_front():
    im=Image.new('RGBA',(217,458),(250,250,250,255))
    d=ImageDraw.Draw(im)
    d.rectangle((83,12,134,56),fill=(204,194,219,255))
    d.rectangle((79,432,101,457),fill=(64,111,219,255))
    d.rectangle((109,414,121,445),fill=(65,107,213,255))
    return im

class CanonFidelitySmokeTests(unittest.TestCase):
    def test_fidelity_guard_no_auto_approval_even_with_good_color(self):
        result=analyze_candidate(fake_front())
        self.assertEqual(result['technical_status'],'REFERENCE_COLOR_GUARDS_CLEAR')
        self.assertFalse(result['runtime_approved'])
        self.assertEqual(result['visual_qa'],'NOT_PASSED')
        self.assertEqual(result['production_release'],'blocked_pending_art')

    def test_dark_hair_is_rejected(self):
        im=fake_front()
        ImageDraw.Draw(im).rectangle((83,12,134,56),fill=(63,48,44,255))
        result=analyze_candidate(im)
        self.assertEqual(result['technical_status'],'NEEDS_ART_CORRECTION')
        self.assertTrue(any('too dark' in item for item in result['issues']))

    def test_missing_left_blue_toe_is_rejected(self):
        im=fake_front()
        ImageDraw.Draw(im).rectangle((79,432,101,457),fill=(255,255,255,0))
        result=analyze_candidate(im)
        self.assertTrue(any('left_blue_toe' in item for item in result['issues']))

    def test_missing_right_blue_toe_is_rejected(self):
        im=fake_front()
        ImageDraw.Draw(im).rectangle((109,414,121,445),fill=(255,255,255,0))
        result=analyze_candidate(im)
        self.assertTrue(any('right_blue_toe' in item for item in result['issues']))

    def test_wrong_camera_and_sheet_aspect_report_alignment(self):
        result=analyze_candidate(Image.new('RGBA',(1536,1024),(255,255,255,255)))
        self.assertEqual(result['technical_status'],'REVIEW_ALIGNMENT')
        self.assertFalse(result['runtime_approved'])

    def test_source_guard_metadata_is_canon_v21(self):
        from cp364_canon_fidelity_gate import CANON_SHA, FRONT_BBOX, BASE_SIZE
        self.assertEqual(CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual((FRONT_BBOX[2]-FRONT_BBOX[0],FRONT_BBOX[3]-FRONT_BBOX[1]),BASE_SIZE)

if __name__=='__main__': unittest.main()
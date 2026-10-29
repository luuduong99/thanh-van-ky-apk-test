"""CP360 motion math regressions. Synthetic fixtures do not approve any Lâm Thiển art."""
import unittest
import numpy as np
from PIL import Image

class Cp360MotionInterpretationTests(unittest.TestCase):
    def test_splitting_then_rotating_can_create_interpolation_seams(self):
        size=(64,64)
        first=Image.new('RGBA',size)
        second=Image.new('RGBA',size)
        a=np.zeros((64,64,4),np.uint8)
        b=np.zeros_like(a)
        a[20:44,12:32]=[232,195,190,255]
        b[20:44,32:52]=[150,180,235,255]
        first=Image.fromarray(a,'RGBA'); second=Image.fromarray(b,'RGBA')
        merged=Image.alpha_composite(first,second)
        grouped=merged.rotate(-9,Image.Resampling.BICUBIC,center=(32,32))
        individual=Image.alpha_composite(
            first.rotate(-9,Image.Resampling.BICUBIC,center=(32,32)),
            second.rotate(-9,Image.Resampling.BICUBIC,center=(32,32)))
        self.assertGreater(np.count_nonzero(np.any(np.array(grouped)!=np.array(individual),axis=2)),0)

    def test_vacated_hand_pixels_are_not_intrinsically_holes(self):
        frame=Image.new('RGBA',(40,25))
        a=np.array(frame)
        a[12:15,3:8]=[235,202,188,255]
        old=Image.fromarray(a,'RGBA')
        newer=Image.new('RGBA',(40,25));newer.paste(old,(5,0))
        old_a=np.array(old)[:,:,3];new_a=np.array(newer)[:,:,3]
        lost=(old_a>127)&(new_a<25)
        self.assertGreater(int(lost.sum()),0)
        # A moving free hand leaves old positions empty by design.

    def test_cp360_builder_cannot_claim_release(self):
        from pathlib import Path
        code=(Path(__file__).resolve().parents[2]/
              'tools/art/cp360_local_underpaint_study.py').read_text(encoding='utf8')
        self.assertIn("'production_sprite_ready':False",code)
        self.assertIn("'spine_ready':False",code)
        self.assertIn("'release_gate':'blocked_pending_art'",code)

    def test_cp360_requires_locked_source_sha(self):
        from pathlib import Path
        code=(Path(__file__).resolve().parents[2]/
              'tools/art/cp360_local_underpaint_study.py').read_text(encoding='utf8')
        self.assertIn('f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a',code)
        self.assertIn('f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497',code)

if __name__=='__main__':
    unittest.main()

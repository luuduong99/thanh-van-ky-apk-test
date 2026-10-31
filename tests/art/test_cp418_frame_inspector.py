"""CP418 Android CANON-only review controls, ROI audit, and unchanged art status.

Technical QA: neither a painter-grade visual review nor a physical Android test.
"""
import hashlib
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
APP = ROOT / 'app/src/main/java/vn/thanhvanky/prototype/TVKCP417SamePoseBlinkActivity.kt'
if not APP.exists():
    APP = HERE/'TVKCP417SamePoseBlinkActivity.kt'
CANON = Path(os.getenv('TVK_CP418_PRIVATE_CANON', '/nonexistent/private-CANON.png'))
ATLAS = Path(os.getenv('TVK_CP418_PRIVATE_ATLAS', '/nonexistent/private-atlas.png'))
CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
ATLAS_SHA = 'cb6cbe03cb1b9ccd3201e4a6bb6ba0e9cc3225111c4f78d441d7d9d7296d05cb'
ROIS = ((88,50,104,56),(107,50,124,57))

class PublicContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.code = APP.read_text(encoding='utf8')
    def test_pinned_source_hashes(self):
        self.assertIn(CANON_SHA,self.code); self.assertIn(ATLAS_SHA,self.code)
    def test_debug_only_not_exported(self):
        self.assertIn('FLAG_DEBUGGABLE',self.code)
    def test_unchanged_private_source_picker(self):
        for marker in ('Intent.ACTION_OPEN_DOCUMENT','require(got == expected)','sameAs(source)','inLeft','inRight'):
            self.assertIn(marker,self.code)
    def test_frame_scrub_control_is_real(self):
        for marker in ('for (step in 0 until FRAMES)','viewer.setFrameOverride(step)',
                       'viewer.setPlaying(false)','frameOverride ?: currentFrame()','playPause.isEnabled = false'):
            self.assertIn(marker,self.code)
    def test_comparison_is_source_pixel_not_new_face(self):
        for marker in ('canvas.drawBitmap(src, face, left, pixelPaint)',
                       'canvas.drawBitmap(data, frameFace, right, pixelPaint)',
                       'isFilterBitmap = false','Rect(88,50,104,56)','Rect(107,50,124,57)'):
            self.assertIn(marker,self.code)
    def test_validation_bulk_reads_and_fail_closed(self):
        self.assertIn('source.getPixels(original',self.code)
        self.assertIn('sheet.getPixels(atlasPixels',self.code)
        self.assertIn('if (!inLeft && !inRight) return null',self.code)
        self.assertNotIn('sheet.getPixel(i * W + x, y)',self.code)
    def test_source_assets_not_in_code(self):
        self.assertNotIn('characters/LAM_THIEN_CANON',self.code)
        self.assertNotIn('assets.open("LAM_THIEN',self.code)

@unittest.skipUnless(CANON.is_file() and ATLAS.is_file(), 'Private CANON+atlas are not stored in public GitHub')
class PrivateSourceAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PIL import Image
        cls.canon = Image.open(CANON).convert('RGBA')
        cls.atlas = Image.open(ATLAS).convert('RGBA')
        cls.front = cls.canon.crop((16,180,224,623))
    def test_exact_source_hash(self): self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),CANON_SHA)
    def test_exact_atlas_hash(self): self.assertEqual(hashlib.sha256(ATLAS.read_bytes()).hexdigest(),ATLAS_SHA)
    def test_dimensions(self):
        self.assertEqual(self.canon.size,(941,1672))
        self.assertEqual(self.front.size,(208,443))
        self.assertEqual(self.atlas.size,(1040,443))
    def test_first_frame_exact(self):
        self.assertEqual(self.atlas.crop((0,0,208,443)).tobytes(),self.front.tobytes())
    def test_counts_and_non_roi_are_unchanged(self):
        p=self.front.load()
        counts=[]
        for n in range(5):
            im=self.atlas.crop((n*208,0,(n+1)*208,443)); pix=im.load(); count=0
            for y in range(443):
                for x in range(208):
                    if pix[x,y]!=p[x,y]:
                        self.assertTrue(any(a<=x<c and b<=y<d for a,b,c,d in ROIS))
                        count+=1
            counts.append(count)
        self.assertEqual(counts,[0,104,119,144,144])
    def test_source_upper_lash_unchanged(self):
        for i in range(5):
            f=self.atlas.crop((i*208,0,(i+1)*208,443))
            for x0,y0,x1,y1 in ROIS:
                self.assertEqual(f.crop((x0,y0,x1,52)).tobytes(),self.front.crop((x0,y0,x1,52)).tobytes())

if __name__ == '__main__': unittest.main()
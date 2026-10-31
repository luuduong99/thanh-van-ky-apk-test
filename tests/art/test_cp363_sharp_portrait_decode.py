"""CP363 Android bitmap decode resolution guard.

Static code contracts + numerical policy examples, not actual on-device FPS.
"""
import unittest
from pathlib import Path

SRC = (Path(__file__).resolve().parents[2] /
       "app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt")


def expected_sample(width, height):
    if width <= 0 or height <= 0:
        return 1
    n = 1
    while width // n > 4096 or height // n > 4096 or (width // n) * (height // n) > 8_000_000:
        n *= 2
    return n


class Cp363SharpPortraitDecodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SRC.read_text(encoding="utf-8")
        cls.decode = cls.source.split("private fun portraitSampleSize(", 1)[1].split(
            "private fun selectScene(", 1)[0]

    def test_no_forced_half_res_character_decoding(self):
        self.assertNotIn("inSampleSize = 2", self.decode)
        self.assertIn("inSampleSize = portraitSampleSize(", self.decode)

    def test_normal_source_sizes_keep_native_pixels(self):
        for w,h in ((215,449),(941,1672),(1024,2048),(2048,2048)):
            with self.subTest(size=(w,h)):
                self.assertEqual(expected_sample(w,h),1)

    def test_large_images_are_power_of_two_sampled(self):
        for w,h in ((4096,4096),(6000,4000),(9000,5000)):
            with self.subTest(size=(w,h)):
                n=expected_sample(w,h)
                self.assertGreaterEqual(n,2)
                self.assertEqual(n & (n-1),0)
                self.assertLessEqual(w//n,4096)
                self.assertLessEqual(h//n,4096)
                self.assertLessEqual((w//n)*(h//n),8_000_000)

    def test_full_image_uses_header_before_pixel_decode(self):
        self.assertIn("inJustDecodeBounds = true", self.decode)
        self.assertIn("bounds.outWidth", self.decode)
        self.assertIn("bounds.outHeight", self.decode)

    def test_region_decode_uses_actual_crop_dimensions(self):
        self.assertIn('crop == "leftThird"', self.decode)
        self.assertIn("val right = (decoder.width / 3).coerceAtLeast(1)", self.decode)
        self.assertIn("portraitSampleSize(right, decoder.height)", self.decode)

    def test_source_color_and_density_not_implicitly_reduced(self):
        self.assertEqual(self.decode.count("inPreferredConfig = Bitmap.Config.ARGB_8888"),2)
        self.assertEqual(self.decode.count("inScaled = false"),2)

    def test_release_sprite_guard_is_preserved(self):
        self.assertIn('val safeHeroineImage =', self.source)
        self.assertIn('selectedId == "lin_qian" && !debugArtPreview', self.source)
        self.assertIn('expressionArt.orEmpty()', self.source)

if __name__ == "__main__":
    unittest.main()

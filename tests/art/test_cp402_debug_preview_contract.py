"""CP402 public checks: a DRAFT atlas can only open in a protected debug viewer."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
JAVA=ROOT/'app/src/main/java/vn/thanhvanky/prototype/TVKBlinkAtlasPreviewActivity.kt'
if not JAVA.is_file():
 JAVA=Path(__file__).resolve().parents[1]/'TVKBlinkAtlasPreviewActivity.kt'
class DebugReviewSafety(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.text=JAVA.read_text(encoding='utf-8')
 def test_debug_only_runtime_gate(self):
  self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',self.text)
  self.assertIn('finish(); return',self.text)
 def test_explicit_source_digest(self):
  self.assertIn('645738fa932a354e3142e2474eb35011491b091d06451a08c4443e6650529c97',self.text)
  self.assertIn('MessageDigest.getInstance("SHA-256")',self.text)
 def test_no_implicit_asset_path(self):
  self.assertNotIn('assets.open(',self.text)
  self.assertIn('Intent.ACTION_OPEN_DOCUMENT',self.text)
 def test_atlas_and_size_checked(self):self.assertIn('img.width == 2520 && img.height == 197',self.text)
 def test_context_marked_draft(self):self.assertIn('KHÔNG PHẢI ẢNH GAME ĐÃ DUYỆT',self.text)

if __name__=='__main__':unittest.main()
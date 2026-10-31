"""CP413 Android test via static contracts. This does NOT approve visual artwork."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
VIEW=ROOT/'app/src/main/java/vn/thanhvanky/prototype/TVKCP413HeadTurnDebugView.kt'
ACT=ROOT/'app/src/main/java/vn/thanhvanky/prototype/TVKCombinedIdlePreviewActivity.kt'
CAT=ROOT/'app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt'

class CP413DebugOnly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.view=VIEW.read_text(encoding='utf8')
        cls.act=ACT.read_text(encoding='utf8')
        cls.cat=CAT.read_text(encoding='utf8')
    def test_head_source_size_and_samples(self):
        self.assertIn('canon.width == 208 && canon.height == 443',self.view)
        self.assertIn('intArrayOf(-4, -2, 0, 2, 4)',self.view)
        self.assertIn('intArrayOf(271, 174, 0, 174, 276)',self.view)
    def test_neutral_exact_unwarped(self):
        self.assertIn('if (sampleAngle == 0)', self.view)
        self.assertIn('canvas.drawBitmap(canon, 0f, 0f, imagePaint)', self.view)
        self.assertIn('bodyWithMissingPaint',self.view)
        self.assertIn('Color.WHITE',self.view)
    def test_no_pretend_production(self):
        for flag in ['NOT character art or a head rig','intentionally BLANK underpaint','White seams are failures']:
            self.assertIn(flag,self.view)
    def test_existing_canon_picker_guard_remains(self):
        self.assertIn('require(actual == hash)', self.act)
        self.assertIn('private const val CANON_HASH', self.act)
        self.assertIn('TVKCP413HeadTurnDebugView(this, crop)', self.act)
        self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',self.act)
    def test_audit_exclusive_with_cp413(self):
        self.assertIn('turnVisible = false', self.act)
        self.assertIn('auditButton.isEnabled = !turnVisible',self.act)
        self.assertIn('preview?.setAuditNeutralSource(true)',self.act)
        self.assertIn('clock.setPlaying(running && !auditVisible && !turnVisible)',self.act)
    def test_character_option_debug_only(self):
        self.assertIn('CP413 | Kiểm tra đường ghép đầu (DEBUG)',self.cat)
        self.assertIn('selectedId == "lin_qian" && debugArtPreview',self.cat)

if __name__=='__main__': unittest.main()
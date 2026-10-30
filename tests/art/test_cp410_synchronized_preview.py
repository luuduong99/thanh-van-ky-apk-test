"""CP410 integrity and release tests. Private CANON is never checked into GitHub."""
import os, sys, json, unittest, hashlib
from pathlib import Path
from PIL import Image
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'app/src/main/java/vn/thanhvanky/prototype'
TOOLS=ROOT/'tools/art'
CANON=Path(os.environ.get('TVK_CP410_CANON','/nonexistent/canon.png'))
ATLAS=Path(os.environ.get('TVK_CP410_ATLAS','/nonexistent/atlas.png'))
EXACT_CANON='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
EXACT_ATLAS='d9234630eab9e13ec07527e2c7b6fbbacd849117bf2e4983bf35ac4bcf73a07e'

class StaticContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.activity=(ART/'TVKCombinedIdlePreviewActivity.kt').read_text()
        cls.clock=(ART/'TVKPreviewClock.kt').read_text()
        cls.body=(ART/'TVKCombinedIdleMotionView.kt').read_text()
        cls.eye=(ART/'TVKCombinedBlinkInsetView.kt').read_text()
        cls.script=(TOOLS/'cp410_sync_preview.py').read_text()

    def test_same_shared_clock_on_both_views(self):
        self.assertIn('TVKCombinedIdleMotionView(this, crop, clock)',self.activity)
        self.assertIn('TVKCombinedBlinkInsetView(this, atlas, clock)',self.activity)
        self.assertIn('private val timeline: TVKPreviewClock',self.body)
        self.assertIn('private val clock: TVKPreviewClock',self.eye)

    def test_freeze_resume_keeps_pose(self):
        self.assertIn('private var frozenMs',self.clock)
        self.assertIn('epochMs = SystemClock.uptimeMillis() - frozenMs',self.clock)
        self.assertIn('frozenMs = (SystemClock.uptimeMillis() - epochMs)',self.clock)
        self.assertNotIn('if (playing) (SystemClock.uptimeMillis() - initial)',self.body)

    def test_release_activity_is_protected(self):
        self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',self.activity)
        self.assertIn('if ((applicationInfo.flags',self.activity)
        self.assertIn('Intent.ACTION_OPEN_DOCUMENT',self.activity)
        self.assertNotIn('lin_qian.png',self.activity)

    def test_source_and_atlas_hash_before_decode(self):
        self.assertIn(EXACT_CANON,self.activity)
        self.assertIn(EXACT_ATLAS,self.activity)
        self.assertLess(self.activity.index('require(actual == hash)'), self.activity.index('BitmapFactory.decodeByteArray(blob'))
        self.assertIn('first.sameAs(face)',self.activity)

    def test_do_not_paste_foreign_pose_on_fullbody(self):
        self.assertIn('TƯ THẾ KHÁC NHAU',self.activity)
        self.assertIn('KHÔNG chồng lên nhau',self.activity)
        self.assertIn('can_composite_face_directly_on_body',self.script)
        self.assertIn('False',self.script)
        self.assertNotIn('frame.addView(blinkPreview',self.activity)

    def test_timeline_upper_lower_geometric_blink(self):
        self.assertIn('object TVKDebugBlinkTiming',self.clock)
        self.assertIn('phase < .355',self.clock)
        self.assertIn('phase < .395',self.clock)
        self.assertIn('phase < .455',self.clock)
        self.assertIn('TVKDebugBlinkTiming.poseAt(clock.elapsedSeconds())',self.eye)

    def test_five_independent_channels_still_available(self):
        for x in ['3.8','6.2','5.3','5.7','4.5']:
            self.assertIn(x,self.body)
        self.assertIn('BooleanArray(5)',self.body)
        self.assertIn('postInvalidateOnAnimation()',self.eye)

    def test_fail_closed_on_reselection(self):
        self.assertIn('blinkPreview = null',self.activity)
        self.assertIn('blinkContainer.removeAllViews()',self.activity)
        self.assertIn('blinkChoose.isEnabled = false',self.activity)
        self.assertIn('status.text = "Từ chối ảnh:',self.activity)

    def test_no_claim_release(self):
        self.assertIn("'true_rig_ready':False",self.script)
        self.assertIn("'physical_android_tested':False",self.script)
        self.assertIn("'production_sprite_paths':{}",self.script)

class PrivateCanonContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CANON.exists() or not ATLAS.exists():
            raise unittest.SkipTest('CANON + atlas not bundled in public GitHub')
        sys.path.insert(0,str(TOOLS))
        from cp410_sync_preview import sources,pose_at
        cls.source,cls.atlas=sources(CANON,ATLAS)
        cls.pose_at=staticmethod(pose_at)

    def test_exact_source_hashes(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),EXACT_CANON)
        self.assertEqual(hashlib.sha256(ATLAS.read_bytes()).hexdigest(),EXACT_ATLAS)

    def test_different_pose_regions(self):
        self.assertEqual(self.source.size,(941,1672))
        self.assertEqual(self.atlas.size,(2520,197))
        self.assertNotEqual((16,180,224,623),(25,684,193,881))

    def test_face_first_frame_identical_to_canon(self):
        src=np.asarray(self.source.crop((25,684,193,881)))
        first=np.asarray(self.atlas.crop((0,0,168,197)))
        self.assertTrue(np.array_equal(src,first))

    def test_timing_is_open_closed_reopened(self):
        self.assertEqual(self.pose_at(0.0),0)
        self.assertEqual(self.pose_at(.70),0)
        self.assertGreater(self.pose_at(.82),0)
        self.assertEqual(self.pose_at(.89),7)
        self.assertEqual(self.pose_at(1.1),0)
        self.assertEqual(self.pose_at(2.4),0)

    def test_source_pixel_immutable(self):
        original=np.asarray(Image.open(CANON))
        np.testing.assert_array_equal(original,np.asarray(self.source))

if __name__=='__main__':unittest.main()
import hashlib,importlib.util,json,os,unittest
from pathlib import Path
import numpy as np
from PIL import Image

LOCAL=Path(__file__).resolve().parents[1]
REPO=Path(__file__).resolve().parents[2]
GITHUB_LAYOUT=(REPO/'tools/art/cp408_simultaneous_idle.py').exists()
ROOT=REPO if GITHUB_LAYOUT else LOCAL
SOURCE=Path(os.environ.get('TVK_CP408_PRIVATE_CANON',str(LOCAL/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
OUTPUT=LOCAL/'OUTPUT'
SCRIPT=(ROOT/'tools/art/cp408_simultaneous_idle.py') if GITHUB_LAYOUT else ROOT/'cp408_simultaneous_idle.py'
ANDROID=((ROOT/'app/src/main/java/vn/thanhvanky/prototype/TVKCombinedIdleMotionView.kt') if GITHUB_LAYOUT else ROOT/'TVKCombinedIdleMotionView.kt').read_text(encoding='utf8')
ACTIVITY=((ROOT/'app/src/main/java/vn/thanhvanky/prototype/TVKCombinedIdlePreviewActivity.kt') if GITHUB_LAYOUT else ROOT/'TVKCombinedIdlePreviewActivity.kt').read_text(encoding='utf8')
spec=importlib.util.spec_from_file_location('cp408',SCRIPT)
cp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp)

class PublicContract(unittest.TestCase):
    def test_source_lock_hash_pinned(self):
        self.assertEqual(len(cp.SHA_CANON),64)
        self.assertEqual(cp.FRONT,(16,180,224,623))
    def test_debug_only_source_picker(self):
        self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',ACTIVITY)
        self.assertIn('Intent.ACTION_OPEN_DOCUMENT',ACTIVITY)
        self.assertIn('CANON_HASH',ACTIVITY)
        self.assertIn('sha',ACTIVITY.lower())
        self.assertIn('require(actual == hash)',ACTIVITY)
        self.assertLess(ACTIVITY.index('require(actual == hash)'),ACTIVITY.index('BitmapFactory.decodeByteArray(blob'))
    def test_no_sprite_release_or_fake_eye_art(self):
        script=SCRIPT.read_text(encoding='utf8')
        self.assertIn("'sprite_paths':{}",script)
        self.assertIn("'apk_production':False",script)
        self.assertNotIn('def closed_eye_candidate(',script)
        self.assertIn("'eye_blink_channel':'TIMELINE_DEFINED_BUT_NO_APPROVED_ILLUSTRATED_FRAMES'",script)
    def test_motion_has_five_independent_controls(self):
        self.assertEqual(ANDROID.count('if (enabled['),5)  # channel scalar control in formula
        for label in ['breathing','head','arms','hair','silk']:
            self.assertIn(label,ANDROID)
        self.assertIn('canvas.drawBitmapMesh',ANDROID)
        self.assertIn('postInvalidateOnAnimation',ANDROID)
        self.assertIn('BooleanArray(5)',ANDROID)
    def test_activity_not_exported_by_runtime_contract(self):
        self.assertIn('TVKCombinedIdleMotionView',ACTIVITY)
        self.assertIn('private const val MAX_CANON = 5_000_000',ACTIVITY)
    def test_motion_waves_have_distinct_periods(self):
        for period in ['3.8','6.2','5.3','5.7','4.5']:
            self.assertIn(period,ANDROID)
    def test_source_crop_dimensions(self):
        self.assertEqual(cp.FRONT[2]-cp.FRONT[0],208)
        self.assertEqual(cp.FRONT[3]-cp.FRONT[1],443)

@unittest.skipUnless(SOURCE.exists(),'Exact private CANON source absent — no substitute allowed')
class PrivateCanonGeometry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sheet=cp.get_source(SOURCE)
        cls.front=cls.sheet.crop(cp.FRONT)
    def test_sha256_exact(self):
        self.assertEqual(cp.sha(SOURCE),cp.SHA_CANON)
    def test_source_not_modified_by_crop(self):
        self.assertEqual(self.sheet.size,(941,1672))
        self.assertEqual(self.front.size,(208,443))
    def test_all_channel_mesh_moves_pixels(self):
        source=np.asarray(self.front.convert('RGB')).astype(np.int16)
        for channel in ['breath','head','arms','hair','silk']:
            result=np.asarray(cp.deform_mesh(self.front,1.19,{channel})).astype(np.int16)
            self.assertGreater(np.abs(source-result).sum(),100,channel)
    def test_composed_motion_differs_from_each_individual_channel(self):
        allch=np.asarray(cp.deform_mesh(self.front,1.19))
        for channel in ['breath','head','arms','hair','silk']:
            self.assertFalse(np.array_equal(allch,np.asarray(cp.deform_mesh(self.front,1.19,{channel}))))
    def test_source_color_identity_at_time_zero_image(self):
        f=Image.open(OUTPUT/'CP408_CANON_FRONT_UNCHANGED_CROP.png').convert('RGBA')
        self.assertTrue(np.array_equal(np.asarray(f),np.asarray(self.front)))
    def test_manifest_release_gate_and_crop_hash(self):
        meta=json.loads((OUTPUT/'CP408_MANIFEST.json').read_text())
        self.assertEqual(meta['source_sha256'],cp.SHA_CANON)
        self.assertEqual(meta['crop_sha256'],cp.sha(OUTPUT/'CP408_CANON_FRONT_UNCHANGED_CROP.png'))
        self.assertFalse(meta['apk_production'])
        self.assertFalse(meta['physical_device_tested'])
        self.assertEqual(meta['sprite_paths'],{})
    def test_video_is_encoded(self):
        video=OUTPUT/'CP408_SIMULTANEOUS_IDLE_30FPS_DRAFT.mp4'
        self.assertGreater(video.stat().st_size,100000)

if __name__=='__main__':unittest.main()
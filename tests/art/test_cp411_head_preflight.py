"""CP411 source-lock / face-pose readiness checks, artwork remains private."""
import hashlib, importlib.util, json, os, unittest, zipfile
from pathlib import Path
import numpy as np
from PIL import Image

LOCAL=Path(__file__).resolve().parents[1]
REPO=Path(__file__).resolve().parents[2]
IN_REPO=(REPO/'tools/art/cp411_front_head_preflight.py').exists()
SCRIPT=REPO/'tools/art/cp411_front_head_preflight.py' if IN_REPO else LOCAL/'cp411_front_head_preflight.py'
ANDROID=(REPO/'app/src/main/java/vn/thanhvanky/prototype/TVKFrontPoseRigAuditOverlay.kt') if IN_REPO else LOCAL/'android/TVKFrontPoseRigAuditOverlay.kt'
ACTIVITY=(REPO/'app/src/main/java/vn/thanhvanky/prototype/TVKCombinedIdlePreviewActivity.kt') if IN_REPO else LOCAL/'android/TVKCombinedIdlePreviewActivity.kt'
CANON=Path(os.environ.get('TVK_CP411_PRIVATE_CANON',str(LOCAL/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
OUTPUT=LOCAL/'output'
spec=importlib.util.spec_from_file_location('cp411',SCRIPT)
cp=importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

class PublicSourceContract(unittest.TestCase):
    def test_source_sha_and_crop_pinned(self):
        self.assertEqual(len(cp.CANON_HASH),64)
        self.assertEqual(cp.FRONT,(16,180,224,623))
        self.assertEqual(cp.EXPRESSION,(25,684,193,881))
    def test_roi_is_front_pose_only(self):
        self.assertEqual(cp.FACE_BOX,(83,40,128,74))
        self.assertNotEqual(cp.FRONT,cp.EXPRESSION)
        for rect in [cp.FACE_BOX,*cp.EYE_BOXES.values()]:
            self.assertTrue(0<=rect[0]<rect[2]<=208)
            self.assertTrue(0<=rect[1]<rect[3]<=443)
    def test_head_polygon_and_anchor_in_image(self):
        self.assertGreaterEqual(len(cp.HEAD_CAPSULE),12)
        self.assertTrue(all(0<=x<208 and 0<=y<443 for x,y in cp.HEAD_CAPSULE))
        self.assertEqual(cp.HEAD_PIVOT,(104,77))
    def test_mask_is_binary_and_bounded(self):
        m=np.array(cp.head_binary_mask())
        self.assertEqual(m.shape,(443,208))
        self.assertEqual(set(np.unique(m).tolist()),{0,255})
        self.assertGreater(np.count_nonzero(m),1000)
        self.assertLess(np.count_nonzero(m),10000)
    def test_art_gate_not_promoted(self):
        text=SCRIPT.read_text(encoding='utf8')
        for marker in ["'head_cutout_art_approved':False","'inpaint_art_approved':False", "'long_hair_isolated':False", "'eye_sprite_correct_pose_present':False", "'sprite_paths':{}"]:
            self.assertIn(marker,text)
    def test_head_audit_android_only_as_overlay(self):
        self.assertTrue(ANDROID.exists())
        a=ANDROID.read_text(encoding='utf8')
        self.assertIn('TVKFrontPoseRigAuditOverlay',a)
        self.assertIn('HEAD_POLY',a)
        self.assertIn('CANON 208x443',a)
        if ACTIVITY.exists():
            b=ACTIVITY.read_text(encoding='utf8')
            self.assertIn('TVKFrontPoseRigAuditOverlay',b)
            self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',b)
            self.assertIn('require(actual == hash)',b)
    def test_audit_guide_freezes_and_displays_unwarped_bitmap(self):
        motion=REPO/'app/src/main/java/vn/thanhvanky/prototype/TVKCombinedIdleMotionView.kt' if IN_REPO else LOCAL/'android/TVKCombinedIdleMotionView.kt'
        if not motion.exists():
            self.skipTest('Full Android source checked in on GitHub; absent in local art-only package')
        content=motion.read_text(encoding='utf8')
        self.assertIn('if (auditNeutralSource)',content)
        self.assertIn('canvas.drawBitmap(canonCrop, null, box, paint)',content)
        self.assertLess(content.index('if (auditNeutralSource)'),content.index('val t = timeline.elapsedSeconds()'))
        activity=ACTIVITY.read_text(encoding='utf8')
        self.assertIn('setAuditNeutralSource(true)',activity)
        self.assertIn('setAuditNeutralSource(false)',activity)
    def test_rig_does_not_falsely_claim_true_layers(self):
        t=SCRIPT.read_text(encoding='utf8')
        self.assertIn('NOT production-ready artwork',t)
        self.assertIn('artist_authored_neck_underpaint_present',t)
        self.assertIn('portrait_pose_mismatch',t)

@unittest.skipUnless(CANON.is_file(),"Private CANON file is not shipped in public GitHub")
class PrivateExactArt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.im=cp.load_checked(CANON)
        cls.front=cls.im.crop(cp.FRONT)
        cls.mask,cls.head,cls.plate,cls.neutral=cp.make_layers(cls.front)
    def test_sha_pinned_exact(self):
        self.assertEqual(cp.digest(CANON),cp.CANON_HASH)
    def test_front_crop_identity(self):
        self.assertEqual(self.front.size,(208,443))
        self.assertTrue(np.array_equal(np.array(self.front),np.array(self.im.crop(cp.FRONT))))
    def test_head_alpha_binary_matte(self):
        m=np.array(self.mask)
        self.assertTrue(np.array_equal(np.array(self.head)[:,:,3],np.where(m>0,np.array(self.front)[:,:,3],0)))
    def test_removed_head_is_not_claimed_original_paint(self):
        m=np.array(self.mask)>0
        self.assertTrue(np.all(np.array(self.plate)[~m]==np.array(self.front)[~m]))
        self.assertTrue(np.any(np.array(self.plate)[m,:3] != np.array(self.front)[m,:3]))
    def test_recomposition_is_pixel_exact(self):
        self.assertTrue(np.array_equal(np.array(self.front),np.array(self.neutral)))
    def test_ora_parses_with_only_canon_visible(self):
        path=OUTPUT/'CP411_HEAD_SEPARATION_SOURCE_LOCKED_DRAFT.ora'
        with zipfile.ZipFile(path) as z:
            self.assertEqual(z.read('mimetype'),b'image/openraster')
            import xml.etree.ElementTree as ET
            tree=ET.fromstring(z.read('stack.xml'))
            layers=tree.find('stack').findall('layer')
            self.assertEqual(len(layers),3)
            self.assertEqual([x.attrib['visibility'] for x in layers],['hidden','hidden','visible'])
            self.assertTrue(np.array_equal(np.array(Image.open(z.open('mergedimage.png')).convert('RGBA')),np.array(self.front)))
    def test_report_release_gate(self):
        report=json.loads((OUTPUT/'CP411_REPORT.json').read_text())
        self.assertEqual(report['source_sha256'],cp.CANON_HASH)
        self.assertTrue(report['neutral_pixel_exact'])
        self.assertFalse(report['independent_head_rig_ready'])
        self.assertFalse(report['head_cutout_art_approved'])
        self.assertFalse(report['eye_sprite_correct_pose_present'])
        self.assertEqual(report['sprite_paths'],{})

if __name__=='__main__':unittest.main()
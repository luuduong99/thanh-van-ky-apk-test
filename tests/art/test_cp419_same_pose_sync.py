"""CP419 static/source integrity checks. DOES NOT approve visual quality, FPS, rig, or phone execution."""
from __future__ import annotations
import hashlib
import os
import unittest
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
ACT=REPO/'app/src/main/java/vn/thanhvanky/prototype/TVKCP417SamePoseBlinkActivity.kt'
if not ACT.exists(): ACT=Path(__file__).with_name('TVKCP417SamePoseBlinkActivity.kt')
MENU=REPO/'app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt'
if not MENU.exists(): MENU=Path(__file__).with_name('CharacterInteractionActivity.kt')
SPEC=REPO/'docs/PROJECT_SPEC.md'
CANON=Path(os.getenv('TVK_CP419_CANON','/no/private/canon'))
ATLAS=Path(os.getenv('TVK_CP419_ATLAS','/no/private/atlas'))
CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
ATLAS_SHA='cb6cbe03cb1b9ccd3201e4a6bb6ba0e9cc3225111c4f78d441d7d9d7296d05cb'

class PublicContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=ACT.read_text(encoding='utf8')
    def test_exact_source_and_atlas_hash(self):
        self.assertIn(CANON_SHA,self.src)
        self.assertIn(ATLAS_SHA,self.src)
        self.assertIn('decodeVerified(uri, CANON_SHA',self.src)
        self.assertIn('decodeVerified(uri, ATLAS_SHA',self.src)
    def test_frame_identity_fullbody_not_portrait(self):
        for phrase in ['private const val W = 208','private const val H = 443','private const val FRAMES = 5','Bitmap.createBitmap(atlas, it*W, 0, W, H)']:
            self.assertIn(phrase,self.src)
        self.assertNotIn('CP409_15_POSE',self.src)
        self.assertIn('if (!first.sameAs(source)) return null',self.src)
    def test_one_clock_drives_blink_and_mesh(self):
        self.assertIn('val seconds = elapsedSeconds()',self.src)
        self.assertIn('currentFrame(seconds)',self.src)
        self.assertIn('drawSamePoseMotion(canvas, slices[i], destination, seconds)',self.src)
        self.assertIn('frameOverride ?: currentFrame(seconds)',self.src)
    def test_motion_is_actual_mesh_not_fake_static_image(self):
        self.assertIn('canvas.drawBitmapMesh(frame,motionColumns,motionRows,motionMesh,0,null,0,paint)',self.src)
        self.assertIn('motionColumns = 20',self.src)
        self.assertIn('motionRows = 36',self.src)
        for name in ['breath','head','arm','hair','silk']:
            self.assertIn('val '+name+'=',self.src)
    def test_play_pause_and_scrub_are_preserved(self):
        for phrase in ['fun setFrameOverride(index: Int?)','fun setPlaying(on: Boolean)','override fun onStop()', 'override fun onResume()', 'var comparing = false']:
            self.assertIn(phrase,self.src)
        self.assertIn('viewer.setCombinedMode(requestedCombined)',self.src)
    def test_cp419_is_debug_only_in_character_menu(self):
        self.assertIn('ApplicationInfo.FLAG_DEBUGGABLE',self.src)
        self.assertIn('cp419_combined',self.src)
        menu=MENU.read_text(encoding='utf8')
        self.assertIn('CP419 | Idle + mắt (DEBUG)',menu)
        self.assertIn('putExtra("cp419_combined", true)',menu)
    def test_no_production_art_promotion(self):
        self.assertIn('KHÔNG phải rig/Spine',self.src)
        self.assertNotIn('app/src/main/assets/LAM_THIEN_CANON',self.src)
        self.assertIn('if (sourcePixel != atlasPixel)',self.src)
        self.assertIn('if (!inLeft && !inRight) return null',self.src)

@unittest.skipUnless(CANON.is_file() and ATLAS.is_file(),'Private CANON and atlas absent on public GitHub')
class PrivateExactSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PIL import Image
        cls.im=Image.open(CANON).convert('RGBA')
        cls.atlas=Image.open(ATLAS).convert('RGBA')
    def test_raw_byte_hash(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),CANON_SHA)
        self.assertEqual(hashlib.sha256(ATLAS.read_bytes()).hexdigest(),ATLAS_SHA)
    def test_frame0_same_front_pose(self):
        self.assertEqual(self.im.size,(941,1672))
        self.assertEqual(self.atlas.size,(1040,443))
        self.assertEqual(self.im.crop((16,180,224,623)).tobytes(),self.atlas.crop((0,0,208,443)).tobytes())
    def test_no_painted_damage_outside_eyes(self):
        import numpy as np
        arr=np.asarray(self.atlas)
        source=arr[:,:208]
        mask=np.zeros((443,208),bool)
        mask[50:56,88:104]=1;mask[50:57,107:124]=1
        for i in range(5):
            crop=arr[:,i*208:(i+1)*208]
            changed=np.any(crop!=source,axis=2)
            self.assertFalse(np.any(changed & ~mask),str(i))

if __name__=='__main__':unittest.main()
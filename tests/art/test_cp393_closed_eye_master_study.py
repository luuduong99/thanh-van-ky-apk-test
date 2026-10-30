"""CP393 tests. Local source assets are private, so public CI intentionally SKIPs source tests."""
from __future__ import annotations
import os,sys,tempfile,unittest,hashlib,zipfile,io
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cp393_closed_eye_master_study as m
CANON=Path(os.getenv('TVK_CANON_PATH','/mnt/data/CP392/OUTPUT/LAM_THIEN_CANON_V2_1_FINAL_20261029.png'))
PRIOR=Path(os.getenv('TVK_CP392_DRAFT_PATH','/mnt/data/CP392/OUTPUT/CP392_NEAR_CLOSED_DRAFT_NOT_APPROVED.png'))

class PublicStatic(unittest.TestCase):
    def test_sha_policy(self):self.assertEqual(len(m.CANON_SHA),64);self.assertEqual(m.SIZE,(168,197))
    def test_rois(self):
        a=m.ROI['LEFT'];b=m.ROI['RIGHT']
        self.assertTrue(a[2]<b[0]);self.assertTrue(all(0<=v<=197 for v in a+b))
    def test_semantic_sides(self):
        self.assertEqual(set(m.EYES),{'LEFT','RIGHT'})
        for g in m.EYES.values():self.assertEqual(set(g),{'upper','lower','lash','crease','donor_shift'})
    def test_release_locked(self):
        self.assertEqual(m.RELEASE['status'],'blocked_pending_art')
        self.assertEqual(m.RELEASE['sprite_paths'],{})
        self.assertFalse(m.RELEASE['spine_ready']);self.assertFalse(m.RELEASE['apk_ready'])

@unittest.skipUnless(CANON.is_file() and PRIOR.is_file(),'Private approved source art absent')
class PrivateCANON(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src=m.source_checked(CANON)
        cls.layers={s:{'SKIN':m.donor_layer(cls.src,s),'SHADOW':m.make_shadows(s),'LASH':m.make_lash(s)} for s in ['LEFT','RIGHT']}
        cls.art=m.paint(cls.src,cls.layers)
    def test_canon_sha(self):self.assertEqual(m.hash_file(CANON),m.CANON_SHA)
    def test_crop_is_pixel_exact(self):
        with Image.open(CANON) as original:
            self.assertTrue(np.array_equal(np.asarray(original.crop(m.CROP)),np.asarray(self.src)))
    def test_six_nonempty_alpha_layers(self):
        for side in self.layers:
            for name,layer in self.layers[side].items():
                self.assertGreater(np.count_nonzero(np.asarray(layer)[:,:,3]),1,(side,name))
    def test_draft_constrained_to_eye_rois(self):
        self.assertEqual(m.changed_outside(self.src,self.art),0)
        self.assertGreater(np.count_nonzero(np.any(np.asarray(self.src)!=np.asarray(self.art),axis=2)),100)
    def test_ora_9_layers_and_exact_visible_canon(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.ora';n=m.make_ora(self.src,self.layers,self.art,m.paint(self.src,self.layers,True),p)
            self.assertEqual(n,9)
            with zipfile.ZipFile(p) as z:
                self.assertIsNone(z.testzip())
                tree=ET.fromstring(z.read('stack.xml'));layers=tree.find('stack')
                self.assertEqual(len(layers),9)
                self.assertEqual(sum(x.attrib.get('visibility')=='visible' for x in layers),1)
                self.assertTrue(np.array_equal(np.asarray(Image.open(io.BytesIO(z.read('mergedimage.png')))),np.asarray(self.src)))
    def test_reject_wrong_source_without_writing_output(self):
        with tempfile.TemporaryDirectory() as d:
            wrong=Path(d)/'wrong.png';output=Path(d)/'out'
            b=bytearray(CANON.read_bytes());b[-12]^=1;wrong.write_bytes(b)
            with self.assertRaises(ValueError):m.create(wrong,PRIOR,output)
            self.assertFalse(output.exists())

if __name__=='__main__':unittest.main(verbosity=2)
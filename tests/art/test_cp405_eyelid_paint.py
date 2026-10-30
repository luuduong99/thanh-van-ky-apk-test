"""Source-locked CP405 technique checks. Artist approval is NEVER inferred."""
import os, sys, unittest, tempfile, hashlib, zipfile, io, json
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import cp405_eyelid_paint as m
import cp401_occlusion_blink as base
CANON=Path(os.getenv('TVK_CP405_CANON','/no_private_art_found'))
PREVIOUS=Path(os.getenv('TVK_CP405_PREVIOUS','/no_previous_art_found'))
OUT=ROOT/'outputs'
class StaticSourceGate(unittest.TestCase):
 def test_canon_hash_pinned(self):self.assertEqual(base.CANON_SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
 def test_approved_source_shape(self):self.assertEqual(base.SIZE,(168,197));self.assertEqual(base.SRC_SIZE,(941,1672))
 def test_rois_unchanged(self):self.assertEqual(base.ROIS,{'LEFT':(29,93,71,124),'RIGHT':(83,70,129,110)})
 def test_frame_count(self):self.assertEqual(len(m.FRAME_STEPS),15);self.assertEqual(m.FRAME_STEPS[0],0);self.assertEqual(m.FRAME_STEPS[-1],0);self.assertEqual(max(m.FRAME_STEPS),1)
 def test_no_approved_assets_claim(self):
  code=Path(m.__file__).read_text();self.assertIn('NOT APPROVED',code.upper());self.assertIn("'sprite_paths':{}",code)
 def test_no_substitute_character(self):self.assertNotIn('imagegen',m.draw_master.__code__.co_names)

@unittest.skipUnless(CANON.exists() and PREVIOUS.exists(),'Private exact source absent — never substitute another character')
class PrivateArtGate(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.src,cls.closed,cls.under,cls.layers=m.draw_master(CANON)
 def test_source_bytes(self):self.assertEqual(m.sha(CANON),base.CANON_SHA)
 def test_source_dimensions(self):self.assertEqual(self.src.size,base.SIZE)
 def test_outside_eye_unchanged(self):self.assertEqual(base.valid_pixels_only(self.src,self.closed),0)
 def test_alpha_unchanged(self):self.assertTrue(np.array_equal(np.array(self.src)[:,:,3],np.array(self.closed)[:,:,3]))
 def test_five_editable_semantic_parts(self):self.assertEqual(len(self.layers),5);self.assertTrue(all(np.array(im)[:,:,3].any() for im in self.layers.values()))
 def test_layers_within_eye_bounds(self):
  allow=np.zeros((197,168),bool)
  for x1,y1,x2,y2 in base.ROIS.values():allow[y1:y2,x1:x2]=True
  for im in self.layers.values():self.assertFalse(np.any(np.array(im)[:,:,3][~allow]))
 def test_change_actually_occurred(self):self.assertGreater(int(np.any(np.array(self.src)!=np.array(self.closed),axis=2).sum()),300)
 def test_reproducibility(self):
  src2,closed2,_,_=m.draw_master(CANON)
  self.assertTrue(np.array_equal(np.array(self.closed),np.array(closed2)))
 def test_reject_source_tampering(self):
  with tempfile.TemporaryDirectory() as td:
   wrong=Path(td)/'x.png';im=Image.open(CANON).convert('RGBA');im.putpixel((1,1),(0,0,0,255));im.save(wrong)
   with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):m.draw_master(wrong)
 def test_ora_canon_stays_visible(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'eye.ora';m.make_ora(self.src,self.under,self.layers,self.closed,p)
   with zipfile.ZipFile(p) as z:
    self.assertEqual(z.read('mimetype'),b'image/openraster')
    stack=ET.fromstring(z.read('stack.xml')).find('stack')
    layer_rows=stack.findall('layer')
    self.assertEqual(len(layer_rows),8)
    self.assertEqual(sum(a.get('visibility')=='visible' for a in layer_rows),1)
    self.assertIn('CANON',layer_rows[-1].get('name'))
    source=Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA')
    self.assertTrue(np.array_equal(np.asarray(source),np.asarray(self.src)))
 def test_poses_within_eye(self):
  for p in [0,.25,.5,.75,1]:
   x=base.eyelid_position(self.src,self.closed,p)
   self.assertEqual(base.valid_pixels_only(self.src,x),0)
 def test_open_ends_exact(self):
  self.assertTrue(np.array_equal(np.asarray(self.src),np.asarray(base.eyelid_position(self.src,self.closed,0))))
 def test_video_and_sprite_not_approved(self):
  report=json.loads((OUT/'CP405_REPORT.json').read_text());self.assertEqual(report['keyframe_visual_approval'],'PENDING');self.assertEqual(report['production_release']['sprite_paths'],{});self.assertFalse(report['production_release']['apk_ready'])
 def test_tampered_previous_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   wrong=Path(td)/'invalid.png'
   arr=np.asarray(self.src).copy();arr[0,0,0]=arr[0,0,0]^16;Image.fromarray(arr,'RGBA').save(wrong)
   with self.assertRaisesRegex(ValueError,'INVALID_PREVIOUS_BASELINE'):m.build(CANON,wrong,Path(td)/'bad_result')

if __name__=='__main__':unittest.main()
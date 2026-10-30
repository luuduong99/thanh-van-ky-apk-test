"""CP372 semantic overlay regression checks; PASS != artwork approval."""
import hashlib, importlib.util, tempfile, unittest, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import numpy as np

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cp372',HERE/'cp372_finger_gold_detail.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CAN=HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
OUT=HERE/'OUTPUT'
HAS_ASSETS=CAN.exists() and (OUT/'CP372_IDLE_TWELVE_LAYER_DRAFT_NOT_SPINE.ora').exists() and (OUT/'CP372_RAISED_TWELVE_LAYER_DRAFT_NOT_SPINE.ora').exists()

class TestCP372(unittest.TestCase):
    def test_source_lock_constants(self):
        self.assertEqual(m.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.SIZE,(1302,2748))
        self.assertEqual(len(m.ORDER),12)
        self.assertEqual(m.FRONT,(13,172,230,630))

    def test_distinct_pose_specific_paths(self):
        for name in (m.HAND,m.WRIST):
            self.assertNotEqual(m.source_svg(name,'idle'),m.source_svg(name,'raised'))
        self.assertEqual(m.source_svg(m.SHOULDER,'idle'),m.source_svg(m.SHOULDER,'raised'))

    def test_new_geometry_is_svg_without_embedded_raster(self):
        for pose in ('idle','raised'):
            for name in m.PARENTS:
                s=m.source_svg(name,pose)
                ET.fromstring(s)
                self.assertIn('<path',s)
                self.assertNotIn('image href=',s)

    def test_release_gate_explicit(self):
        s=(HERE/'cp372_finger_gold_detail.py').read_text(encoding='utf8')
        self.assertIn("'visual_qa':'NOT_PASSED'",s)
        self.assertIn("'production_release':'blocked_pending_art'",s)
        self.assertIn("'sprite_paths':{}",s)

    def test_wrong_source_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            where=Path(directory)
            fake=where/'wrong.png';Image.new('RGBA',(941,1672),'white').save(fake)
            target=where/'should_not_exist'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                m.build(fake,target)
            self.assertFalse(target.exists())

    def test_masked_overlay_preserves_parent_alpha(self):
        parent=Image.new('RGBA',(10,10),(50,60,70,0))
        parent.putpixel((5,5),(50,60,70,255))
        overlay=Image.new('RGBA',(10,10),(255,200,100,255))
        clipped=m.mask_overlay(overlay,parent)
        self.assertEqual(clipped.getpixel((0,0))[3],0)
        self.assertEqual(clipped.getpixel((5,5))[3],255)

    @unittest.skipUnless(HAS_ASSETS,'Local user-approved CANON/ORA binary unavailable in CI')
    def test_canon_hash(self):
        self.assertEqual(hashlib.sha256(CAN.read_bytes()).hexdigest(),m.SHA)

    @unittest.skipUnless(HAS_ASSETS,'Private ORA outputs not checked into repo')
    def test_ora_crc_and_exact_layers(self):
        for pose in ('IDLE','RAISED'):
            with zipfile.ZipFile(OUT/f'CP372_{pose}_TWELVE_LAYER_DRAFT_NOT_SPINE.ora') as z:
                self.assertIsNone(z.testzip())
                stack=ET.fromstring(z.read('stack.xml')).find('stack').findall('layer')
                self.assertEqual(len(stack),13)
                self.assertEqual(sum(x.get('visibility')=='hidden' for x in stack),1)
                self.assertIn('CANON_V2_1_REFERENCE_ONLY_HIDDEN',stack[-1].get('name'))

    @unittest.skipUnless(HAS_ASSETS,'Local CANON and rendered output needed')
    def test_production_report_and_real_overlay(self):
        import json
        r=json.loads((OUT/'CP372_REPORT.json').read_text())
        self.assertEqual(r['visual_qa'],'NOT_PASSED')
        self.assertEqual(r['production_release'],'blocked_pending_art')
        self.assertFalse(r['native_high_res_full_body_art'])
        self.assertTrue(r['static_shoulder_detail_identical_across_poses'])
        self.assertTrue(all(n>0 for n in r['composite_pixels_different_from_cp371'].values()))

    @unittest.skipUnless(HAS_ASSETS,'Local output required')
    def test_new_art_alpha_within_semantic_parents(self):
        for pose in ('idle','raised'):
            directory=OUT/pose
            for name,parent in m.PARENTS.items():
                alpha=np.asarray(Image.open(directory/f'{name}.png').getchannel('A'))>0
                parent_alpha=np.asarray(Image.open(directory/f'{parent}.png').getchannel('A'))>0
                self.assertGreater(int(alpha.sum()),0)
                self.assertEqual(int((alpha & ~parent_alpha).sum()),0)

    @unittest.skipUnless(HAS_ASSETS,'Local output required')
    def test_static_gold_and_raised_wrist_changes(self):
        def read(pose,name):return np.asarray(Image.open(OUT/pose/f'{name}.png'))
        self.assertTrue(np.array_equal(read('idle',m.SHOULDER),read('raised',m.SHOULDER)))
        self.assertFalse(np.array_equal(read('idle',m.WRIST),read('raised',m.WRIST)))
        self.assertFalse(np.array_equal(read('idle',m.HAND),read('raised',m.HAND)))

if __name__=='__main__':unittest.main()
"""CP369 technical regression suite; never art acceptance or a Spine proof."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageChops

HERE=Path(__file__).resolve().parent
SCRIPT=(HERE/'cp369_split_gold_and_underpaint.py')
if not SCRIPT.exists(): SCRIPT=HERE.parent.parent/'tools'/'art'/'cp369_split_gold_and_underpaint.py'
spec=importlib.util.spec_from_file_location('cp369',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
CANON=Path(os.environ.get('TVK_CANON', str(HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
OUT=Path(os.environ.get('TVK_CP369_OUT', str(HERE/'OUTPUT')))
HAS_BINARY=CANON.exists() and (OUT/'CP369_QA_REPORT.json').exists()

class CP369Test(unittest.TestCase):
    def test_source_constants_and_release_immutable(self):
        self.assertEqual(m.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(m.FRONT,(13,172,230,630))
        self.assertEqual(m.SIZE,(1302,2748))
        self.assertEqual(len(m.ORDER),7)
        self.assertNotIn(m.SHOULDER_NAME,m.MOTIONAL)
        self.assertIn(m.WRIST_NAME,m.MOTIONAL)

    def test_editable_distinct_source_layers(self):
        self.assertEqual(set(m.ORDER),set(m.STATIC_NAMES)|set(m.ARM_NAMES)|{m.WRIST_NAME,m.SHOULDER_NAME})
        for name in m.ORDER:
            with self.subTest(name=name):
                source=m.svg_layer(name)
                ET.fromstring(source)
                self.assertIn('<path',source)
                self.assertNotIn('<image ',source)
        self.assertNotEqual(m.svg_layer(m.WRIST_NAME),m.svg_layer(m.SHOULDER_NAME))

    def test_wrong_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake=Path(tmp)/'notcanon.png'
            Image.new('RGBA',(941,1672),'white').save(fake)
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                m.make(fake,Path(tmp)/'out')

    @unittest.skipUnless(HAS_BINARY,'Exact private CANON and generated ORA unavailable in CI')
    def test_exact_canon_sha_and_reference_pixels(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),m.SHA)
        with zipfile.ZipFile(OUT/'CP369_SEVEN_LAYER_SEPARATED_SHOULDER_WRIST_NOT_SPINE.ora') as z:
            with Image.open(CANON) as image:
                ref=image.crop(m.FRONT)
                nearest=ref.resize(m.SIZE,Image.Resampling.NEAREST)
            img=Image.open(io.BytesIO(z.read('data/reference.png'))).convert('RGBA')
            self.assertIsNone(ImageChops.difference(nearest,img).getbbox())

    @unittest.skipUnless(HAS_BINARY,'Exact private CANON and generated ORA unavailable in CI')
    def test_openraster_seven_painted_layers_one_hidden_guide(self):
        path=OUT/'CP369_SEVEN_LAYER_SEPARATED_SHOULDER_WRIST_NOT_SPINE.ora'
        with zipfile.ZipFile(path) as z:
            self.assertIsNone(z.testzip())
            tree=ET.fromstring(z.read('stack.xml'))
            layers=tree.find('stack').findall('layer')
            self.assertEqual(len(layers),8)
            self.assertEqual(sum(x.get('visibility')=='visible' for x in layers),7)
            self.assertEqual(sum(x.get('visibility')=='hidden' for x in layers),1)
            self.assertIn('CANON',layers[-1].get('name'))
            for layer in layers[:-1]:
                image=Image.open(io.BytesIO(z.read(layer.get('src')))).convert('RGBA')
                self.assertEqual(image.size,m.SIZE)
                self.assertIsNotNone(image.getchannel('A').getbbox())

    @unittest.skipUnless(HAS_BINARY,'Exact private CANON and generated ORA unavailable in CI')
    def test_shoulder_hardware_fixed_while_wrist_moves(self):
        layers={name:Image.open(OUT/(name+'.png')).convert('RGBA') for name in m.ORDER}
        a=m.rotate_arm_group(layers,-15)
        b=m.composite_in_order(layers)
        # Shoulder gold overlays moving art and remains pixel-exact at its center.
        xy=(round(67.4*6),round(134.2*6))
        self.assertEqual(b.getpixel(xy),a.getpixel(xy))
        # The wrist component is moved with the arm, not glued to the shoulder.
        self.assertNotEqual(m.rotate_arm_group(layers,-15).tobytes(),b.tobytes())

    @unittest.skipUnless(HAS_BINARY,'Exact private CANON and generated ORA unavailable in CI')
    def test_local_revealed_joint_is_backed_and_negative_control_fails(self):
        layers={name:Image.open(OUT/(name+'.png')).convert('RGBA') for name in m.ORDER}
        intact=m.metrics(layers)
        for angle in ('-8','-15','8'):
            self.assertGreater(intact[angle]['revealed_rest_arm_pixels'],0)
            self.assertEqual(intact[angle]['revealed_missing_body_underpaint'],0)
        bare=layers.copy()
        for k in ('02_hidden_bodice_cloth','03_hidden_shoulder_skin'):
            bare[k]=Image.new('RGBA',m.SIZE)
        control=m.metrics(bare)
        self.assertGreater(control['-15']['revealed_missing_body_underpaint'],0)
        self.assertGreater(control['8']['revealed_missing_body_underpaint'],0)

    @unittest.skipUnless(HAS_BINARY,'Exact private CANON and generated ORA unavailable in CI')
    def test_gate_remains_blocked(self):
        report=json.loads((OUT/'CP369_QA_REPORT.json').read_text(encoding='utf-8'))
        self.assertEqual(report['visual_qa'],'NOT_PASSED')
        self.assertEqual(report['production_release'],'blocked_pending_art')
        self.assertFalse(report['spine_ready'])
        self.assertFalse(report['apk_ready'])
        self.assertEqual(report['sprite_paths'],{})

if __name__=='__main__':unittest.main()
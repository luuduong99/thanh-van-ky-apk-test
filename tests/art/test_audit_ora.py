"""CP315 deterministic ORA QA tests. All test assets are synthetic, not real Lâm Thiển art."""
import argparse
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image, ImageDraw

sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'tools' / 'art'))
import audit_ora as audit


SIZE=(100,100)


def make_ora(path, *, filled_underpaint=True, torso_edits=()):
    torso=Image.new('RGBA',SIZE,(0,0,0,0))
    draw=ImageDraw.Draw(torso)
    draw.rectangle((15,15,80,80),fill=(90,152,175,255))
    if not filled_underpaint:
        draw.rectangle((40,35,50,48),fill=(0,0,0,0))
    for (x,y,color) in torso_edits:
        draw.rectangle((x,y,x+2,y+2),fill=color)
    hair=Image.new('RGBA',SIZE,(0,0,0,0))
    ImageDraw.Draw(hair).rectangle((40,25,60,65),fill=(231,231,241,255))
    layers=[('hair_back',hair),('shoulder_underpaint',torso)]
    for i in range(8):
        layers.append((f'placeholder_{i+1}',Image.new('RGBA',SIZE)))
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'name':'Synthetic fixture'})
    stack=ET.SubElement(root,'stack')
    composite=Image.new('RGBA',SIZE)
    for (_,im) in reversed(layers):
        composite=Image.alpha_composite(composite,im)
    with zipfile.ZipFile(path,'w') as z:
        for i,(name,im) in enumerate(layers):
            dest=f'data/layer{i}.png'
            ET.SubElement(stack,'layer',{'name':name,'src':dest,'x':'0','y':'0','opacity':'1','visibility':'visible','composite-op':'svg:src-over'})
            data=io.BytesIO()
            im.save(data,format='PNG')
            z.writestr(dest,data.getvalue())
        z.writestr('stack.xml',ET.tostring(root))
        data=io.BytesIO()
        composite.save(data,format='PNG')
        z.writestr('mergedimage.png',data.getvalue())
    return composite


def args(source,out,**kw):
    d=dict(source=str(source),out=str(out),expect_layers=10,baseline=None,allowed_roi=[],
           max_outside_changes=0,roi=[],motion_layer=[],motion_roi=None,motion_px=5,max_holes=0)
    d.update(kw)
    return argparse.Namespace(**d)


class AuditTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_complete_underpaint_motion_passes(self):
        p=self.root/'pass.ora'
        make_ora(p,filled_underpaint=True)
        result=audit.run(args(p,self.root/'out',motion_layer=['hair'],motion_roi='35,30,30,30'))
        report=json.loads((self.root/'out'/'report.json').read_text())
        self.assertEqual(result,0)
        self.assertEqual(report['motion_test']['max_new_interior_holes'],0)
        self.assertEqual(report['layer_count'],10)

    def test_hole_uncovered_by_hair_motion_fails(self):
        p=self.root/'fail.ora'
        make_ora(p,filled_underpaint=False)
        result=audit.run(args(p,self.root/'out',motion_layer=['hair'],motion_roi='35,30,30,30'))
        report=json.loads((self.root/'out'/'report.json').read_text())
        self.assertEqual(result,1)
        self.assertGreater(report['motion_test']['max_new_interior_holes'],0)

    def test_repair_inside_allowed_roi_succeeds(self):
        base=self.root/'base.ora'; edited=self.root/'edited.ora'
        image=make_ora(base)
        base_png=self.root/'baseline.png'; image.save(base_png)
        make_ora(edited,torso_edits=[(70,70,(200,50,50,255))])
        result=audit.run(args(edited,self.root/'out',baseline=str(base_png),allowed_roi=['68,68,8,8']))
        report=json.loads((self.root/'out'/'report.json').read_text())
        self.assertEqual(result,0)
        self.assertGreater(report['baseline_comparison']['within_allowed_rois'],0)
        self.assertEqual(report['baseline_comparison']['outside_allowed_rois'],0)

    def test_unintended_edit_outside_roi_fails(self):
        base=self.root/'base.ora'; edited=self.root/'edited.ora'
        image=make_ora(base); baseline=self.root/'baseline.png'; image.save(baseline)
        make_ora(edited,torso_edits=[(70,70,(200,50,50,255))])
        result=audit.run(args(edited,self.root/'out',baseline=str(baseline),allowed_roi=['20,20,10,10']))
        report=json.loads((self.root/'out'/'report.json').read_text())
        self.assertEqual(result,1)
        self.assertGreater(report['baseline_comparison']['outside_allowed_rois'],0)

    def test_roi_bound_validation(self):
        with self.assertRaises(ValueError):
            audit.parse_roi('95,95,10,10',SIZE)


if __name__=='__main__':
    unittest.main(verbosity=2)
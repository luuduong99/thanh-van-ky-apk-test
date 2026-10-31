"""Synthetic unit tests for CP356. They do NOT prove real art readiness."""
import io
import tempfile
import unittest
from pathlib import Path
import zipfile
from xml.etree.ElementTree import Element, SubElement, tostring
from PIL import Image
import sys
candidate_repo=Path(__file__).resolve().parents[2]/'tools'/'art'
candidate_bundle=Path(__file__).resolve().parents[1]/'tools'
sys.path.insert(0,str(candidate_repo if candidate_repo.is_dir() else candidate_bundle))
from cp356_native_art_preflight import inspect, REQUIRED


def png(canvas, painted):
    img=Image.new('RGBA',canvas,(0,0,0,0))
    if painted:
        img.putpixel((10,10),(12,90,180,255))
    output=io.BytesIO();img.save(output,'PNG');return output.getvalue()


def make_ora(path,canvas,missing=()):
    root=Element('image',w=str(canvas[0]),h=str(canvas[1]))
    stack=SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster')
        for idx,(role,name) in enumerate(REQUIRED.items()):
            source=f'data/layer{idx}.png'
            SubElement(stack,'layer',name=name,src=source,visibility='visible',opacity='1.0',x='0',y='0',composite_op='svg:src-over')
            z.writestr(source,png(canvas,role not in missing))
        z.writestr('stack.xml',tostring(root))


class Cp356Test(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.ora=self.root/'front.ora'
        self.canvas=(50,80)

    def test_empty_semantic_underpaint_fails(self):
        make_ora(self.ora,self.canvas,{'hidden_shoulder_skin','hidden_shoulder_bodice'})
        result=inspect(self.ora,minimum=(50,80))
        self.assertEqual(result['semantic_roles_populated'],4)
        self.assertEqual(result['technical_status'],'BLOCKED')
        self.assertEqual(result['required_roles']['hidden_shoulder_skin']['status'],'EMPTY')

    def test_nonempty_layers_still_need_canon_and_pose_pair(self):
        make_ora(self.ora,self.canvas)
        result=inspect(self.ora,minimum=(50,80))
        self.assertEqual(result['semantic_roles_populated'],6)
        self.assertEqual(result['technical_status'],'BLOCKED')
        self.assertTrue(any('CANON' in e for e in result['errors']))

    def test_single_pixel_placeholders_rejected(self):
        make_ora(self.ora,self.canvas)
        result=inspect(self.ora,minimum=(50,80))
        self.assertTrue(any('almost empty' in e for e in result['errors']))

    def test_incorrect_or_unfinished_ora_rejected(self):
        self.ora.write_text('invalid')
        result=inspect(self.ora,minimum=(50,80))
        self.assertEqual(result['technical_status'],'BLOCKED')
        self.assertTrue(any('Invalid ORA' in e for e in result['errors']))

    def test_real_pose_pair_must_differ(self):
        make_ora(self.ora,self.canvas)
        idle=self.root/'idle.png'; moved=self.root/'moved.png'
        Image.new('RGBA',self.canvas,(0,0,0,0)).save(idle)
        Image.new('RGBA',self.canvas,(0,0,0,0)).save(moved)
        result=inspect(self.ora,idle=idle,raise_frame=moved,minimum=(50,80))
        self.assertTrue(any('no visible movement' in e for e in result['errors']))

    def test_reference_layers_cannot_count_as_semantic_art(self):
        make_ora(self.ora,self.canvas,{'left_sleeve'})
        with zipfile.ZipFile(self.ora,'a') as z:
            z.writestr('reference_only_fake.png',png(self.canvas,True))
        result=inspect(self.ora,minimum=(50,80))
        self.assertEqual(result['required_roles']['left_sleeve']['status'],'EMPTY')
        self.assertEqual(result['semantic_roles_populated'],5)


if __name__=='__main__':unittest.main()
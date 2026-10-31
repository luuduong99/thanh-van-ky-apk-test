"""CP365 renderer tests on synthetic semantic paint, never approvals of Lâm Thiển."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[2] / 'tools' / 'art' / 'cp365_pose_exporter.py').exists() else Path(__file__).resolve().parent
SCRIPT = (ROOT / 'tools' / 'art' / 'cp365_pose_exporter.py') if (ROOT / 'tools' / 'art' / 'cp365_pose_exporter.py').exists() else (ROOT / 'cp365_pose_exporter.py')
spec=importlib.util.spec_from_file_location('cp365_pose_exporter',SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
REAL_CANON=Path(__file__).with_name('LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
REAL_SCAFFOLD=Path(__file__).with_name('CP350_NATIVE_PAINTING_SCAFFOLD_NOT_ART_NOT_RIG.ora')

def dummy_canon(directory):
    path=Path(directory)/'canon.fixture'
    path.write_bytes(b'CP365 synthetic test fixture, NOT CANON image')
    return path


def fake_ora(path, visible_flat=False, empty=None):
    size=(160,320)
    root=ET.Element('image',{'w':str(size[0]),'h':str(size[1]),'version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    names=list(m.REQUIRED.values())
    # Order sleeve then arm skin then hidden skin/bodice/back hair.
    if visible_flat:
        names.append('17__FLAT_REFERENCE_ONLY_NOT_PAINT')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster')
        for i,name in enumerate(names):
            img=Image.new('RGBA',size)
            if name!=empty and 'REFERENCE' not in name:
                painter=ImageDraw.Draw(img)
                painter.rectangle((20+i*3,55+i*8,95+i*2,125+i*8),fill=(80+i*15,120,175,255))
            if 'REFERENCE' in name:
                ImageDraw.Draw(img).rectangle((0,0,159,319),fill=(170,170,170,255))
            out=io.BytesIO();img.save(out,format='PNG')
            src=f'data/{i}.png';z.writestr(src,out.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':src,'x':'0','y':'0','visibility':'visible'})
        z.writestr('stack.xml',ET.tostring(root))


class Cp365ProductionRendererTests(unittest.TestCase):
    @unittest.skipUnless(REAL_CANON.exists() and REAL_SCAFFOLD.exists(), 'Local asset-only test: requires Library input bytes')
    def test_real_user_master_is_blocked_instead_of_faking_art(self):
        result,_,_=m.assess(REAL_SCAFFOLD,REAL_CANON)
        self.assertEqual(result['technical_status'],'BLOCKED')
        self.assertEqual(sum(x['nonempty'] for x in result['roles'].values()),0)
        self.assertTrue(result['flat_reference_visible'])

    def test_artists_can_export_same_size_two_pose_technical_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);fake_ora(tmp/'fake.ora')
            canon=dummy_canon(tmp)
            with mock.patch.object(m,'CANON_SHA',m.sha256(canon)):
                report=m.export(tmp/'fake.ora',canon,tmp/'out',-8,(80,110),min_size=(160,320))
            self.assertEqual(report['technical_status'],'READY_FOR_MOTION_DRAFT')
            self.assertFalse(report['runtime_approved'])
            a=Image.open(tmp/'out'/'CP365_IDLE_TECHNICAL_DRAFT.png')
            b=Image.open(tmp/'out'/'CP365_ARM_RAISE_TECHNICAL_DRAFT.png')
            self.assertEqual(a.size,b.size)
            self.assertNotEqual(a.tobytes(),b.tobytes())

    def test_unpainted_underlay_fails_and_never_writes_poses(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);fake_ora(tmp/'fake.ora',empty=m.REQUIRED['hidden_shoulder_bodice'])
            canon=dummy_canon(tmp)
            with mock.patch.object(m,'CANON_SHA',m.sha256(canon)):
                report=m.export(tmp/'fake.ora',canon,tmp/'out',min_size=(160,320))
            self.assertEqual(report['technical_status'],'BLOCKED')
            self.assertFalse((tmp/'out'/'CP365_IDLE_TECHNICAL_DRAFT.png').exists())

    def test_flat_reference_cannot_be_shipped_as_paint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);fake_ora(tmp/'fake.ora',visible_flat=True)
            canon=dummy_canon(tmp)
            with mock.patch.object(m,'CANON_SHA',m.sha256(canon)):
                report,_,_=m.assess(tmp/'fake.ora',canon,(160,320))
            self.assertEqual(report['technical_status'],'BLOCKED')
            self.assertTrue(report['flat_reference_visible'])

    def test_mismatched_canon_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);fake_ora(tmp/'fake.ora')
            with mock.patch.object(m,'CANON_SHA',m.sha256(dummy_canon(tmp))):
                (tmp/'wrong.png').write_bytes(b'not the approved reference')
                report,_,_=m.assess(tmp/'fake.ora',tmp/'wrong.png',(160,320))
            self.assertEqual(report['technical_status'],'BLOCKED')
            self.assertIn('CANON V2.1 SHA mismatch',report['errors'])

    def test_idempotent_rest_and_hidden_static_underpaint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp);fake_ora(tmp/'fake.ora')
            size,layers=m.read_ora(tmp/'fake.ora')
            rest=m.composite(layers,size,0,(80,110))
            second=m.composite(layers,size,0,(80,110))
            self.assertEqual(rest.tobytes(),second.tobytes())
            raised=m.composite(layers,size,-8,(80,110))
            self.assertNotEqual(rest.tobytes(),raised.tobytes())

if __name__=='__main__':unittest.main()
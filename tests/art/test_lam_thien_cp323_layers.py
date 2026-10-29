"""CP323: test real PNG decoding and true non-empty/placeholder behavior."""
import io
import importlib.util
import unittest
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location('cp323',ROOT/'tools/validate_lam_thien_cp323_layers.py')
cp323=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cp323)


def make_png(size, color=(240,180,140,255)):
    f=io.BytesIO()
    image=Image.new('RGBA',size,(0,0,0,0))
    # Put actual independent pixel content on each layer, not a fake PNG header.
    image.paste(color,(6,6,14,14))
    image.save(f,format='PNG')
    return f.getvalue()


def make_ora(size=(48,64), empty=False, guide_visible=False, duplicate=False,
             invalid_layer=None):
    image=Element('image', {'w':str(size[0]),'h':str(size[1])})
    stack=SubElement(image,'stack')
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as z:
        z.writestr('mimetype',b'image/openraster')
        for i,name in enumerate(cp323.LAYER_NAMES):
            path=f'data/layer_{i}.png'
            SubElement(stack,'layer',{'name':name+(' [EMPTY]' if empty else ''),
                                      'src':path,'visibility':'visible'})
            if invalid_layer == name:
                z.writestr(path,b'not png')
            elif empty:
                b=io.BytesIO();Image.new('RGBA',size,(0,0,0,0)).save(b,format='PNG');z.writestr(path,b.getvalue())
            else:
                col=(i*13%255,i*23%255,i*37%255,255)
                z.writestr(path,make_png(size,col if not duplicate else (20,40,60,255)))
        SubElement(stack,'layer',{'name':'GUIDE_REFERENCE_ONLY',
                                    'src':'data/guide.png',
                                    'visibility':'visible' if guide_visible else 'hidden'})
        z.writestr('data/guide.png',make_png(size))
        z.writestr('stack.xml',tostring(image))
    return stream.getvalue()


class CP323Tests(unittest.TestCase):
    def test_empty_alpha_template_blocked(self):
        result=cp323.audit_ora(make_ora(empty=True), label='empty.ora',canvas_size=(48,64),strict=True)
        self.assertTrue(result['structural_ok'])
        self.assertFalse(result['technical_ready'])
        self.assertFalse(result['passed'])
        self.assertTrue(any('body_underpaint' in x for x in result['production_blockers']))

    def test_actual_png_pixel_data(self):
        result=cp323.audit_ora(make_ora(),label='valid.ora',canvas_size=(48,64),strict=True)
        self.assertEqual(result['structural_errors'],[])
        self.assertTrue(result['technical_ready'])
        self.assertFalse(result['spine_ready'])
        self.assertEqual(result['layers']['hair_front']['active_alpha_pixels'],64)

    def test_guide_must_be_hidden(self):
        result=cp323.audit_ora(make_ora(guide_visible=True),label='guide.ora',canvas_size=(48,64),strict=True)
        self.assertFalse(result['passed'])
        self.assertTrue(any('Guide' in x for x in result['production_blockers']))

    def test_rejects_invalid_png_content(self):
        result=cp323.audit_ora(make_ora(invalid_layer='face_base'),label='broken.ora',canvas_size=(48,64))
        self.assertFalse(result['structural_ok'])
        self.assertTrue(any('unreadable PNG' in x for x in result['structural_errors']))

    def test_duplicate_layers_blocked(self):
        result=cp323.audit_ora(make_ora(duplicate=True),label='duplicate.ora',canvas_size=(48,64),strict=True)
        self.assertFalse(result['passed'])
        self.assertTrue(any('Identical' in x for x in result['production_blockers']))


if __name__=='__main__':unittest.main()
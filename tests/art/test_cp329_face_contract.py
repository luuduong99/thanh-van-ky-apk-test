"""CP329 GitHub tests: provenance and synthetic ORA QA, not binary asset approval."""
import importlib.util
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'tools/cp329/validate_cp329_intake.py'
spec=importlib.util.spec_from_file_location('cp329_intake',SCRIPT)
qa=importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
MANIFEST=ROOT/'docs/art/LAM_THIEN_CP329_FACE_INTAKE_MANIFEST.json'


def mock_ora(path,names,guide=False,guide_visible=False,corrupt_shape=False):
    src=Image.new('RGBA',(64,64) if corrupt_shape else (2048,2048))
    stream=io.BytesIO();src.save(stream,'PNG');empty=stream.getvalue()
    root=Element('image',{'w':'2048','h':'2048'})
    stack=SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype',b'image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,n in enumerate(names):
            p=f'data/{i}.png'
            SubElement(stack,'layer',{'name':n+' [EMPTY]','src':p,'visibility':'visible'})
            z.writestr(p,empty)
        if guide:
            p='data/guide.png'
            SubElement(stack,'layer',{'name':'GUIDE_CANON_V2_HIDDEN_NOT_ART','src':p,
                    'visibility':'visible' if guide_visible else 'hidden'})
            z.writestr(p,empty)
        z.writestr('stack.xml',tostring(root))
        z.writestr('mergedimage.png',empty)

class CP329GitHubContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(MANIFEST.read_text(encoding='utf-8'))

    def test_approved_source_hashes_unchanged(self):
        d=self.data
        self.assertEqual(d['approved_canon_sha256'],qa.CANON_SHA)
        self.assertEqual(d['approved_expression_sha256'],qa.EMOTION_SHA)
        self.assertEqual(d['approved_canon_visual_id'],qa.CANON_ID)
        self.assertEqual(d['approved_expression_profile_id'],qa.EMOTION_ID)

    def test_iris_guides_preserve_native_to_canvas_mapping(self):
        d=self.data
        self.assertEqual(d['native_face_size_px'],[230,114])
        self.assertEqual(d['guide_scale_factor'],8)
        self.assertEqual(d['working_canvas_px'],[2048,2048])
        for guide in d['iris_guides'].values():
            original=guide['native_bbox_xyxy'];work=guide['work_bbox_xyxy']
            expected=[104+8*original[0],568+8*original[1],
                      104+8*original[2],568+8*original[3]]
            self.assertEqual(work,expected)
            self.assertFalse(guide['measured_iris_only'])

    def test_explicitly_not_production_art_or_apk(self):
        d=self.data
        self.assertEqual(d['created_empty_oras'],6)
        self.assertEqual(d['created_painted_face_layers'],0)
        self.assertEqual(d['expressions'],list(qa.EMOTIONS))
        for key in ('production_face_master_ready','underpaint_artist_approved',
                    'independent_facial_art_ready','spine_rig_verified','android_apk_verified'):
            self.assertIs(d[key],False)

    def test_real_ora_shape_check_detects_bad_layer(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'sample.ora'
            mock_ora(path,qa.PARTS,corrupt_shape=True)
            report=qa.audit_ora(path,qa.PARTS)
            self.assertFalse(report['structural_ok'])
            self.assertTrue(any('expected RGBA 2048x2048' in x for x in report['problems']))

    def test_hidden_canon_guide_is_valid_but_visible_guide_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'face.ora'
            mock_ora(path,qa.MASTER,guide=True)
            self.assertTrue(qa.audit_ora(path,qa.MASTER,allow_guide=True)['structural_ok'])
            mock_ora(path,qa.MASTER,guide=True,guide_visible=True)
            self.assertFalse(qa.audit_ora(path,qa.MASTER,allow_guide=True)['structural_ok'])

    def test_transparent_layer_skeleton_must_not_be_called_painted(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'empty.ora'
            mock_ora(path,qa.PARTS)
            r=qa.audit_ora(path,qa.PARTS)
            self.assertEqual(r['nonempty_layers'],0)
            self.assertTrue(r['structural_ok'])

if __name__=='__main__':unittest.main()
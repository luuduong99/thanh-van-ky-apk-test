"""CP390 regression tests. Public CI intentionally skips private-asset-dependent tests."""
import hashlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
REPO_TOOL=HERE.parents[1]/'tools'/'art'/'cp390_boundary_skin_study.py' if len(HERE.parents)>1 else HERE/'cp390_boundary_skin_study.py'
MODULE=REPO_TOOL if REPO_TOOL.exists() else HERE/'cp390_boundary_skin_study.py'
spec=importlib.util.spec_from_file_location('cp390_boundary_skin_study',MODULE)
p=importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
CANON=Path(os.environ.get('TVK_CP390_CANON',str(HERE/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')))
ART=Path(os.environ.get('TVK_CP390_PREV_ART',str(HERE/'CP389_art')))
HAS_ASSETS=CANON.is_file() and all((ART/(k+'_DRAFT.png')).is_file() for k in ('LEFT_UNDERLAY','RIGHT_UNDERLAY','LEFT_CLOSED_EYELID','RIGHT_CLOSED_EYELID'))

class CP390Tests(unittest.TestCase):
    def test_01_static_canon_contract(self):
        self.assertEqual(p.SHA,'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a')
        self.assertEqual(p.WH,(168,197))
        self.assertEqual(p.CROP,(25,684,193,881))

    def test_02_static_release_contract(self):
        self.assertEqual(set(p.REGIONS),{'LEFT','RIGHT'})
        self.assertIn('NOT_APPROVED',p.PREFIX)
        # Source-controlled code must not write generated sprites into app assets.
        script=MODULE.read_text(encoding='utf8')
        self.assertNotIn('app/src/main/assets/',script)

    def test_03_wrong_canon_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as temp:
            temp=Path(temp)
            wrong=temp/'wrong.png';Image.new('RGBA',p.CANON_WH,'white').save(wrong)
            out=temp/'MUST_NOT_CREATE'
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):
                p.generate(wrong,temp,out)
            self.assertFalse(out.exists())

    @unittest.skipUnless(HAS_ASSETS,'private CANON and CP389 layer PNG not available in public CI')
    def test_04_actual_canon_sha(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),p.SHA)
        self.assertEqual(p.check_canon(CANON).size,p.WH)

    @unittest.skipUnless(HAS_ASSETS,'private CANON and CP389 layer PNG not available in public CI')
    def test_05_layers_are_independent_and_limited_to_eyes(self):
        src=p.check_canon(CANON)
        for s in ('LEFT','RIGHT'):
            old=Image.open(ART/f'{s}_UNDERLAY_DRAFT.png').convert('RGBA')
            skin,stats=p.refine_underlay(src,old,s)
            lash=p.lash_detail(s)
            p.assert_layer(skin,s);p.assert_layer(lash,s)
            self.assertGreater(skin.getchannel('A').getbbox()[2],0)
            self.assertGreater(lash.getchannel('A').getbbox()[2],0)
            self.assertGreater(stats['boundary_sample_count'],40)

    @unittest.skipUnless(HAS_ASSETS,'private CANON and CP389 layer PNG not available in public CI')
    def test_06_full_generation_source_exact_and_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'output'
            rep=p.generate(CANON,ART,out)
            self.assertTrue(rep['source_preserved'])
            self.assertEqual(rep['face_visual_qa'],'NOT_PASSED')
            self.assertEqual(rep['release']['status'],'blocked_pending_art')
            self.assertEqual(rep['release']['sprite_paths'],{})
            self.assertFalse(rep['release']['apk_ready'])
            self.assertEqual(rep['pixels_changed_outside_eye_roi'],0)
            self.assertEqual(rep['ora_layers'],10)

    @unittest.skipUnless(HAS_ASSETS,'private CANON and CP389 layer PNG not available in public CI')
    def test_07_open_canon_exact_in_ora(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'r';p.generate(CANON,ART,out)
            with zipfile.ZipFile(out/'CP390_TEN_LAYER_FACE_DRAFT_NOT_APPROVED.ora') as z:
                self.assertIsNone(z.testzip())
                self.assertEqual(z.read('mimetype'),b'image/openraster')
                doc=ET.fromstring(z.read('stack.xml'))
                layers=doc.find('stack').findall('layer')
                self.assertEqual(len(layers),10)
                self.assertEqual([x.get('visibility') for x in layers].count('visible'),1)
                exact=Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA')
                self.assertTrue(np.array_equal(np.asarray(exact),np.asarray(p.check_canon(CANON))))

    @unittest.skipUnless(HAS_ASSETS,'private CANON and CP389 layer PNG not available in public CI')
    def test_08_measured_seam_change_not_aesthetic_claim(self):
        with tempfile.TemporaryDirectory() as td:
            rep=p.generate(CANON,ART,Path(td)/'result')
            before=rep['skin_boundary_rgb_mae_to_open_eye_source_before']
            after=rep['skin_boundary_rgb_mae_to_open_eye_source_after']
            self.assertTrue(all(before[x]>after[x] for x in ('LEFT','RIGHT')))
            self.assertFalse(rep['closed_eye_is_artist_approved'])
            self.assertIn('not closed-eye ground truth',rep['skin_boundary_metric_limitations'])

    @unittest.skipUnless(HAS_ASSETS,'private CANON and CP389 layer PNG not available in public CI')
    def test_09_existing_layers_not_modified(self):
        before={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in ART.glob('*.png')}
        with tempfile.TemporaryDirectory() as td:p.generate(CANON,ART,Path(td)/'r')
        after={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in ART.glob('*.png')}
        self.assertEqual(before,after)

if __name__=='__main__':unittest.main()
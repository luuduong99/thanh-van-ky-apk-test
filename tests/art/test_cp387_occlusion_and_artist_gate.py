"""CP387 contract. Private exact CANON tests skip on public CI, not falsely pass."""
import hashlib, importlib.util, json, tempfile, unittest, zipfile
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent
SCRIPT=HERE/'cp387_occlusion_and_artist_gate.py'
if not SCRIPT.exists():SCRIPT=HERE.parents[1]/'tools'/'art'/'cp387_occlusion_and_artist_gate.py'
spec=importlib.util.spec_from_file_location('cp387',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
CANON=HERE/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
PRIOR=HERE/'source'/'OUTPUT'/'frames'/'CP386_FRAME_03_TECH_ONLY.png'
PRIVATE=CANON.exists() and PRIOR.exists()

class TestCP387(unittest.TestCase):
    def test_static_contract(self):
        self.assertEqual(g.SIZE,(168,197));self.assertEqual(g.BBOX,(25,684,193,881));self.assertEqual(len(g.POLYGONS),2)
    def test_no_art_release(self):
        src=SCRIPT.read_text(encoding='utf8')
        self.assertIn('NOT_PASSED',src);self.assertIn('blocked_pending_art',src);self.assertIn('REJECTED HIDDEN',src)
    def test_wrong_source_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'wrong.png';Image.new('RGBA',(941,1672),'white').save(f)
            with self.assertRaisesRegex(ValueError,'CANON_SHA_MISMATCH'):g.run(f, f,Path(td)/'should_not_exist')
            self.assertFalse((Path(td)/'should_not_exist').exists())
    @unittest.skipUnless(PRIVATE,'Private user-approved CANON & prior CP386 are not on public runner')
    def test_approved_sha(self):
        self.assertEqual(hashlib.sha256(CANON.read_bytes()).hexdigest(),g.SHA)
    @unittest.skipUnless(PRIVATE,'Private source missing')
    def test_candidates_stay_inside_eye_masks(self):
        source=g.load_approved(CANON)
        opts,mask,selection=g.candidates(source)
        self.assertEqual(len(opts),3)
        for image in opts.values():
            self.assertTrue(np.array_equal(np.asarray(image)[~selection],np.asarray(source)[~selection]))
    @unittest.skipUnless(PRIVATE,'Private source missing')
    def test_only_reversible_rejected_options(self):
        with tempfile.TemporaryDirectory() as td:
            report=g.run(CANON,PRIOR,td); self.assertFalse(report['new_eyelid_art_approved'])
            self.assertEqual(report['visual_qa'],'NOT_PASSED')
            self.assertEqual(report['changed_pixels_outside_eye_ROI'],0)
            self.assertEqual(len(report['three_candidates_evaluated']),3)
    @unittest.skipUnless(PRIVATE,'Private source missing')
    def test_ora_exact_visible_and_crc(self):
        with tempfile.TemporaryDirectory() as td:
            r=g.run(CANON,PRIOR,td)
            path=Path(td)/'art'/'CP387_SEVEN_LAYER_EYELID_REVIEW_NOT_ART.ora'
            with zipfile.ZipFile(path) as z:
                self.assertIsNone(z.testzip());self.assertEqual(len([n for n in z.namelist() if n.startswith('data/layer_')]),7)
                import xml.etree.ElementTree as ET
                stack=ET.fromstring(z.read('stack.xml')).find('stack')
                self.assertEqual(sum(x.get('visibility')=='visible' for x in stack),1)
                import io
                merged=Image.open(io.BytesIO(z.read('mergedimage.png')))
                self.assertTrue(np.array_equal(np.asarray(merged),np.asarray(g.load_approved(CANON))))
    @unittest.skipUnless(PRIVATE,'Private source missing')
    def test_export_source_is_byte_exact(self):
        with tempfile.TemporaryDirectory() as td:
            r=g.run(CANON,PRIOR,td)
            self.assertTrue(r['original_bytes_preserved'])
            self.assertEqual(Path(td,'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes(),CANON.read_bytes())
    @unittest.skipUnless(PRIVATE,'Private source missing')
    def test_qa_source_and_report(self):
        with tempfile.TemporaryDirectory() as td:
            g.run(CANON,PRIOR,td)
            report=json.loads(Path(td,'CP387_REPORT.json').read_text(encoding='utf8'))
            self.assertEqual(report['release']['sprite_paths'],{})
            self.assertFalse(report['release']['apk_ready'])
            self.assertTrue(Path(td,'qa/CP387_CANON_VS_REJECTED_EYELID_CANDIDATES.png').exists())

if __name__=='__main__':unittest.main()
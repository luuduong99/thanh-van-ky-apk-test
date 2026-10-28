"""CP317 image reconstruction contract tests. Uses synthetic gradient, never real CP313."""
import io
import sys
import tempfile
from pathlib import Path
import zipfile
import unittest
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'art'))
import reconstruct_back_ora as cp317
import source_inventory as inventory

class ProxyReconstructionTests(unittest.TestCase):
    def test_proxy_static_composite_exact_and_original_detection_rejects(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            height,width=656,207
            xx=np.tile(np.arange(width,dtype=np.uint8),(height,1))
            yy=np.tile(np.arange(height,dtype=np.int32).astype('uint8')[:,None],(1,width))
            rgb=np.stack((xx,yy,xx//2 + yy//2),axis=2)
            src=root/'reference_flat.png'
            Image.fromarray(rgb,'RGB').save(src)
            path=root/'CP317_PROXY_NOT_ORIGINAL.ora'
            report=cp317.create(src,path)
            self.assertEqual(report['static_composite_drift_pixels'],0)
            self.assertEqual(report['layer_count'],10)
            self.assertFalse(report['ready_to_replace_CP313'])
            with zipfile.ZipFile(path) as z:
                self.assertIn('data/CP317_PROVENANCE.json',z.namelist())
                merged=Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGB')
                self.assertTrue(np.array_equal(np.asarray(merged),rgb))
                names=[x for x in z.namelist() if x.startswith('data/layer_')]
                self.assertEqual(len(names),10)
                for name in names:
                    im=Image.open(io.BytesIO(z.read(name))).convert('RGBA')
                    self.assertIsNotNone(im.getchannel('A').getbbox(),name)
            inv=inventory.scan([path])
            self.assertEqual(inv['candidate_count'],0)
            self.assertIn('not original CP313',' '.join(inv['ora_candidates'][0]['errors']))

if __name__=='__main__':unittest.main()
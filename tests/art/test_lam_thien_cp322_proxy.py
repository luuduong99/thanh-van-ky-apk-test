"""CP322 tests use synthetic RGBA PNGs and a pure-data manifest, not art bytes."""
import hashlib
import importlib.util
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/validate_lam_thien_cp322_proxy.py"
SPEC = importlib.util.spec_from_file_location("cp322", MODULE)
cp322 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cp322)


def chunk(kind, payload):
    return (struct.pack('>I', len(payload)) + kind + payload +
            struct.pack('>I', zlib.crc32(kind + payload) & 0xFFFFFFFF))


def make_png(width=2, height=2, alpha=255):
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    pixels = bytes([0] + [100, 160, 220, alpha] * width) * height
    return cp322.SIGNATURE + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b'')


class CP322Tests(unittest.TestCase):
    def test_valid_png_decodes_real_alpha(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'a.png'
            path.write_bytes(make_png(2, 3, 255))
            self.assertEqual(cp322.png_alpha_coverage(path), (2, 3, 6))
            path.write_bytes(make_png(2, 3, 0))
            self.assertEqual(cp322.png_alpha_coverage(path), (2, 3, 0))

    def test_invalid_crc_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'bad.png'
            raw = bytearray(make_png())
            raw[-8] ^= 1
            path.write_bytes(raw)
            with self.assertRaises(ValueError):
                cp322.png_alpha_coverage(path)

    def test_manifest_cannot_be_canon(self):
        manifest = json.loads((ROOT/'docs/art/LAM_THIEN_CP322_ALPHA_TRIAL_MANIFEST.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['visual_approval'], 'NOT_APPROVED')
        self.assertTrue(manifest['new_visual_is_not_canon'])
        self.assertEqual(manifest['canonical_reference_id'], cp322.CANON)
        self.assertEqual(manifest['canonical_reference_sha256'], cp322.CANON_SHA)
        self.assertEqual(len(manifest['files']), 5)

    def test_strict_gate_rejects_unapproved_alpha_proxies(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            rows = []
            for view in sorted(cp322.VIEWS):
                name = view + '_draft_RGBA_PROXY.png'
                source = make_png(2, 2, 255)
                (folder/name).write_bytes(source)
                rows.append({'view_id':view, 'file':name, 'native_px':[2,2],
                             'alpha_occupied_pixels':4, 'alpha_coverage_pct':100,
                             'sha256':hashlib.sha256(source).hexdigest()})
            manifest = {'visual_approval':'NOT_APPROVED','new_visual_is_not_canon':True,
                        'canonical_reference_id':cp322.CANON,'canonical_reference_sha256':cp322.CANON_SHA,
                        'files':rows}
            (folder/'manifest.json').write_text(json.dumps(manifest))
            self.assertTrue(cp322.audit(folder, strict=True))
            self.assertIn('production', ' '.join(cp322.audit(folder, strict=True)))

if __name__=='__main__':
    unittest.main()
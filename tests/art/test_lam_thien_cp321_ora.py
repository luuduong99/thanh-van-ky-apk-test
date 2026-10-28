"""CP321: structural OpenRaster checks and strict art-readiness guard."""
import importlib.util
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "cp321", ROOT / "tools/validate_lam_thien_cp321_ora.py"
)
cp321 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cp321)


def make_ora(path, bad_size=False):
    image = Element("image", {"w": "2048", "h": "3072"})
    stack = SubElement(image, "stack")
    names = sorted(cp321.REQUIRED)
    names.append("GUIDE_REFERENCE_ONLY_hide_before_export")
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", b"image/openraster")
        for i, name in enumerate(names):
            src = f"data/layer_{i:02d}.png"
            SubElement(stack, "layer", {
                "name": name + (" [EMPTY]" if i < 15 else ""),
                "src": src,
                "visibility": "visible",
            })
            # Synthetic PNG header only: enough to exercise the file
            # signature, canvas-size and RGBA guards; not a real production asset.
            width = 1 if bad_size else 2048
            header = (
                bytes([137, 80, 78, 71, 13, 10, 26, 10]) +
                struct.pack(">I", 13) + b"IHDR" +
                struct.pack(">II", width, 3072) +
                bytes([8, 6, 0, 0, 0]) +
                bytes([0, 0, 0, 0])
            )
            archive.writestr(src, header)
        archive.writestr("stack.xml", tostring(image, encoding="utf-8"))


class CP321AuditTests(unittest.TestCase):
    def test_missing_file_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            errors, pending = cp321.audit(Path(temp) / "missing.ora")
            self.assertTrue(any("Missing ORA" in x for x in errors))
            self.assertEqual(pending, [])

    def test_non_ora_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "fake.ora"
            file.write_bytes(b"not an ORA")
            errors, _ = cp321.audit(file)
            self.assertTrue(errors)

    def test_scaffold_passes_structure_but_fails_art_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "mock.ora"
            make_ora(file)
            errors, pending = cp321.audit(file)
            self.assertEqual(errors, [])
            self.assertTrue(any("EMPTY" in x for x in pending))
            strict_errors, _ = cp321.audit(file, strict=True)
            self.assertTrue(strict_errors)

    def test_rejects_incorrect_layer_dimensions(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "wrong_size.ora"
            make_ora(file, bad_size=True)
            errors, _ = cp321.audit(file)
            self.assertTrue(any("dimensions" in x for x in errors))


if __name__ == "__main__":
    unittest.main()

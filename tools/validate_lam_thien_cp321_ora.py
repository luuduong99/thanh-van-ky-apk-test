#!/usr/bin/env python3
"""Check CP321 OpenRaster layer templates without claiming rig or art readiness."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

REQUIRED = {
    'hair_front', 'eye_left', 'eye_right', 'mouth', 'face_base',
    'ornaments', 'sleeve_left', 'sleeve_right', 'costume_outer',
    'damage_overlay', 'skirt_front', 'costume_inner',
    'body_underpaint', 'skirt_back', 'hair_back',
}


def audit(path, strict=False):
    errors, pending = [], []
    path = Path(path)
    if not path.is_file():
        return [f'Missing ORA: {path}'], []
    try:
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:
                errors.append('ZIP CRC failed')
            if z.read('mimetype') != b'image/openraster':
                errors.append('Not an OpenRaster file')
            root = ET.fromstring(z.read('stack.xml'))
            if (root.attrib.get('w'), root.attrib.get('h')) != ('2048', '3072'):
                errors.append('Unexpected canvas dimensions')
            items = root.findall('./stack/layer')
            actual = [e for e in items if not e.attrib.get('name', '').startswith('GUIDE_REFERENCE_ONLY')]
            guide = [e for e in items if e not in actual]
            names = [e.attrib['name'].removesuffix(' [EMPTY]') for e in actual]
            if len(items) != 16 or len(actual) != 15 or set(names) != REQUIRED or len(set(names)) != 15:
                errors.append('Incorrect number or names of layers')
            if len(guide) != 1:
                errors.append('Exactly one reference-only guide is required')
            hashes = []
            for layer in items:
                src = layer.attrib.get('src')
                if not src or src not in z.namelist() or not src.startswith('data/'):
                    errors.append('Invalid layer source')
                    continue
                raw = z.read(src)
                if not raw.startswith(bytes([137, 80, 78, 71, 13, 10, 26, 10])):
                    errors.append('Layer is not PNG')
                if layer in actual:
                    hashes.append(hashlib.sha256(raw).hexdigest())
            if len(set(hashes)) == 1 and len(hashes) == 15:
                pending.append('All art layers identical transparent templates (no segmented artwork)')
            if any('[EMPTY]' in e.attrib.get('name','') for e in actual):
                pending.append('Character layer names still marked EMPTY')
            if guide and guide[0].attrib.get('visibility', 'visible') != 'hidden':
                pending.append('Reference-only guide visible; hide before production export')
    except (KeyError, zipfile.BadZipFile, ET.ParseError, OSError) as exc:
        errors.append(f'Unreadable ORA package: {exc}')
    if strict:
        errors.extend(pending)
    return errors, pending


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('ora', nargs='+', type=Path)
    p.add_argument('--strict', action='store_true')
    args = p.parse_args()
    outcomes = []
    for ora in args.ora:
        errors, pending = audit(ora, args.strict)
        outcomes.append({'path': str(ora), 'passed': not errors, 'errors': errors, 'pending': pending})
    print(json.dumps(outcomes, indent=2, ensure_ascii=False))
    return 1 if any(x['errors'] for x in outcomes) else 0


if __name__ == '__main__':
    raise SystemExit(main())

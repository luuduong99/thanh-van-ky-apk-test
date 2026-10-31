#!/usr/bin/env python3
"""CP323: inspect actual pixels in OpenRaster files for Lâm Thiển.

Checks technical integrity; NEVER certifies that art matches CANON V2, that
underpaint is artistically correct, or that Spine/runtime/Android is finished.

Usage:
  python tools/validate_lam_thien_cp323_layers.py FRONT.ora BACK.ora
  python tools/validate_lam_thien_cp323_layers.py --strict FRONT.ora BACK.ora
  python tools/validate_lam_thien_cp323_layers.py --zip path/to/CP321_templates.zip
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

try:
    from PIL import Image, UnidentifiedImageError
except ImportError as exc:
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc

LAYER_NAMES = (
    'hair_front', 'eye_left', 'eye_right', 'mouth', 'face_base',
    'ornaments', 'sleeve_left', 'sleeve_right', 'costume_outer',
    'damage_overlay', 'skirt_front', 'costume_inner',
    'body_underpaint', 'skirt_back', 'hair_back'
)
ALLOWED_EMPTY = {'damage_overlay'}  # Intact wardrobe 100% can have no damage.
CANVAS_SIZE = (2048, 3072)
SOURCE_CANON_ID = 'LT_CANON_BODY_REF_2026-10-28_V2'


def audit_ora(ora_bytes: bytes, *, label: str, canvas_size=CANVAS_SIZE,
              strict=False, threshold=16, minimum_pixels=32):
    """Audit one OpenRaster byte blob, report both defects and blockers."""
    result = {'file': label, 'structural_errors': [], 'production_blockers': [],
              'layers': {}, 'technical_ready': False,
              'human_art_review': 'NOT_ASSESSED', 'spine_ready': False}
    errors = result['structural_errors']
    blockers = result['production_blockers']
    try:
        with zipfile.ZipFile(io.BytesIO(ora_bytes)) as z:
            bad = z.testzip()
            if bad is not None:
                errors.append('ZIP CRC failed at ' + bad)
            if z.read('mimetype') != b'image/openraster':
                errors.append('Invalid OpenRaster mimetype')
            root = ET.fromstring(z.read('stack.xml'))
            dimensions = (int(root.attrib['w']), int(root.attrib['h']))
            result['canvas_px'] = list(dimensions)
            if dimensions != tuple(canvas_size):
                errors.append(f'Canvas {dimensions} != required {canvas_size}')
            entries = root.findall('./stack/layer')
            labels = [e.attrib.get('name', '') for e in entries]
            art = [e for e in entries if not e.attrib.get('name','').startswith('GUIDE_REFERENCE_ONLY')]
            guides = [e for e in entries if e not in art]
            art_names = [e.attrib.get('name','').removesuffix(' [EMPTY]') for e in art]
            if len(art) != len(LAYER_NAMES) or set(art_names) != set(LAYER_NAMES) or len(set(art_names)) != len(LAYER_NAMES):
                errors.append('Expected exactly 15 distinct named art slots')
            if len(guides) != 1:
                errors.append('Expected exactly one reference guide')
            if any('[EMPTY]' in lab for lab in labels):
                blockers.append('Layer names still have [EMPTY] placeholders')
            if guides and guides[0].attrib.get('visibility', 'visible') != 'hidden':
                blockers.append('Guide reference visible; it must be hidden for game export')
            seen = set()
            hashes_by_name = {}
            for element in entries:
                name = element.attrib.get('name', '').removesuffix(' [EMPTY]')
                src = element.attrib.get('src', '')
                rel = PurePosixPath(src)
                if (not src.startswith('data/') or rel.is_absolute() or '..' in rel.parts
                    or src in seen or src not in z.namelist() or not src.endswith('.png')):
                    errors.append('Invalid, duplicated, or unsafe image source for '+name)
                    continue
                seen.add(src)
                raw = z.read(src)
                try:
                    with Image.open(io.BytesIO(raw)) as image:
                        if image.format != 'PNG' or image.mode != 'RGBA':
                            errors.append(f'{name}: must use genuine RGBA PNG')
                            continue
                        if image.size != dimensions:
                            errors.append(f'{name}: native size {image.size} != canvas {dimensions}')
                            continue
                        image.load()  # Forces real IDAT decode and catches invalid PNG.
                        h = image.getchannel('A').histogram()
                        active = int(sum(h[threshold+1:]))
                        bbox = image.getchannel('A').getbbox()
                        opaque = int(sum(h[250:]))
                        result['layers'][name] = {'active_alpha_pixels':active,
                                                  'alpha_nonzero_bbox':list(bbox) if bbox else None,
                                                  'opaque_pixels': opaque,
                                                  'sha256':hashlib.sha256(raw).hexdigest(),
                                                  'reference_only':element in guides}
                        if element in art:
                            hashes_by_name[name] = hashlib.sha256(raw).hexdigest()
                            if name not in ALLOWED_EMPTY and active < minimum_pixels:
                                blockers.append(f'{name}: {active} visible pixels (<{minimum_pixels})')
                except (UnidentifiedImageError, OSError, ValueError, SyntaxError) as exc:
                    errors.append(f'{name}: unreadable PNG IDAT ({type(exc).__name__})')
            # Duplicate art often indicates a flattened silhouette copied into every slot;
            # report it for manual review rather than claiming it is a valid separation.
            seen_hashes={}
            for name,hsh in hashes_by_name.items():
                if name in ALLOWED_EMPTY: continue
                seen_hashes.setdefault(hsh, []).append(name)
            for group in seen_hashes.values():
                if len(group)>1:
                    blockers.append('Identical PNG bytes across different art layers: '+','.join(group))
    except (KeyError, zipfile.BadZipFile, ET.ParseError, ValueError, OSError) as exc:
        errors.append('Unreadable ORA: '+str(exc))

    result['structural_ok'] = not errors
    result['technical_ready'] = not errors and not blockers
    result['passed'] = (not errors and not blockers) if strict else (not errors)
    result['production_gate'] = 'PASS_TECHNICAL_ONLY' if result['technical_ready'] else 'BLOCKED'
    return result


def audit_zip(path: Path, strict=False):
    results=[]
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if name.endswith('.ora'):
                results.append(audit_ora(archive.read(name), label=name, strict=strict))
    if not results:
        raise ValueError('No ORA files in ZIP')
    return results


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('oras', nargs='*', type=Path)
    p.add_argument('--zip', type=Path, help='Archive with ORA files to inspect')
    p.add_argument('--strict', action='store_true', help='Fail if any production art blockers')
    p.add_argument('--output', type=Path, help='Write JSON report for QA handoff')
    args=p.parse_args(argv)
    if not args.oras and not args.zip:
        p.error('Pass ORA files or --zip archive')
    items=[]
    if args.zip:
        items.extend(audit_zip(args.zip, strict=args.strict))
    for f in args.oras:
        items.append(audit_ora(f.read_bytes(),label=str(f),strict=args.strict))
    output={'checkpoint':'CP323','canon_reference_id':SOURCE_CANON_ID,
            'gate':'TECHNICAL_ONLY_NOT_ART_APPROVAL',
            'items':items,'passed':all(x['passed'] for x in items)}
    serialized=json.dumps(output,ensure_ascii=False,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized+'\n',encoding='utf-8')
    print(serialized)
    return 0 if output['passed'] else 1


if __name__=='__main__':
    sys.exit(main())
#!/usr/bin/env python3
"""CP316 read-only source recovery: find *structural* ORA candidates in files/archives.

No artwork is modified. A matching structure is NOT proof of authenticity.
Usage:
  python tools/art/source_inventory.py /mnt/data --expect-layers 10 --out reports/cp316_inventory
  python tools/art/source_inventory.py export.zip --expect-layers 10 --require-candidate
"""
import argparse
from collections import Counter
from hashlib import sha256
import io
import json
from pathlib import Path
import sys
import zipfile
from xml.etree import ElementTree as ET

from PIL import Image, UnidentifiedImageError

MAX_ARCHIVE_ENTRY = 256 * 1024 * 1024  # 256 MB max source payload
MAX_MEMBER_COUNT = 2000
MAX_FILE_PIXELS = 120_000_000
MAX_DEPTH = 3


def _sha(data):
    return sha256(data).hexdigest()


def _read_bounded(z, name):
    info = z.getinfo(name)
    if info.file_size > MAX_ARCHIVE_ENTRY:
        raise ValueError(f"member too large: {info.file_size}")
    with z.open(name) as f:
        data = f.read(MAX_ARCHIVE_ENTRY + 1)
    if len(data) > MAX_ARCHIVE_ENTRY:
        raise ValueError('member exceeds safe read budget')
    return data


def analyze_ora(ora, locator, digest, expect_layers, min_nonempty):
    names = ora.namelist()
    errors = []
    warnings = []
    if len(names) > MAX_MEMBER_COUNT:
        errors.append('too many entries')
    dupe = [name for name, freq in Counter(names).items() if freq > 1]
    if dupe:
        errors.append('duplicate ZIP members: '+', '.join(dupe[:5]))
    if 'stack.xml' not in names:
        errors.append('missing stack.xml')
        return dict(locator=locator, sha256=digest, errors=errors, warnings=warnings,
                    status='INVALID_ORA')
    try:
        root = ET.fromstring(_read_bounded(ora, 'stack.xml'))
        w, h = int(root.attrib['w']), int(root.attrib['h'])
        if w <= 0 or h <= 0 or w * h > MAX_FILE_PIXELS:
            raise ValueError('out-of-range canvas')
        nodes = list(root.iter('layer'))
        count = len(nodes)
        if count != expect_layers:
            errors.append(f'expected {expect_layers} layers; found {count}')
        nonempty = 0
        layer_info = []
        for node in nodes:
            name = node.attrib.get('name', '')
            src = node.attrib.get('src', '')
            item = {'name': name, 'src': src, 'nonempty_alpha': False}
            if src not in names or not src:
                errors.append(f'missing layer data: {name} / {src}')
            else:
                with Image.open(io.BytesIO(_read_bounded(ora, src))) as im:
                    if im.width * im.height > MAX_FILE_PIXELS:
                        raise ValueError('over-large layer pixel count')
                    im = im.convert('RGBA')
                    opaque = im.getchannel('A').getbbox() is not None
                    item['nonempty_alpha'] = bool(opaque)
                    nonempty += int(opaque)
            layer_info.append(item)
        if nonempty < min_nonempty:
            errors.append(f'only {nonempty} nonempty layers (< {min_nonempty})')
        placeholders = [l['name'] for l in layer_info if any(word in l['name'].lower() for word in
                         ('placeholder', 'synthetic', 'dummy', 'test_layer'))]
        if placeholders:
            errors.append(f'placeholder-like layer names: {placeholders}')
        if 'mergedimage.png' not in names:
            warnings.append('missing mergedimage.png — required for composite review')
        if root.find('.//stack/stack') is not None:
            warnings.append('nested stacks; manually verify group transforms and blending')
        status = 'STRUCTURAL_CANDIDATE_NEEDS_ART_REVIEW' if not errors else 'NOT_A_VALID_CANDIDATE'
        return {'locator': locator, 'sha256': digest, 'canvas': [w,h],
                'layer_count': count, 'nonempty_layer_count': nonempty,
                'layers': layer_info, 'warnings': warnings, 'errors': errors, 'status': status}
    except (ET.ParseError, ValueError, KeyError, OSError, UnidentifiedImageError, zipfile.BadZipFile) as e:
        errors.append(f'parse/decode failure: {str(e)[:200]}')
        return {'locator': locator, 'sha256': digest,
                'warnings': warnings, 'errors': errors, 'status': 'INVALID_ORA'}


def inspect_zip(z, locator, digest, *, expect_layers=10, min_nonempty=6, depth=0):
    if depth > MAX_DEPTH:
        return [], [f'{locator}: maximum archive depth reached']
    results, warnings = [], []
    names = z.namelist()
    if len(names) > MAX_MEMBER_COUNT:
        return [], [f'{locator}: archive has too many members']
    if 'stack.xml' in names:
        results.append(analyze_ora(z, locator, digest, expect_layers, min_nonempty))
        return results, warnings
    for name in names:
        if not name.lower().endswith(('.ora', '.zip')) or name.startswith('__MACOSX/'):
            continue
        try:
            b = _read_bounded(z, name)
            with zipfile.ZipFile(io.BytesIO(b)) as child:
                more, notices = inspect_zip(child, locator+'!'+name, _sha(b),
                            expect_layers=expect_layers, min_nonempty=min_nonempty, depth=depth+1)
                results += more
                warnings += notices
        except (zipfile.BadZipFile, KeyError, OSError, ValueError) as e:
            warnings.append(f'{locator}!{name}: {str(e)[:160]}')
    return results, warnings


def scan(paths, expect_layers=10, min_nonempty=6):
    seen = set()
    report = {'examined_archives': [], 'ora_candidates': [], 'warnings': []}
    for path in paths:
        p = Path(path)
        files = sorted(p.rglob('*')) if p.is_dir() else [p]
        for candidate in files:
            if not candidate.is_file() or candidate.suffix.lower() not in ('.ora', '.zip'):
                continue
            if candidate.resolve() in seen:
                continue
            seen.add(candidate.resolve())
            if candidate.stat().st_size > MAX_ARCHIVE_ENTRY:
                report['warnings'].append(f'{candidate}: file exceeds safe read budget; skipped')
                continue
            try:
                b = candidate.read_bytes()
                digest = _sha(b)
                with zipfile.ZipFile(io.BytesIO(b)) as z:
                    results, warnings = inspect_zip(z, str(candidate), digest,
                                        expect_layers=expect_layers, min_nonempty=min_nonempty)
                report['examined_archives'].append({'path': str(candidate), 'sha256': digest})
                report['ora_candidates'] += results
                report['warnings'] += warnings
            except (zipfile.BadZipFile, OSError) as e:
                report['warnings'].append(f'{candidate}: {str(e)[:160]}')
    report['candidate_count'] = sum(1 for x in report['ora_candidates'] if
                           x['status'] == 'STRUCTURAL_CANDIDATE_NEEDS_ART_REVIEW')
    report['status'] = 'CANDIDATES_REQUIRE_MANUAL_VERIFICATION' if report['candidate_count'] else 'NO_QUALIFYING_ORA_SOURCE'
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('paths', nargs='+', help='Folder(s), ORA or ZIP files to scan read-only')
    ap.add_argument('--expect-layers', type=int, default=10)
    ap.add_argument('--min-nonempty', type=int, default=6)
    ap.add_argument('--out', default='reports/cp316_source_inventory')
    ap.add_argument('--require-candidate', action='store_true', help='nonzero exit if no qualifying candidate')
    args = ap.parse_args()
    if not (1 <= args.min_nonempty <= args.expect_layers <= 200):
        ap.error('1 <= --min-nonempty <= --expect-layers <= 200 required')
    result = scan(args.paths, args.expect_layers, args.min_nonempty)
    dest = Path(args.out)
    dest.mkdir(parents=True, exist_ok=True)
    (dest/'inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'archive_count': len(result['examined_archives']),
                      'ora_candidates': len(result['ora_candidates']), 'qualifying': result['candidate_count'],
                      'inventory': str(dest/'inventory.json')}, ensure_ascii=False))
    if args.require_candidate and not result['candidate_count']:
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
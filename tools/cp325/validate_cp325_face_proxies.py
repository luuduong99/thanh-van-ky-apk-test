#!/usr/bin/env python3
"""CP325 reference pixel-patch ORA inspector; this deliberately NEVER certifies Spine art.

Usage: python validate_cp325_face_proxies.py <folder> [--strict]
The folder must contain manifest.json and each named *.ora. Requires Pillow.
"""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image

EXPECTED=['shy','angry','pain','embarrassed','alluring']
REGIONS=['brow_image_left','brow_image_right','eye_image_left','eye_image_right','mouth','blush_image_left','blush_image_right']
CANON='LT_CANON_BODY_REF_2026-10-28_V2'
APPROVED='LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED'


def sha(raw): return hashlib.sha256(raw).hexdigest()


def audit_ora(ora, record):
    errors=[]
    try:
        with zipfile.ZipFile(ora) as z:
            if z.testzip() is not None:
                errors.append('ORA CRC failed')
            if z.read('mimetype') != b'image/openraster':
                errors.append('Wrong ORA mimetype')
            xml=ET.fromstring(z.read('stack.xml'))
            w,h=record['native_size_px']
            if [int(xml.attrib['w']),int(xml.attrib['h'])]!=[w,h]:
                errors.append('Unexpected ORA canvas size')
            layers=xml.findall('./stack/layer')
            if len(layers)!=8: errors.append('Expected exactly seven regions + hidden guide')
            refs=[x for x in layers if x.attrib.get('name','').startswith('REFERENCE_FLAT_')]
            if len(refs)!=1 or refs[0].get('visibility')!='hidden':
                errors.append('Reference guide must exist and remain hidden')
            pixel_layers=[x for x in layers if '[PROXY_PIXEL_PATCH]' in x.attrib.get('name','')]
            if sorted(x.get('name').split(' [')[0] for x in pixel_layers)!=sorted(REGIONS):
                errors.append('Region layer names do not match required list')
            if not refs:
                return errors
            flat=Image.open(io.BytesIO(z.read(refs[0].get('src')))).convert('RGB')
            if flat.size!=(w,h): errors.append('Reference source dimensions incorrect')
            for r in record['regions']:
                key=r['name']
                match=[x for x in pixel_layers if x.get('name').startswith(key+' [')]
                if len(match)!=1:
                    errors.append('Missing or repeated region '+key);continue
                raw=z.read(match[0].get('src'))
                if sha(raw)!=r['sha256']:
                    errors.append('Patch SHA mismatch '+key)
                patch=Image.open(io.BytesIO(raw)).convert('RGBA')
                if patch.size!=(w,h): errors.append('Patch size differs '+key)
                alpha=patch.getchannel('A')
                if not alpha.getbbox():
                    errors.append('Region empty '+key)
                if sum(a>0 for a in alpha.tobytes())!=r['alpha_nonzero']:
                    errors.append('Alpha pixel count mismatch '+key)
                bounds=alpha.getbbox()
                desired=r['source_bbox_xyxy']
                if bounds and not (desired[0]<=bounds[0] and desired[1]<=bounds[1] and bounds[2]<=desired[2] and bounds[3]<=desired[3]):
                    errors.append('Mask spills outside region bbox '+key)
                # The patch is copied from the approved portrait, not painted.
                # RGB values under nonzero alpha must be the original reference.
                if any(a>0 and patch.getpixel((x,y))[:3]!=flat.getpixel((x,y))
                       for y in range(h) for x,a in enumerate(alpha.crop((0,y,w,y+1)).tobytes())):
                    errors.append('Reference RGB pixel modified in patch '+key)
            if 'tvk_cp325.json' not in z.namelist():
                errors.append('Missing embedded status')
            else:
                info=json.loads(z.read('tvk_cp325.json'))
                if info.get('status')!='NOT_SPINE_READY_REFERENCE_PIXEL_PATCH' or info.get('artwork_from_canon_v2') is not False:
                    errors.append('Incorrect claims about art readiness')
    except (OSError, KeyError, ValueError, ET.ParseError, zipfile.BadZipFile) as exc:
        errors.append(f'Invalid ORA file: {exc}')
    return errors


def audit(root,strict=False):
    root=Path(root); issues=[]
    try:
        manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
        items=manifest['items']
        if [it['emotion_id'] for it in items]!=EXPECTED or len(items)!=5:
            issues.append('Expected exact approved five-expression sequence')
        if manifest.get('canonical_body_visual_id')!=CANON or manifest.get('approved_expression_profile_id')!=APPROVED:
            issues.append('CANON V2 or approved expression source changed')
        if manifest.get('spine_ready') is not False or manifest.get('asset_registration_allowed') is not False:
            issues.append('Reference proxies must NOT claim Spine/game readiness')
        for item in items:
            ora=root/item['ora_filename']
            if not ora.exists():
                issues.append('Missing ORA '+str(ora));continue
            if sha(ora.read_bytes())!=item['ora_sha256']:
                issues.append('ORA SHA mismatch '+ora.name)
            issues.extend(f"{item['emotion_id']}: {e}" for e in audit_ora(ora,item))
    except (KeyError, OSError, json.JSONDecodeError, ValueError) as exc:
        issues.append('Manifest could not be read: '+str(exc))
    # Strict has a mandatory blocker: cropped poster pixels are NOT regenerated
    # production assets. This cannot be changed by renaming status fields.
    if strict: issues.append('CP325 reference region patches are not CANON V2 independent face sprite layers')
    return issues


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder',type=Path)
    p.add_argument('--strict',action='store_true')
    args=p.parse_args()
    issues=audit(args.folder,args.strict)
    print(json.dumps({'checkpoint':'CP325','passed':not issues,'errors':issues,
      'production_ready':False,'strict':args.strict},ensure_ascii=False,indent=2))
    return 1 if issues else 0


if __name__=='__main__':
    raise SystemExit(main())
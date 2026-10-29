#!/usr/bin/env python3
"""CP326 independently-drawn facial layers audit. Not a production art approval."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image, ImageChops

EMOTIONS=['shy','angry','pain','embarrassed','alluring']
PARTS=['blush_image_left','blush_image_right','eye_image_left','eye_image_right','brow_image_left','brow_image_right','mouth']
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXPR_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
CANON_ID='LT_CANON_BODY_REF_2026-10-28_V2'


def audit(directory,strict=False,canon=None):
    directory=Path(directory)
    errors=[];pending=[]
    try:
        manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    except (OSError,ValueError) as exc:return [f'Cannot read manifest: {exc}'],[]
    if manifest.get('canonical_body_visual_id')!=CANON_ID or manifest.get('canonical_body_sha256')!=CANON_SHA:
        errors.append('Approved body V2 source identity mismatch')
    if manifest.get('approved_five_expression_sheet_sha256')!=EXPR_SHA:
        errors.append('Five-expression approved visual reference SHA mismatch')
    if manifest.get('expression_ids')!=EMOTIONS:
        errors.append('Must preserve five distinct approved emotion identifiers')
    if manifest.get('native_source_size_px')!=[230,114] or manifest.get('rendered_canvas_px')!=[920,456]:
        errors.append('Misrepresented native face resolution / working canvas')
    if len(manifest.get('items',[]))!=5:errors.append('Expected five face ORAs')
    if canon and hashlib.sha256(Path(canon).read_bytes()).hexdigest()!=CANON_SHA:
        errors.append('Local CANON V2 PNG checksum mismatch')
    for item in manifest.get('items',[]):
        path=directory/item.get('ora_file','')
        if item.get('id') not in EMOTIONS or item.get('alpha_independent_layers')!=7:
            errors.append('Incorrect emotion or independent layer count')
        try:
            with zipfile.ZipFile(path) as z:
                if z.testzip() is not None or z.read('mimetype')!=b'image/openraster':
                    errors.append(f'{path.name}: failed ORA/ZIP CRC or mimetype')
                    continue
                root=ET.fromstring(z.read('stack.xml'))
                if (root.get('w'),root.get('h'))!=('920','456'):
                    errors.append(f'{path.name}: invalid canvas')
                layers=root.findall('./stack/layer')
                if len(layers)!=9:
                    errors.append(f'{path.name}: expected 7 vector parts + underpaint + guide')
                    continue
                labels=[l.get('name') for l in layers]
                if set(PARTS)-set(labels):errors.append(f'{path.name}: missing independent parts')
                if labels[-1]!='GUIDE_CANON_V2_ORIGINAL_REFERENCE_ONLY' or layers[-1].get('visibility')!='hidden':
                    errors.append(f'{path.name}: unmodified canonical reference must remain hidden')
                if labels[-2]!='BASE_UNDERPAINT_AUTO_NOT_APPROVED':
                    errors.append(f'{path.name}: provisional underpaint not labeled')
                parts={};composite=None
                for layer in reversed(layers):
                    img=Image.open(io.BytesIO(z.read(layer.get('src')))).convert('RGBA')
                    if img.size!=(920,456):errors.append(f'{path.name}: mismatched layer dimensions')
                    if layer.get('name') in PARTS:
                        data=img.getchannel('A');count=sum(v for k,v in enumerate(data.histogram()) if k>0)
                        if count==0:errors.append(f'{path.name}: empty alpha in {layer.get("name")}')
                        parts[layer.get('name')]=hashlib.sha256(z.read(layer.get('src'))).hexdigest()
                    if layer.get('visibility')!='hidden':
                        composite=img.copy() if composite is None else Image.alpha_composite(composite,img)
                if len(parts)!=7 or len(set(parts.values()))!=7:
                    errors.append(f'{path.name}: duplicate / missing independent sprite layers')
                merged=Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA')
                if composite is None or ImageChops.difference(composite,merged).getbbox() is not None:
                    errors.append(f'{path.name}: merged preview differs from visible ORA layers')
                if item.get('underpaint_status')!='algorithmic_placeholder':
                    errors.append('Inpainting cannot be claimed artist-approved')
        except (OSError,KeyError,zipfile.BadZipFile,ET.ParseError) as exc:
            errors.append(f'{path.name}: file read error {exc}')
    if manifest.get('status')!='new_vector_facial_parts_on_canon_v2_inpaint_prototype_not_approved_for_game':
        errors.append('Prototype status must not be changed without independent art approval')
    if any(manifest.get(x) is not False for x in ('production_ready','spine_ready','apk_ready','asset_registration_allowed')):
        errors.append('Prototype must not be promoted as game-ready')
    pending.extend(['Native face guide is 230x114: requires real high-resolution V2-compatible art',
                    'Underpaint is algorithmic: needs artist skin/eyelid reconstruction',
                    'Independent SVG shapes need visual review, redraw and Spine/Android integration'])
    if strict:errors+=pending
    return errors,pending

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    p.add_argument('--canon',type=Path)
    p.add_argument('--strict',action='store_true')
    opts=p.parse_args()
    errors,pending=audit(opts.directory,strict=opts.strict,canon=opts.canon)
    print(json.dumps({'passed':not errors,'errors':errors,'pending':pending},ensure_ascii=False,indent=2))
    raise SystemExit(bool(errors))
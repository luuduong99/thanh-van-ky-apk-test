#!/usr/bin/env python3
"""CP330 technical audit. Does NOT certify expression art, CANON likeness or Spine.

Only checks pixel provenance, layer integrity and default compositing against
flat *unapproved* redraw candidates. Strict mode always blocks this checkpoint.
"""
from __future__ import annotations
import argparse,hashlib,io,json,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image,ImageChops

EMOTIONS=['shy','angry','pain','embarrassed','alluring']
PARTS=['brow_image_left','brow_image_right','eye_image_left','eye_image_right','mouth','blush_image_left','blush_image_right']
CANON='LT_CANON_BODY_REF_2026-10-28_V2';EXPRESSION='LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED'
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXP_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'

def hash_file(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def audit_package(directory,strict=False):
    root=Path(directory);manifest=json.loads((root/'manifest.json').read_text())
    errors=[];checks=[]
    if manifest.get('canonical_visual_id')!=CANON or manifest.get('canonical_sha256')!=CANON_SHA:errors.append('CANON V2 mismatch')
    if manifest.get('approved_expression_profile')!=EXPRESSION or manifest.get('approved_expression_sha256')!=EXP_SHA:errors.append('approved expression mismatch')
    if manifest.get('status')!='candidate_flat_art_decomposed_technical_only_NOT_CANON':errors.append('candidate art must not be marked CANON')
    if [x.get('expression_id') for x in manifest.get('results',[])]!=EMOTIONS:errors.append('unexpected expressions')
    for m in manifest.get('results',[]):
        eid=m['expression_id'];p=root/'ora'/f'CP330_{eid}_PAINTED_REGION_TRIAL_NOT_GAME_ART.ora'
        source=root/'candidates'/f'{eid}_NATIVE_UNAPPROVED.png'
        if hash_file(source)!=m['candidate_sha256']:errors.append(eid+': candidate SHA mismatch')
        if hash_file(p)!=m['ora_sha256']:errors.append(eid+': ORA SHA mismatch')
        if not p.exists():errors.append(eid+': ORA absent');continue
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None:errors.append(eid+': ORA CRC error')
            if z.read('mimetype')!=b'image/openraster':errors.append(eid+': not OpenRaster')
            xml=ET.fromstring(z.read('stack.xml'))
            layers=xml.findall('./stack/layer')
            src=Image.open(source).convert('RGB');W,H=src.size
            if (xml.get('w'),xml.get('h'))!=(str(W),str(H)):errors.append(eid+': wrong canvas')
            names=[l.attrib['name'] for l in layers]
            expected=PARTS+['face_base_cutout','automatic_underpaint_REQUIRES_ARTIST_REVIEW','GUIDE_UNAPPROVED_CP330_SOURCE_REFERENCE_ONLY']
            if names!=expected:errors.append(eid+': wrong layer names/order')
            imgs={}
            for layer in layers:
                name=layer.attrib['name']
                b=z.read(layer.attrib['src'])
                image=Image.open(io.BytesIO(b)).convert('RGBA')
                if image.size!=(W,H):errors.append(eid+'/'+name+': wrong dimensions')
                if name in PARTS and image.getchannel('A').getbbox() is None:errors.append(eid+'/'+name+': empty facial alpha')
                imgs[name]=image
            if layers[-1].attrib.get('visibility')!='hidden':errors.append(eid+': guide must be hidden')
            if imgs['automatic_underpaint_REQUIRES_ARTIST_REVIEW'].getchannel('A').getextrema()!=(255,255):errors.append(eid+': underpaint not opaque')
            comp=Image.new('RGBA',(W,H),(0,0,0,0))
            for layer in layers[::-1]:
                if layer.attrib.get('visibility')=='visible':comp=Image.alpha_composite(comp,imgs[layer.attrib['name']])
            if ImageChops.difference(comp.convert('RGB'),src).getbbox():errors.append(eid+': not exact native-source composite')
            ref=Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA')
            if ImageChops.difference(comp,ref).getbbox():errors.append(eid+': merged thumbnail not from layers')
            alpha_union=Image.new('L',(W,H),0)
            for name in PARTS:
                mask=imgs[name].getchannel('A')
                if ImageChops.multiply(alpha_union,mask).getbbox():errors.append(eid+': overlapping painted region masks')
                alpha_union=ImageChops.lighter(alpha_union,mask)
            basealpha=imgs['face_base_cutout'].getchannel('A')
            if ImageChops.difference(basealpha,ImageChops.invert(alpha_union)).getbbox():errors.append(eid+': base cutouts not complementary')
            checks.append({'expression_id':eid,'layers_total':len(layers),'facial_layers':len(PARTS),'native_size_px':[W,H],'composite_pixel_exact':True})
    if manifest.get('production_asset_allowed') is not False or manifest.get('same_canonical_face_master') is not False:errors.append('unapproved art cannot be production/shared face master')
    if strict:errors.append('STRICT_PRODUCTION_BLOCK: CP330 new reference art not user-approved, independent candidate faces, source resolution too low, auto inpaint underpaint not approved')
    return {'passed':not errors,'errors':errors,'checks':checks,'production_ready':False}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--strict',action='store_true');p.add_argument('--out',type=Path);a=p.parse_args()
 result=audit_package(a.directory,a.strict)
 if a.out:a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result['passed'] else 1)
#!/usr/bin/env python3
"""CP329: audit art-intake scaffolds without mistakenly declaring production readiness.

Scaffold QA verifies ORA structure/source fidelity. Production mode requires real
painted independent layers, approved underpaint AND a separately approved art
review. It cannot automatically judge anime art resemblance or real animation.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image

CANON_ID='LT_CANON_BODY_REF_2026-10-28_V2'
EMOTION_ID='LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED'
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EMOTION_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
EMOTIONS=('shy','angry','pain','embarrassed','alluring')
MASTER=('hair_back','face_base','neck','ear','skin_underpaint','eye_socket_left',
        'eye_socket_right','nose','jaw_transition','hair_front','ornaments')
PARTS=('brow_image_left','brow_image_right','eye_image_left','eye_image_right',
       'mouth','blush_image_left','blush_image_right')
W,H=2048,2048

def hash_bytes(raw):return hashlib.sha256(raw).hexdigest()
def hash_file(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _png_qa(raw,cache):
    sh=hash_bytes(raw)
    if sh in cache:return cache[sh]
    with Image.open(io.BytesIO(raw)) as image:
        image.verify()
    with Image.open(io.BytesIO(raw)) as image:
        if image.size!=(W,H) or image.mode!='RGBA':
            result={'bad_shape':f'expected RGBA {W}x{H}, got {image.mode} {image.size}', 'alpha_pixels':None}
        else:
            alpha=image.getchannel('A')
            histogram=alpha.histogram()
            pixels=sum(histogram[5:])
            result={'bad_shape':None,'alpha_pixels':pixels}
    cache[sh]=result
    return result

def audit_ora(path,required_names,allow_guide=False):
    problems=[]; warnings=[]; counts={}; hashes={}
    with zipfile.ZipFile(path) as z:
        if z.testzip():problems.append(f'ORA has corrupted member: {path.name}')
        if z.read('mimetype') != b'image/openraster':problems.append('wrong OpenRaster MIME')
        root=ET.fromstring(z.read('stack.xml'))
        if (root.attrib.get('w'),root.attrib.get('h'))!=(str(W),str(H)):
            problems.append('wrong ORA canvas: must be 2048x2048')
        layers=root.findall('./stack/layer')
        clean={};guides=[];cache={}
        for layer in layers:
            name=layer.attrib.get('name','')
            source=layer.attrib.get('src','')
            if not source.startswith('data/') or source not in z.namelist():
                problems.append('invalid layer PNG source: '+source);continue
            if name.startswith('GUIDE_'):
                guides.append(layer)
                if layer.attrib.get('visibility')!='hidden':problems.append('reference guide must remain hidden')
                continue
            key=name.removesuffix(' [EMPTY]')
            if key in clean:problems.append('duplicate layer name '+key)
            clean[key]=layer
            raw=z.read(source)
            try:result=_png_qa(raw,cache)
            except Exception as exc:problems.append(f'invalid PNG in {key}: {exc}');continue
            if result['bad_shape']:problems.append(key+': '+result['bad_shape'])
            counts[key]=result['alpha_pixels']
            hashes[key]=hash_bytes(raw)
        if set(clean)!=set(required_names):
            problems.append('wrong art layer set: '+str(sorted(set(required_names)^set(clean))))
        if allow_guide:
            if len(guides)!=1:problems.append('face master needs one hidden CANON V2 guide')
            else:
                guide_raw=z.read(guides[0].attrib['src'])
                try:
                    img=Image.open(io.BytesIO(guide_raw))
                    if img.size!=(W,H) or img.mode!='RGBA':problems.append('invalid guide PNG dimensions')
                except Exception:problems.append('corrupt guide PNG')
        elif guides:problems.append('expression ORA must not contain visual guide')
        empty=[name for name,pixels in counts.items() if pixels==0]
        if empty:warnings.append(f'{len(empty)}/{len(required_names)} art layers are empty')
        else:
            unique=len(set(hashes.values()))
            if unique<len(required_names):problems.append('duplicate painted PNG layer bytes; possible fake separation')
        if 'mergedimage.png' not in z.namelist():problems.append('missing mergedimage.png')
    return {'file':Path(path).name,'structural_ok':not problems,'problems':problems,
            'warnings':warnings,'alpha_pixels_by_layer':counts,'nonempty_layers':sum(bool(x) for x in counts.values()),
            'total_required_layers':len(required_names),'guide_count':len(guides)}

def audit(root,strict=False):
    root=Path(root)
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    failures=[]
    if m.get('approved_canon_visual_id')!=CANON_ID or m.get('approved_canon_sha256')!=CANON_SHA:
        failures.append('CANON V2 ID/SHA mismatch')
    if m.get('approved_expression_profile_id')!=EMOTION_ID or m.get('approved_expression_sha256')!=EMOTION_SHA:
        failures.append('Five approved expression source mismatch')
    if m.get('native_face_size_px')!=[230,114] or m.get('guide_scale_factor')!=8:
        failures.append('Native source size/scale provenance changed')
    if m.get('expressions')!=list(EMOTIONS):failures.append('Emotions differ from five approved IDs')
    if m.get('created_painted_face_layers')!=0 or m.get('production_face_master_ready') is not False:
        failures.append('Scaffold is falsely marked as painted or ready')
    for name,sha in m.get('files_sha256',{}).items():
        path=root/name
        if not path.is_file() or hash_file(path)!=sha:failures.append('File changed or missing: '+name)
    png=root/'reference/CANON_V2_FACE_NATIVE_230x114.png'
    with Image.open(png) as img:
        if img.size!=(230,114):failures.append('CANON face native reference changed')
    reports=[]
    for name,layers,guide in [('CP329_FACE_MASTER_EMPTY.ora',MASTER,True)]+[
            (f'CP329_{emo}_EXPRESSION_EMPTY.ora',PARTS,False) for emo in EMOTIONS]:
        path=root/'ora'/name
        if not path.exists():failures.append('ORA missing: '+name);continue
        result=audit_ora(path,layers,allow_guide=guide)
        reports.append(result)
        failures.extend(result['problems'])
        if strict and result['nonempty_layers']!=result['total_required_layers']:
            failures.append('Strict art gate requires painted, nonempty layers: '+name)
    # Production approval is independent from the frozen reference design approval.
    if strict:
        if m.get('underpaint_artist_approved') is not True:
            failures.append('No artist-approved clean underpaint')
        if m.get('independent_facial_art_ready') is not True:
            failures.append('No validated independently painted face art')
        if m.get('final_face_asset_user_approved') is not True:
            failures.append('No explicit user approval of final sprite asset')
    return {'checkpoint':'CP329','mode':'strict-production' if strict else 'reference-scaffold',
            'passed':not failures,'failures':failures,'ora_reports':reports,
            'notice':'Structural success is not proof of production art, Spine or APK.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('root',type=Path)
    p.add_argument('--strict',action='store_true')
    args=p.parse_args()
    try:r=audit(args.root,strict=args.strict)
    except (OSError,ValueError,KeyError,zipfile.BadZipFile,ET.ParseError) as e:r={'passed':False,'failures':[str(e)]}
    print(json.dumps(r,indent=2,ensure_ascii=False))
    raise SystemExit(0 if r['passed'] else 1)
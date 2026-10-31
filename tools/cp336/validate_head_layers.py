#!/usr/bin/env python3
"""CP336: verify real layered *face-art staging* before any Spine/Android release.

This cannot decide artistic fidelity; an explicit human visual approval is
mandatory even if the structural/alpha/palette checks all pass.
"""
from __future__ import annotations
import argparse,hashlib,json,re,sys
from pathlib import Path
from PIL import Image

CANON='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
APPROVED='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
IDS=('shy','angry','pain','embarrassed','alluring')
VIEWS=('front','three_quarter')
MASTER=('hair_back','face_underpaint','hair_front','ornament')
PARTS=('brow_left','brow_right','eye_white_left','eye_white_right','iris_left',
       'iris_right','lash_left','lash_right','lid_left','lid_right',
       'mouth','blush_left','blush_right')

class FaceGateError(ValueError): pass

def h(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

def check_path(root:Path, name:str, errors:list[str])->Path|None:
    if not isinstance(name,str) or not name or name.startswith('/') or '\\' in name or '..' in Path(name).parts:
        errors.append(f'Unsafe or missing relative path: {name!r}');return None
    if not name.startswith('art/') or not name.endswith('.png'):
        errors.append(f'Art files must be PNG under art/: {name!r}');return None
    p=(root/name).resolve()
    if not p.is_relative_to(root.resolve()):
        errors.append(f'Art path escaped root: {name!r}');return None
    if not p.is_file():
        errors.append(f'Art file missing: {name!r}');return None
    return p

def alpha_bbox(im:Image.Image):return im.getchannel('A').getbbox()

def samples_opaque(im:Image.Image, bounds:list[int], min_alpha:int=235)->bool:
    x0,y0,x1,y1=bounds
    a=im.getchannel('A')
    for sx in (0.2,0.5,0.8):
        for sy in (0.2,0.5,0.8):
            x=min(im.width-1,max(0,round(x0+sx*(x1-x0-1))))
            y=min(im.height-1,max(0,round(y0+sy*(y1-y0-1))))
            if a.getpixel((x,y))<min_alpha:return False
    return True

def amber_count(im:Image.Image):
    # Rough color warning: iris pixel hue cannot be predominantly blue.
    # Counts RGBA opaque vivid orange/brown; skin pixels do not belong in iris layer.
    n=0;blue=0
    for r,g,b,a in (im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()):
        if a<150:continue
        if r>75 and r>=g*1.17 and g>=b*1.10 and g>32:n+=1
        if b>95 and b>r*1.15 and b>g*1.08:blue+=1
    return n,blue

def validate(root:Path, *,strict:bool=False,minimum:int=1024):
    root=root.resolve();fail=[];checks=[]
    mf=root/'face_art_manifest.json'
    if not mf.is_file():return {'ok':False,'errors':['Missing face_art_manifest.json'],'checks':[]}
    try:d=json.loads(mf.read_text(encoding='utf-8'))
    except (ValueError,OSError) as e:return {'ok':False,'errors':[f'Manifest invalid: {e}'],'checks':[]}
    if d.get('schema_version')!=1:fail.append('Wrong schema_version')
    if d.get('canonical_body_sha256')!=CANON or d.get('approved_expression_sha256')!=APPROVED:
        fail.append('CANON V2 or approved five-emotion checksum mismatch')
    if d.get('character_id')!='lin_qian':fail.append('Wrong character: this profile is Lam Thien only')
    if set(d.get('views',{}))!=set(VIEWS):fail.append('Both front and three_quarter required')
    sizes={};images={};visited=set()
    for view in VIEWS:
        v=d.get('views',{}).get(view,{})
        if not v:continue
        size=v.get('canvas_px',[])
        if not isinstance(size,list) or len(size)!=2 or not all(isinstance(i,int) and i>0 for i in size):
            fail.append(f'{view}: invalid canvas_px');continue
        w,hh=size;sizes[view]=(w,hh)
        if (w!=hh):fail.append(f'{view}: face master must be square with fixed coordinate system')
        if strict and min(w,hh)<minimum:fail.append(f'{view}: native art below {minimum}px; do not upscale source poster')
        roi=v.get('face_attachment_roi_xyxy')
        skin=v.get('underpaint_skin_roi_xyxy')
        for label,b in [('face_attachment',roi),('underpaint_skin',skin)]:
            if not isinstance(b,list) or len(b)!=4 or not all(isinstance(i,int) for i in b):
                fail.append(f'{view}: invalid {label} ROI');continue
            x0,y0,x1,y1=b
            if not (0<=x0<x1<=w and 0<=y0<y1<=hh):fail.append(f'{view}: {label} ROI out of bounds')
        refs=v.get('master_layers',{})
        if set(refs)!=set(MASTER):fail.append(f'{view}: expected exactly {len(MASTER)} base layers')
        face=None
        def read_png(tag,rec,allow_full=False):
            if not isinstance(rec,dict):fail.append(f'{view}/{tag}: expected layer record');return None
            name=rec.get('path');p=check_path(root,name,fail)
            if p is None:return None
            if name in visited:fail.append(f'Duplicate art path across layer roles: {name}')
            visited.add(name)
            if rec.get('sha256')!=h(p):fail.append(f'{view}/{tag}: PNG checksum mismatch')
            try:
                with Image.open(p) as img:
                    if img.format!='PNG' or img.mode!='RGBA':
                        fail.append(f'{view}/{tag}: needs real PNG RGBA; RGB files prohibited');return None
                    im=img.copy()
            except Exception as e:
                fail.append(f'{view}/{tag}: unreadable PNG: {e}');return None
            if im.size!=(w,hh):fail.append(f'{view}/{tag}: dimensions differ from head canvas');return None
            box=alpha_bbox(im)
            if box is None:fail.append(f'{view}/{tag}: fully transparent layer');return None
            if not allow_full and isinstance(roi,list) and len(roi)==4:
                x0,y0,x1,y1=box;u0,v0,u1,v1=roi
                if not (u0<=x0 and x1<=u1 and v0<=y0 and y1<=v1):
                    fail.append(f'{view}/{tag}: alpha outside face attachment ROI')
            images[(view,tag)]=im
            return im
        for item in MASTER:
            im=read_png('master/'+item,refs.get(item),True)
            if item=='face_underpaint':face=im
        if face is not None and isinstance(skin,list) and len(skin)==4:
            if not samples_opaque(face,skin):fail.append(f'{view}: holes in base underpaint across sampled face skin')
        em=v.get('expressions',{})
        if set(em)!=set(IDS):fail.append(f'{view}: missing or extra expression IDs')
        for expression in IDS:
            parts=em.get(expression,{})
            if set(parts)!=set(PARTS):fail.append(f'{view}/{expression}: expected exactly {len(PARTS)} expression parts')
            for part in PARTS:
                im=read_png(expression+'/'+part,parts.get(part))
                if im is not None and part.startswith('iris_'):
                    amber,blue=amber_count(im)
                    if amber<2 or blue>amber:
                        fail.append(f'{view}/{expression}/{part}: amber iris heuristic failed (amber {amber}, blue {blue})')
        # Not possible for approved layer art to have different base PNGs per emotion:
        # the manifest references the one master set above for all five expressions.
        checks.append(f'{view}: shared {len(MASTER)} base layers, {len(IDS)} emotions × {len(PARTS)} attachments')
    if strict:
        prod=d.get('production_release',{})
        if prod.get('status')!='approved_for_runtime':fail.append('Art release remains BLOCKED')
        if prod.get('artist_qa_passed') is not True:fail.append('Artist QA not confirmed')
        if prod.get('runtime_qa_passed') is not True:fail.append('Android runtime QA not confirmed')
        approval=prod.get('user_asset_approval_id')
        if not isinstance(approval,str) or not re.fullmatch(r'[A-Za-z0-9_-]{8,100}',approval):
            fail.append('Missing explicit user acceptance of NEW completed art')
        if not prod.get('front_and_three_quarter_visual_review_passed'):
            fail.append('Front+3/4 visual identity QA missing')
        if not prod.get('independent_face_parts_artist_verified'):
            fail.append('Independent semantic facial parts not artist verified')
        if not prod.get('clean_underpaint_artist_verified'):
            fail.append('Clean underpaint not artist verified')
        if not prod.get('native_resolution_artist_verified'):
            fail.append('Native-resolution redraw not verified (upscale != native art)')
    return {'ok':not fail,'errors':fail,'checks':checks,'layers_read':len(images),
            'views_checked':len(sizes),'strict':strict,'art_acceptance_is_separate_from_technical_gate':True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('art_root',type=Path)
    ap.add_argument('--strict',action='store_true')
    ap.add_argument('--min-native',type=int,default=1024)
    ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    result=validate(args.art_root,strict=args.strict,minimum=args.min_native)
    output=json.dumps(result,ensure_ascii=False,indent=2)
    if args.out:args.out.write_text(output+'\n')
    print(output)
    return 0 if result['ok'] else 1

if __name__=='__main__':sys.exit(main())
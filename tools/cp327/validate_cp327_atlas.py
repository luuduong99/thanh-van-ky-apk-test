#!/usr/bin/env python3
"""CP327 verify exported atlas pixels against its real ORA region sources.

The nonproduction source art is NOT certified by a passing technical audit.
"""
import argparse, hashlib, io, json, sys, zipfile
from pathlib import Path
from PIL import Image, ImageChops
import xml.etree.ElementTree as ET

EXPECTED=('shy','angry','pain','embarrassed','alluring')
PARTS=('brow_image_left','brow_image_right','eye_image_left','eye_image_right','mouth','blush_image_left','blush_image_right')
APPROVED_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def validate(atlas_dir,ora_dir=None,strict=False):
    atlas_dir=Path(atlas_dir); issues=[]; stats={}
    metadata_path=atlas_dir/'CP327_TECH_DEMO_FACE_ATLAS.json'
    if not metadata_path.is_file():return ['Missing atlas metadata'],stats
    try:data=json.loads(metadata_path.read_text(encoding='utf-8'))
    except Exception as e:return ['Invalid atlas metadata: '+str(e)],stats
    imgpath=atlas_dir/data.get('atlas_file','')
    if not imgpath.is_file():return ['Missing atlas PNG'],stats
    try: atlas=Image.open(imgpath).convert('RGBA');atlas.load()
    except Exception as e:return ['Unreadable atlas: '+str(e)],stats
    if atlas.size!=tuple(data.get('atlas_size_px',())):issues.append('Atlas size mismatch')
    if sha(imgpath)!=data.get('atlas_sha256'):issues.append('Atlas SHA256 mismatch')
    if data.get('canonical_sha256') != CANON_SHA:issues.append('Body CANON V2 SHA mismatch')
    if data.get('approved_expression_sheet_sha256') != APPROVED_SHA:issues.append('Approved 5 expression SHA mismatch')
    if data.get('regions_count')!=35 or len(data.get('regions',[]))!=35:issues.append('Expected 35 independent components')
    if sorted({r.get('expression') for r in data.get('regions',[])})!=sorted(EXPECTED):issues.append('Wrong expressions')
    if data.get('source_kind')!='CP326_existing_vector_prototype_not_approved':issues.append('Provenance changed')
    if any(data.get(k) is not False for k in ('production_ready','spine_ready','android_asset_registration_allowed')):
        issues.append('Unapproved draft must never be promoted to production')
    rectangles=[];name_set=set();all_regions=data.get('regions',[])
    source_files={r.get('expression'):r for r in data.get('source_ora_files',[])}
    for rec in all_regions:
        key=rec.get('id');eid=rec.get('expression');part=rec.get('slot')
        if eid not in EXPECTED or part not in PARTS or key!=eid+'__'+part or key in name_set:
            issues.append('Invalid or duplicate layer key '+str(key));continue
        name_set.add(key)
        rect=rec.get('atlas_rect_xywh',[])
        if len(rect)!=4:issues.append(f'Bad atlas bounds {key}');continue
        x,y,w,h=rect
        if any(not isinstance(v,int) for v in rect) or w<1 or h<1 or x<0 or y<0 or x+w>atlas.width or y+h>atlas.height:
            issues.append('Out of bounds layer '+key);continue
        rectangles.append((x,y,x+w,y+h,key))
        patch=atlas.crop((x,y,x+w,y+h))
        if patch.getchannel('A').getbbox() is None:
            issues.append('Empty atlas region '+key)
        if ora_dir is not None:
            src=source_files.get(eid)
            if src is None or not str(src.get('filename','')).endswith('.ora'):
                issues.append('Missing source ORA entry '+key);continue
            source_path=Path(ora_dir)/src['filename']
            if not source_path.is_file() or sha(source_path)!=src.get('source_sha256'):
                issues.append('Source ORA missing/changed '+key);continue
            with zipfile.ZipFile(source_path) as z:
                root=ET.fromstring(z.read('stack.xml'))
                matching=[el for el in root.findall('./stack/layer') if el.attrib.get('name')==part]
                if len(matching)!=1:issues.append('Source ORA layer mismatch '+key);continue
                original=Image.open(io.BytesIO(z.read(matching[0].attrib['src']))).convert('RGBA')
                bbox=original.getchannel('A').getbbox()
                if list(bbox)!=rec.get('original_bbox_xyxy'):
                    issues.append('Source trim mismatch '+key);continue
                if ImageChops.difference(patch,original.crop(bbox)).getbbox() is not None:
                    issues.append('Atlas pixels do not match ORA '+key)
    for i,a in enumerate(rectangles):
        for b in rectangles[i+1:]:
            if a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]:
                issues.append('Overlapping atlas rectangles '+a[4]+' and '+b[4]);break
    for eid in EXPECTED:
        parts={r.get('slot') for r in all_regions if r.get('expression')==eid}
        if parts!=set(PARTS): issues.append(f'Wrong parts for {eid}')
    if strict:issues.append('Production gate blocked: CP326 source art is not artist-approved V2 face sprites')
    stats.update(regions=len(all_regions),atlas_size=list(atlas.size),sources_checked=ora_dir is not None,production_gate='FAIL_EXPECTED' if strict else 'NOT_RUN')
    return issues,stats


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--atlas-dir',type=Path,required=True)
    p.add_argument('--ora-dir',type=Path)
    p.add_argument('--strict',action='store_true')
    args=p.parse_args()
    issues,stats=validate(args.atlas_dir,args.ora_dir,args.strict)
    print(json.dumps({'passed':not issues,'issues':issues,'stats':stats},indent=2))
    return 1 if issues else 0

if __name__=='__main__':sys.exit(main())
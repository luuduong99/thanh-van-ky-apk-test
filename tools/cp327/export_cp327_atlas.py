#!/usr/bin/env python3
"""CP327: deterministic engine-neutral facial attachment atlas from existing ORA.

STRICTLY TECH DEMO. Input ORAs are CP326 vector face prototypes, NOT production art.
Output is NOT a Spine skeleton/atlas, and never registers Android sprite paths.
"""
from __future__ import annotations
import argparse, hashlib, io, json, re, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

EXPRESSIONS=('shy','angry','pain','embarrassed','alluring')
PARTS=('brow_image_left','brow_image_right','eye_image_left','eye_image_right','mouth','blush_image_left','blush_image_right')
REF_CANON='LT_CANON_BODY_REF_2026-10-28_V2'
APPROVED_PROFILE='LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED'
APPROVED_SHEET_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
CANVAS=2048
PADDING=6


def sha_bytes(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def inspect_ora(ora:Path, eid:str):
    """Only allow exact 7 facial layers and an underlying base/hidden guide."""
    if not ora.is_file():raise ValueError(f'missing ORA {ora}')
    with zipfile.ZipFile(ora) as z:
        corrupted=z.testzip()
        if corrupted is not None:raise ValueError(f'zip crc error {corrupted}')
        if z.read('mimetype') != b'image/openraster':raise ValueError('not OpenRaster')
        root=ET.fromstring(z.read('stack.xml'))
        ww,hh=int(root.attrib['w']),int(root.attrib['h'])
        if (ww,hh)!=(920,456): raise ValueError(f'invalid CP326 canvas {(ww,hh)}')
        layers=root.findall('./stack/layer')
        outputs={}
        for layer in layers:
            name=layer.attrib.get('name','')
            if name.startswith('GUIDE_'):
                if layer.attrib.get('visibility')!='hidden':raise ValueError('reference guide must be hidden')
                continue
            if name.startswith('BASE_'):continue
            if name not in PARTS or name in outputs: raise ValueError(f'unexpected/repeated layer {name}')
            src=layer.attrib.get('src','')
            if not re.fullmatch(r'data/layer\d\d\.png',src):raise ValueError('unsafe ORA source')
            image=Image.open(io.BytesIO(z.read(src))).convert('RGBA')
            if image.size!=(ww,hh):raise ValueError(f'layer size mismatch {name}')
            bbox=image.getchannel('A').getbbox()
            if not bbox: raise ValueError(f'empty layer {name}')
            outputs[name]=(image.crop(bbox),bbox)
        if set(outputs)!=set(PARTS):raise ValueError(f'missing facial parts for {eid}')
        return outputs,(ww,hh)


def layout_atlas(parts:list[dict],size=CANVAS,pad=PADDING):
    """Repeatable shelf packing sorted by height, then stable key."""
    parts=sorted(parts,key=lambda r:(-r['image'].height, -r['image'].width, r['id']))
    x,y,rowh=pad,pad,0
    for p in parts:
        w,h=p['image'].size
        if x+w+pad > size:
            x=pad;y+=rowh+pad;rowh=0
        if y+h+pad>size:raise ValueError('atlas full')
        p['atlas_origin']=(x,y)
        x+=w+pad; rowh=max(rowh,h)
    return parts


def export(ora_dir:Path,out_dir:Path):
    out_dir.mkdir(parents=True,exist_ok=True)
    parts=[];source=[]
    for i,eid in enumerate(EXPRESSIONS,1):
        filename=f'CP326_{i:02d}_{eid}_VECTOR_FACE_LAYERS_PROTOTYPE.ora'
        filepath=ora_dir/filename
        region,orig=inspect_ora(filepath,eid)
        source.append({'expression':eid,'filename':filename,'source_sha256':sha_bytes(filepath.read_bytes()),'canvas':orig})
        for part in PARTS:
            im,bbox=region[part]
            parts.append({'id':eid+'__'+part,'expression':eid,'slot':part,'image':im,'original_bbox_xyxy':bbox,'original_canvas':orig})
    parts=layout_atlas(parts)
    atlas=Image.new('RGBA',(CANVAS,CANVAS),(0,0,0,0))
    records=[]
    for part in parts:
        x,y=part['atlas_origin'];pic=part['image']
        atlas.paste(pic,(x,y))
        bbox=part['original_bbox_xyxy']
        records.append({
            'id':part['id'], 'expression':part['expression'],'slot':part['slot'],
            'atlas_rect_xywh':[x,y,pic.width,pic.height],
            'offset_in_original_canvas_xy':[bbox[0],bbox[1]],
            'original_bbox_xyxy':list(bbox),'source_canvas_px':list(part['original_canvas']),
            'trimmed_alpha_nonzero':int(sum(v>0 for v in pic.getchannel('A').getdata()))
        })
    atlaspath=out_dir/'CP327_TECH_DEMO_FACE_ATLAS_RGBA.png'
    atlas.save(atlaspath,optimize=True)
    data={
      'schema_version':1,'checkpoint':'CP327','character_id':'lin_qian',
      'production_ready':False,'spine_ready':False,'android_asset_registration_allowed':False,
      'source_kind':'CP326_existing_vector_prototype_not_approved',
      'canonical_visual_id':REF_CANON,'canonical_sha256':CANON_SHA,
      'approved_expression_id':APPROVED_PROFILE,'approved_expression_sheet_sha256':APPROVED_SHEET_SHA,
      'atlas_format':'engine_neutral_png_json_not_spine_atlas','atlas_file':atlaspath.name,
      'atlas_size_px':[CANVAS,CANVAS],'atlas_sha256':sha_bytes(atlaspath.read_bytes()),
      'alpha_mode':'straight_RGBA','extrusion_pixels':0,'padding_pixels':PADDING,
      'regions_count':len(records),'source_ora_files':source,'regions':records,
      'limits':['CP326 vector shapes diverge from approved anime linework',
                'body V2 face source is native 230x114 px',
                'inpainted underpaint has artifacts',
                'no approved production full-body layered artwork',
                'atlas is not a Spine skeleton and is not registered in Android']
    }
    p=out_dir/'CP327_TECH_DEMO_FACE_ATLAS.json'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--ora-dir',type=Path,required=True)
    a.add_argument('--out',type=Path,required=True)
    args=a.parse_args()
    info=export(args.ora_dir,args.out)
    print('CP327 atlas exported:',info['regions_count'],'parts,',info['atlas_size_px'],'production ready=',info['production_ready'])

if __name__=='__main__':main()
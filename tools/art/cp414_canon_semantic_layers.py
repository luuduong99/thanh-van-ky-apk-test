#!/usr/bin/env python3
"""CP414 exact-CANON source sampled rough layer separation (artist DRAFT only).
All RGB comes from original CANON. Masks are human-estimated, NOT rig-quality.
No hidden underpaint or closed-eyelid art is fabricated.
"""
from __future__ import annotations
import argparse, hashlib, io, json, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_FILE = 'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
CANON_DIMS = (941,1672)
FRONT_RECT = (16,180,224,623)
FRONT_SIZE = (208,443)
# All polygons in the 208x443 front-standing canvas; all positions preliminary.
REGIONS = {
 '01_hair_crown_fringe': [(100,0),(88,2),(78,9),(69,20),(70,38),(78,52),(85,52),(90,43),(99,40),(112,42),(121,53),(131,52),(141,39),(140,21),(132,9),(116,1)],
 '02_face_cheeks': [(89,42),(85,46),(84,57),(87,65),(94,72),(103,77),(113,75),(123,69),(129,60),(129,49),(121,42)],
 '03_left_open_eye_source': [(86,49),(88,46),(95,45),(102,47),(105,52),(103,58),(95,59),(88,57)],
 '04_right_open_eye_source': [(105,46),(112,44),(121,45),(126,49),(127,55),(120,60),(111,59),(107,55)],
 '05_left_hair_ornament': [(76,13),(66,18),(65,32),(64,40),(61,50),(67,67),(74,63),(83,49),(92,32),(85,18)],
 '06_right_hair_ornament': [(122,8),(133,12),(146,25),(145,42),(152,61),(138,67),(130,51),(121,36)],
 '07_left_upper_hair': [(77,37),(87,46),(90,73),(101,93),(91,112),(78,136),(57,160),(52,151),(68,117),(73,85),(61,63)],
 '08_right_upper_hair': [(126,34),(140,45),(146,71),(151,96),(164,125),(177,148),(159,163),(136,123),(123,98),(116,82)],
 '09_neck_collar_source': [(96,70),(113,70),(122,85),(127,97),(117,105),(103,105),(85,98),(92,85)],
 '10_left_long_hair_research': [(67,105),(80,124),(74,153),(63,179),(49,205),(29,206),(41,172),(49,135)],
 '11_right_long_hair_research': [(148,99),(157,115),(175,143),(188,181),(182,207),(167,199),(153,166),(130,133)],
}
ARTIST_EMPTY = ['12_NECK_SCALP_UNDERPAINT_EMPTY','13_TRUE_CLOSED_EYELIDS_SAME_POSE_EMPTY']


def sha(path: Path): return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path):
    if sha(path) != CANON_SHA: raise ValueError('Incorrect CANON raw sha256')
    im=Image.open(path).convert('RGBA')
    if im.size!=CANON_DIMS: raise ValueError('Incorrect CANON canvas size')
    return im

def mask_polygon(pts, dim=FRONT_SIZE):
    mask=Image.new('L', dim, 0);ImageDraw.Draw(mask).polygon(pts, fill=255)
    return mask

def extract(front: Image.Image, points):
    # Copy exact rgba values where polygon has coverage. No repaint or resynthesis.
    a=np.asarray(front).copy()
    m=np.asarray(mask_polygon(points))
    a[:,:,3]=np.minimum(a[:,:,3],m)
    return Image.fromarray(a,'RGBA')

def boxes_from_polys(polys):
    return {k:[min(p[0] for p in v),min(p[1] for p in v),max(p[0] for p in v),max(p[1] for p in v)] for k,v in polys.items()}

def save_ora(target:Path, source:Image.Image, layers):
    root=ET.Element('image',{'w':'208','h':'443','name':'CP414 CANON source + source-sampled semantic DRAFT (NO artist underpaint)','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(target,'w') as z:
        z.writestr('mimetype',b'image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,layer,visible) in enumerate(layers):
            entry=f'data/layer_{i:02d}.png'
            blob=io.BytesIO();layer.save(blob,format='PNG');z.writestr(entry,blob.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':entry,'opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        blob=io.BytesIO();source.save(blob,format='PNG');z.writestr('mergedimage.png',blob.getvalue())

def preview_board(front, separated, scale=3):
    # Diagnostic not artwork. Flatten original separated source pieces against checkerboard.
    w=270*4; cell_h=scale*138+37
    h=cell_h*4+62
    out=Image.new('RGB',(w,h),(239,244,250)); d=ImageDraw.Draw(out)
    d.text((14,10),'CP414 - CANON SOURCE-PIXEL LAYERS / ROUGH MASKS / NOT PRODUCTION ART',fill=(15,43,79))
    records=[('00 ORIGINAL (CANON)',front.crop((53,0,155,138)))]
    for name,img in separated.items():records.append((name,img.crop((53,0,155,138))))
    while len(records)<16:records.append(('UNDERPAINT / EYELID MISSING', Image.new('RGBA',(102,138),(0,0,0,0))))
    for idx,(name,img) in enumerate(records[:16]):
        row=idx//4;col=idx%4;x=8+col*270;y=52+row*cell_h
        d.rectangle((x,y,x+256,y+cell_h-6),fill=(255,255,255),outline=(196,207,220))
        d.text((x+7,y+6),name[:31],fill=(37,58,76))
        bg=Image.new('RGBA',(102,138),(239,239,239,255));pix=bg.load()
        for py in range(0,138,7):
            for px in range(0,102,7):
                if ((px//7+py//7)%2)==0:
                    for iy in range(py,min(py+7,138)):
                        for ix in range(px,min(px+7,102)):pix[ix,iy]=(215,222,231,255)
        bg.alpha_composite(img)
        if name.startswith('00'):bg=img.convert('RGBA')
        v=bg.convert('RGB').resize((204,276),Image.Resampling.NEAREST)
        out.paste(v,(x+25,y+28))
    return out

def full_guide(front):
    zoom=front.resize((832,1772),Image.Resampling.NEAREST).convert('RGB');d=ImageDraw.Draw(zoom)
    colors=[(39,111,203),(198,60,112),(44,164,113),(44,164,113),(203,130,18),(203,130,18),(78,90,220),(78,90,220),(169,71,209),(85,169,213),(85,169,213)]
    for (key,points),c in zip(REGIONS.items(),colors):
        pol=[(x*4,y*4) for x,y in points]
        d.line(pol+[pol[0]],fill=c,width=3)
        bx,by=pol[0];d.text((max(0,bx),max(0,by-11)),key[:3],fill=c,stroke_width=1,stroke_fill='white')
    return zoom

def run(source:Path,out_dir:Path):
    im=load(source)
    front=im.crop(FRONT_RECT);out_dir.mkdir(parents=True,exist_ok=True)
    front.save(out_dir/'CP414_CANON_FRONT_EXACT.png')
    layers={}; meta=[]
    for key,coords in REGIONS.items():
        p=extract(front,coords)
        outfile=out_dir/f'CP414_{key.upper()}.png';p.save(outfile)
        layers[key]=p
        a=np.asarray(p)[:,:,3]
        meta.append({'name':key,'file':outfile.name,'nonempty_alpha_pixels':int((a>0).sum()),'coords_box':boxes_from_polys({key:coords})[key], 'status':'SOURCE_SAMPLE_ROUGH_DRAFT_NOT_APPROVED'})
    blank=Image.new('RGBA',FRONT_SIZE,(0,0,0,0))
    ora_layers=[(name+' | DRAFT / original CANON pixels',val,False) for name,val in layers.items()]
    for name in ARTIST_EMPTY:ora_layers.append((name,blank,False))
    ora_layers.append(('00 EXACT CANON FRONT (visible only)',front,True))
    save_ora(out_dir/'CP414_SOURCE_PIXEL_LAYERS_NOT_RIG_READY.ora',front,ora_layers)
    preview_board(front,layers).save(out_dir/'CP414_HEAD_LAYER_INSPECTION_BOARD.png')
    full_guide(front).save(out_dir/'CP414_LAYER_BOUNDARIES_4X_SOURCE.png')
    report={
      'checkpoint':'CP414','canon_sha256':CANON_SHA,'source_sha256':sha(source),'source_size':list(im.size),
      'front_crop':list(FRONT_RECT),'front_size':list(front.size),
      'layers_nonempty_source_sampled':len(layers),'layers_blank_artist_required':len(ARTIST_EMPTY),'ora_layers':len(ora_layers),
      'source_rgb_unchanged_where_sampled':True,
      'neutral_canon_visible_exact':True, 'has_new_painter_art':False,'has_artist_neck_underpaint':False,
      'has_artist_correct_pose_eyes_closed':False,'long_hair_art_isolated_verified':False,
      'rig_ready':False,'spine_ready':False,'visual_approved':False,'android_device_verified':False,
      'production_release':{'status':'blocked_pending_art','sprite_paths':{},'apk_production_ready':False},
      'regions':meta,'files':{}
    }
    for f in sorted(out_dir.iterdir()):
        if f.is_file():report['files'][f.name]={'sha256':sha(f),'bytes':f.stat().st_size}
    (out_dir/'CP414_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--canon',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    opt=parser.parse_args()
    result=run(opt.canon,opt.out)
    print(json.dumps({'source_verified':result['source_sha256']==CANON_SHA,'nonempty_layers':result['layers_nonempty_source_sampled'],'artist_approved':result['visual_approved']}))
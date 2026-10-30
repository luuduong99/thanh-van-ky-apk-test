#!/usr/bin/env python3
"""CP389 manual-coordinate closed-eye *draft* for Lâm Thiển V2.1.

Creates independent editable raster layers, source-locked, without external images.
This deliberately does NOT claim painter-grade asset, approved closed-eye art, or rig.
"""
import argparse, hashlib, io, json, shutil, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE=(941,1672); BBOX=(25,684,193,881); SIZE=(168,197); SCALE=8
LEFT=(31,98,67,119); RIGHT=(86,73,127,100)


def verify(canon):
    canon=Path(canon)
    if hashlib.sha256(canon.read_bytes()).hexdigest()!=CANON_SHA:
        raise ValueError('CANON_SHA_MISMATCH: refuse unapproved reference')
    with Image.open(canon) as im:
        if im.mode != 'RGBA' or im.size != CANON_SIZE: raise ValueError('CANON_FORMAT_MISMATCH')
        return im.crop(BBOX).copy()

def bezier(p0,p1,p2,p3,n=100):
    a=[]
    for t in np.linspace(0,1,n):
        u=1-t
        a.append(((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0]),(u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1])))
    return a

def coords(points):return [(int(round(x*SCALE)),int(round(y*SCALE))) for x,y in points]

def down(im):
    # Native output, supersampling only for antialiased edges, not true HD detail.
    return im.resize(SIZE,Image.Resampling.LANCZOS)

def polygon_mask(points,blur=.75):
    mask=Image.new('L',(SIZE[0]*SCALE,SIZE[1]*SCALE));d=ImageDraw.Draw(mask)
    d.polygon(coords(points),fill=255)
    if blur:mask=mask.filter(ImageFilter.GaussianBlur(blur*SCALE))
    return mask

def draw_skin(side):
    spec= {
      'left':dict(points=[(34,103),(41,99),(52,99),(63,99),(66,105),(62,113),(56,119),(43,120),(36,114)],
                  stops=[(0,(214,146,151)),(.40,(242,178,164)),(.75,(250,189,172)),(1,(249,199,186))],
                  roi=LEFT,slant=-.15),
      'right':dict(points=[(87,83),(92,78),(104,75),(118,75),(124,81),(124,88),(115,99),(99,102),(89,94)],
                  stops=[(0,(252,204,193)),(.40,(253,201,185)),(.75,(251,190,177)),(1,(231,177,174))],
                  roi=RIGHT,slant=-.21)
    }[side]
    w,h=SIZE[0]*SCALE,SIZE[1]*SCALE
    xs=np.arange(w,dtype=np.float32).reshape(1,-1)/SCALE
    ys=np.arange(h,dtype=np.float32).reshape(-1,1)/SCALE
    x0,y0,x1,y1=spec['roi']; t=np.clip((xs-x0)/(x1-x0),0,1)
    cols=np.zeros((h,w,3),dtype=np.float32)
    for c in range(3):
        cols[:,:,c]=np.interp(t[0], [i[0] for i in spec['stops']], [i[1][c] for i in spec['stops']])[None,:]
    # translucent eyelid warm highlight/shade on same controlled skin region.
    lid_ref=109+(xs-38)*spec['slant'] if side=='left' else 87+(xs-90)*spec['slant']
    d=ys-lid_ref
    warm=np.exp(-((d-1.5)/4.0)**2)*3.2
    shade=np.exp(-((d+2.2)/3.8)**2)*(-4.7)
    cols[:,:,0]+=warm+shade;cols[:,:,1]+=warm*.60+shade;cols[:,:,2]+=warm*.35+shade*1.2
    arr=np.zeros((h,w,4),dtype=np.uint8)
    arr[:,:,:3]=np.clip(cols,0,255).astype(np.uint8)
    arr[:,:,3]=np.asarray(polygon_mask(spec['points'],.85))
    return down(Image.fromarray(arr,'RGBA'))

def draw_lid(side):
    im=Image.new('RGBA',(SIZE[0]*SCALE,SIZE[1]*SCALE))
    d=ImageDraw.Draw(im)
    if side=='left':
      path=bezier((35.5,108.3),(41.3,104.2),(56.4,100.4),(64.4,103.1))
      crease=bezier((37,104.5),(44,100.2),(56,97.9),(64,100.1))
      lash_pts=[((38,106.9),(35.8,108.1)),((45,103.9),(43.2,106.2)),((53.5,102.3),(53,104.0)),((61,102.5),(63.0,104.5))]
    else:
      path=bezier((89,88.2),(96,82.1),(111,77.2),(122.5,79.4))
      crease=bezier((91,81.2),(100,76.5),(112,73.6),(122.5,75.4))
      lash_pts=[((91,87.6),(88.6,89.3)),((98,82.9),(96.3,85.0)),((110,79.3),(109,81.5)),((120.2,79.4),(123.4,81))]
    # Warming underside before actual lash ink: separate raster from skin layer.
    d.line(coords([(x,y+1) for x,y in path]),fill=(183,91,98,94),width=round(.85*SCALE),joint='curve')
    d.line(coords(crease),fill=(170,93,105,105),width=round(.42*SCALE),joint='curve')
    d.line(coords(path),fill=(75,38,54,235),width=round(1.05*SCALE),joint='curve')
    for p0,p1 in lash_pts:
        d.line(coords([p0,p1]),fill=(65,35,52,140),width=max(1,round(.35*SCALE)),joint='curve')
    return down(im)

def image_bytes(img):
    b=io.BytesIO(); img.save(b,'PNG'); return b.getvalue()

def make_ora(src,parts,dest):
    # leave all unapproved art hidden; only exact CANON visible.
    all_layers=[('CANON SHY EXACT V2.1 • VISIBLE',src,True)]
    all_layers += [(name+' • CLOSED EYE DRAFT HIDDEN',img,False) for name,img in parts.items()]
    # Demonstrate an editable proposed closed state without replacing source.
    proposal=src.copy()
    for item in parts.values():proposal.alpha_composite(item)
    all_layers += [('CP389 CLOSED-EYE COMPOSITE • DRAFT HIDDEN',proposal,False)]
    root=ET.Element('image',w=str(SIZE[0]),h=str(SIZE[1]),name='CP389 CANON exact plus manual eyelid/skin proposal',version='0.0.3')
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(dest,'w') as z:
       z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
       for i,(name,img,visible) in enumerate(all_layers):
           path=f'data/layer{i:02d}.png'
           z.writestr(path,image_bytes(img))
           ET.SubElement(stack,'layer',{'name':name,'src':path,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
       z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
       z.writestr('mergedimage.png',image_bytes(src))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
    return proposal,all_layers

def make_preview(src,proposal,path):
    # Important: source from exact user's CANON; NOT generated substitute.
    W,H=1510,960
    board=Image.new('RGB',(W,H),(18,36,55));d=ImageDraw.Draw(board)
    fp='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    f=ImageFont.truetype(fp,23) if Path(fp).exists() else ImageFont.load_default()
    small=ImageFont.truetype(fp,16) if Path(fp).exists() else ImageFont.load_default()
    d.text((26,16),'CP389 / LÂM THIỂN — CANON-LOCKED EYE PAINT STUDY',font=f,fill=(240,245,255))
    d.text((26,53),'CANON V2.1 gốc — bản mắt nhắm chỉ là bản VẼ THỬ, CHƯA ĐƯỢC DUYỆT',font=small,fill=(250,210,160))
    for i,(img,name) in enumerate([(src,'CANON V2.1 · MỞ MẮT · CHUẨN'),(proposal,'CP389 · NHẮM MẮT · DRAFT / NOT APPROVED')]):
        x=28+i*743
        board.paste(img.resize((672,788),Image.Resampling.NEAREST).convert('RGB'),(x,90))
        d.text((x,888),name,font=small,fill='white' if i==0 else (255,211,160))
    board.save(path)

def generate(canon,dest):
    src=verify(canon) # validate source BEFORE making output directory
    dest=Path(dest);(dest/'art').mkdir(parents=True,exist_ok=True);(dest/'qa').mkdir(exist_ok=True)
    shutil.copyfile(canon,dest/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    src.save(dest/'CANON_SHY_EXACT.png')
    parts={'LEFT_UNDERLAY':draw_skin('left'),'RIGHT_UNDERLAY':draw_skin('right'), 'LEFT_CLOSED_EYELID':draw_lid('left'),'RIGHT_CLOSED_EYELID':draw_lid('right')}
    for name,im in parts.items():im.save(dest/'art'/f'{name}_DRAFT.png')
    candidate,layers=make_ora(src,parts,dest/'CP389_CANON_EXACT_CLOSED_EYE_EDITABLE_STUDY_NOT_APPROVED.ora')
    candidate.save(dest/'CP389_CLOSED_EYE_DRAFT_NOT_APPROVED.png')
    make_preview(src,candidate,dest/'qa'/'CP389_CANON_VS_CLOSED_EYE_ART_DRAFT_NOT_APPROVED.png')
    changes=int(np.any(np.array(src)!=np.array(candidate),axis=2).sum())
    report=dict(checkpoint='CP389',source_sha256=CANON_SHA,face_crop=BBOX,source_preserved=True,
        independent_new_layers=list(parts),ora_layers=len(layers),changed_pixels_draft=changes,
        underpaint_method='manual geometric raster painting sampled to match original palette; NOT source-pixel-exact',
        original_expression_exact=True,closed_eye_artist_approval=False,visual_qa='NOT_PASSED',
        final_game_art=False,production_release=dict(status='blocked_pending_art',sprite_paths={},spine_ready=False,apk_ready=False),
        next_checkpoint='CP390: artist refine closed eye skin/crease and facial edge, review at 168x197 native, obtain approval before blink in-betweens')
    (dest/'CP389_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--canon',required=True);a.add_argument('--out',required=True);ns=a.parse_args()
    print(json.dumps(generate(ns.canon,ns.out),ensure_ascii=False,indent=2))
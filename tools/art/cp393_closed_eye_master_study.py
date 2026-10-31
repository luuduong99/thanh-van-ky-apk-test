#!/usr/bin/env python3
"""CP393 — editable CANON-based closed-eyelid painting *study*, not approved game art.

Uses ONLY exact Lâm Thiển CANON V2.1 pixels and hand-authored mask/stroke
geometry. An unaltered source layer remains visible by default in Krita ORA.
All newly created closed-eye layers and composites are hidden for review.
"""
from __future__ import annotations
import argparse, hashlib, io, json, zipfile, shutil, math
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CROP=(25,684,193,881)
SIZE=(168,197)
ROI={'LEFT':(29,93,71,124),'RIGHT':(83,70,129,110)}
# Hand keyed positions (x,y). These are not final artist-approved curves.
EYES={
 'LEFT': {'upper':[(31,106),(40,102),(53,98),(66,100)],
          'lower':[(31,109),(41,116),(55,111),(67,106)],
          'lash':[(31,107.8),(42,105.4),(55,101.9),(65,101.3)],
          'crease':[(35,100),(45,96.2),(58,94.3),(65,97)],
          'donor_shift':16},
 'RIGHT':{'upper':[(85,86),(95,78),(112,74),(123,77)],
          'lower':[(85,90),(97,96),(112,94),(126,83)],
          'lash':[(86,87.3),(97,83.9),(111,80.2),(123,79.0)],
          'crease':[(89,79),(101,73.5),(114,69.4),(123,72.5)],
          'donor_shift':16}
}
RELEASE={'status':'blocked_pending_art','sprite_paths':{},'spine_ready':False,'apk_ready':False}

def hash_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def source_checked(p):
    if hash_file(p)!=CANON_SHA: raise ValueError('CANON_SHA_MISMATCH')
    with Image.open(p) as im:
        if im.mode!='RGBA' or im.size!=(941,1672):raise ValueError('CANON_DIM_OR_MODE_MISMATCH')
        return im.crop(CROP).copy()

def bezier(points,n=110):
    p=np.array(points,dtype=float);tt=np.linspace(0,1,n)
    return [tuple(((1-t)**3*p[0]+3*t*(1-t)**2*p[1]+3*t*t*(1-t)*p[2]+t**3*p[3]).tolist()) for t in tt]

def rgba_bytes(im):
    buf=io.BytesIO();im.save(buf,'PNG');return buf.getvalue()

def make_masks(side):
    geom=EYES[side];scale=8
    hi=Image.new('L',(SIZE[0]*scale,SIZE[1]*scale),0);d=ImageDraw.Draw(hi)
    up=bezier(geom['upper']);lo=bezier(geom['lower'])
    pts=[(int(round(x*scale)),int(round(y*scale))) for x,y in up+list(reversed(lo))]
    d.polygon(pts,fill=255)
    # Slight 0.6px feather — retains source texture at the boundary.
    lo_mask=hi.resize(SIZE,Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(.60))
    ar=np.asarray(lo_mask,dtype=np.uint8).copy();x1,y1,x2,y2=ROI[side]
    outside=np.zeros_like(ar);outside[y1:y2,x1:x2]=ar[y1:y2,x1:x2]
    return outside

def donor_layer(src,side):
    # Preserve real localized tonal texture from CANON itself, rather than flat fill.
    a=np.asarray(src).copy();res=np.zeros_like(a);h,w=a.shape[:2]
    mask=make_masks(side);shift=EYES[side]['donor_shift']
    xx=np.arange(w)[None,:]; yy=np.arange(h)[:,None]
    # Small horizontal offset avoids replicating exact eye contour from donor.
    sx=np.clip(xx+1,0,w-1);sy=np.clip(yy+shift,0,h-1)
    donor=a[sy,sx,:3].astype('float32')
    # Under-lid donor illumination from the adjacent skin in the same source.
    x1,y1,x2,y2=ROI[side]
    # Delicate warm tint; only within eye mask and not global facial recoloring.
    donor[:,:,0]=np.clip(donor[:,:,0]+1.3,0,255)
    donor[:,:,1]=np.clip(donor[:,:,1]-.3,0,255)
    donor[:,:,2]=np.clip(donor[:,:,2]-.9,0,255)
    res[...,:3]=np.uint8(donor)
    res[...,3]=mask
    return Image.fromarray(res,'RGBA')

def make_shadows(side):
    # Soft crease and lash-root shadow, separated from donor skin; not a flat patch.
    scale=8;geom=EYES[side];im=Image.new('RGBA',(SIZE[0]*scale,SIZE[1]*scale));
    d=ImageDraw.Draw(im,'RGBA')
    cr=bezier(geom['crease']);las=bezier(geom['lash']);x1,y1,x2,y2=ROI[side]
    def ps(points):return [(int(x*scale),int(y*scale)) for x,y in points]
    d.line(ps(cr),fill=(121,69,83,44),width=scale)
    # Soft lid crease along source eye angle.
    d.line(ps(las),fill=(117,50,63,70),width=2*scale)
    blur=im.filter(ImageFilter.GaussianBlur(radius=2.1*scale))
    return clip_roi(blur.resize(SIZE,Image.Resampling.LANCZOS),side)

def make_lash(side,taper=1.0):
    # Explicit independent fine lash strokes; each side has different curvature.
    geom=EYES[side];S=8;im=Image.new('RGBA',(SIZE[0]*S,SIZE[1]*S));d=ImageDraw.Draw(im)
    curve=bezier(geom['lash'],n=200)
    d.line([(int(x*S),int(y*S)) for x,y in curve],fill=(68,38,44,175),width=8)
    # warm highlight/reflection at upper edge of the eyelid
    d.line([(int(x*S),int((y-.65)*S)) for x,y in curve],fill=(151,79,85,64),width=3)
    for frac in ([.09,.18,.27,.38,.52,.66,.79,.9] if side=='LEFT' else [.06,.16,.29,.43,.55,.69,.81,.91]):
        pos=curve[int(frac*(len(curve)-1))];x,y=pos
        # Tuft length tapers toward corners; very subtle near its center.
        length=(.7+1.65*abs(frac-.50))*taper
        dx=(-.60 if side=='LEFT' else .58)*(1 if frac>.3 else .7)
        d.line([(int(x*S),int(y*S)),(int((x+dx)*S),int((y+length)*S))],fill=(75,40,47,135),width=4)
    out=im.resize(SIZE,Image.Resampling.LANCZOS)
    return clip_roi(out,side)

def clip_roi(im,side):
    ar=np.asarray(im).copy();x1,y1,x2,y2=ROI[side]
    ar[:y1,:,3]=0;ar[y2:,:,3]=0;ar[:,:x1,3]=0;ar[:,x2:,3]=0
    return Image.fromarray(ar,'RGBA')

def paint(src,layers,subtle=False):
    out=src.copy()
    for side in ['LEFT','RIGHT']:
        out.alpha_composite(layers[side]['SKIN'])
        if not subtle: out.alpha_composite(layers[side]['SHADOW'])
        out.alpha_composite(layers[side]['LASH'])
    return out

def changed_outside(original,changed):
    a=np.asarray(original);b=np.asarray(changed)
    outside=np.ones((SIZE[1],SIZE[0]),bool)
    for x1,y1,x2,y2 in ROI.values():outside[y1:y2,x1:x2]=False
    return int(np.any(a[outside]!=b[outside],axis=1).sum())

def validate_art(src,art):
    assert src.size==art.size==SIZE
    assert changed_outside(src,art)==0
    assert np.count_nonzero(np.any(np.asarray(src)!=np.asarray(art),axis=2))>100

def make_ora(src,layers,candidate,subtle,ora_path):
    # Only the original approved CANON is visible by default.
    data=[('CANON V2.1 / SHY / ORIGINAL / visible',src,True)]
    for side in ['LEFT','RIGHT']:
        for typ in ['SKIN','SHADOW','LASH']:
            data.append((f'CP393 {side} {typ} / DRAFT / HIDDEN',layers[side][typ],False))
    data += [('CP393 CLOSED-EYE CANDIDATE / NOT APPROVED',candidate,False),('CP393 SOFT CANDIDATE / NOT APPROVED',subtle,False)]
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'name':'CP393 closed-eyelid painted layers / NOT APPROVED','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(ora_path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(data):
            ref=f'data/layer_{i:02d}.png'
            z.writestr(ref,rgba_bytes(im))
            ET.SubElement(stack,'layer',{'name':name,'src':ref,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',rgba_bytes(src))
        z.writestr('Thumbnails/thumbnail.png',rgba_bytes(src.resize((84,98))))
    with zipfile.ZipFile(ora_path) as z:
        assert z.testzip() is None
        assert len(ET.fromstring(z.read('stack.xml')).find('stack'))==len(data)
        assert np.array_equal(np.array(Image.open(io.BytesIO(z.read('mergedimage.png')))),np.array(src))
    return len(data)

def comparison(src,cp392,full,soft,path):
    scale=3;pad=22;gap=12;top=98;w,h=SIZE
    cards=[('CANON V2.1 / exact source',src),('CP392 / near-closed old draft',cp392),('CP393 / fully-closed sketch',full),('CP393 / soft closed variant',soft)]
    cw=(w*scale);width=pad*2+cw*4+gap*3
    bg=Image.new('RGB',(width,800),(13,34,53));d=ImageDraw.Draw(bg)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    hfont=ImageFont.truetype(font,22);body=ImageFont.truetype(font,15);small=ImageFont.truetype(font,13)
    d.text((pad,17),'TVK CP393 | Lam Thien V2.1 | exact source and two closed-eye painting studies',fill='white',font=hfont)
    d.text((pad,53),'DRAFT ONLY: 168 x 197 native pixels, no approved closed-eye keyframe, rig or APK.',fill=(255,206,152),font=body)
    for i,(name,im) in enumerate(cards):
        x=pad+i*(cw+gap)
        bg.paste(im.convert('RGB').resize((cw,h*scale),Image.Resampling.NEAREST),(x,top))
        d.text((x,top+h*scale+12),name,fill='white',font=small)
    d.text((pad,top+h*scale+44),'CANON is pixel-exact. Skin underpaint samples from CANON; lash/shadow paths are hand authored.',font=small,fill=(204,225,238))
    d.text((pad,top+h*scale+69),'Artist acceptance: NOT PASSED. No claim of genuine HD redrawing or in-game smooth motion.',font=small,fill=(255,206,152))
    bg.save(path)

def create(canon,prior,out):
    # Verify sources before any output (including directories) is written.
    src=source_checked(canon)
    with Image.open(prior) as im:
        if im.size!=SIZE:raise ValueError('PRIOR_SIZE_MISMATCH')
        old=im.convert('RGBA').copy()
    out=Path(out); art=out/'art';qa=out/'qa';art.mkdir(parents=True,exist_ok=True);qa.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(canon,out/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    src.save(out/'CANON_SHY_EXACT.png')
    layers={}
    for side in ['LEFT','RIGHT']:
        layers[side]={'SKIN':donor_layer(src,side),'SHADOW':make_shadows(side),'LASH':make_lash(side)}
        for kind,p in layers[side].items():p.save(art/f'{side}_{kind}_DRAFT.png')
    full=paint(src,layers);soft=paint(src,layers,subtle=True)
    validate_art(src,full);validate_art(src,soft)
    full.save(out/'CP393_FULL_CLOSED_PAINT_STUDY_NOT_APPROVED.png')
    soft.save(out/'CP393_SOFT_CLOSED_PAINT_STUDY_NOT_APPROVED.png')
    ora=out/'CP393_CANON_AND_6_EDITABLE_EYELID_PAINT_LAYERS_NOT_APPROVED.ora'
    n=make_ora(src,layers,full,soft,ora)
    comparison(src,old,full,soft,qa/'CP393_CANON_CP392_AND_NEW_CLOSED_EYE_STUDY.png')
    report={
       'checkpoint':'CP393','source':'Lâm Thiển user-approved CANON V2.1','source_sha256':CANON_SHA,
       'crop_xyxy':list(CROP),'native_size':list(SIZE),'layers':n,
       'art_layers':6,'original_canon_visible_exact':True,
       'candidate_pixels_changed':{p:int(np.any(np.asarray(src)!=np.asarray(im),axis=2).sum()) for p,im in [('full',full),('soft',soft)]},
       'outside_eye_change_count':{p:changed_outside(src,im) for p,im in [('full',full),('soft',soft)]},
       'source_reuse_policy':'CANON-only, hand keyed mask curves, colors sampled from same portrait; all edited layers hidden by default',
       'visual_qa':'NOT_PASSED','manual_artist_approval':False,'native_HD_master':False,'actual_rig_animation':False,
       'release':RELEASE,'next':'CP394: manual artist correction of fully closed-lid contour and skin/eyelash shading; user approves visual master first.'
    }
    (out/'CP393_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--prior',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(create(a.canon,a.prior,a.out),indent=2,ensure_ascii=False))
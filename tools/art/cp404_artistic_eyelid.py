#!/usr/bin/env python3
"""CP404: editable eye-only same-CANON eyelid art study; never production approved."""
import hashlib, sys, json, io, zipfile, math
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from xml.etree import ElementTree as ET

sys.path.insert(0,str(Path(__file__).resolve().parents[0]))
import cp401_occlusion_blink as base
SHA=base.CANON_SHA; SIZE=base.SIZE; ROIS=base.ROIS


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def compose_study(src, kind='feather'):
    """Reconstruct local eyelids from source RGB only; split editable paint into semantic RGBA layers.
    No intended modification beyond ROI; manual artist signoff remains mandatory.
    """
    if kind not in ('feather','defined'):raise ValueError('UNKNOWN_VARIANT')
    rgb=np.asarray(src.convert('RGB'))
    h,w=SIZE[1],SIZE[0];s=12
    mask=np.zeros((h,w),dtype=np.uint8)
    # Remove original visible iris, sclera and source eyelashes, with a margin for skin repair.
    for side,(x1,y1,x2,y2) in ROIS.items():
        for x in range(x1+2,x2-1):
            u=base.curve(side,x,base.UPPER);l=base.curve(side,x,base.LOWER)
            ylo=max(y1+1,int(math.floor(u-4.5)));yhi=min(y2-1,int(math.ceil(l+7.0)))
            mask[ylo:yhi,x]=255
    # Source-only inpainting. Keep mask within ROI; feather borders without altering source beyond ROIs.
    inpaint=cv2.cvtColor(cv2.inpaint(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),mask,6,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
    alpha=cv2.GaussianBlur(mask,(5,5),.85).astype(np.float32)/255.
    alpha[mask==0]=0
    repaired=np.uint8(np.rint(rgb*(1-alpha[...,None])+inpaint*alpha[...,None]))
    repaired_rgba=np.dstack([repaired,np.asarray(src)[:,:,3]])

    def layer():return Image.new('RGBA',(w*s,h*s),(0,0,0,0))
    shade, crease, lash, tips = layer(),layer(),layer(),layer()
    sh=ImageDraw.Draw(shade,'RGBA'); cr=ImageDraw.Draw(crease,'RGBA'); la=ImageDraw.Draw(lash,'RGBA'); ti=ImageDraw.Draw(tips,'RGBA')
    def P(x,y):return (round(x*s),round(y*s))
    def polygon_curve(draw, side, pts, color, width, offset=0):
        draw.line([P(float(x),float(y+offset)) for x,y in pts],fill=color,width=round(width*s),joint='curve')

    for side,(x1,y1,x2,y2) in ROIS.items():
        # LEFT outer corner is x1; RIGHT outer corner is x2.
        for t in np.linspace(.045,.955,110):
            x,y=base.bez(base.CLOSED[side],float(t)); x=float(x);y=float(y)
            outer=(1-t if side=='LEFT' else t)
            mid=math.sin(math.pi*t)**.75
            # Soft eyelid fold from same warm rose skin palette, not a uniform black pen line.
            # Keep faint lower-lid skin shadow to give depth.
            for delta,radius,opacity,color in [(-2.1,.54,16,(156,79,94)),(-1.2,.70,9,(181,112,122)),(1.45,.90,13,(180,105,116))]:
                opa=round(opacity*mid)
                sh.ellipse((P(x-radius,y+delta-radius),P(x+radius,y+delta+radius)),fill=(*color,opa))
        # Thin upper-lid fold: faded near tear ducts / corners.
        fold=[base.bez(base.CLOSED[side],float(t)) for t in np.linspace(.17,.83,60)]
        polygon_curve(cr,side,fold,(151,81,96,34 if kind=='feather' else 44),.38,offset=-2.55)
        # Variable-width, gently curved warm brown lash roots; fade at center/inner corners.
        for t in np.linspace(.038,.962,190):
            x,y=base.bez(base.CLOSED[side],float(t));x=float(x);y=float(y)
            outer=(1-t if side=='LEFT' else t)
            edge=math.sin(math.pi*t)**.59
            density=(.32+.68*outer)*edge
            opacity=round((203 if kind=='feather' else 238)*(.45+.55*outer)*edge)
            thickness=(.72+.60*outer)*edge
            la.ellipse((P(x-thickness/2,y-thickness/2),P(x+thickness/2,y+thickness/2)),fill=(70,40,51,opacity))
        # Fine separated native-corner lash tips: organic curves, 4 per corner, graded rather than spiky triangles.
        ts=[.06,.115,.185,.27] if side=='LEFT' else [.72,.80,.88,.94]
        for j,t in enumerate(ts):
            x,y=base.bez(base.CLOSED[side],t);x=float(x);y=float(y)
            outward=-1 if side=='LEFT' else 1
            length=(.55+.12*(3-j if side=='LEFT' else j))
            pt=[P(x,y),P(x+outward*length*.55,y-.28),P(x+outward*length,y-.57)]
            ti.line(pt,fill=(83,50,58,155 if kind=='feather' else 200),width=max(1,round(.27*s)),joint='curve')
    # Compose hi-res semantic layers then feather to canonical native pixels.
    layers=[('skin_shade',shade),('soft_crease',crease),('source_palette_lashes',lash),('tapered_lash_tips',tips)]
    all_rgba=Image.fromarray(repaired_rgba,'RGBA')
    editable={}
    allow=np.zeros((h,w),bool)
    for x1,y1,x2,y2 in ROIS.values():allow[y1:y2,x1:x2]=True
    for name,hi in layers:
        image=hi.resize((w,h),Image.Resampling.LANCZOS)
        overlay=np.asarray(image).copy();overlay[~allow]=0
        image=Image.fromarray(overlay,'RGBA')
        editable[name]=image
        all_rgba=Image.alpha_composite(all_rgba,image)
    ret=np.asarray(all_rgba).copy()
    original=np.asarray(src)
    ret[~allow]=original[~allow]
    ret[:,:,3]=original[:,:,3]
    painted=Image.fromarray(ret,'RGBA')
    assert base.valid_pixels_only(src,painted)==0
    return painted,editable,Image.fromarray(repaired_rgba,'RGBA'),mask

def make_ora(src, painted, previous, layers, repaired, out):
    """ORA workmaster: visible exact CANON; unapproved candidate deliberately hidden."""
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'name':'CP404_CANON_LOCKED_UNAPPROVED','version':'0.0.1'})
    stack=ET.SubElement(root,'stack')
    named=[('CP404 BALANCED - HIDDEN',painted,False), ('CP402 PREVIOUS - HIDDEN',previous,False),
           *[(f'RETOUCH {k} - HIDDEN',v,False) for k,v in layers.items()],
           ('INPAINT SAME CANON - HIDDEN',repaired,False),
           ('CANON V2.1 (VISIBLE, DO NOT EDIT)',src,True)]
    with zipfile.ZipFile(out,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,img,visible) in enumerate(named):
            where=f'data/layer{i:02}.png'; buf=io.BytesIO(); img.save(buf,format='PNG');z.writestr(where,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':where,'opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
        buf=io.BytesIO(); src.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))

def review_board(src, prev, candidate1, candidate2, balanced, p):
    v=[('CANON / OPEN',src),('CP402 / OLDER DRAFT',prev),('CP404 / FEATHER DRAFT',candidate1),('CP404 / DEFINED DRAFT',candidate2),('CP404 / BALANCED DRAFT',balanced)]
    scale=4; pad=22; gap=16; top=102; tile_w=SIZE[0]*scale; tile_h=SIZE[1]*scale
    out=Image.new('RGB',(pad*2+tile_w*5+gap*4,top+tile_h+60),(19,33,47))
    d=ImageDraw.Draw(out)
    f='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font1=ImageFont.truetype(f,25);font2=ImageFont.truetype(f,14)
    d.text((pad,17),'CP404 / LAM THIEN / SOURCE-LOCKED EYELID ART STUDY',font=font1,fill=(244,244,246))
    d.text((pad,54),'NO RELEASE: New candidates are technical art drafts. Need direct user approval.',font=font2,fill=(250,193,166))
    d.text((pad,75),'CANON 941 x 1672 -> exact native 168 x 197 crop; zoom is for inspection only.',font=font2,fill=(216,222,235))
    for i,(label,img) in enumerate(v):
        x=pad+i*(tile_w+gap)
        out.paste(img.convert('RGB').resize((tile_w,tile_h),Image.Resampling.NEAREST),(x,top))
        d.text((x,top+tile_h+18),label,font=font2,fill=(255,255,255))
    out.save(p)

def run(canon,prev_path,out_dir):
    src=base.exact_source(canon)
    prev=Image.open(prev_path).convert('RGBA')
    if prev.size!=SIZE or base.valid_pixels_only(src,prev):raise ValueError('PREVIOUS_SOURCE_ROI_MISMATCH')
    a,layers,repaired,mask=compose_study(src,'feather')
    b,_,_,_=compose_study(src,'defined')
    orig=np.asarray(src)
    prior=np.asarray(prev).astype(float)
    defined=np.asarray(b).astype(float)
    composite=np.uint8(np.rint(np.clip(prior*.68+defined*.32,0,255)))
    allow=np.zeros((SIZE[1],SIZE[0]),dtype=bool)
    for x1,y1,x2,y2 in ROIS.values():allow[y1:y2,x1:x2]=True
    composite[~allow]=orig[~allow]
    composite[:,:,3]=orig[:,:,3]
    balanced=Image.fromarray(composite,'RGBA')
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    src.save(out/'CP404_SOURCE_CANON_EXACT.png');a.save(out/'CP404_FEATHER_DRAFT_NOT_APPROVED.png');b.save(out/'CP404_DEFINED_DRAFT_NOT_APPROVED.png');balanced.save(out/'CP404_BALANCED_DRAFT_NOT_APPROVED.png')
    review_board(src,prev,a,b,balanced,out/'CP404_COMPARE_CANON_CP402_DRAFTS.png')
    make_ora(src,balanced,prev,layers,repaired,out/'CP404_EYE_EDITABLE_8_LAYER_NOT_APPROVED.ora')
    # 15 positions: eyelid closure geometry from same source CP401.
    poses=[0,.15,.30,.45,.60,.75,.90,1,.90,.75,.60,.45,.30,.15,0]
    atlas=Image.new('RGBA',(SIZE[0]*15,SIZE[1]))
    for i,p in enumerate(poses):
        atlas.alpha_composite(base.eyelid_position(src,balanced,p),(SIZE[0]*i,0))
    atlas.save(out/'CP404_EYE_ATLAS_15_DRAFT_NOT_APPROVED.png')
    frames=base.render_sequence(src,balanced,72)
    # GIF/APNG preview at 30 fps, native RGBA frames.
    frames[0].save(out/'CP404_BLINK_PREVIEW_DRAFT.gif',save_all=True,append_images=frames[1:],duration=33,loop=0,optimize=False,disposal=2)
    frames[0].save(out/'CP404_BLINK_PREVIEW_DRAFT.apng.png',save_all=True,append_images=frames[1:],duration=33,loop=0,disposal=2)
    import cv2
    video=cv2.VideoWriter(str(out/'CP404_BLINK_COMPARISON_30FPS_DRAFT.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),30,(SIZE[0]*8,SIZE[1]*4))
    if not video.isOpened():raise RuntimeError('VIDEO_WRITER_NOT_AVAILABLE')
    source=np.asarray(src.convert('RGB').resize((SIZE[0]*4,SIZE[1]*4),Image.Resampling.BICUBIC))
    for im in frames:
        second=np.asarray(im.convert('RGB').resize((SIZE[0]*4,SIZE[1]*4),Image.Resampling.BICUBIC))
        video.write(cv2.cvtColor(np.concatenate([source,second],axis=1),cv2.COLOR_RGB2BGR))
    video.release()
    report={'checkpoint':'CP404','canon_sha256':SHA,'prev_sha256':sha(prev_path),'native_dimensions':list(SIZE),'roi':ROIS,'outside_roi_changed':base.valid_pixels_only(src,balanced),'closed_eye_art_user_approved':False,'style_art_qa':'PENDING_USER_REVIEW','rig_complete':False,'apk_runtime_tested':False,'production_sprite_paths':{},'atlas_sha256':sha(out/'CP404_EYE_ATLAS_15_DRAFT_NOT_APPROVED.png'),'closed_balanced_sha256':sha(out/'CP404_BALANCED_DRAFT_NOT_APPROVED.png'),'ora_sha256':sha(out/'CP404_EYE_EDITABLE_8_LAYER_NOT_APPROVED.ora'),'video_frames':len(frames),'fps':30,'note':'All CP404 variations remain visually unapproved; old CP402 should remain review baseline. No high-resolution original eyelid source has been painted.'}
    (out/'CP404_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--prev',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();print(json.dumps(run(args.canon,args.prev,args.out),indent=2))
#!/usr/bin/env python3
"""CP402: original-CANON eyelash-pigment guided retouch and blink preview.
This produces REVIEW ART ONLY. Not a painter-approved sprite or APK release.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Source lock and geometric eyelid closure are from the CP401 audited pipeline.
import cp401_occlusion_blink as cp401
CANON_SHA=cp401.CANON_SHA
SIZE=cp401.SIZE
ROIS=cp401.ROIS


def hashed(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def source_lash_color(src,side,x,pixels=None):
    """Find original dark lash-root pigment at the upper eyelid, never use foreign art."""
    a=np.asarray(src) if pixels is None else pixels
    y=cp401.curve(side,x,cp401.UPPER)
    x=int(np.clip(round(x),0,SIZE[0]-1))
    yy=np.arange(max(0,int(y)-3),min(SIZE[1],int(y)+5))
    candidates=a[yy,x,:3].astype(float)
    # Match dark, saturated original root and avoid bright iris/white pixels.
    score=.28*candidates[:,0]+.52*candidates[:,1]+.20*candidates[:,2]
    k=int(score.argmin()); color=candidates[k]
    # Bound color to dark warm source-root pigment, but retain variation in values.
    return tuple(int(v) for v in np.clip(.86*color+.14*np.array([74,40,55]),0,255))


def draw_refined_closed(source:Image.Image, variant='root'):
    """Composite source-root lashes over CP401 same-CANON inpainted eyelids.
    Retouches only the two authorized ROI rectangles.
    """
    if variant not in ('root','soft'):raise ValueError('BAD_VARIANT')
    closed=cp401.eyelid_art(source)
    original=np.asarray(source)
    base=np.asarray(closed).copy()
    S=8
    overlay=Image.new('RGBA',(SIZE[0]*S,SIZE[1]*S),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    for side,(x1,y1,x2,y2) in ROIS.items():
        xmin=x1+3; xmax=x2-3
        def pt(x,y):return (round(x*S),round(y*S))
        # Narrow wash two pixels above crease; spare corner pixels and preserve original eyebrows.
        for x in np.arange(xmin,xmax,.125):
            t=float((x-xmin)/(xmax-xmin))
            strength=max(0,math.sin(math.pi*t))**.78
            y=cp401.curve(side,x,cp401.CLOSED)
            color=source_lash_color(source,side,x,original)
            # Source-palette skin shadow, not a flat artificial black stroke.
            shadow=(int(.42*color[0]+.58*189),int(.42*color[1]+.58*118),int(.42*color[2]+.58*137),int(18*strength))
            r=.78
            d.ellipse((pt(x-r,y-2.1-r),pt(x+r,y-2.1+r)),fill=shadow)
        # Source-root graded lash band. Sharp outer roots + delicate tapered inner ends.
        for x in np.arange(xmin,xmax,.10):
            t=float((x-xmin)/(xmax-xmin))
            taper=max(0,math.sin(math.pi*t))**.5
            pigment=source_lash_color(source,side,x,original)
            y=cp401.curve(side,x,cp401.CLOSED)
            # eye's lateral edge is near x1 for LEFT, x2 for RIGHT
            edge=(1-t if side=='LEFT' else t)
            thick=(.28+.33*edge)*taper
            strength=(.47 if variant=='root' else .26)*taper
            for yy,weight in ((-.23,.55),(.14,1),(.48,.55)):
                a=int(255*strength*weight)
                d.ellipse((pt(x-thick,y+yy-thick),pt(x+thick,y+yy+thick)),fill=(*pigment,a))
        # Tapered individual lashes; thickness intentionally limited at native resolution.
        anchors=([.06,.13,.23] if side=='LEFT' else [.73,.83,.91])
        for index,t in enumerate(anchors):
            x,y=cp401.bez(cp401.CLOSED[side],t)
            dx=(-1 if side=='LEFT' else 1)*(.40+.12*index)
            dy=-.60-.10*index
            ink=source_lash_color(source,side,x,original)
            a=round((94 if variant=='root' else 62)*(1-.10*index))
            d.line([pt(x,y),pt(x+dx,y+dy)],fill=(*ink,a),width=2)
    paint=np.asarray(overlay.resize(SIZE,Image.Resampling.LANCZOS)).astype(float)
    # Guard all painting by ROIs. No source alpha alterations, no other features changed.
    for x1,y1,x2,y2 in ROIS.values():
        dst=base[y1:y2,x1:x2,:3].astype(float)
        p=paint[y1:y2,x1:x2]
        alpha=p[:,:,3:4]/255.
        base[y1:y2,x1:x2,:3]=np.uint8(np.rint(np.clip(dst*(1-alpha)+p[:,:,:3]*alpha,0,255)))
    base[:,:,3]=original[:,:,3]
    ret=Image.fromarray(base,'RGBA')
    if cp401.valid_pixels_only(source,ret)!=0:raise AssertionError('OUT_OF_EYE_MODIFICATION')
    return ret

def compare_board(src,root,soft,p):
    frames=[('CANON / UNCHANGED',src),('CP401 / DRAFT',cp401.eyelid_art(src)),('CP402 / SOURCE ROOT',root),('CP402 / SOFT ROOT',soft)]
    s=4; pad=22; top=89; gap=16; width=SIZE[0]*s
    out=Image.new('RGB',(2*pad+4*width+3*gap,top+SIZE[1]*s+54),(18,36,49))
    d=ImageDraw.Draw(out)
    f='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    d.text((pad,17),'CP402 | LAM THIEN | SAME-CANON EYELASH ROOT REVIEW',font=ImageFont.truetype(f,24),fill=(252,250,248))
    d.text((pad,51),'DRAFT - exact face pixels outside both eyes; source 168 x 197, not painted-HD master.',font=ImageFont.truetype(f,15),fill=(246,212,178))
    for i,(name,img) in enumerate(frames):
        x=pad+i*(width+gap);out.paste(img.convert('RGB').resize((width,SIZE[1]*s),Image.Resampling.NEAREST),(x,top))
        d.text((x,top+SIZE[1]*s+15),name,font=ImageFont.truetype(f,15),fill='white')
    out.save(p)

def run(canon,output):
    source=cp401.exact_source(canon)
    a=draw_refined_closed(source,'root');b=draw_refined_closed(source,'soft')
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    source.save(out/'CP402_EXACT_SOURCE_FACE.png')
    a.save(out/'CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png')
    b.save(out/'CP402_CLOSED_SOFT_CANDIDATE_NOT_APPROVED.png')
    compare_board(source,a,b,out/'CP402_CANON_CP401_ROOT_SOFT_REVIEW.png')
    # Use full CP401 geometric occlusion; data files are REVIEW ONLY.
    poses=[0,.15,.30,.45,.60,.75,.90,1.,.90,.75,.60,.45,.30,.15,0]
    atlas=Image.new('RGBA',(SIZE[0]*len(poses),SIZE[1]))
    for i,t in enumerate(poses):
        im=cp401.eyelid_position(source,a,t)
        if cp401.valid_pixels_only(source,im):raise AssertionError('EYE_ROI_BROKEN')
        atlas.alpha_composite(im,(i*SIZE[0],0))
    atlas.save(out/'CP402_ATLAS_ROOT_DRAFT_15.png')
    frames=cp401.render_sequence(source,a,72)
    # preview GIF only, full 72 frames in input are generated in memory (not committed as assets)
    smpl=[frames[i] for i in range(0,72,2)]
    smpl[0].save(out/'CP402_BLINK_ROOT_DRAFT.gif',save_all=True,append_images=smpl[1:],duration=67,loop=0,disposal=2,optimize=False)
    result={'checkpoint':'CP402','canon_sha256':CANON_SHA,'source_size':SIZE,'image_crop':cp401.CROP,
            'variants':['root','soft'],'atlas_frames':len(poses),'video_equivalent_frames':len(frames),
            'outside_roi_changed':cp401.valid_pixels_only(source,a),'closed_root_sha256':hashed(out/'CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png'),
            'atlas_sha256':hashed(out/'CP402_ATLAS_ROOT_DRAFT_15.png'),
            'visual_qa':'NOT_APPROVED','android_runtime_tested':False,'sprite_paths':{},
            'note':'pixel-level root-sourced retouch from same CANON; not artist-approved master'}
    (out/'CP402_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return result

if __name__=='__main__':
    ar=argparse.ArgumentParser();ar.add_argument('--canon',required=True);ar.add_argument('--out',required=True)
    cfg=ar.parse_args();print(json.dumps(run(cfg.canon,cfg.out),ensure_ascii=False,indent=2))
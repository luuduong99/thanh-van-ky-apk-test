#!/usr/bin/env python3
"""CP405 — exact CANON eye-local, editable subpixel painting candidate, NOT APPROVED.

This draws differentiated lid folds, skin shading, tapered lashes in separate
source-locked layers instead of simply applying a flat dark stroke. It does not
claim to recover hidden details or create a production hand-painted sprite.
"""
import io, json, zipfile, hashlib, math, argparse, sys
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cp401_occlusion_blink as base

SCALE = 16
FRAME_STEPS = [0,.12,.26,.42,.58,.74,.90,1,.90,.74,.58,.42,.26,.12,0]

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _source_and_underpaint(canon):
    source=base.exact_source(canon)
    a=np.array(source)
    mask=np.zeros(a.shape[:2],np.uint8)
    for side, (x1,y1,x2,y2) in base.ROIS.items():
        for x in range(x1+2,x2-2):
            u=base.curve(side,x,base.UPPER); l=base.curve(side,x,base.LOWER)
            yl=max(y1+1,math.floor(u-3.9)); yr=min(y2-1,math.ceil(l+6.1))
            mask[yl:yr,x]=255
    rgb=cv2.cvtColor(cv2.inpaint(cv2.cvtColor(a[:,:,:3],cv2.COLOR_RGB2BGR),mask,6,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
    blend=cv2.GaussianBlur(mask,(5,5),.7).astype(float)/255
    blend[mask==0]=0
    a[:,:,:3]=np.uint8(np.clip(np.rint(a[:,:,:3]*(1-blend[:,:,None])+rgb*blend[:,:,None]),0,255))
    return source,Image.fromarray(a,'RGBA'),mask

def _draw_paint_layers():
    width,height=base.SIZE
    names=['skin_plane_shadow','warm_lid_fold','upper_lash_core','individual_lash_tips','inner_corner_detail']
    pages={n:Image.new('RGBA',(width*SCALE,height*SCALE)) for n in names}
    pens={n:ImageDraw.Draw(v,'RGBA') for n,v in pages.items()}
    def xy(a,b):return (round(a*SCALE),round(b*SCALE))
    for side, (x1,y1,x2,y2) in base.ROIS.items():
        # Use SOURCE SAME CANON bezier, no portrait generation.
        closed=base.CLOSED[side]
        steps=[(float(t),*base.bez(closed,float(t))) for t in np.linspace(.045,.96,350)]
        # Layer 1: diffuse cheek/makeup in multiple passes. Gentle variation
        # mimics translucency rather than a binary shadow stripe.
        for t,x,y in steps:
            fall=math.sin(math.pi*t)**.75
            for shift,radius,rgba in [(-1.28,1.55,(170,87,107,12)),(1.30,1.45,(165,86,109,8)),(-2.3,1.15,(152,86,111,7))]:
                r=radius*(.62+.38*fall)
                pens['skin_plane_shadow'].ellipse((*xy(x-r,y+shift-r),*xy(x+r,y+shift+r)),fill=rgba[:3]+(round(rgba[3]*fall),))
        # Eyelid fold slightly higher, broken irregular pigmentation; do not
        # introduce an ink-pencil cartoon line above the lash roots.
        for j,(t,x,y) in enumerate(steps):
            if not .13<t<.87:continue
            fade=(math.sin(math.pi*t)**2)*(.78+.22*math.sin(j*1.17))
            if j%5==0:
                pens['warm_lid_fold'].ellipse((*xy(x-.38,y-2.15-.38),*xy(x+.38,y-2.15+.38)),fill=(135,78,99,round(30*fade)))
        # Main root: varies smoothly in width, pigment depth and warmth. Entire
        # line stays within eyebrow/eye ROI, confirmed by QA.
        for t,x,y in steps:
            outer=(1-t) if side=='LEFT' else t
            shape=max(0,math.sin(math.pi*t))**.52
            thick=(.48+.76*outer)*shape
            alpha=round((162+58*outer)*shape)
            # Deep warm violet/brown matches the CANON anime palette.
            pens['upper_lash_core'].ellipse((*xy(x-thick/2,y-thick/2),*xy(x+thick/2,y+thick/2)),fill=(60,37,58,alpha))
        # Real tapered separated tips. End starts within root and naturally
        # curves toward external corner. Stroke tapers to transparent 0.05px.
        anchors=np.linspace(.08,.88,19)
        for i,t in enumerate(anchors):
            x,y=base.bez(closed,float(t))
            outer=1-t if side=='LEFT' else t
            fade=math.sin(math.pi*t)**.6
            length=(.38+1.30*outer)*fade
            # Avoid uniform comb: deterministic, delicately alternating angles.
            tilt=(-.40 if side=='LEFT' else .40)*(.6+.45*outer)
            d=((i%5)-2)*.055
            endx=x+tilt*length+d
            endy=y+(.22+.82*outer)*length
            points=[(x+(endx-x)*u,y+(endy-y)*u-.10*math.sin(math.pi*u)) for u in np.linspace(0,1,14)]
            for j,(px,py) in enumerate(points):
                tip_width=(.29+.30*outer)*(1-j/13)**.83
                opacity=round(132*fade*(1-j/13)**.58)
                pens['individual_lash_tips'].ellipse((*xy(px-tip_width/2,py-tip_width/2),*xy(px+tip_width/2,py+tip_width/2)),fill=(72,44,65,opacity))
        # Corner detail: tear duct tiny warm matte highlight and outer soft taper.
        inner_t=.91 if side=='LEFT' else .09
        x,y=base.bez(closed,inner_t)
        pens['inner_corner_detail'].ellipse((*xy(x-.57,y+.18-.32),*xy(x+.57,y+.18+.32)),fill=(197,104,115,48))
    # Anti-alias and exact ROI lock after rasterizing. Clear outside ROI explicitly.
    allow=np.zeros((height,width),bool)
    for roi in base.ROIS.values():x1,y1,x2,y2=roi;allow[y1:y2,x1:x2]=True
    out={}
    for n,v in pages.items():
        native=np.array(v.resize(base.SIZE,Image.Resampling.LANCZOS))
        native[~allow]=0
        out[n]=Image.fromarray(native,'RGBA')
    return out

def draw_master(canon):
    src,under,mask=_source_and_underpaint(canon)
    layers=_draw_paint_layers()
    out=under.copy()
    for im in layers.values():out=Image.alpha_composite(out,im)
    a=np.asarray(src);b=np.asarray(out).copy()
    allow=np.zeros(a.shape[:2],bool)
    for x1,y1,x2,y2 in base.ROIS.values():allow[y1:y2,x1:x2]=True
    b[~allow]=a[~allow];b[:,:,3]=a[:,:,3]
    ret=Image.fromarray(b,'RGBA')
    assert base.valid_pixels_only(src,ret)==0
    return src,ret,under,layers

def make_ora(src,under,layers,closed,path):
    root=ET.Element('image',{'w':'168','h':'197','name':'CP405 SOURCE LOCKED ARTIST-DIRECTED DRAFT','version':'0.0.1'})
    stack=ET.SubElement(root,'stack')
    rows=[('CLOSED MASTER / DRAFT (HIDDEN)',closed,False)]+[(n+' / DRAFT (HIDDEN)',im,False) for n,im in layers.items()]+[('UNDERPAINT / DRAFT (HIDDEN)',under,False),('CANON V2.1 EXACT - VISIBLE',src,True)]
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(rows):
            buf=io.BytesIO();im.save(buf,format='PNG');loc=f'data/layer{i:02d}.png';z.writestr(loc,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':loc,'opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
        buf=io.BytesIO();src.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))

def review(src,baseline,closed,out):
    tiles=[('CANON / OPEN / APPROVED',src),('CP402 / ROOT / DRAFT',baseline),('CP405 / NEW PAINT / DRAFT',closed)]
    zoom=5;panel=base.SIZE[0]*zoom;ph=base.SIZE[1]*zoom;pad=22;gap=14;top=110
    im=Image.new('RGB',(2*pad+panel*3+2*gap,top+ph+46),(20,36,55));d=ImageDraw.Draw(im)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';h1=ImageFont.truetype(font,24);h2=ImageFont.truetype(font,14)
    d.text((pad,14),'CP405 / LAM THIEN / EXACT CANON EYE ART PASS',fill='white',font=h1)
    d.text((pad,48),'All candidates are DRAFT; no preview passes artist visual QA automatically.',fill=(255,196,154),font=h2)
    d.text((pad,70),'168x197 native source. 5x enlarged for inspecting eyelid pigments only.',fill=(191,212,231),font=h2)
    for i,(label,bitmap) in enumerate(tiles):
        left=pad+i*(panel+gap)
        im.paste(bitmap.convert('RGB').resize((panel,ph),Image.Resampling.NEAREST),(left,top))
        d.text((left,top+ph+12),label,fill='white',font=h2)
    im.save(out)

def build(canon,prev,out):
    dst=Path(out);dst.mkdir(exist_ok=True,parents=True)
    src,closed,under,layers=draw_master(canon)
    prior=Image.open(prev).convert('RGBA')
    if prior.size!=base.SIZE or base.valid_pixels_only(src,prior):raise ValueError('INVALID_PREVIOUS_BASELINE')
    src.save(dst/'CP405_CANON_EXACT.png');closed.save(dst/'CP405_CLOSED_EYE_DRAFT.png')
    make_ora(src,under,layers,closed,dst/'CP405_EYE_ART_8_LAYER_NOT_APPROVED.ora')
    review(src,prior,closed,dst/'CP405_CANON_CP402_NEW_REVIEW.png')
    poses=Image.new('RGBA',(168*15,197))
    for i,p in enumerate(FRAME_STEPS):poses.alpha_composite(base.eyelid_position(src,closed,p),(168*i,0))
    poses.save(dst/'CP405_15_POSE_ATLAS_NOT_APPROVED.png')
    seq=base.render_sequence(src,closed,72)
    seq[0].save(dst/'CP405_BLINK_DRAFT.gif',save_all=True,append_images=seq[1:],duration=33,loop=0,optimize=False,disposal=2)
    # 30 fps side-by-side source
    writer=cv2.VideoWriter(str(dst/'CP405_BLINK_30FPS_DRAFT.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),30,(168*8,197*4))
    if not writer.isOpened():raise ValueError('MP4_VIDEO_ENCODER_UNAVAILABLE')
    fix=np.asarray(src.convert('RGB').resize((168*4,197*4),Image.Resampling.BICUBIC))
    for frame in seq:
        moving=np.asarray(frame.convert('RGB').resize((168*4,197*4),Image.Resampling.BICUBIC))
        writer.write(cv2.cvtColor(np.concatenate([fix,moving],axis=1),cv2.COLOR_RGB2BGR))
    writer.release()
    a=np.asarray(src);b=np.asarray(closed)
    report={'checkpoint':'CP405','canon_sha':base.CANON_SHA,'native_size':[168,197],
        'changed_pixels':int(np.any(a!=b,axis=2).sum()),
        'outside_eye_changed':base.valid_pixels_only(src,closed),'native_alpha_exact':bool(np.array_equal(a[:,:,3],b[:,:,3])),
        'ora_layers':8,'atlas_frame_count':15,'animation_frames':72,'fps':30,
        'master_sha':sha(dst/'CP405_CLOSED_EYE_DRAFT.png'), 'atlas_sha':sha(dst/'CP405_15_POSE_ATLAS_NOT_APPROVED.png'),
        'keyframe_visual_approval':'PENDING', 'animation_visual_approval':'PENDING',
        'production_release':{'status':'blocked_pending_artist_and_user_approval','sprite_paths':{},'apk_ready':False},
        'important':'Do NOT use a generated black-haired CP405 completion infographic: it is not Lâm Thiển CANON and its completion checkmarks are false.'}
    (dst/'CP405_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--canon',required=True);parser.add_argument('--prev',required=True);parser.add_argument('--out',required=True)
    a=parser.parse_args(); print(json.dumps(build(a.canon,a.prev,a.out),ensure_ascii=False,indent=2))
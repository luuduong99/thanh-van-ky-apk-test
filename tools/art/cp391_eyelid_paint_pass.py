#!/usr/bin/env python3
"""CP391: source-locked, non-destructive eyelid/skin-shading draft.

This is *not* an artist-approved game sprite. The approved CANON is displayed
pixel-exact in the ORA and the new paint is hidden for human visual review.
"""
import argparse
import hashlib
import io
import json
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFont

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CROP = (25, 684, 193, 881)
WH = (168,197)
ROIS = {'LEFT':(31,94,70,124), 'RIGHT':(84,70,130,107)}
ART_NAMES = ['LEFT_SOFT_SHADOW', 'RIGHT_SOFT_SHADOW', 'LEFT_CREASE', 'RIGHT_CREASE', 'LEFT_TAPER_LASHES', 'RIGHT_TAPER_LASHES']


def load_canon(p):
    p=Path(p)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=CANON_SHA:
        raise ValueError('CANON_SHA_MISMATCH: do not use alternate character art')
    with Image.open(p) as im:
        if im.size!=(941,1672) or im.mode!='RGBA':
            raise ValueError('CANON_FORMAT_MISMATCH')
        return im.crop(CROP).copy()


def load_prev(p):
    p=Path(p)
    image=Image.open(p).convert('RGBA')
    if image.size!=WH:raise ValueError('CP390_SIZE_MISMATCH')
    return image


def roi_clip(im, side):
    arr=np.asarray(im.convert('RGBA')).copy()
    x1,y1,x2,y2=ROIS[side]
    keep=np.zeros((WH[1],WH[0]),dtype=bool)
    keep[y1:y2,x1:x2]=True
    arr[~keep,3]=0
    return Image.fromarray(arr,'RGBA')


def in_roi(im, side):
    a=np.asarray(im.getchannel('A'))
    x1,y1,x2,y2=ROIS[side]
    mask=np.zeros_like(a,dtype=bool);mask[y1:y2,x1:x2]=True
    return bool(np.count_nonzero(a[~mask])==0)


def bezier_points(p0,p1,p2,p3,n=64):
    t=np.linspace(0,1,n)
    return [((1-q)**3*p0[0]+3*(1-q)**2*q*p1[0]+3*(1-q)*q*q*p2[0]+q**3*p3[0],
             (1-q)**3*p0[1]+3*(1-q)**2*q*p1[1]+3*(1-q)*q*q*p2[1]+q**3*p3[1]) for q in t]


CURVES={
    'LEFT': [(32.0,109.0),(41.0,103.0),(54.0,99.8),(64.7,102.4)],
    'RIGHT':[(85.5,87.9),(96.0,79.2),(108.6,76.7),(121.7,80.4)]
}


def shadow_layer(side):
    # Localized, hand-shaped translucent eyelid shadow. No source pixels overwritten.
    a=np.zeros((WH[1],WH[0],4),dtype=np.uint8)
    coords=bezier_points(*CURVES[side],64)
    yy,xx=np.mgrid[:WH[1],:WH[0]]
    dist=np.full((WH[1],WH[0]),np.inf,dtype=np.float32)
    for x,y in coords:
        dist=np.minimum(dist,(xx-x)**2+((yy-(y+2.2))/.85)**2)
    gaussian=np.exp(-dist/(2*2.6**2))
    # Dark pink edge contour / soft pigment, bounded by eye ROI.
    a[:,:,:3]=[123,68,92]
    a[:,:,3]=np.clip(gaussian*48,0,55).astype(np.uint8)
    return roi_clip(Image.fromarray(a,'RGBA'),side)


def make_pen_layer(side, kind):
    S=8
    out=Image.new('RGBA',(WH[0]*S,WH[1]*S),(0,0,0,0))
    draw=ImageDraw.Draw(out)
    path=bezier_points(*CURVES[side],n=88)
    def p(x):return round(x*S)
    if kind=='CREASE':
        # A muted crease gliding above the primary lash line.
        shifted=[(p(x),p(y-2.8)) for x,y in path[4:-5]]
        draw.line(shifted, fill=(134,77,96,92),width=3)
        # a soft highlight immediately above fold
        draw.line([(p(x),p(y-4.0)) for x,y in path[10:-9]],fill=(255,228,214,58),width=3)
    elif kind=='TAPER_LASHES':
        # Short, individual pointed lashes with manually controlled taper.
        draw.line([(p(x),p(y)) for x,y in path], fill=(66,39,53,148),width=5)
        # Small highlight tracing the lower lash edge for dimension.
        draw.line([(p(x),p(y+.6)) for x,y in path[8:-9]],fill=(204,119,122,76),width=3)
        for i,q in enumerate(np.linspace(.12,.9,11)):
            j=int(q*(len(path)-1))
            x,y=path[j]
            x2,y2=path[min(j+3,len(path)-1)]
            vx,vy=(x2-x,y2-y)
            length=(vx*vx+vy*vy)**.5 or 1
            outward=(vx/length,vy/length)
            # eye surface slightly downward, tip moves outward depending on position
            tip=(x+outward[0]*(.4+.5*q), y+1.0+(0.65 if i%2 else 0.25))
            # tapered triangle rather than a uniform vertical line
            root=[(p(x-.42),p(y-.22)),(p(x+.42),p(y+.12)),(p(tip[0]),p(tip[1]))]
            draw.polygon(root,fill=(61,35,53,105 if i%3 else 84))
        # lash-corner tips are longest near outer edge
        x,y=path[-2]
        draw.line((p(x-0.2),p(y),p(x+1.4),p(y+0.45)),fill=(64,36,55,142),width=3)
    else:raise ValueError(kind)
    return roi_clip(out.resize(WH,Image.Resampling.LANCZOS),side)


def paint_layers():
    layers={}
    for s in ('LEFT','RIGHT'):
        layers[f'{s}_SOFT_SHADOW']=shadow_layer(s)
        layers[f'{s}_CREASE']=make_pen_layer(s,'CREASE')
        layers[f'{s}_TAPER_LASHES']=make_pen_layer(s,'TAPER_LASHES')
    for name,im in layers.items():
        side=name.split('_')[0]
        assert in_roi(im,side),f'{name}: strokes escape eye ROI'
        assert im.getchannel('A').getbbox(),f'{name}: empty painting'
    return layers


def compose(src,prior,layers):
    # compare a CP391 proposed *closed-eye* frame with the prior CP390 draft.
    output=prior.copy()
    for name in ART_NAMES:
        output.alpha_composite(layers[name])
    return output


def png_data(im):
    f=io.BytesIO();im.save(f,format='PNG');return f.getvalue()


def make_ora(src,prior,layers,candidate,path):
    # Canon open-eye is the ONLY visible layer; every unapproved image remains hidden.
    images=[('LÂM THIỂN / CANON V2.1 / EYES OPEN / ORIGINAL PIXELS',src,'visible'),
            ('CP390 CLOSED-EYE BASE / DRAFT / HIDDEN',prior,'hidden')]
    images.extend((f'CP391 {k} / DRAFT / HIDDEN',layers[k],'hidden') for k in ART_NAMES)
    images.append(('CP391 CLOSED-EYE COMPOSITE / UNAPPROVED',candidate,'hidden'))
    root=ET.Element('image',w=str(WH[0]),h=str(WH[1]),name='CP391 Lâm Thiển source-locked eyelid paint study',version='0.0.3')
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,vis) in enumerate(images):
            layer_path=f'data/layer_{i:02d}.png'
            z.writestr(layer_path,png_data(im))
            ET.SubElement(stack,'layer',{'name':name,'src':layer_path,'opacity':'1.0','visibility':vis,'x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',png_data(src))
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:raise AssertionError('ORA_ZIP_CRC_FAIL')
        assert len(ET.fromstring(z.read('stack.xml')).find('stack'))==len(images)
    return len(images)


def make_preview(src,prior,candidate,path):
    W,H=1540,845
    board=Image.new('RGB',(W,H),(18,38,60))
    d=ImageDraw.Draw(board)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    f=ImageFont.truetype(font,20)
    small=ImageFont.truetype(font,14)
    d.text((20,12),'TVK CP391 | Lâm Thiển - CANON-locked eyelid paint trial',font=f,fill='#FAFCFF')
    d.text((20,48),'Only approved CANON V2.1 / new closed-eye draft NOT APPROVED / no game sprite',font=small,fill='#F9D6B7')
    for i,(name,im) in enumerate([('01  CANON V2.1 / source exact',src),('02  CP390 / closed-eye prior draft',prior),('03  CP391 / additional lash, crease, shadow DRAFT',candidate)]):
        x=18+i*510
        b=im.resize((476,559),Image.Resampling.NEAREST).convert('RGB')
        board.paste(b,(x,86))
        d.text((x,653),name,font=small,fill='#FFFFFF')
    d.text((20,714),'The original open-eye CANON is preserved byte-for-byte. New eye paint is hidden in ORA.',font=small,fill='#EFF7FD')
    d.text((20,744),'Visual QA: NOT PASSED / no painter-quality skin underpaint / no Spine, Android integration or APK.',font=small,fill='#FFD5AF')
    board.save(path)


def generate(canon_path, cp390_path, output):
    src=load_canon(canon_path)                 # reject wrong reference *before* creating output
    prior=load_prev(cp390_path)
    layers=paint_layers()
    candidate=compose(src,prior,layers)
    a=np.asarray(src);b=np.asarray(candidate)
    outside=np.ones((WH[1],WH[0]),dtype=bool)
    for x1,y1,x2,y2 in ROIS.values():outside[y1:y2,x1:x2]=False
    outside_changed=int(np.count_nonzero(np.any(a[outside]!=b[outside],axis=1)))
    if outside_changed:raise AssertionError('PAINT_OUTSIDE_APPROVED_EYE_REGIONS')
    p=Path(output);(p/'art').mkdir(parents=True,exist_ok=True);(p/'qa').mkdir(parents=True,exist_ok=True)
    shutil.copyfile(canon_path,p/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    src.save(p/'CANON_SHY_OPEN_PIXEL_EXACT.png')
    prior.save(p/'CP390_CLOSED_EYE_PRIOR_DRAFT.png')
    candidate.save(p/'CP391_CLOSED_EYE_ART_DRAFT_NOT_APPROVED.png')
    for k,im in layers.items(): im.save(p/'art'/f'{k}_CP391_DRAFT.png')
    ora=p/'CP391_EYELID_PAINTER_STUDY_CANON_VISIBLE_NOT_APPROVED.ora'
    layer_n=make_ora(src,prior,layers,candidate,ora)
    make_preview(src,prior,candidate,p/'qa'/'CP391_CANON_CP390_CP391_ACTUAL_SOURCE_COMPARE.png')
    report={
        'checkpoint':'CP391','canon_sha256':CANON_SHA,'source_crop_xyxy':list(CROP),
        'open_eyes_preserved_exact_pixels':True,'source_canon_preserved_exact_bytes':hashlib.sha256((p/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes()).hexdigest()==CANON_SHA,
        'new_independent_native_paint_layers':ART_NAMES,'ora_layers':layer_n,
        'new_paint_alpha_pixels':{k:int(np.count_nonzero(np.array(v.getchannel('A')))) for k,v in layers.items()},
        'closed_eye_changes_inside_eye_roi':int(np.count_nonzero(np.any(a[~outside]!=b[~outside],axis=1))),
        'changed_pixels_outside_eye_roi':outside_changed,
        'uses_only_approved_canon_and_historical_drafts':True,
        'no_unverified_generated_concept_art_in_artifact':True,
        'visual_qa':'NOT_PASSED','artist_approval':False,
        'limitations':'New shadow/crease/lashes are raster linework studies on a native 168x197 source; no painter-quality hidden anatomy, no eye-closed ground truth. Counts do not certify fidelity. Not a rig or frame-ready animation.',
        'release':{'status':'blocked_pending_art','sprite_paths':{},'spine_ready':False,'apk_ready':False},
        'next':'CP392: independent human-quality eyelid and hidden-skin painting accepted against CANON before blink keyframes, animation or Android APK.'
    }
    (p/'CP391_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--canon',required=True);ap.add_argument('--cp390',required=True);ap.add_argument('--out',required=True)
    args=ap.parse_args()
    print(json.dumps(generate(args.canon,args.cp390,args.out),ensure_ascii=False,indent=2))
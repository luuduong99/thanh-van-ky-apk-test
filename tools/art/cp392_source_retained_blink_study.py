#!/usr/bin/env python3
"""TVK CP392: source-retaining narrow-eye occlusion study, NOT approved art.

Exactly preserves Lâm Thiển V2.1 source in visible ORA layer, obtains all
replacement skin colors from that SAME portrait and preserves its existing
CANON eyelash contours. The 'near closed' variant is NOT a completed blink.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, shutil, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CP391_SHA = '24787edd37449346d0c6a97bc6a3cd06e2f4bfc8a093d21acbf6cb435d32acac'
CROP = (25, 684, 193, 881)
SIZE = (168, 197)
ROIS = {'LEFT': (31, 94, 70, 124), 'RIGHT': (84, 70, 130, 107)}
# Same face, same left/right eye outlines; these landmarks are geometric STUDY marks.
LIDS = {
 'LEFT': ((32., 109.), (40., 102.2), (56., 101.), (66., 104.)),
 'RIGHT': ((85., 91.), (95., 82.), (110., 78.), (123., 82.))
}
VARIANTS = {'gentle': (2.0, 9.5, .70), 'near_closed': (-.50, 11.0, .60)}
PUBLISHED_RELEASE = {'status': 'blocked_pending_art', 'sprite_paths': {}, 'spine_ready': False, 'apk_ready': False}


def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_checked(canon_path, prior_path):
    # Reject alternate art *before* creating an output directory or writing artifacts.
    if sha256(canon_path) != CANON_SHA: raise ValueError('CANON_SHA_MISMATCH')
    if sha256(prior_path) != CP391_SHA: raise ValueError('CP391_HISTORY_SHA_MISMATCH')
    with Image.open(canon_path) as x:
        if x.size != (941, 1672) or x.mode != 'RGBA': raise ValueError('CANON_SIZE_OR_MODE_MISMATCH')
        source = x.crop(CROP).copy()
    with Image.open(prior_path) as x:
        if x.size != SIZE: raise ValueError('CP391_HISTORY_SIZE_MISMATCH')
        prior = x.convert('RGBA').copy()
    return source, prior


def bezier(p, count=96):
    p0, p1, p2, p3 = [np.asarray(x, dtype=float) for x in p]
    result=[]
    for t in np.linspace(0, 1, count):
        result.append((tuple(((1-t)**3*p0 + 3*(1-t)**2*t*p1 + 3*(1-t)*t*t*p2 + t**3*p3).tolist())))
    return result


def alpha_mask(side, variant):
    # Antialiased hand-placed patch under the original lash line.
    # It does not reconstruct hidden eyelid anatomy or invent source details.
    above, below, blur = VARIANTS[variant]
    S=8
    mask=Image.new('L',(SIZE[0]*S,SIZE[1]*S),0)
    draw=ImageDraw.Draw(mask)
    line=bezier(LIDS[side])
    polygon=[(round(x*S),round((y+above)*S)) for x,y in line]
    polygon += [(round(x*S),round((y+below)*S)) for x,y in reversed(line)]
    draw.polygon(polygon,fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(radius=blur*S)).resize(SIZE,Image.Resampling.LANCZOS)
    data=np.array(mask)
    x1,y1,x2,y2=ROIS[side]
    limited=np.zeros_like(data)
    limited[y1:y2,x1:x2]=data[y1:y2,x1:x2]
    return limited


def donor_pixels(source, shift=13):
    # A deterministic locally sampled cheek region within the *same* source,
    # unlike unverified generated character art or CP391 inpainting patches.
    source=np.asarray(source, dtype=np.uint8)
    ys=np.minimum(np.arange(SIZE[1])+shift, SIZE[1]-1)
    return source[ys, :].copy()


def overlay(src, side, variant):
    skin=donor_pixels(src)
    alpha=alpha_mask(side, variant)
    patch=skin.copy()
    patch[...,3]=alpha
    return Image.fromarray(patch,'RGBA')


def candidate(src, side_layers):
    result=src.copy()
    for part in ('LEFT','RIGHT'):
        result.alpha_composite(side_layers[part])
    return result


def changed_outside(a,b):
    mask=np.ones((SIZE[1],SIZE[0]),dtype=bool)
    for x1,y1,x2,y2 in ROIS.values(): mask[y1:y2,x1:x2]=False
    return int(np.count_nonzero(np.any(np.asarray(a)[mask] != np.asarray(b)[mask],axis=1)))


def pngbytes(im):
    stream=io.BytesIO(); im.save(stream,format='PNG');return stream.getvalue()


def create_ora(src,prior,patches,variants,path):
    layers=[('CANON V2.1 / SHY / EXACT / ONLY VISIBLE',src,True),
            ('CP391 HISTORY / NOT APPROVED',prior,False)]
    for variant in VARIANTS:
        for side in ('LEFT','RIGHT'):
            layers.append((f'CP392 {variant} {side} / CANON CHEEK-SAMPLED PATCH / DRAFT',patches[variant][side],False))
    for variant in VARIANTS:
        layers.append((f'CP392 {variant} / COMPOSITE / NOT APPROVED',variants[variant],False))
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'name':'CP392 source-preserving CANON eyelid study','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(layers):
            srcname=f'data/layer_{i:02d}.png'
            z.writestr(srcname,pngbytes(im))
            ET.SubElement(stack,'layer',{'name':name,'src':srcname,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',pngbytes(src))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        assert len(ET.fromstring(z.read('stack.xml')).find('stack'))==len(layers)
    return len(layers)


def preview(src,prior,variants,path):
    scale=3; W,H=SIZE; left=22; top=95; gap=12
    width=left*2+4*W*scale+gap*3
    canvas=Image.new('RGB',(width,760),(14,34,55))
    draw=ImageDraw.Draw(canvas)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    header=ImageFont.truetype(font,21);small=ImageFont.truetype(font,13)
    draw.text((22,15),'TVK CP392 | Lâm Thiển / verified CANON V2.1 / eyelash-retaining skin occlusion',font=header,fill='#FFFFFF')
    draw.text((22,48),'Study only: this is NOT a finished closed-eye master, animation or APK asset.',font=small,fill='#FFDFA6')
    cards=[('01  CANON V2.1 / source exact',src),('02  CP391 / older draft',prior),('03  CP392 / gentle partial',variants['gentle']),('04  CP392 / near-closed DRAFT',variants['near_closed'])]
    for i,(lab,im) in enumerate(cards):
        x=left+i*(W*scale+gap)
        canvas.paste(im.convert('RGB').resize((W*scale,H*scale),Image.Resampling.NEAREST),(x,top))
        draw.text((x,top+H*scale+12),lab,font=small,fill='#FFFFFF')
    draw.text((22,top+H*scale+43),'Preserves eye-open CANON exactly. Uses skin samples from the same portrait; both eye patches remain separate in the ORA.',font=small,fill='#DEEAF3')
    draw.text((22,top+H*scale+64),'Artist approval: NOT PASSED. Near-closed still retains the source lash contour and is not a genuinely new full-closure drawing.',font=small,fill='#FFDFA6')
    canvas.save(path)


def generate(canon,previous,output):
    src,prior=load_checked(canon,previous)
    patches={};variants={}
    for variant in VARIANTS:
        patches[variant]={side:overlay(src,side,variant) for side in ('LEFT','RIGHT')}
        variants[variant]=candidate(src,patches[variant])
    if any(changed_outside(src,x)!=0 for x in variants.values()):raise AssertionError('OUTSIDE_EYE_REGION_CHANGED')
    output=Path(output)
    (output/'art').mkdir(parents=True,exist_ok=True)
    (output/'qa').mkdir(parents=True,exist_ok=True)
    shutil.copyfile(canon,output/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    src.save(output/'CANON_SHY_SOURCE_PIXEL_EXACT.png')
    prior.save(output/'CP391_HISTORICAL_DRAFT.png')
    for v in VARIANTS:
        for side in ('LEFT','RIGHT'):
            patches[v][side].save(output/'art'/f'{v}_{side}_CHEEK_SAMPLE_PATCH.png')
        variants[v].save(output/f'CP392_{v.upper()}_DRAFT_NOT_APPROVED.png')
    ora=output/'CP392_EYELASH_RETAINED_SKIN_PATCH_EDITABLE_NOT_APPROVED.ora'
    n=create_ora(src,prior,patches,variants,ora)
    preview(src,prior,variants,output/'qa'/'CP392_SOURCE_REAL_CANON_AND_TWO_BLINK_VARIANTS.png')
    a=np.asarray(src)
    changed={v:int(np.count_nonzero(np.any(a!=np.asarray(im),axis=2))) for v,im in variants.items()}
    diff=int(np.count_nonzero(np.any(np.asarray(variants['gentle'])!=np.asarray(variants['near_closed']),axis=2)))
    result={
      'checkpoint':'CP392','exact_canon_sha256':CANON_SHA,'cp391_history_sha256':CP391_SHA,
      'source_dimensions':list(SIZE),'original_sheet_dimensions':[941,1672],
      'only_source_character':'Lâm Thiển V2.1','source_eyelash_contours_retained':True,
      'method':'hand-aligned narrow occlusion masks, skin color sampled from +13px cheek in the same original portrait; NOT painter-master redraw',
      'draft_variants':list(VARIANTS),'pixels_changed_from_source':changed,
      'pixels_differ_between_variants':diff,'pixels_changed_outside_eye_roi':{v:changed_outside(src,im) for v,im in variants.items()},
      'ora_layers':n,'original_open_eye_exact_in_ora':True,
      'visual_qa':'NOT_PASSED','artist_approval':False,
      'limitations':'Native 168x197; image quality inspection is subjective; near-closed variant is a technical partial lid closure, not complete painter-grade hidden-skin and blink animation. No real-time FPS/Spine/APK test.',
      'release':PUBLISHED_RELEASE,
      'next':'CP393: hand-paint a real closed-eye lid/underpaint matching source CANON; acceptance preview before animation.'}
    (output/'CP392_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--canon',required=True);p.add_argument('--cp391',required=True);p.add_argument('--out',required=True)
    args=p.parse_args()
    print(json.dumps(generate(args.canon,args.cp391,args.out),ensure_ascii=False,indent=2))
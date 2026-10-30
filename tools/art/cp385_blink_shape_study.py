#!/usr/bin/env python3
"""CP385 Lâm Thiển V2.1 blink shape study: source-faithful static face, DRAFT closed eyes.
No claim of finished painter-grade art, animation, usable transparent sprites or APK.
"""
from pathlib import Path
import argparse, hashlib, io, json, math, shutil, zipfile, xml.etree.ElementTree as ET
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE=(941,1672)
BBOX=(25,684,193,881)
SIZE=(168,197)
# Manual tighter local eyelid polygons; NOT approved artist semantic masks.
EYES={
 'left_eye':[(28,104),(32,100),(41,97),(57,95),(69,98),(69,104),(63,111),(54,115),(37,116),(29,110)],
 'right_eye':[(86,89),(89,81),(98,75),(114,72),(127,73),(129,78),(123,86),(113,92),(96,96),(87,94)],
}
MOUTH=[(72,121),(77,119),(89,122),(95,126),(93,132),(79,134),(73,131)]

def validate(canon):
    src=Path(canon)
    if hashlib.sha256(src.read_bytes()).hexdigest()!=CANON_SHA:
        raise ValueError('CANON_SHA_MISMATCH; no output directory created')
    with Image.open(src) as im:
        if im.mode!='RGBA' or im.size!=CANON_SIZE:
            raise ValueError('CANON_FORMAT_MISMATCH')
        return im.crop(BBOX).copy()

def part_mask(shape, points):
    mask=np.zeros((shape[1],shape[0]),np.uint8)
    cv2.fillPoly(mask,[np.array(points,np.int32)],255)
    return Image.fromarray(mask,'L')

def build_underpaint(img, masks):
    src=np.asarray(img)
    # Inpaint one tightened eye shape at a time. Avoid removing mouth/brow/other source.
    base=src[:,:,:3].copy()
    for k in ['left_eye','right_eye','mouth']:
        mask=np.array(masks[k])
        base=cv2.cvtColor(cv2.inpaint(cv2.cvtColor(base,cv2.COLOR_RGB2BGR),mask,2,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
    return Image.fromarray(np.dstack([base,src[:,:,3]]),'RGBA')

def cutout(img, mask):
    a=img.copy();a.putalpha(mask);return a

def lid_layer(side, amount):
    """Manually authored eyelid curves in native crop coordinates; test-only. 
    amount 0..1, only >0 draws a closure line, not authentic artist animation.
    """
    scale=4
    canvas=Image.new('RGBA',(SIZE[0]*scale,SIZE[1]*scale),(0,0,0,0))
    if amount<=0:return canvas.resize(SIZE)
    d=ImageDraw.Draw(canvas)
    if side=='left':
        coords=[(35.2,106.1),(41,103.0),(48,101.7),(55.5,101.0),(63.0,99.8)]
        accent=[(36.8,108.1),(43.8,105.9),(52.5,104.8),(60,103.9)]
        lashes=[((35.8,106), (33.5,107)),((39,104.5),(36.3,104.6)),((62.6,100),(65.0,98.5))]
    else:
        coords=[(90,88.2),(95.5,84.5),(102,81.2),(112.5,79.0),(122,77.9)]
        accent=[(92,90.0),(99.5,85.8),(109,82.4),(119,80.3)]
        lashes=[((121,78),(125,75.8)),((119,78.4),(122,76.1)),((91,88),(88.2,89.6))]
    # blend from a faint traced lid to the full lid for three study states.
    primary_alpha=int(230*amount)
    outer_alpha=int(126*amount)
    def pts(arr):return [(round(x*scale),round(y*scale)) for x,y in arr]
    d.line(pts(accent),fill=(232,135,137,outer_alpha),width=max(1,round(1.75*scale)),joint='curve')
    d.line(pts(coords),fill=(101,52,66,primary_alpha),width=max(1,round(1.45*scale)),joint='curve')
    for a,b in lashes: d.line(pts([a,b]),fill=(89,45,60,int(190*amount)),width=max(1,round(0.70*scale)))
    return canvas.resize(SIZE,Image.Resampling.LANCZOS)

def compose(base, mouth, left, right, left_lid=None,right_lid=None):
    img=base.copy();img.alpha_composite(mouth)
    if left is not None:img.alpha_composite(left)
    if right is not None:img.alpha_composite(right)
    if left_lid is not None:img.alpha_composite(left_lid)
    if right_lid is not None:img.alpha_composite(right_lid)
    return img

def render_frame(base,mouth,eye_parts,amount):
    # For half-open frames, source eye part is attenuated; only a review device.
    def fade(img,amount):
        a=img.copy();a.putalpha(Image.fromarray((np.asarray(a.getchannel('A'))*(1-amount)).astype('uint8')));return a
    return compose(base,mouth,fade(eye_parts['left_eye'],amount),fade(eye_parts['right_eye'],amount),lid_layer('left',amount),lid_layer('right',amount))

def ora_write(path, parts, static, guide):
    xroot=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'name':'CP385 source-preserved static + unapproved blink','version':'0.0.3'})
    stack=ET.SubElement(xroot,'stack')
    layer_spec=[
      ('source_mouth_visible',parts['mouth'],True),
      ('source_right_eye_visible',parts['right_eye'],True),
      ('source_left_eye_visible',parts['left_eye'],True),
      ('closed_left_lid_DRAFT_HIDDEN',lid_layer('left',1),False),
      ('closed_right_lid_DRAFT_HIDDEN',lid_layer('right',1),False),
      ('skin_underlay_TECH_INPAINT_NOT_APPROVED',parts['underlay'],True),
      ('exact_CANON_168x197_HIDDEN',guide,False),
    ]
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(layer_spec):
            filename=f'data/layer_{i:02d}.png';buf=io.BytesIO();im.save(buf,format='PNG');z.writestr(filename,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':filename,'visibility':'visible' if visible else 'hidden',
                'opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(xroot,encoding='utf8',xml_declaration=True))
        buf=io.BytesIO();static.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
    return len(layer_spec)

def make(canon,old_base,out):
    guide=validate(canon)
    old=Image.open(old_base).convert('RGBA')
    if old.size!=SIZE:raise ValueError('CP384 base size wrong')
    # only after preflight, create outputs
    root=Path(out)
    for d in ['layers','frames','qa','source']: (root/d).mkdir(parents=True,exist_ok=True)
    masks={k:part_mask(SIZE,p) for k,p in {**EYES,'mouth':MOUTH}.items()}
    underlay=build_underpaint(guide,masks)
    parts={k:cutout(guide,m) for k,m in masks.items()}
    parts['underlay']=underlay
    exact=compose(underlay,parts['mouth'],parts['left_eye'],parts['right_eye'])
    if not np.array_equal(np.asarray(exact),np.asarray(guide)):
        raise RuntimeError('STATIC_PIXEL_EXACT_FAILURE')
    shutil.copyfile(canon,root/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    guide.save(root/'source'/'SHY_CANON_168x197_EXACT.png')
    for k,m in masks.items():
        m.save(root/'layers'/f'{k}_mask.png')
        parts[k].save(root/'layers'/f'{k}_SOURCE_PIXEL_CUTOUT.png')
    underlay.save(root/'layers'/'skin_underlay_TECH_NOT_APPROVED.png')
    for side in EYES:lid_layer(side.split('_')[0],1).save(root/'layers'/f'{side}_closed_lid_DRAFT.png')
    exact.save(root/'CP385_CANON_PIXEL_EXACT_STATIC_FACE.png')
    # Five-frame QA, open -> partial -> closed -> partial -> open
    seq=[0,.55,1,.55,0]
    frames=[]
    for i,v in enumerate(seq):
        f=guide.copy() if v==0 else render_frame(underlay,parts['mouth'],parts,v)
        f.save(root/'frames'/f'CP385_BLINK_FRAME_{i:02}_DRAFT.png');frames.append(f)
    # Pixel identity of open endpoints and visible source outside new masks
    assert np.array_equal(np.asarray(frames[0]),np.asarray(guide))
    assert np.array_equal(np.asarray(frames[-1]),np.asarray(guide))
    mask_union=np.maximum.reduce([np.asarray(m) for m in masks.values()])>0
    old_delta=np.abs(np.asarray(old).astype(np.int16)-np.asarray(guide).astype(np.int16))[:,:,:3]
    new_delta=np.abs(np.asarray(underlay).astype(np.int16)-np.asarray(guide).astype(np.int16))[:,:,:3]
    affected_old=int(np.count_nonzero(np.any(old_delta>0,axis=2)))
    affected_new=int(np.count_nonzero(np.any(new_delta>0,axis=2)))
    untouched_outside=int(np.count_nonzero(np.any(new_delta[~mask_union,:]>0,axis=1)))
    report={
      'checkpoint':'CP385','canon_sha256':CANON_SHA,'portrait_size':list(SIZE),
      'source_exact_static':True,'open_frame_0_4_exact':True,'eye_polygons_localized':True,
      'old_underpaint_changed_pixels':affected_old,'new_underpaint_changed_pixels':affected_new,
      'new_changes_outside_eye_and_mouth_masks':untouched_outside,
      'five_frame_draft_sequence':seq,
      'ora_layers':ora_write(root/'CP385_SHY_SOURCE_AND_BLINK_DRAFT_NOT_RIG.ora',parts,exact,guide),
      'source_canvas_native_hd':False,'background_transparent':False,
      'blink_artist_approved':False,'inpaint_artist_approved':False,'visual_qa':'NOT_PASSED',
      'spine_ready':False,'apk_ready':False,'sprite_paths':{},'production_release':'blocked_pending_art',
      'notes':['Eye masks are new hand-bounded technical polygons, not validated painted semantic eye rigs.',
        'Do not fill missing eyelid areas with a generalized patch and call it artist-grade painting.',
        'Frames .55 and 1.0 are technical guides and must not be imported into game.',
        'Canvas native source is only 168x197 and has infographic background; no Android runtime test.']}
    # Preview using the exact CANON and same-character derivatives only.
    board=Image.new('RGB',(1460,560),(19,37,59));dr=ImageDraw.Draw(board)
    labels=['01 APPROVED CANON','02 CP384 BLINK DRAFT','03 CP385 BLINK DRAFT','04 CP385 STATIC EXACT']
    old_eyes=Image.open(root/'source'/'SHY_CANON_168x197_EXACT.png').convert('RGBA') # compare prev below
    oldblink=Image.open(root/'source'/'SHY_CANON_168x197_EXACT.png').convert('RGBA')
    # previous technical blink optional is not a required source because comparison is QA only
    previous_blink=Path(old_base).parent.parent/'qa'/'CP384_BLINK_TECHNICAL_DRAFT_NOT_APPROVED.png'
    if previous_blink.exists():oldblink=Image.open(previous_blink).convert('RGBA')
    samples=[guide,oldblink,frames[2],exact]
    for i,(im,label) in enumerate(zip(samples,labels)):
        x=22+i*360
        dr.text((x,23),label,fill=(236,245,255))
        view=im.resize((322,377),Image.Resampling.NEAREST)
        bg=Image.new('RGB',(322,377),'#eaf1f8');bg.paste(view,(0,0),view.getchannel('A'))
        board.paste(bg,(x,65))
    dr.text((24,475),'All figures are sourced from the user-approved Lam Thien V2.1 CANON. Blink layers are UNAPPROVED.',fill=(255,216,170))
    dr.text((24,508),'Static face is exactly preserved. Technical underpaint and blink need an artist review; NO APK / NO Spine.',fill=(255,216,170))
    board.save(root/'qa'/'CP385_CANON_VS_BLINK_DRAFT.png')
    flip=[im.resize((336,394)) for im in frames]
    flip[0].save(root/'qa'/'CP385_FIVE_FRAME_TECH_BLINK.gif',save_all=True,append_images=flip[1:],duration=[320,90,130,90,480],loop=0,disposal=2)
    (root/'CP385_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--canon',required=True);p.add_argument('--cp384-base',required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    print(json.dumps(make(a.canon,a.cp384_base,a.out),ensure_ascii=False,indent=2))
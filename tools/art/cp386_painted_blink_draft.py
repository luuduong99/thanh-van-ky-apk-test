#!/usr/bin/env python3
"""TVK CP386: source-exact CANON open face + editable artist-guided closed-eye TECH draft.

No painter-grade art claim, no full rig. Entire source image must match approved SHA.
"""
from pathlib import Path
import argparse, hashlib, json, io, shutil, zipfile, xml.etree.ElementTree as ET
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BBOX=(25,684,193,881)
EYES={
 'left':[(28,104),(32,100),(41,97),(57,95),(69,98),(69,104),(63,111),(54,115),(37,116),(29,110)],
 'right':[(86,89),(89,81),(98,75),(114,72),(127,73),(129,78),(123,86),(113,92),(96,96),(87,94)]}
MOUTH=[(72,121),(77,119),(89,122),(95,126),(93,132),(79,134),(73,131)]
SIZE=(168,197)

def check(canon):
    canon=Path(canon)
    if hashlib.sha256(canon.read_bytes()).hexdigest()!=CANON_SHA:
        raise ValueError('WRONG_CANON_SHA: refuse writes')
    with Image.open(canon) as im:
        if im.size!=(941,1672) or im.mode!='RGBA':raise ValueError('WRONG_CANON_FORMAT')
        return im.crop(BBOX).copy()

def mask_polygon(points):
    im=Image.new('L',SIZE,0)
    ImageDraw.Draw(im).polygon(points,fill=255)
    return im

def cutout(im,mask):
    a=im.copy();a.putalpha(mask);return a

def skin_underlay(canon):
    """Candidate cheek-color restoration; avoids sampling adjacent dark lashes into center.
    Outputs a TECHNICAL skin base, NOT genuine painted hidden skin.
    """
    src=np.asarray(canon).copy();h,w=src.shape[:2]
    yy,xx=np.indices((h,w));candidate=src[:,:,:3].astype(np.float32).copy()
    # Sample cheek skin at offset and smooth lightly; region/weights are editable.
    for name,dx,dy in [('left',8,15),('right',-4,14)]:
        region=np.asarray(mask_polygon(EYES[name]),dtype=np.uint8)
        # source-pixel patch sampled from cheek below, excluding neighboring hair/eyes.
        sx=np.clip(xx+dx,44 if name=='left' else 96,67 if name=='left' else 126)
        sy=np.clip(yy+dy,117 if name=='left' else 99,124 if name=='left' else 109)
        patch=src[sy,sx,:3].astype(np.float32)
        patch=cv2.GaussianBlur(patch,(5,5),1.15)
        # Retain upper/lower skin tone variation from in-mask y position.
        t=np.clip((yy-(96 if name=='left' else 77))/22,0,1).astype(np.float32)
        skin_top=np.array([249,209,198] if name=='left' else [252,217,207],np.float32)
        patch=(0.74*patch+0.26*(skin_top[None,None,:]*(1-t[:,:,None])+patch*t[:,:,None]))
        # anti-aliased polygon edge feather, stays fully source exact outside polygon
        m=region>0
        candidate[m]=patch[m]
    # Keep all original source RGB outside eye polygon, no blurred transition outside.
    out=np.asarray(canon).copy()
    union=np.maximum(np.asarray(mask_polygon(EYES['left'])),np.asarray(mask_polygon(EYES['right'])))>0
    out[:,:,:3][union]=np.uint8(np.clip(candidate[union],0,255))
    return Image.fromarray(out,'RGBA'), union

def polyline_bezier(points,scale=5):
    """Catmull-Rom sampled path for manually chosen eyelid landmarks."""
    pts=np.array(points,dtype=float)
    arr=[]
    for i in range(len(pts)-1):
        p0=pts[max(i-1,0)];p1=pts[i];p2=pts[i+1];p3=pts[min(i+2,len(pts)-1)]
        for t in np.linspace(0,1,16,endpoint=False):
            t2=t*t;t3=t2*t
            x=.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3)
            arr.append(tuple(np.round(x*scale).astype(int)))
    arr.append(tuple(np.round(pts[-1]*scale).astype(int)))
    return arr

def eyelid(side,closure=1.0):
    """Manually controlled lid arc; pixel-painted on its own transparent layer.
    For CP386 this is a *technical* candidate, not user-approved eye art.
    """
    S=5
    canvas=Image.new('RGBA',(SIZE[0]*S,SIZE[1]*S),(0,0,0,0));d=ImageDraw.Draw(canvas)
    if closure<=0:return canvas.resize(SIZE,Image.Resampling.LANCZOS)
    if side=='left':
        # under hairline: top-to-bottom slope from x36 to x65.
        pts=[(34.2,106.4),(40,105.8),(47,104.2),(55,103.3),(64,99.7)]
        crease=[(37,109.5),(44,108.2),(53,106.5),(61,103.6)]
        lashes=[((35,107),(33,108.2)),((40,105.8),(38,107.4)),((63,100),(66,98.9))]
    else:
        pts=[(89.2,89),(97,86.8),(104.5,84.5),(113,82.7),(124,78.8)]
        crease=[(93,92.2),(100,89.2),(110,86.0),(120,81.7)]
        lashes=[((89.4,88.9),(87.5,90.7)),((121,79.9),(125,78)),((123,79.1),(127,76.4))]
    # geometry changes with closure: partial lid line follows upper location and visible lower pupil preserved for partially open frame
    shift=(1-closure)*(3.4 if side=='left' else 3.2)
    p=[(x,y-shift) for x,y in pts]
    c=[(x,y-shift) for x,y in crease]
    d.line(polyline_bezier(c,S),fill=(209,111,127,135),width=2*S,joint='curve')
    d.line(polyline_bezier(p,S),fill=(102,50,68,241),width=round(1.3*S),joint='curve')
    d.line(polyline_bezier([(x,y+.48) for x,y in p],S),fill=(161,80,90,140),width=round(.55*S),joint='curve')
    for a,b in lashes:
        d.line([(int(x*S),int((y-shift)*S)) for x,y in [a,b]],fill=(77,47,62,210),width=round(.65*S))
    return canvas.resize(SIZE,Image.Resampling.LANCZOS)

def save_ora(path, base, source, parts, lids):
    entries=[('CANON_exact_right_eye',parts['right'],True),('CANON_exact_left_eye',parts['left'],True),('CANON_exact_mouth',parts['mouth'],True),
             ('CP386_skin_reconstruction_TECH_ONLY',base,True),('CP386_closed_left_lid_DRAFT',lids['left'],False),('CP386_closed_right_lid_DRAFT',lids['right'],False),('CANON_exact_source_guide_HIDDEN',source,False)]
    root=ET.Element('image',w=str(SIZE[0]),h=str(SIZE[1]),name='CP386 original static + blink technical not game art',version='0.0.3')
    stack=ET.SubElement(root,'stack')
    static=base.copy()
    for k in ['mouth','left','right']:static.alpha_composite(parts[k])
    assert np.array_equal(np.asarray(static),np.asarray(source))
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,img,visible) in enumerate(entries):
            internal=f'data/layer_{i:02d}.png';buf=io.BytesIO();img.save(buf,format='PNG');z.writestr(internal,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':internal,'visibility':'visible' if visible else 'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        buf=io.BytesIO();static.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    with zipfile.ZipFile(path) as z:assert z.testzip() is None
    return static

def run(canon,output,prev_blink=None):
    src=check(canon)
    root=Path(output)
    for k in ['source','layers','frames','qa','ora']:(root/k).mkdir(parents=True,exist_ok=True)
    shutil.copyfile(canon,root/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    src.save(root/'source'/'EXACT_SHY_168x197.png')
    under,union=skin_underlay(src)
    masks={k:mask_polygon(pts) for k,pts in {**EYES,'mouth':MOUTH}.items()}
    mouth=cutout(src,masks['mouth'])
    # Static base: same source within mouth region as original; eyelids replaced only when eyes hidden.
    parts={k:cutout(src,mask) for k,mask in masks.items()}
    # Need preserve mouth original in base except eyes; avoids unrelated mouth inpainting
    base=under
    closed_lids={k:eyelid(k,1.0) for k in EYES}
    exact=save_ora(root/'ora'/'CP386_SOURCE_EXACT_AND_EYELIDS_DRAFT_NOT_RIG.ora',base,src,parts,closed_lids)
    for k,l in closed_lids.items():l.save(root/'layers'/f'{k}_closed_eyelid_DRAFT.png')
    for k,mask in masks.items():
        mask.save(root/'layers'/f'{k}_source_mask.png')
        parts[k].save(root/'layers'/f'{k}_source_exact_cutout.png')
    base.save(root/'layers'/'CP386_CHEEK_BASE_TECH_NOT_APPROVED.png')
    exact.save(root/'CP386_CANON_SOURCE_EXACT_OPEN.png')
    if not np.array_equal(np.asarray(exact),np.asarray(src)):raise AssertionError('source identity lost')
    # Frame sequence; no eye-source fade, uses actual source for open and source eye cutouts for partial frames only.
    old=Image.open(prev_blink).convert('RGBA') if prev_blink else src.copy()
    exposures=[0,.25,.65,1,.65,.25,0]
    frames=[]
    for i,t in enumerate(exposures):
        if t==0: frame=exact.copy()
        else:
            frame=base.copy();frame.alpha_composite(mouth)
            # only technical intermediate, use native source eyes source geometry at t<=0.25
            if t<=.25:
                frame.alpha_composite(parts['left']);frame.alpha_composite(parts['right'])
            for name in EYES:frame.alpha_composite(eyelid(name,t))
        frame.save(root/'frames'/f'CP386_FRAME_{i:02d}_TECH_ONLY.png');frames.append(frame)
    assert np.array_equal(np.asarray(frames[0]),np.asarray(src)) and np.array_equal(np.asarray(frames[-1]),np.asarray(src))
    changed=np.any(np.asarray(under)[:,:,:3]!=np.asarray(src)[:,:,:3],axis=2)
    assert int(np.count_nonzero(changed&~union))==0
    # Honest QA: no misleading scalar "looks better" score.
    board=Image.new('RGB',(1600,630),(17,35,56));draw=ImageDraw.Draw(board)
    title='TVK CP386  |  LAM THIEN EXACT CANON — EYELID REPAINT STUDY (NOT APPROVED)'
    draw.text((20,16),title,fill=(245,245,245))
    cards=[('01 CANON SOURCE',src),('02 CP385 TECH BLINK' if prev_blink else '02 PRIOR BLINK NOT PROVIDED',old),('03 CP386 EYELID PATCH DRAFT',frames[3]),('04 CP386 CANON EXACT OPEN',exact)]
    for i,(label,img) in enumerate(cards):
        x=20+i*397
        draw.text((x,52),label,fill='#cfe6f7')
        face=img.resize((360,422),Image.Resampling.NEAREST)
        board.paste(face.convert('RGB'),(x,78))
    draw.text((20,521),'New underpaint is color-guided technical reconstruction, NOT artist-approved. Static face must remain pixel-exact.',fill=(255,209,170))
    draw.text((20,548),'CP386 MUST NOT be imported as Spine, live animation, or Android APK asset. No synthetic substitute characters.',fill=(255,209,170))
    board.save(root/'qa'/'CP386_CANON_CP385_CP386_COMPARE_NOT_APPROVED.png')
    atlas=Image.new('RGBA',(168*7,197),(0,0,0,0))
    for i,f in enumerate(frames):atlas.paste(f,(168*i,0))
    atlas.save(root/'qa'/'CP386_SEVEN_FRAME_CONTACT_SHEET_TECH.png')
    frames[0].save(root/'qa'/'CP386_FRAMES_TECH_NOT_APPROVED.gif',save_all=True,append_images=frames[1:],duration=[370,100,85,150,85,100,400],loop=0,disposal=2)
    report={'checkpoint':'CP386','canon_sha256':CANON_SHA,'portrait_size':list(SIZE),
            'open_source_exact':True,'open_frame_0_and_6_pixel_exact':True,
            'skin_changed_pixels':int(changed.sum()),'skin_changed_outside_eyes':0,
            'draft_blend_is_skin_from_cheek':True,'seven_test_frames':exposures,
            'visual_qa':'NOT_PASSED','skin_paint_artist_approved':False,'closed_eye_artist_approved':False,
            'is_fullbody_hd':False,'rig_ready':False,'apk_ready':False,'sprite_paths':{},'production_release':'blocked_pending_art',
            'warning':'Technical cheek-color patch and drawn lid arc, not validated painting; no production import.'}
    (root/'CP386_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True);p.add_argument('--prev-blink');a=p.parse_args();print(json.dumps(run(a.canon,a.out,a.prev_blink),ensure_ascii=False,indent=2))
#!/usr/bin/env python3
"""CP384 CANON-exact Lâm Thiển portrait: editable source eyes/mouth + experimental hidden skin underpaint.
This does not produce native artist-painted HD, approved animation, or a production portrait.
"""
from pathlib import Path
import argparse, hashlib, io, json, shutil, zipfile, xml.etree.ElementTree as ET
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE=(941,1672)
PORTRAIT_BBOX=(25,684,193,881) # original shy 174x203 panel, trim 3 px each side -> 168x197
EYE_ROIS={'left_eye':(30,94,66,115),'right_eye':(86,74,123,99)}
MOUTH_ROI=(73,120,94,134)


def verify_source(canon):
    c=Path(canon)
    if hashlib.sha256(c.read_bytes()).hexdigest()!=CANON_SHA:
        raise ValueError('CANON_SHA_MISMATCH; no outputs created')
    im=Image.open(c)
    if im.size!=CANON_SIZE or im.mode!='RGBA':
        raise ValueError('CANON_FORMAT_MISMATCH; no outputs created')
    return im


def masks(size):
    output={}
    for name,(x1,y1,x2,y2) in [*EYE_ROIS.items(),('mouth',MOUTH_ROI)]:
        m=Image.new('L',size,0)
        d=ImageDraw.Draw(m)
        # Carefully bounded eye/mouth editing areas; including some skin edge.
        d.ellipse((x1,y1,x2,y2),fill=255)
        output[name]=m
    return output


def alpha_layer(im,mask):
    rgba=im.copy()
    rgba.putalpha(mask)
    return rgba


def make_closed_lid(size,x1,y1,x2,y2,curvature):
    """Simple technical vector-like painted lid line, not artist-approved closed-eye artwork."""
    s=4
    layer=Image.new('RGBA',(size[0]*s,size[1]*s),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    x_mid=(x1+x2)/2
    points=[]
    for t in np.linspace(0,1,45):
        x=x1+(x2-x1)*t
        y=y1+(y2-y1)*t+curvature*4*t*(1-t)
        points.append((int(x*s),int(y*s)))
    d.line(points,fill=(110,61,66,239),width=round(1.45*s),joint='curve')
    d.line([(int((x1+1)*s),int((y1+1.7)*s)),(int((x_mid-1)*s),int(((y1+y2)/2+curvature+1.5)*s))],fill=(187,107,101,128),width=round(0.65*s))
    return layer.resize(size,Image.Resampling.LANCZOS)


def merge_part(base,parts):
    out=base.copy()
    for k in ('left_eye','right_eye','mouth'):
        out.alpha_composite(parts[k])
    return out


def create(canon,output):
    original=verify_source(canon)
    # All preflights above precede output creation.
    inner=original.crop(PORTRAIT_BBOX)
    size=inner.size
    if size!=(168,197): raise ValueError('Unexpected portrait dimensions')
    region_masks=masks(size)
    total=np.maximum.reduce([np.asarray(m) for m in region_masks.values()])
    if int(np.count_nonzero(total>0))<100: raise RuntimeError('Empty masks')
    src=np.asarray(inner).copy()
    inpaint=cv2.inpaint(cv2.cvtColor(src[:,:,:3],cv2.COLOR_RGB2BGR),total.astype(np.uint8),3,cv2.INPAINT_TELEA)
    base=Image.fromarray(np.dstack((cv2.cvtColor(inpaint,cv2.COLOR_BGR2RGB),src[:,:,3])).astype(np.uint8),'RGBA')
    layers={k:alpha_layer(inner,v) for k,v in region_masks.items()}
    reconstructed=merge_part(base,layers)
    if not np.array_equal(np.array(reconstructed),src):
        raise RuntimeError('Static master not pixel-exact: refuse')
    # Technical blink draft uses hidden artificial lids, and eye cutouts are toggled off.
    left_lid=make_closed_lid(size,34,103,62,99,2.1)
    right_lid=make_closed_lid(size,91,89,117,80,3.2)
    blink=base.copy()
    blink.alpha_composite(layers['mouth'])
    blink.alpha_composite(left_lid);blink.alpha_composite(right_lid)
    root=Path(output)
    (root/'art_layers').mkdir(parents=True,exist_ok=True)
    (root/'qa').mkdir(exist_ok=True)
    (root/'source').mkdir(exist_ok=True)
    shutil.copyfile(canon,root/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    inner.save(root/'source'/'CP384_SHY_CANON_NATIVE_CROP_168x197.png')
    base.save(root/'art_layers'/'00_technical_inpaint_underpaint_NOT_APPROVED.png')
    for key,v in layers.items():
        v.save(root/'art_layers'/f'01_{key}_EXACT_SOURCE.png')
        region_masks[key].save(root/'art_layers'/f'{key}_editable_mask.png')
    left_lid.save(root/'art_layers'/'05_left_blink_lid_DRAFT_HIDDEN.png')
    right_lid.save(root/'art_layers'/'06_right_blink_lid_DRAFT_HIDDEN.png')
    reconstructed.save(root/'CP384_STATIC_SOURCE_EXACT_MASTER.png')
    blink.save(root/'qa'/'CP384_BLINK_TECHNICAL_DRAFT_NOT_APPROVED.png')
    # ORA static stack order visible eye/mouth/underpaint, hidden other references.
    layer_list=[
        ('mouth_SOURCE_EXACT',layers['mouth'],True),
        ('right_eye_SOURCE_EXACT',layers['right_eye'],True),
        ('left_eye_SOURCE_EXACT',layers['left_eye'],True),
        ('left_closed_lid_TECH_DRAFT',left_lid,False),
        ('right_closed_lid_TECH_DRAFT',right_lid,False),
        ('skin_underpaint_TECH_UNAPPROVED',base,True),
        ('CANON_NATIVE_168x197_REFERENCE_HIDDEN',inner,False),
    ]
    zpath=root/'CP384_CANON_EXACT_FACE_EDITABLE_EYES_TECH_NOT_RIG.ora'
    xroot=ET.Element('image',{'w':str(size[0]),'h':str(size[1]),'name':'CP384 canonical static face, unapproved animated variants','version':'0.0.3'})
    stack=ET.SubElement(xroot,'stack')
    with zipfile.ZipFile(zpath,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(layer_list):
            path=f'data/layer_{i:02}.png';buffer=io.BytesIO();im.save(buffer,format='PNG');z.writestr(path,buffer.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':path,'visibility':'visible' if visible else 'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(xroot,encoding='utf-8',xml_declaration=True))
        b=io.BytesIO();reconstructed.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
    with zipfile.ZipFile(zpath) as z:
        if z.testzip(): raise RuntimeError('ORA CRC failed')
    # QA only from original Lâm Thiển CANON and its derivative.
    panel=Image.new('RGB',(1300,540),'#142a41')
    d=ImageDraw.Draw(panel)
    for i,(title,sub,im) in enumerate([
        ('1. CANON native source','168 x 197 • unchanged',inner),
        ('2. CP384 editable static','Pixel-exact RGB/A',reconstructed),
        ('3. Experimental underpaint','NOT APPROVED',base),
        ('4. Blink pose study','NOT APPROVED',blink)
    ]):
        xp=22+i*325
        d.text((xp,23),title,fill='#ffffff')
        d.text((xp,48),sub,fill='#9ebbdc')
        canvas=Image.new('RGB',(294,402),'#edf5fd')
        colored=im.resize((294,344),Image.Resampling.NEAREST)
        canvas.paste(colored,(0,29),colored.getchannel('A'))
        panel.paste(canvas,(xp,85))
    d.text((23,511),'All character imagery comes from LAM THIEN CANON V2.1. Blink/inpaint are unapproved technical studies.',fill='#f2c6aa')
    qapath=root/'qa'/'CP384_CANON_STATIC_MASTER_AND_BLINK_DRAFT.png'
    panel.save(qapath)
    report={
      'checkpoint':'CP384','canon_sha256':CANON_SHA,'portrait_bbox':list(PORTRAIT_BBOX),
      'portrait_native_size':list(size),'expression':'01_shy_Ngai_ngung',
      'static_recomposition_pixel_exact':True,
      'reference_color_source':'CANON only',
      'editable_source_part_count':3,
      'hidden_blink_draft_layers':2,
      'technical_underpaint_layer_count':1,
      'ora_total_layers':len(layer_list),
      'partial_occluded_art':'inpaint_TECH_NOT_APPROVED',
      'portrait_background_transparent':False,
      'source_expression_approved':True,
      'face_painting_approved':False,
      'full_native_high_resolution_painting':False,
      'blink_animation_verified':False,
      'visual_qa':'NOT_PASSED',
      'production_release':'blocked_pending_art','sprite_paths':{},
      'spine_ready':False,'apk_ready':False,
      'next':'CP385 painter-authored eye closure, mouth states, hair and transparent portrait matting; review against CANON before release.'
    }
    (root/'CP384_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    print(json.dumps(create(a.canon,a.out),ensure_ascii=False,indent=2))
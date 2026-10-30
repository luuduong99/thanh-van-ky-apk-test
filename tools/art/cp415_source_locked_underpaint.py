#!/usr/bin/env python3
"""CP415: source-locked actual pigment study for head/hair/neck underpaint.

IMPORTANT: These are authored paths painted on exact CANON colors, not a portrait
regeneration. The under-head support is partly OpenCV inpaint and IS NOT final art.
The head capsule is still a rough technical matte. Nothing here is approved for game.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter

CANON='LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BOX=(16,180,224,623)
SIZE=(208,443)
PIVOT=(104,77)
POLY=[(100,1),(91,2),(81,8),(72,18),(66,31),(64,46),(69,58),(75,68),(85,77),(94,82),(106,85),(118,80),(129,73),(138,60),(143,47),(138,33),(131,22),(128,13),(115,3)]
ANGLES=(-4,-2,0,2,4)
S=4

def h(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def checked(path):
    if h(path)!=SHA:raise ValueError('Wrong CANON raw SHA - reject before outputs')
    im=Image.open(path)
    if im.size!=(941,1672) or im.mode!='RGBA':raise ValueError('Wrong CANON properties')
    return im.copy()

def mask():
    m=Image.new('L',SIZE,0)
    ImageDraw.Draw(m).polygon(POLY,fill=255)
    return m

def rgba():return Image.new('RGBA',SIZE,(0,0,0,0))

def paint_paths(front):
    """Art study: human-chosen Bézier/PIL stroke paths in CANON-local coordinates.
    Hair is shaded from source hues; neck is constructed behind fixed head.
    Always editable as separate paint layers. Not AI-inferred anatomy / not production.
    """
    big=(SIZE[0]*S,SIZE[1]*S)
    hair=Image.new('RGBA',big,(0,0,0,0))
    skin=Image.new('RGBA',big,(0,0,0,0))
    transitions=Image.new('RGBA',big,(0,0,0,0))
    hd=ImageDraw.Draw(hair,'RGBA'); sd=ImageDraw.Draw(skin,'RGBA'); td=ImageDraw.Draw(transitions,'RGBA')
    def points(coords):return [(int(round(x*S)),int(round(y*S))) for x,y in coords]
    def polygon(d,coords,color):d.polygon(points(coords),fill=color)
    def bezier(p0,p1,p2,p3,n=60):
        out=[]
        for i in range(n+1):
            t=i/n;v=1-t
            x=v**3*p0[0]+3*v*v*t*p1[0]+3*v*t*t*p2[0]+t**3*p3[0]
            y=v**3*p0[1]+3*v*v*t*p1[1]+3*v*t*t*p2[1]+t**3*p3[1]
            out.append((int(round(x*S)),int(round(y*S))))
        return out
    # Pigment hidden by the head: underlying rear hair fans toward the neck.
    # Clip to head-region later; no production front hair has been moved.
    polygon(hd,[(67,15),(93,3),(119,6),(142,26),(139,72),(125,86),(86,85),(65,67)],(174,163,192,248))
    polygon(hd,[(71,12),(90,8),(101,14),(89,43),(77,82),(64,73)],(144,137,172,236))
    polygon(hd,[(117,8),(135,21),(145,52),(130,82),(114,85),(122,44)],(153,143,182,235))
    polygon(hd,[(84,54),(98,48),(116,58),(122,80),(115,87),(91,86)],(181,154,180,250))
    # Inner hair shadow and strand-level strokes, hand-selected along long hair direction.
    lines=[
      ((90,8),(80,21),(70,48),(75,84),(224,208,227,195),1.5),
      ((104,6),(91,21),(88,57),(84,83),(215,203,223,155),1.1),
      ((113,8),(120,28),(132,51),(123,86),(226,213,230,175),1.2),
      ((125,20),(132,37),(143,57),(128,81),(114,105,151,155),1.1),
      ((81,15),(75,30),(64,50),(82,78),(238,226,238,110),.8),
      ((92,18),(89,30),(79,66),(94,83),(236,218,229,170),.8),
      ((117,17),(113,36),(127,69),(114,87),(241,221,235,125),.9),
      ((109,24),(103,45),(110,67),(107,89),(122,105,142,135),.8),
    ]
    for p0,p1,p2,p3,c,w in lines:
        hd.line(bezier(p0,p1,p2,p3),fill=c,width=max(2,int(w*S)),joint='curve')
    # A *painted* continuation of neck skin under jaw, behind movable head.
    # Deliberately slightly wider than exposed jaw transition.
    polygon(sd,[(94,65),(113,66),(117,74),(114,89),(91,91),(90,77)],(220,166,151,255))
    polygon(sd,[(99,65),(110,65),(111,84),(107,90),(96,89),(97,75)],(251,208,192,251))
    polygon(sd,[(108,70),(114,72),(114,84),(109,90),(104,87)],(189,126,113,130))
    polygon(sd,[(91,70),(98,71),(98,88),(92,89)],(172,121,118,98))
    # Soft jaw and collar contact shadows from manual stroke placements.
    for p0,p1,p2,p3,c,w in [
      ((94,74),(97,82),(99,84),(98,90),(167,111,112,150),1.1),
      ((111,72),(110,81),(110,85),(107,90),(156,104,110,155),1.4),
      ((94,84),(99,87),(109,87),(114,85),(128,88,109,190),1.3),
      ((83,78),(90,85),(94,86),(99,88),(142,124,158,155),1.1),
      ((115,85),(122,88),(127,81),(130,78),(132,118,153,145),1.0),
    ]:td.line(bezier(p0,p1,p2,p3),fill=c,width=max(2,round(w*S)),joint='curve')
    # Low-opacity collar under-shadow (not a replacement of visible collar).
    polygon(td,[(93,83),(98,89),(110,89),(118,83),(115,92),(104,94),(92,91)],(84,82,127,110))
    layers=[x.resize(SIZE,Image.Resampling.LANCZOS) for x in (hair,skin,transitions)]
    return layers

def create_plate(front):
    # Technical fallback is retained and *disclosed*; the new layers contain real
    # authored pigment but are not yet a complete unobstructed backing master.
    src=np.array(front)
    m=np.array(mask())
    rgb=cv2.cvtColor(src[:,:,:3],cv2.COLOR_RGB2BGR)
    inf=cv2.cvtColor(cv2.inpaint(rgb,m,3,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
    plate=Image.fromarray(np.dstack([inf,src[:,:,3]]),'RGBA')
    layers=paint_paths(front)
    # Never touch pixels outside the original rough head matte. All replacement
    # pigment stays under the still-visible CANON at neutral.
    mm=np.array(mask(),dtype=np.uint16)
    clipped=[]
    for idx,ly in enumerate(layers):
        ar=np.array(ly).copy()
        # Visible source has pale background around crown: a painted crown-sized
        # patch reveals as a violet halo when head tilts. Reject that artifact.
        # Only study hidden locks that join the neck and rear long hair.
        if idx==0:
            yy=np.arange(SIZE[1])[:,None]
            fade=np.clip((yy-62)/12.0,0.0,1.0)
            ar[:,:,3]=(ar[:,:,3]*fade).astype(np.uint8)
        ar[:,:,3]=((ar[:,:,3].astype(np.uint16)*mm)//255).astype(np.uint8)
        clipped.append(Image.fromarray(ar,'RGBA'))
    layers=clipped
    for ly in layers:plate=Image.alpha_composite(plate,ly)
    return plate,layers

def cut_head(front):
    src=np.array(front).copy()
    src[:,:,3]=np.where(np.array(mask())>0,src[:,:,3],0).astype('uint8')
    return Image.fromarray(src,'RGBA')

def preview(front,plate,head,angle):
    if angle==0:return front.copy()
    rr=head.rotate(angle,resample=Image.Resampling.BICUBIC,center=PIVOT,expand=False)
    return Image.alpha_composite(plate,rr)

def plate_before(front):
    src=np.array(front);m=np.array(mask())
    inf=cv2.cvtColor(cv2.inpaint(cv2.cvtColor(src[:,:,:3],cv2.COLOR_RGB2BGR),m,3,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
    return Image.fromarray(np.dstack([inf,src[:,:,3]]),'RGBA')

def review_board(front,pl,head):
    # Source only: 5-angle after + before head ROIs compare the authored underpaint.
    crop=(56,0,154,117); z=4; tw=(crop[2]-crop[0])*z; th=(crop[3]-crop[1])*z
    gap=14;top=70;footer=75
    w=(tw+gap)*len(ANGLES)+gap;h=top+2*th+footer+46
    out=Image.new('RGB',(w,h),(226,235,247));d=ImageDraw.Draw(out)
    d.text((gap,10),'CP415: SOURCE-LOCKED HAIR / NECK PIGMENT STUDY - UNAPPROVED',fill=(36,63,102))
    d.text((gap,28),'TOP: CP412 auto-inpaint only | BOTTOM: 3 new painted overlays on same exact source',fill=(56,76,112))
    before=plate_before(front)
    for i,a in enumerate(ANGLES):
        x=gap+i*(tw+gap)
        d.rectangle((x,48,x+tw,68),fill=(29,56,90))
        d.text((x+10,52),f'{a:+d} degrees',fill='white')
        for j,p in enumerate((before,pl)):
            im=preview(front,p,head,a).crop(crop).resize((tw,th),Image.Resampling.NEAREST).convert('RGB')
            out.paste(im,(x,top+j*(th+22)))
    d.text((gap,h-44),'0 degrees is exact CANON; angles are diagnostic transforms, NOT finished animation.',fill=(156,57,79))
    d.text((gap,h-26),'Some white clipping / incomplete long hair remains; visual approval is REQUIRED.',fill=(156,57,79))
    return out

def layer_board(front,layers):
    names=['BACK_HAIR_PAINT','NECK_SKIN_PAINT','TRANSITION_SHADOW_PAINT']
    out=Image.new('RGB',(4*208*2+5*12,443*2+80),(235,243,252));d=ImageDraw.Draw(out)
    imgs=[front]+[Image.alpha_composite(Image.new('RGBA',SIZE,(230,233,240,255)),p) for p in layers]
    for i,img in enumerate(imgs):
        x=12+i*(208*2+12)
        out.paste(img.convert('RGB').resize((416,886),Image.Resampling.NEAREST),(x,42))
        d.text((x+4,15),['ORIGINAL CANON',*names][i],fill=(28,60,91))
    return out

def save_ora(path,front,head,plate,layers):
    transparent=rgba(); names=['PAINT 03 - transition / collar shadow','PAINT 02 - neck flesh under jaw','PAINT 01 - behind-head hair pigment']
    layers_order=[(names[0],layers[2],False),(names[1],layers[1],False),(names[2],layers[0],False),
      ('STUDY ROTATABLE HEAD rough mask - NOT clean hair',head,False),
      ('TECHNICAL INPAINT + NEW PAINT composite hidden',plate,False),
      ('EMPTY - artist to draw correct same-pose closed eyelids',transparent,False),
      ('CANON STANDING FRONT exact source / LOCKED',front,True)]
    root=ET.Element('image',w='208',h='443',name='CP415 SOURCE LOCKED UNDERPAINT STUDY / NOT APPROVED',version='0.0.3')
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,p,vis) in enumerate(layers_order):
            b=io.BytesIO();p.save(b,format='PNG');loc=f'data/layer{i:02d}.png';z.writestr(loc,b.getvalue())
            ET.SubElement(stack,'layer',name=name,src=loc,opacity='1.0',visibility='visible' if vis else 'hidden',x='0',y='0',**{'composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        b=io.BytesIO();front.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
    with zipfile.ZipFile(path) as z:assert z.testzip() is None

def run(source,out):
    im=checked(source)
    out.mkdir(parents=True,exist_ok=True)
    front=im.crop(BOX)
    head=cut_head(front)
    plate,layers=create_plate(front)
    neutral=Image.alpha_composite(plate,head)
    assert np.array_equal(np.array(neutral),np.array(front)), 'CANON 0 deg exact failed'
    front.save(out/'CP415_CANON_FRONT_EXACT.png')
    head.save(out/'CP415_HEAD_ROUGH_SOURCE.png')
    plate.save(out/'CP415_BACKING_CANDIDATE_AUTOFILL_PLUS_PAINT.png')
    for name,layer in zip(('HAIR_PIGMENT','NECK_SKIN','COLLAR_SHADOW'),layers):layer.save(out/f'CP415_{name}_PAINTED_STUDY.png')
    review_board(front,plate,head).save(out/'CP415_BEFORE_AFTER_5_ANGLES_CANON.png')
    layer_board(front,layers).save(out/'CP415_PAINT_LAYERS_CANON_BOARD.png')
    save_ora(out/'CP415_UNDERPAINT_PIGMENT_STUDY_NOT_APPROVED.ora',front,head,plate,layers)
    source=np.array(front)
    alpha_counts=[int(np.count_nonzero(np.array(layer.getchannel('A')))) for layer in layers]
    report={
     'checkpoint':'CP415','status':'UNDERPAINT_PIGMENT_STUDY_NOT_APPROVED',
     'source_sha256':SHA,'source_exact':True,'front_crop':BOX,'front_size':SIZE,
     'neutral_pixel_exact':True,'layers_painted':3,'paint_nonempty_pixel_counts':alpha_counts,
     'backing_has_technical_inpaint':True,'mask_semantically_clean':False,
     'face_eye_source_preserved_when_neutral':True,
     'real_human_artist_approved':False,'eyelid_closed_same_pose_art_approved':False,
     'spine_ready':False,'apk_art_ready':False,'android_device_verified':False,
     'production_release_status':'blocked_pending_art','sprite_paths':{},
     'note':'New painter-like strokes are hand-specified procedural paint, mixed with inpaint; no claim of painter-grade underpaint. No original CANON visible pixels changed in neutral.','outputs':{}
    }
    for p in sorted(out.iterdir()):
      if p.is_file():report['outputs'][p.name]={'sha256':h(p),'size_bytes':p.stat().st_size}
    (out/'CP415_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    a=p.parse_args();print(json.dumps(run(a.canon,a.out),indent=2))
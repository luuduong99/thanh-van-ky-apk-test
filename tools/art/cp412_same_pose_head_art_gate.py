#!/usr/bin/env python3
"""CP412: exact-CANON artist intake and head-seam diagnostic.

This is NOT a head rig, author-painted underpaint, or artwork approval.
A technical rough cutout is used ONLY to expose what fails when the head tilts.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import math
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CANON_NAME = 'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
CANON_HASH = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE = (941,1672)
FRONT_BOX = (16,180,224,623)
FRONT_SIZE = (208,443)
HEAD_PIVOT = (104,77)
HEAD_CAPSULE = [(100,1),(91,2),(81,8),(72,18),(66,31),(64,46),(69,58),(75,68),(85,77),(94,82),(106,85),(118,80),(129,73),(138,60),(143,47),(138,33),(131,22),(128,13),(115,3)]
FACE_ROI = (83,40,128,74)
EYE_ROIS = {'left':(89,48,102,58),'right':(107,48,122,58)}
NECK_ROI = (92,70,117,91)
ANGLES=(-4,-2,0,2,4)
# Entries are intentionally EMPTY, to be handpainted using exact pose. No false master.
REQUIRED_LAYERS = (
    '01_front_hair_around_face',
    '02_face_neutral_pose',
    '03_closed_eyelids_same_pose',
    '04_back_hair_long_strands',
    '05_neck_scalp_underpaint',
    '06_shoulder_underpaint',
    '07_hair_underpaint',
    '08_head_accessories',
)

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def load_canon(path:Path)->Image.Image:
    if sha(path)!=CANON_HASH:
        raise ValueError('CANON SHA-256 mismatch. No outputs created.')
    with Image.open(path) as src:
        if src.size!=CANON_SIZE or src.mode!='RGBA':
            raise ValueError('CANON image size/mode mismatch')
        return src.copy()

def matte()->Image.Image:
    im=Image.new('L',FRONT_SIZE,0)
    ImageDraw.Draw(im).polygon(HEAD_CAPSULE,fill=255)
    return im

def derive_diagnostic(front:Image.Image):
    m=np.array(matte())
    pixels=np.array(front)
    rgb=cv2.cvtColor(pixels[:,:,:3],cv2.COLOR_RGB2BGR)
    inpaint=cv2.cvtColor(cv2.inpaint(rgb,m,3,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
    plate=Image.fromarray(np.dstack((inpaint,pixels[:,:,3])),'RGBA')
    head=pixels.copy()
    head[:,:,3]=np.where(m>0,head[:,:,3],0)
    head=Image.fromarray(head,'RGBA')
    assert np.array_equal(np.array(Image.alpha_composite(plate,head)),pixels)
    return plate,head

def rotate_diagnostic(front,plate,head,angle):
    """Return rough overlay and number of technical-placeholder pixels newly exposed.
    Angles are ONLY to test seam risk, never to claim true motion.
    """
    if angle==0:
        return front.copy(),0
    rotated=head.rotate(angle,resample=Image.Resampling.BICUBIC,center=HEAD_PIVOT,expand=False)
    output=Image.alpha_composite(plate,rotated)
    original_mask=np.array(matte())>0
    new_alpha=np.array(rotated.getchannel('A'))
    revealed=original_mask & (new_alpha<250)
    # This diagnostic counts pixels inside the ROUGH removed-head polygon that
    # now need invented underpaint; not an artistic quality score.
    return output,int(np.count_nonzero(revealed))

def guide(front,scale=4):
    out=front.resize((front.width*scale,front.height*scale),Image.Resampling.NEAREST).convert('RGB')
    d=ImageDraw.Draw(out)
    xy=[(x*scale,y*scale) for x,y in HEAD_CAPSULE]
    d.line(xy+[xy[0]],fill='#f4a340',width=3)
    for box,color in [(FACE_ROI,'#28b3dd'),(NECK_ROI,'#ed5d9d'),*[(b,'#7dde9b') for b in EYE_ROIS.values()]]:
        d.rectangle(tuple(v*scale for v in box),outline=color,width=3)
    px,py=HEAD_PIVOT
    d.ellipse((px*scale-7,py*scale-7,px*scale+7,py*scale+7),fill='#e52324',outline='white',width=2)
    return out

def board(front,plate,head):
    """5 full-body poses and enlarged seam ROI; all panels use exact CANON crop."""
    scale=2
    w,h=front.size
    gap=14
    tile_w=w*scale
    top_h=42
    footer=68
    frame_h=h*scale
    crop_box=(60,0,152,125)
    face_scale=4
    zoom_h=(crop_box[3]-crop_box[1])*face_scale
    width=(tile_w+gap)*len(ANGLES)+gap
    output=Image.new('RGB',(width,top_h+frame_h+zoom_h+footer+42),'#e6eff9')
    d=ImageDraw.Draw(output)
    counts={}
    for idx,angle in enumerate(ANGLES):
        pose,count=rotate_diagnostic(front,plate,head,angle)
        counts[str(angle)]=count
        ox=gap+idx*(tile_w+gap)
        d.rectangle((ox,3,ox+tile_w,top_h-4),fill='#1b3554')
        d.text((ox+10,13),f'{angle:+} deg | exposed {count} px',fill='white')
        output.paste(pose.convert('RGB').resize((tile_w,frame_h),Image.Resampling.NEAREST),(ox,top_h))
        face=pose.crop(crop_box).convert('RGB').resize(((crop_box[2]-crop_box[0])*face_scale,zoom_h),Image.Resampling.NEAREST)
        output.paste(face,(ox+(tile_w-face.width)//2,top_h+frame_h+28))
    y=top_h+frame_h
    d.text((gap,y+5),'CLOSE-UP: same source pose | nearest-neighbor viewing enlargement only',fill='#1c466b')
    d.text((gap,y+zoom_h+38),'TECHNICAL DIAGNOSTIC - NOT ANIMATION / NOT APPROVED ART',fill='#9c1f32')
    d.text((gap,y+zoom_h+58),'Exposed-pixel counts describe rough underpaint dependency, NOT visual quality.',fill='#31465d')
    return output,counts

def write_ora(target:Path,front:Image.Image):
    """OpenRaster artist preparation; original CANON only visible layer."""
    layer_names=list(reversed(REQUIRED_LAYERS))
    rgba=Image.new('RGBA',FRONT_SIZE,(0,0,0,0))
    layers=[(name,rgba,False) for name in layer_names]
    layers.append(('CANON FRONT - exact unedited source / LOCKED',front,True))
    root=ET.Element('image',w=str(FRONT_SIZE[0]),h=str(FRONT_SIZE[1]),name='CP412 FRONT POSE - ARTIST INTAKE ONLY',version='0.0.3')
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(target,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,img,visible) in enumerate(layers):
            bio=io.BytesIO();img.save(bio,format='PNG')
            loc=f'data/layer{i:02d}.png'
            z.writestr(loc,bio.getvalue())
            ET.SubElement(stack,'layer',name=name,src=loc,visibility=('visible' if visible else 'hidden'),opacity='1.0',x='0',y='0',**{'composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        bio=io.BytesIO();front.save(bio,format='PNG')
        z.writestr('mergedimage.png',bio.getvalue())
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None

def run(source:Path,output:Path):
    canon=load_canon(source)
    output.mkdir(parents=True,exist_ok=True)
    front=canon.crop(FRONT_BOX)
    front.save(output/'CP412_CANON_FRONT_UNMODIFIED.png')
    guide(front).save(output/'CP412_FRONT_HEAD_ANNOTATION_4X.png')
    plate,head=derive_diagnostic(front)
    visual,counts=board(front,plate,head)
    visual.save(output/'CP412_HEAD_ROTATION_SEAM_DIAGNOSTIC.png')
    write_ora(output/'CP412_ARTIST_INTAKE_BLANK_LAYERS.ora',front)
    manifest={
      'checkpoint':'CP412','source_filename':CANON_NAME,'source_sha256':CANON_HASH,
      'canvas':list(FRONT_SIZE),'canon_original_size':list(CANON_SIZE),
      'front_crop':list(FRONT_BOX),'head_pivot':list(HEAD_PIVOT),
      'angles_degrees':list(ANGLES),'technical_placeholder_exposed_pixels':counts,
      'master_hd_available':False,'blank_artist_layers':list(REQUIRED_LAYERS),
      'human_paint_complete':False,'closed_eyelid_same_pose_available':False,
      'art_approved':False,'head_rig_ready':False,'spine_ready':False,
      'android_device_tested':False,'apk_production_ready':False,'sprite_paths':{},
      'state':'ARTIST_HANDOFF_BLOCKED_PENDING_TRUE_LAYERED_ART',
      'note':'x4 is a NEAREST preview, not extra source resolution. Rotation is seam diagnostic, not accepted animation.'
    }
    (output/'CP412_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return manifest

if __name__=='__main__':
    arg=argparse.ArgumentParser()
    arg.add_argument('--canon',type=Path,required=True)
    arg.add_argument('--output',type=Path,required=True)
    a=arg.parse_args()
    print(json.dumps(run(a.canon,a.output),ensure_ascii=False,indent=2))
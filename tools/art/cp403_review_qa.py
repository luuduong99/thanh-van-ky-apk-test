#!/usr/bin/env python3
"""CP403: inspect already-generated source-locked CP402 blink atlas. No changes to canonical art."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

SOURCE_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
ATLAS_SHA='645738fa932a354e3142e2474eb35011491b091d06451a08c4443e6650529c97'
CROP=(25,684,193,881); W,H=168,197
ROIS=((29,93,71,124),(83,70,129,110))
POSITIONS=[0,.15,.30,.45,.60,.75,.90,1.,.90,.75,.60,.45,.30,.15,0]

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def verify(canon,atlas):
    if digest(canon)!=SOURCE_SHA: raise ValueError('WRONG_CANON_SOURCE_SHA256')
    if digest(atlas)!=ATLAS_SHA: raise ValueError('WRONG_CP402_ATLAS_SHA256')
    with Image.open(canon) as i:
        if i.size!=(941,1672) or i.mode!='RGBA':raise ValueError('WRONG_CANON_IMAGE_TYPE')
        ref=np.array(i.crop(CROP))
    with Image.open(atlas) as a:
        if a.size!=(2520,197) or a.mode!='RGBA':raise ValueError('WRONG_ATLAS_IMAGE_TYPE')
        allframes=np.array(a).reshape(H,15,W,4).transpose(1,0,2,3)
    if not np.array_equal(allframes[0],ref) or not np.array_equal(allframes[-1],ref):
        raise ValueError('BLINK_START_END_NOT_CANON')
    allow=np.zeros((H,W),bool)
    for x1,y1,x2,y2 in ROIS:allow[y1:y2,x1:x2]=True
    differences=np.any(allframes!=ref[None,:,:,:],axis=-1)
    if np.any(differences[:,~allow]):raise ValueError('OUTSIDE_EYES_CHANGED')
    if not np.array_equal(allframes[:,:,:,3],np.broadcast_to(ref[:,:,3],(15,H,W))):
        raise ValueError('ALPHA_CHANGED')
    if not np.array_equal(allframes[1:7],allframes[13:7:-1]):
        raise ValueError('REVERSE_OPEN_SEQUENCE_MISMATCH')
    changed=[int(differences[i,allow].sum()) for i in range(15)]
    if changed[7]==0:raise ValueError('CLOSED_FRAME_IDENTICAL_OPEN')
    if any(changed[i]==0 for i in [2,3,4,5,6,7]):
        raise ValueError('UNEXPECTED_EMPTY_CLOSING_STEP')
    unique=len(set(frame.tobytes() for frame in allframes))
    return dict(checkpoint='CP403',source_sha256=SOURCE_SHA,atlas_sha256=ATLAS_SHA,
                native_face_size=[W,H],atlas_size=[W*15,H],frames=15,
                changed_pixels_by_pose=changed,unique_frame_count=unique,
                outside_roi_changed=0,source_alpha_unchanged=True,
                open_source_exact=True,release='DRAFT_NOT_APPROVED',
                eyeblink_qa='AWAITING_ARTIST_AND_USER_VISUAL_ACCEPTANCE',
                device_test='NOT_PERFORMED',production_sprite_paths={})

def board(atlas, output):
    with Image.open(atlas) as a: a=a.convert('RGBA')
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    def font(size):
        try:return ImageFont.truetype(fontpath,size)
        except OSError:return ImageFont.load_default()
    cols=5; rows=3; scale=2; pad=22; gap=13; cellw=W*scale; cellh=H*scale
    header=92; foot=48
    full=Image.new('RGB',(2*pad+cols*cellw+(cols-1)*gap,
                          header+rows*(cellh+40)+(rows-1)*gap+foot),(19,38,53))
    draw=ImageDraw.Draw(full)
    draw.text((pad,14),'CP403 | LAM THIEN - 15 EXACT BLINK POSES FROM CP402',font=font(24),fill='white')
    draw.text((pad,47),'CANON-only draft: images are unmodified CP402 frames; not a painter-approved sprite.',font=font(16),fill=(245,213,174))
    for i in range(15):
        row,col=divmod(i,cols); x=pad+col*(cellw+gap); y=header+row*(cellh+40+gap)
        crop=a.crop((i*W,0,(i+1)*W,H)).convert('RGB')
        full.paste(crop.resize((cellw,cellh),Image.Resampling.NEAREST),(x,y))
        draw.text((x+3,y+cellh+7),f'FRAME {i:02}  /  {round(POSITIONS[i]*100):3}%',font=font(15),fill='white')
    draw.text((pad,full.height-foot+13),'Source identity pinned | eye-only edits | Android preview remains DEBUG ONLY',font=font(15),fill=(226,210,178))
    full.save(output)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--atlas',required=True);p.add_argument('--output',required=True);ar=p.parse_args()
    result=verify(ar.canon,ar.atlas)
    out=Path(ar.output);out.mkdir(parents=True,exist_ok=True)
    board(ar.atlas,out/'CP403_15_POSE_REVIEW_NOT_APPROVED.png')
    (out/'CP403_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
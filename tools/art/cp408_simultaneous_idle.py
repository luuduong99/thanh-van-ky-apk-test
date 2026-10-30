#!/usr/bin/env python3
"""CP408 exact-source debug-only simultaneous idle motion (NOT approved rig/art).

Source: user-approved Lâm Thiển CANON V2.1 941x1672. Never substitute art.
The small front pose is a crop of a CHARACTER SHEET, not a production sprite.
"""
from pathlib import Path
import argparse,hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import cv2

SHA_CANON='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
SOURCE_NAME='LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
FRONT=(16,180,224,623)  # 208 x 443, first standing/front pose on the sheet
EYES=((83,44,102,62),(105,44,125,62))  # local approximate eye regions; DRAFT only
POSE_COUNT=15
TIMER_SECONDS=4.7


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def get_source(path):
    path=Path(path)
    if path.name!=SOURCE_NAME or sha(path)!=SHA_CANON:
        raise ValueError('Refusing altered/mismatched Lâm Thiển CANON V2.1')
    im=Image.open(path).convert('RGBA')
    if im.size!=(941,1672):raise ValueError('Wrong exact CANON dimensions')
    return im


# The blink-channel timing remains separate from body motion but no new
# eyelid artwork is produced here. CP402/CP407 face studies are DRAFT, not
# spatially aligned with this tiny whole-body source crop.

def gaussian(x,center,sigma):return np.exp(-.5*((x-center)/sigma)**2)


def deform_mesh(frame,t,enabled=None):
    """CPU reference for Android procedural bitmap-mesh channels.
    All motion is one combined bitmap; without segmented art it's NOT articulated body rig.
    """
    enabled=enabled or ('breath','head','arms','hair','silk')
    src=np.asarray(frame.convert('RGB'))
    h,w=src.shape[:2]
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    u=xx/w;v=yy/h
    breath=np.sin(2*np.pi*t/3.8)
    head=np.sin(2*np.pi*t/6.2+.42)
    arms=np.sin(2*np.pi*t/5.3+.9)
    hair=np.sin(2*np.pi*t/5.7+.15)
    silk=np.sin(2*np.pi*t/4.5+.3)
    dx=np.zeros_like(u);dy=np.zeros_like(v)
    if 'breath' in enabled:
        torso=gaussian(v,.29,.13)*gaussian(u,.49,.22)
        dx+=(u-.49)*.010*breath*torso*w
        dy-=.0031*breath*torso*h
    if 'head' in enabled:
        headmask=gaussian(v,.13,.09)*gaussian(u,.50,.30)
        dx+=.0055*head*headmask*w
        dy+=.0013*head*headmask*h
    if 'arms' in enabled:
        arm=gaussian(v,.45,.19)*(gaussian(u,.19,.10)+gaussian(u,.81,.10))
        dx+=.0045*arms*arm*w
        dy+=.0011*arms*arm*h
    if 'hair' in enabled:
        strand=gaussian(v,.32,.29)*(gaussian(u,.14,.13)+gaussian(u,.89,.13))
        dx+=.0065*hair*strand*w
        dy+=.0009*hair*strand*h
    if 'silk' in enabled:
        hem=gaussian(v,.80,.23)*(gaussian(u,.15,.23)+gaussian(u,.84,.23))
        dx+=.0085*silk*hem*w
        dy+=.0014*silk*hem*h
    # positive flow means image moves right; sample from x-dx
    res=cv2.remap(src,xx-dx,yy-dy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(res,'RGB')


def select_pose(t):
    # short 0.24s blink around t % 4.7 = 1.55, all other times eyes open
    u=t%TIMER_SECONDS
    return min(14,int((u-1.55)/.24*15)) if 1.55<=u<1.79 else 0


def create(source, out,video=True):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    original=get_source(source)
    front=original.crop(FRONT)
    front.save(out/'CP408_CANON_FRONT_UNCHANGED_CROP.png')
    path=out/'CP408_CANON_FRONT_UNCHANGED_CROP.png'
    # Exactly zero edits to the original front source: no fake eyelid paint.
    assert np.array_equal(np.asarray(front),np.asarray(original.crop(FRONT)))
    # Contact sheet: exact front, 3 variants of combined idle, evidence-not-release.
    previews=[front.convert('RGB'),deform_mesh(front,1.63),deform_mesh(front,1.7),deform_mesh(front,3.0)]
    scale=2; margin=18; pad=10;head=84
    board=Image.new('RGB',(4*front.width*scale+5*pad,front.height*scale+head+2*pad),'#eaf1fa')
    d=ImageDraw.Draw(board)
    labels=['CANON V2.1 - exact front','Breath + head motion','Arms + hair (preview)','Silk + torso (preview)']
    for i,p in enumerate(previews):
        x=pad+i*(front.width*scale+pad)
        board.paste(p.resize((front.width*scale,front.height*scale),Image.Resampling.BICUBIC),(x,head))
        d.text((x+4,10),f'{i+1}. {labels[i]}',fill='#243856')
    d.text((pad,38),'CP408: BODY IDLE TECH DEMO / BLINK ART LOCKED / NOT A RIG',fill='#bd4a4a')
    board.save(out/'CP408_CANON_SIMULTANEOUS_MOTION_BOARD.png')
    # video split exact original vs. combined CPU reference from identical approved crop
    videopath=out/'CP408_SIMULTANEOUS_IDLE_30FPS_DRAFT.mp4'
    if video:
        fps=30;dur=5.0;tw=360;th=int(front.height*tw/front.width);m=26;hh=100
        writer=cv2.VideoWriter(str(videopath),cv2.VideoWriter_fourcc(*'mp4v'),fps,(tw*2+m*3,th+hh+20))
        if not writer.isOpened():raise RuntimeError('MP4 writer failed')
        constant=np.array(front.convert('RGB').resize((tw,th),Image.Resampling.BICUBIC))[:,:,::-1]
        for k in range(int(fps*dur)):
            t=k/fps
            moving=deform_mesh(front,t)
            current=cv2.resize(np.asarray(moving), (tw,th), interpolation=cv2.INTER_CUBIC)[:,:,::-1]
            frame=np.full((th+hh+20,tw*2+m*3,3), (246,238,227),np.uint8)
            frame[hh:hh+th,m:m+tw]=constant
            frame[hh:hh+th,m*2+tw:m*2+tw*2]=current
            cv2.putText(frame,'CANON V2.1 - SOURCE CROP',(m,30),cv2.FONT_HERSHEY_SIMPLEX,.53,(95,50,35),1,cv2.LINE_AA)
            cv2.putText(frame,'CP408 - BODY IDLE DRAFT',(m*2+tw,30),cv2.FONT_HERSHEY_SIMPLEX,.52,(95,50,35),1,cv2.LINE_AA)
            cv2.putText(frame,'Breath/head/arms/hair/silk in parallel',(m*2+tw,53),cv2.FONT_HERSHEY_SIMPLEX,.38,(92,82,75),1,cv2.LINE_AA)
            cv2.putText(frame, 'Debug mesh, no eyelid art / not an approved rig',(m,80),cv2.FONT_HERSHEY_SIMPLEX,.52,(50,50,145),1,cv2.LINE_AA)
            writer.write(frame)
        writer.release()
    data={
      'checkpoint':'CP408','source_sha256':SHA_CANON,'source_dimensions':[941,1672],
      'crop_rect':FRONT,'crop_dimensions':list(front.size),
      'crop_sha256':sha(path),
      'independent_motion_channels':['breath','head','arms','hair','silk'],
      'eye_blink_channel':'TIMELINE_DEFINED_BUT_NO_APPROVED_ILLUSTRATED_FRAMES',
      'technical_mode':'single-bitmap mesh, not layered rig','art_acceptance':'NOT_APPROVED',
      'sprite_paths':{},'apk_production':False,'physical_device_tested':False,
      'notes':'No source replacement, no fake eye overlays. Body motion channels combine on source crop. Independent anatomy/art rig, eyelid and Android device QA still missing.'
    }
    (out/'CP408_MANIFEST.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--out',required=True);args=parser.parse_args()
    print(json.dumps(create(args.source,args.out),ensure_ascii=False,indent=2))
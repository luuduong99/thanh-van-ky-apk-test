#!/usr/bin/env python3
"""CP410 source-locked synchronized review, NEVER a production layered rig.
The CP408 standing body and CP409 face expression are two different POSES in the
same CANON visual sheet. Rendering them side-by-side avoids an incorrect overlay.
"""
from pathlib import Path
import hashlib, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from cp408_simultaneous_idle import deform_mesh, get_source, FRONT

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
ATLAS_SHA = 'd9234630eab9e13ec07527e2c7b6fbbacd849117bf2e4983bf35ac4bcf73a07e'
FACE = (25, 684, 193, 881)
ATLAS_FRAME = (168,197)
FRAME_COUNT = 15
FPS = 30
DURATION = 4.8

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def sources(canon, atlas):
    source=get_source(canon)
    if sha(canon)!=CANON_SHA: raise ValueError('CANON exact SHA mismatch')
    if sha(atlas)!=ATLAS_SHA: raise ValueError('CP409 atlas SHA mismatch')
    a=Image.open(atlas).convert('RGBA')
    if a.size!=(FRAME_COUNT*ATLAS_FRAME[0],ATLAS_FRAME[1]): raise ValueError('Atlas size mismatch')
    if not np.array_equal(np.asarray(source.crop(FACE)),np.asarray(a.crop((0,0,*ATLAS_FRAME)))):
        raise ValueError('Atlas first pose is not the exact CANON face')
    return source,a

def smooth(x):
    x=max(0.0,min(1.0,x))
    return x*x*(3-2*x)

def pose_at(seconds):
    p=(seconds % 2.4)/2.4
    if p<.30:return 0
    if p<.355:return max(0,min(7,round(7*smooth((p-.30)/.055))))
    if p<.395:return 7
    if p<.455:return max(7,min(14,round(7+7*smooth((p-.395)/.060))))
    return 0

def compose_body_face(body, face, title=True):
    W,H=970,810
    im=Image.new('RGB',(W,H),'#e9eff6')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((24,95,490,770),radius=20,fill='#ffffff')
    d.rounded_rectangle((510,95,946,770),radius=20,fill='#ffffff')
    tw=304;th=round(tw*body.height/body.width)
    im.paste(body.convert('RGB').resize((tw,th),Image.Resampling.BICUBIC),(105,110))
    fw=344;fh=round(fw*face.height/face.width)
    im.paste(face.convert('RGB').resize((fw,fh),Image.Resampling.BICUBIC),(556,165))
    d.text((27,12),'THANH VAN KY — CP410 / SAME CLOCK DEBUG DEMO',fill='#1f3853',stroke_width=0)
    d.text((27,40),'CANON V2.1 locked  |  TWO DIFFERENT POSES  |  NOT A RIG',fill='#a33d3d')
    d.text((37,100),'BODY: CP408 5 channels in parallel',fill='#25476a')
    d.text((520,100),'FACE: CP409 geometric eyelids',fill='#25476a')
    d.text((520,127),'Different source pose; NEVER overlay on body',fill='#a33d3d')
    d.text((25,784),'DRAFT TECH REVIEW — ART QA & PHYSICAL DEVICE NOT APPROVED',fill='#af3e3e')
    return im

def build(canon,atlas,out,video=True):
    source,blink=sources(canon,atlas)
    body=source.crop(FRONT)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    orig=np.asarray(source); assert np.array_equal(orig,np.asarray(Image.open(canon)))
    keytimes=[0.,.77,.82,.86,.94,1.0,2.0]
    poses=[]
    for t in keytimes:
        p=pose_at(t)
        fm=blink.crop((p*168,0,(p+1)*168,197))
        poses.append((t,p,compose_body_face(deform_mesh(body,t),fm)))
    for i,(t,p,im) in enumerate(poses):
        im.save(out/f'CP410_SYNC_STAGE_{i:02}_POSE_{p:02}.png')
    grid=Image.new('RGB',(3*500+40,2*440+72),'#e9eff6')
    gg=ImageDraw.Draw(grid)
    gg.text((12,10),'CP410 / SHARED CLOCK  |  body and face from different CANON sheet locations',fill='#25476a')
    for i,(_,p,image) in enumerate(poses[1:7]):
        grid.paste(image.resize((490,408),Image.Resampling.BICUBIC),(10+(i%3)*500,50+(i//3)*428))
    grid.save(out/'CP410_SHARED_CLOCK_6_STAGES.png')
    videoPath=out/'CP410_SIMULTANEOUS_BODY_AND_EYE_DEBUG_30FPS.mp4'
    if video:
        vw=cv2.VideoWriter(str(videoPath),cv2.VideoWriter_fourcc(*'mp4v'),FPS,(970,810))
        if not vw.isOpened():raise RuntimeError('Video writer failed')
        for i in range(round(FPS*DURATION)):
            t=i/FPS
            p=pose_at(t)
            face=blink.crop((p*168,0,(p+1)*168,197))
            f=compose_body_face(deform_mesh(body,t),face)
            cv2.imwrite('/dev/null',np.asarray(f)) if False else None
            vw.write(cv2.cvtColor(np.asarray(f),cv2.COLOR_RGB2BGR))
        vw.release()
    report={
      'checkpoint':'CP410','canon_sha256':CANON_SHA,'cp409_atlas_sha256':ATLAS_SHA,
      'source_pose_regions':{'standing_fullbody':list(FRONT),'face_expression':list(FACE)},
      'face_matches_atlas_frame_zero':True,'same_character_but_different_pose':True,
      'synchronized_timebase_seconds':True,'blink_pose_count':FRAME_COUNT,
      'body_motion_tracks':['breath','head','arms','hair','silk'],
      'can_composite_face_directly_on_body':False,
      'true_rig_ready':False,'eyelid_art_approved':False,'physical_android_tested':False,
      'production_sprite_paths':{},'status':'DEBUG_SIDE_BY_SIDE_TWO_POSE_REVIEW'
    }
    (out/'CP410_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--atlas',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(build(a.canon,a.atlas,a.out),ensure_ascii=False,indent=2))
#!/usr/bin/env python3
"""CP409: CANON-exact, pupil occlusion by *moving eyelid geometry*, not composited closed-eye photos.

Non-production study. Native source: 168x197 px approved expression, so high fidelity is limited.
The original source PNG stays untouched. Draft images never enter production APK.
"""
from pathlib import Path
import argparse, hashlib, json, math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE=(941,1672); CROP=(25,684,193,881); FACE_SIZE=(168,197)
ROIS={'left':(29,93,71,124),'right':(83,70,129,110)}
UPPER={
 'left':[(31,107),(39,103.8),(53,99.8),(66,100.7)],
 'right':[(85,86.6),(97,79.5),(112,75.4),(125,77.8)]}
LOWER={
 'left':[(31,111),(41,119),(55,116),(67,108)],
 'right':[(85,92),(97,99),(113,94),(126,84)]}
PRODUCTION={'artist_approved':False,'blink_runtime_released':False,'sprite_paths':{},'physical_device_tested':False}


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def source(path):
 if sha(path)!=CANON_SHA: raise ValueError('CANON_SHA_MISMATCH')
 with Image.open(path) as im:
  if im.size!=CANON_SIZE or im.mode!='RGBA': raise ValueError('CANON_SIZE_MODE_MISMATCH')
  return im.crop(CROP).copy()

def bezier(p,t):
 a=np.asarray(p,np.float64)
 return (1-t)**3*a[0]+3*(1-t)**2*t*a[1]+3*(1-t)*t*t*a[2]+t**3*a[3]

def curve(side,x,curves):
 pts=np.asarray([bezier(curves[side],t) for t in np.linspace(0,1,1000)])
 return np.interp(x,pts[:,0],pts[:,1]).astype(np.float32)

def masks_and_base(src,scale=4):
 """One-time background reconstruction ONLY using approved source pixels.
    Fill the original visible pupil/upper lash area; physical edges drawn on top per frame.
 """
 orig=np.asarray(src)
 w,h=FACE_SIZE; H,W=h*scale,w*scale
 image=np.asarray(src.resize((W,H),Image.Resampling.BICUBIC))
 mask=np.zeros((H,W),np.uint8)
 roi4=np.zeros((H,W),np.uint8)
 for side,(x1,y1,x2,y2) in ROIS.items():
  roi4[y1*scale:y2*scale,x1*scale:x2*scale]=255
  xs=np.arange(x1*scale+2,x2*scale-2)/scale
  up=curve(side,xs,UPPER)
  lo=curve(side,xs,LOWER)
  for k,xs4 in enumerate(range(x1*scale+2,x2*scale-2)):
   ytop=max(y1*scale,round((up[k]-2.2)*scale));ybottom=min(y2*scale,round((lo[k]+2.4)*scale))
   mask[ytop:ybottom,xs4]=255
 # Inpaint local eye/iris to get base skin; source CANON ONLY.
 rgb=image[:,:,:3].copy()
 bg=cv2.inpaint(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR),mask,8*scale,cv2.INPAINT_TELEA)
 bg=cv2.cvtColor(bg,cv2.COLOR_BGR2RGB)
 # Preserve all pixels outside eye ROIs exactly, including alpha.
 base=image.copy()
 base[roi4>0,:3]=bg[roi4>0]
 base[:,:,3]=image[:,:,3]
 return image,base,roi4,mask

def lid_frame(src,progress,scale=4,cache=None):
 """Anatomical motion: pupil aperture is compressed, eyelid advances, its lashes FOLLOW edge.
    No closed-eye replacement bitmap or dissolve. Original image at both ends of blink.
 """
 progress=float(np.clip(progress,0,1))
 original=src.resize((src.width*scale,src.height*scale),Image.Resampling.BICUBIC)
 if progress<=0:return original.copy()
 raw,base,roi4,_=(cache if cache is not None else masks_and_base(src,scale))
 H,W=raw.shape[:2]
 out=raw.copy()
 # Coordinates relative native image, computed at display resolution to move boundary subpixel.
 for side,(x1,y1,x2,y2) in ROIS.items():
  xs4=np.arange(x1*scale+2,x2*scale-2)
  xs=(xs4+.5)/scale
  u=curve(side,xs,UPPER); l=curve(side,xs,LOWER)
  gap=np.maximum(0.8,l-u)
  # Narrow opening by upper eyelid moving down 82%, lower lid lifting 18%.
  upper_new=u+progress*.82*gap
  lower_new=l-progress*.18*gap
  # Maintain changed pixels inside ROI with spatial taper at eye corners.
  t=np.clip((xs-x1-2)/(x2-x1-4),0,1)
  corner=np.sin(t*np.pi)**.55
  upper_new=u+(upper_new-u)*corner
  lower_new=l+(lower_new-l)*corner
  for k,x4 in enumerate(xs4):
   yl=max(y1*scale,int((u[k]-2)*scale));yr=min(y2*scale,int((l[k]+3)*scale))
   if yl>=yr:continue
   y4=np.arange(yl,yr); y=(y4+.5)/scale
   e=float(upper_new[k]); bot=float(lower_new[k]); top=float(u[k]); bottom=float(l[k]);
   # 1) Track material points of the iris under narrowing aperture using a vertical remap.
   # This is *compression of the visible original aperture*, not fading eyes out.
   iris=(y>=e)&(y<bot)&(bot-e>.10)
   if np.any(iris):
    y_source=top+(y[iris]-e)*((bottom-top)/max(.1,bot-e))
    at=np.clip(y_source*scale,0,H-1)
    y0=np.floor(at).astype(int);y1s=np.minimum(y0+1,H-1);v=(at-y0)[:,None]
    px=raw[y0,x4,:3]*(1-v)+raw[y1s,x4,:3]*v
    out[y4[iris],x4,:3]=np.uint8(np.clip(np.round(px),0,255))
   # 2) Moving eyelid skin occludes visible pupil; use same-source cheek/eyelid inpaint.
   skin=(y>=top-2)&(y<e)
   if np.any(skin):out[y4[skin],x4,:3]=base[y4[skin],x4,:3]
   # Lower lid is slightly lifted and shares same CANON-derived skin.
   lower=(y>=bot)&(y<=bottom+.85)
   if np.any(lower):out[y4[lower],x4,:3]=base[y4[lower],x4,:3]
   # 3) Moving upper lash *edge*, source sampled along approved upper eyelid.
   # Dark tint is extracted from source lash root color (not substituted eye bitmap).
   edge_strength=progress**.55*corner[k]
   if edge_strength>.02:
    center=e
    tip_center=int(round(center*scale))
    if tip_center<y1*scale+1 or tip_center>=y2*scale-2:continue
    # Native upper-lash ink sampled near original line, with capped weight.
    upper_y=int(np.clip(round(top*scale),0,H-1))
    ink=raw[upper_y,x4,:3].astype(float)
    skinref=base[upper_y,x4,:3].astype(float)
    luminance=float(.299*ink[0]+.587*ink[1]+.114*ink[2]);darkness=np.clip((192-luminance)/130,.18,.78)
    color=skinref*(1-darkness*.76)+ink*(darkness*.76)
    # soft subpixel line, thicker at lateral corner, no opaque flat black stroke
    outer=(1-t[k]) if side=='left' else t[k]
    width=.34+.26*outer
    for jj in range(-2,3):
     yi=tip_center+jj
     if not (y1*scale<yi<y2*scale-1):continue
     dist=abs((yi+.5)/scale-center)
     a=math.exp(-.5*(dist/max(.12,width))**2)*edge_strength*.80
     if a>.002:out[yi,x4,:3]=np.uint8(np.clip(np.round(out[yi,x4,:3]*(1-a)+color*a),0,255))
 # Keep alpha source exact and outside ROIs EXACT native projection.
 out[:,:,3]=raw[:,:,3]
 out[roi4==0]=raw[roi4==0]
 return Image.fromarray(out,'RGBA')

def loop_progress(t):
 t=float(t)%1
 if t<.30:return 0.0
 if t<.355:
  v=(t-.30)/.055;return v*v*(3-2*v)
 if t<.395:return 1.0
 if t<.455:
  v=(t-.395)/.060;return 1-v*v*(3-2*v)
 return 0.0

def build(canon,out,scale=4):
 src=source(canon);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 cache=masks_and_base(src,scale)
 poses=[0,.15,.30,.45,.60,.75,.90,1.0,.90,.75,.60,.45,.30,.15,0]
 frames=[lid_frame(src,x,scale,cache) for x in poses]
 for i,im in enumerate(frames):im.save(out/f'pose_{i:02}.png')
 atlas=Image.new('RGBA',(len(frames)*src.width*scale,src.height*scale),(0,0,0,0))
 for i,img in enumerate(frames):atlas.alpha_composite(img,(i*src.width*scale,0))
 atlas.save(out/'CP409_15_POSE_4X_DETAIL_DRAFT.png')
 # Lightweight native-resolution atlas for an exact-hash Android debug viewer.
 # No extra HD pixels are claimed; preserve CANON outside ROI exactly.
 orig_native=np.asarray(src)
 native_atlas=Image.new('RGBA',(len(frames)*src.width,src.height),(0,0,0,0))
 for i,high in enumerate(frames):
  pix=(np.asarray(src).copy() if i in (0,len(frames)-1) else np.asarray(high.resize(FACE_SIZE,Image.Resampling.LANCZOS)).copy())
  outside=np.ones((src.height,src.width),bool)
  for x1,y1,x2,y2 in ROIS.values():outside[y1:y2,x1:x2]=False
  pix[outside]=orig_native[outside]
  pix[:,:,3]=orig_native[:,:,3]
  native_atlas.alpha_composite(Image.fromarray(pix,'RGBA'),(i*src.width,0))
 native_atlas.save(out/'CP409_15_POSE_NATIVE_SHA_LOCKED_DRAFT.png')
 src.save(out/'CP409_EXACT_CANON_FACE_NATIVE.png')
 sample_ids=[0,3,5,7,9,12,14];labels=['MỞ CANON','KHÉP 45%','KHÉP 75%','NHẮM','MỞ 75%','MỞ 30%','MỞ LẠI']
 # Compose poster with only exact original character, no generated alternatives.
 view_scale=3
 canv=Image.new('RGB',(len(sample_ids)*src.width*view_scale+8*(len(sample_ids)+1),src.height*view_scale+100),(17,30,44));d=ImageDraw.Draw(canv)
 for col,idx in enumerate(sample_ids):
  x=8+col*(src.width*view_scale+8)
  canv.paste(frames[idx].convert('RGB').resize((src.width*view_scale,src.height*view_scale),Image.Resampling.LANCZOS),(x,68))
  d.text((x,17),labels[col],fill=(246,238,213))
 d.text((8,44),'CP409 / SAME CANON / EYELID GEOMETRY DEMO / NOT ART APPROVED',fill=(233,181,130))
 canv.save(out/'CP409_CANON_LID_MOTION_7_STAGES.png')
 # MP4 preview assembled 72 frames, 30 fps; use lossless source PNG for QA.
 video=out/'CP409_EYELID_MOTION_30FPS_DEMO.mp4'
 writer=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*'mp4v'),30,(src.width*scale*2,src.height*scale))
 for i in range(72):
  left=src.resize((src.width*scale,src.height*scale),Image.Resampling.BICUBIC)
  right=lid_frame(src,loop_progress(i/72),scale,cache)
  rgb=np.concatenate([np.asarray(left.convert('RGB')),np.asarray(right.convert('RGB'))],axis=1)
  writer.write(cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR))
 writer.release()
 frames[0].save(out/'CP409_BLINK_DEMO.gif',save_all=True,append_images=frames[1:],duration=80,loop=0,disposal=2,optimize=True)
 manifest={'checkpoint':'CP409','purpose':'geometric eyelid motion avoiding closed-eye overlay','canon_sha256':CANON_SHA,'source_crop':CROP,'native_size':FACE_SIZE,'render_scale':scale,'pose_count':15,'frame_count':72,'fps':30,'native_atlas_sha256':sha(out/'CP409_15_POSE_NATIVE_SHA_LOCKED_DRAFT.png'),'key_poses':poses,'geometry':'moving_upper_and_lower_eyelids_plus_compressed_aperture_no_bitmap_crossfade','visual_qa':'NOT_APPROVED','release':PRODUCTION,'limitation':'Image detail remains based on 168x197 source crop, not a new HD painter master.'}
 (out/'CP409_REPORT.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 return manifest

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--canon',required=True);a.add_argument('--out',required=True);args=a.parse_args()
 print(json.dumps(build(args.canon,args.out),ensure_ascii=False,indent=2))
#!/usr/bin/env python3
"""CP401 CANON-locked eyelid-occlusion animation STUDY, not production art.

Unlike a crossfade, partial frames retain an exposed lower aperture and cover
upper iris/white pixels using skin sampled from the *same approved portrait*.
The closed-eye keyframe remains painter-review DRAFT and is not Android-ready.
"""
from pathlib import Path
import argparse, hashlib, json, io, zipfile
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CROP=(25,684,193,881); SIZE=(168,197); SRC_SIZE=(941,1672)
ROIS={'LEFT':(29,93,71,124),'RIGHT':(83,70,129,110)}
UPPER={
 'LEFT':[(31,107),(39,103.8),(53,99.8),(66,100.7)],
 'RIGHT':[(85,86.6),(97,79.5),(112,75.4),(125,77.8)]}
LOWER={
 'LEFT':[(31,111),(41,119),(55,116),(67,108)],
 'RIGHT':[(85,92),(97,99),(113,94),(126,84)]}
CLOSED={
 'LEFT':[(32.5,109.2),(39.8,106.15),(53.8,100.55),(66,101.9)],
 'RIGHT':[(85.7,88.25),(96,84),(113,77.05),(125.2,79.05)]}
RELEASE={'status':'blocked_pending_painter_approval','apk_ready':False,'sprite_paths':{},'rig_ready':False}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def exact_source(path):
 if sha(path)!=CANON_SHA:raise ValueError('CANON_SHA_MISMATCH')
 with Image.open(path) as im:
  if im.size!=SRC_SIZE or im.mode!='RGBA':raise ValueError('CANON_IMAGE_DIM_OR_MODE_INVALID')
  return im.crop(CROP).copy()
def bez(p,t):
 a=np.asarray(p,float)
 return (1-t)**3*a[0]+3*(1-t)**2*t*a[1]+3*(1-t)*t*t*a[2]+t**3*a[3]
_CURVE_CACHE = {}
def curve(side,x,points):
 key=(id(points),side)
 pp=_CURVE_CACHE.get(key)
 if pp is None:
  pp=np.array([bez(points[side],t) for t in np.linspace(0,1,300)])
  _CURVE_CACHE[key]=pp
 return float(np.interp(x,pp[:,0],pp[:,1]))
def valid_pixels_only(src,candidate):
 a=np.asarray(src);b=np.asarray(candidate)
 if a.shape!=b.shape:raise ValueError('SIZE_DRIFT')
 keep=np.ones((SIZE[1],SIZE[0]),bool)
 for x1,y1,x2,y2 in ROIS.values():keep[y1:y2,x1:x2]=False
 return int(np.any(a[keep]!=b[keep],axis=1).sum())
def feather_x(x,x1,x2):
 return float(np.clip((x-(x1+2))/3,0,1)*np.clip(((x2-3)-x)/3,0,1))

def sample_skin(src,side,x,y):
 """Re-use top eyelid / lower cheek pigment, never another character's face."""
 x1,y1,x2,y2=ROIS[side]
 upper=curve(side,x,UPPER); lower=curve(side,x,LOWER)
 yy1=int(np.clip(round(upper-7.5),y1-4,SIZE[1]-1))
 yy_mid=int(np.clip(round(upper-4.5),0,SIZE[1]-1))
 yy2=int(np.clip(round(lower+5),0,SIZE[1]-1))
 raw=np.asarray(src)
 a=raw[yy1,x,:3].astype(float); mid=raw[yy_mid,x,:3].astype(float);b=raw[yy2,x,:3].astype(float)
 # Mostly cheek skin with a modest upper-lid shadow at the drawn fold.
 v=float(np.clip((y-(upper-1))/max(5,lower-upper+2),0,1))
 fraction=.60*(1-v)+.45*v
 return np.uint8(np.clip(a*fraction+mid*.32+b*(.68-fraction),0,255))

def eyelid_art(src):
 """Eye-local inpaint from SAME CANON + tapered lash strokes; never releases art."""
 original=np.asarray(src).copy()
 h,w=SIZE[1],SIZE[0]
 mask=np.zeros((h,w),np.uint8)
 for side,(x1,y1,x2,y2) in ROIS.items():
  for x in range(x1+3,x2-3):
   u=curve(side,x,UPPER); l=curve(side,x,LOWER)
   ytop=max(y1,int(np.floor(u-3.0))); ybottom=min(y2,int(np.ceil(l+5.0)))
   mask[ytop:ybottom,x]=255
 # Telea inpainting is offline: it samples ONLY pixels of the exact CANON.
 # This removes vertical columns from source skin re-projection in CP400.
 rgb=cv2.cvtColor(cv2.inpaint(cv2.cvtColor(original[:,:,:3],cv2.COLOR_RGB2BGR),mask,7,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
 feather=cv2.GaussianBlur(mask,(3,3),1.3).astype(float)/255.
 feather[mask==0]=0.
 result=original.copy()
 result[:,:,:3]=np.uint8(np.rint(original[:,:,:3]*(1-feather[:,:,None])+rgb*feather[:,:,None]))
 # Transparent editable paint layer at 12x subpixel sampling; tapered ends.
 S=12
 hi=Image.new('RGBA',(w*S,h*S),(0,0,0,0));p=ImageDraw.Draw(hi)
 for side,(x1,y1,x2,y2) in ROIS.items():
  xmin=x1+3; xmax=x2-3
  for x in np.arange(xmin,xmax,.10):
   position=(x-xmin)/max(1,xmax-xmin)
   taper=max(0.,np.sin(np.pi*position))**.42
   if taper<.012:continue
   y=curve(side,x,CLOSED)
   outer=1-position if side=='LEFT' else position
   thickness=(.72+.56*outer)*taper
   # Original iris is completely occluded by real skin pixels first.
   # The warm ink tint is chosen to match the CANON upper lash palette.
   alpha=round(220*taper)
   p.ellipse(((x-thickness/2)*S,(y-thickness/2)*S,(x+thickness/2)*S,(y+thickness/2)*S),fill=(65,34,48,alpha))
  ts=[.06,.14,.22] if side=='LEFT' else [.78,.86,.94]
  for i,t in enumerate(ts):
   x,y=bez(CLOSED[side],t)
   dx=(-.55 if side=='LEFT' else .55)*(1.0-.10*i)
   dy=-.55-.12*i
   p.line([(int(x*S),int(y*S)),(int((x+dx)*S),int((y+dy)*S))],fill=(73,38,54,150),width=max(1,round(.25*S)))
  # exceptionally subtle crease/shadow just above the lid line
  path=[bez(CLOSED[side],float(t)) for t in np.linspace(.13,.87,130)]
  p.line([(round(x*S),round((y-2.65)*S)) for x,y in path],fill=(152,82,104,31),width=max(1,round(.36*S)))
 ov=np.asarray(hi.resize((w,h),Image.Resampling.LANCZOS))
 # Composite ONLY inside two ROIs and copy alpha from CANON exactly.
 for side,(x1,y1,x2,y2) in ROIS.items():
  co=ov[y1:y2,x1:x2].astype(float)
  dest=result[y1:y2,x1:x2].astype(float)
  k=co[:,:,3:4]/255.
  result[y1:y2,x1:x2,:3]=np.uint8(np.rint(np.clip(dest[:,:,:3]*(1-k)+co[:,:,:3]*k,0,255)))
 result[:,:,3]=original[:,:,3]
 output=Image.fromarray(result,'RGBA')
 if valid_pixels_only(src,output):raise AssertionError('EYE_ONLY_CONTRACT_BROKEN')
 return output

def eyelid_position(src,closed,progress):
 """Partial eye is geometrically covered from upper edge downward.

No dissolve of white iris pixels. At 0 and 1, preserve exact CANON / closed
keyframes. Interior eye aperture narrows and natural skin slides over it.
"""
 progress=float(np.clip(progress,0,1))
 if progress<=0:return src.copy()
 if progress>=1:return closed.copy()
 source=np.asarray(src);a=source.copy();z=np.asarray(closed)
 for side,(x1,y1,x2,y2) in ROIS.items():
  for x in range(x1+2,x2-2):
   u=curve(side,x,UPPER);l=curve(side,x,LOWER)
   # downward moving edge, at late stages quickly replace the last iris sliver
   # with already painted eye closure rather than fading iris into skin.
   boundary=u+max(0,l-u)*progress
   taper=feather_x(x,x1,x2)
   for y in range(y1,y2):
    # erase interior starting from the top, without any ghostly doubled pupil
    if y < u-1.8:continue
    mask=float(np.clip((boundary-y+.8)/1.25,0,1))*taper
    if mask<=0:continue
    # The same-source cheek pigment in the painted endpoint now covers the top.
    a[y,x,:3]=np.uint8(np.rint(a[y,x,:3]*(1-mask)+z[y,x,:3]*mask))
   # Animate a narrow upper-lash edge at the moving boundary, not a second iris.
   if progress>.10:
    yy=int(np.clip(round(boundary),y1+1,y2-2))
    # darkness rises as eyelid covers more area; only a local 1px lash trace.
    fade=progress*(1-progress)*.85*taper
    if fade>.01:
     for dy in [0]:
      y=yy+dy
      source_rgb=source[y,x,:3].astype(float)
      tint=np.asarray([73,40,59],float)
      a[y,x,:3]=np.uint8(np.rint(source_rgb*(1-fade)+tint*fade))
 # At near closure, swap the last exposed eye pixels for the authentic painted
 # close keyframe. This only affects inside the two ROIs.
 late=float(np.clip((progress-.82)/.18,0,1))
 if late:
  late=late*late*(3-2*late)
  for x1,y1,x2,y2 in ROIS.values():
   a[y1:y2,x1:x2,:3]=np.uint8(np.rint(a[y1:y2,x1:x2,:3]*(1-late)+z[y1:y2,x1:x2,:3]*late))
 out=Image.fromarray(a,'RGBA')
 if valid_pixels_only(src,out):raise AssertionError('EYE_REGION_ESCAPE')
 return out

def frame_progress(t):
 """T in [0,1] of a 2.4s loop: one quick blink, rest open."""
 t=float(t)%1
 if t<.31:return 0.
 if t<.355:
  v=(t-.31)/.045;return v*v*(3-2*v)
 if t<.395:return 1.
 if t<.46:
  v=(t-.395)/.065;return 1-v*v*(3-2*v)
 return 0.

def render_sequence(src,closed,count=72):
 frames=[eyelid_position(src,closed,frame_progress(i/count)) for i in range(count)]
 assert valid_pixels_only(src,frames[0])==0
 return frames

def make_panel(src,closed,frames,path):
 scale=4;w,h=SIZE;top=86;gap=16;pad=20
 title='CP401 | LAM THIEN / CANON BLINK OCCLUSION / DRAFT ONLY'
 samples=[('OPEN / CANON',src),('CLOSING 60%',eyelid_position(src,closed,.6)),('CLOSED / DRAFT',closed),('OPENING 40%',eyelid_position(src,closed,.4))]
 bg=Image.new('RGB',(len(samples)*w*scale+(len(samples)-1)*gap+pad*2,top+h*scale+70),(15,36,55));d=ImageDraw.Draw(bg)
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 f1=ImageFont.truetype(font,25);f2=ImageFont.truetype(font,14)
 d.text((pad,20),title,fill='white',font=f1)
 d.text((pad,51),'Exact approved source outside BOTH eye ROIs; still requires painter QA / Android runtime test.',fill=(255,214,178),font=f2)
 for i,(label,im) in enumerate(samples):
  x=pad+i*(w*scale+gap);bg.paste(im.convert('RGB').resize((w*scale,h*scale),Image.Resampling.NEAREST),(x,top))
  d.text((x,top+h*scale+15),label,font=f2,fill='white')
 bg.save(path)

def build(canon,output):
 src=exact_source(canon)
 closed=eyelid_art(src)
 # create output only AFTER source verified
 out=Path(output);out.mkdir(parents=True,exist_ok=True)
 closed.save(out/'CP401_CLOSED_EYE_REPAINT_DRAFT_NOT_APPROVED.png')
 src.save(out/'CP401_CANON_PIXEL_EXACT_168x197.png')
 poses=[0,.15,.3,.45,.60,.75,.90,1,.90,.75,.60,.45,.30,.15,0]
 pdir=out/'poses';pdir.mkdir(exist_ok=True)
 for i,p in enumerate(poses):eyelid_position(src,closed,p).save(pdir/f'pose_{i:02d}.png')
 atlas=Image.new('RGBA',(SIZE[0]*len(poses),SIZE[1]),(0,0,0,0))
 for i,p in enumerate(poses):atlas.alpha_composite(eyelid_position(src,closed,p),(SIZE[0]*i,0))
 atlas.save(out/'CP401_POSE_ATLAS_DRAFT.png')
 loop=render_sequence(src,closed)
 # Smooth 30fps video; GIF preview uses finite subset to reduce size
 preview=[loop[k] for k in range(0,72,2)]
 preview[0].save(out/'CP401_BLINK_PREVIEW.apng.png',save_all=True,append_images=preview[1:],duration=67,loop=0,disposal=2,default_image=False)
 preview[0].save(out/'CP401_BLINK_PREVIEW.gif',save_all=True,append_images=preview[1:],duration=67,loop=0,disposal=2,optimize=False)
 # video frames at 30fps (source-sized; user-facing enlarged video made separately)
 vf=out/'video_frames';vf.mkdir(exist_ok=True)
 for i,img in enumerate(loop):img.save(vf/f'frame_{i:03}.png')
 make_panel(src,closed,loop,out/'CP401_CANON_OCCLUSION_REVIEW.png')
 report={'checkpoint':'CP401','kind':'source_locked_shaped_blink_study','canon_sha256':CANON_SHA,'native_crop':list(CROP),'native_size':list(SIZE),'eye_rois':ROIS,'pose_count':len(poses),'loop_frames':len(loop),'loop_fps':30,'outside_eye_changes':valid_pixels_only(src,closed),'closed_changed_pixels':int(np.any(np.asarray(src)!=np.asarray(closed),axis=2).sum()),'blink_transition':'geometric_skin_occlusion_not_simple_crossfade','closed_keyframe_method':'same_CANON_only_inpaint_plus_tapered_lashes','visual_qa':'NOT_APPROVED','production_release':RELEASE,'limitations':['Closed keyframe inpainted from original CANON with computer-drawn lashes; still not painter-approved.', 'Native expression region only 168x197, resampling cannot create original HD detail.','No official Android sprite registration, APK QA, Spine or physics performed.']}
 (out/'CP401_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True);args=p.parse_args()
 print(json.dumps(build(args.canon,args.out),ensure_ascii=False,indent=2))
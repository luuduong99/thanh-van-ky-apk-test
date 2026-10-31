#!/usr/bin/env python3
"""Source-locked Lâm Thiển blink art study, staged for human visual QA.

Creates true eye-only editable paint layers, intermediate frames, APNG and GIF.
Standalone preview is NOT production runtime approval.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from xml.etree import ElementTree as ET
import numpy as np
import hashlib, io, json, zipfile, math

CANON_HASH='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CP398_SOFT_SHA='5ce4ab198235a58905d8f867f53973d7d49d3e9686bb769675568d454c142c17'
SRC_SIZE=(941,1672); CROP=(25,684,193,881); NATIVE=(168,197)
ROIS={'LEFT':(29,93,71,124),'RIGHT':(83,70,129,110)}
BEZ={
'LEFT':[(32.5,109.2),(39.8,106.15),(53.8,100.55),(66.0,101.9)],
'RIGHT':[(85.7,88.25),(96.0,84.0),(113.0,77.05),(125.2,79.05)]}
LOWER={
'LEFT':[(31,111),(41,119),(55,116),(67,108)],
'RIGHT':[(85,92),(97,99),(113,94),(126,84)]}

N=12

def hash_bytes(b): return hashlib.sha256(b).hexdigest()
def sha(p):return hash_bytes(Path(p).read_bytes())
def load_canon(path):
 if sha(path)!=CANON_HASH: raise ValueError('CANON_SHA256_REJECTED')
 im=Image.open(path)
 if im.size!=SRC_SIZE or im.mode!='RGBA':raise ValueError('CANON_DIMENSIONS_MODE_REJECTED')
 return im.crop(CROP).copy()
def bez(side,t,kind='upper'):
 pts=np.asarray(BEZ[side] if kind=='upper' else LOWER[side],np.float64)
 return (1-t)**3*pts[0]+3*(1-t)**2*t*pts[1]+3*(1-t)*t*t*pts[2]+t**3*pts[3]
def line_at(side,x,kind='upper'):
 v=np.asarray([bez(side,t,kind) for t in np.linspace(0,1,400)])
 return float(np.interp(x,v[:,0],v[:,1]))
def clip_eye(arr,side):
 b=np.zeros_like(arr);x1,y1,x2,y2=ROIS[side];b[y1:y2,x1:x2]=arr[y1:y2,x1:x2]
 return b

def paint_eyes(src, previous):
 # CP398 SOFT is a source-locked closed-eye draft; refine its broad gray lash
 # to a tapered warm eyelid pigment with donor skin from same CANON face.
 a=np.asarray(src,dtype=np.uint8); old=np.asarray(previous,dtype=np.uint8)
 h,w=a.shape[:2]
 retouch=np.zeros((h,w,4),np.uint8)
 for side,(x1,y1,x2,y2) in ROIS.items():
  for x in range(x1+2,x2-2):
   yline=line_at(side,x)
   xe=float(np.clip(min((x-x1-2)/6,(x2-2-x)/6),0,1))
   if xe<=0:continue
   # Local blend from original same-expression cheek *below* eye.
   cy=int(np.clip(round(yline+8),y1+4,y2-3))
   source_skin=old[cy,x,:3].astype(float)
   deep_skin=old[y2+2,x,:3].astype(float)
   donor=source_skin*.78+deep_skin*.22
   for y in range(y1,y2):
    dy=y-yline
    envelope=np.exp(-.5*((dy-.6)/3.0)**2)
    alpha=min(.995, 1.23*xe*envelope)
    if alpha<.006:continue
    prev_col=old[y,x,:3].astype(float)
    # shade fades below the lid and adds natural rosy boundary tint
    pink=np.array([0.,2.5,4.]) * np.exp(-.5*((dy-1.8)/2.7)**2)
    target=np.clip(donor-pink,0,255)
    retouch[y,x,:3]=target.astype('uint8')
    retouch[y,x,3]=round(alpha*255)
 under=Image.fromarray(retouch,'RGBA');face=previous.copy();face.alpha_composite(under)
 layers={'UNDERPAINT':under}
 for category in ('SHADOW','CREASE','LASH'):
  high=Image.new('RGBA',(w*N,h*N),(0,0,0,0));d=ImageDraw.Draw(high)
  for side in ROIS:
   coords=[tuple(bez(side,t)*N) for t in np.linspace(.045,.955,160)]
   if category=='SHADOW':
    d.line([(x,y+1.4*N) for x,y in coords],fill=(165,91,103,34),width=round(1.7*N))
   elif category=='CREASE':
    d.line([(x,y-2.8*N) for x,y in coords],fill=(136,77,110,37),width=round(.55*N))
   elif category=='LASH':
    d.line(coords,fill=(75,36,55,244),width=round(1.10*N))
    d.line([(x,y-.15*N) for x,y in coords],fill=(116,64,79,80),width=max(1,round(.38*N)))
    ts=([.075,.14,.21,.29] if side=='LEFT' else [.73,.81,.88,.94])
    for j,t in enumerate(ts):
     pt=bez(side,t);direction=(-1 if side=='LEFT' else 1)
     dx=direction*(.5+(.18*j));dy=-(.6+.12*j)
     c=(pt[0]*N,pt[1]*N);end=((pt[0]+dx)*N,(pt[1]+dy)*N)
     d.line([c,end],fill=(89,44,64,130),width=max(1,round(.32*N)))
  if category=='SHADOW':high=high.filter(ImageFilter.GaussianBlur(6))
  elif category=='CREASE':high=high.filter(ImageFilter.GaussianBlur(3))
  mat=np.asarray(high.resize((w,h),Image.Resampling.LANCZOS)).copy()
  mat[:]=np.maximum(0,sum([clip_eye(mat,side).astype('int16') for side in ROIS])).clip(0,255).astype('uint8')
  layer=Image.fromarray(mat,'RGBA');layers[category]=layer;face.alpha_composite(layer)
 # Pixel-exact original lash-root pigment, copied only from the approved CANON.
 # Narrow coverage avoids restoring underlying iris or eye-white.
 pigment=np.zeros((h,w,4),np.uint8)
 for side,(x1,y1,x2,y2) in ROIS.items():
  for x in range(x1+2,x2-2):
   xx=float(np.clip(min((x-x1-2)/6,(x2-2-x)/6),0,1))
   edge=line_at(side,x)
   for y in range(y1,y2):
    coverage=.32*xx*math.exp(-.5*((y-edge+.32)/.55)**2)
    if coverage>.008:
     pigment[y,x,:3]=a[y,x,:3]
     pigment[y,x,3]=round(coverage*255)
 source_lash=Image.fromarray(pigment,'RGBA')
 layers['CANON_LASH_ROOT']=source_lash
 face.alpha_composite(source_lash)
 return face,layers,None

def limit_check(src,im):
 a=np.asarray(src);b=np.asarray(im)
 outside=np.ones((NATIVE[1],NATIVE[0]),bool)
 for x1,y1,x2,y2 in ROIS.values():outside[y1:y2,x1:x2]=False
 return int(np.any(a[outside]!=b[outside],axis=1).sum())

def sequence(src,closed,steps=9):
 a=np.asarray(src).astype(np.float32);z=np.asarray(closed).astype(np.float32)
 if steps<3:raise ValueError('steps')
 # ease to a quick narrow closed pose; rest mainly open for natural blinking
 phases=[0,.13,.42,.80,1.,.94,.57,.20,0]
 result=[]
 for v in phases:
  # Artistic timed in-betweens: same-eye source cross-fade, with occlusion
  # at eye ROIs only; not a genuine skeletal eyelid simulation.
  k=v*v*(3-2*v)
  out=np.uint8(np.rint(np.clip(a*(1-k)+z*k,0,255)))
  eye_mask=np.zeros((NATIVE[1],NATIVE[0]),dtype=bool)
  for x1,y1,x2,y2 in ROIS.values():eye_mask[y1:y2,x1:x2]=True
  out[~eye_mask]=np.asarray(src)[~eye_mask]
  result.append(Image.fromarray(out,'RGBA'))
 return result

def png(im):
 bio=io.BytesIO();im.save(bio,format='PNG');return bio.getvalue()

def openraster(src,closed,layers,path):
 desc=[('CANON V2.1 original source / visible',src,True)]
 desc += [(f'CP400 {k} / review draft / hidden',v,False) for k,v in layers.items()]
 desc.append(('CP400 composite / review draft / hidden',closed,False))
 root=ET.Element('image',{'w':'168','h':'197','version':'0.0.3','name':'TVK CP400 source-locked blink paint draft'});stack=ET.SubElement(root,'stack')
 with zipfile.ZipFile(path,'w') as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for i,(name,img,visible) in enumerate(desc):
   addr=f'data/layer_{i:02}.png';z.writestr(addr,png(img))
   ET.SubElement(stack,'layer',{'name':name,'src':addr,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
  z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True));z.writestr('mergedimage.png',png(src))
 with zipfile.ZipFile(path) as z:assert z.testzip() is None
 return len(desc)

def board(src,closed,frames,path):
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';fh=ImageFont.truetype(font,27);f=ImageFont.truetype(font,16)
 scale=4; imw,imh=(NATIVE[0]*scale,NATIVE[1]*scale);pad=32;gap=20;top=110
 a=[('CANON — GỐC',src),('CP400 — MẮT NHẮM (CHƯA DUYỆT)',closed),('IN-BETWEEN 03/09',frames[2]),('IN-BETWEEN 07/09',frames[6])]
 out=Image.new('RGB',(2*pad+4*imw+3*gap,top+imh+110),(13,33,52));d=ImageDraw.Draw(out)
 d.text((pad,18),'TVK / LÂM THIỂN — CP400: BỘ KHUNG CHỚP MẮT',font=fh,fill='white')
 d.text((pad,62),'Vẽ từ 1 CANON; không đổi da/tóc/trang phục ngoài mắt. Ảnh draft, CHƯA DUYỆT.',font=f,fill=(255,218,186))
 for i,(label,img) in enumerate(a):
  x=pad+i*(imw+gap);out.paste(img.convert('RGB').resize((imw,imh),Image.Resampling.NEAREST),(x,top));d.text((x,top+imh+16),label,font=f,fill='white')
 d.text((pad,out.height-37),'Frame được dựng để test nhịp chuyển động — chưa phải atlas đã được nghiệm thu nghệ thuật.',font=f,fill=(255,218,186))
 out.save(path)

def build(canon,previous_path,outdir):
 src=load_canon(canon)
 if sha(previous_path)!=CP398_SOFT_SHA:raise ValueError('CP398_SOFT_SOURCE_SHA_MISMATCH')
 previous=Image.open(previous_path).convert('RGBA')
 if previous.size!=NATIVE or limit_check(src,previous)!=0:raise ValueError('CP398_NON_CANON_PIXELS')
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 closed,layers,_=paint_eyes(src,previous)
 frames=sequence(src,closed)
 if limit_check(src,closed)!=0 or any(limit_check(src,f)!=0 for f in frames):raise RuntimeError('Outside CANON eyes changed')
 if not np.array_equal(np.asarray(src),np.asarray(frames[0])) or not np.array_equal(np.asarray(src),np.asarray(frames[-1])):raise RuntimeError('open frame mismatch')
 src.save(out/'CP400_CANON_EXACT_FACE.png');closed.save(out/'CP400_CLOSED_EYE_ART_DRAFT.png')
 for k,v in layers.items():v.save(out/f'CP400_LAYER_{k}_DRAFT.png')
 fdir=out/'frames';fdir.mkdir(exist_ok=True)
 for i,f in enumerate(frames):f.save(fdir/f'blink_{i:02}.png')
 timing=[900,35,35,65,90,35,45,35,40] # ms; 1.28 sec repeating (can hold open longer)
 frames[0].save(out/'CP400_BLINK_PREVIEW.gif',save_all=True,append_images=frames[1:],duration=timing,loop=0,disposal=2,optimize=False)
 frames[0].save(out/'CP400_BLINK_PREVIEW.png',save_all=True,append_images=frames[1:],duration=timing,loop=0,disposal=2,default_image=False)
 # Spritesheet (visual QA/preflight); no in-game registration until art signoff.
 sheet=Image.new('RGBA',(NATIVE[0]*len(frames),NATIVE[1]),(0,0,0,0))
 for i,img in enumerate(frames):sheet.alpha_composite(img,(i*NATIVE[0],0))
 sheet.save(out/'CP400_BLINK_FRAMES_ATLAS_DRAFT.png')
 openraster(src,closed,layers,out/'CP400_CANON_REPAINT_EDITABLE_DRAFT.ora')
 board(src,closed,frames,out/'CP400_CANON_VS_BLINK_REVIEW.png')
 info={'checkpoint':'CP400','source_sha256':CANON_HASH,'crop':CROP,'native_size':NATIVE,'eye_rois':ROIS,
 'cp398_soft_sha256':CP398_SOFT_SHA,'frames':len(frames),'timing_ms':timing,'changed_outside_eyes':limit_check(src,closed),
 'closed_changed_pixels':int(np.any(np.asarray(src)!=np.asarray(closed),axis=2).sum()),
 'status':'ANIMATED_TECHNICAL_PREVIEW_ONLY','visual_qa':'PENDING_USER_APPROVAL',
 'ready_for_apk':False,'limitations':['Native eye crop is 168x197: detail is constrained by original CANON resolution.','Inbetween frames use source-locked eye-only blending; not a fully hand-painted eyelid mesh.', 'Do not insert into expression catalog without approving close-eye art.']}
 (out/'CP400_REPORT.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
 return info

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--prior',required=True);p.add_argument('--out',required=True);a=p.parse_args(); print(json.dumps(build(a.canon,a.prior,a.out),ensure_ascii=False,indent=2))
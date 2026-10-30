#!/usr/bin/env python3
"""CP394 exact-CANON eye closure study. DRAFT only; release BLOCKED.

This is *not* painter-grade redraw. The original CANON eye line is kept
and the hidden iris is occluded with a feathered same-source donor field.
All candidates remain hidden in the editable OpenRaster master.
"""
from __future__ import annotations
import argparse,hashlib,json,io,zipfile,shutil
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFilter,ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CROP=(25,684,193,881); SIZE=(168,197)
# Conservative source-coordinate eye ROIs. No changes outside.
ROIS={'LEFT':(29,93,71,124),'RIGHT':(83,70,129,110)}
GEOM={
 'LEFT': {'upper':[(31,107),(39,103.8),(53,99.8),(66,100.7)], 'lower':[(31,111),(41,119),(55,116),(67,108)], 'lash':[(31,106.6),(41,103.4),(55,100.3),(66,100.5)]},
 'RIGHT':{'upper':[(85,86.6),(97,79.5),(112,75.4),(125,77.8)], 'lower':[(85,92),(97,99),(113,94),(126,84)], 'lash':[(85,85.9),(97,80.7),(113,76.9),(125,77.7)]}
}
RELEASE={'status':'blocked_pending_art','sprite_paths':{},'spine_ready':False,'apk_ready':False}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def checked_canon(p):
 if sha(p)!=CANON_SHA: raise ValueError('CANON_SHA_MISMATCH')
 im=Image.open(p)
 if im.size!=(941,1672) or im.mode!='RGBA':raise ValueError('CANON_DIMENSIONS_INVALID')
 return im.crop(CROP).copy()
def bez(points,t):
 p=np.array(points,dtype=np.float64)
 return (1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3]
def curve_at(pts,x):
 samples=np.array([bez(pts,t) for t in np.linspace(0,1,300)])
 return np.interp(x,samples[:,0],samples[:,1])
def gauss(v,s):return np.exp(-0.5*(v/s)**2)

def make_layers(source,side):
 src=np.array(source,dtype=np.uint8);H,W=src.shape[:2]
 geom=GEOM[side];x1,y1,x2,y2=ROIS[side]
 # Output premultiplied alpha compositing; manually reconstruct real color samples
 # from actual portrait cheek below the iris. Never pull samples from iris.
 up=np.zeros((H,W),np.float32);las=np.zeros_like(up);lo=np.zeros_like(up)
 for x in range(x1,x2):
  up[:,x]=curve_at(geom['upper'],x)
  las[:,x]=curve_at(geom['lash'],x)
  lo[:,x]=max(curve_at(geom['lower'],x),float(up[0,x])+4.8)
 Y,X=np.indices((H,W)); masks=np.zeros((H,W),np.float32)
 # soft edge at corners and lower lid, protected lash root zone
 for x in range(x1+1,x2-1):
  yy=Y[:,x].astype(float)
  u=up[0,x];b=min(lo[0,x]+4.8,y2-1)
  # Keep natural upper lash colors up to 0.9px below its reference contour.
  top=u+(-1.6 if side=='LEFT' else .75)
  wt=np.clip((yy-top)/1.35,0,1)*np.clip((b-yy)/2.6,0,1)
  xt=np.clip((x-x1-1)/2.1,0,1)*np.clip((x2-x-2)/2.1,0,1)
  masks[:,x]=wt*xt
 # A slight blur avoids hard local masks; clip to ROIs strictly afterwards
 mask_img=Image.fromarray(np.uint8(np.clip(masks*255,0,255)),'L').filter(ImageFilter.GaussianBlur(.6))
 alpha=np.array(mask_img,dtype=np.uint8);alpha[:y1,:]=0;alpha[y2:,:]=0;alpha[:,:x1]=0;alpha[:,x2:]=0
 donor=np.zeros_like(src); donor[:,:,3]=alpha
 # Texture-preserving skin colors are sampled in each column below the eye;
 # avoid source eye whites/iris and do not simply paint constant peach.
 for x in range(x1,x2):
  u=float(up[0,x]);b=max(float(lo[0,x]),u+4.8)
  for y in range(y1,y2):
   if alpha[y,x]==0: continue
   t=np.clip((y-u)/max(3.0,b-u+3),0,1)
   dy=int(round(np.clip(b+6 + .45*(y-u), y1+4, min(y2+17,H-2))))
   # Make sure sample comes from facial skin, not a lash or hair strand.
   dx=int(np.clip(x+(2 if side=='LEFT' else -2),0,W-1))
   pix=src[dy,dx,:3].astype(float)
   # low-frequency shading from upper skin is blended for realistic gradient.
   uy=int(np.clip(round(u-6),0,H-1))
   top=src[uy,x,:3].astype(float)
   mix=.16*(1-t)**2
   color=pix*(1-mix)+top*mix
   # subtle soft darkening adjacent to the lash edge
   shade=2.9*np.exp(-((y-(u+2.7))/2.5)**2)
   color=np.clip(color-[shade*.55,shade*.95,shade*.85],0,255)
   donor[y,x,:3]=color.astype('uint8')
 # Preserve the CANON eyelash pixels by source overlay, *not* generated black strokes.
 # Exact source lash strip is reintroduced with a curve-guided soft mask.
 lash=np.zeros_like(src)
 la=np.zeros((H,W),np.float32)
 for x in range(x1+1,x2-1):
  u=float(las[0,x]); yv=Y[:,x].astype(float)
  # Narrow band over the original line and fine lash tips.
  weight=np.clip(gauss(yv-u,.93)*.91+gauss(yv-(u-1.9),1.15)*.28,0,1)
  # soft taper at both ends
  weight*=np.clip((x-x1-1)/2,0,1)*np.clip((x2-x-2)/2,0,1)
  la[:,x]=weight
 lash[:,:,:3]=src[:,:,:3]
 lash[:,:,3]=np.uint8(np.clip(la*255,0,255))
 lash[:y1,:,3]=0;lash[y2:,:,3]=0;lash[:,:x1,3]=0;lash[:,x2:,3]=0
 # Thin lavender lid crease, harmonized to surrounding source shadows.
 shadow=Image.new('RGBA',SIZE,(0,0,0,0));d=ImageDraw.Draw(shadow)
 scale=4
 hi=Image.new('RGBA',(W*scale,H*scale),(0,0,0,0)); dh=ImageDraw.Draw(hi)
 pts=[bez(geom['upper'],float(t)) for t in np.linspace(.05,.95,140)]
 # translucent, not a thick black vector line
 dh.line([(round(p[0]*scale),round((p[1]-2.65)*scale)) for p in pts],fill=(121,72,90,51),width=3)
 sh=hi.resize(SIZE,Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(.7));ar=np.asarray(sh).copy()
 ar[:y1,:,3]=0;ar[y2:,:,3]=0;ar[:,:x1,3]=0;ar[:,x2:,3]=0
 return {'SKIN':Image.fromarray(donor,'RGBA'),'CANON_LASH':Image.fromarray(lash,'RGBA'),'CREASE':Image.fromarray(ar,'RGBA')}

def composite(src,layers,mode='closed'):
 out=src.copy()
 for side in ('LEFT','RIGHT'):
  out.alpha_composite(layers[side]['SKIN'])
  out.alpha_composite(layers[side]['CANON_LASH'])
  if mode=='closed':out.alpha_composite(layers[side]['CREASE'])
 return out

def outside_changes(src,candidate):
 p=np.asarray(src);q=np.asarray(candidate);outside=np.ones((SIZE[1],SIZE[0]),dtype=bool)
 for x1,y1,x2,y2 in ROIS.values():outside[y1:y2,x1:x2]=False
 return int(np.any(p[outside]!=q[outside],axis=-1).sum())
def diff_count(src,c):return int(np.any(np.asarray(src)!=np.asarray(c),axis=2).sum())
def png(im):
 b=io.BytesIO();im.save(b,'PNG');return b.getvalue()
def ora(src,layers,closed,soft,path):
 # Keep original CANON visible. All technical candidates remain hidden.
 desc=[('CANON V2.1 / user approved / ORIGINAL VISIBLE',src,True)]
 for side in ('LEFT','RIGHT'):
  for k in ('SKIN','CANON_LASH','CREASE'):
   desc.append((f'CP394 {side} {k} / NOT APPROVED',layers[side][k],False))
 desc+=[('CP394 closed technical study / NOT APPROVED',closed,False),('CP394 soft technical study / NOT APPROVED',soft,False)]
 guide=Image.new('RGBA',SIZE,(0,0,0,0));gg=ImageDraw.Draw(guide)
 for box in ROIS.values():gg.rectangle(box,outline=(35,200,255,180),width=1)
 desc.append(('Eye ROI / guide only / hidden',guide,False))
 xml=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'name':'CP394 Lâm Thiển exact source / NOT APPROVED','version':'0.0.3'});stack=ET.SubElement(xml,'stack')
 with zipfile.ZipFile(path,'w') as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for i,(name,im,visible) in enumerate(desc):
   ref=f'data/layer_{i:02d}.png';z.writestr(ref,png(im))
   ET.SubElement(stack,'layer',{'name':name,'src':ref,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
  z.writestr('stack.xml',ET.tostring(xml,encoding='utf-8',xml_declaration=True))
  z.writestr('mergedimage.png',png(src));z.writestr('Thumbnails/thumbnail.png',png(src.resize((84,98))))
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  assert len(ET.fromstring(z.read('stack.xml')).find('stack'))==len(desc)
 return len(desc)

def qa_board(src,prior,closed,soft,path):
 scale=4;w,h=SIZE;gap=17;left=32;top=92
 cards=[('CANON V2.1 / ORIGINAL',src),('CP393 / PRIOR DRAFT',prior),('CP394 / SOURCE LASH',closed),('CP394 / NO CREASE',soft)]
 width=left*2+(w*scale)*4+gap*3;height=top+h*scale+100
 bg=Image.new('RGB',(width,height),(13,34,54));d=ImageDraw.Draw(bg)
 font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 fh=ImageFont.truetype(font,24);fs=ImageFont.truetype(font,14)
 d.text((left,17),'CP394 | Lam Thien CANON V2.1 | eyelash-retained closed-eye study',font=fh,fill='white')
 d.text((left,54),'DRAFT ART ONLY. Source 168x197. No painter approval, rig, or APK.',font=fs,fill='#ffd2a5')
 for i,(name,im) in enumerate(cards):
  x=left+i*(w*scale+gap)
  bg.paste(im.convert('RGB').resize((w*scale,h*scale),Image.Resampling.NEAREST),(x,top))
  d.text((x,top+h*scale+16),name,font=fs,fill='white')
 d.text((left,height-41),'CANON remains exact. Closure retains original lash pixels; new skin uses samples from the same portrait.',font=fs,fill='#cde4f5')
 bg.save(path)

def create(canon,prior,out):
 # No output until source validated.
 src=checked_canon(canon)
 old=Image.open(prior).convert('RGBA')
 if old.size!=SIZE:raise ValueError('PRIOR_SIZE_MISMATCH')
 out=Path(out);art=out/'layers';qa=out/'qa';art.mkdir(parents=True,exist_ok=True);qa.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(canon,out/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png');src.save(out/'CANON_SHY_PIXEL_EXACT.png')
 layers={s:make_layers(src,s) for s in ROIS}
 for side,v in layers.items():
  for k,im in v.items():im.save(art/f'{side}_{k}_DRAFT.png')
 closed=composite(src,layers,'closed');soft=composite(src,layers,'soft')
 assert outside_changes(src,closed)==0 and outside_changes(src,soft)==0
 closed.save(out/'CP394_CLOSED_EYE_SOURCE_LASH_STUDY_NOT_APPROVED.png')
 soft.save(out/'CP394_SOFT_EYE_SOURCE_LASH_STUDY_NOT_APPROVED.png')
 n=ora(src,layers,closed,soft,out/'CP394_CANON_LASH_PRESERVED_EYELID_DRAFT_NOT_RIG.ora')
 qa_board(src,old,closed,soft,qa/'CP394_CANON_CP393_CP394_SOURCE_REAL_COMPARISON.png')
 data={'checkpoint':'CP394','source_sha256':CANON_SHA,'native_size':list(SIZE),'source_crop':list(CROP),
       'layers':n,'authored_technical_layers':6,'outside_eye_changed_pixels':outside_changes(src,closed),
       'closed_changed_pixels':diff_count(src,closed),'soft_changed_pixels':diff_count(src,soft),
       'source_eyelashes_retained':True,'closed_eye_native_painter_quality':False,
       'visual_qa':'NOT_PASSED','release':RELEASE,
       'next':'CP395: original eye geometry from CANON retained; manually paint the closed eyelid keyframe at artist quality, obtain preview approval before rig/in-betweens.'}
 (out/'CP394_REPORT.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return data

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--prior',required=True);p.add_argument('--out',required=True)
 a=p.parse_args();print(json.dumps(create(a.canon,a.prior,a.out),ensure_ascii=False,indent=2))
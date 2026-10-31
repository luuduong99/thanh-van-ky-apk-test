#!/usr/bin/env python3
"""CP398 source-locked eye-closure eyelash+skin refinement — visual review draft only.
No substitute faces, no art release until explicit approval.
"""
from __future__ import annotations
import argparse, json, zipfile, hashlib, io, math, shutil
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
PREVIOUS_SHA='0baf2ad9c2524ac355d106556dea0b506f12644dc99a1b3d77df3e522de3d554'
SIZE=(168,197); CANON_SIZE=(941,1672); CROP=(25,684,193,881)
ROIS={'LEFT':(29,93,71,124),'RIGHT':(83,70,129,110)}
# Manually guided eye closure centerlines follow CANON anatomy; non-symmetric
LID={
 'LEFT': [(32.0,108.15),(41.0,104.4),(54.0,101.0),(65.8,101.4)],
 'RIGHT': [(86.2,87.6),(96.5,83.6),(113.0,76.8),(125.4,78.1)],
}
OLD_LID={
 'LEFT':[(32,107.3),(40,105.3),(53,100.9),(66,101.0)],
 'RIGHT':[(85.7,86.5),(96.5,81.9),(112.5,77.1),(125.5,77.0)],
}
SCALE=12
RELEASE={'status':'blocked_pending_visual_art_approval','sprite_paths':{},'spine_ready':False,'apk_ready':False}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def checked(canon,prior):
 if sha(canon)!=CANON_SHA:raise ValueError('CANON_SHA_MISMATCH')
 if sha(prior)!=PREVIOUS_SHA:raise ValueError('CP397_PRIOR_SHA_MISMATCH')
 with Image.open(canon) as img:
  if img.size!=CANON_SIZE or img.mode!='RGBA':raise ValueError('CANON_MODE_SIZE_MISMATCH')
  source=img.crop(CROP).copy()
 with Image.open(prior) as img:
  if img.size!=SIZE or img.mode!='RGBA':raise ValueError('CP397_MODE_SIZE_MISMATCH')
  prev=img.copy()
 if outside_diff(source,prev):raise ValueError('CP397_OUTSIDE_ROI_MISMATCH')
 return source,prev

def bez(points,t):
 p=np.asarray(points,np.float64)
 return (1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t*t*t*p[3]
def curve_y(points,x):
 seq=np.asarray([bez(points,t) for t in np.linspace(0,1,400)])
 return float(np.interp(x,seq[:,0],seq[:,1]))
def transparent():return Image.new('RGBA',SIZE,(0,0,0,0))
def restrict(img,side):
 a=np.asarray(img).copy();x1,y1,x2,y2=ROIS[side]
 a[:y1,:,3]=0;a[y2:,:,3]=0;a[:,:x1,3]=0;a[:,x2:,3]=0
 return Image.fromarray(a,'RGBA')
def sample_skin(a,x,y,side):
 # All samples are from the exact CANON image, outside the ocular interior.
 # Mix cheek sampling with the immediate upper lid to retain ambient lighting.
 if side=='LEFT':
  sx=int(np.clip(max(52,x+12),52,81)); low=int(np.clip(122+round(.22*(y-105)),120,138)); upper=int(np.clip(round(curve_y(OLD_LID[side],x)-9),91,99))
 else:
  sx=int(np.clip(x,92,119)); low=int(np.clip(108+round(.30*(y-82)),106,126)); upper=int(np.clip(round(curve_y(OLD_LID[side],x)-9),62,77))
 cheek=a[low,sx,:3].astype(np.float32)
 # Maintain natural local texture by using multiple individual adjacent face pixels.
 cheek_next=a[min(low+1,a.shape[0]-1),max(0,sx-2),:3].astype(np.float32)
 upper_c=a[max(0,upper),int(np.clip(x,0,SIZE[0]-1)),:3].astype(np.float32)
 # Color luminance subtly varies with position and neighboring pixel texture.
 base=cheek*.77+cheek_next*.18+upper_c*.05
 return base

def skin_retouch(source,side,variant):
 a=np.asarray(source)
 H,W=SIZE[1],SIZE[0]
 pix=np.zeros((H,W,4),np.uint8)
 x1,y1,x2,y2=ROIS[side]
 for x in range(x1,x2):
  cy=curve_y(OLD_LID[side],x)
  # Lower and upper closed-lid underpaint, tapering to transparent at corners.
  xedge=min(np.clip((x-(x1+1))/4.5,0,1),np.clip(((x2-2)-x)/4.5,0,1))
  for y in range(y1,y2):
   d=y-cy
   # Wider only around former CP397 flat stroke; CP397 iris remains occluded.
   alpha=float(math.exp(-.5*(d/3.4)**2)*xedge)
   alpha *= .75 if variant=='natural' else .82
   if alpha<.010:continue
   base=sample_skin(a,x,y,side)
   # Warm muted eyelid gradient follows the edge, not a uniform skin rectangle.
   under=math.exp(-.5*((d-3.1)/3.5)**2)
   upper=math.exp(-.5*((d+2.4)/2.7)**2)
   shade=np.array([1.4,4.5,5.4])*under+np.array([1.0,2.4,3.0])*upper
   base=np.clip(base-shade,0,255)
   pix[y,x,:3]=base.astype('uint8');pix[y,x,3]=round(alpha*255)
 return restrict(Image.fromarray(pix,'RGBA'),side)

def draw_spline(draw,points,fill,width,substart=.025,subend=.975):
 samples=[tuple(bez(points,t)*SCALE) for t in np.linspace(substart,subend,210)]
 draw.line(samples,fill=fill,width=max(1,round(width*SCALE)),joint='curve')

def wash_shadow(side,variant):
 hi=Image.new('RGBA',(SIZE[0]*SCALE,SIZE[1]*SCALE),(0,0,0,0));d=ImageDraw.Draw(hi)
 points=np.asarray(LID[side],float).copy();points[:,1]+=1.1
 draw_spline(d,points,(151,82,107,68 if variant=='natural' else 56),2.45)
 points[:,1]+=1.7
 draw_spline(d,points,(182,109,117,30 if variant=='natural' else 25),1.6)
 out=hi.filter(ImageFilter.GaussianBlur(SCALE*.55)).resize(SIZE,Image.Resampling.LANCZOS)
 return restrict(out,side)

def skin_highlight(side,variant):
 hi=Image.new('RGBA',(SIZE[0]*SCALE,SIZE[1]*SCALE),(0,0,0,0));d=ImageDraw.Draw(hi)
 points=np.asarray(LID[side],float).copy();points[:,1]-=3.1
 draw_spline(d,points,(251,205,194,28 if variant=='natural' else 34),.65,.18,.82)
 out=hi.filter(ImageFilter.GaussianBlur(SCALE*.50)).resize(SIZE,Image.Resampling.LANCZOS)
 return restrict(out,side)

def lash_layer(source,side,variant):
 hi=Image.new('RGBA',(SIZE[0]*SCALE,SIZE[1]*SCALE),(0,0,0,0));d=ImageDraw.Draw(hi)
 a=np.asarray(source);x1,y1,x2,y2=ROIS[side]
 block=a[y1:y2,x1:x2,:3];inten=block.astype(np.float32).mean(axis=2)
 tones=block[inten<np.percentile(inten,8)]
 rgb=np.median(tones,axis=0).astype(int) if len(tones) else np.array([77,43,62]);rgb=tuple(int(c) for c in rgb)
 pts=LID[side]
 # Base thin, warm-lash line rather than a broad flat dark slash.
 draw_spline(d,pts,(*rgb, 125 if variant=='natural' else 102),2.35)
 draw_spline(d,pts,(*rgb, 248 if variant=='natural' else 220),1.30)
 # Tapered lash-root accents distributed along the upper lid (not all uniform).
 roots=([(.13,.17),(.30,.17),(.54,.20),(.76,.21),(.90,.17)] if side=='RIGHT' else
        [(.12,.17),(.32,.20),(.58,.17),(.78,.18),(.90,.14)])
 for t,half in roots:
  draw_spline(d,pts,(*rgb,232 if variant=='natural' else 190),1.23,max(.02,t-half),min(.98,t+half))
 # Distinct eyelashes at outer third, tapered using two progressively thinner lines.
 spikes=([(.74,1.0,-1.0),(.81,1.4,-1.35),(.88,1.75,-1.65),(.93,2.05,-1.7)] if side=='RIGHT' else
         [(.09,-1.25,-1.35),(.17,-1.25,-1.20),(.24,-.85,-.85)])
 for t,dx,dy in spikes:
  p=bez(pts,t);x,y=p
  d.line([(x*SCALE,y*SCALE),((x+dx*.5)*SCALE,(y+dy*.45)*SCALE)],fill=(*rgb,178 if variant=='natural' else 153),width=round(.55*SCALE))
  d.line([((x+dx*.5)*SCALE,(y+dy*.45)*SCALE),((x+dx)*SCALE,(y+dy)*SCALE)],fill=(*rgb,95 if variant=='natural' else 85),width=max(1,round(.18*SCALE)))
 return restrict(hi.resize(SIZE,Image.Resampling.LANCZOS),side)

def make_layers(source,variant):
 if variant not in ('natural','soft'):raise ValueError('VARIANT_UNKNOWN')
 out={}
 for side in ROIS:
  out[side]={'SKIN_RETOUCH':skin_retouch(source,side,variant),'LID_SHADOW':wash_shadow(side,variant),'SKIN_HIGHLIGHT':skin_highlight(side,variant),'FINE_LASH':lash_layer(source,side,variant)}
 return out

def make_candidate(prev,layers):
 result=prev.copy()
 for side in ('LEFT','RIGHT'):
  for name in ('SKIN_RETOUCH','LID_SHADOW','SKIN_HIGHLIGHT','FINE_LASH'):result.alpha_composite(layers[side][name])
 return result

def outside_diff(src,target):
 a=np.asarray(src);b=np.asarray(target)
 mask=np.ones((SIZE[1],SIZE[0]),bool)
 for x1,y1,x2,y2 in ROIS.values():mask[y1:y2,x1:x2]=False
 return int(np.any(a[mask]!=b[mask],axis=1).sum())
def diff(src,tar):return int(np.any(np.asarray(src)!=np.asarray(tar),axis=-1).sum())
def png(im):
 buf=io.BytesIO();im.save(buf,format='PNG');return buf.getvalue()
def save_ora(source,prev,layers,variants,out):
 slots=[('CANON V2.1 ORIGINAL / VISIBLE / APPROVED',source,True),('CP397 previous CLOSED DRAFT / HISTORY ONLY',prev,False)]
 for side in ('LEFT','RIGHT'):
  for kind in ('SKIN_RETOUCH','LID_SHADOW','SKIN_HIGHLIGHT','FINE_LASH'):
   slots.append((f'CP398 NATURAL {side} {kind} / DRAFT / HIDDEN',layers[side][kind],False))
 for variant in ('natural','soft'):
  slots.append((f'CP398 {variant.upper()} COMPOSITE / NOT APPROVED',variants[variant],False))
 roi=transparent();dr=ImageDraw.Draw(roi)
 for area in ROIS.values():dr.rectangle(area,outline=(0,214,240,200),width=1)
 slots.append(('EYE ROI QA GUIDE / HIDDEN',roi,False))
 root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'version':'0.0.3','name':'CP398 Canon-only eyelid & skin detail, approval pending'})
 stack=ET.SubElement(root,'stack')
 with zipfile.ZipFile(out,'w') as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for i,(title,im,visible) in enumerate(slots):
   path=f'data/layer_{i:02d}.png';z.writestr(path,png(im))
   ET.SubElement(stack,'layer',{'name':title,'src':path,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
  z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
  z.writestr('mergedimage.png',png(source));z.writestr('Thumbnails/thumbnail.png',png(source.resize((84,98))))
 with zipfile.ZipFile(out) as z:assert z.testzip() is None
 return len(slots)

def font(sz):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',sz)
def compare_board(src,old,variants,out):
 items=[('CANON V2.1 / GỐC',src),('CP397 / CŨ',old),('CP398 / NATURAL DRAFT',variants['natural']),('CP398 / SOFT DRAFT',variants['soft'])]
 s=4;w,h=SIZE;pad=21;gap=16;top=108
 W=pad*2+w*s*4+gap*3;H=top+h*s+107
 can=Image.new('RGB',(W,H),(11,32,51));d=ImageDraw.Draw(can)
 d.text((pad,14),'LÂM THIỂN — CP398 / SO SÁNH CÙNG ẢNH CANON V2.1',font=font(24),fill='white')
 d.text((pad,51),'Đúng nhân vật, không thay nguồn — chỉ chỉnh bên trong 2 mắt — ART DRAFT, CHƯA DUYỆT',font=font(15),fill=(255,207,164))
 for i,(title,im) in enumerate(items):
  x=pad+i*(w*s+gap)
  can.paste(im.convert('RGB').resize((w*s,h*s),Image.Resampling.NEAREST),(x,top))
  d.text((x,top+h*s+13),title,font=font(15),fill='white')
 d.text((pad,H-31),'Không xem kiểm thử pixel là nghiệm thu mỹ thuật. Chưa dùng làm rig / APK.',font=font(15),fill=(255,204,167))
 can.save(out)

def zoom_board(src,old,variants,out):
 items=[]
 for side,(x1,y1,x2,y2) in ROIS.items():
  box=(max(0,x1-5),max(0,y1-6),min(SIZE[0],x2+5),min(SIZE[1],y2+6))
  for name,im in [('CANON',src),('CP397',old),('CP398 Natural',variants['natural']),('CP398 Soft',variants['soft'])]:
   items.append((side,name,im.crop(box).resize(((box[2]-box[0])*6,(box[3]-box[1])*6),Image.Resampling.NEAREST)))
 panelw=max(x.width for _,_,x in items);panelh=max(x.height for _,_,x in items)
 margin=16;gap=14;top=66
 W=margin*2+4*panelw+3*gap;H=top+panelh*2+gap+56
 b=Image.new('RGB',(W,H),(11,32,51));d=ImageDraw.Draw(b);f=font(16)
 d.text((margin,18),'CP398 | CANON / CP397 / NATURAL / SOFT — PHÓNG TO PIXEL GỐC',font=font(19),fill='white')
 for i,(side,name,img) in enumerate(items):
  row=i//4;col=i%4;x=margin+col*(panelw+gap);y=top+row*(panelh+gap)
  d.text((x,y-20),f'{side} {name}',font=f,fill='white');b.paste(img,(x,y))
 d.text((margin,H-30),'Phóng to chỉ để kiểm tra; nguồn native là 168×197 px; giữ nguyên CANON.',font=f,fill=(255,205,170))
 b.save(out)

def build(canon,previous,output):
 source,prior=checked(canon,previous)  # Source validates BEFORE writing anything
 l_nat=make_layers(source,'natural');l_soft=make_layers(source,'soft')
 opts={'natural':make_candidate(prior,l_nat),'soft':make_candidate(prior,l_soft)}
 for key,img in opts.items():
  if outside_diff(source,img)!=0:raise AssertionError('CANON_NON_EYE_PIXEL_CHANGED: '+key)
  if diff(img,prior)<30:raise AssertionError('NO_MEANINGFUL_REFINEMENT')
 output=Path(output);output.mkdir(parents=True,exist_ok=True)
 layersdir=output/'layers';layersdir.mkdir(exist_ok=True)
 shutil.copyfile(canon,output/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
 source.save(output/'CP398_CANON_SHY_PIXEL_EXACT.png')
 shutil.copyfile(previous,output/'CP397_PREVIOUS_CLOSED_EYE_DRAFT_NOT_APPROVED.png')
 for key,im in opts.items():im.save(output/f'CP398_CLOSED_EYE_{key.upper()}_DRAFT_NOT_APPROVED.png')
 for side in ROIS:
  for name,img in l_nat[side].items():img.save(layersdir/f'CP398_NATURAL_{side}_{name}_DRAFT.png')
  for name,img in l_soft[side].items():img.save(layersdir/f'CP398_SOFT_{side}_{name}_DRAFT.png')
 layer_count=save_ora(source,prior,l_nat,opts,output/'CP398_CANON_EYELID_REFINEMENT_13_LAYER_NOT_APPROVED.ora')
 compare_board(source,prior,opts,output/'CP398_CANON_CP397_NATURAL_SOFT_COMPARE.png')
 zoom_board(source,prior,opts,output/'CP398_BOTH_EYES_NATIVE_ZOOM_COMPARE.png')
 info={'checkpoint':'CP398','status':'TECHNICAL_DRAFT_FOR_ART_REVIEW',
 'canon_source_sha256':CANON_SHA,'cp397_prior_sha256':PREVIOUS_SHA,'source_crop':list(CROP),
 'native_size':list(SIZE),'eye_rois':{k:list(v) for k,v in ROIS.items()},
 'variants':['natural','soft'],'openraster_layers':layer_count,'editable_art_layers_per_variant':8,
 'changed_from_cp397':{k:diff(prior,img) for k,img in opts.items()},
 'outside_eyes_changed_from_canon':{k:outside_diff(source,img) for k,img in opts.items()},
 'visual_qa':'NOT_PASSED_PENDING_HUMAN_REVIEW',
 'not_artist_painted_HD_master':True,
 'known_limits':['At 168x197 native pixels, eyelid skin and lash quality still need close visual review.',
                 'Brow/skin/shading fidelity cannot be certified by pixel-diff tests.',
                 'Both variants are experimental source-derived raster retouches, not a completed production blink keyframe.'],
 'production_release':RELEASE,
 'next':'User review: approve one source-locked draft or request hand-painted native higher-detail eyelids. Only after visual acceptance begin blink in-betweens.'}
 (output/'CP398_REPORT.json').write_text(json.dumps(info,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 return info

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--cp397',required=True);p.add_argument('--out',required=True)
 a=p.parse_args();print(json.dumps(build(a.canon,a.cp397,a.out),ensure_ascii=False,indent=2))
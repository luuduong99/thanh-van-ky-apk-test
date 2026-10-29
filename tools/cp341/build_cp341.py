#!/usr/bin/env python3
"""CP341: extract detail-preserving alpha from approved V2.1 flat Front.

This is still a 215x449 source image and a single foreground, NOT artist-drawn semantic rig layers.
"""
from pathlib import Path
import hashlib, io, json, zipfile, xml.etree.ElementTree as ET
import numpy as np, cv2
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
CP340=Path('/mnt/data/TVK_LamThien_CP340_Canon_V21_Front_Alpha_Trial')
SOURCE=ROOT/'source/CANON_V2_1_EXACT_ORIGINAL.png'
CROP=ROOT/'source/FRONT_CANON_V2_1_EXACT_NATIVE_CROP.png'
OLD=ROOT/'source/FRONT_CP340_PREVIOUS_NOT_PRODUCTION.png'
EXPECTED='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BBOX=(13,177,228,626)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def png(im):
 b=io.BytesIO();im.save(b,'PNG');return b.getvalue()
def font(n=20):
 for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
  try:return ImageFont.truetype(p,n)
  except OSError:continue
 return ImageFont.load_default()

def refine(src_rgba,older):
 rgb=np.array(src_rgba.convert('RGB'),np.uint8)
 orig_a=np.array(older.convert('RGBA'),np.uint8)[:,:,3]
 h,w=orig_a.shape
 if (w,h)!=(215,449):raise ValueError('CP341 only for the hash-checked 215x449 V2.1 Front native crop')
 # A conservative white-panel background model, coupled with already verified GrabCut foreground.
 # This extends alpha into purple hair, pale blue sleeves and hanging drapes that CP340 lost.
 back=np.array([251.,253.,254.]);delta=back[None,None,:]-rgb.astype(float)
 dist=np.sqrt(np.sum((delta*np.array([1.0,1.1,1.2]))**2,axis=-1))
 colour_alpha=np.clip((dist-13)/29.,0,1)*255
 a=np.maximum(orig_a.astype(float),colour_alpha)
 Y,X=np.mgrid[:h,:w]
 # Remove panel borders/title. The canonical source image itself remains completely unchanged.
 a[Y<8]=0
 a[(Y<13)&((X<65)|(X>155))]=0
 a[(Y<115)&(X<33)]=0
 a[(Y<115)&(X>182)]=0
 # The bottom board has an ambient floor shadow that is NOT attached to the character.
 # Keep only the CP340 character core in that central lower zone, preserving outer dangling tails.
 bottom=(Y>431)&(X>=49)&(X<=169)
 a[bottom]=orig_a[bottom]
 a[(Y>440)&(X>48)&(X<90)]=0
 a[(Y>440)&(X>142)&(X<171)]=0
 # Crop border prevents background artifacts extending beyond sheet panel.
 a=cv2.GaussianBlur(a.astype('float32'),(3,3),.6)
 a=np.uint8(np.clip(a,0,255))
 rgba=np.dstack([rgb,a])
 return Image.fromarray(rgba,'RGBA')

def checkered(im, tile=12):
 a=np.array(im.convert('RGBA'));h,w=a.shape[:2]
 k=(np.indices((h,w)).sum(0)//tile)%2
 bg=np.where(k[...,None],np.array([207,207,210]),np.array([251,251,251])).astype(float)
 out=(1-a[:,:,3:4]/255)*bg+(a[:,:,3:4]/255)*a[:,:,:3]
 return Image.fromarray(np.uint8(np.clip(out,0,255)),'RGB')

def make_ora(path,source,old,refined):
 w,h=source.size
 # Single new foreground, plus two hidden previous versions, never 'complete rig'.
 root=ET.Element('image',{'version':'0.0.3','w':str(w),'h':str(h),'name':'CP341_ALPHA_REFINE_TECHNICAL_ONLY'})
 stack=ET.SubElement(root,'stack')
 layers=[('CP341_REFINED_SINGLE_FLAT_FOREGROUND_NOT_RIG',refined,'visible'),('CP340_PREVIOUS_ALPHA_FOR_COMPARISON',old,'hidden'),('CANON_V2_1_PIXEL_EXACT_CROP_REFERENCE',source,'hidden')]
 with zipfile.ZipFile(path,'w') as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for i,(label,im,visible) in enumerate(layers):
   ET.SubElement(stack,'layer',{'name':label,'src':f'data/layer{i}.png','opacity':'1.0','visibility':visible,'composite-op':'svg:src-over','x':'0','y':'0'})
   z.writestr(f'data/layer{i}.png',png(im),compress_type=zipfile.ZIP_DEFLATED)
  z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
  z.writestr('mergedimage.png',png(refined))
  thumb=refined.copy();thumb.thumbnail((256,256));z.writestr('Thumbnails/thumbnail.png',png(thumb))

def qa_preview(front,old,new):
 p=Image.new('RGB',(1190,1070),'#f8fafc');d=ImageDraw.Draw(p)
 d.text((36,21),'CP341 | LAM THIEN | CANON V2.1 MATTE RECOVERY',font=font(28),fill='#153653')
 d.text((38,58),'Native 215 x 449 only |  Original RGB pixels locked  |  Nonproduction R&D | NO SPINE',font=font(17),fill='#365778')
 imgs=[('CANON V2.1  ORIGINAL CROP',front.convert('RGB')),('CP340  PREVIOUS GRABCUT',checkered(old)),('CP341  RECOVERED STRANDS',checkered(new))]
 for i,(title,im) in enumerate(imgs):
  x=31+i*392
  d.rounded_rectangle((x,104,x+360,1000),radius=12,fill='white',outline='#a1b5c9',width=2)
  d.text((x+12,122),title,font=font(16),fill='#17436b')
  s=im.resize((344,718),Image.Resampling.NEAREST)
  p.paste(s,(x+8,181))
  d.text((x+14,923),['ORIGINAL PANEL: MAY INCLUDE LABELS','LOST OUTER FABRIC + HAIR','RECOVERED BUT HALOS REMAIN'][i],font=font(13),fill='#82452a')
  d.text((x+14,953),'APPROVED MODEL UNCHANGED',font=font(13),fill='#385d77')
 d.text((44,1032),'Technical alpha improvement, NOT clean garment/head decomposition, no new art acceptance.',font=font(16),fill='#753e3e')
 return p

def main():
 for path in [SOURCE,CROP,OLD]:
  if not path.exists():raise FileNotFoundError(path)
 if sha(SOURCE)!=EXPECTED:raise ValueError('Source CANON V2.1 checksum mismatch; refusing extraction')
 src=Image.open(SOURCE).convert('RGBA');front=src.crop(BBOX)
 if np.any(np.array(front)!=np.array(Image.open(CROP).convert('RGBA'))):raise AssertionError('Reference crop was modified')
 old=Image.open(OLD).convert('RGBA');new=refine(front,old)
 (ROOT/'source').mkdir(exist_ok=True,parents=True)
 original=ROOT/'source/FRONT_CANON_V2_1_EXACT_NATIVE_CROP.png';front.save(original)
 a=ROOT/'source/FRONT_CP340_PREVIOUS_NOT_PRODUCTION.png';old.save(a)
 new_path=ROOT/'source/FRONT_CP341_REFINED_SINGLE_FOREGROUND_NOT_RIG.png';new.save(new_path)
 Image.fromarray(np.array(new)[:,:,3],'L').save(ROOT/'source/FRONT_CP341_EDITABLE_ALPHA_MASK.png')
 ora=ROOT/'ora/CP341_FRONT_MATTE_REVIEW_NOT_RIG.ora';make_ora(ora,front,old,new)
 p=ROOT/'preview/CP341_BEFORE_AFTER_ALPHA_QA.png';qa_preview(front,old,new).save(p)
 o=np.array(old)[:,:,3];n=np.array(new)[:,:,3]
 # Regions CP340 had lost lots of actual dyed hair or drape strands.
 regions={'left_hair_sleeve':[0,127,54,303],'right_hair_sleeve':[162,124,215,326],'lower_left_drape':[0,290,64,442],'lower_right_drape':[166,284,215,445]}
 region_counts={}
 for key,(x0,y0,x1,y1) in regions.items():
  before=np.count_nonzero(o[y0:y1,x0:x1]>128)
  after=np.count_nonzero(n[y0:y1,x0:x1]>128)
  region_counts[key]={'original_cp340_opaque_px':int(before),'cp341_opaque_px':int(after),'delta_opaque_px':int(after-before)}
 man={'checkpoint':'CP341','canonical_id':'LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29',
      'canonical_sha256':EXPECTED,'canonical_pixel_size':[941,1672],'front_source_bbox_xyxy':list(BBOX),
      'front_native_px':[215,449],'mode':'source_locked_rgb_plus_refined_alpha',
      'flat_source_only':True,'not_artist_semantic_layers':True,
      'front_rgb_exact_original':True,
      'old_cutout_opaque_px':int(np.count_nonzero(o>128)),
      'refined_cutout_opaque_px':int(np.count_nonzero(n>128)),
      'opaque_px_gain':int(np.count_nonzero(n>128)-np.count_nonzero(o>128)),
      'region_checks':region_counts,
      'output_files':{'source':{'path':str(original.relative_to(ROOT)),'sha256':sha(original)},'previous':{'path':str(a.relative_to(ROOT)),'sha256':sha(a)},
        'refined':{'path':str(new_path.relative_to(ROOT)),'sha256':sha(new_path)},'alpha_mask':{'path':'source/FRONT_CP341_EDITABLE_ALPHA_MASK.png','sha256':sha(ROOT/'source/FRONT_CP341_EDITABLE_ALPHA_MASK.png')},'ora':{'path':str(ora.relative_to(ROOT)),'sha256':sha(ora)},'preview':{'path':str(p.relative_to(ROOT)),'sha256':sha(p)}},
      'production_gate':{'canon_v21_locked':True,'flat_background_removal_only':True,'artist_clean_edges_approved':False,
       'separate_character_parts_completed':False,'face_underpaint_completed':False,'spine_verified':False,'apk_verified':False,
       'android_production_release':'blocked_pending_art','sprite_paths_registered':0},
      'limitations':['Recovering bright hair and semitransparent cloth from a white-background thumbnail cannot recover hidden pixels',
       'Source had off-white and compression/antialias baked pixels which create edge halos',
       'Floor shadow around toe and tail ends may remain: manual retouch required',
       'No new high-resolution artwork, bone-ready separation or movement-safe underpaint'],
      'status':'IMPROVED_FLAT_ALPHA_ONLY_NOT_ARTIST_APPROVED_NOT_RIG'}
 (ROOT/'CP341_MANIFEST.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'opaque_before':man['old_cutout_opaque_px'],'opaque_after':man['refined_cutout_opaque_px'],'delta':man['opaque_px_gain'],'regions':region_counts},indent=2))
if __name__=='__main__':main()
#!/usr/bin/env python3
"""CP342: floor-shadow and off-white-matte cleanup, on EXACT V2.1 pixels.
This is a deliberately limited native-resolution technical mask. It is NOT painting missing
pixels, exporting semantic parts, or a complete Spine-ready character.
"""
from pathlib import Path
import hashlib, json, io, zipfile, xml.etree.ElementTree as ET, shutil
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name == 'tools' else Path('/mnt/data/TVK_LamThien_CP342_Front_Alpha_Shadow_Cleanup')
PRE=ROOT/'source'
CANON=ROOT/'source/LAM_THIEN_CANON_V2_1_EXACT_UNMODIFIED.png'
if not CANON.exists():
 CANON=Path('/mnt/data/TVK_LamThien_CANON_V2_1_20261029/LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
HASH='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CROP=(13,177,228,626)

def sh(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def png(im):
 b=io.BytesIO();im.save(b,format='PNG');return b.getvalue()
def font(size=18):
 for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
  try:return ImageFont.truetype(f,size)
  except OSError:pass
 return ImageFont.load_default()

def cleanup(source_rgb, cp341):
 """Reversible mask-only change, confines edits to last 39 native scanlines.
 Shadow: nearly-neutral blue-gray low saturation floor behind the ankles/feet and drapes.
 Preserves bright saturated hair/drapes, warm-tone shoes and the original upper body.
 """
 src=np.array(source_rgb.convert('RGB'),np.uint8)
 old=np.array(cp341.convert('RGBA'),np.uint8)
 assert src.shape[:2]==(449,215) and old.shape[:2]==(449,215)
 assert np.array_equal(src,old[:,:,:3])
 h,w=src.shape[:2];Y,X=np.mgrid[:h,:w]
 hsv=cv2.cvtColor(src,cv2.COLOR_RGB2HSV)
 sat=hsv[:,:,1].astype(float);val=hsv[:,:,2].astype(float)
 r=src[:,:,0].astype(float);g=src[:,:,1].astype(float);b=src[:,:,2].astype(float)
 a=old[:,:,3].astype(float)
 # General low-saturation floor strip; protect center foot and outer drape tips
 under=(Y>=414)&(X>22)&(X<194)&(~((X>=77)&(X<=128)))
 chroma=np.clip((77-sat)/40,0,1)*np.clip((val-105)/55,0,1)
 bluegray=(b-r>5)&(b-r<62)&(g-r>1)&(hsv[:,:,0]>88)&(hsv[:,:,0]<120)
 progress=np.clip((Y-414)/15,0,1)
 shadow=under*bluegray*chroma*progress
 new=a*(1-0.97*shadow)
 # Flat horizontal shadow bar on bottom; limit to x strips outside footwear
 # and to desaturated blue-gray floor; colored fabric remains.
 band=(Y>=421)&(((X>=32)&(X<=84))|((X>=123)&(X<=182)))
 floor=(hsv[:,:,0]>=93)&(hsv[:,:,0]<=123)&(sat<86)&(val>175)&((b-r)<90)
 factor=np.clip((Y-421)/6,0,1)
 select=band&floor
 new[select]=new[select]*(1-0.998*factor[select])
 # Drop near-white panel specks only along far lower margins
 far=(Y>=410)&((X<22)|(X>193))
 neutral=(val>238)&(sat<35)
 select=far&neutral
 new[select]=np.minimum(new[select],new[select]*.15)
 revised=np.uint8(np.clip(np.round(new),0,255))
 return Image.fromarray(np.dstack([src,revised]),'RGBA')

def checker(size,tile=15):
 w,h=size; y,x=np.indices((h,w));m=((x//tile+y//tile)%2).astype('uint8')
 v=np.where(m>0,205,246).astype('uint8')
 return Image.fromarray(np.stack([v,v,v],axis=-1),'RGB')

def composite(overlay):
 bg=checker(overlay.size).convert('RGBA');bg.alpha_composite(overlay);return bg.convert('RGB')

def review(original,old,clean):
 # crop header out of focus, use three column source + old/new pixel-nearest compare
 p=Image.new('RGB',(1380,1150),'#f8fafc');d=ImageDraw.Draw(p)
 d.text((34,23),'CP342 | LAM THIEN | V2.1 FRONT ALPHA SHADOW CLEANUP',font=font(27),fill='#0d3554')
 d.text((34,67),'CANON file locked  | Native 215 x 449 | Mask-only delta | NOT Spine / game production',font=font(17),fill='#375574')
 for idx,(lab,im) in enumerate([('CANON EXACT RGB',original.convert('RGB')),('CP341 MATTE',composite(old)),('CP342 FLOOR SUPPRESSION',composite(clean))]):
  x=27+idx*455
  d.rounded_rectangle((x,118,x+429,1050),radius=12,fill='white',outline='#9db4c8',width=2)
  d.text((x+13,135),lab,font=font(17),fill='#173b61')
  p.paste(im.resize((419,874),Image.Resampling.NEAREST),(x+5,170))
 d.text((34,1083),'New mask attenuates neutral floor shadows; some pale drape edges and background halos remain.',font=font(16),fill='#854d3e')
 d.text((34,1113),'All upper-body RGB unchanged. Alpha edits only in bottom 39 rows. Still a single flat cutout.',font=font(16),fill='#375574')
 return p

def focus(old,clean):
 p=Image.new('RGB',(960,640),'#f8fafc');d=ImageDraw.Draw(p)
 d.text((20,14),'CP342 FOOT/DRAPE DETAIL | 2x source pixels | Alpha review',font=font(23),fill='#173b61')
 d.text((22,52),'Floor shadow is reduced; compare both hanging fabric tips and foot shape',font=font(15),fill='#375574')
 for i,(name,im) in enumerate([('CP341 BEFORE',old),('CP342 AFTER',clean)]):
  x=15+i*480
  d.rounded_rectangle((x,86,x+464,615),radius=12,fill='white',outline='#99b0c6',width=2)
  d.text((x+12,103),name,font=font(17),fill='#173b61')
  crop=composite(im).crop((0,292,215,449))
  p.paste(crop.resize((440,322),Image.Resampling.NEAREST),(x+12,151))
  d.text((x+12,491),'Technical mask-only; not a painted asset',font=font(13),fill='#72514b')
 return p

def make_ora(path,source,prev,cur,difference):
 w,h=source.size
 root=ET.Element('image',{'version':'0.0.3','w':str(w),'h':str(h),'name':'CP342_NONPRODUCTION_MATTE_REVIEW'})
 stack=ET.SubElement(root,'stack')
 layers=[('CP342_REFINED_FLAT_MATTE_NOT_GAME_ART',cur,'visible'),('CP342_SHADOW_REMOVAL_MAP_DIAGNOSTIC',difference,'hidden'),('CP341_ORIGINAL_ALPHA_FOR_COMPARISON',prev,'hidden'),('CANON_V2_1_PIXEL_EXACT_CROP_REFERENCE',source,'hidden')]
 with zipfile.ZipFile(path,'w') as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for i,(lab,im,vis) in enumerate(layers):
   src=f'data/layer{i}.png'
   ET.SubElement(stack,'layer',{'name':lab,'src':src,'opacity':'1.0','visibility':vis,'composite-op':'svg:src-over','x':'0','y':'0'})
   z.writestr(src,png(im),compress_type=zipfile.ZIP_DEFLATED)
  z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
  z.writestr('mergedimage.png',png(cur))
  th=cur.copy();th.thumbnail((256,256));z.writestr('Thumbnails/thumbnail.png',png(th))

def main():
 assert sh(CANON)==HASH
 canon=Image.open(CANON).convert('RGBA')
 original=canon.crop(CROP)
 old_path=PRE/'FRONT_CP341_PREVIOUS.png'
 if not old_path.exists():old_path=Path('/mnt/data/TVK_LamThien_CP341_Matte_Recovery/source/FRONT_CP341_REFINED_SINGLE_FOREGROUND_NOT_RIG.png')
 prev=Image.open(old_path).convert('RGBA')
 assert prev.size==original.size
 assert np.array_equal(np.array(prev)[:,:,:3],np.array(original)[:,:,:3])
 final=cleanup(original,prev)
 arr0=np.array(prev);arr1=np.array(final)
 assert np.array_equal(arr0[:,:,:3],arr1[:,:,:3])
 assert np.array_equal(arr0[:410,:,3],arr1[:410,:,3])
 assert np.all(arr1[:,:,3]<=arr0[:,:,3])
 files={}
 for d in ['source','preview','ora','tools','tests']:(ROOT/d).mkdir(parents=True,exist_ok=True)
 file_sources={
  'canonical_original':'source/LAM_THIEN_CANON_V2_1_EXACT_UNMODIFIED.png',
  'front_native':'source/FRONT_NATIVE_EXACT_CROP.png',
  'cp341_previous':'source/FRONT_CP341_PREVIOUS.png',
  'cp342_refined':'source/FRONT_CP342_FLOOR_CLEAN_ALPHA_NOT_RIG.png',
  'cp342_mask':'source/FRONT_CP342_EDITABLE_ALPHA_MASK.png',
  'cp342_delta':'source/FRONT_CP342_REMOVED_ALPHA_DIAGNOSTIC.png',
  'ora':'ora/CP342_MATTE_VARIANTS_NOT_RIG.ora',
  'comparison':'preview/CP342_THREE_WAY_CANON_ALPHA_QA.png',
  'shoe_detail':'preview/CP342_SHADOW_BEFORE_AFTER_DETAIL.png'}
 shutil.copyfile(CANON,ROOT/file_sources['canonical_original'])
 original.save(ROOT/file_sources['front_native'])
 prev.save(ROOT/file_sources['cp341_previous'])
 final.save(ROOT/file_sources['cp342_refined'])
 Image.fromarray(arr1[:,:,3],'L').save(ROOT/file_sources['cp342_mask'])
 removed=arr0[:,:,3].astype(np.int16)-arr1[:,:,3].astype(np.int16)
 removal=Image.fromarray(np.uint8(np.clip(removed,0,255)),'L')
 removal.save(ROOT/file_sources['cp342_delta'])
 # diagnostic hidden as black alpha removed (not game part)
 d_arr=np.zeros_like(arr1);d_arr[:,:,:3]=[210,40,80];d_arr[:,:,3]=np.uint8(removed)
 diagnostic=Image.fromarray(d_arr,'RGBA')
 make_ora(ROOT/file_sources['ora'],original,prev,final,diagnostic)
 review(original,prev,final).save(ROOT/file_sources['comparison'])
 focus(prev,final).save(ROOT/file_sources['shoe_detail'])
 for k,p in file_sources.items():files[k]={'path':p,'sha256':sh(ROOT/p)}
 y,x=np.indices(removed.shape)
 qa={
  'upper_body_untouched_pixels':int(np.count_nonzero(removed[:410,:]==0)),
  'alpha_pixels_changed':int(np.count_nonzero(removed>0)),
  'alpha_pixels_removed_sum':int(np.sum(removed)),
  'before_alpha_gt_128':int(np.count_nonzero(arr0[:,:,3]>128)),
  'after_alpha_gt_128':int(np.count_nonzero(arr1[:,:,3]>128)),
  'floor_zone_delta':int(np.sum(removed[421:438,32:184])),
  'center_shoe_delta':int(np.sum(removed[398:435,85:120])),
  'upper_torso_delta':int(np.sum(removed[:345,:])),
  'left_drape_strong_alpha_after':int(np.count_nonzero(arr1[275:410,:35,3]>128)),
  'right_drape_strong_alpha_after':int(np.count_nonzero(arr1[275:410,180:,3]>128)),
 }
 manifest={
  'checkpoint':'CP342','date':'2026-10-29','canon_id':'LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29',
  'canon_sha256':HASH,'source_px':[941,1672],'source_bbox_xyxy':list(CROP),'native_front_px':[215,449],
  'mode':'RGB_unchanged_alpha_floor_shadow_attenuation',
  'rgb_unchanged':True,'upper_410_scanlines_alpha_unchanged':True,
  'still_single_flat_character_foreground':True,
  'not_artist_clean_semantic_layers':True,
  'edit_confined_to':'bottom_39_rows_floor_shadow_neutral_blue_gray_only',
  'pixel_qa':qa,'output_files':files,
  'production_gate':{'canon_locked':True,'manual_artist_edge_clean_approved':False,'face_underpaint_complete':False,
    'independent_hair_body_garment_parts_created':False,'riggable_layers_ready':False,'spine_verified':False,
    'apk_built_and_tested':False,'runtime_release':'blocked_pending_art','sprite_paths_registered':0},
  'limitations':[
    'Some floor shadow remains, especially central under-foot grey pixels and pale drape edges.',
    'Source contains pre-composited white/light fabric and background; 215px thumbnail cannot recover hidden brush strokes or body parts.',
    'RGB source is locked but alpha remains heuristic; line-art rerender/manual painter cleanup is necessary.',
    'No 2D rig, no independent facial/bodice/hair/skin parts, no user asset approval.'
  ],'status':'CLEANER_FLOOR_ALPHA_R_AND_D_NOT_PRODUCTION_READY'
 }
 (ROOT/'CP342_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(qa,indent=2));print('files',len(files))
if __name__=='__main__':main()
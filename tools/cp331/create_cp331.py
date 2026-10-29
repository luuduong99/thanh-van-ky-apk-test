#!/usr/bin/env python3
"""CP331: fixed-identity technical composite test from an UNAPPROVED flat board.

Output is not canonical face art, not a semantic rig, and not high-resolution redraw.
The test verifies FIVE expressions share identical non-facial pixel content.
"""
import hashlib, io, json, zipfile, shutil
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont

OUT=Path('/mnt/data/TVK_LamThien_CP331_SharedFace_Trial')
SOURCE=Path('/mnt/data/a_polished_infographic_style_character_design_ass.png')
CANON=Path('/mnt/data/TVK_LamThien_CANON_BodyCostume_V2_20261028.png')
APPROVED=Path('/mnt/data/a_clean_anime_character_expression_reference_sheet.png')
CANON_HASH='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
APPROVED_HASH='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
IDS=('shy','angry','pain','embarrassed','alluring')
LABELS=('Ngại ngùng','Tức giận','Đau đớn','Xấu hổ','Quyến rũ')
CROPS=[(12,90,270,454),(276,90,534,454),(540,90,798,454),(806,90,1064,454),(1066,90,1324,454)]
MASTER_INDEX=1
PARTS=('brow_image_left','brow_image_right','eye_image_left','eye_image_right','mouth','blush_image_left','blush_image_right')
# Seven regions deliberately cover ONLY the face. They are approximate manual
# art-direction coordinates, *not* trained landmark extraction or rig anchors.
# Coordinate system: 258x364 (native pixel size of one generated sheet panel).
# Rectangles are x0,y0,x1,y1, and not derived from approved canonical image.
DONOR={
'shy':[(72,129,123,151),(140,121,208,143),(64,142,130,180),(140,136,208,178),(117,194,167,225),(62,177,120,209),(166,163,223,207)],
'angry':[(72,130,126,153),(140,119,208,145),(63,140,130,181),(140,133,213,178),(119,192,169,226),(62,177,121,209),(167,162,222,208)],
'pain':[(73,132,130,159),(143,123,208,149),(65,143,135,185),(143,135,213,184),(113,191,176,233),(63,181,125,213),(167,164,226,210)],
'embarrassed':[(75,131,127,155),(145,122,210,144),(68,140,133,181),(144,136,215,181),(118,193,171,232),(66,175,128,213),(170,159,227,210)],
'alluring':[(76,130,128,153),(146,122,212,147),(67,145,134,188),(146,139,217,183),(119,190,173,228),(66,179,128,216),(170,164,229,216)]
}
TARGET=DONOR['angry']

def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def rawpng(im):
 b=io.BytesIO();im.save(b,format='PNG',compress_level=6);return b.getvalue()
def font(sz):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',sz)
def makemask(size,bbox,blur=2.6):
 m=Image.new('L',size,0);d=ImageDraw.Draw(m)
 d.ellipse(bbox,fill=255)
 return m.filter(ImageFilter.GaussianBlur(blur))
def nonempty(image):return int(np.count_nonzero(np.asarray(image.getchannel('A'))>3))
def makeora(path, size, layers, composite):
 root=Element('image',{'w':str(size[0]),'h':str(size[1]),'version':'0.0.3','name':path.stem})
 st=SubElement(root,'stack')
 with zipfile.ZipFile(path,'w') as z:
  def add(name,data,ty=zipfile.ZIP_DEFLATED):
   info=zipfile.ZipInfo(name,date_time=(2026,10,29,0,0,0));info.compress_type=ty;info.create_system=3
   z.writestr(info,data)
  add('mimetype',b'image/openraster',zipfile.ZIP_STORED)
  for i,(name,im,visible) in enumerate(layers):
   loc=f'data/layer_{i:02d}.png'
   SubElement(st,'layer',{'name':name,'src':loc,'visibility':'visible' if visible else 'hidden','opacity':'1.0','composite-op':'svg:src-over','x':'0','y':'0'})
   add(loc,rawpng(im))
  add('stack.xml',tostring(root,encoding='utf-8'))
  add('mergedimage.png',rawpng(composite))
  add('Thumbnails/thumbnail.png',rawpng(composite.resize((181,256),Image.Resampling.LANCZOS)))

def compose(under, overlays):
 out=under.convert('RGBA')
 for img in overlays:out=Image.alpha_composite(out,img)
 return out

def main():
 if sha(CANON)!=CANON_HASH:raise ValueError('Canon V2 SHA mismatch')
 if sha(APPROVED)!=APPROVED_HASH:raise ValueError('Approved expression sheet SHA mismatch')
 for dir in ('reference','ora','preview','layers','candidates'): (OUT/dir).mkdir(parents=True,exist_ok=True)
 source=Image.open(SOURCE).convert('RGB')
 imgs=[source.crop(b) for b in CROPS]; size=imgs[0].size
 if size!=(258,364):raise ValueError('Unexpected native panel size')
 master=imgs[MASTER_INDEX].copy()
 master.save(OUT/'reference'/'CP331_FIXED_IDENTITY_SOURCE_UNAPPROVED.png')
 Image.open(CANON).crop((1160,0,1390,114)).save(OUT/'reference'/'CANON_V2_FACE_NATIVE_230x114.png')
 shutil.copy(APPROVED,OUT/'reference'/'FIVE_EMOTIONS_ALREADY_APPROVED.png')
 # Clean synthetic underpaint is NOT artist drawn: inpaint same ROI across variants.
 masks=[]
 for box in TARGET:masks.append(makemask(size,box,2.4))
 occupied=Image.new('L',size,0)
 for mask in masks:occupied=ImageChops.lighter(occupied,mask)
 mask_arr=np.asarray(occupied,dtype=np.uint8)
 inp=cv2.inpaint(cv2.cvtColor(np.asarray(master),cv2.COLOR_RGB2BGR),mask_arr,5,cv2.INPAINT_TELEA)
 shared_underpaint=Image.fromarray(cv2.cvtColor(inp,cv2.COLOR_BGR2RGB)).convert('RGBA')
 shared_underpaint.save(OUT/'reference'/'SHARED_FACE_UNDERPAINT_CV2_NOT_APPROVED.png')
 master.save(OUT/'reference'/'SHARED_FACE_ORIGINAL_UNAPPROVED.png')
 # Canon remains independent; the same working master underpaint is present in all ORAs.
 refsha=sha(OUT/'reference'/'SHARED_FACE_UNDERPAINT_CV2_NOT_APPROVED.png')
 records=[]; portraits=[]
 for name,donor in zip(IDS,imgs):
  layers=[]
  active_pixels=0
  for slot,box,goal in zip(PARTS,DONOR[name],TARGET):
   x0,y0,x1,y1=box;gx0,gy0,gx1,gy1=goal
   part=donor.crop(box).convert('RGBA')
   # Align each feature to the SAME target ROI size using small affine resizing.
   # Content is still a flat generated-poster patch, not a clean art attachment.
   part=part.resize((gx1-gx0,gy1-gy0),Image.Resampling.BICUBIC)
   mask=makemask(part.size,(1,1,part.width-2,part.height-2),blur=7.0)
   part.putalpha(mask)
   whole=Image.new('RGBA',size,(0,0,0,0));whole.paste(part,(gx0,gy0))
   layers.append((slot,whole,True))
   active_pixels+=nonempty(whole)
   outpath=OUT/'layers'/f'{name}_{slot}.png';whole.save(outpath)
  composed=compose(master.convert('RGBA'),[t[1] for t in layers])
  opath=OUT/'ora'/f'CP331_{name}_SHARED_FACE_TECH_TRIAL_NOT_GAME_ART.ora'
  ordered=list(reversed(layers))+[('SHARED_FLAT_MASTER_WITH_BAKED_FACE_FEATURES_NOT_RIGGABLE',master.convert('RGBA'),True),('INPAINT_UNDERPAINT_DRAFT_HIDDEN_NOT_APPROVED',shared_underpaint,False),('GUIDE_SOURCE_UNAPPROVED_REFERENCE_ONLY',master.convert('RGBA'),False)]
  makeora(opath,size,ordered,composed)
  imagepath=OUT/'preview'/f'{name}_FIXED_FACE_COMPOSITE.png';composed.save(imagepath)
  portraits.append(composed)
  records.append({'id':name,'ora_sha256':sha(opath),'preview_sha256':sha(imagepath),'source_patch_layers_nonempty':7,'alpha_pixels_across_layers':active_pixels,'underpaint_sha256':refsha,'shared_master_same_rgba_every_state':True,'base_has_baked_eye_and_mouth':True,'native_dimensions_px':list(size),'production_approved':False})
 # Build static QA board at face-source native resolution with sizing tests.
 W,H=1600,1060
 board=Image.new('RGB',(W,H),'#091c30');d=ImageDraw.Draw(board)
 d.text((28,18),'CP331  /  SHARED FACE MASTER — TECHNICAL R&D ONLY',font=font(31),fill='#f1e8d0')
 d.text((28,64),'Five emotions share one exact 258x364 base. Canon V2 identity/artwork and five emotion directions stay separately approved.',font=font(16),fill='#c8d7e8')
 names=('SHY','ANGRY','PAIN','EMBARRASSED','ALLURING')
 for i,(img,n) in enumerate(zip(portraits,names)):
  x=20+i*316
  board.paste(img.convert('RGB'),(x+28,135))
  d.text((x+26,105),f'{i+1:02d} / {n}',font=font(18),fill='#f2ddb3')
  t=img.resize((132,186),Image.Resampling.LANCZOS).convert('RGB')
  board.paste(t,(x+70,550))
  s=img.resize((64,90),Image.Resampling.LANCZOS).convert('RGB')
  board.paste(s,(x+106,763))
  d.text((x+26,522),'Native 258x364',font=font(15),fill='#9fded5')
  d.text((x+72,738),'132px',font=font(14),fill='#d9e9f4')
  d.text((x+100,860),'64px',font=font(14),fill='#d9e9f4')
 d.rectangle((24,927,W-24,H-25),fill='#17334b',outline='#5f829e',width=2)
 d.text((42,943),'ART GATE: NOT APPROVED     |     Base still has baked-in face features     |     No Spine / APK',font=font(21),fill='#ffbd9c')
 d.text((42,989),'Hair, clothing and background are pixel-identical outside the face mask. Flat base is NOT clean underpaint.',font=font(15),fill='#cdddeb')
 board.save(OUT/'preview'/'CP331_SHARED_FACE_FIVE_EMOTIONS_CONTACT_NOT_APPROVED.png')
 # Comparison V2 vs preview, mark distinct authority.
 comp=Image.new('RGB',(1350,660),'#0c2035');dd=ImageDraw.Draw(comp)
 canon_face=Image.open(OUT/'reference'/'CANON_V2_FACE_NATIVE_230x114.png').convert('RGB')
 canon_face=canon_face.resize((690,342),Image.Resampling.NEAREST)
 comp.paste(canon_face,(22,90)); comp.paste(master.resize((258,364)),(830,78))
 dd.text((22,25),'CANON V2 / approved face reference / native only 230x114',font=font(20),fill='#fff3db')
 dd.text((830,25),'CP331 new generated master / NOT APPROVED',font=font(20),fill='#ffbd9c')
 dd.text((22,470),'CP331 is SAME-FACE across all five expressions, but that does NOT prove face matches Canon V2.',font=font(18),fill='#d9e9f4')
 dd.text((22,510),'Review facial silhouette, iris color and accessories. The enlarged Canon on left is NEAREST-NEIGHBOR, not native HD art.',font=font(15),fill='#d9e9f4')
 comp.save(OUT/'preview'/'CP331_CANON_V2_VS_MASTER_ALIGNMENT_REVIEW.png')
 # Mask invariance check: pixels outside union bbox exact across all output frames.
 fixed_roi=Image.new('L',size,0);roi_draw=ImageDraw.Draw(fixed_roi)
 for b in TARGET:roi_draw.rectangle((max(0,b[0]-1),max(0,b[1]-1),min(size[0]-1,b[2]+1),min(size[1]-1,b[3]+1)),fill=255)
 outside=np.asarray(fixed_roi)==0
 arrs=[np.array(p.convert('RGB')) for p in portraits]
 for arr in arrs[1:]:
  if not np.array_equal(arrs[0][outside],arr[outside]):raise RuntimeError('identity background changed outside region')
 data={'checkpoint':'CP331','date':'2026-10-29','status':'shared_face_master_technical_trial_unapproved_not_spine_ready',
 'canonical_visual_id':'LT_CANON_BODY_REF_2026-10-28_V2','canonical_sha256':CANON_HASH,
 'approved_expression_profile':'LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED','approved_expression_sha256':APPROVED_HASH,
 'new_sheet_sha256':sha(SOURCE),'new_sheet_source_kind':'AI_generated_flat_unapproved',
 'base_source_panel':'angry','native_source_dimensions_px':list(size),'source_is_true_high_resolution':False,
 'shared_master_art_production_ready':False,'new_generated_face_visual_approved':False,'shared_underpaint_artist_approved':False,'shared_underpaint_is_hidden_draft_only':True,'flat_master_contains_baked_facial_features':True,
 'all_variants_share_same_fixed_underpaint_sha256':refsha,'outside_face_region_pixel_identical':True,
 'face_attachment_semantics':'feathered_flat_painted_patches_on_baked_flat_base_not_independent_rig_attachments',
 'target_region_boxes':{part:list(box) for part,box in zip(PARTS,TARGET)},'layer_count_total':35,'orafiles':5,'spine_ready':False,'apk_verified':False,
 'asset_registration_allowed':False,'results':records}
 (OUT/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'master':str(OUT),'manifest':str(OUT/'manifest.json'),'underpaintSha':refsha,'results':records},ensure_ascii=False,indent=2))
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--source',type=Path,default=SOURCE,help='Unapproved source image (1536x1024)')
 parser.add_argument('--canon',type=Path,default=CANON,help='Actual approved CANON V2 PNG, SHA checked')
 parser.add_argument('--approved',type=Path,default=APPROVED,help='Original five-expression approved PNG, SHA checked')
 parser.add_argument('--out',type=Path,default=OUT,help='Output directory')
 args=parser.parse_args()
 SOURCE=args.source;CANON=args.canon;APPROVED=args.approved;OUT=args.out
 main()

#!/usr/bin/env python3
"""Create an honest, lossless reference handoff from two *approved* sources.
Does not manufacture face layers, native resolution or a Spine skeleton.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib,json,shutil

ROOT=Path(__file__).resolve().parents[1]
CANON=Path('/mnt/data/TVK_LamThien_CANON_BodyCostume_V2_20261028.png')
EMOTIONS=Path('/mnt/data/TVK_CP335_Art_Release_Gate/reference/FIVE_EXPRESSIONS_APPROVED.png')
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXPRESSION_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
REFS=[
 ('front','FRONT / GÓC HƠI NGHIÊNG', (14,116,159,267)),
 ('three_quarter','GÓC 3/4 / REFERENCE',(321,116,464,267)),
 ('closeup','CẬN MẶT V2',(1160,0,1390,114))]
IDS=['shy','angry','pain','embarrassed','alluring']
NAMES=['Ngại ngùng','Tức giận','Đau đớn','Xấu hổ','Quyến rũ']
APPROVED_CROPS=Path('/mnt/data/TVK_LamThien_CP324_Approved_Expression_Handoff')
COLORS={'navy':(12,34,55),'accent':(71,148,183),'light':(240,246,250),'ink':(23,55,75),'gold':(212,163,97),'note':(90,116,133)}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(size,bold=False):
 name='DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
 return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+name,size)

def main():
 if sha(CANON)!=CANON_SHA or sha(EMOTIONS)!=EXPRESSION_SHA:
  raise RuntimeError('An approved input has a different checksum; stop.')
 (ROOT/'reference').mkdir(exist_ok=True,parents=True)
 (ROOT/'preview').mkdir(exist_ok=True,parents=True)
 canon=Image.open(CANON).convert('RGBA');emo=Image.open(EMOTIONS).convert('RGB')
 shutil.copyfile(CANON,ROOT/'reference'/'CANON_V2_ORIGINAL_1672x941_RGBA.png')
 shutil.copyfile(EMOTIONS,ROOT/'reference'/'FIVE_EXPRESSIONS_APPROVED_1536x1024_RGB.png')
 out=Image.new('RGB',(1680,1100),COLORS['light']);d=ImageDraw.Draw(out)
 d.rectangle((0,0,1680,112),fill=COLORS['navy'])
 d.text((36,21),'THANH VÂN KÝ · LÂM THIỂN',font=font(38,True),fill=(252,250,244))
 d.text((38,73),'CP336 · Nguồn tạo hình đã chốt / Reference only — chưa có sprite hoặc rig',font=font(17),fill=(196,217,229))
 # 3 view columns; the previews are scaled with NEAREST only to make tiny native pixels visible.
 ref_manifest=[]
 for i,(id,label,bbox) in enumerate(REFS):
  x0=26+i*555;x1=x0+532
  d.rounded_rectangle((x0,127,x1,604),radius=14,fill='white',outline=(196,211,220),width=2)
  d.rectangle((x0,127,x1,175),fill=(20,64,92));d.text((x0+20,140),label,font=font(20,True),fill='white')
  crop=canon.crop(bbox)
  file=ROOT/'reference'/f'V2_{id}_NATIVE_{crop.width}x{crop.height}.png';crop.save(file)
  display=crop.copy();display.thumbnail((502,360),resample=Image.Resampling.NEAREST)
  # upscale for display with fixed sharp pixels, never call it native detail
  scale=min((500/display.width),(360/display.height))
  if scale>1: display=display.resize((round(display.width*scale),round(display.height*scale)),Image.Resampling.NEAREST)
  dx=x0+(532-display.width)//2;dy=187+(362-display.height)//2
  out.paste(display.convert('RGB'),(dx,dy))
  d.line((x0+20,556,x1-20,556),fill=(219,229,234),width=2)
  d.text((x0+18,568),f'Native: {crop.width} × {crop.height}px  ·  x={bbox[0]}–{bbox[2]}, y={bbox[1]}–{bbox[3]}',font=font(13),fill=COLORS['ink'])
  ref_manifest.append({'id':id,'label':label,'source_box_xyxy':list(bbox),'native_size_px':[crop.width,crop.height],'sha256':sha(file),'file':f'reference/{file.name}'})
 d.text((26,618),'NĂM SẮC THÁI ĐÃ DUYỆT  ·  Dùng làm hướng cảm xúc, KHÔNG thay mắt/mặt của V2',font=font(21,True),fill=COLORS['ink'])
 desc=[('shy','Ngại ngùng'),('angry','Tức giận'),('pain','Đau đớn'),('embarrassed','Xấu hổ'),('alluring','Quyến rũ')]
 crops=[]
 for i,(eid,label) in enumerate(desc):
  x0=26+i*333;x1=x0+309
  d.rounded_rectangle((x0,658,x1,1008),radius=12,fill='white',outline=(196,211,220),width=2)
  f=APPROVED_CROPS/f'{i+1:02d}_{eid}_portrait_APPROVED_REFERENCE_ONLY.png'
  im=Image.open(f).convert('RGB')
  # Need NOT alter source crop. Store a byte-identical copy to avoid infer native res.
  dst=ROOT/'reference'/f'approved_{eid}_portrait_native.png';shutil.copyfile(f,dst)
  im.thumbnail((297,287),Image.Resampling.LANCZOS)
  out.paste(im,(x0+(309-im.width)//2,667))
  d.text((x0+14,956),label,font=font(18,True),fill=COLORS['ink'])
  d.text((x0+14,980),f'{Image.open(f).width}×{Image.open(f).height}px · reference',font=font(11),fill=COLORS['note'])
  crops.append({'id':eid,'name':label,'sha256':sha(dst),'native_size_px':list(Image.open(f).size),'file':f'reference/{dst.name}'})
 d.rectangle((0,1030,1680,1100),fill=COLORS['navy']);d.text((30,1051),'BẮT BUỘC: 1 master/angle  •  Underpaint không baked mắt-miệng  •  Alpha độc lập  •  QA trước Spine/APK',font=font(18,True),fill='white')
 p=ROOT/'preview'/'CP336_APPROVED_ANGLES_AND_EXPRESSIONS.png';out.save(p)
 result={'schema_version':1,'checkpoint':'CP336','date':'2026-10-29',
 'status':'source_crop_and_gate_preflight_complete_production_art_missing',
 'canonical_visual_id':'LT_CANON_BODY_REF_2026-10-28_V2','canonical_sha256':CANON_SHA,
 'approved_expression_profile':'LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED','approved_expression_sha256':EXPRESSION_SHA,
 'canonical_original_size_px':list(canon.size),'approved_expression_sheet_size_px':list(emo.size),
 'source_angle_crops':ref_manifest,'emotion_crops':crops,
 'native_high_res_front_face_master_ready':False,'native_high_res_three_quarter_face_master_ready':False,
 'clean_underpaint_completed':False,'five_expressions_semantic_layers_completed':False,
 'spine_verified':False,'apk_verified':False,'user_asset_approval_id':None,
 'sprite_paths_registered':0,
 'source_recovery':'Drive canonical folder contains PNG and flat ZIP only; no accessible native ORA/PSD/KRA found',
 'note':'Crops are lossless extracts from canon; rendering larger in the board does not increase native detail.'}
 (ROOT/'CP336_REFERENCE_MANIFEST.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'board':str(p),'sha256':sha(p),'face_crops':[v['native_size_px'] for v in ref_manifest],'source_hashes':[CANON_SHA,EXPRESSION_SHA]},ensure_ascii=False))

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser(description='Lossless guide from approved CANON V2 + five emotions, not asset art')
 ap.add_argument('--canon',type=Path,required=True)
 ap.add_argument('--emotions',type=Path,required=True)
 ap.add_argument('--approved-crops',type=Path,required=True)
 ap.add_argument('--out',type=Path,required=True)
 args=ap.parse_args()
 CANON=args.canon;EMOTIONS=args.emotions;APPROVED_CROPS=args.approved_crops;ROOT=args.out
 main()
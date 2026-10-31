#!/usr/bin/env python3
"""CP329 edit-ready OpenRaster guides from immutable reference sheets.

A reference guide and a transparent art scaffold are NOT finished art.
The generated ORA must never be labeled production-ready.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from PIL import Image, ImageDraw, ImageFont

CANON_SHA = '41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXPR_SHA = 'ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
CANON_ID = 'LT_CANON_BODY_REF_2026-10-28_V2'
EXPR_ID = 'LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED'
FACE_ROI = (1160,0,1390,114)
CANVAS = (2048,2048)
GUIDE_SIZE = (1840,912)  # integer 8x of 230x114, NOT higher native quality
GUIDE_ORIGIN = (104,568)
EYE_ROIS = {'eye_image_left':(69,57,105,88),'eye_image_right':(130,30,176,61)}
EMOTIONS = [('shy','Ngại ngùng',(11,131,308,516)),('angry','Tức giận',(319,131,622,516)),
            ('pain','Đau đớn',(633,131,924,516)),('embarrassed','Xấu hổ',(936,131,1228,516)),
            ('alluring','Quyến rũ',(1240,131,1525,516))]
BASE_LAYERS = ['hair_back','face_base','neck','ear','skin_underpaint','eye_socket_left',
               'eye_socket_right','nose','jaw_transition','hair_front','ornaments']
EXPRESSION_LAYERS = ['brow_image_left','brow_image_right','eye_image_left','eye_image_right',
                     'mouth','blush_image_left','blush_image_right']
FONT = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'


def sha(path:Path):return hashlib.sha256(path.read_bytes()).hexdigest()

def png_bytes(image):
    bio=io.BytesIO();image.save(bio,format='PNG');return bio.getvalue()

def make_ora(path:Path, layer_names:list[str], guide:Image.Image|None=None):
    image=Element('image',{'w':str(CANVAS[0]),'h':str(CANVAS[1]),'name':path.stem,'version':'0.0.3'})
    stack=SubElement(image,'stack')
    empty=png_bytes(Image.new('RGBA', CANVAS))
    with zipfile.ZipFile(path,'w') as archive:
        archive.writestr('mimetype',b'image/openraster',compress_type=zipfile.ZIP_STORED)
        for n,name in enumerate(layer_names):
            p=f'data/layer_{n:02d}.png'
            SubElement(stack,'layer',{'name':name+' [EMPTY]', 'src':p,'visibility':'visible','opacity':'1.0','composite-op':'svg:src-over','x':'0','y':'0'})
            archive.writestr(p,empty,compress_type=zipfile.ZIP_DEFLATED)
        if guide is not None:
            p='data/GUIDE_CANON_V2_DO_NOT_EXPORT.png'
            SubElement(stack,'layer',{'name':'GUIDE_CANON_V2_HIDDEN_NOT_ART','src':p,'visibility':'hidden','opacity':'1.0','composite-op':'svg:src-over','x':'0','y':'0'})
            archive.writestr(p,png_bytes(guide),compress_type=zipfile.ZIP_DEFLATED)
        archive.writestr('stack.xml',tostring(image,encoding='utf-8',xml_declaration=True))
        archive.writestr('mergedimage.png',empty,compress_type=zipfile.ZIP_DEFLATED)

def text(draw,x,y,s,size=22,bold=False,fill='#13283F'):
    f=ImageFont.truetype(FONT_BOLD if bold else FONT,size)
    draw.text((x,y),s,font=f,fill=fill)

def safe_fit(im,size):
    out=im.copy();out.thumbnail(size,Image.Resampling.LANCZOS)
    return out

def create(canon_path:Path,expression_path:Path,out:Path):
    if sha(canon_path)!=CANON_SHA:raise ValueError('CANON V2 SHA mismatch')
    if sha(expression_path)!=EXPR_SHA:raise ValueError('Approved expression reference SHA mismatch')
    canon=Image.open(canon_path).convert('RGBA')
    expr=Image.open(expression_path).convert('RGBA')
    if canon.size!=(1672,941) or expr.size!=(1536,1024):raise ValueError('Native source dimension mismatch')
    out.mkdir(parents=True,exist_ok=True)
    for sub in ('reference','ora','preview'):(out/sub).mkdir(exist_ok=True)
    native=canon.crop(FACE_ROI)
    native.save(out/'reference/CANON_V2_FACE_NATIVE_230x114.png')
    guide=Image.new('RGBA', CANVAS, (0,0,0,0))
    guide.paste(native.resize(GUIDE_SIZE,Image.Resampling.NEAREST),GUIDE_ORIGIN)
    # All content in the guide is hidden in the ORA and is never merged into the sprite.
    make_ora(out/'ora/CP329_FACE_MASTER_EMPTY.ora',BASE_LAYERS,guide=guide)
    for emo,label,_ in EMOTIONS:
        make_ora(out/f'ora/CP329_{emo}_EXPRESSION_EMPTY.ora',EXPRESSION_LAYERS)
    # Produce an artist alignment board with exact-source previews.
    W,H=1700,1060
    board=Image.new('RGB',(W,H),'#F3F6FA');d=ImageDraw.Draw(board)
    d.rectangle((0,0,W,90),fill='#0D2136')
    text(d,35,18,'THANH VÂN KÝ · CP329  |  FACE MASTER INTAKE',33,True,'#FFFFFF')
    text(d,35,65,'SOURCE LOCK  •  Bản V2 và 5 biểu cảm đã duyệt  •  Chưa phải art game',17,False,'#D4E7F4')
    d.rounded_rectangle((24,110,810,635),12,fill='#FFFFFF',outline='#CFDAE5',width=2)
    text(d,46,127,'CANON V2: khuôn mặt gốc (230 × 114 pixel)',23,True)
    # Enlarged by exact 3x for viewing only, no invented detail
    up=native.convert('RGB').resize((690,342),Image.Resampling.NEAREST)
    board.paste(up,(72,193))
    for key,xy in EYE_ROIS.items():
        x0,y0,x1,y1=xy
        rect=(72+x0*3,193+y0*3,72+x1*3,193+y1*3)
        d.rectangle(rect,outline='#12B6DB',width=3)
    text(d,72,543,'Hai vùng mắt cần đối chiếu màu HỔ PHÁCH (không phải ROI mống mắt thuần)',17)
    text(d,72,572,'Phóng to ×3 để xem; chi tiết nguồn vẫn chỉ 230 × 114.',17)
    d.rounded_rectangle((825,110,1675,635),12,fill='#FFFFFF',outline='#CFDAE5',width=2)
    text(d,847,127,'5 BIỂU CẢM ĐÃ CHỐT — chỉ dùng để học sắc thái',23,True)
    for idx,(emo,label,bbox) in enumerate(EMOTIONS):
        crop=expr.crop(bbox).convert('RGB')
        shown=safe_fit(crop,(151,381))
        x=845+idx*162; y=193
        board.paste(shown,(x,y))
        d.rectangle((x,y,x+shown.width,y+shown.height),outline='#B6C8D9',width=2)
        text(d,x,y+396,label,17,True)
    d.rounded_rectangle((24,655,1675,1025),12,fill='#FFFFFF',outline='#CFDAE5',width=2)
    text(d,50,678,'CỔNG NGHIỆM THU CP329  —  KHÔNG ĐƯỢC BỎ QUA',25,True)
    notes=[
        '01  File ORA thật 2048 × 2048, alpha độc lập; không crop poster làm sprite',
        '02  Cùng face master V2 cho cả 5 trạng thái, giữ màu mắt hổ phách',
        '03  Underpaint sạch: chuyển động mí/miệng không tạo lỗ alpha hoặc nhân đôi nét',
        '04  QA ở 256 / 132 / 64 px, chính diện và góc 3/4, không mất nhận diện',
        '05  Cần duyệt riêng ART đã hoàn thiện trước Spine, physics và APK',
    ]
    for i,s in enumerate(notes):text(d,61,732+i*53,s,22,False)
    board.save(out/'preview/CP329_ART_SOURCE_LOCK_AND_REVIEW.png')
    cx=lambda x:GUIDE_ORIGIN[0]+x*8
    cy=lambda y:GUIDE_ORIGIN[1]+y*8
    map_data={
      'schema_version':1,'checkpoint':'CP329','status':'artist_intake_scaffold_not_production_art',
      'approved_canon_visual_id':CANON_ID,'approved_canon_sha256':CANON_SHA,
      'approved_expression_profile_id':EXPR_ID,'approved_expression_sha256':EXPR_SHA,
      'face_bbox_in_canon_xyxy':list(FACE_ROI),'native_face_size_px':[230,114],
      'working_canvas_px':list(CANVAS),'scaled_guide_size_px':list(GUIDE_SIZE),
      'scaled_guide_origin_px':list(GUIDE_ORIGIN),'guide_scale_factor':8,
      'warning':'Reference guide is nearest-neighbor 8x, NOT high-resolution source art. Hidden in ORA.',
      'iris_guides':{k:{'native_bbox_xyxy':list(v),'work_bbox_xyxy':[cx(v[0]),cy(v[1]),cx(v[2]),cy(v[3])], 'measured_iris_only':False}for k,v in EYE_ROIS.items()},
      'base_layers':BASE_LAYERS,'facial_layers_per_expression':EXPRESSION_LAYERS,
      'expressions':[x[0] for x in EMOTIONS],
      'created_empty_oras':6,'created_painted_face_layers':0,
      'visual_preview_approval':'previously_approved_reference_only',
      'production_face_master_ready':False,'underpaint_artist_approved':False,
      'independent_facial_art_ready':False,'spine_rig_verified':False,'android_apk_verified':False,
      'needs_artist_redraw_native_quality':True,
      'files_sha256':{},
    }
    for file in sorted(out.rglob('*')):
        if file.is_file():map_data['files_sha256'][str(file.relative_to(out))]=sha(file)
    (out/'manifest.json').write_text(json.dumps(map_data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return map_data

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--canon',type=Path,required=True)
    ap.add_argument('--expressions',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    print(json.dumps(create(args.canon,args.expressions,args.out),ensure_ascii=False,indent=2)[:1200])
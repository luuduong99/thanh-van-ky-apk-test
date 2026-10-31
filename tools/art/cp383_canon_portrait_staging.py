#!/usr/bin/env python3
"""CP383: Stage exact user-approved CANON source portraits for UI preview.

No generative replacement images, no semantic animation layers, no gameplay release.
Must not be confused with an artist-painted face master or a rig-ready sprite.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_DIM = (941, 1672)
CROPS = [
 ('01_shy_Ngai_ngung', 'Ngại ngùng', (22,681,196,884)),
 ('02_angry_Tuc_gian', 'Tức giận', (203,681,377,884)),
 ('03_pain_Dau_don', 'Đau đớn', (382,681,556,884)),
 ('04_embarrassed_Xau_ho', 'Xấu hổ', (561,681,737,884)),
 ('05_charming_Quyen_ru', 'Quyến rũ', (744,681,918,884)),
]
FRONT = (13,172,230,630)
FONTPATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(sz, bold=False):
    p = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else FONTPATH
    return ImageFont.truetype(p, sz)

def validate(canon_path):
    canon_path = Path(canon_path)
    if hashlib.sha256(canon_path.read_bytes()).hexdigest() != CANON_SHA:
        raise ValueError('CANON_SHA_MISMATCH: refuse to stage unknown character picture')
    with Image.open(canon_path) as im:
        if im.size != CANON_DIM or im.mode != 'RGBA':
            raise ValueError('CANON_FORMAT_MISMATCH')
        return im.copy()

def portrait_panel_image(source, inset=3):
    """Still image only. A strictly interior crop discards the sheet's colored frame.
    Does not promise alpha or image details not present in approved CANON.
    """
    w,h=source.size
    return source.crop((inset,inset,w-inset,h-inset))

def framed_image(im, out_size=(220,260)):
    """UI visualization. Resize is presentation-only, not new source painting."""
    scaled = im.copy(); scaled.thumbnail((out_size[0]-14, out_size[1]-14),Image.Resampling.LANCZOS)
    frame = Image.new('RGBA',out_size, '#1b3b69')
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle((0,0,out_size[0]-1,out_size[1]-1),radius=10,outline='#d8c28a',width=3)
    frame.alpha_composite(scaled,((out_size[0]-scaled.width)//2,(out_size[1]-scaled.height)//2))
    return frame

def draw_proof(canon, images, out):
    board=Image.new('RGB',(1500,750),'#122540');d=ImageDraw.Draw(board)
    d.text((35,23),'CP383 | LÂM THIỂN — 5 ẢNH BIỂU CẢM CANON CHO HỘI THOẠI',fill='#f6f7fc',font=font(27,True))
    d.text((35,68),'Chỉ lấy nguyên pixel từ CANON V2.1, KHÔNG dùng lại ảnh vector CP379–382 để thay mặt nhân vật.',fill='#dfebff',font=font(17))
    for i,((key,label,box),im) in enumerate(zip(CROPS,images)):
        x=25+i*293
        d.rounded_rectangle((x,113,x+278,575),radius=14,fill='#213b5b',outline='#9ab9df',width=2)
        f=framed_image(portrait_panel_image(im),(246,292));board.paste(f.convert('RGB'),(x+16,144))
        d.text((x+17,118),f'{i+1:02d}. {label}',fill='#fff0cc',font=font(17,True))
        d.text((x+16,458),f'{im.width}×{im.height} pixel CANON',fill='#cfe2fa',font=font(15))
        d.text((x+16,490),'Nguồn: cùng ảnh đã duyệt',fill='#bcd4ec',font=font(13))
        d.text((x+16,518),'Chưa phải sprite chuyển động',fill='#ffdbbd',font=font(13))
    d.rounded_rectangle((34,607,1468,712),radius=12,fill='#1f3652',outline='#627fa0',width=2)
    d.text((54,630),'Nguồn bitmap gốc: đúng nhận diện • Hình xem thử UI có thay đổi kích thước hiển thị, KHÔNG tăng chi tiết nguồn.',fill='#dceafd',font=font(17))
    d.text((54,663),'CP383: ảnh chân dung tĩnh có kiểm chứng. Mặt vẽ mới, tóc/da ẩn, Spine và APK vẫn CHƯA ĐẠT.',fill='#f2d5bc',font=font(16))
    board.save(out)

def draw_dialogue_mock(canon, portrait, output):
    W,H=1600,900
    # Purely decorative fantasy UI backdrop. Only character illustration is exact CANON-derived bitmap.
    array=np.empty((H,W,3),dtype=np.uint8)
    for y in range(H):
        t=y/(H-1)
        array[y,:,0]=int(11+14*t)
        array[y,:,1]=int(26+19*t)
        array[y,:,2]=int(53+18*t)
    im=Image.fromarray(array,'RGB').convert('RGBA'); d=ImageDraw.Draw(im)
    for i in range(9):
        x=i*220+30
        d.arc((x-120,85,x+260,620),190,342,fill=(64,100,151,65),width=2)
    d.text((48,29),'THANH VÂN KÝ',font=font(28,True),fill='#f1e2c4')
    d.text((49,73),'BẢN XEM THỬ GIAO DIỆN — CHỈ DÙNG ẢNH CANON',font=font(17),fill='#cfdfec')
    # Full character from the same sheet for reference, NO vector proxy.
    front=canon.crop(FRONT)
    side=front.resize((282,594),Image.Resampling.LANCZOS)
    im.alpha_composite(side,(93,158))
    # Bottom half-transparent dialogue frame and CANON closeup.
    pane=Image.new('RGBA',(1512,305),(14,33,66,220))
    pd=ImageDraw.Draw(pane)
    pd.rounded_rectangle((0,0,1511,304),radius=22,outline=(196,174,120,240),width=3)
    im.alpha_composite(pane,(44,570))
    face=framed_image(portrait_panel_image(portrait),(216,251))
    im.alpha_composite(face,(426,598))
    d=ImageDraw.Draw(im)
    d.text((682,616),'Lâm Thiển',font=font(29,True),fill='#f9e4bb')
    d.text((682,674),'Biểu cảm: Ngại ngùng',font=font(24),fill='#f5f7fd')
    d.text((682,726),'Ảnh gốc của nhân vật, không phải bản vector kỹ thuật.',font=font(20),fill='#cfdef4')
    d.text((682,772),'Ảnh hội thoại tĩnh — hoạt ảnh và rig chưa hoàn thành.',font=font(17),fill='#b9cedf')
    for j,ch in enumerate(['◉','◇','☰']):
        d.rounded_rectangle((1495,164+j*96,1556,225+j*96),radius=12,outline='#9db4d1',width=2)
        d.text((1512,178+j*96),ch,font=font(22,True),fill='#ebd8ab')
    im.convert('RGB').save(output)

def build(canon_path, outdir):
    # Full preflight: invalid CANON creates no output folder.
    canon=validate(canon_path)
    root=Path(outdir);root.mkdir(parents=True,exist_ok=True)
    (root/'portraits').mkdir(exist_ok=True)
    shutil.copyfile(canon_path,root/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    (root/'qa').mkdir(exist_ok=True)
    exact=[]; inner=[]
    for key,label,box in CROPS:
        im=canon.crop(box)
        im.save(root/'portraits'/f'{key}_CANON_EXACT.png')
        sub=portrait_panel_image(im)
        sub.save(root/'portraits'/f'{key}_INNER_CROP_SOURCE_ONLY.png')
        exact.append(im);inner.append(sub)
    # Atlas: pad each image without scaling, no resampling and no color changes.
    padding=16; xcur=padding; atlas_w=32+sum(im.width+padding for im in exact); atlas_h=max(im.height for im in exact)+padding*2
    atlas=Image.new('RGBA',(atlas_w,atlas_h),(0,0,0,0)); entries=[]
    for (key,label,box),im,sub in zip(CROPS,exact,inner):
        atlas.alpha_composite(im,(xcur,padding))
        entries.append({'id':key,'expression_label':label,'atlas_rect_px':[xcur,padding,im.width,im.height],
                        'source_sheet_bbox_px':list(box),'source_native_dimensions_px':[im.width,im.height],
                        'exact_crop_filename':f'portraits/{key}_CANON_EXACT.png',
                        'ui_inner_crop_filename':f'portraits/{key}_INNER_CROP_SOURCE_ONLY.png',
                        'ui_inner_crop_source_bounds':[3,3,im.width-3,im.height-3],
                        'game_asset_state':'staging_only_not_imported'})
        xcur+=im.width+padding
    atlas.save(root/'PORTRAIT_ATLAS_EXACT_SOURCE_ONLY.png')
    draw_proof(canon,exact,root/'qa'/'CP383_CANON_ONLY_PORTRAIT_PREVIEW.png')
    draw_dialogue_mock(canon,exact[0],root/'qa'/'CP383_LANDSCAPE_DIALOGUE_CANON_STATIC_PREVIEW.png')
    report={
        'checkpoint':'CP383','identity':'Lâm Thiển','canon_sha256':CANON_SHA,
        'source_approved':True,'character_design_source':'user_approved_CANON_V2_1',
        'source_only_no_generated_character_replacements':True,
        'assets':entries,'atlas_dimensions_px':[atlas_w,atlas_h],
        'portrait_mode':'static_bitmap_exact_CANON_crops',
        'atlas_rgb_source_pixel_exact':True,
        'not_a_transparent_cutout':True,
        'not_an_artist_painted_new_face':True,
        'not_a_high_res_new_face_master':True,
        'native_source_resolution_limited':True,
        'rig_or_spine_ready':False,'fullbody_animation_ready':False,
        'visual_qa':'SOURCE_FIDELITY_PASSED_ART_REBUILD_PENDING',
        'production_release':'blocked_pending_art','sprite_paths':{},'apk_ready':False,
        'limitations':['Original CANON portraits include sheet backgrounds; no semantic hair/skin separation.',
                       'Portraits are 174/176 by 203 source pixels, UI scaling does not create details.',
                       'No blinking, mouth animation, Spine, combat sprite, or built Android APK.',
                       'Landscape mock is a static UI-only preview, not a screenshot of a running build.'],
        'next':'CP384 artist-painted face master per approved CANON and alpha/rig validation'
    }
    (root/'CP383_SOURCE_PORTRAIT_MANIFEST.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=build(a.canon,a.out)
    print(json.dumps({'checkpoint':result['checkpoint'],'atlas':result['atlas_dimensions_px'],'portraits':len(result['assets']),'release':result['production_release']},ensure_ascii=False))
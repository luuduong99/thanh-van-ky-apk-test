#!/usr/bin/env python3
"""CP399: exact CANON / CP398 review board & approval hold.

No artificial edits to the character, no animation frames or production export.
All displayed pictures are crops of exact input sources.
"""
from __future__ import annotations
import argparse, hashlib, io, json, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CP397_SHA = '0baf2ad9c2524ac355d106556dea0b506f12644dc99a1b3d77df3e522de3d554'
CP398_NATURAL_SHA = '6f36ba97e307f3c31c4166dd9a539ec945f12dde4a31370196e0c7497af391ea'
CP398_SOFT_SHA = '5ce4ab198235a58905d8f867f53973d7d49d3e9686bb769675568d454c142c17'
CROP = (25,684,193,881); SIZE = (168,197); FULL_SIZE = (941,1672)
ROIS = {'LEFT': (29,93,71,124), 'RIGHT': (83,70,129,110)}
ART_APPROVAL = 'PENDING_HUMAN_VISUAL_REVIEW'
PRODUCTION = {'status':'blocked_pending_approved_eye_art','sprite_paths':{},'spine_ready':False,'apk_ready':False}

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load_checked(path,expected,dim):
    if sha(path) != expected: raise ValueError('SHA_MISMATCH_'+Path(path).stem)
    with Image.open(path) as image:
        if image.size != dim or image.mode != 'RGBA': raise ValueError('MODE_OR_SIZE_MISMATCH_'+Path(path).stem)
        return image.copy()

def outside_changes(a,b):
    ia=np.asarray(a);ib=np.asarray(b)
    mask=np.ones((SIZE[1],SIZE[0]),dtype=bool)
    for x1,y1,x2,y2 in ROIS.values():mask[y1:y2,x1:x2]=False
    return int(np.any(ia[mask]!=ib[mask],axis=-1).sum())

def changed(a,b):
    return int(np.any(np.asarray(a)!=np.asarray(b),axis=-1).sum())

def validate(canon,cp397,natural,soft):
    source=load_checked(canon,CANON_SHA,FULL_SIZE)
    original=source.crop(CROP).copy()
    previous=load_checked(cp397,CP397_SHA,SIZE)
    variants={'Natural':load_checked(natural,CP398_NATURAL_SHA,SIZE),
              'Soft':load_checked(soft,CP398_SOFT_SHA,SIZE)}
    for name,image in [('CP397',previous),*variants.items()]:
        if outside_changes(original,image):raise ValueError('OUTSIDE_EYE_ROI_CHANGED_'+name)
    if changed(variants['Natural'],variants['Soft']) < 5:
        raise ValueError('VARIANTS_NOT_INDEPENDENT')
    return original, previous, variants

def f(size, bold=False):
    p='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf'
    return ImageFont.truetype(p,size)

def board(orig,prev,variants,path):
    # Presentation-only interpolation. All source pixels remain in native PNGs.
    cards=[('CANON V2.1 / APPROVED',orig),('CP398 NATURAL / DRAFT',variants['Natural']),('CP398 SOFT / DRAFT',variants['Soft'])]
    W,H=1920,1080; bg=Image.new('RGB',(W,H),(243,248,252)); d=ImageDraw.Draw(bg)
    ink=(27,52,76); muted=(77,100,119); accent=(156,85,63)
    d.text((65,38),'THANH VÂN KÝ  /  CP399 — LÂM THIỂN',font=f(35,True),fill=ink)
    d.text((65,98),'Duyệt mỹ thuật mắt nhắm • Nguồn ảnh CANON V2.1 nguyên vẹn • Chưa có animation',font=f(21),fill=muted)
    for i,(name,im) in enumerate(cards):
        x=64+i*615; y=188
        d.rounded_rectangle((x,y,x+570,y+767),radius=14,fill='white',outline=(212,225,235),width=3)
        w,h=504,591
        bg.paste(im.convert('RGB').resize((w,h),Image.Resampling.LANCZOS),(x+33,y+60))
        d.text((x+32,y+16),name,font=f(21,True),fill=ink if i==0 else accent)
        note='Crop gốc 168×197 • hiển thị ×3' if i==0 else 'Đề xuất, CHƯA ĐƯỢC DUYỆT'
        d.text((x+31,y+679),note,font=f(18),fill=muted)
        d.text((x+31,y+720),'Mọi pixel ngoài vùng mắt vẫn là CANON',font=f(16),fill=muted)
    d.text((66,991),'NHẬN XÉT: Natural rõ nét hơn; Soft nhẹ hơn nhưng mờ. Cả hai cần họa sĩ xử lý chuyển sắc da và chân mi.',font=f(18),fill=ink)
    d.text((66,1027),'Ảnh minh họa từ đúng CANON và các bản CP398; không phải render nhân vật mới hoặc ảnh nghiệm thu.',font=f(16),fill=accent)
    bg.save(path)

def eyes_board(orig,prev,variants,path):
    items=[('CANON',orig),('CP397',prev),('NATURAL / DRAFT',variants['Natural']),('SOFT / DRAFT',variants['Soft'])]
    W,H=1880,870;bg=Image.new('RGB',(W,H),(13,32,50)); d=ImageDraw.Draw(bg)
    d.text((32,21),'CP399 — SO SÁNH MẮT GỐC  /  PHÓNG 8×, KHÔNG NỘI SUY',font=f(24,True),fill='white')
    d.text((32,60),'Đường nét ở kích thước gốc chỉ 168×197 px. Các vùng ảnh bên dưới đều đến từ Lâm Thiển CANON V2.1.',font=f(17),fill=(220,235,248))
    for row,(side,bb) in enumerate(ROIS.items()):
        l,t,r,b=bb; box=(max(0,l-5),max(0,t-5),min(168,r+5),min(197,b+5))
        crop_w,crop_h=box[2]-box[0],box[3]-box[1]
        zoom=8; top=131+row*356
        for i,(title,image) in enumerate(items):
            x=32+i*460
            d.text((x,top-31),f'{side} / {title}',font=f(17,True),fill='white')
            shot=image.crop(box).resize((crop_w*zoom,crop_h*zoom),Image.Resampling.NEAREST).convert('RGB')
            bg.paste(shot,(x,top))
        # Annotation in the margin, not on face pixels
    d.text((32,H-35),'Đề nghị vẽ lại mỹ thuật trên lớp gốc: chân mi thon dần, da mí có kết cấu mềm, không còn viền xám thẳng.',font=f(17),fill=(255,208,175))
    bg.save(path)

def build(canon,cp397,natural,soft,out):
    orig,prev,opts=validate(canon,cp397,natural,soft) # Validate everything BEFORE output dir creation.
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    orig.save(out/'CP399_EXACT_CANON_FACE_168x197.png')
    prev.save(out/'CP399_CP397_SOURCE_DRAFT.png')
    for name,im in opts.items():im.save(out/f'CP399_CP398_{name.upper()}_SOURCE_DRAFT.png')
    board(orig,prev,opts,out/'CP399_CANON_NATURAL_SOFT_REVIEW_16x9.png')
    eyes_board(orig,prev,opts,out/'CP399_EYES_EXACT_NATIVE_ZOOM.png')
    report={
     'checkpoint':'CP399','date':'2026-10-30','source_policy':'EXACT_CANON_ONLY',
     'canon_full_image_sha256':CANON_SHA,'source_size':list(SIZE),'crop':list(CROP),
     'source_hashes':{'CP397':CP397_SHA,'Natural':CP398_NATURAL_SHA,'Soft':CP398_SOFT_SHA},
     'eye_rois':{k:list(v) for k,v in ROIS.items()},
     'changed_pixels_vs_canon':{name:changed(orig,im) for name,im in opts.items()},
     'changed_pixels_vs_CP397':{name:changed(prev,im) for name,im in opts.items()},
     'difference_between_variants':changed(opts['Natural'],opts['Soft']),
     'outside_eye_changes':{name:outside_changes(orig,im) for name,im in opts.items()},
     'review':{'natural':'crisper lid, still artificial dark contour',
               'soft':'subtler contour, but overly pale/flat',
               'choice':'NO_FINAL_CHOICE_YET',
               'needs_hand_painted_refinement':['taper real lashes at corners',
                'blend eyelid crease with exact CANON skin light','remove artificially straight gray lash band',
                'visual check at native and enlarged size']},
     'human_visual_approval':ART_APPROVAL,'production_release':PRODUCTION,
     'next':'Obtain artist-quality closed-eye master from the same character and explicit user approval BEFORE blink inbetweens or APK import.'}
    (out/'CP399_REVIEW_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    approval={'status':'NOT_APPROVED','character':'Lâm Thiển','candidate':'NONE',
        'verified_source_sha256':CANON_SHA,'approved_visual_sha256':None,
        'approved_by_user':False,'production_release':PRODUCTION,
        'note':'This is intentionally incomplete. Do not mark approved based on technical PASS or assistant judgement alone.'}
    (out/'CP399_APPROVAL_GATE_NOT_APPROVED.json').write_text(json.dumps(approval,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

def release_allowed(record):
    # CP399 explicitly cannot release a draft, even with a spurious approval key.
    return False

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--canon',required=True);parser.add_argument('--cp397',required=True)
    parser.add_argument('--natural',required=True);parser.add_argument('--soft',required=True);parser.add_argument('--out',required=True)
    a=parser.parse_args();print(json.dumps(build(a.canon,a.cp397,a.natural,a.soft,a.out),ensure_ascii=False,indent=2))
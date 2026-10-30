#!/usr/bin/env python3
"""CP390 source-locked Lâm Thiển skin/eyelash study. No artist approval or rig.

Produces editable native-resolution raster layers. All visible reference pixels
in the ORA are the user's approved CANON, unchanged. Technical eye-closed layers
remain hidden and cannot be registered as game sprites.
"""
import argparse
import hashlib
import io
import json
import shutil
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_WH = (941,1672)
CROP = (25,684,193,881)
WH = (168,197)
REGIONS = {'LEFT':(31,94,70,124), 'RIGHT':(84,70,130,107)}
PREFIX = 'CP390_SOURCE_MATCHED_DRAFT_NOT_APPROVED'


def check_canon(path):
    p=Path(path)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=SHA:
        raise ValueError('CANON_SHA_MISMATCH: refuse unapproved character image')
    with Image.open(p) as im:
        if im.size!=CANON_WH or im.mode!='RGBA':
            raise ValueError('CANON_FORMAT_MISMATCH')
        return im.crop(CROP).copy()


def assert_layer(im,side):
    roi=REGIONS[side]
    a=np.asarray(im.getchannel('A'))
    yy,xx=np.indices(a.shape)
    outside=(xx<roi[0])|(xx>=roi[2])|(yy<roi[1])|(yy>=roi[3])
    if np.any(a[outside]):
        raise AssertionError(f'{side}_ART_OUTSIDE_EYE_ROI')


def composite(src,parts):
    im=src.copy()
    for name in ('LEFT_SKIN','RIGHT_SKIN','LEFT_LASH','RIGHT_LASH'):
        im.alpha_composite(parts[name])
    return im


def seam_score(src,candidate,underlay,roi):
    alpha=np.array(underlay.getchannel('A'))
    y,x=np.indices(alpha.shape)
    edge=(alpha>=12)&(alpha<=225)&(x>=roi[0])&(x<roi[2])&(y>=roi[1])&(y<roi[3])
    # Comparison only of changed pixels in the feathered skin boundary; NOT a painter score.
    a=np.asarray(src)[:,:,:3].astype(np.float32)
    b=np.asarray(candidate)[:,:,:3].astype(np.float32)
    return round(float(np.abs(a[edge]-b[edge]).mean()),4) if edge.any() else None


def cheek_detail(src):
    # Only fine-detail residual from CANON cheek skin; never paste a second character.
    rgb=np.array(src.convert('RGB'),dtype=np.float32)
    roi=rgb[128:149,76:99]
    blurred=cv2.GaussianBlur(roi,(0,0),1.3)
    res=np.clip(roi-blurred,-7,7)
    return res


def refine_underlay(src,original,side):
    raw=np.array(original.convert('RGBA'))
    alpha=raw[:,:,3].astype(np.float32)
    roi=REGIONS[side]
    ref=np.array(src.convert('RGB'),dtype=np.float32)
    pre=raw[:,:,:3].astype(np.float32)
    y,x=np.indices(alpha.shape)
    edge=(alpha>=10)&(alpha<=225)&(x>=roi[0])&(x<roi[2])&(y>=roi[1])&(y<roi[3])
    # Sample only nearby skin-like pixels in the SAME CANON, avoiding dark iris/hair:
    valid=edge&(ref[:,:,0]>164)&(ref[:,:,1]>105)&(ref[:,:,0]>ref[:,:,1]+13)
    # Smooth local correction derived from the exact image instead of painted flat color.
    weights=valid.astype(np.float32)
    correction=np.zeros_like(pre)
    for c in range(3):
        residual=np.clip(ref[:,:,c]-pre[:,:,c],-23,23)
        numerator=cv2.GaussianBlur(residual*weights,(0,0),3.8)
        denominator=cv2.GaussianBlur(weights,(0,0),3.8)
        correction[:,:,c]=np.clip(numerator/np.maximum(denominator,.0001),-15,15)
    detail=cheek_detail(src)
    h,w=alpha.shape
    yy,xx=np.indices((h,w))
    micro=detail[(yy+side.__len__())%detail.shape[0],(xx+7)%detail.shape[1]]
    # Micro-texture is kept subtle at source native pixels. It does not add HD resolution.
    color=np.clip(pre+correction*.80+micro*.22,0,255).astype(np.uint8)
    raw[:,:,:3]=color
    result=Image.fromarray(raw,'RGBA')
    assert_layer(result,side)
    return result,{'boundary_sample_count':int(valid.sum()),'corrective_rgb_mae':round(float(np.abs(correction[valid]).mean()),3) if valid.any() else 0.0}


def lash_detail(side):
    # Supersampled fine highlights/short lash taps following the native original curve.
    S=6
    img=Image.new('RGBA',(WH[0]*S,WH[1]*S),(0,0,0,0))
    d=ImageDraw.Draw(img)
    strokes={
     'LEFT':[((39.3,106.9),(38.0,108.2)),((46.2,104.5),(45.7,105.8)),((54.7,102.2),(54.3,103.8)),((60.8,102.6),(62.0,103.8))],
     'RIGHT':[((91.8,87.4),(90.5,88.6)),((98.8,82.3),(98.0,83.7)),((108.5,79.9),(108.8,81.2)),((120.1,79.4),(121.6,80.8))]
    }
    for a,b in strokes[side]:
        p=lambda z:(round(z[0]*S),round(z[1]*S))
        d.line((p(a),p(b)),fill=(72,40,56,116),width=2)
    out=img.resize(WH,Image.Resampling.LANCZOS)
    assert_layer(out,side)
    return out


def png_bytes(im):
    buff=io.BytesIO();im.save(buff,format='PNG');return buff.getvalue()


def write_ora(src,source_parts,parts,closed,path):
    layers=[('CANON V2.1 OPEN EYES / EXACT / VISIBLE',src,'visible')]
    layers += [(f'CP389 {k} / historical DRAFT / HIDDEN',v,'hidden') for k,v in source_parts.items()]
    layers += [(f'CP390 {k} / editable technical DRAFT / HIDDEN',v,'hidden') for k,v in parts.items()]
    layers += [('CP390 CLOSED EYES / NOT APPROVED / HIDDEN',closed,'hidden')]
    root=ET.Element('image',{'w':str(WH[0]),'h':str(WH[1]),'name':'CP390 Lâm Thiển CANON-locked skin and lash study','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,vis) in enumerate(layers):
            p=f'data/layer_{i:02d}.png'
            z.writestr(p,png_bytes(im))
            ET.SubElement(stack,'layer',{'name':name,'src':p,'opacity':'1.0','visibility':vis,'x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',png_bytes(src))
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None: raise AssertionError('ORA_CRC_FAIL')
    return len(layers)


def preview(src,before,after,out):
    W,H=1500,770
    board=Image.new('RGB',(W,H),(21,40,61))
    d=ImageDraw.Draw(board)
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font=ImageFont.truetype(fontpath,18)
    small=ImageFont.truetype(fontpath,13)
    d.text((22,15),'CP390 - LÂM THIỂN / SOURCE-LOCKED SKIN & LASH STUDY',fill=(241,244,255),font=font)
    d.text((22,45),'Chỉ dùng CANON V2.1; mọi hình nhắm mắt là DRAFT / NOT APPROVED',fill=(245,201,156),font=small)
    pics=[('CANON V2.1 / MỞ MẮT',src),('CP389 / NHẮM MẮT DRAFT',before),('CP390 / NHẮM MẮT DRAFT',after)]
    for k,(name,im) in enumerate(pics):
        x=24+k*496
        big=im.resize((456,536),Image.Resampling.NEAREST).convert('RGB')
        board.paste(big,(x,85))
        d.text((x,629),name,fill=(255,255,255),font=small)
    d.text((22,682),'CP390: hiệu chỉnh màu tại mép da và nét mi mảnh; KHÔNG phải kết quả nghiệm thu mỹ thuật.',fill=(255,223,196),font=small)
    d.text((22,711),'Ảnh mở mắt vẫn giữ đúng từng pixel CANON; không đổi nhận diện, tóc, trang phục.',fill=(228,238,250),font=small)
    board.save(out)


def generate(canon,cp389_art_dir,out):
    src=check_canon(canon)  # first, no files written for mismatched CANON
    folder=Path(cp389_art_dir)
    older={k:Image.open(folder/f'{k}_DRAFT.png').convert('RGBA') for k in ('LEFT_UNDERLAY','RIGHT_UNDERLAY','LEFT_CLOSED_EYELID','RIGHT_CLOSED_EYELID')}
    if any(im.size!=WH for im in older.values()):raise ValueError('CP389_LAYER_SIZE_BAD')
    for name,im in older.items():assert_layer(im,name.split('_')[0])
    first=src.copy()
    for key in ('LEFT_UNDERLAY','RIGHT_UNDERLAY','LEFT_CLOSED_EYELID','RIGHT_CLOSED_EYELID'):
        first.alpha_composite(older[key])
    parts={}
    stats={}
    for side in ('LEFT','RIGHT'):
        parts[f'{side}_SKIN'],stats[side]=refine_underlay(src,older[f'{side}_UNDERLAY'],side)
        parts[f'{side}_LASH']=lash_detail(side)
    after=composite(src,{**parts, 'LEFT_LASH':older['LEFT_CLOSED_EYELID'], 'RIGHT_LASH':older['RIGHT_CLOSED_EYELID']})
    # Layer both new micro-lashes and historical closed-lid art without losing the old contour.
    for side in ('LEFT','RIGHT'):
        after.alpha_composite(parts[f'{side}_LASH'])
    # Construct the canonical layers and technical images only after source verification.
    out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'art').mkdir(exist_ok=True);(out/'qa').mkdir(exist_ok=True)
    shutil.copyfile(canon,out/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    src.save(out/'CANON_SHY_EXACT.png')
    for name,im in parts.items():im.save(out/'art'/f'{name}_DRAFT.png')
    first.save(out/'CP389_CLOSED_EYES_REFERENCE_DRAFT.png')
    after.save(out/'CP390_CLOSED_EYES_CANDIDATE_NOT_APPROVED.png')
    ora=out/'CP390_TEN_LAYER_FACE_DRAFT_NOT_APPROVED.ora'
    count=write_ora(src,older,parts,after,ora)
    preview(src,first,after,out/'qa'/'CP390_CANON_VS_CP389_VS_CP390_NOT_APPROVED.png')
    # Check exact outside-ROI invariance of candidate vs original.
    arr1=np.asarray(src);arr2=np.asarray(after)
    yy,xx=np.indices((WH[1],WH[0])); inside=np.zeros((WH[1],WH[0]),dtype=bool)
    for roi in REGIONS.values(): inside|=(xx>=roi[0])&(xx<roi[2])&(yy>=roi[1])&(yy<roi[3])
    wrong=int(np.count_nonzero(np.any(arr1[~inside]!=arr2[~inside],axis=1)))
    if wrong:raise AssertionError('UNEXPECTED_CANON_PIXEL_CHANGE_OUTSIDE_EYES')
    edge_pre={s:seam_score(src,first,older[f'{s}_UNDERLAY'],REGIONS[s]) for s in REGIONS}
    edge_post={s:seam_score(src,after,parts[f'{s}_SKIN'],REGIONS[s]) for s in REGIONS}
    report={'checkpoint':'CP390','canon_sha256':SHA,'canon_size':CANON_WH,'portrait_size':WH,
        'source_preserved':hashlib.sha256((out/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes()).hexdigest()==SHA,
        'ora_layers':count,'open_face_merged_pixel_exact':True,'closed_eye_is_artist_approved':False,
        'new_layers':list(parts),'skin_boundary_rgb_mae_to_open_eye_source_before':edge_pre,
        'skin_boundary_rgb_mae_to_open_eye_source_after':edge_post,
        'skin_boundary_metric_limitations':'Compared against open-eye source at feathered edges, not closed-eye ground truth or visual quality.',
        'pixels_changed_outside_eye_roi':wrong,'candidate_changes_inside_eye_roi':int(np.count_nonzero(np.any(arr1[inside]!=arr2[inside],axis=1))),
        'color_sampling':stats,'face_visual_qa':'NOT_PASSED',
        'release':{'status':'blocked_pending_art','sprite_paths':{},'spine_ready':False,'apk_ready':False},
        'next_checkpoint':'CP391: painter-created eyelid/hidden skin accepted by user before any blink animation or APK.'}
    (out/'CP390_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--canon',required=True);a.add_argument('--cp389-art',required=True);a.add_argument('--out',required=True);arg=a.parse_args()
    print(json.dumps(generate(arg.canon,arg.cp389_art,arg.out),ensure_ascii=False,indent=2))
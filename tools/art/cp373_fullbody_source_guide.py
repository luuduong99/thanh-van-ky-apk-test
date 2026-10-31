#!/usr/bin/env python3
"""CP373 Lâm Thiển exact-CANON source-derived full-body guide.

NOT a native-painted high resolution production art, NOT rig/Spine-ready.
Preserves original RGB where alpha survives, and creates coarse source-region masks.
It deliberately reports the lack of occluded underpaint as a release-blocking condition.
"""
import argparse
import hashlib
import io
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
SIZE = (941,1672)
BBOX = (13,172,230,630)
FRONT_SIZE=(217,458)
TOES = {'image_left':(79,432,102,458),'image_right':(109,414,122,446)}
NAMES=[
  '01_left_outer_ribbons','02_right_outer_ribbons',
  '03_rear_hair_left_guide','04_rear_hair_right_guide',
  '05_left_leg_source','06_right_leg_source',
  '07_left_shoe_blue_toe','08_right_shoe_blue_toe',
  '09_center_skirt_source','10_bodice_waist_source',
  '11_neck_jewelry_source','12_face_front_hair_source',
  '13_left_sleeve_source','14_left_hand_source',
  '15_right_sleeve_source','16_right_hand_source',
  '17_left_shoulder_gold_source','18_right_shoulder_gold_source',
  '19_transition_residual_source'
]
COLORS=['#5a83c7','#89b7ee','#b899c8','#9a88c1','#e4a09e','#efc1a1',
 '#2475dc','#67a5ed','#83bade','#7b9ecd','#bd9b43','#aa83b1',
 '#7f76c4','#e1a2ad','#9b83c9','#dca3af','#d4a343','#b58532','#777b86']

def get_canon(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SHA:
        raise ValueError('Wrong CANON bytes; refuse to create CP373 output')
    im=Image.open(io.BytesIO(raw))
    if im.mode!='RGBA' or im.size!=SIZE:
        raise ValueError('CANON dimensions/mode mismatch')
    return im

def region_polygon(labels, code, points):
    canvas=Image.fromarray(labels.astype(np.int32),mode='I')
    ImageDraw.Draw(canvas).polygon(points,fill=code)
    return np.array(canvas,dtype=np.int32)

def matte(front):
    rgb=np.asarray(front.convert('RGB'))
    h,w=rgb.shape[:2]
    mask=np.zeros((h,w),np.uint8)
    cv2.grabCut(rgb[:,:,::-1].copy(),mask,(5,12,207,443),
                np.zeros((1,65),np.float64),np.zeros((1,65),np.float64),
                5,cv2.GC_INIT_WITH_RECT)
    original=np.logical_or(mask==cv2.GC_FGD,mask==cv2.GC_PR_FGD)
    R,G,B=[rgb[:,:,i].astype(np.int16) for i in range(3)]
    blue=((B-R>=13)&(B-G>=3)&(B>135)) | ((B-R>=6)&(B-G>=2)&(R<205)&(G<225))
    yy,xx=np.ogrid[:h,:w]
    probable=blue & (yy>=90)&(yy<455)&(xx>=3)&(xx<214)
    probable=cv2.morphologyEx(probable.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    n,lab,stats,_=cv2.connectedComponentsWithStats(probable)
    good=[i for i in range(1,n) if stats[i,4]>=8]
    probable=cv2.dilate(np.isin(lab,good).astype(np.uint8),np.ones((3,3),np.uint8),iterations=1)>0
    result=original|probable
    result[:12,:]=False  # visible "Front" header is not part of the character
    # Exclude obviously flat floor band; keep deep-blue ribbons and central shoes.
    floor=(yy>=428) & ~(((B-R>=19)&(B-G>=6)) | ((xx>=83)&(xx<=121)))
    result=np.where(floor,False,result)
    # For shoe-tip safety, blue toe coverage comes from the original image.
    for box in TOES.values():
        x1,y1,x2,y2=box
        patch=((B[y1:y2,x1:x2]-R[y1:y2,x1:x2]>=18)&(B[y1:y2,x1:x2]>90))
        result[y1:y2,x1:x2] |= patch
    result[457:,:]=False  # bottom border / floor, not a foot keypoint
    return (result*255).astype(np.uint8),original.astype(bool),probable.astype(bool)

def labels_map():
    # Source-pixel routing hints only. These polygon boundaries DO NOT encode real anatomical separations.
    x=np.full((458,217),19,dtype=np.int32)
    # broad flowing lengths
    x=region_polygon(x,1,[(0,105),(86,105),(92,170),(91,260),(83,380),(51,458),(0,458)])
    x=region_polygon(x,2,[(124,112),(217,110),(217,458),(166,458),(126,373),(126,260),(128,164)])
    # back hair and neck
    x=region_polygon(x,3,[(80,12),(112,18),(105,92),(76,154),(41,194),(23,173),(57,93)])
    x=region_polygon(x,4,[(110,17),(139,20),(165,98),(195,169),(167,179),(127,131),(121,80)])
    # legs in front of long ribbons
    x=region_polygon(x,5,[(78,222),(106,221),(108,260),(104,362),(103,436),(87,433),(81,391),(74,307)])
    x=region_polygon(x,6,[(106,222),(134,222),(142,305),(130,389),(121,431),(109,423),(105,340),(102,263)])
    x=region_polygon(x,7,[(84,395),(104,398),(103,443),(101,458),(84,458),(83,425)])
    x=region_polygon(x,8,[(107,389),(121,393),(123,437),(108,442),(107,421)])
    x=region_polygon(x,9,[(71,170),(144,169),(144,213),(120,270),(99,265),(75,217)])
    x=region_polygon(x,10,[(68,99),(148,99),(152,182),(132,198),(86,193),(67,170)])
    x=region_polygon(x,11,[(93,75),(123,77),(126,110),(96,112)])
    x=region_polygon(x,12,[(76,14),(145,14),(144,82),(130,93),(88,91),(76,76)])
    # shoulder/sleeve pieces drawn on top
    x=region_polygon(x,13,[(62,117),(84,126),(75,163),(50,192),(22,212),(17,194),(37,153)])
    x=region_polygon(x,14,[(0,183),(35,179),(41,193),(24,211),(0,214)])
    x=region_polygon(x,15,[(135,125),(159,119),(194,159),(204,195),(173,210),(143,173)])
    x=region_polygon(x,16,[(180,180),(217,183),(217,214),(192,211),(176,195)])
    x=region_polygon(x,17,[(54,110),(80,111),(78,146),(55,145)])
    x=region_polygon(x,18,[(138,111),(163,111),(164,149),(140,150)])
    return x.astype(np.uint8)

def blue_mask(arr):
    rgb=arr[...,:3].astype(np.float32)
    return ((rgb[...,2]>rgb[...,0]*1.14)&(rgb[...,2]>rgb[...,1]*1.09)&(rgb[...,2]>90))

def create(canon_path, dest):
    canon=get_canon(canon_path)  # preflight before any output directory is made
    out=Path(dest);out.mkdir(parents=True,exist_ok=True)
    for sub in ('source','masks','layers','qa','ora'):(out/sub).mkdir(exist_ok=True)
    src=canon.crop(BBOX)
    src.save(out/'source'/'FRONT_EXACT_CROP_WITH_BACKGROUND.png')
    alpha,raw_grab,extra=matte(src)
    rgb=np.asarray(src.convert('RGB'))
    rgba=np.dstack([rgb,alpha]).astype(np.uint8)
    Image.fromarray(rgba).save(out/'source'/'FRONT_MATTE_DRAFT_NOT_ART.png')
    Image.fromarray(alpha).save(out/'masks'/'foreground_alpha_editable.png')
    label=labels_map()
    srcLayers=[]
    for i,name in enumerate(NAMES,1):
        lm=np.where(label==i,alpha,0).astype(np.uint8)
        Image.fromarray(lm).save(out/'masks'/(name+'_mask.png'))
        img=Image.fromarray(np.dstack([rgb,lm]).astype(np.uint8),'RGBA')
        img.save(out/'layers'/(name+'.png'))
        srcLayers.append(img)
    # Every visible source-matte pixel goes into exactly one region; no additive overlaps.
    rebuilt=Image.new('RGBA',FRONT_SIZE,(0,0,0,0))
    for layer in srcLayers:rebuilt.alpha_composite(layer)
    result=np.asarray(rebuilt)
    assert np.array_equal(result[:,:,3],alpha)
    assert np.array_equal(result[alpha>0,:3],rgb[alpha>0])
    # explicit ORA top-to-bottom, no semantic underpaint
    ora=out/'ora'/'CP373_FRONT_19_SOURCE_REGION_GUIDES_NOT_RIG.ora'
    root=ET.Element('image',{'w':'217','h':'458','version':'0.0.3','name':'CP373 source guide, NOT production painted art'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for order in reversed(range(len(NAMES))):
            p='data/layer_%02d.png'%order
            b=io.BytesIO();srcLayers[order].save(b,format='PNG');z.writestr(p,b.getvalue())
            ET.SubElement(stack,'layer',{'name':'SOURCE_PIXELS__'+NAMES[order]+'__NOT_PAINTED',
                              'src':p,'visibility':'visible','opacity':'1.0','x':'0','y':'0',
                              'composite-op':'svg:src-over'})
        b=io.BytesIO();src.save(b,format='PNG');z.writestr('data/hidden_canon_front.png',b.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_EXACT_FRONT_REFERENCE_ONLY_HIDDEN',
                              'src':'data/hidden_canon_front.png','visibility':'hidden',
                              'opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf8',xml_declaration=True))
        b=io.BytesIO();rebuilt.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
    assert zipfile.ZipFile(ora).testzip() is None
    # Objective regression results: two blue toes still present
    toes={}
    ref=np.array(src)
    for key,(x1,y1,x2,y2) in TOES.items():
        m=blue_mask(ref[y1:y2,x1:x2]) & (ref[y1:y2,x1:x2,3]>=128)
        retained=m & (result[y1:y2,x1:x2,3]>=128) & blue_mask(result[y1:y2,x1:x2])
        toes[key]={'reference_blue_px':int(m.sum()),'retained_visible_blue_px':int(retained.sum()),'pass':bool(retained.sum()>=int(m.sum()*0.8))}
    # smoke motion: shift left hand -6,+3; no actual hidden shoulder drawn
    hand_mask=np.where(label==14,alpha,0).astype('uint8')
    moved=np.zeros_like(hand_mask);moved[3:,0:-6]=hand_mask[:-3,6:]
    uncovered=((hand_mask>128)&(moved<=128))
    if uncovered.sum()==0: raise AssertionError('Expected motion-seam diagnostic to detect missing underpaint')
    # image card using ONLY ACTUAL CANON and direct derivatives
    W,H=1580,950; sheet=Image.new('RGB',(W,H),'#102039');draw=ImageDraw.Draw(sheet)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    big=ImageFont.truetype(font,27);small=ImageFont.truetype(font,16);tiny=ImageFont.truetype(font,13)
    draw.text((30,18),'TVK CP373 | LAM THIEN | SOURCE-LOCKED FRONT FULL-BODY GUIDE',font=big,fill='#f6f8fc')
    draw.text((30,57),'Approved CANON V2.1 only | full body source-derived editability | NOT HIGH-RES ART / NOT RIG READY',font=small,fill='#b9d0e5')
    approved=canon.copy(); approved.thumbnail((420,798))
    sheet.paste(approved.convert('RGB'),(30,99))
    draw.text((30,902),'01  EXACT USER-APPROVED CANON',font=small,fill='#ffffff')
    frontZoom=src.resize((339,716),Image.Resampling.NEAREST).convert('RGB')
    sheet.paste(frontZoom,(490,134));draw.text((490,902),'02  FRONT EXACT SOURCE CROP',font=small,fill='#ffffff')
    # transparent matte on dark non-black surface
    matteImg=rebuilt.resize((339,716),Image.Resampling.NEAREST)
    bg=Image.new('RGBA',(339,716),'#25415b'); bg.alpha_composite(matteImg)
    sheet.paste(bg.convert('RGB'),(858,134))
    draw.text((858,902),'03  ALPHA MATTE: QA DRAFT',font=small,fill='#ffffff')
    color=np.zeros((458,217,3),dtype=np.uint8)
    from PIL import ImageColor
    for i,c in enumerate(COLORS,1):color[label==i]=ImageColor.getrgb(c)
    color[alpha==0]=[23,39,57]
    lab=Image.fromarray(color).resize((339,716),Image.Resampling.NEAREST)
    sheet.paste(lab,(1220,134))
    draw.text((1220,902),'04  19 COARSE SOURCE REGIONS',font=small,fill='#ffffff')
    draw.text((490,102),'Origin: 217x458 pixels | not a 4K master; the 19 partitions lack hidden anatomy.',font=tiny,fill='#f4c79b')
    preview=out/'qa'/'CP373_CANON_FRONT_MATTE_19REGION_COMPARISON.png';sheet.save(preview)
    # checkerboard transparency review for alpha artifact detection
    cb=Image.new('RGBA',FRONT_SIZE,'#dae1e8');d=ImageDraw.Draw(cb)
    for yy in range(0,458,16):
        for xx in range(0,217,16):
            if ((xx//16+yy//16)%2)==0:d.rectangle((xx,yy,xx+15,yy+15),fill='#aab8c7')
    cb.alpha_composite(rebuilt);cb.resize((651,1374),Image.Resampling.NEAREST).convert('RGB').save(out/'qa'/'CP373_FRONT_ALPHA_CHECKER_QA_NOT_READY.png')
    report={
      'checkpoint':'CP373','source_sha256':SHA,'canon_dimensions':list(SIZE),
      'front_crop_bbox':list(BBOX),'front_native_pixels':list(FRONT_SIZE),
      'source_reference_only':True,'foreground_opaque_pixels':int((alpha>=128).sum()),
      'reference_source_rgb_exact_where_visible':True,'static_ora_recompose_exact':True,
      'source_region_layers':len(NAMES),'ora_layers_including_hidden_guide':len(NAMES)+1,
      'toe_blue_color_checks':toes,'technical_motion_missing_underpaint_px':int(uncovered.sum()),
      'original_grabcut_foreground_count':int(raw_grab.sum()),
      'extra_blue_edge_detection_count':int(extra.sum()),
      'visual_qa':'NOT_PASSED','art_quality':'LOW_RES_FROM_INFOGRAPHIC',
      'native_painted_full_body':False,'true_semantic_occluded_layers':False,
      'alpha_manual_cleanup_required':True,'floor_shadow_contamination_possible':True,
      'rig_spine_ready':False,'apk_ready':False,'production_release':'blocked_pending_art','sprite_paths':{},
      'required_next':[
         'Manually clean outer silk and floor shadows in alpha matte',
         'Artist redraw full-body native high-resolution semantic parts independently from exact CANON',
         'Paint hidden anatomy under moving sleeves/cloth and repair layer transitions',
         'Paint correct left and right blue shoe tips',
         'Draw and QA real keyframes, expression states and damage overlays',
         'Obtain art approval before Spine/Android' ]}
    (out/'CP373_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (out/'SOURCE_ROLE_MANIFEST.json').write_text(json.dumps({
      'source_sha256':SHA,'note':'These are rough SOURCE PIXEL ROUTING masks, not rig geometry or new painting',
      'roles':[{'index':i,'filename':n+'.png','requires_manual_redraw':True} for i,n in enumerate(NAMES,1)]},ensure_ascii=False,indent=2)+'\n')
    (out/'README_CP373.md').write_text('''# CP373 — Lâm Thiển full-body exact-source **guide**, NOT production art\n\n'''
      'Source: CANON V2.1 941x1672 RGBA, exact SHA256 '+SHA+'\n\n'
      'Front source crop 217x458 is the **actual native detail level**. Do not call scaled previews high-resolution art.\n'
      '19 independently editable region/mask PNGs plus an ORA containing 19 source-pixel layers and one hidden approved reference.\n'
      'Rest composite exactly reconstructs this *experimental* alpha foreground; it does NOT reconstruct the white-background CANON source and is NOT a native redraw.\n'
      'Two blue shoe toes are QA-gated. Movement without newly painted hidden skin/cloth is explicitly flagged as failed.\n'
      'The transparency still needs manual cleanup (floor shadow / pale outer drapes). Art approval, rig, physics and APK remain blocked.\n'
      'Next: CP374 native independent painted head/torso/sleeves/legs/shoes with proper hidden underpaint, compared directly to CANON.\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(create(a.canon,a.out),ensure_ascii=False,indent=2))
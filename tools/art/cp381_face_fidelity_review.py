#!/usr/bin/env python3
"""CP381: immutable Lâm Thiển V2.1 CANON face/hair/bodice painting handoff.

Produces registered low-resolution reference crops and an editable, EMPTY painting
workspace. It does NOT generate painted high-resolution art or release assets.
"""
from __future__ import annotations
import argparse, hashlib, io, json, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from skimage.metrics import structural_similarity

SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
SOURCE_SIZE=(941,1672)
FRONT_BBOX=(13,172,230,630)
FRONT_SIZE=(217,458)
CANVAS=(1302,2748)
ZONES={
    '01_face_identity':(84,39,139,92),
    '02_hair_and_headpieces':(65,7,157,119),
    '03_bodice_neck_waist':(67,90,153,204),
}
# Larger, exact-pixel reference areas already present INSIDE the approved CANON sheet.
# They must not be mistaken for separately approved/new painted art.
EXPRESSION_REFS={
    '01_shy_Ngai_ngung':(22,681,196,884),
    '02_angry_Tuc_gian':(203,681,377,884),
    '03_pain_Dau_don':(382,681,556,884),
    '04_embarrassed_Xau_ho':(561,681,737,884),
    '05_charming_Quyen_ru':(744,681,918,884),
}
ACCESSORY_REFS={
    '01_eye_detail':(22,1453,100,1516),
    '02_hair_flower':(103,1453,176,1609),
    '03_ear_earring':(177,1453,245,1609),
    '04_collar':(247,1453,314,1609),
    '05_bodice_jewel':(316,1453,381,1609),
    '06_back_bow':(382,1453,449,1609),
    '07_tassel':(450,1453,519,1609),
    '08_ornament':(520,1453,590,1609),
}
PAINT_LAYERS=['03_PAINT_bodice_waist_EMPTY','02_PAINT_hair_headpieces_EMPTY','01_PAINT_face_identity_EMPTY']

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def preflight(canon,draft):
    if sha(canon)!=SHA:raise ValueError('Wrong CANON V2.1 source SHA; refusing edits')
    with Image.open(canon) as im:
        if im.mode!='RGBA' or im.size!=SOURCE_SIZE:raise ValueError('CANON dimensions/mode not approved')
        front=im.crop(FRONT_BBOX).convert('RGBA')
    with Image.open(draft) as im:
        if im.mode!='RGBA' or im.size!=CANVAS:raise ValueError('CP380 draft dimensions/mode mismatch')
        block=im.copy()
    return front,block

def data_bytes(im):
    bio=io.BytesIO();im.save(bio,'PNG');return bio.getvalue()

def blank_alpha():return Image.new('RGBA',CANVAS,(0,0,0,0))

def boxguide(box, name):
    guide=Image.new('RGBA',CANVAS,(0,0,0,0));d=ImageDraw.Draw(guide)
    x1,y1,x2,y2=box;coords=(6*x1,6*y1,6*x2,6*y2)
    d.rectangle(coords,outline='#ffbc4c',width=7)
    d.rectangle((coords[0],coords[1],min(CANVAS[0],coords[0]+len(name)*11+24),coords[1]+28),fill='#142941')
    d.text((coords[0]+10,coords[1]+7),name,fill='#fff2da')
    return guide

def audit_zone(source, rendered, box):
    a=np.asarray(source.crop(box).convert('RGB'),dtype=np.float32)
    b=np.asarray(rendered.crop(box).convert('RGB'),dtype=np.float32)
    mae=float(np.abs(a-b).mean())
    # Structural comparison on an exact same-canvas coordinate system, *not* acceptance score.
    ssim=float(structural_similarity(a.astype('uint8'),b.astype('uint8'),channel_axis=2,data_range=255))
    return {'mean_absolute_rgb_error':round(mae,2),'structural_similarity_observation':round(ssim,4),
            'result':'MANUAL_REPAINT_REQUIRED',
            'caveat':'Source is a small image within a composition. Image similarity is diagnostic only, not a production-art grading threshold.'}

def pack_ora(source_up,draft,folder):
    ora=folder/'CP381_FACE_HAIR_BODICE_PAINTING_WORKSPACE_NOT_ART.ora'
    root=ET.Element('image',{'w':str(CANVAS[0]),'h':str(CANVAS[1]),'version':'0.0.3',
                             'name':'CP381 EMPTY PAINTING WORKSPACE - SOURCE CANON ONLY'})
    stack=ET.SubElement(root,'stack')
    top=[]
    for name in PAINT_LAYERS:top.append((name,blank_alpha(),'visible'))
    for name,zone in ZONES.items():top.append(('HIDDEN_ZONE__'+name,boxguide(zone,name),'hidden'))
    top.append(('HIDDEN_CP380_UNAPPROVED_DRAFT',draft,'hidden'))
    top.append(('CANON_SOURCE_UPSCALED_REFERENCE_ONLY_NOT_HD',source_up,'visible'))
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for idx,(name,img,visibility) in enumerate(top):
            src=f'data/layer_{idx:02d}.png'
            z.writestr(src,data_bytes(img))
            ET.SubElement(stack,'layer',{'name':name,'src':src,'visibility':visibility,
                'opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',data_bytes(source_up))
    assert zipfile.ZipFile(ora).testzip() is None
    return ora

def make_board(canon,front,draft,metrics,out):
    W,H=2000,1330
    board=Image.new('RGB',(W,H),'#15283d');draw=ImageDraw.Draw(board)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    title=ImageFont.truetype(font,31);heading=ImageFont.truetype(font,21);small=ImageFont.truetype(font,17)
    draw.text((32,23),'CP381  |  LAM THIEN CANON V2.1 — IDENTITY FIDELITY REVIEW',font=title,fill='white')
    draw.text((32,69),'Approved CANON is authoritative • CP380 is UNAPPROVED • painting workspace has EMPTY art layers',font=small,fill='#c3d5e7')
    full=canon.copy();full.thumbnail((445,1110));board.paste(full.convert('RGB'),(28,133))
    draw.text((35,1254),'APPROVED CANON — exact full sheet',font=small,fill='white')
    fg=Image.alpha_composite(Image.new('RGBA',CANVAS,'#e9eef6'),draft)
    # crop from original at true native pixels; draft downsampled once for same coordinate crop
    ds=fg.resize(FRONT_SIZE,Image.Resampling.LANCZOS)
    xsrc=510
    for index,(name,box) in enumerate(ZONES.items()):
        y=135+index*371
        small_a=front.crop(box)
        small_b=ds.crop(box)
        avail_w=410;avail_h=275
        scale=min(avail_w/small_a.width, avail_h/small_a.height)
        w,h=int(small_a.width*scale),int(small_a.height*scale)
        a=small_a.resize((w,h),Image.Resampling.NEAREST)
        b=small_b.resize((w,h),Image.Resampling.LANCZOS)
        board.paste(a.convert('RGB'),(xsrc,y+50))
        board.paste(b.convert('RGB'),(xsrc+485,y+50))
        draw.text((xsrc,y+10),name.upper().replace('_',' '),font=heading,fill='#f8e5ba')
        draw.text((xsrc,y+340),'SOURCE CANON CROP (pixel enlargement)',font=small,fill='#e2f0fd')
        draw.text((xsrc+485,y+340),'CP380 DRAFT (unapproved)',font=small,fill='#e2f0fd')
        score=metrics[name]
        draw.text((xsrc+975,y+98),f'RGB difference: {score["mean_absolute_rgb_error"]:.2f}',font=small,fill='#ffe2bd')
        draw.text((xsrc+975,y+132),f'Structure: {score["structural_similarity_observation"]:.3f}',font=small,fill='#ffe2bd')
        draw.text((xsrc+975,y+176),'REPAINT',font=heading,fill='#ffb6ae')
        draw.text((xsrc+975,y+209),'NOT ART-READY',font=small,fill='#ffb6ae')
    board.save(out)

def exact_sheet_detail_references(canon,folder,qa):
    # All crops use original full-sheet pixels and are never resampled/AI-generated.
    expressions=folder/'expression_refs';accessories=folder/'accessory_refs'
    for sub in (expressions,accessories):sub.mkdir(exist_ok=True)
    for name,box in EXPRESSION_REFS.items():canon.crop(box).save(expressions/(name+'.png'))
    for name,box in ACCESSORY_REFS.items():canon.crop(box).save(accessories/(name+'.png'))
    W,H=1960,860;board=Image.new('RGB',(W,H),'#14283e');d=ImageDraw.Draw(board)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    title=ImageFont.truetype(font,29);body=ImageFont.truetype(font,17);sub=ImageFont.truetype(font,15)
    d.text((30,20),'CP381  |  FIVE CANON EXPRESSIONS + EXACT ACCESSORY REFERENCES',font=title,fill='#f1f5fe')
    d.text((30,60),'These are crops from the same user-approved sheet, NOT unrelated characters or newly painted art.',font=body,fill='#c5d8e6')
    for i,(name,box) in enumerate(EXPRESSION_REFS.items()):
        crop=canon.crop(box);x=24+i*386;y=118
        crop=crop.resize((348,406),Image.Resampling.NEAREST)
        board.paste(crop.convert('RGB'),(x,y))
        d.text((x,y+415),name.replace('_',' '),font=sub,fill='#f6e5c6')
    d.text((26,584),'APPROVED ACCESSORY DETAIL — pixel-exact crops; source dimensions preserved',font=body,fill='#e4ebf7')
    for i,(name,box) in enumerate(ACCESSORY_REFS.items()):
        crop=canon.crop(box);x=25+i*238;y=622
        thumb=crop.copy();thumb.thumbnail((168,176))
        board.paste(thumb.convert('RGB'),(x,y))
        d.text((x,y+183),name.replace('_',' '),font=sub,fill='#f0d8ae')
    d.text((26,835),'Do not promote any CP380/CP381 draft into the game without user/artist visual acceptance.',font=sub,fill='#ffd3bd')
    board.save(qa/'CP381_EXACT_CANON_EXPRESSION_AND_ACCESSORY_REFERENCES.png')

def generate(canon_path,draft_path,out):
    # Check source hashes before writing any outputs.
    front,draft=preflight(canon_path,draft_path)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    src=out/'source';ref=out/'reference_crops';qa=out/'qa';ora=out/'ora'
    for d in [src,ref,qa,ora]:d.mkdir(exist_ok=True)
    src_file=src/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
    src_file.write_bytes(Path(canon_path).read_bytes())
    assert sha(src_file)==SHA
    front.save(src/'FRONT_NATIVE_217x458_SOURCE_WITH_BACKGROUND.png')
    nearest=front.resize(CANVAS,Image.Resampling.NEAREST)
    nearest.save(src/'FRONT_UPSCALED_REFERENCE_ONLY_NOT_NEW_DETAIL.png')
    draft_preview=Image.alpha_composite(Image.new('RGBA',CANVAS,'#e9eef6'),draft)
    draft_small=draft_preview.resize(FRONT_SIZE,Image.Resampling.LANCZOS)
    metrics={}
    for name,box in ZONES.items():
        front.crop(box).save(ref/f'{name}_CANON_NATIVE_CROP.png')
        draft_small.crop(box).save(ref/f'{name}_CP380_DRAFT_CROP.png')
        metrics[name]=audit_zone(front,draft_small,box)
    ora_path=pack_ora(nearest,draft,ora)
    from PIL import ImageChops
    with zipfile.ZipFile(ora_path) as z:
        merged=Image.open(io.BytesIO(z.read('mergedimage.png')))
        assert ImageChops.difference(merged,nearest).getbbox() is None
    with Image.open(canon_path) as orig:
        make_board(orig,front,draft,metrics,qa/'CP381_CANON_FACE_HAIR_BODICE_REVIEW.png')
        exact_sheet_detail_references(orig,ref,qa)
    report={
      'checkpoint':'CP381','canon_sha256':SHA,'canon_bytes_preserved':sha(src_file)==SHA,
      'source_front_native_resolution':list(FRONT_SIZE),'working_canvas_resolution':list(CANVAS),
      'reference_workflow':'Non-HD nearest pixel enlargement for annotation only',
      'regions':{k:{'bbox_source_front':list(v),**metrics[k]} for k,v in ZONES.items()},
      'total_ora_layers':8,'canon_expression_reference_crops':len(EXPRESSION_REFS),
      'canon_accessory_reference_crops':len(ACCESSORY_REFS),'blank_editable_paint_layers':3,'hidden_review_layers':4,'visible_reference_layers':1,
      'painting_layers_have_artist_pixels':False,'native_fullbody_painting_complete':False,
      'visual_qa':'NOT_PASSED','production_release':'blocked_pending_art','sprite_paths':{},
      'rig_ready':False,'apk_ready':False,
      'next_step':'Artist redraw face identity FIRST, then hair/ornaments and bodice, with preview and approval before replacing CP380 assets.'
    }
    (out/'CP381_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--canon',required=True);a.add_argument('--draft',required=True);a.add_argument('--out',required=True)
    v=a.parse_args();print(json.dumps(generate(v.canon,v.draft,v.out),ensure_ascii=False,indent=2))
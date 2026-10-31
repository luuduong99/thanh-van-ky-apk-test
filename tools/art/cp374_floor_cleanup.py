#!/usr/bin/env python3
"""CP374 conservative floor-cast removal from CP373 full-body *source-pixel guide*.

This only changes candidate alpha below shoes; RGB and original CANON are immutable.
The resulting image is NOT approved character art, native HD, riggable or game-ready.
"""
from pathlib import Path
import argparse, io, json, hashlib, zipfile, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
SIZE=(941,1672); BBOX=(13,172,230,630); FRONT=(217,458)
TOES={'left':(79,432,102,458),'right':(109,414,122,446)}

def read_canon(path):
    path=Path(path)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=SHA:
        raise ValueError('CANON_V2_1_SHA_MISMATCH: no output allowed')
    img=Image.open(path)
    if img.size!=SIZE or img.mode!='RGBA':raise ValueError('CANON size/mode mismatch')
    return img

def check_source_and_parts(canon,cp373):
    cp373=Path(cp373)
    crop=np.asarray(canon.crop(BBOX).convert('RGBA'))
    source=np.asarray(Image.open(cp373/'source'/'FRONT_EXACT_CROP_WITH_BACKGROUND.png').convert('RGBA'))
    if not np.array_equal(crop,source):raise ValueError('CP373 crop is not exact canon')
    matte=np.asarray(Image.open(cp373/'source'/'FRONT_MATTE_DRAFT_NOT_ART.png').convert('RGBA'))
    if matte.shape!=source.shape or not np.array_equal(matte[:,:,:3],source[:,:,:3]):
        raise ValueError('CP373 source RGB differs from CANON')
    names=[p.stem.replace('_mask','') for p in sorted((cp373/'masks').glob('*_mask.png'))]
    if len(names)!=19:raise ValueError('Expected 19 source-region masks')
    ms=[np.asarray(Image.open(cp373/'masks'/f'{n}_mask.png').convert('L')) for n in names]
    if not np.array_equal(np.maximum.reduce(ms),matte[:,:,3]):raise ValueError('Partition alpha mismatch')
    if not np.all(np.sum(np.array(ms)>0,axis=0)[matte[:,:,3]>0]==1):
        raise ValueError('Source masks overlap')
    return source,matte,names,ms

def blue_mask(rgba):
    pix=rgba[:,:,:3].astype(np.float32)
    return (pix[:,:,2]>pix[:,:,0]*1.14)&(pix[:,:,2]>pix[:,:,1]*1.09)&(pix[:,:,2]>90)

def candidate_floor(rgba):
    # Narrow, reversible candidate. Do not pretend a photometric mask is a manual silhouette.
    pix=rgba.astype(np.int16);r,g,b=[pix[:,:,i] for i in range(3)]
    yy,xx=np.mgrid[:FRONT[1],:FRONT[0]]
    greyblue=(r>=160)&(r<=250)&((g-r)>=5)&((g-r)<=27)&((b-g)>=8)&((b-g)<=31)&((b-r)>=19)&((b-r)<=55)
    zone=(yy>=431)&(yy<=451)&(xx>=37)&(xx<=164)
    safety=(xx>=76)&(xx<=126)&(yy>=410)
    return greyblue & zone & ~safety & (pix[:,:,3]>=128)

def toe_report(ref,matt):
    report={}
    for key,(x1,y1,x2,y2) in TOES.items():
        base=ref[y1:y2,x1:x2];after=matt[y1:y2,x1:x2]
        bm=blue_mask(base)&(base[:,:,3]>=128)
        good=bm & (after[:,:,3]>=128) & blue_mask(after)
        report[key]={'reference_blue_px':int(bm.sum()),'preserved_blue_px':int(good.sum()),'pass':bool(bm.sum()>=20 and good.sum()==bm.sum())}
    return report

def checker(im,scale=3):
    w,h=im.size;back=Image.new('RGBA',(w,h),'#dfe8f0');d=ImageDraw.Draw(back)
    for y in range(0,h,12):
        for x in range(0,w,12):
            if ((x//12+y//12)%2)==0:d.rectangle((x,y,x+11,y+11),fill='#b8c8d8')
    back.alpha_composite(im)
    return back.convert('RGB').resize((w*scale,h*scale),Image.Resampling.NEAREST)

def make(canon_path,cp373,out):
    # No side effects until source is verified.
    canon=read_canon(canon_path)
    source,old,names,source_masks=check_source_and_parts(canon,cp373)
    floor=candidate_floor(old)
    if floor.sum()<200:raise ValueError('Floor candidate absent; inspect provenance before changing alpha')
    new=old.copy();new[floor,3]=0
    assert np.array_equal(new[:,:,:3],source[:,:,:3]);assert np.array_equal(old[:431,:,3],new[:431,:,3])
    assert np.array_equal(old[410:458,76:127,3],new[410:458,76:127,3])
    toes=toe_report(source,new)
    if not all(v['pass'] for v in toes.values()):raise AssertionError('Blue shoe-tip regression')
    out=Path(out)
    for sub in ['source','masks','layers','ora','qa']:(out/sub).mkdir(parents=True,exist_ok=True)
    src=Image.fromarray(source,'RGBA');before=Image.fromarray(old,'RGBA');after=Image.fromarray(new,'RGBA')
    src.save(out/'source'/'FRONT_EXACT_CANON_CROP.png')
    before.save(out/'source'/'CP373_BEFORE_TRANSPARENT_SOURCE_MATTE.png')
    after.save(out/'source'/'CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png')
    Image.fromarray((floor.astype(np.uint8)*255),'L').save(out/'masks'/'CP374_REMOVED_FLOOR_CANDIDATES.png')
    Image.fromarray(new[:,:,3],'L').save(out/'masks'/'CP374_EDITABLE_FOREGROUND_ALPHA.png')
    slices=[]
    for i,(name,m) in enumerate(zip(names,source_masks)):
        mask=m.copy(); mask[floor]=0
        Image.fromarray(mask,'L').save(out/'masks'/f'{name}_mask.png')
        part=Image.fromarray(np.dstack([source[:,:,:3],mask]),'RGBA')
        part.save(out/'layers'/f'{name}.png');slices.append(part)
    rebuilt=Image.new('RGBA',FRONT,(0,0,0,0))
    for im in slices:rebuilt.alpha_composite(im)
    actual=np.asarray(rebuilt)
    assert np.array_equal(actual[:,:,3],new[:,:,3]);assert np.array_equal(actual[new[:,:,3]>0,:3],new[new[:,:,3]>0,:3])
    hidden_review=old.copy();hidden_review[:,:,3]=np.where(floor,old[:,:,3],0)
    ora=out/'ora'/'CP374_FRONT_19_REVISED_SOURCE_MASKS_NOT_RIG.ora'
    root=ET.Element('image',{'w':'217','h':'458','name':'CP374 partial floor cleanup, NOT production art','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i in reversed(range(19)):
            p=f'data/visible_{i:02}.png';b=io.BytesIO();slices[i].save(b,format='PNG');z.writestr(p,b.getvalue())
            ET.SubElement(stack,'layer',{'name':f'SOURCE_PART__{names[i]}__NOT_PAINTED','src':p,'visibility':'visible','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        for name,im in [('REMOVED_FLOOR_CANDIDATE_REVIEW_ONLY',Image.fromarray(hidden_review,'RGBA')),('CANON_EXACT_FRONT_REFERENCE_ONLY',src)]:
            p=f'data/{name}.png';b=io.BytesIO();im.save(b,format='PNG');z.writestr(p,b.getvalue())
            ET.SubElement(stack,'layer',{'name':name+'__HIDDEN','src':p,'visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf8',xml_declaration=True))
        buf=io.BytesIO();rebuilt.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
    assert zipfile.ZipFile(ora).testzip() is None
    # CANON-only review. This includes current same-character crop and experimental source-matte derivatives.
    canvas=Image.new('RGB',(1550,1000),'#122338');d=ImageDraw.Draw(canvas)
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    ft=ImageFont.truetype(fontpath,20);title=ImageFont.truetype(fontpath,25);minor=ImageFont.truetype(fontpath,14)
    d.text((24,18),'TVK CP374 | LAM THIEN | CANON V2.1 ONLY',font=title,fill='#f5f8ff')
    d.text((24,53),'Selective floor candidate cleanup - UNAPPROVED TECHNICAL MATTE / NOT ART / NOT RIG',font=minor,fill='#f0ba9c')
    canon_img=canon.copy();canon_img.thumbnail((412,805))
    canvas.paste(canon_img.convert('RGB'),(15,90));d.text((18,918),'01  APPROVED FULL CANON',font=ft,fill='white')
    bef=checker(before,2).resize((400,844))
    aft=checker(after,2).resize((400,844))
    canvas.paste(bef,(440,85));canvas.paste(aft,(870,85))
    d.text((440,940),'02  CP373 BEFORE (DRAFT)',font=ft,fill='white')
    d.text((870,940),'03  CP374 AFTER (DRAFT)',font=ft,fill='white')
    cut=np.zeros_like(old);cut[:,:,:3]=[255,72,157];cut[:,:,3]=np.where(floor,210,0)
    overlay=Image.alpha_composite(after,Image.fromarray(cut,'RGBA'))
    canvas.paste(checker(overlay,1).resize((238,520)),(1305,235))
    d.text((1300,780),'04  REMOVED PX',font=minor,fill='white')
    d.text((1300,807),f'{int(floor.sum())} candidates',font=minor,fill='#f6c4d2')
    d.text((1300,848),'Floor still partly',font=minor,fill='#f5d0b9')
    d.text((1300,869),'present; inspect',font=minor,fill='#f5d0b9')
    d.text((1300,891),'silk edges',font=minor,fill='#f5d0b9')
    canvas.save(out/'qa'/'CP374_CANON_FLOOR_BEFORE_AFTER_NOT_APPROVED.png')
    # Failure-gated handoff; source roles remain coarse. The 204px CP373 motion gap is unresolved.
    rep={'checkpoint':'CP374','source_sha256':SHA,'front_source_px':list(FRONT),
      'floor_candidate_alpha_removed_px':int(floor.sum()),'before_nonzero_alpha_px':int((old[:,:,3]>0).sum()),
      'after_nonzero_alpha_px':int((new[:,:,3]>0).sum()),'source_rgb_exact':True,
      'upper_431_rows_alpha_unchanged':True,'protected_foot_band_alpha_unchanged':True,
      'blue_shoe_tip_checks':toes,'visible_regions':19,'hidden_review_layers':2,
      'ora_layer_count':21,'ora_recomposes_alpha_exact':True,
      'manual_floor_cleanup_still_needed':True,'pale_silk_halo_repaint_needed':True,
      'underpaint_missing_motion_gap_cp373_px':204,'full_motion_gap_free':False,
      'native_painted_hd_fullbody':False,'true_semantic_layers_painted':False,
      'spine_ready':False,'apk_ready':False,'visual_qa':'NOT_PASSED',
      'production_release':'blocked_pending_art','sprite_paths':{},
      'warning':'Color and region heuristic removes some floor; can remove near-color fabric. Needs human QA, not production.',
      'next':'CP375: native hand-painted full-body art and actual hidden anatomy; do not treat masks as painted sprites.'}
    (out/'CP374_REPORT.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return rep

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--canon',required=True);ap.add_argument('--cp373',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args();print(json.dumps(make(a.canon,a.cp373,a.out),ensure_ascii=False,indent=2))
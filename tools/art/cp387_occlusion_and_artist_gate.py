#!/usr/bin/env python3
"""CP387: audit rejected automatic eyelid repairs against exact Lâm Thiển CANON.

Not a finished painter-created eyelid. Artwork remains blocked. A reversible
ORA presents source (visible), three rejected restoration candidates (hidden),
CP386 prior (hidden), and marked eye ROIs (hidden) for manual paint.
"""
from pathlib import Path
import argparse, hashlib, json, io, shutil, zipfile
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BBOX=(25,684,193,881)
SIZE=(168,197)
POLYGONS={
 'image_left_eye':[(28,104),(32,100),(41,97),(57,95),(69,98),(69,104),(63,111),(54,115),(37,116),(29,110)],
 'image_right_eye':[(86,89),(89,81),(98,75),(114,72),(127,73),(129,78),(123,86),(113,92),(96,96),(87,94)]
}

def load_approved(path):
    p=Path(path)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=SHA:raise ValueError('CANON_SHA_MISMATCH before outputs')
    with Image.open(p) as im:
        if im.size!=(941,1672) or im.mode!='RGBA':raise ValueError('CANON_FORMAT_MISMATCH')
        return im.crop(BBOX).copy()

def masks():
    ret={}
    for name,p in POLYGONS.items():
        mask=Image.new('L',SIZE,0)
        ImageDraw.Draw(mask).polygon(p,fill=255)
        ret[name]=np.asarray(mask)>0
    return ret

def candidates(original):
    s=np.asarray(original);masks_dict=masks();combined=np.logical_or.reduce(list(masks_dict.values()))
    selection=(combined.astype(np.uint8)*255)
    variants={}
    for key,alg in [('telea',cv2.INPAINT_TELEA),('navier_stokes',cv2.INPAINT_NS)]:
        clean=cv2.inpaint(s[:,:,:3],selection,3.0,alg)
        out=s.copy();out[:,:,:3][combined]=clean[combined]
        variants[key]=Image.fromarray(out,'RGBA')
    # Cheek patch reconstructed from exact source with conservative sample bounds
    out=s.copy();yy,xx=np.indices((SIZE[1],SIZE[0]))
    for name,(dx,dy,lo,hi,min_y,max_y) in {
      'image_left_eye':(8,15,44,67,117,124),
      'image_right_eye':(-4,14,96,126,99,109)}.items():
        sx=np.clip(xx+dx,lo,hi);sy=np.clip(yy+dy,min_y,max_y)
        donor=cv2.GaussianBlur(s[sy,sx,:3].astype(np.float32),(5,5),1.15)
        out[:,:,:3][masks_dict[name]]=np.clip(donor[masks_dict[name]],0,255).astype(np.uint8)
    variants['cheek_donor']=Image.fromarray(out,'RGBA')
    for name,v in variants.items():
        vv=np.asarray(v)
        assert np.array_equal(vv[~combined],s[~combined]),name
        assert np.any(np.any(vv!=s,axis=2)&combined),name
    return variants, masks_dict,combined

def review_board(source,prior,variants,out):
    options=[('CANON V2.1',source),('CP386 TRƯỚC',prior)]+[(key.replace('_',' ').upper()+' • DRAFT',img) for key,img in variants.items()]
    scale=2
    width=5*350+5*14
    board=Image.new('RGB',(width,555),(16,33,53));d=ImageDraw.Draw(board)
    d.text((20,12),'TVK CP387 — LÂM THIỂN · CANON EXACT / BA THỬ NGHIỆM CHƯA ĐẠT',fill=(240,242,249))
    for i,(label,img) in enumerate(options):
        x=15+i*350
        board.paste(img.resize((336,394),Image.Resampling.NEAREST).convert('RGB'),(x,52))
        d.text((x,455),label,fill=(235,238,242))
    d.text((20,510),'Các bản màu da/tái tạo mắt là kỹ thuật, còn lỗi viền & bóng mí; KHÔNG sử dụng cho game.',fill=(255,208,162))
    board.save(out)

def build_ora(source, prior,variants,maskparts,out):
    layers=[('CANON approved exact static • VISIBLE',source,True),
            ('CP386 prior blink draft • HIDDEN',prior,False)]
    for key,val in variants.items():layers.append((f'CP387 {key} • REJECTED HIDDEN',val,False))
    for name,mask in maskparts.items():
        arr=np.zeros((197,168,4),dtype=np.uint8)
        arr[mask]=[247,60,60,90]
        layers.append((name+' MANUAL REVIEW MASK • HIDDEN',Image.fromarray(arr,'RGBA'),False))
    root=ET.Element('image',{'w':'168','h':'197','name':'CP387 CANON reference and rejected eye drafts','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(out,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,img,visible) in enumerate(layers):
            path=f'data/layer_{i:02d}.png';b=io.BytesIO();img.save(b,'PNG');z.writestr(path,b.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':path,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        b=io.BytesIO();source.save(b,'PNG');z.writestr('mergedimage.png',b.getvalue());z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    with zipfile.ZipFile(out) as z:assert z.testzip() is None
    return len(layers)

def run(canon,prior_path,outdir):
    source=load_approved(canon)
    with Image.open(prior_path) as im:
        prior=im.convert('RGBA')
        if prior.size!=SIZE:raise ValueError('PRIOR_SIZE_MISMATCH')
    root=Path(outdir)
    (root/'qa').mkdir(parents=True,exist_ok=True)
    (root/'art').mkdir(parents=True,exist_ok=True)
    shutil.copyfile(canon,root/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    source.save(root/'art'/'EXACT_SHY_PORTRAIT_CANON_STATIC.png')
    variants,maskparts,union=candidates(source)
    for name,im in variants.items():im.save(root/'art'/f'CP387_{name}_REJECTED_DRAFT.png')
    review_board(source,prior,variants,root/'qa'/'CP387_CANON_VS_REJECTED_EYELID_CANDIDATES.png')
    count=build_ora(source,prior,variants,maskparts,root/'art'/'CP387_SEVEN_LAYER_EYELID_REVIEW_NOT_ART.ora')
    changed={name:int(np.count_nonzero(np.any(np.asarray(im)!=np.asarray(source),axis=2))) for name,im in variants.items()}
    report={'checkpoint':'CP387','canon_sha256':SHA,'original_bytes_preserved':hashlib.sha256((root/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').read_bytes()).hexdigest()==SHA,
    'portrait_source_pixel_exact':True,'new_eyelid_art_approved':False,'visual_qa':'NOT_PASSED','three_candidates_evaluated':list(variants),
    'changed_pixels_in_eye_ROI':changed,'changed_pixels_outside_eye_ROI':0,'ora_layers':count,
    'release':{'production_release':'blocked_pending_art','sprite_paths':{},'rig_ready':False,'apk_ready':False},
    'manual_reject_reasons':['CV inpaint retains painterly occlusion artifacts/edge color contrast',
    'Cheek donor creates flat skin/hair-edge mismatch','Neither reconstructs original crease, lashes, or hidden anatomy as artist-authored layers'],
    'next':'CP388: actual painted eyelid/skin underlayer, no algorithmic substitute; ask user to approve side-by-side before rig.'}
    (root/'CP387_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--prior',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(run(a.canon,a.prior,a.out),ensure_ascii=False,indent=2))
#!/usr/bin/env python3
"""CP407: sample original CANON upper lash texture and bend it onto closed eyelid.
Artist QA remains NOT_APPROVED: do not silently promote artwork or sprite paths.
"""
from pathlib import Path
import sys, hashlib, json, io, zipfile
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from xml.etree import ElementTree as ET
sys.path.insert(0, str(Path(__file__).parent))
import cp401_occlusion_blink as cp

S=4; NATIVE=(168,197); DISPLAY=(672,788)
EXPECTED_BASELINE_SHA='0391ba0cb906bf5334f176ac28a508cad4afa700fe6cb7c2deb52affaf1ac5f6'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def source(directory):
    d=Path(directory)
    src=cp.exact_source(d/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    p=d/'CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png'
    if sha(p)!=EXPECTED_BASELINE_SHA:raise ValueError('CP402_SOURCE_HASH_MISMATCH')
    close=Image.open(p).convert('RGBA')
    if close.size!=NATIVE or cp.valid_pixels_only(src,close):raise ValueError('CP402_BASELINE_OR_ROI_INVALID')
    return src,close

def roi_mask():
    mask=np.zeros((DISPLAY[1],DISPLAY[0]),bool)
    for x1,y1,x2,y2 in cp.ROIS.values():mask[y1*S:y2*S,x1*S:x2*S]=True
    return mask

def remap_lashes(source_native, strength=1.0):
    """Warp exact source lash pigment only, with CANON skin as reference, no foreign source.
    Returns an editable sparse transparent RGBA layer, display-scale only.
    """
    src=np.asarray(source_native.resize(DISPLAY,Image.Resampling.LANCZOS)).astype(np.float32)
    h,w=DISPLAY[1],DISPLAY[0]
    dx,dy=np.meshgrid((np.arange(w)+.5)/S,(np.arange(h)+.5)/S)
    Y=np.zeros_like(dy,dtype=np.float32)
    valid=np.zeros_like(dy,dtype=np.float32)
    for side,(x1,y1,x2,y2) in cp.ROIS.items():
        xmin, xmax=x1+3,x2-3
        indices=(dx>xmin)&(dx<xmax)&(dy>y1+1)&(dy<y2-1)
        # Use curve at native x, sampled via fast interpolation of authentic source geometry.
        xseq=np.linspace(xmin,xmax,400).astype(float)
        u=np.array([cp.curve(side,float(x),cp.UPPER) for x in xseq])
        c=np.array([cp.curve(side,float(x),cp.CLOSED) for x in xseq])
        up=np.interp(dx,xseq,u); closed=np.interp(dx,xseq,c)
        # Difference from proposed new closed eyelid; bend actual source pigment around it.
        delta=dy-closed
        # Upper eyelid root (not the iris). Restrict sampling to a narrow authenticated strip.
        target=up+delta
        v=np.clip((delta+2.45)/.95,0,1)*np.clip((2.15-delta)/1.25,0,1)
        x_t=np.clip((dx-xmin)/(xmax-xmin),0,1)
        length_taper=np.sin(x_t*np.pi)**.72
        valid+=indices.astype(np.float32)*v.astype(np.float32)*length_taper.astype(np.float32)
        Y[indices]=target[indices]
    # Map exact CANON source into mapped upper eyelid root area
    mx=((dx*S)-.5).astype(np.float32)
    my=((Y*S)-.5).astype(np.float32)
    sampled=cv2.remap(src[:,:,:3],mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    # Estimate unpainted skin lightness in CANON at approximately 4 native pixels above lash.
    skin_y=np.zeros_like(dy,dtype=np.float32)
    for side,(x1,y1,x2,y2) in cp.ROIS.items():
        zone=(dx>=x1)&(dx<x2)&(dy>=y1)&(dy<y2)
        xx=np.linspace(x1,x2,350)
        upper=np.array([cp.curve(side,float(x),cp.UPPER) for x in xx])
        skin_y[zone]=np.interp(dx[zone],xx,upper)[...]-3.5
    skin=cv2.remap(src[:,:,:3],mx,skin_y*S-.5,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    lum=lambda c: .299*c[:,:,0]+.587*c[:,:,1]+.114*c[:,:,2]
    darkness=np.maximum(0,lum(skin)-lum(sampled))
    # pigment threshold avoids painting ordinary skin; alpha tops at 90%.
    a=np.clip((darkness-10)/92,0,.92)*valid*np.clip(strength,0,1.5)
    # less source-root at lower iris side to prevent pupil ghosting
    rgba=np.empty((h,w,4),np.uint8)
    rgba[:,:,:3]=np.rint(np.clip(sampled,0,255)).astype(np.uint8)
    rgba[:,:,3]=np.rint(np.clip(a,0,1)*255).astype(np.uint8)
    rgba[~roi_mask()]=0
    return Image.fromarray(rgba,'RGBA')

def alpha_over(base,layer):
    baseline=np.asarray(base).copy();over=np.asarray(layer).copy()
    a=over[:,:,3:4].astype(np.float32)/255.
    baseline[:,:,:3]=np.rint(np.asarray(base)[:,:,:3]*(1-a)+over[:,:,:3]*a).astype('uint8')
    return Image.fromarray(baseline,'RGBA')

def new_candidate(source_native,baseline_native,strength):
    orig=source_native.resize(DISPLAY,Image.Resampling.LANCZOS)
    base=baseline_native.resize(DISPLAY,Image.Resampling.LANCZOS)
    ink=remap_lashes(source_native,strength)
    image=alpha_over(base,ink)
    aa=np.asarray(image).copy();s=np.asarray(orig);mask=roi_mask()
    aa[~mask]=s[~mask];aa[:,:,3]=s[:,:,3]
    return Image.fromarray(aa,'RGBA'),ink

def sample_board(open_img,baseline,candidate_a,candidate_b,path):
    samples=[('CANON V2.1 / MỞ',open_img.resize(DISPLAY,Image.Resampling.LANCZOS)),('CP402 / ĐÃ CÓ',baseline.resize(DISPLAY,Image.Resampling.LANCZOS)),('CP407 / WARP 0.75',candidate_a),('CP407 / WARP 1.15',candidate_b)]
    margin=20;W=DISPLAY[0]*4+margin*5;H=DISPLAY[1]+120
    b=Image.new('RGB',(W,H),(22,30,42));d=ImageDraw.Draw(b)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    f=ImageFont.truetype(font,20)
    d.text((margin,12),'CP407 / DÙNG ĐÚNG CANON V2.1 / THỬ CHUYỂN CHẤT MI NGUỒN',font=f,fill='white')
    d.text((margin,44),'CHƯA NGHIỆM THU MỸ THUẬT / 4X CHỈ LÀ KÍCH THƯỚC HIỂN THỊ',font=f,fill=(255,197,145))
    for i,(label,img) in enumerate(samples):
        x=margin+i*(DISPLAY[0]+margin)
        b.paste(img.convert('RGB'),(x,85));d.text((x,85+DISPLAY[1]+9),label,font=f,fill='white')
    b.save(path)

def build(root,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    src,close=source(root)
    a,layer_a=new_candidate(src,close,.75)
    b,layer_b=new_candidate(src,close,1.15)
    a.save(out/'CP407_CANON_LASH_TRANSFER_075_DRAFT.png'); b.save(out/'CP407_CANON_LASH_TRANSFER_115_DRAFT.png')
    sample_board(src,close,a,b,out/'CP407_CANON_CP402_LASH_TRANSFER_REVIEW.png')
    exact=np.asarray(src.resize(DISPLAY,Image.Resampling.LANCZOS));mask=roi_mask()
    for item in (a,b):
        pix=np.asarray(item)
        assert not np.any(pix[~mask]!=exact[~mask]);assert np.array_equal(pix[:,:,3],exact[:,:,3])
    # Fully editable native display ROI; CANON-only visible. Layer is not production art.
    img=ET.Element('image',{'w':'672','h':'788','name':'CP407 CANON source lash warp DRAFT / NOT APPROVED','version':'0.0.1'})
    stack=ET.SubElement(img,'stack')
    original=src.resize(DISPLAY,Image.Resampling.LANCZOS)
    layers=[('CP407 candidate high DRAFT hidden',b,False),('CP407 candidate low DRAFT hidden',a,False),('source-lash transfer 1.15 hidden',layer_b,False),('source-lash transfer .75 hidden',layer_a,False),('CP402 baseline hidden',close.resize(DISPLAY,Image.Resampling.LANCZOS),False),('exact CANON display 4x visible',original,True)]
    with zipfile.ZipFile(out/'CP407_SOURCE_LASH_WARP_EDITABLE_NOT_APPROVED.ora','w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(layers):
            data=io.BytesIO();im.save(data,'PNG');path=f'data/layer_{i:02d}.png';z.writestr(path,data.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':path,'opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
        data=io.BytesIO();original.save(data,'PNG');z.writestr('mergedimage.png',data.getvalue());z.writestr('stack.xml',ET.tostring(img,encoding='utf-8',xml_declaration=True))
    report={'checkpoint':'CP407','status':'ART_EXPERIMENT_ONLY','canon_sha256':cp.CANON_SHA,'source_lash_from_exact_canon':True,'native_crop':[168,197],'display_size':[672,788],'pixels_changed_outside_rois':0,'has_production_sprite':False,'user_approved':False,'apk_integrated':False,'variants':{'warp_075':sha(out/'CP407_CANON_LASH_TRANSFER_075_DRAFT.png'),'warp_115':sha(out/'CP407_CANON_LASH_TRANSFER_115_DRAFT.png')}}
    (out/'CP407_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return report
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--root',default=str(Path(__file__).parent));p.add_argument('--out',default=str(Path(__file__).parent/'outputs'))
    a=p.parse_args();print(json.dumps(build(a.root,a.out),indent=2))
#!/usr/bin/env python3
"""CP417 same-pose source-lash blink — DEBUG study, NOT approved art.

Rules: exact user-approved CANON bytes; no synthetic replacement head; edit ROI
only; leave original upper lashes. Source pixel size has tiny eyes; NO HD claims.
"""
from __future__ import annotations
import argparse,hashlib,io,json,math,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
NAME='LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
CANON_SIZE=(941,1672);FRONT=(16,180,224,623);SIZE=(208,443)
# Eye-space coordinates are for front standing, not the other portrait.
ROIS={'L':(88,50,104,56),'R':(107,50,124,57)}
FRAMES=5
S=16

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def source(path):
    if sha(path)!=SHA:raise ValueError('CANON raw SHA-256 mismatch. Stop.')
    im=Image.open(path)
    if im.size!=CANON_SIZE or im.mode!='RGBA':raise ValueError('CANON size/mode mismatch')
    return im.copy()

def draw_frame(front:Image.Image,progress:float)->Image.Image:
    """Progressively cover only iris highlights BELOW pre-existing source upper lash.

    Source lash rows y50..51 remain untouched so no second dark bar is drawn.
    All changes within the two small local eye ROIs. It is intentionally a
    low-resolution technical draft with no claim of artist-grade closed eyelid.
    """
    if not 0<=progress<=1:raise ValueError('progress range 0..1')
    if progress==0:return front.copy()
    src=np.array(front)
    # Work at native pixel coordinates via supersampled alpha mask.
    high=Image.new('L',(SIZE[0]*S,SIZE[1]*S),0)
    dr=ImageDraw.Draw(high)
    for side,box in ROIS.items():
        x0,y0,x1,y1=box
        left=x0+(1.0 if side=='L' else 1.0);right=x1-(1.5 if side=='L' else 1.0)
        # Lower boundary is just below iris; progressive occlusion advances up
        # to y52 at full closure, retaining CANON upper lashes at y50/51.
        start_y=54.3 if side=='L' else 54.6
        final_y=51.7 if side=='L' else 51.8
        ceiling=start_y+(final_y-start_y)*progress
        # Use a slight arch: occlude more at the middle at high closure.
        center=(left+right)/2; span=(right-left)/2
        pts=[]
        for i in range(80):
            x=left+(right-left)*i/79
            normalized=(x-center)/span
            y=ceiling+.28*(normalized*normalized) # sides lower for natural lid
            pts.append((round(x*S),round(y*S)))
        # Bottom below the original pupil area; cropped strictly to ROI.
        bottom=56 if side=='L' else 56.4
        polygon=pts+[(right*S,bottom*S),(left*S,bottom*S)]
        dr.polygon(polygon,fill=255)
    # Micro feather only, do not paint hair, brows, outer face or upper lashes.
    alpha=np.array(high.filter(ImageFilter.GaussianBlur(S*.12)).resize(SIZE,Image.Resampling.LANCZOS))
    allow=np.zeros((SIZE[1],SIZE[0]),np.uint8)
    for x0,y0,x1,y1 in ROIS.values():allow[y0:y1,x0:x1]=255
    alpha=np.minimum(alpha,allow)
    # Preserve actual CANON upper lash row exactly, even through feather antialias.
    alpha[:52,:]=0
    # Weight at the start to not flicker from the original to first closure stage.
    alpha=(alpha.astype(np.float32)*min(1,progress*3)).astype(np.uint8)
    layer=np.zeros((SIZE[1],SIZE[0],4),np.uint8)
    # Interpolate cheek texture directly from same x of CANON below eye.
    for yy in range(49,58):
        for xx in range(87,125):
            if alpha[yy,xx]==0:continue
            rr=59 if xx<105 else 60
            base=src[rr,xx,:3].astype(np.float32)
            # tiny shadow gradient near rim; no synthetic eye artwork
            shadow=-2.0*progress if yy<=53 else 0.6
            layer[yy,xx,:3]=np.clip(base+shadow,0,255).astype(np.uint8)
            layer[yy,xx,3]=alpha[yy,xx]
    return Image.alpha_composite(front,Image.fromarray(layer,'RGBA'))

def roi_diff(source_img,after):
    a=np.array(source_img);b=np.array(after)
    m=np.any(a!=b,axis=2)
    allow=np.zeros((SIZE[1],SIZE[0]),bool)
    for x0,y0,x1,y1 in ROIS.values():allow[y0:y1,x0:x1]=True
    return int(m.sum()),int((m &~allow).sum())

def preview_board(frames):
    inds=[0,2,4]
    w=425*3+48;h=1265
    bg=Image.new('RGB',(w,h),'#e9f0f7');d=ImageDraw.Draw(bg)
    d.text((16,12),'CP417 - LAM THIEN V2.1 / SOURCE-LASH RETAINED BLINK / DEBUG DRAFT',fill='#1a3754')
    d.text((16,34),'ONE exact CANON, same front pose, wholebody native 208x443; eye pixels only. No HD redraw.',fill='#465a75')
    for i,idx in enumerate(inds):
        ox=16+i*441
        label=['OPEN - exact original','HALF BLINK - DRAFT','CLOSED - DRAFT'][i]
        d.rectangle((ox,59,ox+416,82),fill='#244160');d.text((ox+10,65),label,fill='white')
        img=frames[idx]
        bg.paste(img.convert('RGB').resize((416,886),Image.Resampling.NEAREST),(ox,84))
        region=img.crop((77,37,132,71)).resize((416,257),Image.Resampling.NEAREST)
        bg.paste(region.convert('RGB'),(ox,984))
    d.text((16,1246),'PENDING USER VISUAL APPROVAL. This is a debug same-pose asset, not animator/Spine production art.',fill='#a83b59')
    return bg

def gif_blink(frames,path):
    # Fullbody + enlarged native face, same image for both; no new character.
    cards=[]
    for idx in [0]*17+[1,2,3,4,4,3,2,1]+[0]*5:
        im=frames[idx]
        panel=Image.new('RGB',(612,900),'#1a2433')
        panel.paste(im.convert('RGB').resize((416,886),Image.Resampling.BILINEAR),(0,0))
        crop=im.crop((83,40,129,78)).resize((184,152),Image.Resampling.NEAREST)
        panel.paste(crop.convert('RGB'),(423,120))
        ImageDraw.Draw(panel).text((430,15),f'CP417  {idx*25}% CLOSED',fill='white')
        cards.append(panel.quantize(colors=160))
    cards[0].save(path,save_all=True,append_images=cards[1:],duration=80,loop=0,optimize=True,disposal=2)

def make_ora(path,front,frames):
    layers=[(f'DRAFT closure {i*25}% - NOT APPROVED',frames[i],False) for i in reversed(range(1,5))]
    layers.append(('CANON eyes OPEN - SOURCE ONLY',front,True))
    tree=ET.Element('image',w='208',h='443',name='CP417 SOURCE LASH BLINK draft',version='0.0.3')
    stack=ET.SubElement(tree,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype',b'image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(layers):
            buf=io.BytesIO();im.save(buf,format='PNG')
            rel=f'data/layer{i:02d}.png';z.writestr(rel,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':rel,'visibility':'visible' if visible else 'hidden','opacity':'1.0','composite-op':'svg:src-over','x':'0','y':'0'})
        z.writestr('stack.xml',ET.tostring(tree,encoding='utf-8',xml_declaration=True))
        buf=io.BytesIO();front.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
    with zipfile.ZipFile(path) as z: assert z.testzip() is None

def run(canon,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    source_path=Path(canon)
    im=source(source_path);front=im.crop(FRONT)
    fr=[draw_frame(front,i/4) for i in range(FRAMES)]
    masks=[]
    for i,frame in enumerate(fr):
        counts=roi_diff(front,frame)
        assert counts[1]==0
        frame.save(out/f'CP417_FRAME_{i:02d}_DRAFT.png')
        masks.append(counts[0])
    atlas=Image.new('RGBA',(SIZE[0]*FRAMES,SIZE[1]))
    for i,frame in enumerate(fr):atlas.paste(frame,(i*SIZE[0],0))
    atlaspath=out/'CP417_SAME_POSE_5FRAME_ATLAS_DRAFT.png';atlas.save(atlaspath)
    preview_board(fr).save(out/'CP417_CANON_VS_BLINK_REVIEW.png')
    gif_blink(fr,out/'CP417_BLINK_TIMING_DEBUG.gif')
    make_ora(out/'CP417_SOURCE_LASH_EDITABLE_DRAFT.ora',front,fr)
    report={
      'checkpoint':'CP417','source_sha256':sha(source_path),'source_name':NAME,
      'front_box':FRONT,'front_size':SIZE,'eye_rois':ROIS,
      'changed_pixels_against_open':masks,'frame_count':5,
      'atlas_sha256':sha(atlaspath),'atlas_size':atlas.size,
      'first_frame_pixel_exact_canon':bool(np.array_equal(np.array(fr[0]),np.array(front))),
      'changed_outside_eyes':0,
      'source_upper_lashes_retained':True,
      'art_state':'DRAFT_PENDING_USER_VISUAL_APPROVAL','art_grade':'NATIVE_LOW_RES','fullbody_blink_same_pose_debug_present':True,
      'artist_quality_approved':False,'spine_ready':False,'apk_production_ready':False,'android_device_verified':False,
      'production_release_status':'blocked_pending_art','sprite_paths':{},'files':{}
    }
    for p in out.iterdir():
        if p.is_file():report['files'][p.name]={'sha256':sha(p),'bytes':p.stat().st_size}
    (out/'CP417_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--canon',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();print(json.dumps(run(a.canon,a.out),indent=2))
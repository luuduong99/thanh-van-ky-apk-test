#!/usr/bin/env python3
"""CP395 Lâm Thiển — source-locked LEFT eyelid/iris remnant audit.

All modifications are technical CANON-derived drafts. Not artist-approved.
Static mergedimage uses exactly the supplied CANON expression.
"""
from __future__ import annotations
import argparse, hashlib, io, json, shutil, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import cp394_source_lash_underpaint as cp394

CANON_SHA = cp394.CANON_SHA
CROP = cp394.CROP
SIZE = cp394.SIZE
PREVIOUS_SHA = 'd3774068b0d9464a7c3c640b0f21289a812493765259365a3ee481cc8af326d9'
RELEASE = {'status':'blocked_pending_art','sprite_paths':{},'spine_ready':False,'apk_ready':False}
LEFT_ROI = cp394.ROIS['LEFT']; RIGHT_ROI=cp394.ROIS['RIGHT']

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def checked_inputs(canon_path,prior_path):
    source=cp394.checked_canon(canon_path)
    if sha(prior_path)!=PREVIOUS_SHA: raise ValueError('CP394_PRIOR_SHA_MISMATCH')
    prior=Image.open(prior_path).convert('RGBA')
    if prior.size!=SIZE:raise ValueError('CP394_PRIOR_SIZE_MISMATCH')
    if cp394.outside_changes(source,prior):raise ValueError('CP394_PRIOR_OUTSIDE_EYE_MISMATCH')
    return source,prior

def masks(source,variant='tight'):
    """Transparent left-eye patch layers for local revision only.

    Top roots are protected; no redraw of forehead, eyebrow, hair or face.
    Two variants differ only in local coverage / lash band width.
    """
    if variant not in ('tight','soft'):raise ValueError('UNKNOWN_VARIANT')
    src=np.asarray(source)
    H,W=src.shape[:2]
    cp_layers=cp394.make_layers(source,'LEFT')
    skin=np.asarray(cp_layers['SKIN']); up_geom=cp394.GEOM['LEFT']['upper']
    left_skin=np.zeros((H,W,4),dtype=np.uint8)
    source_lash=np.zeros_like(left_skin)
    x1,y1,x2,y2=LEFT_ROI
    for x in range(35,67):
        upper=cp394.curve_at(up_geom,x)
        edge=float(np.clip(min((x-34)/4,(67-x)/4),0,1))
        for y in range(max(y1,int(upper)-2),min(y2,int(upper)+13)):
            dy=y-upper
            # Local under-lash shield: clear residual iris pixels but taper at eye corners.
            cover=float(1/(1+np.exp(-3.5*(dy-.7))) / (1+np.exp(2*(dy-10))) * edge * (.99 if variant=='tight' else .85))
            if cover>.008:
                if skin[y,x,3]:pix=skin[y,x,:3]
                else:pix=src[min(y+10,H-1),x,:3]
                left_skin[y,x,:3]=pix
                left_skin[y,x,3]=round(np.clip(cover,0,1)*255)
            # Keep original lash pigments in a *narrow* band; broad-source lash
            # alpha from CP394 retains some iris-gray, which looks like an open slit.
            width=.65 if variant=='tight' else .95
            strength=float(np.exp(-.5*((dy+.25)/width)**2)*edge*(.91 if variant=='tight' else .99))
            if strength>.005:
                source_lash[y,x,:3]=src[y,x,:3]
                source_lash[y,x,3]=round(np.clip(strength,0,1)*255)
    return {'SKIN_LOCAL':Image.fromarray(left_skin,'RGBA'), 'LASH_LOCAL':Image.fromarray(source_lash,'RGBA')}

def apply(prior,layer_dict):
    result=prior.copy()
    result.alpha_composite(layer_dict['SKIN_LOCAL'])
    result.alpha_composite(layer_dict['LASH_LOCAL'])
    return result

def diff(src,target):return int(np.any(np.asarray(src)!=np.asarray(target),axis=2).sum())
def left_only_change(prior,target):
    a=np.asarray(prior);b=np.asarray(target)
    outside=np.ones((SIZE[1],SIZE[0]),dtype=bool)
    x1,y1,x2,y2=LEFT_ROI;outside[y1:y2,x1:x2]=False
    return int(np.any(a[outside]!=b[outside],axis=1).sum())
def png_bytes(im):
    bio=io.BytesIO();im.save(bio,'PNG');return bio.getvalue()

def save_ora(source,prior,layers,candidates,path):
    desc=[('CANON V2.1 / exact / VISIBLE',source,True),
          ('CP394 old source-lash eye / historical hidden',prior,False)]
    for var in ('tight','soft'):
        for label in ('SKIN_LOCAL','LASH_LOCAL'):
            desc.append((f'CP395 {var} {label} / TECHNICAL NOT APPROVED',layers[var][label],False))
        desc.append((f'CP395 {var} composite / NOT APPROVED',candidates[var],False))
    mark=Image.new('RGBA',SIZE,(0,0,0,0));ImageDraw.Draw(mark).rectangle(LEFT_ROI,outline=(30,190,255,190),width=1)
    desc.append(('LEFT ROI audit / hidden',mark,False))
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'version':'0.0.3','name':'CP395 Lâm Thiển CANON exact, left eye drafts unapproved'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for idx,(label,im,visible) in enumerate(desc):
            name=f'data/layer_{idx:02}.png'
            z.writestr(name,png_bytes(im))
            ET.SubElement(stack,'layer',{'name':label,'src':name,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',png_bytes(source))
        z.writestr('Thumbnails/thumbnail.png',png_bytes(source.resize((84,98))))
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
    return len(desc)

def make_review(source,prior,candidates,path):
    scale=4; cardw=168*scale; cardh=197*scale;gap=14; left=24; top=88
    W=left*2+cardw*4+gap*3;H=top+cardh+100
    out=Image.new('RGB',(W,H),(12,34,54));d=ImageDraw.Draw(out)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    title=ImageFont.truetype(font,23);label=ImageFont.truetype(font,15)
    d.text((left,13),'CP395 | Lam Thien CANON V2.1 | LEFT eye local correction',font=title,fill='white')
    d.text((left,50),'Actual CANON source 168x197 | technical drafts only | ART NOT APPROVED',font=label,fill='#ffd6b6')
    for i,(caption,im) in enumerate((('CANON / APPROVED SOURCE',source),('CP394 / OLD DRAFT',prior),('CP395 / TIGHT DRAFT',candidates['tight']),('CP395 / SOFT DRAFT',candidates['soft']))):
        x=left+i*(cardw+gap)
        out.paste(im.convert('RGB').resize((cardw,cardh),Image.Resampling.NEAREST),(x,top))
        d.text((x,top+cardh+12),caption,font=label,fill='#ecf7ff')
    d.text((left,H-35),'Small localized corrections do NOT demonstrate painter-grade eyelid quality or animation readiness.',font=label,fill='#ffd6b6')
    out.save(path)

def make_eye_zoom(source,prior,candidates,path):
    box=(25,89,75,127)
    scale=8;w=(box[2]-box[0])*scale;h=(box[3]-box[1])*scale
    out=Image.new('RGB',(w*4+70, h+95),(12,34,54));D=ImageDraw.Draw(out)
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
    for i,(name,img) in enumerate((('CANON',source),('CP394',prior),('CP395 TIGHT',candidates['tight']),('CP395 SOFT',candidates['soft']))):
        x=10+i*(w+16)
        out.paste(img.crop(box).convert('RGB').resize((w,h),Image.Resampling.NEAREST),(x,45))
        D.text((x,13),name,font=f,fill='white')
    D.text((10,h+57),'Left-eye crop from the same approved CANON. The lash seam still requires artist review.',font=f,fill='white')
    out.save(path)

def build(canon,prior,outdir):
    # Fail-fast input validity before creating the output folder.
    source,old=checked_inputs(canon,prior)
    layers={v:masks(source,v) for v in ('tight','soft')}
    candidates={v:apply(old,layers[v]) for v in layers}
    for name,target in candidates.items():
        if left_only_change(old,target):raise AssertionError('Non LEFT-eye pixel modified')
        if cp394.outside_changes(source,target):raise AssertionError('Outside both eye ROIs changed')
    out=Path(outdir);art=out/'layers';qa=out/'qa';art.mkdir(parents=True,exist_ok=True);qa.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(canon,out/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    shutil.copyfile(prior,out/'CP394_CLOSED_EYE_SOURCE_LASH_STUDY_NOT_APPROVED.png')
    source.save(out/'CANON_SHY_PIXEL_EXACT.png')
    for v in layers:
        for label,img in layers[v].items():img.save(art/f'CP395_{v.upper()}_{label}_DRAFT.png')
        candidates[v].save(out/f'CP395_LEFT_{v.upper()}_DRAFT_NOT_APPROVED.png')
    count=save_ora(source,old,layers,candidates,out/'CP395_CANON_LEFT_EYE_9_LAYER_DRAFT_NOT_APPROVED.ora')
    make_review(source,old,candidates,qa/'CP395_CANON_CP394_CP395_SOURCE_EXACT_COMPARE.png')
    make_eye_zoom(source,old,candidates,qa/'CP395_LEFT_EYE_NATIVE_ZOOM_COMPARE.png')
    report={'checkpoint':'CP395','canon_sha256':CANON_SHA,'prior_cp394_sha256':PREVIOUS_SHA,
        'source_pixels':[168,197], 'source_portrait_crop':list(CROP),'openraster_layers':count,
        'technical_new_layers':4,'draft_variants':['tight','soft'],
        'changed_vs_cp394':{v:diff(old,candidates[v]) for v in candidates},
        'outside_left_eye_changed':{v:left_only_change(old,candidates[v]) for v in candidates},
        'outside_both_eye_rois_changed':{v:cp394.outside_changes(source,candidates[v]) for v in candidates},
        'original_canon_visible':True, 'closed_eye_visual_qa':'NOT_PASSED',
        'reason':'Subtle local narrowing still leaves uncertain skin/eyelash fidelity; low native resolution; requires manual artist-painted master and user approval.',
        'production_release':RELEASE,
        'next':'CP396: Painter-quality closed-eye master based on exact character identity, especially LEFT eyelid and skin shadows; await review before inbetweens and rig.'}
    (out/'CP395_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--cp394',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();print(json.dumps(build(args.canon,args.cp394,args.out),ensure_ascii=False,indent=2))
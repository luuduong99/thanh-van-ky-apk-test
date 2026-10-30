#!/usr/bin/env python3
"""CP406 high-resolution *DISPLAY PROXY*, CANON pixel-fidelity gate.
This is an editable display-scale overlay study, not a new native HD master.
It never changes the exact CANON outside two eye ROIs, never unlocks production.
"""
from pathlib import Path
import hashlib, io, zipfile, json, math, sys
import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from xml.etree import ElementTree as ET
sys.path.insert(0,str(Path(__file__).parent))
import cp401_occlusion_blink as cp

CANON='LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
BASELINE='CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png'
BASELINE_SHA='0391ba0cb906bf5334f176ac28a508cad4afa700fe6cb7c2deb52affaf1ac5f6'
D=4
S=12 # supersampling for all curves before converting to display resolution
size=(168*D,197*D)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def source_images(directory):
    root=Path(directory)
    open_img=cp.exact_source(root/CANON)
    if sha(root/BASELINE)!=BASELINE_SHA:raise ValueError('BASELINE_SHA_MISMATCH')
    close=Image.open(root/BASELINE).convert('RGBA')
    assert close.size==(168,197)
    assert cp.valid_pixels_only(open_img,close)==0
    return open_img,close

def colored_layers(scale=S):
    w,h=168*scale,197*scale
    keys=['soft_skin_shadow','upper_crease_warm','lash_tapered_core','separated_lash_strands','inner_corner_warmth']
    layers={key:Image.new('RGBA',(w,h),(0,0,0,0)) for key in keys}
    pens={k:ImageDraw.Draw(v,'RGBA') for k,v in layers.items()}
    def xy(x,y): return (int(round(x*scale)),int(round(y*scale)))
    for side,roi in cp.ROIS.items():
        x1,y1,x2,y2=roi
        closed=cp.CLOSED[side]
        points=np.array([cp.bez(closed,t) for t in np.linspace(0,1,800)])
        # Broad gentle lid/eyeshadow; use pigment variation rather than gray flat line
        for j,(x,y) in enumerate(points):
            t=j/(len(points)-1)
            f=max(0,np.sin(np.pi*t))**.5
            if f<=0: continue
            r=1.1+.8*f
            colors=[(-1.1,(143,73,91,13)),(-.1,(140,73,96,18)),(1.0,(148,76,96,10))]
            for oy,(rr,gg,bb,alpha) in colors:
                a=round(alpha*f)
                pens['soft_skin_shadow'].ellipse((*xy(x-r,y+oy-.52),*xy(x+r,y+oy+.52)),fill=(rr,gg,bb,a))
        # short gentle crease, broken not solid pencil stroke
        for j,t in enumerate(np.linspace(.16,.85,175)):
            x,y=cp.bez(closed,float(t)); f=(math.sin(math.pi*t)**2)
            if j%3==0:
                shift=2.5+.30*math.cos(4.3*t)
                r=.21+.12*f
                pens['upper_crease_warm'].ellipse((*xy(x-r,y-shift-r),*xy(x+r,y-shift+r)),fill=(113,62,75,round(70*f)))
        # Source CANON pigment: deep dark brown-violet with variable local density.
        # thicker at outer edge, narrow at inner. No giant solid straight stroke.
        for j,t in enumerate(np.linspace(.035,.97,900)):
            x,y=cp.bez(closed,float(t))
            outer=(1-t) if side=='LEFT' else t
            envelope=max(0., math.sin(math.pi*t))**.48
            w_core=(.62+.65*outer)*envelope
            alpha=round((185+42*outer)*envelope)
            pens['lash_tapered_core'].ellipse((*xy(x-w_core/2,y-w_core*.30),*xy(x+w_core/2,y+w_core*.42)),fill=(53,35,52,alpha))
        # tapered, staggered lashes: each tip is a triangle, not dots/comb.
        ts=np.linspace(.07,.92,29)
        for j,t in enumerate(ts):
            x,y=cp.bez(closed,float(t))
            outer=(1-t) if side=='LEFT' else t
            envelope=math.sin(math.pi*t)**.72
            amplitude=(.40+1.65*outer)*(0.80+0.17*math.sin(j*2.07))*envelope
            tilt=(-.15-.32*outer) if side=='LEFT' else (.15+.32*outer)
            # Normally eyelashes grow down when eyes shut; keep endpoints thin
            ex=x+tilt*amplitude
            ey=y+(.48+.65*outer)*amplitude
            width=(.17+.28*outer)*envelope
            poly=[xy(x-.55*width,y-.16),xy(x+.55*width,y+.09),xy(ex,ey)]
            pens['separated_lash_strands'].polygon(poly,fill=(64,41,58,round(135*envelope)))
        # Tear ducts use delicate skin tint
        t=.93 if side=='LEFT' else .07
        x,y=cp.bez(closed,t)
        pens['inner_corner_warmth'].ellipse((*xy(x-.55,y-.2),*xy(x+.65,y+.42)),fill=(180,89,103,55))
    # ROI mask at full-resolution ensures no paint anywhere outside the original eye areas
    m=np.zeros((197*scale,168*scale),np.uint8)
    for x1,y1,x2,y2 in cp.ROIS.values(): m[y1*scale:y2*scale,x1*scale:x2*scale]=255
    for k in layers:
        a=np.asarray(layers[k]).copy();a[m==0]=0;layers[k]=Image.fromarray(a,'RGBA')
    return layers

def composite_source_locked(src,baseline,layers,display_scale=D):
    large_orig=src.resize((src.width*display_scale,src.height*display_scale),Image.Resampling.LANCZOS)
    large=baseline.resize(large_orig.size,Image.Resampling.LANCZOS)
    for k,v in layers.items():
        low=v.resize(large_orig.size,Image.Resampling.LANCZOS)
        large=Image.alpha_composite(large,low)
    # Enforce equality with original outside eye polygons at exact DISPLAY resolution.
    a=np.array(large); b=np.array(large_orig)
    mask=np.zeros(a.shape[:2],bool)
    for x1,y1,x2,y2 in cp.ROIS.values(): mask[y1*display_scale:y2*display_scale,x1*display_scale:x2*display_scale]=True
    a[~mask]=b[~mask]
    a[:,:,3]=b[:,:,3]
    out=Image.fromarray(a,'RGBA')
    assert not np.any(np.array(out)[~mask]!=b[~mask])
    return large_orig,out

def review(open_img,baseline,master,preview_path):
    zoom=2
    items=[('CANON MỞ - NGUỒN',open_img.resize(size,Image.Resampling.LANCZOS)),
      ('CP402 NHẮM - MỐC CŨ',baseline.resize(size,Image.Resampling.LANCZOS)),
      ('CP406 NHẮM - BẢN THỬ',master)]
    W,H=size; pad=26; gap=16; top=110
    canvas=Image.new('RGB',(pad*2+W*3+gap*2,top+H+66),(21,32,45))
    d=ImageDraw.Draw(canvas)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    f0=ImageFont.truetype(font,30);f1=ImageFont.truetype(font,20)
    d.text((pad,13),'CP406 / LAM THIEN / DU DUNG CANON V2.1',font=f0,fill='white')
    d.text((pad,57),'Ban overlay mi 4x chi de duyet hinh anh - CHUA DUYET / KHONG THAY CANON',font=f1,fill=(255,199,150))
    for i,(title,im) in enumerate(items):
        x=pad+i*(W+gap)
        canvas.paste(im.convert('RGB'),(x,top))
        d.text((x,top+H+16),title,font=f1,fill='white')
    canvas.save(preview_path)

def make_ora(original,baseline,master,layers,path):
    '''Editable 4x ORA — display proxy only. Original source precisely scaled.'''
    root=ET.Element('image',{'w':str(size[0]),'h':str(size[1]),'name':'CP406 DRAFT / 4X DISPLAY PROXY / NOT CANON MASTER','version':'0.0.1'})
    stack=ET.SubElement(root,'stack')
    entries=[('CLOSED 4X COMPOSITE / DRAFT / HIDDEN',master,False)]
    entries += [(k+' / SEPARATE PAINT / HIDDEN',v.resize(size,Image.Resampling.LANCZOS),False) for k,v in reversed(list(layers.items()))]
    entries += [('CP402 CLOSED BASELINE UPSCALED / HIDDEN',baseline.resize(size,Image.Resampling.LANCZOS),False),('CANON EXACT UPSCALE / VISIBLE',original.resize(size,Image.Resampling.LANCZOS),True)]
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(entries):
            buf=io.BytesIO();im.save(buf,format='PNG')
            entry=f'data/layer_{i:02d}.png'
            z.writestr(entry,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':entry,'opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
        b=io.BytesIO();original.resize(size,Image.Resampling.LANCZOS).save(b,format='PNG')
        z.writestr('mergedimage.png',b.getvalue())
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))

def build(inp,outdir):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    src,baseline=source_images(inp)
    layers=colored_layers()
    source_x4,master=composite_source_locked(src,baseline,layers)
    source_x4.save(out/'CP406_CANON_UPSCALE_REFERENCE_NOT_HD.png')
    master.save(out/'CP406_CLOSED_EYE_4X_OVERLAY_DRAFT.png')
    review(src,baseline,master,out/'CP406_EXACT_CANON_CP402_CP406_COMPARE.png')
    make_ora(src,baseline,master,layers,out/'CP406_EYELID_8_LAYER_DISPLAY_DRAFT.ora')
    a=np.array(source_x4);b=np.array(master)
    mask=np.zeros(a.shape[:2],bool)
    for x1,y1,x2,y2 in cp.ROIS.values():mask[y1*D:y2*D,x1*D:x2*D]=True
    changed=int(np.any(a!=b,axis=2).sum());outside=int(np.any(a[~mask]!=b[~mask],axis=1).sum())
    report={'checkpoint':'CP406','canonsource_sha256':cp.CANON_SHA,'crop_size_native':[168,197],
      'display_scale':4,'display_proxy_size':list(master.size),'changed_display_pixels_inside_rois':changed,
      'outside_eye_changed_pixels':outside,'layers':8,'layering':'source 4x visible, baseline 4x hidden, 5 new RGBA painter layers hidden, composite hidden',
      'actual_original_HD_art_master':False,'artist_visual_qa':'NOT_APPROVED',
      'user_approval':'NOT_OBTAINED','android_build_tested':False,'production_release':'BLOCKED',
      'original_source_sha_verified':True,'master_sha256':sha(out/'CP406_CLOSED_EYE_4X_OVERLAY_DRAFT.png')}
    (out/'CP406_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--inputs',default=str(Path(__file__).parent));p.add_argument('--out',default=str(Path(__file__).parent/'outputs'))
    args=p.parse_args();print(json.dumps(build(args.inputs,args.out),indent=2))

# The following function is intentionally separate from the native-source
# builder: a 4x display preview must not be mistaken for recovered source art.
def run_animation(inp,outdir):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    src,baseline=source_images(inp)
    hi_base=baseline.resize(size,Image.Resampling.LANCZOS)
    hi_open=src.resize(size,Image.Resampling.LANCZOS)
    master=Image.open(out/'CP406_CLOSED_EYE_4X_OVERLAY_DRAFT.png').convert('RGBA')
    mm=np.zeros((size[1],size[0]),bool)
    for x1,y1,x2,y2 in cp.ROIS.values():mm[y1*D:y2*D,x1*D:x2*D]=True
    alpha_src=np.array(hi_open)[:,:,3]
    def frame(p):
        if p<=0: return hi_open.copy()
        if p>=1: return master.copy()
        native=cp.eyelid_position(src,baseline,p).resize(size,Image.Resampling.LANCZOS)
        a=np.array(native);b=np.array(master);s=np.array(hi_open)
        v=float(np.clip((p-.67)/.33,0,1));v=v*v*(3-2*v)
        a[mm,:3]=np.rint(a[mm,:3]*(1-v)+b[mm,:3]*v).astype(np.uint8)
        a[~mm]=s[~mm];a[:,:,3]=alpha_src
        return Image.fromarray(a,'RGBA')
    progress=[0,.14,.28,.42,.56,.72,.86,1,.86,.72,.56,.42,.28,.14,0]
    atlas=Image.new('RGBA',(size[0]*15,size[1]),(0,0,0,0))
    for i,p in enumerate(progress):atlas.alpha_composite(frame(p),(i*size[0],0))
    atlas.save(out/'CP406_ATLAS_15_DISPLAY_DRAFT.png')
    writer=cv2.VideoWriter(str(out/'CP406_BLINK_PREVIEW_30FPS_DRAFT.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),30,(size[0]*2,size[1]))
    if not writer.isOpened():raise ValueError('video encoder not available')
    frames=[]
    for t in range(72):
        p=cp.frame_progress(t/72)
        im=frame(p)
        if t%3==0:frames.append(im.resize((336,394),Image.Resampling.LANCZOS))
        composed=np.concatenate([np.asarray(hi_open.convert('RGB')),np.asarray(im.convert('RGB'))],axis=1)
        writer.write(cv2.cvtColor(composed,cv2.COLOR_RGB2BGR))
    writer.release()
    frames[0].save(out/'CP406_BLINK_PREVIEW_DRAFT.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
    assert np.array_equal(np.asarray(frame(0)),np.asarray(hi_open))
    assert np.array_equal(np.asarray(frame(1)),np.asarray(master))
    for p in progress:
        a=np.asarray(frame(p));b=np.asarray(hi_open)
        if not np.array_equal(a[~mm],b[~mm]):raise AssertionError('Frame leaks pixels outside eyes')
    return {'atlas_sha':sha(out/'CP406_ATLAS_15_DISPLAY_DRAFT.png'), 'atlas_dimensions':[size[0]*15,size[1]],'fps':30,'video_frames':72,'pose_frames':15,'review_only':True}

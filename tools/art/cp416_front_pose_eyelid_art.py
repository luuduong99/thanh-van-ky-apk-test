#!/usr/bin/env python3
"""CP416 adult Lâm Thiển exact-CANON front-pose closed-eye *art study*.

Original CANON is private. Only edited eye details are made; all other pixels
are untouched. Draft is not automatic paint approval, master HD, Spine or APK art.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SOURCE='LAM_THIEN_CANON_V2_1_FINAL_20261029.png'
SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BOX=(16,180,224,623)
SIZE=(208,443)
# Actual source front standing, NEVER expression portrait.
ROIS={'viewer_left':(87,47,105,60),'viewer_right':(105,47,125,60)}
S=12


def checksum(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def checked(path):
    if checksum(path)!=SHA: raise ValueError('Wrong CANON SHA (raw bytes); no output allowed')
    img=Image.open(path)
    if img.size!=(941,1672) or img.mode!='RGBA':raise ValueError('Wrong canonical size/mode')
    return img.copy()

def bezier(p0,p1,p2,p3,n=100):
    result=[]
    for k in range(n+1):
        t=k/n;u=1-t
        x=u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0]
        y=u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]
        result.append((round(x*S),round(y*S)))
    return result

def big_rgba():return Image.new('RGBA',(SIZE[0]*S,SIZE[1]*S),(0,0,0,0))

def draw_lid(front:Image.Image, variant:str)->tuple[Image.Image,Image.Image,Image.Image]:
    """Carefully hand-positioned underlid coverage and tapered lashes.

    Retain source skin via adjacent cheek texture, not a fabricated face sprite.
    Alpha compositing is constrained within each eye ROI and human review is needed.
    """
    if variant not in ('restful','complete'):raise ValueError('Unknown variant')
    image=np.asarray(front).astype(np.uint8)
    # New pigment on separate layers: underpaint and lash/crease, as editable RGBA.
    skin=big_rgba(); stroke=big_rgba(); shadow=big_rgba()
    # Eye shapes from exact front pose; x,y coordinates are NOT portrait coordinates.
    eyes=[
      {'roi':ROIS['viewer_left'], 'x0':89.70,'x1':101.8,'y':53.0,'shape':.8,'cheekrow':60},
      {'roi':ROIS['viewer_right'],'x0':108.20,'x1':121.35,'y':53.0,'shape':.6,'cheekrow':60},
    ]
    for eye in eyes:
        x0,y0,x1,y1=eye['roi']
        # The low-res image has no real closed eyelid hidden behind irises. Paint a
        # delicate skin plate from adjacent same-identity facial colors. Use tiny
        # graded local color variation so the fill does not turn into a flat band.
        texture=Image.new('RGBA',((x1-x0)*S,(y1-y0)*S),(0,0,0,0))
        pixels=texture.load()
        for yy in range((y1-y0)*S):
            py=y0+yy/S
            for xx in range((x1-x0)*S):
                px=x0+xx/S
                # Copy face colors from cheek just under the eyes, shifted 7 px.
                sy=eye['cheekrow']
                sx=int(min(SIZE[0]-1,max(0,math.floor(px))))
                c=image[sy,sx,:3].astype(float)
                # Hand-painted light catching the full lid, subtract dark blush noise.
                bright=1.7-0.26*abs(px-(x0+x1)/2)
                c=np.clip(c+bright,0,255)
                pixels[xx,yy]=(int(c[0]),int(c[1]),int(c[2]),255)
        # Dense center mask, tapered near brow and cheek. Keep outside original source.
        mask=Image.new('L',texture.size,0);m=ImageDraw.Draw(mask)
        # y of eye plate 50..57.8: no alterations to hair/eyebrow/nose/mouth.
        m.ellipse(((eye['x0']-x0-.5)*S,(51.4-y0)*S,(eye['x1']-x0+.6)*S,(57.6-y0)*S),fill=255)
        # Ellipse is clipped to the eye ROI.
        mask=mask.filter(ImageFilter.GaussianBlur(S*.22))
        texture.putalpha(mask)
        skin.alpha_composite(texture,(x0*S,y0*S))
        # Delicate lid shadow/crease follows the shape of each eye.
        lip=eye['y'] if variant=='complete' else eye['y']-.10
        p0=(eye['x0'],lip-.23);p1=(eye['x0']+3.6,lip+.7)
        p2=(eye['x1']-3.1,lip+.68);p3=(eye['x1'],lip-.20)
        line=bezier(p0,p1,p2,p3)
        d=ImageDraw.Draw(stroke,'RGBA')
        # Soft under-shadow, then fine line; avoid muddy eyes at 13 px native.
        d.line([(x,y+int(.28*S)) for x,y in line],fill=(160,91,102,40),width=max(1,int(.48*S)),joint='curve')
        d.line(line,fill=(94,53,73,225 if variant=='complete' else 192),width=max(1,int(.58*S)),joint='curve')
        # Eyelid fold drawn above the closure line, weaker and partly interrupted.
        crease=bezier((eye['x0']+1.2,lip-1.9),(eye['x0']+4.5,lip-2.25),
                     (eye['x1']-3.0,lip-2.05),(eye['x1']-1.0,lip-1.75))
        sh=ImageDraw.Draw(shadow,'RGBA')
        sh.line(crease,fill=(171,102,110,30 if variant=='complete' else 22),width=int(.30*S),joint='curve')
        # A few hand-authored lashes that taper by using very short strokes at
        # the outer edge. At source native size, they are deliberately subtle.
        lash_start=eye['x0']+.85
        d.line(bezier((lash_start,lip-.4),(lash_start-.48,lip-.46),(lash_start-.72,lip-.74),(lash_start-.9,lip-1.03),n=15),
               fill=(82,52,72,140),width=int(.21*S))
        d.line(bezier((eye['x1']-.50,lip-.3),(eye['x1']+.0,lip-.63),(eye['x1']+.27,lip-1.08),(eye['x1']+.5,lip-1.25),n=15),
               fill=(92,56,78,108),width=int(.20*S))
    # Convert once, then enforce EXACT ROI clamping: alpha must be zero elsewhere.
    result=[]
    allow=np.zeros((SIZE[1],SIZE[0]),np.uint8)
    for x0,y0,x1,y1 in ROIS.values():allow[y0:y1,x0:x1]=255
    for im in (skin,shadow,stroke):
        small=im.resize(SIZE,Image.Resampling.LANCZOS)
        a=np.array(small);a[:,:,3]=np.minimum(a[:,:,3],allow)
        result.append(Image.fromarray(a,'RGBA'))
    cover,fold,lashes=result
    composed=Image.alpha_composite(front,cover)
    composed=Image.alpha_composite(composed,fold)
    composed=Image.alpha_composite(composed,lashes)
    return cover,fold,lashes,composed

def difference_mask(a,b):
    aa=np.array(a);bb=np.array(b)
    return np.any(aa!=bb,axis=2)

def make_ora(path,front,versions):
    # Original is only visible layer. Candidates and their actual pigment layers
    # are hidden; mergedimage is pixel-exact source, preventing accidental promotion.
    layers=[]
    for name,(cover,fold,lashes,result) in versions.items():
        layers.extend([(f'{name} - lashes DRAFT',lashes,False),
                       (f'{name} - eyelid crease DRAFT',fold,False),
                       (f'{name} - skin hidden by iris DRAFT',cover,False),
                       (f'{name} - closed-eye composite DRAFT',result,False)])
    layers.append(('CANON front standing unchanged APPROVED SOURCE',front,True))
    root=ET.Element('image',w='208',h='443',name='CP416 same-pose eyelid study / NOT APPROVED',version='0.0.3')
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype',b'image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(layers):
            buf=io.BytesIO();im.save(buf,format='PNG')
            layer_path=f'data/layer{i:02}.png';z.writestr(layer_path,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':layer_path,'visibility':'visible' if visible else 'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        buf=io.BytesIO();front.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
    with zipfile.ZipFile(path) as z:assert z.testzip() is None
    return len(layers)

def qa_board(front,versions):
    names=['CANON eyes OPEN', 'DRAFT rest closed', 'DRAFT full closed']
    ims=[front,versions['restful'][3],versions['complete'][3]]
    # 2x viewing proxy (NOT native), plus approx. 8x eye region, shows limits.
    crop=(77,35,132,75);panel_w=416;gap=16;top=75
    width=(panel_w+gap)*3+gap;height=top+886+365+60
    board=Image.new('RGB',(width,height),(231,238,247));d=ImageDraw.Draw(board)
    d.text((16,12),'CP416  -  EXACT CANON LAM THIEN V2.1 FRONT-POSE EYE STUDY',fill=(23,55,87))
    d.text((16,31),'Original sprite 208x443; shown 2x + close crop. 2 eye ROIs only; DRAFT / NOT APPROVED',fill=(61,84,112))
    for i,(name,img) in enumerate(zip(names,ims)):
        x=gap+i*(panel_w+gap)
        d.rectangle((x,51,x+panel_w,73),fill=(31,57,88))
        d.text((x+10,55),name,fill=(255,255,255))
        board.paste(img.convert('RGB').resize((416,886),Image.Resampling.NEAREST),(x,top))
        ci=img.crop(crop).resize((panel_w,round(panel_w*(crop[3]-crop[1])/(crop[2]-crop[0]))),Image.Resampling.NEAREST)
        board.paste(ci.convert('RGB'),(x,top+886+12))
    d.text((16,height-39),'Native size is only 208x443: zoom is NOT extra HD art.',fill=(151,52,69))
    d.text((16,height-23),'No user visual approval, no blink timing or production sprite has been integrated.',fill=(151,52,69))
    return board

def run(source,out):
    img=checked(source);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    front=img.crop(BOX)
    versions={v:draw_lid(front,v) for v in ('restful','complete')}
    before=np.asarray(front)
    mask=np.zeros((SIZE[1],SIZE[0]),bool)
    for x0,y0,x1,y1 in ROIS.values():mask[y0:y1,x0:x1]=True
    counts={}
    for name,v in versions.items():
        diff=difference_mask(front,v[3]);outside=int(np.count_nonzero(diff & ~mask))
        assert outside==0
        counts[name]={'changed_pixels':int(diff.sum()),'outside_eye_changed':outside}
        v[3].save(out/f'CP416_{name.upper()}_CLOSED_EYE_DRAFT.png')
        for slot,im in zip(('skin','crease','lash'),v[:3]):
            im.save(out/f'CP416_{name.upper()}_{slot.upper()}_LAYER.png')
    front.save(out/'CP416_SOURCE_CANON_FRONT_208x443.png')
    atlas=Image.new('RGBA',(SIZE[0]*3,SIZE[1]),(0,0,0,0))
    for k,im in enumerate((front,versions['restful'][3],versions['complete'][3])):
        atlas.paste(im,(k*SIZE[0],0))
    atlas.save(out/'CP416_OPEN_SOFT_CLOSED_ATLAS_DRAFT.png')
    qa_board(front,versions).save(out/'CP416_CANON_NATIVE_AND_ZOOM_REVIEW.png')
    layers=make_ora(out/'CP416_SAME_POSE_CLOSED_EYE_EDITABLE_NOT_APPROVED.ora',front,versions)
    report={
      'checkpoint':'CP416','canon_sha256':SHA,'source_size':[941,1672],
      'front_box':BOX,'front_size':SIZE,'eye_rois':ROIS,
      'comparison_only_exact_canon':True,'versions':counts,
      'ora_layers':layers,'sprite_atlas_size':[SIZE[0]*3,SIZE[1]],'atlas_frame_zero_exact_source':True,'visual_approval':'PENDING_USER',
      'art_grade':'LOW_RES_SAME_POSE_SOURCE_LOCKED_DRAFT',
      'hd_redraw_ready':False,'closed_eyelid_same_pose_draft_present':True,
      'eyelid_closed_same_pose_art_approved':False,
      'neck_hair_underpaint_artist_approved':False,
      'rig_ready':False,'spine_ready':False,'apk_art_ready':False,
      'physical_android_tested':False,'sprite_paths':{},
      'production_release_status':'blocked_pending_art',
      'files':{}
    }
    for p in sorted(out.iterdir()):
        if p.is_file():report['files'][p.name]={'sha256':checksum(p),'bytes':p.stat().st_size}
    (out/'CP416_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();print(json.dumps(run(args.source,args.out),indent=2,ensure_ascii=False))
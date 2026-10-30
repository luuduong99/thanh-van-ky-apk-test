#!/usr/bin/env python3
"""CP411 CANON-only technical head separation audit. NOT production-ready artwork.

Output layers preserve exact source at neutral; generated underpaint is only a placeholder.
Never use the head capsule as an accepted rig, and never composite CP409 face on front pose.
"""
from __future__ import annotations
import argparse,hashlib,json,zipfile,io,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np, cv2
from PIL import Image,ImageDraw,ImageFont,ImageChops

CANON_HASH='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE=(941,1672)
FRONT=(16,180,224,623)
EXPRESSION=(25,684,193,881)
FACE_BOX=(83,40,128,74)
EYE_BOXES={'left':(89,48,102,58),'right':(107,48,122,58)}
HEAD_PIVOT=(104,77)
NECK_OVERLAP=(92,70,117,91)
# Conservative rough source-coordinate polygon, NOT semantically separated long hair.
HEAD_CAPSULE=[(100,1),(91,2),(81,8),(72,18),(66,31),(64,46),(69,58),(75,68),(85,77),(94,82),(106,85),(118,80),(129,73),(138,60),(143,47),(138,33),(131,22),(128,13),(115,3)]
INPAINT_RADIUS=3


def digest(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()

def load_checked(path:Path)->Image.Image:
    assert digest(path)==CANON_HASH,'CANON raw SHA mismatch'
    im=Image.open(path).convert('RGBA')
    assert im.size==CANON_SIZE
    return im

def head_binary_mask(size=(208,443)):
    img=Image.new('L',size,0)
    ImageDraw.Draw(img).polygon(HEAD_CAPSULE,fill=255)
    return img

def make_layers(front:Image.Image):
    mask=head_binary_mask(front.size)
    front_arr=np.array(front)
    matte_arr=np.array(mask)
    head_arr=front_arr.copy();head_arr[:,:,3]=np.where(matte_arr>0,front_arr[:,:,3],0)
    # The removed region has no real back/neck painting. Inpaint ONLY generates an audit placeholder.
    rgb=cv2.cvtColor(front_arr[:,:,:3],cv2.COLOR_RGB2BGR)
    plate=cv2.cvtColor(cv2.inpaint(rgb,matte_arr,INPAINT_RADIUS,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB)
    out=np.dstack((plate,front_arr[:,:,3]))
    plate_im=Image.fromarray(out,'RGBA')
    head_im=Image.fromarray(head_arr,'RGBA')
    neutral=Image.alpha_composite(plate_im,head_im)
    assert np.array_equal(np.array(neutral),front_arr),'neutral reconstruction MUST match CANON exactly'
    return mask,head_im,plate_im,neutral


def draw_guide(front:Image.Image,scale=4)->Image.Image:
    canvas=front.resize((front.width*scale,front.height*scale),Image.Resampling.NEAREST).convert('RGB')
    d=ImageDraw.Draw(canvas)
    poly=[(x*scale,y*scale) for x,y in HEAD_CAPSULE]
    d.line(poly+[poly[0]],fill='#ffb400',width=2)
    for label,box in [('face',FACE_BOX),('neck',NECK_OVERLAP),*[(f'eye-{k}',v) for k,v in EYE_BOXES.items()]]:
        c= '#46caad' if label.startswith('eye') else '#ea61a0' if label=='neck' else '#1284d6'
        d.rectangle(tuple(v*scale for v in box),outline=c,width=2)
    cx,cy=HEAD_PIVOT
    d.ellipse((cx*scale-5,cy*scale-5,cx*scale+5,cy*scale+5),fill='red',outline='white',width=2)
    d.text((max(0,cx*scale-100),max(1,cy*scale-25)),'HEAD PIVOT',fill='#b52528',stroke_width=1,stroke_fill='white')
    return canvas


def board(front,head,plate,guide,neutral,scale=2):
    # Full source high fidelity board with readable labels; no arbitrary new character image.
    panels=[front,head,plate,neutral]
    labels=['01 CANON FRONT','02 HEAD CUTOUT - ROUGH','03 GENERATED UNDERPAINT - NOT ART','04 NEUTRAL RECOMPOSITE EXACT']
    w,h=front.size; gutter=16;bar=36; top=50
    output=Image.new('RGB',(w*scale*4+gutter*5,top+(h*scale+bar)+52),'#e5edf5')
    d=ImageDraw.Draw(output)
    d.text((gutter,12),'CP411  |  CANON-LOCKED FRONT POSE HEAD SEPARATION   (TECHNICAL DRAFT)',fill='#14375a')
    for i,(name,p) in enumerate(zip(labels,panels)):
        ox=gutter+(w*scale+gutter)*i;oy=top
        d.rectangle((ox,oy,ox+w*scale,oy+bar),fill='#233f62')
        d.text((ox+8,oy+10),name,fill='#ffffff')
        if i==1:
            bg=Image.new('RGBA',p.size,'#cdd7e3')
            bg.alpha_composite(p)
            p=bg
        pane=p.convert('RGB').resize((w*scale,h*scale),Image.Resampling.NEAREST)
        output.paste(pane,(ox,oy+bar))
    d.text((gutter,top+bar+h*scale+14),'NEUTRAL COMPOSITE IS PIXEL EXACT. MOVING HEAD IS NOT APPROVED: NO TRUE NECK/HAIR UNDERPAINT.',fill='#9c3047')
    return output


def save_ora(path:Path,layers:list[tuple[str,Image.Image,bool]],merged:Image.Image):
    w,h=merged.size
    # ORA stack order is top-to-bottom; keep source visible and all experimental layers hidden.
    root=ET.Element('image',{'w':str(w),'h':str(h),'name':'CP411 CANON source + editable rough head segmentation (NOT APPROVED)','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,img,visible) in enumerate(layers):
            layer_path=f'data/layer{i:02d}.png'
            buf=io.BytesIO();img.save(buf,format='PNG')
            z.writestr(layer_path,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':layer_path,'opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        buf=io.BytesIO();merged.save(buf,format='PNG')
        z.writestr('mergedimage.png',buf.getvalue())


def run(source:Path,out:Path):
    out.mkdir(parents=True,exist_ok=True)
    canon=load_checked(source);front=canon.crop(FRONT)
    mask,head,plate,neutral=make_layers(front)
    originals={
        'CP411_CANON_FRONT_UNCHANGED.png':front,
        'CP411_HEAD_BINARY_MASK_RESEARCH_ONLY.png':mask,
        'CP411_HEAD_CAPSULE_ROUGH_NOT_RIG.png':head,
        'CP411_NECK_UNDERPAINT_AUTOMATIC_NOT_ART.png':plate,
        'CP411_NEUTRAL_RECOMPOSE_PIXEL_EXACT.png':neutral,
    }
    for name,img in originals.items():img.save(out/name)
    guide=draw_guide(front)
    guide.save(out/'CP411_FRONT_HEAD_ANCHOR_GUIDE_4X.png')
    board(front,head,plate,guide,neutral).save(out/'CP411_HEAD_SEGMENTATION_QA_BOARD.png')
    save_ora(out/'CP411_HEAD_SEPARATION_SOURCE_LOCKED_DRAFT.ora',[
        ('EXPERIMENT - head only, NOT rig-ready',head,False),
        ('EXPERIMENT - automatic underpaint, NOT art',plate,False),
        ('CANON front standing - unchanged, approved reference only',front,True),
    ],front)
    mask_count=int((np.array(mask)>0).sum())
    report={
        'checkpoint':'CP411','canon_hash':CANON_HASH,'canon_size':CANON_SIZE,'front_box':FRONT,'front_size':front.size,
        'face_expression_box':EXPRESSION,'front_face_box':FACE_BOX,'front_eyes':EYE_BOXES,
        'head_pivot':HEAD_PIVOT,'head_polygon':HEAD_CAPSULE,
        'mask_opaque_pixel_count':mask_count,'neutral_pixel_exact':True,
        'source_sha256':digest(source),'front_sha256':digest(out/'CP411_CANON_FRONT_UNCHANGED.png'),
        'portrait_pose_mismatch':True,'independent_head_rig_ready':False,
        'head_cutout_art_approved':False,'inpaint_art_approved':False,
        'artist_authored_neck_underpaint_present':False,'long_hair_isolated':False,
        'eye_sprite_correct_pose_present':False,'blink_fullbody_integrated':False,'physical_android_tested':False,
        'next_required':['high-resolution front face / true eyelid layers','artist-painted underlying scalp/neck/hair','semantic long-hair/arms/silk layer masks','seamless turning test'],
        'apk_production':False,'sprite_paths':{},'outputs':{}
    }
    for f in sorted(out.iterdir()):
        if f.is_file():report['outputs'][f.name]={'sha256':digest(f),'bytes':f.stat().st_size}
    (out/'CP411_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();result=run(args.canon,args.output)
    print(json.dumps({k:result[k] for k in ['mask_opaque_pixel_count','neutral_pixel_exact','front_sha256']},indent=2))
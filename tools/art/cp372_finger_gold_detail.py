#!/usr/bin/env python3
"""CP372 — source locked LOCAL hand + gold ornaments art fidelity trial.
Two separate SVG poses, three additional semantic layers, raster alpha clipped
against their parent artwork. NOT a complete sprite, animation or approved art.
"""
from pathlib import Path
import argparse, hashlib, io, json, importlib.util, zipfile
import xml.etree.ElementTree as ET
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cp371',ROOT/'cp371_refine_pose_details.py')
cp371=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp371)
SIZE=cp371.SIZE; SHA=cp371.SHA; FRONT=cp371.FRONT
HAND='10_hand_finger_engraving';WRIST='11_wrist_gold_filigrane';SHOULDER='12_shoulder_gold_filigrane'
ORDER=[]
for name in cp371.ORDER:
    ORDER.append(name)
    if name=='04_arm_skin_and_hand':ORDER.append(HAND)
    if name=='06_wrist_gold_moving':ORDER.append(WRIST)
    if name=='07_shoulder_gold_fixed':ORDER.append(SHOULDER)
ORDER=tuple(ORDER)
PARENTS={HAND:'04_arm_skin_and_hand',WRIST:'06_wrist_gold_moving',SHOULDER:'07_shoulder_gold_fixed'}
SHAPES={
 'idle':{
  HAND:r'''
   <!-- Three fingers, nail glints and soft joint creases, locally contained by arm silhouette. -->
   <path d="M2.2 199.9 Q7.3 197.8 11.4 197.1 M3.3 203.1 Q8.1 201.3 12.8 199.3 M8.6 194.2 Q12.9 191.4 17.9 190.7" fill="none" stroke="#ca8c94" stroke-width=".43" opacity=".61" stroke-linecap="round"/>
   <path d="M5.2 197.8 Q6.7 197.2 8.0 196.7 M8.9 192.6 Q10.4 192.1 12.2 191.5 M4.6 201.4 Q6 201.0 7.7 200.4" stroke="#fff7f3" stroke-width=".39" opacity=".85" fill="none"/>
   <path d="M15.1 192.2 Q15.9 193.8 15.1 194.7 M18.4 188.8 Q19 190.5 18.7 190.9" fill="none" stroke="#b87881" stroke-width=".34" opacity=".5"/>
   <path d="M12.5 194.0 Q14 193.5 14.8 193.6" fill="none" stroke="#edcbc5" stroke-width=".5" opacity=".65"/>
  ''',
  WRIST:r'''
   <path d="M21.4 188.0 Q24.3 188.4 25.4 191.5 Q27 193.1 30.7 193.3" fill="none" stroke="#fdf0c6" stroke-width=".54" opacity=".92"/>
   <path d="M23 191.1 Q22 193.2 24 195.3 Q26.4 197.2 28.6 194.1" fill="none" stroke="#91612f" stroke-width=".32" opacity=".69"/>
   <path d="M22.0 194 Q23.0 194.8 23.4 196 M30 189.9 Q31 191.4 30 193.2" fill="none" stroke="#fff8d6" stroke-width=".35"/>
   <circle cx="26.6" cy="192.6" r=".6" fill="#f8eed1" opacity=".8"/>
  ''',
 },
 'raised':{
  HAND:r'''
   <!-- Distinct raised palm line, no translated idle hand bitmap. -->
   <path d="M3 87.4 Q5.6 89.9 7.4 92.2 M6.8 83.9 Q9.0 87.0 11.0 90.5 M14.1 84.4 Q16.5 87 18.6 91.3" fill="none" stroke="#c78f99" stroke-width=".43" opacity=".65" stroke-linecap="round"/>
   <path d="M3.5 88.7 Q5.0 89.7 5.5 90.6 M8.5 85.2 L9.6 87.1 M15.0 85.7 Q16 86.9 16.4 88.0" fill="none" stroke="#fff7ef" stroke-width=".47" opacity=".88"/>
   <path d="M12.2 93.7 Q15.1 96.1 17.4 95.3 M16.1 96.4 Q20.0 98.6 22.7 98.0" fill="none" stroke="#ca9c9c" stroke-width=".39" opacity=".62"/>
  ''',
  WRIST:r'''
   <path d="M20.7 103 Q22.0 99.8 24.4 100.9 Q27 101.4 27.5 103.2" fill="none" stroke="#fff4cc" stroke-width=".54"/>
   <path d="M21.2 106.2 Q23.1 108.8 26.5 106.3 M20.9 102 Q21.8 104.3 22.0 106.0" fill="none" stroke="#926635" stroke-width=".33" opacity=".73"/>
   <path d="M24.8 102.7 L25.4 104.5 L24.2 105.6 L23.1 103.8Z" fill="none" stroke="#f9e9b5" stroke-width=".33"/>
   <path d="M21.9 104.5 L22.4 105.4 M26.5 103.9 L27.4 104.5" fill="none" stroke="#fff9d8" stroke-width=".32"/>
  ''',
 },
}
# Must remain identical between poses (static shoulder ornament).
SHOULDER_PATH=r'''
  <path d="M61 127.8 Q64.9 125.8 68 129.1 Q70.9 131.5 73.7 134.7" fill="none" stroke="#fff5c8" stroke-width=".5" opacity=".93"/>
  <path d="M59.3 135.2 Q64 133.2 66.2 136.9 Q67.2 139.0 69.1 139.4" fill="none" stroke="#915f36" stroke-width=".38" opacity=".66"/>
  <path d="M61.5 129.7 Q65 130 66.7 133.4 M68.6 132.8 Q71 133.7 71.5 136.0" fill="none" stroke="#fce5a6" stroke-width=".32" opacity=".8"/>
  <path d="M64.9 131.2 l1.5 -1.3 l1.4 1.5 l-1.4 1.5Z" fill="#9cc9ee" stroke="#ffefb6" stroke-width=".34" opacity=".8"/>
'''

def source_svg(name,pose):
    if pose not in ('idle','raised'): raise ValueError('Unknown pose')
    if name in PARENTS:
        inner=SHOULDER_PATH if name==SHOULDER else SHAPES[pose][name]
        return cp371.cp370.cp369.wrap_svg(inner)
    return cp371.svg(name,pose)

def raster_svg(name,pose):
    s=source_svg(name,pose)
    ET.fromstring(s)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=SIZE[0],output_height=SIZE[1]))).convert('RGBA')

def mask_overlay(overlay,parent):
    """Physically restrict new artwork to the colored alpha of its semantic parent."""
    alpha=ImageChops.multiply(overlay.getchannel('A'),parent.getchannel('A'))
    dst=overlay.copy();dst.putalpha(alpha)
    return dst

def create_ora(path,layers,canon_guide,pose):
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'version':'0.0.3','name':f'CP372 {pose} SEMANTIC DRAFT NOT APPROVED'})
    stack=ET.SubElement(root,'stack')
    merged=Image.new('RGBA',SIZE)
    for name in ORDER:merged.alpha_composite(layers[name])
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,name in enumerate(reversed(ORDER)):
            buf=io.BytesIO();layers[name].save(buf,format='PNG')
            target=f'data/layer_{i:02d}.png';z.writestr(target,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':f'CP372_{pose.upper()}_DRAFT__{name}', 'src':target,'x':'0','y':'0','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over'})
        buf=io.BytesIO();canon_guide.resize(SIZE,Image.Resampling.NEAREST).save(buf,format='PNG')
        z.writestr('data/CANON_HIDDEN_GUIDE.png',buf.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_REFERENCE_ONLY_HIDDEN_NOT_ART','src':'data/CANON_HIDDEN_GUIDE.png','x':'0','y':'0','opacity':'1.0','visibility':'hidden','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        b=io.BytesIO();merged.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
        assert z.testzip() is None
    return merged

def make_preview(path,canon_crop,old,rendered):
    focus=(0,80,115,265);dims=(392,632)
    items=[('01  ACTUAL CANON V2.1',canon_crop.crop(focus).resize(dims,Image.Resampling.LANCZOS)),
    ('02  CP371 IDLE, OLD DRAFT',old['idle'].crop(tuple(v*6 for v in focus)).resize(dims,Image.Resampling.LANCZOS)),
    ('03  CP372 IDLE, NEW DRAFT',rendered['idle'].crop(tuple(v*6 for v in focus)).resize(dims,Image.Resampling.LANCZOS)),
    ('04  CP372 RAISED, NEW DRAFT',rendered['raised'].crop(tuple(v*6 for v in focus)).resize(dims,Image.Resampling.LANCZOS))]
    canvas=Image.new('RGB',(1665,792),'#14253b');p=ImageDraw.Draw(canvas)
    p.text((23,22),'THANH VAN KY   /   LAM THIEN CP372   /   CANON-ONLY ARM AND GOLD DETAIL STUDY',fill='#fff6e9')
    p.text((23,49),'Two pose-specific finger + wrist designs; gold shoulder stays still. ALL NEW ART UNAPPROVED.',fill='#b6c9dc')
    for i,(label,img) in enumerate(items):
        x=23+i*410;p.text((x,100),label,fill='#e8f0ff')
        bg=Image.new('RGBA',dims,'white' if i==0 else '#d9e4ef')
        if i:
            d=ImageDraw.Draw(bg)
            for xx in range(0,dims[0],22):
                for yy in range(0,dims[1],22):
                    if ((xx//22+yy//22)%2)==0:d.rectangle((xx,yy,xx+21,yy+21),fill='#cbd6e2')
        bg.alpha_composite(img.convert('RGBA'))
        canvas.paste(bg.convert('RGB'),(x,126))
    p.text((23,767),'VISUAL QA NOT PASSED: only localized vector detail; not a CANON replacement / full-body sprite / Spine / Android APK.',fill='#ffd3a5')
    canvas.save(path)

def build(canon_file,out_dir):
    canon_file=Path(canon_file);out=Path(out_dir)
    if hashlib.sha256(canon_file.read_bytes()).hexdigest()!=SHA:raise ValueError('CANON_SHA_MISMATCH')
    with Image.open(canon_file) as canon:
        if canon.size!=(941,1672) or canon.mode!='RGBA':raise ValueError('CANON_FORMAT_MISMATCH')
        crop=canon.crop(FRONT)
    out.mkdir(parents=True,exist_ok=True)
    visible={};previous={};layers_by_pose={};clipping={}
    for pose in ('idle','raised'):
        local=out/pose;local.mkdir(exist_ok=True)
        layers={}
        for name in ORDER:
            svg=source_svg(name,pose)
            (local/(name+'.svg')).write_text(svg,encoding='utf-8')
            im=raster_svg(name,pose)
            if name in PARENTS:
                before=np.asarray(im.getchannel('A'))>12
                im=mask_overlay(im,layers[PARENTS[name]])
                after=np.asarray(im.getchannel('A'))>12
                clipping[(pose,name)]={'raw_visible_px':int(before.sum()),'retained_visible_px':int(after.sum()),'cut_px':int(np.count_nonzero(before & ~after))}
            layers[name]=im
            im.save(local/(name+'.png'))
        layers_by_pose[pose]=layers
        before_layers={n:cp371.rgba(n,pose) for n in cp371.ORDER}
        previous[pose]=cp371.compose(before_layers)
        visible[pose]=create_ora(out/f'CP372_{pose.upper()}_TWELVE_LAYER_DRAFT_NOT_SPINE.ora',layers,crop,pose)
        visible[pose].save(out/f'CP372_{pose.upper()}_TRANSPARENT_DRAFT.png')
    unchanged=all(np.array_equal(np.asarray(layers_by_pose['idle'][k]),np.asarray(layers_by_pose['raised'][k])) for k in cp371.cp370.cp369.STATIC_NAMES+(cp371.cp370.cp369.SHOULDER_NAME,SHOULDER))
    differences={pose:int(np.count_nonzero(np.any(np.asarray(visible[pose])!=np.asarray(previous[pose]),axis=2))) for pose in ('idle','raised')}
    for pose in ('idle','raised'):
        for name in PARENTS:
            if clipping[(pose,name)]['retained_visible_px']<5:raise ValueError(f'{pose}:{name} invisible/fully clipped')
    pv=out/'CP372_CANON_CP371_CP372_COMPARE_UNAPPROVED.png'
    make_preview(pv,crop,previous,visible)
    report={'checkpoint':'CP372','canon_sha256':SHA,'canon_px':[941,1672], 'front_crop':list(FRONT),
            'working_canvas':list(SIZE),'native_high_res_full_body_art':False,
            'pose_specific_finger_and_wrist_svg':True,'static_shoulder_detail_identical_across_poses':unchanged,
            'layers_per_pose':len(ORDER),'ora_layer_count_including_hidden_guide':len(ORDER)+1,
            'added':list(PARENTS),'clipping_metrics':{f'{k[0]}:{k[1]}':v for k,v in clipping.items()},
            'composite_pixels_different_from_cp371':differences,
            'visual_qa':'NOT_PASSED','production_release':'blocked_pending_art',
            'sprite_paths':{},'spine_ready':False,'apk_built':False,
            'warnings':['Local artwork is still schematic compared with approved CANON','A raster mask clip does not prove natural anatomy or bone interpolation',
                        'No full-body high-resolution semantic parts, no face/feet/game art','No verified runtime movement or Android APK'],
            'preview':pv.name}
    (out/'CP372_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--canon',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(build(a.canon,a.out),ensure_ascii=False,indent=2))
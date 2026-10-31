#!/usr/bin/env python3
"""CP369: source-locked edit of Lâm Thiển left shoulder/sleeve for technical articulation.

Real independent editable SVG geometry/PNG alpha and OpenRaster, but this is a
DRAFT and neither approved character art nor a validated Spine animation.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

import cairosvg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT if (ROOT/'cp368_refine_sleeve.py').exists() else ROOT.parent
CP368_PATH = SRC_DIR/'cp368_refine_sleeve.py'
spec = importlib.util.spec_from_file_location('cp368', CP368_PATH)
cp368 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp368)

SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
SIZE = (1302, 2748)
FRONT = (13,172,230,630)
PIVOT = (67,135)
STATIC_NAMES = ('01_rear_hair_lavender','02_hidden_bodice_cloth','03_hidden_shoulder_skin')
ARM_NAMES = ('04_arm_skin_and_hand','05_translucent_front_sleeve')
WRIST_NAME = '06_wrist_gold_moving'
SHOULDER_NAME = '07_shoulder_gold_fixed'
ORDER = (*STATIC_NAMES, *ARM_NAMES, WRIST_NAME, SHOULDER_NAME) # bottom -> top
MOTIONAL = (*ARM_NAMES,WRIST_NAME)

# The two hidden-area extensions are newly drawn vector fills. They do NOT come
# from alpha dilation or nearest-neighbour enlargement of a flat composite.
NEW_OVERPAINT = {
  '02_hidden_bodice_cloth': '''
  <defs><linearGradient id="hidden-bodice-369" x1="0.18" y1="0.03" x2=".82" y2="1">
   <stop stop-color="#fafaf9"/><stop offset=".32" stop-color="#dce9fa"/>
   <stop offset=".74" stop-color="#99bde9"/><stop offset="1" stop-color="#386ba9"/>
  </linearGradient></defs>
  <path d="M71 135 C78 137 84 145 86 158 C89 171 87 181 84 190
           C81 181 78 169 72 159 C68 150 67 141 71 135Z"
           fill="url(#hidden-bodice-369)" stroke="#6e9bd0" stroke-width=".65" opacity=".96"/>
  <path d="M74 139 C80 150 83 164 84 181" fill="none" stroke="#fffefa"
        stroke-width="1.1" opacity=".75"/>
  <path d="M78 145 C81 155 83 169 84 183" fill="none" stroke="#3b72b3"
        stroke-width=".62" opacity=".54"/>
  ''',
  '03_hidden_shoulder_skin': '''
  <defs><radialGradient id="occluded-skin-369" cx=".43" cy=".26" r=".86">
    <stop stop-color="#fff8f1"/><stop offset=".46" stop-color="#fae0d5"/>
    <stop offset=".83" stop-color="#ecc2b9"/><stop offset="1" stop-color="#ddaba7"/>
  </radialGradient></defs>
  <path d="M66 122 C61 125 57 131 57 139 C57 149 61 157 66 164
           Q73 169 76 160 C79 151 80 139 76 130 C73 124 69 121 66 122Z"
        fill="url(#occluded-skin-369)" stroke="#deaca4" stroke-width=".55"/>
  <path d="M62 128 C60 138 63 149 67 155" fill="none" stroke="#fff6ed"
        stroke-width="1.05" opacity=".74"/>
  <path d="M73 148 Q76 155 73 162" fill="none" stroke="#dda7a8"
        stroke-width=".56" opacity=".52"/>
  <!-- Locally painted seam underlays: cover newly exposed skin at +/- joint motion -->
  <path d="M57 138 C53.3 140 52.4 143 52.8 146.5 C53 150 56 152 60 151
           Q56 148 57 138Z" fill="#f7dcd1" stroke="#efc4b9" stroke-width=".35"/>
  <path d="M65 162 C68 163 70 166 70.3 170 C70.1 172 67 173 65 170Z"
        fill="#efc4bb" stroke="#e7b9b2" stroke-width=".35"/>
  ''',
}

# Distinct anchoring eliminates CP368's defect: the same gold layer previously
# contained both shoulder hardware and wrist hardware, so both rotated together.
GOLD_FIXED = '''
 <defs><linearGradient id="g369fixed" x1="0" y1="0" x2="1" y2="1">
  <stop stop-color="#fff2c7"/><stop offset=".41" stop-color="#bf914d"/>
  <stop offset=".77" stop-color="#f8dc9b"/><stop offset="1" stop-color="#8f6532"/>
 </linearGradient></defs>
 <path d="M59 129 C62 125 66 126 69 127 Q72 128 73 131
          C77 131 76 136 73 139 C69 140 65 139 62 140
          C58 140 56 136 59 129Z" fill="url(#g369fixed)" stroke="#a37334" stroke-width=".55"/>
 <path d="M60 133 C64 129 68 131 69 135 Q72 137 74 133"
       stroke="#fff4cd" stroke-width=".7" fill="none"/>
 <path d="M58 135 C61 134 62 135 61 138 Q65 140 67 136"
       stroke="#b7833d" stroke-width=".6" fill="none"/>
 <path d="M69 128 C67 125 67 122 69 123 C71 124 70 128 69 128Z"
       fill="#ddc483" stroke="#f7e4ac" stroke-width=".43"/>
 <path d="M73 133 C76 130 77 128 76 126" stroke="#f7df9d" stroke-width=".54" fill="none"/>
 <ellipse cx="67.4" cy="134.2" rx="1.85" ry="2.42"
          fill="#3b98d6" stroke="#f7e7bc" stroke-width=".6"/>
 <path d="M66.9 132.9 L67.3 134.2" stroke="#fbfdff" stroke-width=".48"/>
'''
GOLD_WRIST = '''
 <defs><linearGradient id="g369wrist" x1="0" y1="0" x2="1" y2="1">
  <stop stop-color="#fff0c1"/><stop offset=".42" stop-color="#c09046"/>
  <stop offset=".72" stop-color="#f5d79e"/><stop offset="1" stop-color="#8d622e"/>
 </linearGradient></defs>
 <path d="M23 189 C25 187 29 186 32 190 L29 196
        C26 199 23 197 21 194Z" fill="url(#g369wrist)" stroke="#98713e" stroke-width=".45"/>
 <path d="M23 192 Q26 189 30 192 M24 194 Q27 196 30 193"
       fill="none" stroke="#fff6d2" stroke-width=".61"/>
 <path d="M26.9 189.2 L29 192.3 L26.8 194.5 L25.1 191.7Z"
       fill="#419bce" stroke="#fff6ca" stroke-width=".38"/>
'''


def wrap_svg(content):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE[0]}" height="{SIZE[1]}" viewBox="0 0 217 458">{content}</svg>'


def svg_layer(name):
    if name in STATIC_NAMES or name in ARM_NAMES:
        content = cp368.svg_for_layer(name)
        if name in NEW_OVERPAINT:
            # Append occluded paint as a distinct design extension while retaining
            # source outlines in the editable geometry. This study is not full art.
            content = content.replace('</svg>', NEW_OVERPAINT[name] + '</svg>')
        return content
    if name == SHOULDER_NAME: return wrap_svg(GOLD_FIXED)
    if name == WRIST_NAME: return wrap_svg(GOLD_WRIST)
    raise KeyError(name)


def render(name):
    src=svg_layer(name)
    ET.fromstring(src)
    data=cairosvg.svg2png(bytestring=src.encode('utf-8'),output_width=SIZE[0],output_height=SIZE[1])
    return src,Image.open(io.BytesIO(data)).convert('RGBA')


def composite_in_order(layers):
    img=Image.new('RGBA',SIZE)
    for name in ORDER: img.alpha_composite(layers[name])
    return img


def rotate_arm_group(layers,angle,pivot=PIVOT):
    """Only arm, sleeve, wrist move; back hair/underpaint/shoulder ornament are fixed."""
    moved=Image.new('RGBA',SIZE)
    for name in MOTIONAL: moved.alpha_composite(layers[name])
    # Small-angle grouped transform; not an artist-painted second keyframe.
    moved=moved.rotate(angle,Image.Resampling.BICUBIC,center=(pivot[0]*6,pivot[1]*6))
    final=Image.new('RGBA',SIZE)
    for name in ORDER:
        if name==ARM_NAMES[0]:final.alpha_composite(moved)
        elif name not in MOTIONAL:final.alpha_composite(layers[name])
    return final


def region_alpha(im, box):
    return np.asarray(im.getchannel('A').crop(tuple(v*6 for v in box)))


def metrics(layers):
    """Diagnostic revealed pixels, restricted to body underpaint, NOT rear hair.

    Compare pixels previously covered by the moving arm at rest, subsequently
    exposed after rotation. This only probes a tight local shoulder region.
    """
    roi=(54,124,83,170)
    static=Image.new('RGBA',SIZE)
    for name in ('02_hidden_bodice_cloth','03_hidden_shoulder_skin'):
        static.alpha_composite(layers[name])
    resting_arm=Image.new('RGBA',SIZE)
    for name in MOTIONAL: resting_arm.alpha_composite(layers[name])
    backed=region_alpha(static,roi)>80
    at_rest=region_alpha(resting_arm,roi)>80
    result={}
    for angle in [0,-8,-15,8]:
        arm=resting_arm.rotate(angle,Image.Resampling.BICUBIC,center=(PIVOT[0]*6,PIVOT[1]*6))
        current=region_alpha(arm,roi)>80
        revealed=at_rest & ~current
        protected=revealed & backed
        unbacked=revealed & ~backed
        revealed_count=int(revealed.sum())
        result[str(angle)]={
           'static_body_underpaint_pixels':int(backed.sum()),
           'revealed_rest_arm_pixels':revealed_count,
           'revealed_with_body_underpaint':int(protected.sum()),
           'revealed_missing_body_underpaint':int(unbacked.sum()),
           'protected_fraction_of_revealed':round(int(protected.sum())/revealed_count,4) if revealed_count else None,
           'note':'Only local relative alpha check, NOT a verified full character rig or proof of gap-free joints',
        }
    return result


def make(canon_path,out_dir):
    canon_path=Path(canon_path)
    digest=hashlib.sha256(canon_path.read_bytes()).hexdigest()
    if digest!=SHA:raise ValueError('CANON_SHA_MISMATCH - refuse non-approved art')
    with Image.open(canon_path) as c:
        if c.mode!='RGBA' or c.size!=(941,1672):raise ValueError('CANON_FORMAT_MISMATCH')
        ref=c.crop(FRONT)
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(canon_path,out/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    layers={}
    for name in ORDER:
        svg,im=render(name)
        layers[name]=im
        (out/(name+'.svg')).write_text(svg,encoding='utf-8')
        im.save(out/(name+'.png'))
    rest=composite_in_order(layers)
    assert np.asarray(rest).shape==(SIZE[1],SIZE[0],4)
    rest.save(out/'CP369_IDLE_LOCAL_ART_DRAFT_NOT_APPROVED.png')
    for angle in [-8,-15,8]:
        rotate_arm_group(layers,angle).save(out/f'CP369_ROTATED_{angle:+d}_TECHNICAL_NOT_KEYFRAME.png')
    # OpenRaster: seven art layers editable separately plus hidden exact-source guide.
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'name':'CP369 Lâm Thiển partial art UNAPPROVED','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    ora_path=out/'CP369_SEVEN_LAYER_SEPARATED_SHOULDER_WRIST_NOT_SPINE.ora'
    with zipfile.ZipFile(ora_path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,name in enumerate(reversed(ORDER)):
            dest=f'data/layer{i:02d}.png';raw=io.BytesIO();layers[name].save(raw,format='PNG')
            z.writestr(dest,raw.getvalue())
            ET.SubElement(stack,'layer',{'name':'CP369_DRAFT__'+name,'src':dest,'opacity':'1.0','visibility':'visible','x':'0','y':'0','composite-op':'svg:src-over'})
        raw=io.BytesIO();ref.resize(SIZE,Image.Resampling.NEAREST).save(raw,format='PNG')
        z.writestr('data/reference.png',raw.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_REFERENCE_HIDDEN_NOT_ART','src':'data/reference.png','visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        raw=io.BytesIO();rest.save(raw,format='PNG');z.writestr('mergedimage.png',raw.getvalue())
    with zipfile.ZipFile(ora_path) as z:assert z.testzip() is None
    # Side-by-side exactly-approved CANON crop, CP368 draft, CP369 idle & rotation.
    focus=(0,98,103,259);zoom=(354,553)
    canon_focus=ref.crop(focus).resize(zoom,Image.Resampling.LANCZOS).convert('RGBA')
    old=Image.open(SRC_DIR/'CP368_OUT'/'CP368_LEFT_SLEEVE_REFINED_DRAFT_TRANSPARENT.png').convert('RGBA') if (SRC_DIR/'CP368_OUT'/'CP368_LEFT_SLEEVE_REFINED_DRAFT_TRANSPARENT.png').exists() else None
    sources=[('CANON V2.1 / APPROVED',canon_focus),
             ('CP368 / PREVIOUS DRAFT',old.crop(tuple(v*6 for v in focus)).resize(zoom,Image.Resampling.LANCZOS) if old else None),
             ('CP369 / IDLE DRAFT',rest.crop(tuple(v*6 for v in focus)).resize(zoom,Image.Resampling.LANCZOS)),
             ('CP369 / -15° TECH ONLY',rotate_arm_group(layers,-15).crop(tuple(v*6 for v in focus)).resize(zoom,Image.Resampling.LANCZOS))]
    w,h=1600,740;sheet=Image.new('RGB',(w,h),'#142238');d=ImageDraw.Draw(sheet)
    d.text((24,22),'THANH VAN KY / LAM THIEN CP369 - EXACT CANON & LOCALIZED DRAFT',fill='#f0f5ff')
    d.text((24,47),'Authoritative reference = user-approved CANON V2.1 only. CP368 & CP369 are NOT APPROVED.',fill='#ccd7e8')
    for idx,(label,im) in enumerate(sources):
        x=24+idx*395
        d.text((x,98),f'{idx+1:02d}  {label}',fill='#dbe9f4')
        if im is None:continue
        chess=Image.new('RGBA',zoom,'#e1e8ee');dc=ImageDraw.Draw(chess)
        for yy in range(0,zoom[1],24):
            for xx in range(0,zoom[0],24):
                if (xx//24+yy//24)%2==0:dc.rectangle((xx,yy,xx+23,yy+23),fill='#d1d9e5')
        if idx==0:chess=Image.new('RGBA',zoom,'#ffffff')
        sheet.paste(Image.alpha_composite(chess,im).convert('RGB'),(x,132))
    d.text((24,696),'CP369 change: gold shoulder fitting stays FIXED while wrist cuff follows arm; extra painted hidden shoulder/bodice.',fill='#f8dcb5')
    d.text((24,718),'VISUAL QA NOT PASSED | NOT full-body art, painter-drawn raised pose, Spine animation or Android APK.',fill='#a8bdd5')
    preview=out/'CP369_CANON_V2_1_CP368_CP369_SIDE_BY_SIDE_UNAPPROVED.png'
    sheet.save(preview)
    qa={
       'checkpoint':'CP369','canon_sha256':digest,'canon_valid':True,
       'canon_dimensions':[941,1672],'source_front_crop':list(FRONT),
       'editable_layer_count':len(ORDER), 'hidden_reference_layers':1,
       'functional_improvement':'Separate fixed shoulder gold from mobile wrist gold; extend independently drawn hidden shoulder and bodice material.',
       'motion':'grouped bitmap rotation only; no distinct raised-arm keyframe',
       'shoulder_static_ornament_does_not_rotate':True,
       'wrist_mobile_follows_arm':True,
       'joint_coverage_diagnostic_only':metrics(layers),
       'qa_limitations':['No artist-level visual approval','Only partial left sleeve/shoulder material','No pixel-exact game sprite or other full-body layers','No verified gap-free animation or Spine', 'No Android build or device FPS evidence'],
       'visual_qa':'NOT_PASSED','production_release':'blocked_pending_art',
       'sprite_paths':{},'spine_ready':False,'apk_ready':False,
       'files':{'ora':ora_path.name,'preview':preview.name}
    }
    (out/'CP369_QA_REPORT.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--canon',required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    result=make(a.canon,a.out)
    print(json.dumps(result,ensure_ascii=False,indent=2))
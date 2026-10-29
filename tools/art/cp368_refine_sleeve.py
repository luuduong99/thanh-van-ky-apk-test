#!/usr/bin/env python3
"""CP368: localized editable SVG fidelity refinement for Lam Thien CANON V2.1.
Draft source shapes; NOT approved full-body illustration, Spine art, or runtime image.
"""
from __future__ import annotations
from pathlib import Path
import hashlib, importlib.util, io, json, math, zipfile
import xml.etree.ElementTree as ET
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('cp366_source', HERE/'cp366_build_vector_sleeve.py')
cp366 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp366)
CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BBOX=(13,172,230,630)
SIZE=(1302,2748)

# Every layer below is new editable SVG geometry built against the actual user's
# approved CANON. Working resolution is 6x reference for curves; there is no
# claim that source art detail has grown by pixel upscaling.
DETAILS = {
'01_rear_hair_lavender': '''
 <g fill="none" stroke-linecap="round">
  <path d="M66 110 C43 131 38 151 31 169 C22 193 19 212 9 239" stroke="#f6f5ff" stroke-width="1.25" opacity=".74"/>
  <path d="M67 111 C44 139 32 159 29 182 Q22 220 6 249" stroke="#899fcf" stroke-width=".55" opacity=".7"/>
  <path d="M69 113 C53 127 42 141 38 163 C33 181 23 202 23 222" stroke="#d4daee" stroke-width="1.75" opacity=".53"/>
  <path d="M72 114 C60 129 46 146 43 164 C39 188 31 204 20 226" stroke="#7b9aca" stroke-width=".62" opacity=".50"/>
  <path d="M65 117 C48 142 45 158 39 177 C30 193 28 219 13 246" stroke="#ffffff" stroke-width=".65" opacity=".68"/>
  <path d="M73 113 C62 138 55 151 50 173 C47 200 30 217 27 246" stroke="#a3b6de" stroke-width=".6" opacity=".56"/>
 </g>''',
'02_hidden_bodice_cloth': '''
 <path d="M73 134 Q85 145 86 158 Q88 178 88 194 Q80 183 75 171 L69 158Z" fill="#8bb1df" fill-opacity=".25"/>
 <path d="M76 138 C81 148 83 157 84 172" stroke="#fdf9ef" stroke-width=".8" fill="none" opacity=".75"/>
 <path d="M79 147 C80 160 83 174 85 184" stroke="#3166b0" stroke-width=".55" fill="none" opacity=".62"/>
 <path d="M70 152 C76 162 78 175 84 188" stroke="#d9e9fb" stroke-width="1" fill="none" opacity=".6"/>
 ''',
'03_hidden_shoulder_skin': '''
 <path d="M65 122 C57 133 57 149 61 159 Q65 168 71 168 C76 161 77 154 79 148 L77 125 Q73 115 65 122Z" fill="#f4cdc4" fill-opacity=".92"/>
 <path d="M61 127 Q60 143 66 154" fill="none" stroke="#fff4e7" stroke-width="1.4" opacity=".8"/>
 <path d="M70 153 Q75 155 77 148" fill="none" stroke="#dfa6a4" stroke-width="1" opacity=".5"/>
 ''',
'04_arm_skin_and_hand': '''
 <g fill="none" stroke-linecap="round">
  <path d="M58 151 C51 163 41 178 30 188" stroke="#fff9ed" stroke-width="1.0" opacity=".8"/>
  <path d="M27 192 Q19 198 10 201" stroke="#cb9297" stroke-width=".45" opacity=".65"/>
  <path d="M24 195 Q16 201 8 203" stroke="#f9e2dd" stroke-width=".55" opacity=".76"/>
  <path d="M22 189 Q18 190 14 192" stroke="#d8a0a6" stroke-width=".4" opacity=".65"/>
 </g>''',
'05_translucent_front_sleeve': '''
 <defs>
 <linearGradient id="gauze368" x1="0" y1="0" x2="0.65" y2="1">
  <stop stop-color="#fffdfc" stop-opacity=".89"/>
  <stop offset=".35" stop-color="#f0f7ff" stop-opacity=".64"/>
  <stop offset=".72" stop-color="#a0c2e9" stop-opacity=".48"/>
  <stop offset="1" stop-color="#2d75c4" stop-opacity=".12"/>
 </linearGradient>
 <linearGradient id="edgeblue368" x1="0" y1="0" x2="1" y2="1">
  <stop stop-color="#ffffff" stop-opacity=".72"/>
  <stop offset=".5" stop-color="#9bbbe5" stop-opacity=".62"/>
  <stop offset="1" stop-color="#2377d0" stop-opacity=".65"/>
 </linearGradient>
 </defs>
 <!-- broad soft gauze panels; fluttering asymmetry rather than a stiff triangle -->
 <path d="M68 136 C51 151 42 166 35 183 C27 204 20 224 9 245 C27 237 44 219 51 203 C50 225 41 245 17 263 C51 254 69 229 72 204 Q79 166 74 147Z" fill="url(#gauze368)" stroke="#b5c9e7" stroke-width=".46" stroke-opacity=".63"/>
 <path d="M65 145 C52 165 46 188 39 209 C31 228 21 248 14 255 C37 244 49 220 59 194 C65 177 70 160 65 145Z" fill="#fbf9fc" fill-opacity=".36"/>
 <path d="M68 147 C72 161 67 181 63 197 C58 220 49 241 33 263 C60 246 75 215 79 192 C81 166 76 149 68 147Z" fill="#77a6df" fill-opacity=".24"/>
 <path d="M60 155 C45 182 36 200 29 219 C21 237 16 247 13 251" fill="none" stroke="#fdfefe" stroke-width="1.25" opacity=".83"/>
 <path d="M68 153 C59 179 54 195 46 216 C39 231 27 245 22 255" fill="none" stroke="#7ca4d8" stroke-width=".78" opacity=".70"/>
 <path d="M72 161 C74 190 68 222 43 247" fill="none" stroke="url(#edgeblue368)" stroke-width="1.24" opacity=".82"/>
 <path d="M55 171 C43 192 35 214 23 237" fill="none" stroke="#f8fbfd" stroke-width=".54" opacity=".9"/>
 <path d="M63 173 C53 201 45 231 33 250" fill="none" stroke="#4f8ac8" stroke-width=".44" opacity=".45"/>
 <path d="M51 165 C44 175 37 186 31 197" fill="none" stroke="#f2d8d0" stroke-width=".56" opacity=".5"/>
 ''',
'06_gold_shoulder_cuff_trim': '''
 <defs><linearGradient id="g368" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fdf0bf"/><stop offset=".45" stop-color="#bc8a49"/><stop offset=".78" stop-color="#f5dda1"/><stop offset="1" stop-color="#84552a"/></linearGradient></defs>
 <!-- filigree: narrow laced shoulder fitting, not the large flat star of CP366 -->
 <path d="M60 130 Q65 126 72 134 Q74 137 70 139 Q64 137 60 140 Q55 136 60 130Z" fill="url(#g368)" stroke="#a57237" stroke-width=".47"/>
 <g fill="none" stroke-linecap="round">
  <path d="M58 135 C62 131 64 130 66 132 C68 136 62 137 62 134 C63 132 65 133 64 134" stroke="#f9e6af" stroke-width=".76"/>
  <path d="M69 130 C66 129 66 126 69 125 C72 125 72 128 70 128" stroke="#ad7a37" stroke-width=".63"/>
  <path d="M70 134 C74 134 76 131 75 129 Q73 128 73 131" stroke="#f4d99a" stroke-width=".62"/>
  <path d="M57 135 C53 136 55 140 59 140" stroke="#be9455" stroke-width=".66"/>
  <path d="M68 137 C70 141 72 142 74 139" stroke="#9f713a" stroke-width=".50"/>
 </g>
 <ellipse cx="67.4" cy="134.1" rx="1.75" ry="2.3" fill="#4b96d1" stroke="#fff7d7" stroke-width=".55"/>
 <path d="M66.8 132.5 L67.3 134" stroke="white" stroke-width=".4" opacity=".65"/>
 <path d="M24 189 C27 187 29 187 31 189 Q31 193 28 196 L22 195Z" fill="url(#g368)" stroke="#9f723f" stroke-width=".48"/>
 <path d="M23 192 Q26 189 30 191 M24 194 Q28 195 30 192" stroke="#fce9b8" stroke-width=".58" fill="none"/>
 <path d="M26.7 189 L28 192.4 L26.3 193.5 L25 191Z" fill="#499bcc" stroke="#fff3c9" stroke-width=".3"/>
 ''',
}

def svg_for_layer(name):
    if name in ('05_translucent_front_sleeve','06_gold_shoulder_cuff_trim'):
        content = DETAILS[name]
    else:
        content = cp366.LAYER_CONTENT[name] + DETAILS[name]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE[0]}" height="{SIZE[1]}" viewBox="0 0 217 458">{content}</svg>'

def rotated(im,angle,pivot=(66,135)):
    # Approximate technical motion only, not real independent keyframes.
    return im.rotate(angle, Image.Resampling.BICUBIC, center=(pivot[0]*6,pivot[1]*6))

def alpha_count(im):
    return int(np.count_nonzero(np.asarray(im.getchannel('A'))>128))

def make(canon_path,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    cpath=Path(canon_path)
    got=hashlib.sha256(cpath.read_bytes()).hexdigest()
    if got!=CANON_SHA:raise ValueError('CANON_SHA_MISMATCH '+got)
    canon=Image.open(cpath)
    if canon.size!=(941,1672) or canon.mode!='RGBA':raise ValueError('CANON_MODE_OR_SIZE_INVALID')
    ref=canon.crop(BBOX)
    names=list(cp366.LAYER_CONTENT)
    images={}
    for name in names:
        source=svg_for_layer(name)
        ET.fromstring(source)
        (out/f'{name}.svg').write_text(source,encoding='utf-8')
        png=cairosvg.svg2png(bytestring=source.encode('utf-8'),output_width=SIZE[0],output_height=SIZE[1])
        image=Image.open(io.BytesIO(png)).convert('RGBA')
        images[name]=image
        image.save(out/f'{name}.png')
    comp=Image.new('RGBA',SIZE)
    for name in names:comp.alpha_composite(images[name])
    comp.save(out/'CP368_LEFT_SLEEVE_REFINED_DRAFT_TRANSPARENT.png')
    # ORA real independently editable SVG derived alpha layers + hidden source guide.
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'version':'0.0.3','name':'CP368 localized unfinished art draft'})
    stack=ET.SubElement(root,'stack')
    ora=out/'CP368_REFINED_SIX_LAYER_SLEEVE_DRAFT_NOT_SPINE.ora'
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,name in enumerate(reversed(names)):
            data=io.BytesIO();images[name].save(data,format='PNG');src=f'data/layer{i:02d}.png';z.writestr(src,data.getvalue())
            ET.SubElement(stack,'layer',{'name':'CP368_DRAFT__'+name,'src':src,'opacity':'1.0','visibility':'visible','x':'0','y':'0','composite-op':'svg:src-over'})
        data=io.BytesIO();ref.resize(SIZE,Image.Resampling.NEAREST).save(data,format='PNG')
        z.writestr('data/reference_only.png',data.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_REFERENCE_ONLY_HIDE','src':'data/reference_only.png','opacity':'1.0','visibility':'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        data=io.BytesIO();comp.save(data,format='PNG');z.writestr('mergedimage.png',data.getvalue())
    assert zipfile.ZipFile(ora).testzip() is None
    # QA: small motion overlap between fixed shoulder paint and moving sleeve/arm paint.
    static=Image.new('RGBA',SIZE)
    for name in names[:3]: static.alpha_composite(images[name])
    move=Image.new('RGBA',SIZE)
    for name in names[3:]: move.alpha_composite(images[name])
    # inspect joint in a tight fixed ROI, never claim an entire body seam is proven
    x1,y1,x2,y2=(53*6,123*6,83*6,161*6)
    sm=np.asarray(static.getchannel('A'))>50
    motion_metrics={}
    for angle in (0,-8,-15,8):
        shifted=rotated(move,angle)
        ma=np.asarray(shifted.getchannel('A'))>50
        j=int(np.count_nonzero(sm[y1:y2,x1:x2]&ma[y1:y2,x1:x2]))
        motion_metrics[str(angle)]={'shoulder_region_overlap_px':j,'overlap_nonzero':j>0}
        if angle in (0,-8,-15):
            pos=Image.alpha_composite(static,shifted)
            pos.save(out/f'CP368_{angle:+d}_DEGREE_TECHNICAL_ONLY.png')
    # Preview CANON only + explicit DRAFT not approved + same camera crop, not fake source.
    W,H=1510,850
    canvas=Image.new('RGB',(W,H),'#132237');d=ImageDraw.Draw(canvas)
    d.text((28,19),'LAM THIEN / CP368 - CANON-ONLY COMPARISON',fill='#f3f6fc')
    d.text((28,44),'Source = the exact user-approved CANON V2.1; NEW ART = UNAPPROVED localized SVG draft',fill='#c3d4e9')
    ref_focus=ref.crop((0,98,102,255)).resize((405,615),Image.Resampling.LANCZOS).convert('RGBA')
    cp366_image=Image.open(out.parent/'CP366_BASE'/'CP366_LEFT_SLEEVE_PARTIAL_STUDY_TRANSPARENT.png').convert('RGBA')
    old=cp366_image.crop((0,98*6,102*6,255*6)).resize((405,615),Image.Resampling.LANCZOS)
    new=comp.crop((0,98*6,102*6,255*6)).resize((405,615),Image.Resampling.LANCZOS)
    def checkboard():
        b=Image.new('RGBA',(405,615),'#e8edf3');dd=ImageDraw.Draw(b)
        for y in range(0,615,24):
            for x in range(0,405,24):
                if ((x//24+y//24)%2)==0:dd.rectangle((x,y,x+23,y+23),fill='#d6dee7')
        return b
    a=Image.alpha_composite(checkboard(),old)
    b=Image.alpha_composite(checkboard(),new)
    for x,title,img in [(26,'01  CANON V2.1 - APPROVED',ref_focus),(528,'02  CP366 - OLDER STUDY',a),(1030,'03  CP368 - NEW DRAFT',b)]:
        d.text((x,96),title,fill='#eaf0fb')
        canvas.paste(img.convert('RGB'),(x,127))
    d.text((26,770),'CP368 is a LOCAL sleeve art iteration, not the CANON full-body sprite and not ready for APK.',fill='#f6d6b0')
    d.text((26,799),'Artist visual review NOT PASSED. No character reference besides the approved CANON has been used.',fill='#bad1e7')
    canvas.save(out/'CP368_CANON_V2_1_vs_CP366_vs_CP368_UNAPPROVED.png')
    report={'checkpoint':'CP368','source_sha256':got,'source_size':list(canon.size),
        'origin':'user_approved_canon_v2_1_only','source_front_bbox':list(BBOX),'canvas':list(SIZE),
        'new_editable_svg_layers':len(names),'source_locked':True,
        'provenance_gate':'PASS','zip_crc_gate':'PASS','visual_qa':'NOT_PASSED',
        'production_release':'blocked_pending_art', 'rig_ready':False,'apk_ready':False,
        'technical_motion_overlap':motion_metrics,
        'interpretation':'Joint overlap >0 only shows some painted overlap near pivot; it does NOT establish gap-free body movement or Spine readiness.',
        'layers':[{'name':name,'alpha_pixels_gt_128':alpha_count(images[name]),'bbox':list(images[name].getchannel('A').getbbox())} for name in names],
        'unresolved':['Silk/hair paint fidelity to CANON not artist-approved','Full body hidden paint and accurate face are missing','Real second raised-arm keyframe not drawn','No independent Android runtime test']}
    (out/'CP368_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True)
    args=p.parse_args()
    print(json.dumps(make(args.canon,args.out),ensure_ascii=False,indent=2))
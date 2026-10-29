#!/usr/bin/env python3
"""CP366: six newly authored SVG fragments for Lâm Thiển image-left sleeve.

NOT approved full-body art, NOT a Spine rig, and NOT a real raised-arm drawing.
Coordinates are manually authored against the exact approved CANON V2.1 crop.
"""
from pathlib import Path
import hashlib, io, json, zipfile, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import cairosvg

SOURCE_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BBOX=(13,172,230,630)
CANVAS=(1302,2748)
LAYER_CONTENT={
 '01_rear_hair_lavender': '''
 <defs>
 <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#516fa8" stop-opacity=".76"/><stop offset=".38" stop-color="#e1deef" stop-opacity=".92"/><stop offset=".74" stop-color="#a5b6db" stop-opacity=".78"/><stop offset="1" stop-color="#f5f1f4" stop-opacity=".2"/></linearGradient>
 </defs>
 <path d="M71 103 C50 114 24 139 15 171 C7 199 13 218 4 247 Q22 239 36 202 C39 178 51 155 76 136Z" fill="url(#hair)" stroke="#9da9ce" stroke-width=".9" opacity=".66"/>
 <path d="M71 107 C40 133 21 164 20 197 C17 222 12 244 6 263" fill="none" stroke="#e9eaf7" stroke-opacity=".83" stroke-width="1.9"/>
 <path d="M68 116 Q26 149 24 201 T9 260" fill="none" stroke="#7596c9" stroke-opacity=".5" stroke-width=".9"/>
 <path d="M69 119 C37 150 32 178 31 211 C28 234 13 247 13 268" fill="none" stroke="#f9f8ff" stroke-opacity=".6" stroke-width="1.2"/>
 ''',
 '02_hidden_bodice_cloth': '''
 <defs><linearGradient id="bodice" x1=".1" x2=".9" y1="0" y2=".7"><stop stop-color="#fefdf8"/><stop offset=".4" stop-color="#b3c7eb"/><stop offset="1" stop-color="#305c99"/></linearGradient></defs>
 <path d="M73 136 Q81 139 84 153 C83 165 82 180 85 194 Q75 181 67 166 C66 153 68 143 73 136Z" fill="url(#bodice)" stroke="#7a9bc5" stroke-width=".8"/>
 <path d="M70 144 Q77 151 78 173 Q80 184 82 187" fill="none" stroke="#fffdf8" stroke-width="2.1" opacity=".8"/>
 <path d="M73 140 Q81 150 81 173" fill="none" stroke="#5d8acb" stroke-width=".6"/>
 ''',
 '03_hidden_shoulder_skin': '''
 <defs><radialGradient id="skin" cx=".48" cy=".25" r=".85"><stop stop-color="#fff5ee"/><stop offset=".45" stop-color="#f7d9cf"/><stop offset=".8" stop-color="#eabaae"/><stop offset="1" stop-color="#d99e9e"/></radialGradient></defs>
 <path d="M68 117 C59 121 56 129 59 141 Q64 153 69 161 Q75 159 80 146 L78 122 Q72 114 68 117Z" fill="url(#skin)" stroke="#cf9c9c" stroke-width=".65"/>
 <path d="M64 120 C59 128 61 138 67 146" fill="none" stroke="#fff8f1" stroke-width="2.4" opacity=".7"/>
 ''',
 '04_arm_skin_and_hand': '''
 <defs><linearGradient id="arm" x1=".35" y1=".0" x2=".78" y2=".94"><stop stop-color="#fff6ef"/><stop offset=".32" stop-color="#fbe2d9"/><stop offset=".8" stop-color="#edbdb5"/><stop offset="1" stop-color="#d69ba2"/></linearGradient></defs>
 <path d="M64 135 Q69 136 70 143 C65 152 58 159 50 169 C44 178 34 189 23 194 Q18 199 13 201 L4 204 Q1 203 4 200 L11 197 Q9 199 6 200 Q3 200 5 197 L14 192 Q14 191 9 193 Q7 192 10 190 L19 186 C32 178 41 167 48 155 Q56 141 64 135Z" fill="url(#arm)" stroke="#dba7a7" stroke-width=".65"/>
 <path d="M64 140 C54 152 50 169 27 187" fill="none" stroke="#fffaf1" stroke-width="2.5" opacity=".72"/>
 <path d="M45 169 Q32 185 22 188" fill="none" stroke="#e5aeb0" opacity=".45" stroke-width="1"/>
 ''',
 '05_translucent_front_sleeve': '''
 <defs><linearGradient id="veil" x1=".2" y1=".0" x2=".8" y2="1"><stop stop-color="#fffcf8" stop-opacity=".94"/><stop offset=".28" stop-color="#f1f6ff" stop-opacity=".76"/><stop offset=".7" stop-color="#b4caed" stop-opacity=".68"/><stop offset="1" stop-color="#5f94df" stop-opacity=".35"/></linearGradient></defs>
 <path d="M69 135 C61 139 55 145 50 153 Q39 165 31 178 Q25 187 15 193 C26 181 29 175 35 168 C28 185 21 203 11 218 C21 221 34 209 39 204 C41 224 31 235 17 247 C45 242 55 223 59 205 Q67 184 73 163 C76 149 75 141 69 135Z" fill="url(#veil)" stroke="#9bb9e4" stroke-opacity=".7" stroke-width=".65"/>
 <path d="M67 142 Q53 154 38 181 C32 191 24 201 14 214" fill="none" stroke="#fffdfb" opacity=".91" stroke-width="2.2"/>
 <path d="M65 151 C51 172 48 185 41 207 Q32 229 18 243" fill="none" stroke="#6f98d8" opacity=".6" stroke-width="1.1"/>
 <path d="M72 152 Q64 187 57 202 Q53 225 30 237" fill="none" stroke="#fff" opacity=".75" stroke-width="1.5"/>
 <path d="M55 158 Q43 171 33 184" fill="none" stroke="#d8bcb8" opacity=".45" stroke-width="1.2"/>
 <path d="M53 166 L40 180 M47 173 L35 187 M45 180 L32 193" fill="none" stroke="#e5c3bc" stroke-opacity=".5" stroke-width=".7"/>
 ''',
 '06_gold_shoulder_cuff_trim': '''
 <defs><linearGradient id="gold" x1="0" x2="1" y1=".0" y2="1"><stop stop-color="#f6e6ab"/><stop offset=".33" stop-color="#ba8745"/><stop offset=".62" stop-color="#f8e1a2"/><stop offset="1" stop-color="#8c612a"/></linearGradient></defs>
 <path d="M62 125 Q65 128 69 127 Q73 133 75 134 L70 142 Q65 138 59 139 L56 134 Q58 130 62 125Z" fill="url(#gold)" stroke="#8d6231" stroke-width=".7"/>
 <path d="M57 134 L65 131 L73 136 M60 137 L67 133 L72 140" fill="none" stroke="#fff1bc" stroke-width="1.1"/>
 <path d="M62 122 L64 128 L66 122 L67 131" fill="none" stroke="#af813e" stroke-width=".85"/>
 <path d="M26 185 Q30 189 33 192 Q29 197 25 197 Q22 194 19 190Z" fill="url(#gold)" stroke="#926d35" stroke-width=".7"/>
 <path d="M23 190 L29 193 L26 196" fill="none" stroke="#fff4c8" stroke-width="1"/>
 <ellipse cx="67.5" cy="133" rx="2" ry="2.8" fill="#76b7e3" stroke="#f8ebc1" stroke-width=".8"/>
 <path d="M67 132.5 L68 135" fill="none" stroke="#fff" stroke-width=".5"/>
 ''',
}

def svg(layer):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS[0]}" height="{CANVAS[1]}" viewBox="0 0 217 458">{LAYER_CONTENT[layer]}</svg>'''

def generate(canon_path,outdir):
    canon_path=Path(canon_path);outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(canon_path.read_bytes()).hexdigest()==SOURCE_SHA, 'Wrong CANON V2.1 master'
    master=Image.open(canon_path).convert('RGBA')
    guide=master.crop(BBOX)
    assert guide.size==(217,458)
    guide.resize(CANVAS,Image.Resampling.NEAREST).save(outdir/'CANON_FRONT_ONLY_HIDDEN_GUIDE_NEAREST.png')
    images={}
    for name in LAYER_CONTENT:
        s=svg(name);(outdir/(name+'.svg')).write_text(s,encoding='utf-8')
        png=cairosvg.svg2png(bytestring=s.encode('utf-8'),output_width=CANVAS[0],output_height=CANVAS[1])
        im=Image.open(io.BytesIO(png)).convert('RGBA')
        assert im.getchannel('A').getbbox() is not None
        images[name]=im
        im.save(outdir/(name+'.png'))
    # Actual independent study composite, topmost gold trim.
    merged=Image.new('RGBA',CANVAS)
    for name in LAYER_CONTENT:
        merged.alpha_composite(images[name])
    merged.save(outdir/'CP366_LEFT_SLEEVE_PARTIAL_STUDY_TRANSPARENT.png')
    root=ET.Element('image',attrib={'w':str(CANVAS[0]),'h':str(CANVAS[1]),'name':'CP366 partial artist authored arm (NOT READY)','version':'0.0.3'})
    stack=ET.SubElement(root,'stack')
    ora=outdir/'CP366_PARTIAL_SIX_LAYER_SLEEVE_ART_STUDY_NOT_SPINE.ora'
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,name in enumerate(reversed(tuple(images))):
            dest=f'data/layer_{i:02d}.png';raw=io.BytesIO();images[name].save(raw,format='PNG');z.writestr(dest,raw.getvalue())
            ET.SubElement(stack,'layer',{'name':'CP366_STUDY__'+name+'__NOT_APPROVED','src':dest,'opacity':'1.0','visibility':'visible','x':'0','y':'0','composite-op':'svg:src-over'})
        raw=io.BytesIO();guide.resize(CANVAS,Image.Resampling.NEAREST).save(raw,format='PNG')
        z.writestr('data/guide_reference.png',raw.getvalue())
        ET.SubElement(stack,'layer',{'name':'07__CANON_FRONT_REFERENCE_ONLY_HIDDEN_NOT_ART','src':'data/guide_reference.png','opacity':'1.0','visibility':'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        raw=io.BytesIO();merged.save(raw,format='PNG');z.writestr('mergedimage.png',raw.getvalue())
    assert zipfile.ZipFile(ora).testzip() is None
    # Preview creates meaningful comparison without falsely depicting finished full-body pose.
    canvas=Image.new('RGB',(1480,840),'#152437')
    d=ImageDraw.Draw(canvas)
    d.text((35,24),'TVK CP366 | LEFT SLEEVE - ART STUDY ONLY',fill='#ebf2f9',stroke_width=0)
    d.text((35,53),'Source-locked CANON V2.1   /   Six editable SVG fragments   /   NO full-body rig',fill='#acc1d6')
    ref=guide.crop((0,98,102,255)).resize((400,616),Image.Resampling.LANCZOS).convert('RGBA')
    # Stand-alone study: crop the same region with a neutral checkerboard backing
    detail=merged.crop((0,98*6,102*6,255*6)).resize((400,616),Image.Resampling.LANCZOS)
    checker=Image.new('RGBA',(400,616),'#e7eaf0');dc=ImageDraw.Draw(checker)
    for yy in range(0,616,24):
        for xx in range(0,400,24):
            if ((xx//24+yy//24)%2)==0:dc.rectangle((xx,yy,xx+23,yy+23),fill='#d6dce6')
    standalone=Image.alpha_composite(checker,detail)
    # 45% overlay to show alignment problems (for reviewers, not a pass)
    overlay=Image.alpha_composite(ref,Image.blend(Image.new('RGBA',detail.size),detail,0.45))
    canvas.paste(ref.convert('RGB'),(35,130));canvas.paste(standalone.convert('RGB'),(540,130));canvas.paste(overlay.convert('RGB'),(1045,130))
    for x,title in ((35,'01  APPROVED CANON CROP'),(540,'02  NEW VECTOR STUDY'),(1045,'03  ALIGNMENT OVERLAY')):
        d.text((x,104),title,fill='#e4eff9')
    d.text((35,770),'Artist review: NOT PASSED. Parts are source-aligned studies, NOT a faithful replacement for approved artwork.',fill='#ffd3a1')
    d.text((35,794),'Do not load into APK; retain original V2.1 proportions, silver hair, outfit and both blue shoes.',fill='#a8c1d8')
    canvas.save(outdir/'CP366_SLEEVE_ART_STUDY_SIDE_BY_SIDE.png')
    report={'checkpoint':'CP366','canon_sha256':SOURCE_SHA,'native_canvas':list(CANVAS),'new_svg_layers':len(images),
        'approved_full_body_art':False,'usable_same_camera_arm_raise_art':False,'spine_ready':False,
        'visual_qa':'NOT_PASSED','production_release':'blocked_pending_art',
        'new_layers':[{'name':key,'bbox':images[key].getchannel('A').getbbox()} for key in images],
        'notes':'Artist-authored vector shapes; still visibly different from original painted texture. No original approved artwork modified.'}
    (outdir/'CP366_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return report
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    print(json.dumps(generate(a.canon,a.out),ensure_ascii=False,indent=2))
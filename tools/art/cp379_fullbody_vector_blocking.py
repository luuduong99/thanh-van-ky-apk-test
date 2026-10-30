#!/usr/bin/env python3
"""CP379 Lâm Thiển: CANON-locked full-body artist-blocking VECTOR DRAFT.

The authored SVG body-part contours are a *newly drawn layout study*, not
CANON-quality painting. Kept separate from pixel-exact CANON trace guide.
No rig, Spine, APK, or release acceptance is implied by technical tests.
"""
import argparse, hashlib, io, json, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cairosvg

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE=(941,1672); FRONT=(13,172,230,630); SOURCE_SIZE=(217,458)
CANVAS=(1302,2748)
# Every visible block is a new Bezier drawing, no embedded bitmaps, no filtered-up source RGB.
# Bottom to top visual order; all positions in approved source's 217x458 Front coordinates.
ART = [
('01_back_left_silk_drape', '''
<path d="M68 146 C44 170 29 217 25 261 Q16 311 14 358 Q6 412 0 444 C23 426 36 405 40 373 Q57 320 69 267 C78 230 81 186 68 146Z" fill="url(#silk)" stroke="#85addd" stroke-width="1"/>
<path d="M66 160 Q35 222 33 305 T7 430 M53 209 Q37 321 18 406 M66 181 Q58 290 36 376" fill="none" stroke="#fff" stroke-width="2" opacity=".62"/>
<path d="M62 185 Q36 267 28 356 T4 439" fill="none" stroke="#4a85cd" stroke-width="1.1" opacity=".69"/>'''),
('02_back_right_silk_drape', '''
<path d="M145 149 Q181 179 187 257 C193 312 203 360 217 447 Q191 429 184 398 Q165 359 159 309 C144 248 133 197 145 149Z" fill="url(#silk)" stroke="#80abe1" stroke-width="1"/>
<path d="M147 157 C183 232 182 324 206 427 M156 189 Q170 282 189 374 M147 197 Q158 328 204 429" fill="none" stroke="#fff" stroke-width="1.8" opacity=".62"/>
<path d="M150 179 Q174 292 184 355 T216 446" fill="none" stroke="#4d8acb" stroke-width="1" opacity=".75"/>'''),
('03_back_left_hair', '''
<path d="M105 19 C76 24 69 66 66 100 Q61 141 35 170 C20 193 22 223 12 250 C34 220 57 211 71 185 Q84 151 93 113 Q101 62 105 19Z" fill="url(#hair)" stroke="#899bc8" stroke-width=".9"/>
<path d="M96 36 Q76 99 56 155 T19 225 M89 49 Q79 132 38 187" fill="none" stroke="#f8f7ff" stroke-width="1.6" opacity=".8"/>'''),
('04_back_right_hair', '''
<path d="M119 18 C142 22 144 70 156 109 Q173 158 184 183 Q198 206 202 247 C180 218 160 209 143 189 Q128 157 123 113 Q116 69 119 18Z" fill="url(#hair)" stroke="#8494be" stroke-width="1"/>
<path d="M122 28 Q144 90 166 158 T193 228 M129 48 Q139 128 184 200" fill="none" stroke="#f9f8ff" stroke-width="1.7" opacity=".78"/>'''),
('05_left_leg_occluded_skin', '''
<path d="M79 227 Q82 216 98 216 C108 239 109 279 106 312 L103 385 Q104 413 102 432 L88 433 C85 398 83 359 85 329 Q75 279 79 227Z" fill="url(#skin)" stroke="#daaca9" stroke-width=".7"/>
<path d="M92 256 Q87 336 94 406" stroke="#fff6f1" stroke-width="2.7" opacity=".6" fill="none"/>'''),
('06_right_leg_occluded_skin', '''
<path d="M109 227 Q126 214 138 229 C143 261 136 314 131 337 Q128 393 121 429 L107 425 C110 382 114 349 110 318 Q103 266 109 227Z" fill="url(#skin)" stroke="#d9a6a0" stroke-width=".7"/>
<path d="M125 257 Q133 311 120 408" stroke="#fff6ec" stroke-width="2.4" opacity=".55" fill="none"/>'''),
('07_left_shoe_blue_toe', '''
<path d="M86 414 Q93 405 101 414 L107 436 Q106 447 97 450 Q88 450 84 441Z" fill="url(#gold)" stroke="#825d32" stroke-width=".8"/>
<path d="M88 432 Q97 440 105 432 Q104 448 97 450 Q90 450 86 442Z" fill="#2e75ca" stroke="#d8e9ff" stroke-width=".8"/>
<path d="M88 418 Q99 413 104 421 M91 425 L99 438 L104 425" fill="none" stroke="#fbe4a7" stroke-width="1.4"/>'''),
('08_right_shoe_blue_toe', '''
<path d="M111 410 Q119 402 126 414 L130 433 Q127 442 119 442 Q109 439 108 430Z" fill="url(#gold)" stroke="#825d32" stroke-width=".8"/>
<path d="M112 430 Q121 433 128 426 L128 436 Q122 442 116 441Z" fill="#296ec5" stroke="#d8ebff" stroke-width=".8"/>
<path d="M110 418 Q121 412 126 419" fill="none" stroke="#f4e1ac" stroke-width="1.3"/>'''),
('09_lower_garment_base', '''
<path d="M76 169 Q87 171 105 173 Q130 171 146 171 C157 201 143 238 128 265 L115 282 Q110 268 105 274 Q94 272 90 259 C77 231 66 207 76 169Z" fill="url(#silk)" stroke="#6e95cb" stroke-width="1"/>
<path d="M96 185 Q86 232 103 265 M118 183 Q132 231 112 272" stroke="#fff" stroke-width="2" opacity=".66" fill="none"/>
<path d="M79 175 Q91 205 85 239 M143 181 Q131 208 135 236" fill="none" stroke="#377ac5" stroke-width="1"/>'''),
('10_torso_occluded_skin', '''
<path d="M89 88 Q111 82 133 92 Q148 107 148 132 Q142 151 136 171 C133 185 128 196 119 206 Q109 202 98 209 Q86 189 80 164 Q69 137 74 113Z" fill="url(#skin)" stroke="#d4a9a5" stroke-width=".65"/>
<path d="M104 95 Q109 104 114 110 M106 176 Q112 189 118 197" fill="none" stroke="#fff1ec" stroke-width="2" opacity=".66"/>'''),
('11_bodice_white_blue', '''
<path d="M69 117 Q81 108 98 115 Q108 124 110 142 Q115 123 123 116 Q138 109 151 120 Q155 138 140 153 L131 162 Q127 178 113 190 Q101 176 93 165 Q75 152 69 135Z" fill="url(#bodice)" stroke="#3f78b3" stroke-width="1"/>
<path d="M78 121 Q89 112 99 124 Q104 132 107 145 M117 141 Q126 114 141 120 M81 145 Q109 164 143 145" stroke="#ffffff" stroke-width="1.6" opacity=".93" fill="none"/>
<path d="M97 165 L112 189 L130 165 M86 149 L113 164 L138 150" fill="none" stroke="#4b83bf" stroke-width="1"/>'''),
('12_left_arm_hand_skin', '''
<path d="M70 118 Q76 123 74 139 C69 150 57 160 46 173 Q38 187 28 189 L13 195 Q8 201 4 199 L13 191 Q7 196 4 194 L17 187 L22 185 Q35 176 47 154 Q56 133 70 118Z" fill="url(#skin)" stroke="#d9a8a3" stroke-width=".72"/>
<path d="M15 189 L4 191 M20 191 L7 198 M42 175 Q54 150 66 136" fill="none" stroke="#fffbf7" stroke-width="1.4" opacity=".7"/>'''),
('13_right_arm_hand_skin', '''
<path d="M151 118 Q165 130 171 150 Q183 177 195 185 L205 189 Q216 196 212 198 L204 196 Q214 204 208 204 L192 192 Q180 191 171 177 L151 145 Q147 132 151 118Z" fill="url(#skin)" stroke="#d9a8a3" stroke-width=".72"/>
<path d="M200 190 L211 197 M192 188 Q177 163 160 140" fill="none" stroke="#fffaf7" stroke-width="1.4" opacity=".7"/>'''),
('14_left_silk_sleeve', '''
<path d="M69 125 C59 132 48 145 41 160 Q33 178 24 186 C31 188 40 184 47 179 Q34 206 19 231 C40 225 55 211 58 197 Q71 173 80 146 Q77 131 69 125Z" fill="url(#veil)" stroke="#8db1d9" stroke-width=".65"/>
<path d="M72 139 Q48 161 28 220 M65 141 Q57 188 30 220" fill="none" stroke="#fff" stroke-width="2" opacity=".77"/>'''),
('15_right_silk_sleeve', '''
<path d="M149 127 Q162 133 173 157 Q183 175 193 185 Q185 188 175 181 Q185 206 199 227 Q177 225 164 202 Q149 177 140 147Z" fill="url(#veil)" stroke="#8aaed8" stroke-width=".7"/>
<path d="M149 139 Q174 172 188 219 M157 146 Q163 182 193 221" fill="none" stroke="#fff" stroke-width="1.9" opacity=".78"/>'''),
('16_neck_collar', '''
<path d="M92 87 Q107 96 116 98 Q127 93 135 88 L130 101 Q119 111 113 119 Q102 105 93 100Z" fill="#f6f3fa" stroke="#ad823f" stroke-width="1.2"/>
<path d="M93 94 L113 113 L134 91 M103 98 L113 110 L123 100" fill="none" stroke="#b68a45" stroke-width="1.1"/>
<circle cx="113" cy="113" r="3.5" fill="#428ec8" stroke="#ead6a4" stroke-width="1.1"/>'''),
('17_face_skin', '''
<path d="M87 41 Q87 23 109 23 Q129 24 131 44 L128 65 C126 76 120 84 112 86 Q99 84 92 73 C86 62 86 50 87 41Z" fill="url(#skin)" stroke="#cda8aa" stroke-width=".7"/>
<path d="M96 63 Q100 66 104 63 M117 63 Q122 66 126 62" fill="none" stroke="#efb6b0" opacity=".65" stroke-width="1.1"/>'''),
('18_face_eyes_mouth', '''
<path d="M92 50 Q98 46 104 51 Q98 54 93 52 M118 51 Q123 46 129 50 Q124 54 119 52" fill="#fbffff" stroke="#594c65" stroke-width="1.2"/>
<ellipse cx="99" cy="51" rx="2" ry="3" fill="#a46e53"/><ellipse cx="124" cy="51" rx="2" ry="3" fill="#a46e53"/>
<path d="M99 72 Q112 78 122 70" fill="none" stroke="#b87577" stroke-width=".9"/>
<path d="M92 44 Q98 41 104 44 M117 44 Q124 41 129 44" fill="none" stroke="#796178" stroke-width=".65"/>'''),
('19_front_silver_lavender_hair', '''
<!-- Forehead remains visible: bang tips and side locks frame eyes rather than occlude the face. -->
<path d="M108 16 Q90 14 88 32 Q85 49 86 67 L94 79 Q96 62 96 51 Q95 37 104 29 C105 36 105 39 109 46 Q112 39 113 31 Q119 43 121 47 Q124 33 126 30 Q135 52 129 79 Q140 62 137 35 Q133 13 108 16Z" fill="url(#hair)" stroke="#788caf" stroke-width=".8"/>
<path d="M100 21 Q90 37 93 67 M123 22 Q132 37 133 66 M106 18 Q102 28 105 38 M115 19 Q121 29 121 38" stroke="#fff" opacity=".86" stroke-width="1.4" fill="none"/>'''),
('20_gold_waist_hip_and_shoulder', '''
<path d="M100 157 L112 166 L123 156 L120 176 L112 187 L104 176Z" fill="url(#gold)" stroke="#7b582d" stroke-width=".75"/>
<path d="M108 170 L113 178 L118 169Z" fill="#4b9bda" stroke="#fcf0cf" stroke-width=".6"/>
<path d="M65 120 Q69 116 78 122 L83 132 Q75 136 68 132Z M143 120 Q151 115 155 125 L152 135 Q146 134 139 131Z" fill="url(#gold)" stroke="#8c673d" stroke-width=".85"/>
<path d="M82 216 Q91 212 97 219 L96 231 Q86 237 80 227Z M128 214 Q139 211 143 223 L137 233 Q132 231 125 222Z" fill="url(#gold)" stroke="#8f682b" stroke-width=".8"/>
<path d="M79 134 Q87 143 89 151 M136 146 Q140 138 145 134" stroke="#b88139" stroke-width="1.2" fill="none"/>'''),
('21_head_flower_ribbons', '''
<path d="M83 22 Q92 15 99 20 Q104 24 99 29 Q93 35 88 27 Q80 28 83 22Z M124 19 Q132 15 138 22 Q137 29 128 30 Q120 25 124 19Z" fill="#fbfafc" stroke="#9b8bb2" stroke-width=".85"/>
<circle cx="93" cy="25" r="3" fill="#d6b073"/><circle cx="131" cy="24" r="3" fill="#d6b073"/>
<path d="M83 25 L76 58 M139 23 L145 58" stroke="#317ec1" stroke-width="2" fill="none"/>
<path d="M77 49 L80 58 L74 61 M145 49 L148 56 L144 62" fill="#4a8fdf" stroke="#cb9d60" stroke-width=".4"/>''')
]
DEFS='''<defs>
<linearGradient id="silk" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f9faff" stop-opacity=".88"/><stop offset=".44" stop-color="#b8d0f2" stop-opacity=".88"/><stop offset=".8" stop-color="#739fd9" stop-opacity=".82"/><stop offset="1" stop-color="#3c74c6" stop-opacity=".63"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="1" y2=".3"><stop stop-color="#a0a0c6"/><stop offset=".36" stop-color="#f8f4ff"/><stop offset=".66" stop-color="#d2cee9"/><stop offset="1" stop-color="#789bcf"/></linearGradient>
<radialGradient id="skin" cx=".34" cy=".27" r=".95"><stop stop-color="#fff3ea"/><stop offset=".6" stop-color="#f3cfc6"/><stop offset="1" stop-color="#dca6a0"/></radialGradient>
<linearGradient id="bodice" x1=".25" y1="0" x2=".8" y2="1"><stop stop-color="#fefcff"/><stop offset=".35" stop-color="#fffefa"/><stop offset=".72" stop-color="#a5c2e9"/><stop offset="1" stop-color="#3776ba"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff3c2"/><stop offset=".25" stop-color="#ba8b4d"/><stop offset=".57" stop-color="#f8d58e"/><stop offset="1" stop-color="#895923"/></linearGradient>
<linearGradient id="veil" x1="0" y1="0" x2=".6" y2="1"><stop stop-color="#ffffff" stop-opacity=".94"/><stop offset=".42" stop-color="#e7edfa" stop-opacity=".76"/><stop offset="1" stop-color="#84b2e6" stop-opacity=".48"/></linearGradient>
</defs>'''

def svg_for(name):
    body=dict(ART)[name]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS[0]}" height="{CANVAS[1]}" viewBox="0 0 217 458">{DEFS}{body}</svg>'

def get_canon(path):
    data=Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest()!=CANON_SHA:raise ValueError('Wrong CANON V2.1 sha256')
    img=Image.open(io.BytesIO(data))
    if img.size!=CANON_SIZE or img.mode!='RGBA':raise ValueError('Wrong CANON mode/size')
    return img

def create_ora(path,layers,guide,visible=True):
    size=guide.size
    root=ET.Element('image',{'w':str(size[0]),'h':str(size[1]),'version':'0.0.3','name':'CP379 DRAFT not rig'})
    stack=ET.SubElement(root,'stack')
    composite=Image.new('RGBA',size)
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for name,image in layers:composite.alpha_composite(image)
        for i,(name,image) in enumerate(reversed(layers)):
            b=io.BytesIO();image.save(b,'PNG');loc=f'data/art_{i:02d}.png'
            z.writestr(loc,b.getvalue());ET.SubElement(stack,'layer',{'name':'DRAFT__'+name,'src':loc,'visibility':'visible' if visible else 'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        b=io.BytesIO();guide.save(b,'PNG');z.writestr('data/CANON_SOURCE_REFERENCE.png',b.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_EXACT_SOURCE_REFERENCE_HIDDEN','src':'data/CANON_SOURCE_REFERENCE.png','visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        b=io.BytesIO();composite.save(b,'PNG');z.writestr('mergedimage.png',b.getvalue())
    assert zipfile.ZipFile(path).testzip() is None
    return composite

def build(canon, source_matte, source_layers_dir, output):
    # Immutable source validation BEFORE producing any files.
    original=get_canon(canon)
    front=original.crop(FRONT)
    matte=Image.open(source_matte).convert('RGBA')
    if matte.size!=SOURCE_SIZE or not np.array_equal(np.asarray(front)[:,:,:3],np.asarray(matte)[:,:,:3]):
        raise ValueError('CP374 source-matte does not match exact approved CANON Front RGB')
    source_dir=Path(source_layers_dir)
    guides=sorted(source_dir.glob('*.png'))
    if len(guides)!=19:raise ValueError('Need exactly 19 source guide layers from CP374')
    source_parts=[]
    for p in guides:
        layer=Image.open(p).convert('RGBA')
        if layer.size!=SOURCE_SIZE:raise ValueError('Invalid source guide size')
        source_parts.append((p.stem,layer))
    # Source-region guide must reassemble *exactly* to the CP374 alpha matte.
    source_merge=Image.new('RGBA',SOURCE_SIZE)
    for _,im in source_parts:source_merge.alpha_composite(im)
    if not np.array_equal(np.asarray(source_merge),np.asarray(matte)):
        # Invisible alpha RGB differences do not matter; compare color for visible pixels.
        a=np.asarray(source_merge);b=np.asarray(matte)
        valid=(a[:,:,3]>0)|(b[:,:,3]>0)
        if not np.array_equal(a[:,:,3],b[:,:,3]) or not np.array_equal(a[:,:,:3][valid],b[:,:,:3][valid]):
            raise ValueError('CP374 source guide does not reconstruct the referenced matte')
    output=Path(output)
    for d in ['source','svg','painted','ora','qa','guide_regions']:(output/d).mkdir(parents=True,exist_ok=True)
    front.save(output/'source'/'CANON_EXACT_FRONT_WITH_BACKGROUND_217x458.png')
    matte.save(output/'source'/'CP374_SOURCE_MATTE_PARTIAL_SHADOW_NOT_ART.png')
    (output/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png').write_bytes(Path(canon).read_bytes())
    # Independently authored geometry: not source pixels, not bitmap cutouts.
    art_layers=[]
    for name,_ in ART:
        source=svg_for(name)
        ET.fromstring(source)
        (output/'svg'/(name+'.svg')).write_text(source,encoding='utf-8')
        rendered=cairosvg.svg2png(bytestring=source.encode('utf8'),output_width=CANVAS[0],output_height=CANVAS[1])
        art=Image.open(io.BytesIO(rendered)).convert('RGBA')
        if not art.getchannel('A').getbbox():raise ValueError('Empty drafted art '+name)
        art.save(output/'painted'/(name+'.png'))
        art_layers.append((name,art))
    # Source trace guide has real original source RGB/alpha but no underpaint.
    for name,im in source_parts:im.save(output/'guide_regions'/(name+'.png'))
    exact_trace=create_ora(output/'ora'/'CP379_SOURCE_19_PARTS_NOT_RIG.ora',source_parts,front)
    guide_full=front.resize(CANVAS,Image.Resampling.NEAREST)
    vector_composite=create_ora(output/'ora'/'CP379_21_AUTHORED_FULLBODY_BLOCKING_DRAFT_NOT_RIG.ora',art_layers,guide_full)
    vector_composite.save(output/'qa'/'CP379_FULLBODY_VECTOR_BLOCKING_TRANSPARENT_NOT_APPROVED.png')
    # Compact CANON-only review, no unrelated faces/reference.
    board=Image.new('RGB',(1480,820),'#15243a'); pen=ImageDraw.Draw(board)
    fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    big=ImageFont.truetype(fontfile,22); font=ImageFont.truetype(fontfile,16)
    pen.text((22,14),'CP379 | LAM THIEN FULLBODY SEMANTIC BLOCKING — NOT APPROVED',font=big,fill='#eef5ff')
    pen.text((22,49),'Exact user CANON V2.1 / Source-trace reference / 21 NEW independent vector blockings',font=font,fill='#b8d2ef')
    # Four views preserve same character. Reference first, technical matte second, newly authored draft third.
    can=original.copy();can.thumbnail((395,685))
    board.paste(can.convert('RGB'),(24,90))
    src=front.resize((300,633),Image.Resampling.NEAREST).convert('RGB')
    board.paste(src,(440,110))
    # Show alpha draft against neutral white-ish checker. Fading alpha only in presentation.
    vsmall=vector_composite.resize((300,633),Image.Resampling.LANCZOS)
    bg=Image.new('RGBA',vsmall.size,'#e8eef6')
    pic=Image.alpha_composite(bg,vsmall)
    board.paste(pic.convert('RGB'),(795,110))
    # ANNOTATIONS: only derived from exact source Front (no other character).
    crop=front.crop((60,15,158,215)).resize((300,633),Image.Resampling.NEAREST)
    board.paste(crop.convert('RGB'),(1154,110))
    for x,label in ((24,'APPROVED CANON'),(440,'EXACT FRONT CROP'),(795,'NEW VECTOR DRAWING DRAFT'),(1154,'CANON DETAIL CROP')):
        pen.text((x,754),label,font=font,fill='white')
    pen.text((22,786),'NO FULL-BODY ART APPROVAL; source crop remains 217x458; vector canvas 1302x2748 is NOT painted high-detail production art.',font=font,fill='#ffcea0')
    board.save(output/'qa'/'CP379_CANON_FULLBODY_VECTOR_COMPARISON_NOT_APPROVED.png')
    # Reference toes: source-based check only, not animated draft verification.
    ref=np.asarray(front);m=np.asarray(matte)
    toes={'image_left':(79,432,102,458),'image_right':(109,414,122,446)}
    toereport={}
    for n,(x1,y1,x2,y2) in toes.items():
        src=ref[y1:y2,x1:x2];dest=m[y1:y2,x1:x2]
        rgb=src[:,:,:3].astype(np.float32)
        blue=(rgb[:,:,2]>rgb[:,:,0]*1.14)&(rgb[:,:,2]>rgb[:,:,1]*1.09)&(rgb[:,:,2]>90)&(src[:,:,3]>=128)
        total=int(blue.sum());kept=int((blue&(dest[:,:,3]>=128)).sum())
        toereport[n]={'blue_source_px':total,'blue_visible_px':kept,'pass':kept==total and total>20}
    report={
      'checkpoint':'CP379','canon_sha256':CANON_SHA,'canon_size':list(CANON_SIZE),
      'source_front_size':list(SOURCE_SIZE),'vector_canvas':list(CANVAS),
      'new_independent_svg_body_part_layers':len(ART),'original_rgb_source_guide_layers':len(source_parts),
      'vector_ora_layers':len(ART)+1,'trace_ora_layers':len(source_parts)+1,
      'source_trace_matches_cp374_matte_at_rest':True,'toe_source_checks':toereport,
      'art_status':'FULLBODY_GEOMETRY_COLOR_BLOCKING_ONLY','visual_qa':'NOT_PASSED',
      'true_native_painted_highdetail_fullbody':False,'semantic_hidden_underpaint_complete':False,
      'five_expressions_ready':False,'four_damage_states_ready':False,
      'motion_approved':False,'spine_ready':False,'apk_ready':False,
      'production_release':'blocked_pending_art','sprite_paths':{},
      'next':'CP380 painter quality work on full-body 21 semantic layers, underpaint, hairstyles, shoes; compare to CANON and seek approval.'}
    (output/'CP379_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--canon',required=True);p.add_argument('--matte',required=True)
    p.add_argument('--source-layers',required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    print(json.dumps(build(a.canon,a.matte,a.source_layers,a.out),ensure_ascii=False,indent=2))
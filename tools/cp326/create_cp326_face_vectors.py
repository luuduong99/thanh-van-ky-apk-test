#!/usr/bin/env python3
"""CP326 first independently-drawn facial-component prototype on CANON V2.

NOT a licensed/approved production sprite, NOT a source for rigging without review.
The face background is inpainted from the actual canon portrait; art overlays
are newly drawn vector shapes and contain no source-image pixels.
"""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np, cv2, cairosvg, io, json, hashlib, zipfile, xml.etree.ElementTree as ET

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--canon',type=Path,default=Path('/mnt/data/TVK_LamThien_CANON_BodyCostume_V2_20261028.png'))
parser.add_argument('--out',type=Path,default=Path('/mnt/data/TVK_LamThien_CP326_Independent_Face_Prototype'))
options=parser.parse_args()
SOURCE=options.canon
OUT=options.out;OUT.mkdir(parents=True,exist_ok=True)
SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXPR_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA

bbox=(1160,0,1390,114)
SCALE=4;WIDTH=230*SCALE;HEIGHT=114*SCALE
src=Image.open(SOURCE).convert('RGB').crop(bbox)
src.save(OUT/'SOURCE_CANON_FACE_NATIVE_230x114_REFERENCE_ONLY.png')

# Retouch a facebase to accommodate separable original *hand-drawn* expressions.
# This is a proof of concept; original 230px sample cannot become HD by upscaling.
arr=np.asarray(src)
mask=np.zeros((114,230),dtype=np.uint8)
for poly in [
    [(65,69),(72,61),(84,57),(102,59),(104,74),(91,81),(73,85)],
    [(132,48),(141,34),(158,31),(171,33),(171,53),(150,60),(137,61)],
    [(113,87),(125,84),(143,85),(143,98),(120,103)],
    [(70,48),(84,39),(105,36),(105,45),(82,56)],
    [(129,28),(141,20),(159,19),(164,27),(141,35)]
]:cv2.fillPoly(mask,[np.array(poly,np.int32)],255)
# Light inpainting does not magically restore hidden skin; treat only as temporary base.
base=cv2.inpaint(cv2.cvtColor(arr,cv2.COLOR_RGB2BGR),mask,5,cv2.INPAINT_TELEA)
base=cv2.cvtColor(base,cv2.COLOR_BGR2RGB)
base=Image.fromarray(base).resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
base.save(OUT/'BASE_CANON_FACE_INPAINT_PROTOTYPE.png')
Image.fromarray(mask).resize((WIDTH,HEIGHT),Image.Resampling.NEAREST).save(OUT/'BASE_UNDERPAINT_MASK_QA.png')
original=src.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS).convert('RGBA')

emotions=[
 ('shy','Ngại ngùng'),('angry','Tức giận'),('pain','Đau đớn'),
 ('embarrassed','Xấu hổ'),('alluring','Quyến rũ')]

# Local coordinate system is relative to source bbox. The eyes/eyebrows are
# intentionally oriented to the *actual slanted V2 face*, not a new face model.
eye_info={
    'image_left': {'start':(70,78),'mid':(84,67),'end':(99,61),'center':(86,69),'r':7.1},
    'image_right':{'start':(136,54),'mid':(149,41),'end':(164,35),'center':(153,45),'r':7.6}
}


def svg_render(svg):
    png=cairosvg.svg2png(bytestring=svg.encode('utf-8'),output_width=WIDTH,output_height=HEIGHT)
    return Image.open(io.BytesIO(png)).convert('RGBA')

def wrap(inner):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="230" height="114" viewBox="0 0 230 114">
    <defs>
      <radialGradient id="iris" cx="48%" cy="65%"><stop offset="0%" stop-color="#F7C987"/>
      <stop offset="45%" stop-color="#D69A55"/><stop offset="84%" stop-color="#AF6B60"/>
      <stop offset="100%" stop-color="#64495F"/></radialGradient>
      <linearGradient id="lip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#AF6472"/>
      <stop offset="1" stop-color="#E8A6A8"/></linearGradient>
    </defs>{inner}</svg>'''


def eye_layer(side,emotion):
    e=eye_info[side];a=e['start'];m=e['mid'];z=e['end'];cx,cy=e['center']
    depression={'shy':0.66,'angry':0.68,'pain':0.11,'embarrassed':0.20,'alluring':0.46}[emotion]
    # eye upper line: intentionally different shapes while keeping exact V2 anchors
    up=f'M {a[0]} {a[1]} Q {m[0]} {m[1]-8*depression:.1f} {z[0]} {z[1]}'
    if emotion=='angry':up=f'M {a[0]} {a[1]-2} Q {m[0]} {m[1]-1} {z[0]} {z[1]+3}'
    if emotion=='embarrassed':up=f'M {a[0]} {a[1]-2} Q {m[0]} {m[1]+1} {z[0]} {z[1]+2}'
    if emotion=='pain':up=f'M {a[0]} {a[1]-2} Q {m[0]} {m[1]+1} {z[0]} {z[1]+1}'
    thick={'shy':1.9,'angry':2.8,'pain':1.8,'embarrassed':1.6,'alluring':2.4}[emotion]
    content=f'<path d="{up}" fill="none" stroke="#4B303E" stroke-width="{thick}" stroke-linecap="round"/>'
    if emotion in ('pain','embarrassed'):
        content+=f'<path d="M {a[0]+4} {a[1]+1} Q {m[0]} {m[1]+5} {z[0]-3} {z[1]+3}" fill="none" stroke="#9A6874" stroke-width="0.7" opacity=".55"/>'
        if emotion=='pain':
            content+=f'<path d="M {a[0]+4} {a[1]+4} q -1 3 -1 6" fill="none" stroke="#A1DCEB" stroke-width="1.5" opacity=".75"/>'
    else:
        cy_adj=cy + (3 if emotion=='alluring' else 1 if emotion=='angry' else 2)
        rx=e['r']*0.87
        ry={'shy':5.7,'angry':4.7,'alluring':3.5}[emotion]
        # white sclera, iris, pupils and highlights are independently rendered
        content+=f'<ellipse cx="{cx}" cy="{cy_adj}" rx="{rx+3}" ry="{ry+1.5}" fill="#F9EDEF" opacity=".92"/>'
        content+=f'<ellipse cx="{cx}" cy="{cy_adj}" rx="{rx}" ry="{ry}" fill="url(#iris)" stroke="#6D5367" stroke-width=".6"/>'
        content+=f'<ellipse cx="{cx+0.6}" cy="{cy_adj-0.4}" rx="{rx*.34}" ry="{ry*.67}" fill="#47394B"/>'
        content+=f'<ellipse cx="{cx-2.0}" cy="{cy_adj-2.1}" rx="1.6" ry="1.4" fill="#FFFFFF" opacity=".96"/>'
        content+=f'<ellipse cx="{cx+1.6}" cy="{cy_adj+1.6}" rx="1.1" ry=".65" fill="#F8EDDC" opacity=".78"/>'
        content+=f'<path d="{up}" fill="none" stroke="#4B303E" stroke-width="{thick}" stroke-linecap="round"/>'
    content+=f'<path d="M {z[0]-2} {z[1]+1} l 2 -2 M {z[0]-5} {z[1]+1} l 0 -2" fill="none" stroke="#604552" stroke-width=".9"/>'
    if emotion=='angry': content+=f'<path d="M {a[0]+5} {a[1]+5} Q {cx} {cy+10} {z[0]-2} {z[1]+8}" fill="none" stroke="#725563" stroke-width=".7"/>'
    return svg_render(wrap(content))


def brow_layer(side, emotion):
    if side=='image_left':p=(72,50,86,40,103,40)
    else:p=(131,29,145,22,160,24)
    x1,y1,xc,yc,x2,y2=p
    if emotion=='angry':
        if side=='image_left':p=(72,45,90,46,103,52)
        else:p=(131,34,147,25,158,21)
    if emotion=='pain':
        if side=='image_left':p=(72,48,89,36,104,42)
        else:p=(131,28,144,15,158,24)
    if emotion=='embarrassed':
        if side=='image_left':p=(72,51,86,40,102,42)
        else:p=(131,32,145,21,159,24)
    if emotion=='alluring':
        if side=='image_left':p=(73,49,87,43,101,43)
        else:p=(132,30,146,27,160,27)
    x1,y1,xc,yc,x2,y2=p
    d=f'M{x1} {y1} Q {xc} {yc} {x2} {y2}'
    return svg_render(wrap(f'<path d="{d}" stroke="#977781" stroke-width="1.65" fill="none" opacity=".78" stroke-linecap="round"/>'))


def mouth_layer(emotion):
    variants={
    'shy':'<path d="M120 91 Q128 88 136 89 Q132 95 125 95 Q122 94 120 91" fill="url(#lip)" stroke="#9F6573" stroke-width=".7"/>',
    'angry':'<path d="M119 91 L137 88 Q132 93 126 93 L120 92" fill="#8C5966" stroke="#77505F" stroke-width=".7"/>',
    'pain':'<path d="M123 86 Q132 84 138 90 Q137 98 131 98 Q123 96 123 86" fill="#AE697A" stroke="#9C5D69" stroke-width=".85"/><path d="M125 87 Q133 87 137 91" stroke="#F9D8D0" fill="none" stroke-width="1"/>',
    'embarrassed':'<path d="M122 93 Q129 89 135 91" stroke="#AB6F77" stroke-width="1.4" fill="none" stroke-linecap="round"/><path d="M125 94 Q131 96 134 92" stroke="#E6AAA9" fill="none" stroke-width=".8"/>',
    'alluring':'<path d="M120 91 Q129 95 139 87 Q134 97 125 96 Q121 95 120 91" fill="url(#lip)" stroke="#A46971" stroke-width=".85"/><path d="M122 92 Q129 94 138 88" stroke="#F8DDCE" fill="none" stroke-width=".8"/>'}
    return svg_render(wrap(variants[emotion]))


def blush_layer(side,emotion):
    peak={'shy':.15,'angry':.035,'pain':.07,'embarrassed':.24,'alluring':.075}[emotion]
    if side=='image_left':cx,cy,rx,ry=93,85,23,10
    else:cx,cy,rx,ry=164,73,17,13
    xx,yy=np.meshgrid(np.arange(WIDTH)/SCALE,np.arange(HEIGHT)/SCALE)
    dist=((xx-cx)/rx)**2+((yy-cy)/ry)**2
    alpha=(np.exp(-3*dist)*peak*255).astype(np.uint8)
    rgba=np.empty((HEIGHT,WIDTH,4),dtype=np.uint8);rgba[:,:,:3]=[225,95,110];rgba[:,:,3]=alpha
    return Image.fromarray(rgba,'RGBA')

layer_names=['blush_image_left','blush_image_right','eye_image_left','eye_image_right','brow_image_left','brow_image_right','mouth']
manifest={
 'schema_version':1,'checkpoint':'CP326','date':'2026-10-29',
 'status':'new_vector_facial_parts_on_canon_v2_inpaint_prototype_not_approved_for_game',
 'canonical_body_visual_id':'LT_CANON_BODY_REF_2026-10-28_V2',
 'canonical_body_sha256':SHA,'approved_five_expression_sheet_sha256':EXPR_SHA,
 'source_bbox_xyxy':list(bbox),'native_source_size_px':[230,114],
 'rendered_canvas_px':[WIDTH,HEIGHT],'enlargement_factor':SCALE,
 'caveats':['Canon face crop is only 230x114 at native resolution',
            'Underpaint is algorithmic inpainting, not artist-approved hidden anatomy',
            'Eyes/brows/mouth are independently drawn SVG vector strokes but not approved for appearance accuracy',
            'Do NOT register these layers as game sprites or set P1-03 production done'],
 'art_mode':'independent_alpha_vector_render_with_source_canon_guide',
 'independent_pixel_layer_count_expected':35,
 'expression_ids':[x for x,_ in emotions],
 'items':[], 'production_ready':False,'spine_ready':False,'apk_ready':False,
 'asset_registration_allowed':False
}

font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
try:ft=ImageFont.truetype(font,22);ft_sm=ImageFont.truetype(font,14)
except:ft=None;ft_sm=None
contact=Image.new('RGB',(5*450+50,660),(19,34,50));d=ImageDraw.Draw(contact)
for idx,(emotion,name) in enumerate(emotions):
    layer_map={
       'blush_image_left':blush_layer('image_left',emotion),
       'blush_image_right':blush_layer('image_right',emotion),
       'eye_image_left':eye_layer('image_left',emotion),
       'eye_image_right':eye_layer('image_right',emotion),
       'brow_image_left':brow_layer('image_left',emotion),
       'brow_image_right':brow_layer('image_right',emotion),
       'mouth':mouth_layer(emotion)
    }
    merged=base.convert('RGBA')
    for nm in layer_names:merged=Image.alpha_composite(merged,layer_map[nm])
    merged.save(OUT/f'{idx+1:02}_{emotion}_CANON_V2_FACE_COMPOSITE_TECH_DEMO.png')
    # Build OpenRaster where every art layer is independent & visible, base is an
    # inpainted canon face (provisional); the original unmodified source is hidden.
    ora=OUT/f'CP326_{idx+1:02}_{emotion}_VECTOR_FACE_LAYERS_PROTOTYPE.ora'
    root=ET.Element('image',{'w':str(WIDTH),'h':str(HEIGHT),'name':'CP326 '+emotion+' (TECH DEMO)'})
    stack=ET.SubElement(root,'stack')
    o_layers=[(nm,layer_map[nm],True) for nm in reversed(layer_names)]
    o_layers.append(('BASE_UNDERPAINT_AUTO_NOT_APPROVED',base.convert('RGBA'),True))
    o_layers.append(('GUIDE_CANON_V2_ORIGINAL_REFERENCE_ONLY',original,False))
    with zipfile.ZipFile(ora,'w',compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for k,(nm,img,visible) in enumerate(o_layers):
            io_obj=io.BytesIO();img.save(io_obj,format='PNG')
            p=f'data/layer{k:02}.png';z.writestr(p,io_obj.getvalue())
            ET.SubElement(stack,'layer',{'name':nm,'src':p,'x':'0','y':'0','opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over'})
        data=io.BytesIO();merged.save(data,format='PNG');z.writestr('mergedimage.png',data.getvalue())
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    good=0; parts={}
    for nm,img in layer_map.items():
        alpha=np.asarray(img.getchannel('A'))
        pixels=int(np.count_nonzero(alpha))
        parts[nm]={'alpha_nonzero_pixels':pixels,'rgba_mode':img.mode,'native_source_pixels_used':False}
        assert pixels>0,nm
        good+=1
    manifest['items'].append({'id':emotion,'name_vi':name,'ora_file':ora.name,'ora_sha256':hashlib.sha256(ora.read_bytes()).hexdigest(),
      'canvas_px':[WIDTH,HEIGHT],'source_image_native_px':[230,114], 'alpha_independent_layers':good,'parts':parts,
      'underpaint_status':'algorithmic_placeholder','guide_status':'original_canon_source_hidden',
      'preview_file':f'{idx+1:02}_{emotion}_CANON_V2_FACE_COMPOSITE_TECH_DEMO.png'})
    # Contact sheet previews original + new expression base cropped to readable area.
    x=20+idx*450
    panel=merged.crop((185,35,725,440)).resize((405,304),Image.Resampling.LANCZOS)
    contact.paste(panel.convert('RGB'),(x,150))
    d.text((x,50),f'{idx+1:02} {emotion.upper()}',font=ft,fill=(240,229,215))
    d.text((x,88),name,font=ft_sm,fill=(180,202,228))
    d.text((x,485),'CANON V2 face + independent vector parts',font=ft_sm,fill=(191,201,214))
    d.text((x,516),'TECH DEMO ONLY - NOT APPROVED FOR GAME',font=ft_sm,fill=(255,192,155))
    d.rounded_rectangle([x-7,36,x+410,555],radius=8,outline=(95,137,180),width=2)
manifest['created_files']=len(list(OUT.glob('*.ora')))
contact.save(OUT/'CP326_FIVE_FACE_COMPOSITES_TECH_DEMO.png')
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(OUT/'README.md').write_text('''# CP326 — independent facial vector component technical prototype

Source: exact body CANON V2 image SHA256 41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711.
Approved emotions: shy / angry / pain / embarrassed / alluring, style reference SHA256 ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7.

Each of five ORAs contains seven **new vector-drawn** transparent facial elements: eyebrow left/right, eye left/right, mouth and blush left/right. The background face is cropped from the original CANON V2 and the former features are algorithmically inpainted. Original unmodified CANON face is hidden as a guide. This differs from CP325's flattened-image feather patches: these new layers do not contain skin or hair pixels.

**Do not approve for production.** The actual face crop is 230x114; 4x rendered pixels are an enlargement, not new source detail. The clean facebase has automatic inpaint artifacts. Facial features are technical artwork, not matching the approved five expressions with production quality. We need a high-resolution new 2D art pass preserving V2 and explicit visual QA before Spine attachments.

QA gate: verify independent alpha layers, never silently declare ready, preserve V2 source, preview proper expressions at native/132/64px; do NOT register them as `sprite_paths` or use in APK.
''',encoding='utf-8')
zip_path=OUT.parent/'TVK_LamThien_CP326_Vector_Face_Prototype_NOT_GAME_READY.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for file in OUT.iterdir():
        if file.is_file():z.write(file,arcname=file.name)
print('ZIP',zip_path,zip_path.stat().st_size,'SHA',hashlib.sha256(zip_path.read_bytes()).hexdigest())
print('CONTACT',OUT/'CP326_FIVE_FACE_COMPOSITES_TECH_DEMO.png')
print('ORA_COUNT',len(list(OUT.glob('*.ora'))),'PARTS',sum(x['alpha_independent_layers'] for x in manifest['items']))
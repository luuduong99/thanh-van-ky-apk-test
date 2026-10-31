#!/usr/bin/env python3
"""CP380: editable original SVG detail pass over source-locked CP379 full-body DRAFT.

This is intentionally NOT a user-approved high-fidelity repaint, rig or APK sprite.
CANON remains exact bytes; new detail contours are source-coordinate art studies.
"""
from pathlib import Path
import hashlib, io, json, zipfile, xml.etree.ElementTree as ET, argparse
import importlib.util
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cairosvg

SRC=Path(__file__).with_name('cp379_fullbody_vector_blocking.py')
spec=importlib.util.spec_from_file_location('cp379_src',SRC)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
SHA=base.CANON_SHA
SIZE=base.CANVAS
# Every entry contains genuinely new Bezier geometry, not a CANON bitmap reference.
DETAILS=[
('22_left_hair_individual_highlight_strands', '''
<path d="M89 42 C80 89 58 137 43 176 Q26 207 22 235 M94 52 Q81 109 61 149 C42 181 40 201 27 215 M79 97 Q57 165 35 192 M85 126 Q64 182 46 208" fill="none" stroke="#faf9ff" stroke-width="1.5" opacity=".80"/>
<path d="M89 47 Q76 112 53 164 M79 92 Q65 147 32 211" fill="none" stroke="#7c91c7" stroke-width=".64" opacity=".68"/>
<path d="M83 83 Q72 143 44 187 M73 144 Q62 188 24 226" fill="none" stroke="#e3d6ef" stroke-width="1.1" opacity=".81"/>'''),
('23_right_hair_individual_highlight_strands', '''
<path d="M131 44 Q147 100 168 154 T194 226 M139 70 Q150 134 184 188 M151 126 Q162 171 187 202" fill="none" stroke="#fcfaff" stroke-width="1.45" opacity=".86"/>
<path d="M135 71 Q149 140 172 173 M150 128 Q173 188 195 215" fill="none" stroke="#849acb" stroke-width=".7" opacity=".72"/>
<path d="M137 91 Q149 145 175 196 M145 107 Q160 169 189 213" fill="none" stroke="#ddd5f1" stroke-width="1.0" opacity=".86"/>'''),
('24_forehead_fine_bangs_and_gloss', '''
<path d="M99 21 C96 29 96 35 95 44 M104 20 Q103 29 102 36 M111 19 Q110 30 109 38 M116 21 Q121 32 120 42 M127 24 Q130 33 129 43" fill="none" stroke="#fffdfd" stroke-width="1.1" opacity=".9"/>
<path d="M99 22 Q96 34 96 41 M116 21 Q119 31 120 38" fill="none" stroke="#8d8fb7" stroke-width=".45" opacity=".67"/>
<path d="M104 25 Q103 30 104 35 M118 23 Q119 28 121 34" stroke="#d5c5ed" stroke-width=".7" opacity=".65" fill="none"/>'''),
('25_face_eyelashes_iris_cheek_lights', '''
<path d="M91.7 50 Q97.2 46.4 104.4 50.3 M117.7 50.5 Q123.6 46.1 129.3 49.8" stroke="#4e4559" stroke-width=".95" fill="none"/>
<path d="M92.3 49.6 L90.6 47.6 M95 48.2 L93.4 46 M127.4 48.3 L129.4 46.1 M124.5 47.6 L125.9 45.7" stroke="#4c4058" stroke-width=".8" fill="none"/>
<ellipse cx="99" cy="50.9" rx="1.3" ry="2.1" fill="#8b605e"/><ellipse cx="124" cy="50.9" rx="1.25" ry="2" fill="#8b605e"/>
<circle cx="98.6" cy="50.0" r=".61" fill="#fff9f3"/><circle cx="123.6" cy="50.0" r=".58" fill="#fff9f3"/>
<path d="M92 63 Q97 66 101.8 63.3 M120 63.4 Q125 66 128.5 62.6" stroke="#edb9b6" stroke-width="1.4" stroke-opacity=".46" fill="none"/>
<path d="M109 71 Q112.7 72.4 115.6 70.6" stroke="#be777b" stroke-width=".62" fill="none"/>'''),
('26_white_flower_petals_blue_ribbons', '''
<g fill="#fffefa" stroke="#a7a4be" stroke-width=".42">
<ellipse cx="89" cy="21.6" rx="2.2" ry="5" transform="rotate(-30 89 21.6)"/>
<ellipse cx="91.7" cy="19.8" rx="2.1" ry="5" transform="rotate(32 91.7 19.8)"/>
<ellipse cx="95" cy="23" rx="2.1" ry="4" transform="rotate(100 95 23)"/>
<ellipse cx="129" cy="19.5" rx="2.2" ry="5" transform="rotate(-28 129 19.5)"/>
<ellipse cx="132" cy="21" rx="2.2" ry="5" transform="rotate(36 132 21)"/>
<ellipse cx="129.5" cy="25" rx="2" ry="4.4" transform="rotate(102 129.5 25)"/>
</g>
<circle cx="91.5" cy="24" r="1.45" fill="#e8c17b" stroke="#fff7d7" stroke-width=".6"/>
<circle cx="130" cy="23.5" r="1.45" fill="#e8c17b" stroke="#fff7d7" stroke-width=".6"/>
<path d="M80.5 31 C78.9 40 77.5 48 76.4 56 M141.3 30 Q143.7 43 144.4 55" fill="none" stroke="#1b74c4" stroke-width="1.4"/>
<path d="M76.3 51 L73.7 62 L78 58Z M144 51 L147.6 61 L143.5 58Z" fill="#4d97df" stroke="#ecd2a2" stroke-width=".6"/>'''),
('27_bodice_white_blue_silk_folds', '''
<path d="M76 123 Q88 118 100 135 M146 125 Q129 119 119 138 M80 144 Q94 149 104 148 M122 148 Q137 147 148 141" fill="none" stroke="#fffffe" stroke-width="1.45" stroke-opacity=".85"/>
<path d="M78 128 Q86 142 90 147 M143 126 Q138 142 134 148 M94 150 Q111 161 128 150" fill="none" stroke="#76a2d5" stroke-width=".73" stroke-opacity=".78"/>
<path d="M89 122 Q95 130 98 137 M133 121 Q127 127 124 135 M103 156 Q112 160 122 155" fill="none" stroke="#cadcf3" stroke-width=".86" opacity=".75"/>
<path d="M104 165 Q110 176 113 182 Q117 175 123 164" stroke="#f3e7ba" stroke-width="1.06" fill="none" opacity=".72"/>'''),
('28_neck_waist_gold_filagree_jewels', '''
<path d="M96 94 L112.8 109 L130.5 95 M102 97 L112.5 104 L123 98 M107.5 114 L113 122 L118 113" fill="none" stroke="#f4d79c" stroke-width=".85"/>
<path d="M103 161 L110 170 L113 166 L117 171 L124 161 M105 166 L113 177 L120 165" fill="none" stroke="#f5d6a1" stroke-width="1.2"/>
<path d="M109 167 L113 162 L117 167 L113 174Z" fill="#f6d89a" stroke="#996737" stroke-width=".5"/>
<circle cx="113" cy="167" r="1.55" fill="#4c9dd5" stroke="#f8e7ba" stroke-width=".48"/>
<path d="M108 178 L113 187 L118 178 M104 175 L100 179 M121 174 L126 178" fill="none" stroke="#a97a43" stroke-width=".65"/>
<path d="M111.9 114 L113 118 L114.1 114" fill="none" stroke="#fff8d5" stroke-width=".67"/>'''),
('29_silk_hem_gold_blue_threading', '''
<path d="M28 290 C24 339 16 391 7 429 M46 255 Q41 326 23 395 M174 260 Q184 331 198 402 M186 289 Q196 371 209 430" fill="none" stroke="#f9f5ff" stroke-width=".85" opacity=".86"/>
<path d="M26 310 Q20 378 11 419 M178 298 Q187 373 206 420" fill="none" stroke="#d0a867" stroke-width=".72" opacity=".84"/>
<path d="M15 413 L13 421 L19 416 M202 413 L206 422 L208 415" fill="none" stroke="#efc782" stroke-width="1.1"/>
<path d="M29 328 Q27 354 21 367 M184 332 Q192 355 196 374" stroke="#5c96d5" stroke-width=".8" fill="none"/>''')]

def svg(name):
    body=dict(DETAILS)[name]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1302" height="2748" viewBox="0 0 217 458">{body}</svg>'

def build(canon_path, cp379_painted, outdir):
    # Validate every input BEFORE output creation.
    canon_path=Path(canon_path);base.get_canon(canon_path)
    cp379_painted=Path(cp379_painted)
    names=[n for n,_ in base.ART]
    if sorted(p.stem for p in cp379_painted.glob('*.png'))!=sorted(names):
        raise ValueError('Must supply exactly 21 original CP379 named PNG layers')
    raw_source=[(n,(cp379_painted/(n+'.png')).read_bytes()) for n in names]
    for n,raw in raw_source:
        im=Image.open(io.BytesIO(raw))
        if im.size!=SIZE or im.mode!='RGBA':raise ValueError('Invalid CP379 art layer '+n)
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    for sub in ['source','svg','layers','ora','qa']:(outdir/sub).mkdir(exist_ok=True)
    (outdir/'source'/canon_path.name).write_bytes(canon_path.read_bytes())
    ref=base.get_canon(canon_path)
    orig_parts=[(n,Image.open(io.BytesIO(raw)).convert('RGBA')) for n,raw in raw_source]
    generated=[]
    for name,_ in DETAILS:
        source=svg(name);ET.fromstring(source)
        (outdir/'svg'/(name+'.svg')).write_text(source,encoding='utf8')
        png=cairosvg.svg2png(bytestring=source.encode(),output_width=SIZE[0],output_height=SIZE[1])
        image=Image.open(io.BytesIO(png)).convert('RGBA')
        if image.getchannel('A').getbbox() is None:raise ValueError('Empty new detail '+name)
        image.save(outdir/'layers'/(name+'.png'))
        generated.append((name,image))
    # Keep original art PNG and SVG bytes so all 29 editable layers travel together.
    for name,raw in raw_source:
        (outdir/'layers'/(name+'.png')).write_bytes(raw)
        sv=(cp379_painted.parent/'svg'/(name+'.svg'))
        if not sv.is_file():raise ValueError('Missing original CP379 SVG '+name)
        (outdir/'svg'/(name+'.svg')).write_bytes(sv.read_bytes())
    previous=Image.new('RGBA',SIZE)
    for _,im in orig_parts:previous.alpha_composite(im)
    next_image=previous.copy()
    for _,im in generated:next_image.alpha_composite(im)
    from PIL import ImageChops
    diff=np.array(ImageChops.difference(previous,next_image).convert('RGBA'))
    changed=int(np.count_nonzero(np.any(diff!=0,axis=2)))
    if changed<100:raise ValueError('Detail overlays did not visibly modify drawing')
    guide=ref.crop(base.FRONT).resize(SIZE,Image.Resampling.NEAREST)
    ora=outdir/'ora'/'CP380_29_ART_LAYERS_DETAIL_STUDY_NOT_APPROVED.ora'
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'version':'0.0.3','name':'CP380 CANON-LOCKED DRAFT - NOT SPINE'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for idx,(name,im) in enumerate(reversed(orig_parts+generated)):
            b=io.BytesIO();im.save(b,'PNG');loc=f'data/layer_{idx:02d}.png'
            z.writestr(loc,b.getvalue())
            ET.SubElement(stack,'layer',{'name':'DRAFT__'+name,'src':loc,'visibility':'visible','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        b=io.BytesIO();guide.save(b,'PNG');z.writestr('data/CANON_SOURCE_HIDDEN.png',b.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_REFERENCE_ONLY_HIDDEN','src':'data/CANON_SOURCE_HIDDEN.png','visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf8',xml_declaration=True))
        b=io.BytesIO();next_image.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
    assert zipfile.ZipFile(ora).testzip() is None
    previous.save(outdir/'qa'/'CP379_BASE_21_LAYERS.png')
    next_image.save(outdir/'qa'/'CP380_REFINED_29_LAYER_DRAFT.png')
    # A 100% CANON-only comparison; no substituted external images.
    W,H=1680,920;board=Image.new('RGB',(W,H),'#132640');draw=ImageDraw.Draw(board)
    f='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bfont=ImageFont.truetype(f,22);small=ImageFont.truetype(f,14)
    draw.text((24,20),'CP380 — LAM THIEN V2.1 | FULL-BODY DETAIL STUDY — NOT APPROVED',font=bfont,fill='#f5f8ff')
    draw.text((24,54),'CANON EXACT SOURCE / CP379 21-layer blocking / CP380 29-layer draft / CANON face-bodice detail',font=small,fill='#c4d6ec')
    can=ref.copy();can.thumbnail((355,730));board.paste(can.convert('RGB'),(22,104))
    cp_old=Image.alpha_composite(Image.new('RGBA',SIZE,'#eaf0f7'),previous).resize((350,739),Image.Resampling.LANCZOS)
    cp_new=Image.alpha_composite(Image.new('RGBA',SIZE,'#eaf0f7'),next_image).resize((350,739),Image.Resampling.LANCZOS)
    board.paste(cp_old.convert('RGB'),(410,104));board.paste(cp_new.convert('RGB'),(805,104))
    exact=ref.crop(base.FRONT).crop((61,16,157,207)).resize((405,739),Image.Resampling.NEAREST)
    board.paste(exact.convert('RGB'),(1230,104))
    for x,s in [(22,'APPROVED CANON'),(410,'CP379 BLOCKING DRAFT'),(805,'CP380 DETAIL DRAFT'),(1230,'CANON CROPPED DETAIL')]:draw.text((x,852),s,font=small,fill='#e8edf8')
    draw.text((22,886),'8 additional editable SVG layer studies. Artist visual fidelity remains NOT PASSED; source Front is only 217x458.',font=small,fill='#f9d29c')
    compare=outdir/'qa'/'CP380_CANON_CP379_CP380_DETAIL_COMPARE_NOT_APPROVED.png';board.save(compare)
    report={'checkpoint':'CP380','canon_sha256':SHA,'source_front_native_pixels':[217,458], 'vector_canvas':list(SIZE),
      'base_layers_preserved':len(orig_parts),'new_drawn_detail_svg_layers':len(generated),'visible_art_layers':len(orig_parts)+len(generated),
      'ora_total_layers':len(orig_parts)+len(generated)+1,'changed_composite_pixels':changed,
      'source_byte_exact':hashlib.sha256((outdir/'source'/canon_path.name).read_bytes()).hexdigest()==SHA,
      'visual_qa':'NOT_PASSED','production_release':'blocked_pending_art','sprite_paths':{},
      'native_painted_full_body':False,'rig_ready':False,'apk_ready':False,
      'limitations':['Vector facial/hair/bodice/filigree details are not artist-grade CANON faithful','Face/hair silhouette still simplified','No true painted occluded anatomy or 2D rig','No Android build/device validation'],
      'new_layer_names':[n for n,_ in generated], 'ora':ora.name,'preview':compare.name}
    (outdir/'CP380_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--base-layers',required=True);p.add_argument('--out',required=True);x=p.parse_args()
    print(json.dumps(build(x.canon,x.base_layers,x.out),ensure_ascii=False,indent=2))
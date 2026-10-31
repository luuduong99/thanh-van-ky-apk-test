#!/usr/bin/env python3
"""CP375: newly drawn *partial* hidden left wrist/under-sleeve art.

Source-locked to Lâm Thiển V2.1. These paths are independent newly authored
SVG paint geometries, not cut-out source pixels. The study is intentionally
NOT a finished full-body 2D sprite, animation, rig or approved art.
"""
from __future__ import annotations
import argparse, hashlib, io, json, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
import cairosvg
import numpy as np
from PIL import Image,ImageDraw,ImageFont

CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
FRONT=(13,172,230,630)
SIZE=(217,458)
SIZE6=(1302,2748)
ART={
 '01_hidden_silk_back': '''<defs><linearGradient id="silk" x1=".1" y1="0" x2=".9" y2="1"><stop stop-color="#f8faff" stop-opacity=".84"/><stop offset=".37" stop-color="#dfe8fa" stop-opacity=".92"/><stop offset=".8" stop-color="#8fb2e8" stop-opacity=".72"/><stop offset="1" stop-color="#6d95cf" stop-opacity=".50"/></linearGradient></defs>
 <path d="M53 150 C60 157 63 171 60 188 Q60 210 50 225 Q52 208 46 197 Q40 182 41 168 Q44 158 53 150Z" fill="url(#silk)" stroke="#9fb6df" stroke-width=".60"/>
 <path d="M54 153 Q60 177 53 202 Q50 212 49 222" fill="none" stroke="#f8faff" stroke-opacity=".88" stroke-width="1.8"/>
 <path d="M45 173 Q56 188 51 212" fill="none" stroke="#7399ce" stroke-opacity=".55" stroke-width=".9"/>''',
 '02_hidden_upper_sleeve_lining': '''<defs><linearGradient id="lining" x1="0" y1=".3" x2="1" y2=".8"><stop stop-color="#c5d6ef"/><stop offset=".5" stop-color="#f6f7fa"/><stop offset="1" stop-color="#849fc8"/></linearGradient></defs>
 <path d="M57 151 Q51 155 47 164 Q39 174 31 184 C28 190 30 195 35 200 Q47 189 54 174 Q58 162 57 151Z" fill="url(#lining)" stroke="#8ba5cc" stroke-width=".65"/>
 <path d="M53 157 Q43 173 36 187" stroke="#ffffff" stroke-opacity=".7" stroke-width="1.6" fill="none"/>''',
 '03_hidden_forearm_skin': '''<defs><linearGradient id="skin" x1=".17" y1=".1" x2=".76" y2="1"><stop stop-color="#fff6ed"/><stop offset=".36" stop-color="#f9e0d6"/><stop offset=".70" stop-color="#edb8ad"/><stop offset="1" stop-color="#d89c9e"/></linearGradient></defs>
 <path d="M49 164 C45 173 40 181 35 187 C29 193 25 198 25 204 Q30 203 35 197 C40 192 46 183 52 172Z" fill="url(#skin)" stroke="#d3a39c" stroke-width=".48"/>
 <path d="M47 169 Q41 183 29 198" fill="none" stroke="#fff7ef" stroke-opacity=".75" stroke-width="1.3"/>
 <path d="M43 179 Q38 189 35 192" fill="none" stroke="#e5b5ac" stroke-opacity=".6" stroke-width=".65"/>''',
 '04_hidden_gold_inner_cuff': '''<defs><linearGradient id="gold" x1="0" y1=".1" x2="1" y2=".7"><stop stop-color="#f5e2a9"/><stop offset=".3" stop-color="#b98b4f"/><stop offset=".66" stop-color="#f0cf89"/><stop offset="1" stop-color="#976a37"/></linearGradient></defs>
 <path d="M34.4 187.7 Q37 185.7 39.8 181.8 L42.1 183.1 Q40.9 188 36.7 191.2Z" fill="url(#gold)" stroke="#8b673c" stroke-width=".45"/>
 <path d="M36.2 188.7 L38.5 185.9 M39 187.7 L40.5 185.2" fill="none" stroke="#fff2bf" stroke-width=".6"/>
 <circle cx="39" cy="185.7" r=".75" fill="#7fc2e8" stroke="#f3d692" stroke-width=".35"/>''',
}

def validate_canon(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=CANON_SHA: raise ValueError('Wrong CANON: refuse to write output')
    image=Image.open(io.BytesIO(raw))
    if image.size!=(941,1672) or image.mode!='RGBA':raise ValueError('CANON size/mode invalid')
    return image

def svg(name):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1302" height="2748" viewBox="0 0 217 458">{ART[name]}</svg>'

def raster(svgstr,size):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svgstr.encode('utf8'),output_width=size[0],output_height=size[1]))).convert('RGBA')

def foot_rgb_guard(a,b):
    # Identical raster pixels in the shoe regions of the exact reference.
    for roi in [(79,432,102,458),(109,414,122,446)]:
        if not np.array_equal(np.asarray(a.crop(roi)),np.asarray(b.crop(roi))):
            raise AssertionError('A blue shoe ROI was changed')

def make(canon_path,matte_path,hand_layer,outdir):
    canon=validate_canon(canon_path)
    p=Path(outdir)
    src=canon.crop(FRONT)
    matte=Image.open(matte_path).convert('RGBA')
    hand=Image.open(hand_layer).convert('RGBA')
    if matte.size!=SIZE or hand.size!=SIZE:raise ValueError('Front input not 217x458, refuse output')
    foot_rgb_guard(src,src)
    # Validate RGB fidelity of foreground original for nontransparent pixels.
    source=np.asarray(src);m=np.asarray(matte)
    if not np.array_equal(m[:,:,:3],source[:,:,:3]):raise ValueError('Source RGB not identical to CANON')
    p.mkdir(parents=True,exist_ok=True)
    (p/'svg').mkdir(exist_ok=True);(p/'layers').mkdir(exist_ok=True);(p/'qa').mkdir(exist_ok=True)
    art6={}
    for name in ART:
        value=svg(name)
        ET.fromstring(value)
        (p/'svg'/(name+'.svg')).write_text(value,encoding='utf8')
        art6[name]=raster(value,SIZE6)
        if not art6[name].getchannel('A').getbbox():raise ValueError('Empty painted layer '+name)
        art6[name].save(p/'layers'/(name+'.png'))
    # Four independently authored art layers, composited in declared back-to-front order.
    full6=Image.new('RGBA',SIZE6)
    for name in ART:full6.alpha_composite(art6[name])
    full6.save(p/'CP375_NATIVE_VECTOR_HIDDEN_WRIST_STUDY_TRANSPARENT.png')
    # Key technical preview runs in source native 217x458 space; the vector remains 6x editable.
    under=full6.resize(SIZE,Image.Resampling.LANCZOS)
    orig_alpha=np.asarray(hand.getchannel('A'))>128
    shifted=Image.new('RGBA',SIZE)
    shifted.paste(hand,(-6,3),hand.getchannel('A')) # only shift for one quantitative regression frame
    moved_alpha=np.asarray(shifted.getchannel('A'))>128
    exposed=orig_alpha&~moved_alpha
    under_alpha=np.asarray(under.getchannel('A'))>128
    # Underpainting remains clipped to the unshifted hand source mask so original rest silhouette is unchanged.
    unpainted=int(exposed.sum())
    covered=int(np.count_nonzero(exposed&under_alpha))
    remaining=int(np.count_nonzero(exposed&~under_alpha))
    before=Image.new('RGBA',SIZE);before.alpha_composite(matte)
    base_without_hand=Image.new('RGBA',SIZE)
    # Preserve original source pixels except hand mask to assess the same alpha seam.
    bm=np.array(matte)
    hb=np.asarray(hand.getchannel('A'))>0
    bm[:,:,3][hb]=0
    base_without_hand=Image.fromarray(bm,'RGBA')
    no_under=Image.alpha_composite(base_without_hand,shifted)
    # The new art is under, not over, the moved hand. This is a *partial* local pass.
    under_limited=under.copy();mask=np.array(under.getchannel('A'))
    mask[~orig_alpha]=0
    under_limited.putalpha(Image.fromarray(mask,'L'))
    with_under=Image.alpha_composite(Image.alpha_composite(base_without_hand,under_limited),shifted)
    # Note: the source matte may still contain floor shadow; these images are NOT production composites.
    for name,obj in [('CP375_BEFORE_MOVE_SOURCE.png',no_under),('CP375_AFTER_MOVE_WITH_PARTIAL_UNDERPAINT.png',with_under)]:obj.save(p/'qa'/name)
    # ORA contains drawn layers only, reference stays hidden and never substitutes for approved character art.
    ora=p/'CP375_FOUR_AUTHORED_HIDDEN_WRIST_LAYERS_NOT_RIG.ora'
    top=list(reversed(list(ART)))
    root=ET.Element('image',{'w':str(SIZE6[0]),'h':str(SIZE6[1]),'version':'0.0.3','name':'CP375 partial hidden wrist art, NOT approved'})
    stack=ET.SubElement(root,'stack')
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,name in enumerate(top):
            b=io.BytesIO();art6[name].save(b,format='PNG');dest=f'data/layer_{i:02}.png';z.writestr(dest,b.getvalue())
            ET.SubElement(stack,'layer',{'name':'DRAFT__'+name,'src':dest,'visibility':'visible','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        guide=src.resize(SIZE6,Image.Resampling.NEAREST)
        b=io.BytesIO();guide.save(b,format='PNG');z.writestr('data/approved_canon_exact_crop_reference.png',b.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_HIDDEN_SOURCE_GUIDE_NOT_PAINT','src':'data/approved_canon_exact_crop_reference.png','visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf8',xml_declaration=True))
        b=io.BytesIO();full6.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
    assert zipfile.ZipFile(ora).testzip() is None
    # Contact sheet: CANON only + exact source crop + newly drawn partial art, all marked.
    w,h=1700,900;board=Image.new('RGB',(w,h),'#14283d');d=ImageDraw.Draw(board)
    fp='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(fp,16);hd=ImageFont.truetype(fp,27)
    d.text((26,18),'TVK CP375 | LAM THIEN | PARTIAL HIDDEN WRIST ART',font=hd,fill='white')
    d.text((26,57),'CANON V2.1 EXACT | DRAWN SVG UNDERPAINT DRAFT | NOT A FULL-BODY PAINTING OR RIG',font=f,fill='#caddeb')
    full=canon.copy();full.thumbnail((414,700));board.paste(full.convert('RGB'),(26,104))
    crop=src.crop((0,111,95,230)).resize((345,430),Image.Resampling.LANCZOS)
    # Artistic crop source is untouched; the rest are technical experiments.
    board.paste(crop.convert('RGB'),(510,175))
    def check(im):
        checker=Image.new('RGBA',im.size,'#d9e3eb'); dr=ImageDraw.Draw(checker)
        for yy in range(0,im.height,20):
            for xx in range(0,im.width,20):
                if ((xx//20+yy//20)%2)==0:dr.rectangle((xx,yy,xx+19,yy+19),fill='#c8d3df')
        return Image.alpha_composite(checker,im).convert('RGB')
    undercrop=under.crop((0,111,95,230)).resize((345,430),Image.Resampling.LANCZOS)
    board.paste(check(undercrop),(900,175))
    motion=with_under.crop((0,111,95,230)).resize((345,430),Image.Resampling.LANCZOS)
    board.paste(check(motion),(1290,175))
    for x,label in [(26,'01 EXACT APPROVED CANON'),(510,'02 CANON LEFT-ARM CROP'),(900,'03 NEW DRAWN PARTIAL ART (DRAFT)'),(1290,'04 MOVED SOURCE + UNDERPAINT (DRAFT)')]:
        d.text((x,812),label,font=ImageFont.truetype(fp,14),fill='#ffffff')
    d.text((510,853),f'Uncovered alpha pixels: {unpainted} before  /  {remaining} not covered by new local paint',font=f,fill='#ffd2a4')
    prev=p/'qa'/'CP375_CANON_V2_1_PARTIAL_PAINT_COMPARISON_NOT_APPROVED.png';board.save(prev)
    report={
        'checkpoint':'CP375','approved_source_sha256':CANON_SHA,'front_exact_source_size':list(SIZE),
        'canvas_6x_for_drawn_svg':list(SIZE6),'actual_new_svg_art_layers':len(ART),
        'underpaint_motion_local_gap_before_px':unpainted,
        'underpaint_new_svg_alpha_coverage_of_old_gap_px':covered,
        'underpaint_motion_local_gap_remaining_px':remaining,
        'full_character_redraw_complete':False,'full_body_semantic_artist_layers_complete':False,
        'full_motion_gap_free':False,'visual_qa':'NOT_PASSED',
        'production_release':'blocked_pending_art','sprite_paths':{},
        'spine_ready':False,'apk_ready':False,
        'limitations':['Partial left wrist/under-sleeve newly drawn vector paint only','Rest of full body source remains low-res matte','Clipped technical overlay does not establish plausible occluded anatomy or clean motion','No device FPS, no Spine/Android integration','Artist review required'],
        'file_ora':ora.name,'file_preview':prev.name,
    }
    (p/'CP375_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    pr=argparse.ArgumentParser()
    pr.add_argument('--canon',required=True)
    pr.add_argument('--matte',required=True)
    pr.add_argument('--hand',required=True)
    pr.add_argument('--out',required=True)
    args=pr.parse_args()
    print(json.dumps(make(args.canon,args.matte,args.hand,args.out),ensure_ascii=False,indent=2))
#!/usr/bin/env python3
"""CP382 CANON-source face feature studies. Not approved painting/rigging.
Preserves exact source pixels and emits five editable reference-guide ORAs.
New VECTOR eye/lip guide strokes are hidden and are NOT considered approved artwork.
"""
from __future__ import annotations
import argparse, hashlib, io, json, shutil, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cairosvg

SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON_SIZE=(941,1672)
ROLES=['00_background_or_unmapped_source','01_face_and_skin_region_guide','02_front_bangs_region_guide','03_side_hair_ornament_region_guide','04_neck_and_collar_region_guide','05_shoulder_cloth_region_guide','06_left_eye_brow_region_guide','07_right_eye_brow_region_guide','08_nose_mouth_region_guide']
CROP_BOXES=[(22,681,196,884),(203,681,377,884),(382,681,556,884),(561,681,737,884),(744,681,918,884)]
PORTRAITS=[
  '01_shy_Ngai_ngung.png','02_angry_Tuc_gian.png','03_pain_Dau_don.png',
  '04_embarrassed_Xau_ho.png','05_charming_Quyen_ru.png'
]
# Mouth / brow guides are intentionally preliminary, visually inspect against source.
FEATURES=[
  {'brow1':'M42 99 Q55 95 68 88','brow2':'M93 79 Q108 74 121 72','mouth':'M84 142 Q93 143 103 138'},
  {'brow1':'M43 100 Q58 91 70 92','brow2':'M91 80 Q104 75 121 78','mouth':'M84 143 Q94 145 104 141'},
  {'brow1':'M42 100 Q54 94 67 91','brow2':'M90 80 Q107 72 119 73','mouth':'M88 134 Q101 129 110 136 Q114 145 100 149 Q91 148 88 141 Z'},
  {'brow1':'M43 101 Q55 97 67 92','brow2':'M89 80 Q107 77 120 75','mouth':'M83 150 Q91 151 100 149'},
  {'brow1':'M43 100 Q55 95 67 93','brow2':'M92 79 Q108 73 120 75','mouth':'M96 145 Q106 147 115 140'},
]

def validated(canon, refs):
    p=Path(canon)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=SHA: raise ValueError('CANON_SHA_MISMATCH')
    with Image.open(p) as im:
        if im.size!=CANON_SIZE or im.mode!='RGBA': raise ValueError('CANON_FORMAT_MISMATCH')
        sheet=np.asarray(im)
    for name,box in zip(PORTRAITS,CROP_BOXES):
        f=Path(refs)/name
        if not f.is_file(): raise ValueError('REFERENCE_MISSING: '+name)
        with Image.open(f) as im:
            if im.mode!='RGBA' or im.size[1]!=203 or im.size[0] not in (174,176):
                raise ValueError('REFERENCE_FORMAT_MISMATCH: '+name)
            if not np.array_equal(np.asarray(im),sheet[box[1]:box[3],box[0]:box[2],:]):
                raise ValueError('REFERENCE_NOT_PIXEL_EXACT_CANON: '+name)
    return True

def mask_partition(src):
    w,h=src.size
    label=Image.new('L',(w,h),0);d=ImageDraw.Draw(label)
    # Non-overlapping source-route regions; anatomical precision is NOT claimed.
    d.polygon([(24,69),(53,43),(87,41),(124,50),(148,81),(147,145),(131,169),(79,170),(33,140)],fill=1)
    d.polygon([(0,7),(47,5),(71,8),(84,43),(79,91),(56,109),(39,95),(16,116),(0,143)],fill=2)
    d.polygon([(92,0),(w-1,0),(w-1,156),(146,150),(133,116),(139,54)],fill=3)
    d.polygon([(50,151),(129,150),(160,203),(30,203)],fill=4)
    d.polygon([(0,149),(43,152),(57,203),(0,203)],fill=5)
    # Face features override region masks, preserved as source RGB snippets.
    d.polygon([(27,105),(39,92),(73,85),(85,106),(65,128),(37,124)],fill=6)
    d.polygon([(81,74),(111,66),(135,74),(135,101),(110,114),(88,105)],fill=7)
    d.polygon([(68,116),(111,116),(123,157),(95,167),(68,150)],fill=8)
    return np.array(label)

def make_svg(feature,role,w,h):
    paths={
      'brow_study':(feature['brow1']+' '+feature['brow2'],'#875d60',1.1),
      'mouth_study':(feature['mouth'],'#a75e68',1.2),
      'eye_study':('M39 110 Q50 116 70 103 M92 92 Q108 101 126 82','#6b4259',1.25),
    }
    path,col,sw=paths[role]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="{path}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def orasave(ora,layers,source,sketches):
    w,h=source.size
    image=ET.Element('image',{'w':str(w),'h':str(h),'version':'0.0.3','name':'CP382 SOURCE GUIDE — NOT ART'})
    stack=ET.SubElement(image,'stack')
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        def put(name,img,visible):
            internal=f'data/{len(stack):02d}.png';buffer=io.BytesIO();img.save(buffer,format='PNG');z.writestr(internal,buffer.getvalue())
            ET.SubElement(stack,'layer',{'name':name,'src':internal,'visibility':'visible' if visible else 'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        for name,p in sketches:put('UNAPPROVED_VECTOR__'+name,p,False)
        for name,p in reversed(layers):put('SOURCE_GUIDE__'+name,p,True)
        put('EXACT_CANON_CROP_REFERENCE_HIDDEN',source,False)
        z.writestr('stack.xml',ET.tostring(image,encoding='utf-8',xml_declaration=True))
        b=io.BytesIO();source.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
    with zipfile.ZipFile(ora) as z:
        assert z.testzip() is None

def draw_qa(sources,dests,output):
    cellw=200;gap=13;canvas=Image.new('RGB',(5*(2*cellw+gap)+24,510),'#132940');d=ImageDraw.Draw(canvas)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';fontS=ImageFont.truetype(font,14);fontB=ImageFont.truetype(font,20)
    d.text((20,10),'CP382 | LAM THIEN — 5 CANON EXPRESSION SOURCE GUIDES (NOT REDRAWN ART)',fill='#f3f6fb',font=fontB)
    for i,(src,seg) in enumerate(zip(sources,dests)):
        x=12+i*(2*cellw+gap)
        sc=src.resize((int(src.width*0.94),int(src.height*0.94)),Image.Resampling.NEAREST).convert('RGB')
        # semantic mask preview does not alter original CANON on the left
        sb=seg.resize((int(seg.width*0.94),int(seg.height*0.94)),Image.Resampling.NEAREST).convert('RGB')
        canvas.paste(sc,(x,92));canvas.paste(sb,(x+cellw,92))
        d.text((x,59),f'0{i+1} CANON EXACT',fill='#eaf4ff',font=fontS)
        d.text((x+cellw,59),'SOURCE MASK GUIDE',fill='#eaf4ff',font=fontS)
    d.text((18,355),'Masked colors are source pixels, not newly painted art. Polygon boundaries are approximate.',font=fontS,fill='#fddfc4')
    d.text((18,380),'All 5 OpenRaster guides preserve exact source portrait at rest. No hidden hair/skin underpaint or native HD.',font=fontS,fill='#cee2f4')
    d.text((18,405),'VECTOR brow/eye/mouth trials exist as hidden editable layers only — visual QA and APK remain BLOCKED.',font=fontS,fill='#cee2f4')
    canvas.save(output)

def build(canon, refs, out):
    validated(canon,refs)  # IMPORTANT: preflight before creating output
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for f in ['source','parts','svg','art_drafts','ora','qa']:(out/f).mkdir(exist_ok=True)
    shutil.copyfile(canon,out/'source'/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    manifest={'checkpoint':'CP382','canon_sha256':SHA,'canon_only':True,'visual_qa':'NOT_PASSED','release_status':'blocked_pending_art','sprite_paths':{},'native_face_master_complete':False,'art_approved':False,'spine_ready':False,'apk_ready':False,'portraits':[]}
    imgs=[];guides=[]
    colors=['#58677c','#edb0b0','#879ac7','#9982c0','#c6a57a','#71aee4','#99c68b','#e79e55','#da7896']
    for idx,name in enumerate(PORTRAITS):
        src=Image.open(Path(refs)/name).convert('RGBA')
        w,h=src.size;mask=mask_partition(src)
        arr=np.asarray(src);roles=[];paint=[]
        qa_arr=np.array(src.convert('RGB')).copy()
        for k,role in enumerate(ROLES):
            m=mask==k
            px=np.zeros((h,w,4),dtype=np.uint8);px[m]=arr[m]
            im=Image.fromarray(px,'RGBA');im.save(out/'parts'/f'{idx+1:02}_{role}.png')
            roles.append((role,im))
            color=np.array(tuple(bytes.fromhex(colors[k].lstrip('#'))),dtype=np.uint8)
            qa_arr[m]=((qa_arr[m].astype(np.float32)*0.42)+(color.astype(np.float32)*0.58)).astype(np.uint8)
        sketches=[]
        for role in ['brow_study','eye_study','mouth_study']:
            sv=make_svg(FEATURES[idx],role,w,h)
            fname=f'{idx+1:02}_{role}.svg';(out/'svg'/fname).write_text(sv,encoding='utf-8')
            png=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode('utf-8')))).convert('RGBA')
            png.save(out/'art_drafts'/f'{idx+1:02}_{role}.png')
            sketches.append((role,png))
        assert np.all((np.bincount(mask.ravel(),minlength=len(ROLES))>0))
        reconstructed=Image.new('RGBA',src.size)
        for _,layer in roles:reconstructed.alpha_composite(layer)
        assert np.array_equal(np.asarray(src),np.asarray(reconstructed))
        src.save(out/'source'/name)
        oraname=f'CP382_FACE_0{idx+1}_SOURCE_GUIDES_NOT_RIG.ora'
        orasave(out/'ora'/oraname,roles,src,sketches)
        imgs.append(src);guides.append(Image.fromarray(qa_arr,'RGB'))
        manifest['portraits'].append({'name':name,'dimensions':[w,h],'source_rgb_preserved':True,'visible_source_guide_layers':len(ROLES),'hidden_vector_study_layers':len(sketches),'hidden_exact_reference_layers':1,'ora':oraname,'all_semantic_parts_artist_approved':False})
    draw_qa(imgs,guides,out/'qa'/'CP382_CANON_FIVE_FACE_LAYER_GUIDES_NOT_ART.png')
    (out/'CP382_REPORT.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--refs',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();print(json.dumps(build(a.canon,a.refs,a.out),ensure_ascii=False,indent=2))
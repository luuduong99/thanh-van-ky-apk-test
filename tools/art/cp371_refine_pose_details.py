#!/usr/bin/env python3
"""CP371: two-pose Lâm Thiển sleeve detail study, source-locked to CANON V2.1.

Creates new hand-authored Bézier geometry: fold highlights and blue/gold hem
stitches in independent editable layers for idle and raised poses, plus small
finger crease refinements. NOT approved sprite art or a rig/animation/APK.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

import cairosvg
import numpy as np
from PIL import Image, ImageDraw, ImageChops

HERE = Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cp370',HERE/'cp370_two_hand_authored_poses.py')
cp370=importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp370)
SHA=cp370.SHA
SIZE=cp370.SIZE
FRONT=cp370.FRONT
NEW_FOLD='08_silk_folds_light'
NEW_HEM='09_hem_blue_gold_thread'
ORDER=(*cp370.ORDER[:5],NEW_FOLD,NEW_HEM,*cp370.ORDER[5:])

# These are manually authored path designs, NOT copied image pixels nor rotated
# CP370 bitmap patches. The folds and trims were drawn separately per key pose.
ART={
 'idle': {
 NEW_FOLD:r'''
 <defs>
  <linearGradient id="fold_idle_371" x1=".22" y1="0" x2=".73" y2="1">
   <stop stop-color="#fffefa" stop-opacity=".67"/>
   <stop offset=".46" stop-color="#e6edfc" stop-opacity=".39"/>
   <stop offset="1" stop-color="#5d94d2" stop-opacity=".25"/>
  </linearGradient>
 </defs>
 <path d="M65 146 C58 159 51 178 43 202 Q32 228 25 240
          C37 221 48 194 56 177 Q61 159 65 146Z"
       fill="url(#fold_idle_371)" opacity=".72"/>
 <path d="M61 154 C51 173 48 192 37 212 Q30 227 22 238"
       fill="none" stroke="#fffef9" stroke-width=".70" opacity=".87"/>
 <path d="M52 161 C44 174 41 194 32 207 Q24 222 18 228"
       fill="none" stroke="#d6e8ff" stroke-width=".47" opacity=".67"/>
 <path d="M66 166 Q63 187 55 203 Q49 220 35 231"
       fill="none" stroke="#8baed9" stroke-width=".36" opacity=".57"/>
 <path d="M34 186 Q30 198 25 207 M43 198 Q36 219 29 224"
       fill="none" stroke="#fff9ee" stroke-width=".41" opacity=".72"/>
 <path d="M59 168 Q55 179 54 193" fill="none" stroke="#edf4ff" stroke-width=".42"/>
 ''',
 NEW_HEM:r'''
 <path d="M66 150 C61 166 57 181 50 196 Q40 222 25 240"
       fill="none" stroke="#c9a16b" stroke-width=".28" opacity=".74"/>
 <path d="M66 150 C60 165 56 181 48 197 Q39 224 24 241"
       fill="none" stroke="#f3e1a7" stroke-width=".23" opacity=".86"/>
 <path d="M53 161 Q42 185 37 204 Q27 225 20 237"
       fill="none" stroke="#709ad0" stroke-width=".36" opacity=".56"/>
 <path d="M59 179 l-2.4 4.7 m-1.7 5.2 l-2.2 4.9 m-1.6 5.2 l-2.1 4.8
          m-1.9 5.3 l-2.2 4.6" stroke="#fff0bd" stroke-width=".32"
       stroke-linecap="round" fill="none" opacity=".61"/>
 ''',
 },
 'raised': {
 NEW_FOLD:r'''
 <defs>
  <linearGradient id="fold_raised_371" x1=".18" y1="0" x2=".72" y2="1">
   <stop stop-color="#fdfdfc" stop-opacity=".81"/>
   <stop offset=".51" stop-color="#ebf3ff" stop-opacity=".42"/>
   <stop offset="1" stop-color="#709bda" stop-opacity=".28"/>
  </linearGradient>
 </defs>
 <!-- New gravity-sagging fold paths for raised arm. Not an affine transform. -->
 <path d="M43 131 Q39 153 34 172 Q29 200 20 226
          Q32 213 38 191 Q45 160 49 138Z"
       fill="url(#fold_raised_371)" opacity=".68"/>
 <path d="M46 132 C42 157 35 179 30 202 Q24 225 17 239"
       stroke="#fffdfa" stroke-width=".73" fill="none" opacity=".87"/>
 <path d="M56 137 Q50 154 47 180 Q42 206 30 228"
       stroke="#d9ebfa" stroke-width=".57" fill="none" opacity=".75"/>
 <path d="M64 144 Q59 171 51 196 Q44 215 35 226"
       stroke="#8ab2e4" stroke-width=".49" fill="none" opacity=".62"/>
 <path d="M31 165 Q27 183 23 195 M38 177 Q32 202 27 216"
       stroke="#fffdfc" stroke-width=".44" fill="none" opacity=".77"/>
 ''',
 NEW_HEM:r'''
 <path d="M30 123 C29 146 27 171 20 197 Q15 214 7 228"
       stroke="#c6a067" stroke-width=".27" fill="none" opacity=".74"/>
 <path d="M31 123 C29 145 28 172 21 198 Q16 215 8 228"
       stroke="#f6e5b9" stroke-width=".25" fill="none" opacity=".84"/>
 <path d="M62 139 C57 165 52 193 42 220 Q35 236 25 245"
       stroke="#76a0d6" stroke-width=".33" fill="none" opacity=".65"/>
 <path d="M28 167 l-.8 5 m-.9 5 l-1 5 m-1.3 5 l-1.3 5 m-1.5 5 l-1.5 5"
       stroke="#fff1bf" stroke-width=".31" fill="none" opacity=".63"/>
 ''',
 }
}

FINGER={
 'idle': r'''
 <path d="M9 193 Q13 191 15 192 M7 197 Q11 195 13 196"
       fill="none" stroke="#d7a9a6" stroke-width=".36" opacity=".7"/>
 <path d="M10 190 Q14 189 17 188" fill="none" stroke="#fff7f0" stroke-width=".37" opacity=".8"/>
 ''',
 'raised': r'''
 <path d="M7.2 87.8 Q10 91 13 93 M14.5 85.8 Q17 90 19 93"
       fill="none" stroke="#dbaaa9" stroke-width=".36" opacity=".74"/>
 <path d="M10 94 Q13 96 16 96" fill="none" stroke="#fff7f0" stroke-width=".36" opacity=".79"/>
 ''',
}

def svg(name, pose):
    if pose not in ART: raise ValueError('Unknown pose')
    if name in (NEW_FOLD,NEW_HEM):
        return cp370.cp369.wrap_svg(ART[pose][name])
    base=cp370.svg(name,pose)
    if name=='04_arm_skin_and_hand':
        return base.replace('</svg>',FINGER[pose]+'</svg>')
    return base

def rgba(name,pose):
    s=svg(name,pose);ET.fromstring(s)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode('utf8'), output_width=SIZE[0],output_height=SIZE[1]))).convert('RGBA')

def compose(layers):
    out=Image.new('RGBA',SIZE)
    for name in ORDER:out.alpha_composite(layers[name])
    return out

def output_ora(path, layers, ref, pose):
    root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'version':'0.0.3','name':'CP371 '+pose+' DRAFT NOT APPROVED'})
    stack=ET.SubElement(root,'stack')
    merged=compose(layers)
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for idx,name in enumerate(reversed(ORDER)):
            key=f'data/layer_{idx:02d}.png';buf=io.BytesIO();layers[name].save(buf,format='PNG');z.writestr(key,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':'CP371_'+pose.upper()+'_DRAFT__'+name,'src':key,'opacity':'1.0','visibility':'visible','x':'0','y':'0','composite-op':'svg:src-over'})
        key='data/canon_hidden.png';buf=io.BytesIO();ref.resize(SIZE,Image.Resampling.NEAREST).save(buf,format='PNG');z.writestr(key,buf.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_REFERENCE_HIDDEN_NOT_PAINT','src':key,'opacity':'1.0','visibility':'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(root,encoding='utf8',xml_declaration=True))
        buf=io.BytesIO();merged.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
        assert z.testzip() is None
    return merged

def measure_layer_containment(layers,layer_name):
    source=np.asarray(layers['05_translucent_front_sleeve'].getchannel('A'))
    new=np.asarray(layers[layer_name].getchannel('A'))
    painted=(new>40)
    # Gold thread near seam edge allowed within 2 source pixels (12 working px).
    from PIL import ImageFilter
    grown=layers['05_translucent_front_sleeve'].getchannel('A').filter(ImageFilter.MaxFilter(25))
    inside=np.asarray(grown)>25
    used=int(painted.sum())
    return {'visible_pixels':used, 'within_sleeve_or_edge':int(np.count_nonzero(painted & inside)),
            'coverage_fraction':round(float(np.count_nonzero(painted & inside))/max(used,1),4)}

def sheet(out,reference,original,new):
    focus=(0,80,115,265);zoom=(392,632)
    panels=[('01  APPROVED CANON V2.1',reference.crop(focus).resize(zoom,Image.Resampling.LANCZOS)),
            ('02  CP370 IDLE / OLD DRAFT',original['idle'].crop(tuple(i*6 for i in focus)).resize(zoom,Image.Resampling.LANCZOS)),
            ('03  CP371 IDLE / NEW DRAFT',new['idle'].crop(tuple(i*6 for i in focus)).resize(zoom,Image.Resampling.LANCZOS)),
            ('04  CP371 RAISED / NEW DRAFT',new['raised'].crop(tuple(i*6 for i in focus)).resize(zoom,Image.Resampling.LANCZOS))]
    w,h=1670,800;board=Image.new('RGB',(w,h),'#152438');d=ImageDraw.Draw(board)
    d.text((25,18),'THANH VAN KY / LAM THIEN / CP371 — CANON-ONLY ART STUDY',fill='#f4f7fc')
    d.text((25,42),'New independent silk-fold and hem-thread paths on two poses. No substitute character image.',fill='#c9d6e8')
    for idx,(title,im) in enumerate(panels):
        x=24+idx*412;d.text((x,101),title,fill='#e4eef9')
        backing=Image.new('RGBA',zoom,'white' if idx==0 else '#dce4ee')
        if idx:
            check=ImageDraw.Draw(backing)
            for yy in range(0,zoom[1],24):
                for xx in range(0,zoom[0],24):
                    if (xx//24+yy//24)%2==0:check.rectangle((xx,yy,xx+23,yy+23),fill='#cbd6e3')
        backing.alpha_composite(im.convert('RGBA'))
        board.paste(backing.convert('RGB'),(x,128))
    d.text((25,775),'NOT APPROVED: limited sleeve vector work; not a full-body character sprite, Spine rig, or APK.',fill='#ffe0b6')
    path=out/'CP371_CANON_CP370_CP371_TWO_POSES_NOT_APPROVED.png';board.save(path);return path

def build(canon_path,output_path):
    canon=Path(canon_path);out=Path(output_path)
    if hashlib.sha256(canon.read_bytes()).hexdigest()!=SHA:raise ValueError('CANON_SHA_MISMATCH')
    with Image.open(canon) as image:
        if image.size!=(941,1672) or image.mode!='RGBA':raise ValueError('CANON_FORMAT_MISMATCH')
        ref=image.crop(FRONT)
    out.mkdir(parents=True,exist_ok=True)
    old={};rendered={};new={};oras={};containment={}
    for pose in ('idle','raised'):
        p=out/pose;p.mkdir(exist_ok=True)
        layers={}
        for name in ORDER:
            source=svg(name,pose);(p/(name+'.svg')).write_text(source,encoding='utf8')
            layers[name]=rgba(name,pose);layers[name].save(p/(name+'.png'))
        rendered[pose]=layers
        old_layers={name:cp370.png(name,pose) for name in cp370.ORDER}
        old[pose]=cp370.composite(old_layers)
        new[pose]=output_ora(out/f'CP371_{pose.upper()}_NINE_ART_LAYERS_NOT_SPINE.ora',layers,ref,pose)
        new[pose].save(out/f'CP371_{pose.upper()}_TRANSPARENT_DRAFT.png')
        containment[pose]={name:measure_layer_containment(layers,name) for name in (NEW_FOLD,NEW_HEM)}
        # Pixel difference must be genuine and localized, but not automatically GOOD art.
    diffs={pose:int(np.count_nonzero(np.any(np.asarray(new[pose])!=np.asarray(old[pose]),axis=2))) for pose in ('idle','raised')}
    unchanged=all(np.array_equal(np.asarray(rendered['idle'][k]),np.asarray(rendered['raised'][k])) for k in cp370.cp369.STATIC_NAMES+(cp370.cp369.SHOULDER_NAME,))
    preview=sheet(out,ref,old,new)
    report={
        'checkpoint':'CP371','canon_sha256':SHA,'reference_size':[941,1672], 'front_crop':list(FRONT),
        'working_canvas':list(SIZE),'working_resolution_is_upscaled_geometry_not_master_art':True,
        'semantic_art_layers_per_pose':len(ORDER),'ora_layers_including_hidden_guide':len(ORDER)+1,
        'new_svg_layers_per_pose':[NEW_FOLD,NEW_HEM],'independent_pose_geometry':True,
        'finger_detail_paths_updated':True,'static_hair_bodice_shoulder_ornament_unchanged_between_poses':unchanged,
        'new_overlay_within_sleeve_or_edge':containment,
        'change_pixels_against_cp370':diffs,
        'user_approved_sprite':False,'visual_qa':'NOT_PASSED','art_release':'blocked_pending_art',
        'spine_ready':False,'apk_built_or_tested':False,'sprite_paths':{},
        'warnings':['Added folds/hem details still do NOT match painter-level CANON detail',
                    'No full-body native semantic master, no accurate face/other arm/feet painted',
                    'No in-between animation, no Android device FPS evaluation',
                    'Local overlay containment is not proof of robust shoulder skinning'],
        'preview':preview.name,
    }
    (out/'CP371_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--canon',required=True);parser.add_argument('--out',required=True)
    args=parser.parse_args()
    print(json.dumps(build(args.canon,args.out),ensure_ascii=False,indent=2))
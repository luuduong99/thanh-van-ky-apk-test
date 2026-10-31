#!/usr/bin/env python3
"""CP370: two independently SVG-drawn arm pose studies for Lam Thien.

CANON remains unchanged. This IS NOT game-ready native full-body paint, nor
Spine rig, nor an approved artwork. Neither of the keyframes is a rotation
of the other; the raised arm and fabric are different hand-authored vector paths.
"""
from pathlib import Path
import argparse, importlib.util, io, hashlib, json, zipfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cairosvg

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'cp369_split_gold_and_underpaint.py'
spec=importlib.util.spec_from_file_location('cp369',SRC)
cp369=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp369)
SHA=cp369.SHA
SIZE=cp369.SIZE
FRONT=cp369.FRONT
ORDER=cp369.ORDER
KEYFRAME_NAMES=cp369.MOTIONAL

# CP370: separate, newly drawn geometry for raised arm, wrist and silk drape.
# Artwork scale is a 6x working vector canvas; the approved raster Front remains
# only 217x458. Do NOT claim a source-resolution increase by upscaling.
RAISED={
'04_arm_skin_and_hand': r'''
<defs>
 <linearGradient id="skin_raise" x1=".1" y1=".15" x2=".9" y2=".9">
  <stop stop-color="#ffefeb"/><stop offset=".42" stop-color="#fbded6"/>
  <stop offset=".8" stop-color="#e9b9b6"/><stop offset="1" stop-color="#dc9eaa"/>
 </linearGradient>
</defs>
<!-- The new arm axis points upward-left (idle arm points downward-left). -->
<path d="M66 132 C62 126 55 121 47 117 Q35 111 25 106
          Q18 103 14 99 L8 96 Q4 91 1 88 Q0 86 3 87 L11 93
          Q5 86 6 83 Q8 82 12 91 L17 94
          Q12 85 15 84 Q18 84 22 94
          L27 98 Q39 103 50 107 C61 111 70 119 71 129
          Q70 133 66 132Z"
 fill="url(#skin_raise)" stroke="#d8a2aa" stroke-width=".66"/>
<path d="M66 128 Q53 114 39 109 Q28 103 18 98" fill="none" stroke="#fff9f2" opacity=".77" stroke-width="1.5"/>
<path d="M48 119 Q30 112 20 106" fill="none" stroke="#e4b1b1" opacity=".63" stroke-width=".65"/>
<path d="M11 94 Q10 91 10 89 M16 95 Q15 92 16 90" fill="none" stroke="#cc9ca6" stroke-width=".4"/>
''',
'05_translucent_front_sleeve': r'''
<defs>
 <linearGradient id="silk_raise" x1=".18" y1=".08" x2=".7" y2=".98">
  <stop stop-color="#fffefc" stop-opacity=".93"/>
  <stop offset=".31" stop-color="#edf3fd" stop-opacity=".81"/>
  <stop offset=".7" stop-color="#b0cdef" stop-opacity=".68"/>
  <stop offset="1" stop-color="#4c85d8" stop-opacity=".27"/>
 </linearGradient>
 <linearGradient id="silk_raise_shadow" x1="0" y1="0" x2="1" y2="1">
  <stop stop-color="#aac8f0" stop-opacity=".04"/>
  <stop offset="1" stop-color="#487ecb" stop-opacity=".57"/>
 </linearGradient>
</defs>
<!-- Unlike idle pose: the raised arm is supported horizontally, silk hangs vertically. -->
<path d="M67 132 Q56 127 49 122 Q40 116 30 112
         C26 120 25 136 25 148 Q22 175 13 195 Q9 212 4 230
         C19 222 29 211 34 197 Q29 228 20 251
         C43 239 57 218 62 193 Q69 173 74 149 Q75 136 67 132Z"
 fill="url(#silk_raise)" stroke="#8fb3e3" stroke-opacity=".83" stroke-width=".69"/>
<path d="M60 138 Q52 155 45 180 Q32 217 24 245 Q47 223 56 200 Q69 162 70 145Z"
 fill="url(#silk_raise_shadow)" opacity=".76"/>
<path d="M48 126 C39 149 33 172 27 195 Q21 216 10 228" fill="none" stroke="#fffdf9" stroke-width="1.64" opacity=".89"/>
<path d="M60 134 Q49 165 42 194 Q34 225 25 246" fill="none" stroke="#e6f1ff" stroke-width="1.2" opacity=".93"/>
<path d="M69 139 Q65 167 55 196 Q46 220 36 234" fill="none" stroke="#6fa1da" stroke-width=".9" opacity=".58"/>
<path d="M35 118 Q27 147 26 174" fill="none" stroke="#d8e7fc" stroke-width=".78" opacity=".83"/>
<path d="M46 127 Q38 160 32 186" fill="none" stroke="#a7bfe2" stroke-width=".5" opacity=".58"/>
<!-- Fold lines are authored to this raised pose; not an affine bitmap rotation. -->
<path d="M31 155 Q24 177 18 186 M30 176 Q25 190 16 204" fill="none" stroke="#fdfbfc" stroke-width=".6" opacity=".55"/>
''',
'06_wrist_gold_moving': r'''
<defs><linearGradient id="raise_wrist_gold" x1="0" y1="0" x2="1" y2="1">
 <stop stop-color="#fff2c1"/><stop offset=".45" stop-color="#c79a51"/>
 <stop offset=".78" stop-color="#f7e5ae"/><stop offset="1" stop-color="#8c622f"/>
</linearGradient></defs>
<!-- A distinct cuff drawn around the new wrist at (23,105), not translated old pixels. -->
<path d="M22 99 Q26 98 29 103 Q30 106 25 109
         Q22 109 19 105Z" fill="url(#raise_wrist_gold)" stroke="#946633" stroke-width=".48"/>
<path d="M22 101 Q25 101 27 104 M21 106 Q24 107 27 105" fill="none" stroke="#ffefbc" stroke-width=".66"/>
<path d="M24.3 101.5 L27.2 104 L24.7 106.8 L22.3 104.2Z"
 fill="#418bc9" stroke="#ffedb8" stroke-width=".38"/>
'''
}

def svg(name, pose):
    if pose=='idle':return cp369.svg_layer(name)
    if name in RAISED:return cp369.wrap_svg(RAISED[name])
    return cp369.svg_layer(name)

def png(name, pose):
    source=svg(name,pose)
    ET.fromstring(source)
    data=cairosvg.svg2png(bytestring=source.encode(),output_width=SIZE[0],output_height=SIZE[1])
    return Image.open(io.BytesIO(data)).convert('RGBA')

def composite(layers):
    image=Image.new('RGBA',SIZE)
    for name in ORDER: image.alpha_composite(layers[name])
    return image

def ora(outpath, layers, pose, reference):
    image_root=ET.Element('image',{'w':str(SIZE[0]),'h':str(SIZE[1]),'version':'0.0.3','name':f'CP370 {pose}: DRAFT NOT APPROVED'})
    stack=ET.SubElement(image_root,'stack')
    combined=composite(layers)
    with zipfile.ZipFile(outpath,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for idx,name in enumerate(reversed(ORDER)):
            internal=f'data/art_{idx:02d}.png'
            buf=io.BytesIO();layers[name].save(buf,format='PNG');z.writestr(internal,buf.getvalue())
            ET.SubElement(stack,'layer',{'name':f'CP370_{pose.upper()}_DRAFT__{name}','src':internal,'opacity':'1.0','visibility':'visible','x':'0','y':'0','composite-op':'svg:src-over'})
        internal='data/canon_reference_HIDDEN.png';buf=io.BytesIO();reference.resize(SIZE,Image.Resampling.NEAREST).save(buf,format='PNG');z.writestr(internal,buf.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_SOURCE_GUIDE_HIDDEN_NOT_PAINT','src':internal,'opacity':'1.0','visibility':'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(image_root,encoding='utf-8',xml_declaration=True))
        buf=io.BytesIO();combined.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
        assert z.testzip() is None
    return combined

def metrics(pose_layers):
    for key in ['idle','raised']:
        assert set(pose_layers[key])==set(ORDER)
    # Relative test: fixed shoulder hardware should stay pixel-identical and
    # wrist must actually relocate. Not evidence of natural or safe animation.
    fixed_unchanged = np.array_equal(np.asarray(pose_layers['idle'][cp369.SHOULDER_NAME]),np.asarray(pose_layers['raised'][cp369.SHOULDER_NAME]))
    wrist_idle=pose_layers['idle'][cp369.WRIST_NAME].getchannel('A').getbbox()
    wrist_raised=pose_layers['raised'][cp369.WRIST_NAME].getchannel('A').getbbox()
    moved_arm_fraction={}
    for name in cp369.MOTIONAL:
        a=np.asarray(pose_layers['idle'][name]); b=np.asarray(pose_layers['raised'][name]);
        moved_arm_fraction[name]=round(float(np.mean(np.any(a!=b,axis=2))),4)
    # Hidden shoulder underpaint checked only at a local, relevant overlap ROI.
    roi=tuple(x*6 for x in (56,121,85,170))
    base=Image.new('RGBA',SIZE)
    for name in ('02_hidden_bodice_cloth','03_hidden_shoulder_skin'):
        base.alpha_composite(pose_layers['idle'][name])
    behind=np.asarray(base.getchannel('A').crop(roi))>90
    rest=Image.new('RGBA',SIZE);raised=Image.new('RGBA',SIZE)
    for name in cp369.MOTIONAL:
        rest.alpha_composite(pose_layers['idle'][name]);raised.alpha_composite(pose_layers['raised'][name])
    idle_mask=np.asarray(rest.getchannel('A').crop(roi))>90
    raised_mask=np.asarray(raised.getchannel('A').crop(roi))>90
    uncovered=idle_mask & ~raised_mask
    absent=uncovered & ~behind
    return {'shoulder_gold_exactly_unchanged':bool(fixed_unchanged),
            'wrist_idle_bbox':wrist_idle,'wrist_raised_bbox':wrist_raised,
            'wrist_relocated':wrist_idle!=wrist_raised,
            'moving_layer_pixel_change_fraction':moved_arm_fraction,
            'shoulder_joint_roi_newly_exposed_px':int(uncovered.sum()),
            'joint_exposed_without_underpaint_px':int(absent.sum()),
            'underpaint_warning_only':'Local ROI alpha test; no overall rig or motion guarantee'}

def preview(out,ref,merged):
    focus=(0,80,115,265)
    dims=(405,650)
    entries=[('01 CANON V2.1 - APPROVED',ref.crop(focus).resize(dims,Image.Resampling.LANCZOS)),
             ('02 CP370 - IDLE DRAFT',merged['idle'].crop(tuple(x*6 for x in focus)).resize(dims,Image.Resampling.LANCZOS)),
             ('03 CP370 - RAISED DRAFT',merged['raised'].crop(tuple(x*6 for x in focus)).resize(dims,Image.Resampling.LANCZOS))]
    canvas=Image.new('RGB',(1320,825),'#152437');p=ImageDraw.Draw(canvas)
    p.text((26,20),'THANH VAN KY / LAM THIEN / CP370',fill='#e8f4ff')
    p.text((26,44),'Exact character CANON + independently drawn raised-arm vector DRAFT. NO replacement character imagery.',fill='#b3cbe4')
    for idx,(label,im) in enumerate(entries):
        x=25+idx*435
        p.text((x,100),label,fill='#dce9f4')
        bg=Image.new('RGBA',dims,'#e1e9f1')
        board=ImageDraw.Draw(bg)
        if idx:
            for yy in range(0,dims[1],24):
                for xx in range(0,dims[0],24):
                    if ((xx//24+yy//24)%2)==0:board.rectangle((xx,yy,xx+23,yy+23),fill='#cddae9')
        else:bg=Image.new('RGBA',dims,'white')
        bg.alpha_composite(im.convert('RGBA'));canvas.paste(bg.convert('RGB'),(x,129))
    p.text((26,790),'VISUAL QA NOT PASSED: partial vector art only. No true full-body sprite, Spine or Android APK.',fill='#fbd29a')
    path=out/'CP370_CANON_IDLE_RAISED_INDEPENDENT_PATHS_UNAPPROVED.png';canvas.save(path)
    return path

def build(canon,outdir):
    canon=Path(canon);out=Path(outdir)
    if hashlib.sha256(canon.read_bytes()).hexdigest()!=SHA:raise ValueError('CANON SHA mismatched; refuse non-canonical reference')
    with Image.open(canon) as img:
        if img.size!=(941,1672) or img.mode!='RGBA':raise ValueError('CANON image shape/mode mismatch')
        reference=img.crop(FRONT)
    out.mkdir(parents=True,exist_ok=True)
    actual={};merged={};ors={}
    for pose in ('idle','raised'):
        parts={}
        directory=out/pose;directory.mkdir(exist_ok=True)
        for name in ORDER:
            layer=png(name,pose);parts[name]=layer
            (directory/f'{name}.svg').write_text(svg(name,pose),encoding='utf-8')
            layer.save(directory/f'{name}.png')
        actual[pose]=parts
        ors[pose]=out/f'CP370_{pose.upper()}_SEVEN_LAYER_DRAFT_NOT_SPINE.ora'
        merged[pose]=ora(ors[pose],parts,pose,reference)
        merged[pose].save(out/f'CP370_{pose.upper()}_TRANSPARENT_LOCAL_DRAFT.png')
    prov=metrics(actual)
    pv=preview(out,reference,merged)
    report={ 'checkpoint':'CP370','canon_sha256':SHA,'source_dimensions':[941,1672],
            'poses':['idle','raised'],'independently_drawn_raised_svg_keys':list(RAISED),
            'render_size':list(SIZE),'work_canvas_is_six_times_source_crop_no_real_detail_claim':True,
            'fixed_vs_moving_diagnostic':prov,
            'ora_files':[p.name for p in ors.values()],
            'preview':pv.name,
            'visual_qa':'NOT_PASSED','production_release':'blocked_pending_art',
            'sprite_paths':{},'spine_ready':False,'apk_ready':False,
            'limitations':['Only left sleeve/arm, NOT character full-body','No professional art acceptance',
                'No blending/in-between frames or rig', 'No claim of gap-free joints or Android FPS']}
    (out/'CP370_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--canon',required=True);ap.add_argument('--out',required=True)
    args=ap.parse_args();print(json.dumps(build(args.canon,args.out),ensure_ascii=False,indent=2))
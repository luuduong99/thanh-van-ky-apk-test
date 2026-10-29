#!/usr/bin/env python3
"""CP360 artist-directed tiny original vector underpaint experiment; not production art."""
from pathlib import Path
import argparse
import io,json,hashlib,zipfile,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import cv2,cairosvg

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cp348-zip',type=Path,required=True)
parser.add_argument('--cp359-zip',type=Path,required=True)
parser.add_argument('--canon',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args()
OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
CP348=args.cp348_zip
CP359=args.cp359_zip
CANON=args.canon
S='f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497'
C='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
assert hashlib.sha256(CP348.read_bytes()).hexdigest()==S
assert hashlib.sha256(CANON.read_bytes()).hexdigest()==C
assert zipfile.ZipFile(CP359).testzip() is None
with zipfile.ZipFile(CP348) as z:
 names=sorted(n for n in z.namelist() if n.startswith('layers/') and n.endswith('.png'))
 parts=[Image.open(io.BytesIO(z.read(n))).convert('RGBA') for n in names]
 original=Image.open(io.BytesIO(z.read('FRONT_CP348_TEN_LAYER_RECON_QA_ONLY.png'))).convert('RGBA')
with zipfile.ZipFile(CP359) as z:
 arm_slices=[Image.open(io.BytesIO(z.read(f'CP359_0{k}_{name}_SOURCE_NOT_PAINT.png'))).convert('RGBA') for k,name in enumerate(['ARM_SKIN','GOLD_TRIM','BACK_SILK','INNER_SLEEVE','LOWER_SILK','SLEEVE_REMAINDER'],1)]
assert len(arm_slices)==6 and original.size==(215,449)
W,H=original.size

# ALL coordinates are in 215x449 source-reference viewBox; curves are newly-authored
# hidden details, not a reconversion/AI upscaling of 215x449 known RGB content.
def svg(paths):
 return (f'''<svg xmlns="http://www.w3.org/2000/svg" width="1290" height="2694" viewBox="0 0 215 449">
 <defs>
 <linearGradient id="skin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f0c3b9"/><stop offset="0.33" stop-color="#ffe7d7"/><stop offset="0.67" stop-color="#fff4ec"/><stop offset="1" stop-color="#d8a7a7"/></linearGradient>
 <linearGradient id="cloth" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7696d7"/><stop offset="0.33" stop-color="#b9ccf4"/><stop offset="0.65" stop-color="#f7f7ff"/><stop offset="1" stop-color="#7a9ad8"/></linearGradient>
 </defs>{paths}</svg>''')
# 1) Anatomical round upper-arm sliver should be obscured beneath the sleeve at rest.
skin_svg=svg('''<path d="M64.2 125 C67.5 123.9 70.7 127.3 72 133 C74.4 139 72.1 148.6 69 153 C66 151 61.4 148.8 59.8 144.5 C59.5 137.7 60.8 130 64.2 125Z" fill="url(#skin)"/>
<path d="M64 128 C63.5 134 63.9 140 65.2 144.8" fill="none" stroke="#fff8f1" opacity=".45" stroke-width="1.2"/>
<path d="M69.8 132.5 C71 137.8 70.5 142.5 69.4 147" fill="none" stroke="#cb9b9f" opacity=".38" stroke-width=".7"/>''')
# 2) Bodice facing / hidden blue-white fabric underlap close to the arm socket.
cloth_svg=svg('''<path d="M61.7 145 C65.5 146.3 71.4 145.2 74.2 151.2 C76 159 74 168.2 70.4 176 C66.5 172 63 169 60.3 165 C60 159.5 59.8 150.5 61.7 145Z" fill="url(#cloth)"/>
<path d="M65.5 147 C67 153 68 160 67 168" stroke="#ffffff" stroke-width=".85" opacity=".65" fill="none"/>
<path d="M70.5 150 C70 156 71.5 163 70.2 172" stroke="#4e77ba" stroke-width=".9" opacity=".4" fill="none"/>''')
for name,data in [('CP360_HIDDEN_SKIN_PAINT_STUDY.svg',skin_svg),('CP360_HIDDEN_BODICE_PAINT_STUDY.svg',cloth_svg)]: (OUT/name).write_text(data,encoding='utf-8')

# Rasterize SVG at 6x so genuinely painted paths carry independent high-resolution samples.
# Clip ONLY to existing fully opaque arm original, so nothing changes at rest; deliberately
# this does not fill entirely missing opaque occluded body pieces beyond the source arm.
opaque=(np.asarray(parts[5])[:,:,3]==255)
mask=Image.fromarray(np.uint8(opaque)*255,'L')
paint_layers=[]
for name,svgdata in [('CP360_HIDDEN_SHOULDER_SKIN_VECTOR_STUDY',skin_svg),('CP360_HIDDEN_BODICE_CLOTH_VECTOR_STUDY',cloth_svg)]:
 png=cairosvg.svg2png(bytestring=svgdata.encode('utf-8'),output_width=1290,output_height=2694)
 painted=Image.open(io.BytesIO(png)).convert('RGBA')
 clip=np.array(mask.resize(painted.size,Image.Resampling.NEAREST))
 rgba=np.array(painted)
 rgba[:,:,3]=np.minimum(rgba[:,:,3],clip)
 high=Image.fromarray(rgba,'RGBA')
 high.save(OUT/(name+'_NATIVE_6X.png'))
 low=high.resize((W,H),Image.Resampling.LANCZOS)
 # strict opacity clip at source scale after downsample again
 r=np.asarray(low).copy(); r[:,:,3]=np.minimum(r[:,:,3],np.where(opaque,255,0).astype('uint8'))
 low=Image.fromarray(r,'RGBA')
 assert np.any(np.array(low.getchannel('A'))>0)
 low.save(OUT/(name+'_CP359_LORES_QA_ONLY.png'))
 paint_layers.append((name,low,high))

# Use exactly source ordering. New patches placed underneath the six original arm textures.
seq=[]
for i,p in enumerate(parts):
 if i==5:
  seq.extend((f'CP360_{name}',x.copy()) for name,x,h in paint_layers)
  seq.extend((f'CP359_0{k}_{s}_SOURCE_NOT_PAINT',x.copy()) for k,(s,x) in enumerate(zip(['ARM_SKIN','GOLD_TRIM','BACK_SILK','INNER_SLEEVE','LOWER_SILK','SLEEVE_REMAINDER'],arm_slices),1))
  # Preserve original CP359 truth: two never-painted roles still blank
  seq.append(('CP360_SHOULDER_HIDDEN_FULL_NATIVE_LAYER_EMPTY',Image.new('RGBA',(W,H))))
  seq.append(('CP360_BODICE_HIDDEN_FULL_NATIVE_LAYER_EMPTY',Image.new('RGBA',(W,H))))
 else: seq.append((f'CP348_{Path(names[i]).stem}',p.copy()))
assert len(seq)==19

def comp(seq):
 out=Image.new('RGBA',(W,H))
 for name,img in seq:out=Image.alpha_composite(out,img)
 return out
rest=comp(seq)
a=np.asarray(original); b=np.asarray(rest)
assert np.array_equal(a[:,:,3],b[:,:,3]), 'Idle alpha drift'
assert np.array_equal(a[a[:,:,3]>0],b[b[:,:,3]>0]), 'Idle visible pixels drift'
rest.save(OUT/'CP360_REST_COMPOSITE_QA.png')

# ORA with separate rasterized painting layers + original lowres source material.
root=ET.Element('image',{'w':str(W),'h':str(H),'name':'CP360_TWO_TINY_PAINT_STUDIES_NOT_FULL_ART','version':'0.0.3'})
stack=ET.SubElement(root,'stack')
ora=OUT/'CP360_LEFT_SHOULDER_PAINT_STUDY_19_LAYER_NOT_RIG.ora'
with zipfile.ZipFile(ora,'w') as z:
 z.writestr('mimetype',b'image/openraster',compress_type=zipfile.ZIP_STORED)
 for i,(name,img) in enumerate(reversed(seq)):
  fn=f'data/layer{i:02d}.png';io_png=io.BytesIO();img.save(io_png,'PNG');z.writestr(fn,io_png.getvalue())
  ET.SubElement(stack,'layer',{'name':name,'src':fn,'x':'0','y':'0','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over'})
 z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
 out=io.BytesIO();rest.save(out,'PNG');z.writestr('mergedimage.png',out.getvalue())
 assert z.testzip() is None

# Seam metric is marked artist-selected geometry, not a proof that each alpha delta is a hole.
def poly(points):
 m=np.zeros((H,W),'uint8');cv2.fillPoly(m,[np.array(points,'int32')],1);return m.astype(bool)
seam_shoulder=poly([(52,115),(77,115),(78,155),(59,168),(49,151)])
seam_body=poly([(61,153),(81,158),(79,194),(60,204),(55,183)]) & ~seam_shoulder
finger_margin=poly([(0,180),(38,171),(45,204),(0,208)])
seam=seam_shoulder|seam_body
# For downstream manual art review, both pose outputs are SAME CAMERA/CANVAS & pivot.
poses={}
arm_group=parts[5]
assert np.array_equal(np.asarray(arm_group)[:,:,3],np.asarray(Image.alpha_composite(Image.new('RGBA',(W,H)),arm_group))[:,:,3])
for deg in [0,-1,-2,-4]:
    # Rasterize the existing arm as ONE temporary group for QA, so splitting the source
    # into six material regions does not introduce artificial interpolation seams.
    group_pose=arm_group.rotate(deg,Image.Resampling.BICUBIC,center=(70,132),expand=False) if deg else arm_group
    def render_group(with_paint):
        items=[];inserted=False
        for name,im in seq:
            if name.startswith('CP359_0') and name.endswith('_SOURCE_NOT_PAINT'):
                if not inserted:
                    items.append((name,group_pose))
                    inserted=True
                else:items.append((name,Image.new('RGBA',(W,H))))
            elif name.startswith('CP360_CP360_HIDDEN_') and not with_paint:
                items.append((name,Image.new('RGBA',(W,H))))
            else:items.append((name,im))
        return comp(items)
    without=render_group(False);alt=render_group(True)
    independent=comp([(name,im.rotate(deg,Image.Resampling.BICUBIC,center=(70,132),expand=False)
                      if name.startswith('CP359_0') and 'SOURCE_NOT_PAINT' in name and deg else im)
                      for name,im in seq if not name.startswith('CP360_CP360_HIDDEN_')])
    ar0=np.asarray(without);ar1=np.asarray(alt);start=a[:,:,3]
    loc0=(start>127)&(ar0[:,:,3]<25);loc1=(start>127)&(ar1[:,:,3]<25)
    cross=np.any(np.asarray(independent)!=ar0,axis=2)
    poses[str(deg)]={'lost_before':int(loc0.sum()),'lost_after':int(loc1.sum()),
        'shoulder_seam_before':int((loc0&seam_shoulder).sum()),'shoulder_seam_after':int((loc1&seam_shoulder).sum()),
        'body_seam_before':int((loc0&seam_body).sum()),'body_seam_after':int((loc1&seam_body).sum()),
        'finger_margin_before':int((loc0&finger_margin).sum()),'finger_margin_after':int((loc1&finger_margin).sum()),
        'independent_six_piece_interpolation_pixel_drift_vs_group':int(cross.sum())}
    for base,img in [('no_patch',without),('with_patch',alt),('individually_rotated',independent)]:
        img.save(OUT/f'CP360_{base}_angle_{abs(deg)}_QA.png')

# Small zoom comparison with mask annotation
board=Image.new('RGB',(1350,1000),'#e7edf5');d=ImageDraw.Draw(board)
try:f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
except:f=ImageFont.load_default()
d.text((25,15),'CP360 / localized underpainting study — NOT painter-approved, NOT rig',font=f,fill='#253a50')
def panel(image,px,py,text):
 crop=image.crop((17,108,95,211)).resize((312,412),Image.Resampling.NEAREST)
 bg=Image.new('RGB',crop.size,'#cfd9e8');bg.paste(crop,(0,0),crop)
 board.paste(bg,(px,py));d.text((px,py+418),text,font=f,fill='#273c59')
for i,degree in enumerate([0,2,4]):
 image=Image.open(OUT/f'CP360_no_patch_angle_{degree}_QA.png').convert('RGBA')
 panel(image,25+440*i,70,f'{degree}deg: source layers')
 image=Image.open(OUT/f'CP360_with_patch_angle_{degree}_QA.png').convert('RGBA')
 panel(image,25+440*i,540,f'{degree}deg: tiny underpaint')
d.text((30,970),'Important: lower silhouette gaps / original pose art remain incomplete.',font=f,fill='#b04137')
board.save(OUT/'CP360_SHOULDER_PAINT_SAME_VIEW_QA.png')

# QA checks: lock, source pixel fidelity, paint nonempty, file metadata, pose similarity, no release flag.
checks={
'correct_original_canons_sha':hashlib.sha256(CANON.read_bytes()).hexdigest()==C,
'correct_cp348_sha':hashlib.sha256(CP348.read_bytes()).hexdigest()==S,
'cp359_integrity':zipfile.ZipFile(CP359).testzip() is None,
'ora_integrity':zipfile.ZipFile(ora).testzip() is None,
'ora_19_layers':len(seq)==19,
'original_idle_alpha_unchanged':np.array_equal(a[:,:,3],b[:,:,3]),
'original_idle_rgb_unchanged_visible':np.array_equal(a[a[:,:,3]>0],b[b[:,:,3]>0]),
'painted_skin_nonempty':np.any(np.array(paint_layers[0][1].getchannel('A'))),
'painted_cloth_nonempty':np.any(np.array(paint_layers[1][1].getchannel('A'))),
'original_hidden_native_slots_still_empty':not any(np.any(np.asarray(im)[:,:,3]) for name,im in seq if name.endswith('EMPTY')),
'all_pose_same_canvas':all(Image.open(OUT/f'CP360_with_patch_angle_{deg}_QA.png').size==(W,H) for deg in [0,1,2,4]),
'zero_art_release_claim':True,
}
assert all(checks.values()),checks
report={'checkpoint':'CP360','status':'TWO_TINY_NATIVE_VECTOR_STUDIES_VISUAL_REVIEW_REQUIRED','source_reference_size':[W,H],
'work_resolution_of_two_vector_studies':[1290,2694], 'ORA_canvas':[W,H],
'original_approved_full_character_native_highres_layers_complete':False,
'new_small_original_underpaint_studies':2,'blank_full_semantic_slots':2,
'production_sprite_ready':False,'spine_ready':False,'apk_art_integrated':False,
'visual_qa':'NOT_PASSED','release_gate':'blocked_pending_art','sprite_paths':{},
'roi_note':'The polygons are selected seam QA regions, not confirmed anatomical holes; finger movement is expected to vacate old pixels.',
'angles_deg':poses,'technical_checks':{k:bool(v) for k,v in checks.items()}}
(OUT/'CP360_METRICS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['CP360_HIDDEN_SKIN_PAINT_STUDY.svg','CP360_HIDDEN_BODICE_PAINT_STUDY.svg']:
 assert (OUT/name).exists()
readme='''# TVK CP360 — Original vector underpaint study / NOT production art

What was actually authored:
- two small new Bezier gradient vector shapes (skin at left shoulder; hidden blue-white bodice fold) on 1290x2694 canvas; NOT derived by simple upscaling of RGB pixels.
- clipped within the genuinely occluded portion of the existing 215x449 arm source, to keep idle image pixel-exact.
- source material separated into six independently editable RGBA layers from CP359 and two deliberately EMPTY wider native semantic slots.
- OpenRaster containing 19 editable low-res guide / partial-paint layers. The **full final character** remains low-resolution! Two isolated vector underpaints alone cannot pass art acceptance.
- same-camera, same pivot -1/-2/-4 test frames. Alpha-coverage loss in the finger region is expected and not necessarily a seam hole.

Key conclusion: these two local studies **do not** reconstruct complete anatomy, hidden garment or animated rig. Needs artist visual review and a full native high-res independent source for actual production. CANON V2.1 is untouched, release blocked_pending_art.

Run `python build_cp360.py --cp348-zip CP348.zip --cp359-zip CP359.zip --canon CANON.png --out output_dir` with the exact locked inputs. Requires Pillow, numpy, opencv-python, cairosvg.
'''
(OUT/'README_CP360.md').write_text(readme,encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
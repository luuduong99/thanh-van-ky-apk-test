#!/usr/bin/env python3
"""CP361: editable native-vector *local* hidden-shoulder illustration study. NOT an approved game sprite."""
from pathlib import Path
import argparse,hashlib,json,io,zipfile,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import cairosvg

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--canon',type=Path,required=True)
parser.add_argument('--cp348-zip',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args()
OUT=args.out; OUT.mkdir(parents=True,exist_ok=True)
CANON=args.canon
CP348=args.cp348_zip
CANON_SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CP348_SHA='f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497'
assert hashlib.sha256(CANON.read_bytes()).hexdigest()==CANON_SHA
assert hashlib.sha256(CP348.read_bytes()).hexdigest()==CP348_SHA
S=6;W,H=215*S,449*S
with zipfile.ZipFile(CP348) as z:
 assert z.testzip() is None
 names=sorted(n for n in z.namelist() if n.startswith('layers/') and n.endswith('.png'))
 originals=[Image.open(io.BytesIO(z.read(n))).convert('RGBA') for n in names]
 flat=Image.open(io.BytesIO(z.read('FRONT_CP348_TEN_LAYER_RECON_QA_ONLY.png'))).convert('RGBA')
assert len(originals)==10
# Editable paint geometry uses true 1290x2694 rasterization (6x original source's view box).
# The untouched source layers are still low-res upscaled; this is a LOCAL art study, not full HD redraw.
shapes={
'01_hidden_shoulder_skin': '''
<path d="M62 122 Q68 121 72 126 C77 131 76.5 141 74 149 Q71 155 69 161 C66 157 62 153 60 148 C58 141 58.8 130 62 122Z" fill="url(#skin)" stroke="#d7aaa6" stroke-width=".4"/>
<path d="M61 128 C63.8 125.5 68 125.8 70.7 130" fill="none" stroke="#fff7eb" stroke-width="1.6" opacity=".68"/>
<path d="M73 133 C74 140 72.2 146 69.8 151" fill="none" stroke="#cba7a5" stroke-width="1.05" opacity=".48"/>
<path d="M62.8 145 Q65 150 69 153" fill="none" stroke="#e8bdb5" stroke-width=".6" opacity=".67"/>
''',
'02_hidden_bodice_inner_fabric': '''
<path d="M62 146 C67 145 72 146 76.5 152 Q80 159 78.5 166 C77 174 73 181 70.8 189 C67 179 63 177 60.2 169 Q58 158 62 146Z" fill="url(#fabric)" stroke="#7799cb" stroke-width=".45"/>
<path d="M62.3 147 Q69 153 70.5 166 T70.5 186" fill="none" stroke="#ffffff" stroke-width="1.75" opacity=".62"/>
<path d="M74 152 Q73 166 74 178" fill="none" stroke="#597fc1" stroke-width="1.1" opacity=".43"/>
<path d="M66 152 C64 157 64.5 166 67 173" fill="none" stroke="#a8bbdf" stroke-width="1.05" opacity=".68"/>
''',
'03_rear_silk_underarm': '''
<path d="M47 145 C54 144 63 148 67.2 154 C68 164 67.6 177 66.5 188 C62 197 57 205 53 214 C54.5 200 50.3 189 47.7 178 C43.5 164 43 152 47 145Z" fill="url(#silk)" stroke="#668cc7" stroke-width=".65"/>
<path d="M49 151 C54 158 56 169 55 185 Q58 196 55 206" fill="none" stroke="#f8fbff" stroke-width="1.6" opacity=".75"/>
<path d="M61 154 C62 166 63 174 59 190" fill="none" stroke="#406ab8" stroke-width="1.25" opacity=".38"/>
<path d="M48 153 C49.8 165 50.5 174 49 181" fill="none" stroke="#ccdefa" stroke-width=".85" opacity=".7"/>
''',
'04_rear_hair_overlap': '''
<path d="M52 113 C58 120 63 131 65 145 C66 157 64 167 60 179 C58 171 56 160 53 151 C51 138 48 124 52 113Z" fill="url(#hair)" stroke="#8b87ae" stroke-width=".6"/>
<path d="M53.4 119 C57.8 128 60 139 61.3 150" fill="none" stroke="#faf5ff" stroke-width="1.1" opacity=".73"/>
<path d="M51.5 131 C54.8 140 57.2 152 58.8 165" fill="none" stroke="#bbc6e7" stroke-width="1.1" opacity=".8"/>
<path d="M61.4 140 Q64 151 60.2 169" fill="none" stroke="#6e7aaf" stroke-width=".8" opacity=".5"/>
'''
}
def svg(body):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1290" height="2694" viewBox="0 0 215 449">
 <defs>
  <linearGradient id="skin" x1="0" y1="0" x2="1" y2=".2"><stop offset="0" stop-color="#e8b8b3"/><stop offset=".25" stop-color="#fff1e7"/><stop offset=".64" stop-color="#ffebe1"/><stop offset="1" stop-color="#cf9ca0"/></linearGradient>
  <linearGradient id="fabric" x1=".1" y1="0" x2=".85" y2="1"><stop offset="0" stop-color="#6f9bd1"/><stop offset=".34" stop-color="#f9faff"/><stop offset=".66" stop-color="#b5cdf1"/><stop offset="1" stop-color="#4f7bc2"/></linearGradient>
  <linearGradient id="silk" x1="0" y1="0" x2="1" y2=".1"><stop offset="0" stop-color="#b8cdf7"/><stop offset=".35" stop-color="#e6f0ff"/><stop offset=".64" stop-color="#91afe7"/><stop offset="1" stop-color="#4e82d0"/></linearGradient>
  <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a9a7d1"/><stop offset=".34" stop-color="#f0eaff"/><stop offset=".65" stop-color="#c4c4e4"/><stop offset="1" stop-color="#7d88b3"/></linearGradient>
 </defs>{body}</svg>'''

hi_parts=[]
for name,body in shapes.items():
 content=svg(body)
 (OUT/f'CP361_{name}.svg').write_text(content,encoding='utf-8')
 png=cairosvg.svg2png(bytestring=content.encode(),output_width=W,output_height=H)
 high=Image.open(io.BytesIO(png)).convert('RGBA')
 assert np.max(np.asarray(high)[:,:,3])>0
 high.save(OUT/f'CP361_{name}_EDITABLE_PAINT_HIGHRES.png')
 hi_parts.append((name,high))

# Keep originally approved visible pixels identical at rest. Underpaint is behind opaque
# original source-arm texture and only revealed during arm movement. This test does not
# establish that the newly imagined hidden anatomy/cloth is canon-correct.
original_hi=[p.resize((W,H),Image.Resampling.NEAREST) for p in originals]
old_arm=np.asarray(original_hi[5])[:,:,3]
# Hard-clip to source arm's fully-opaque footprint, avoiding blue/skin artifacts outside
# existing silhouette in idle. Any part not behind the opaque source is deliberately hidden.
mask=(old_arm==255)
clipped=[]
for name,im in hi_parts:
 a=np.asarray(im).copy()
 a[:,:,3][~mask]=0
 art=Image.fromarray(a,'RGBA')
 clipped.append((name,art))
 art.save(OUT/f'CP361_{name}_UNDER_ARM_QA.png')

# Existing rest: other parts are painted atop/beneath the arm in known, static order.
def composite(arm,with_art=True):
 base=Image.new('RGBA',(W,H))
 for k,p in enumerate(original_hi):
  if k==5:
   if with_art:
    for _,patch in clipped:base=Image.alpha_composite(base,patch)
   base=Image.alpha_composite(base,arm)
  else:base=Image.alpha_composite(base,p)
 return base
idle=composite(original_hi[5]);reference=flat.resize((W,H),Image.Resampling.NEAREST)
x=np.asarray(idle);y=np.asarray(reference)
assert np.array_equal(x[:,:,3],y[:,:,3])
assert np.array_equal(x[x[:,:,3]>0],y[y[:,:,3]>0])
# Dynamic same-camera source mockups, not rigging or designed artist animation poses.
poses={}; rendered={}
for deg in (0,-2,-4,-7):
 moved=original_hi[5].rotate(deg,Image.Resampling.BICUBIC,center=(70*S,132*S)) if deg else original_hi[5]
 before=composite(moved,False);after=composite(moved,True)
 before.save(OUT/f'CP361_ANGLE_{abs(deg)}_BEFORE_STUDY_QA.png')
 after.save(OUT/f'CP361_ANGLE_{abs(deg)}_WITH_ART_STUDY_QA.png')
 src=np.asarray(reference)[:,:,3];b=np.asarray(before)[:,:,3];a=np.asarray(after)[:,:,3]
 # ROI source pixels (all original source scale): only substantive torso seam area.
 roi=np.zeros(src.shape,bool);roi[119*S:191*S,42*S:84*S]=1
 lost_before=int(((src>127)&(b<25)&roi).sum());lost_after=int(((src>127)&(a<25)&roi).sum())
 newly_visible=int(np.sum((a>127)&(b<25)&roi))
 poses[str(abs(deg))]={"source_seam_roi_lost_before_6x_px":lost_before,"source_seam_roi_lost_after_6x_px":lost_after,"patch_revealed_6x_px":newly_visible}
 rendered[deg]=(before,after)

# Create clear preview with small thumbnails (against true original source style).
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(font_path,20)
font_big=ImageFont.truetype(font_path,26)
B=Image.new('RGB',(1250,880),'#e7edf5');draw=ImageDraw.Draw(B)
draw.text((25,15),'CP361 | local semantic shoulder art studies (NOT approved)',font=font_big,fill='#203650')
draw.text((25,53),'Same-view transforms at -2 and -7 degrees; original CP348 still low resolution',font=font,fill='#51667c')
for row,deg in enumerate((-2,-7)):
 for col,which in enumerate(('before','after')):
  im=rendered[deg][0 if col==0 else 1]
  crop=im.crop((22*S,112*S,99*S,207*S)).resize((295,365),Image.Resampling.LANCZOS)
  bg=Image.new('RGB',crop.size,'#cfd9e8');bg.paste(crop,(0,0),crop)
  xpos=115+col*480;ypos=90+row*385
  B.paste(bg,(xpos,ypos))
  draw.text((xpos,ypos+366),f'{abs(deg)}deg | '+('source' if col==0 else 'art study'),font=font,fill='#233750')
# difference truth text
draw.text((930,120),'QA status',font=font_big,fill='#213650')
draw.text((930,169),'Tech: pending',font=font,fill='#43637f')
draw.text((930,204),'Visual: NOT PASS',font=font,fill='#b14639')
draw.text((930,240),'Spine: NOT READY',font=font,fill='#b14639')
draw.text((930,278),'APK: BLOCKED',font=font,fill='#b14639')
B.save(OUT/'CP361_SHOULDER_NEW_ART_STUDY_PREVIEW.png')

# Create editable 1290x2694 ORA: 10 unchanged enlarged sources + four new native sampled art studies
# Four original vector shapes remain separately editable as .svg in the ZIP and paint rasters in ORA.
ordered=[]
for k,p in enumerate(original_hi):
 if k==5:ordered.extend((f'CP361__{name}__NEW_LOCAL_ART',im) for name,im in clipped)
 ordered.append((f'CP348__{Path(names[k]).stem}__LOWRES_SOURCE_6X',p))
assert len(ordered)==14
root=ET.Element('image',{'w':str(W),'h':str(H),'name':'CP361_LOCAL_ART_VECTORS_OVER_LOWRES_SOURCE_NOT_SPINE','version':'0.0.3'})
stack=ET.SubElement(root,'stack')
ora=OUT/'CP361_EDITABLE_14_LAYER_HIGH_CANVAS_ART_STUDY_NOT_RIG.ora'
with zipfile.ZipFile(ora,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 z.writestr('mimetype',b'image/openraster',compress_type=zipfile.ZIP_STORED)
 for j,(name,im) in enumerate(reversed(ordered)):
  stream=io.BytesIO();im.save(stream,format='PNG')
  entry=f'data/layer{j:02d}.png';z.writestr(entry,stream.getvalue())
  ET.SubElement(stack,'layer',{'name':name,'src':entry,'opacity':'1.0','visibility':'visible','x':'0','y':'0','composite-op':'svg:src-over'})
 z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
 stream=io.BytesIO();idle.save(stream,format='PNG');z.writestr('mergedimage.png',stream.getvalue())
assert zipfile.ZipFile(ora).testzip() is None

metrics={
'checkpoint':'CP361', 'date':'2026-10-29',
'canonical_original_sha256':CANON_SHA,'original_cp348_archive_sha256':CP348_SHA,
'canvas':[W,H],'original_character_source':[215,449],
'new_editable_vector_art_components':list(shapes.keys()),'new_highres_vector_components':4,
'complete_highres_character_semantic_art':False,'approved_sprite':False,'spine_ready':False,
'production_release':'blocked_pending_art','sprite_paths':{},
'original_visible_pixels_at_rest_unchanged':True,
'pose_type':'rigless grouped-arm raster rotation; NOT designed matching highres keyframe art',
'pose_diagnostics':poses,
'alpha_note':'Lost source coverage is not automatically a hole; hand/sleeve silhouette moves naturally.',
'visual_qa':'NOT_PASSED: colors and seam require artist review',
'ora':ora.name,
}
(OUT/'CP361_REPORT.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks={
'CANON_SHA_locked':hashlib.sha256(CANON.read_bytes()).hexdigest()==CANON_SHA,
'CP348_SHA_locked':hashlib.sha256(CP348.read_bytes()).hexdigest()==CP348_SHA,
'4_nonempty_authored_components':len(hi_parts)==4 and all(np.any(np.array(im)[:,:,3]) for _,im in hi_parts),
'clipped_only_inside_existing_arm':all(np.count_nonzero(np.array(im)[:,:,3][~mask])==0 for _,im in clipped),
'pixel_exact_rest_alpha':np.array_equal(x[:,:,3],y[:,:,3]),
'pixel_exact_rest_visible_color':np.array_equal(x[x[:,:,3]>0],y[y[:,:,3]>0]),
'same_canvas_all_pose_outputs':all(img.size==(W,H) for pair in rendered.values() for img in pair),
'nonzero_raised_pose_change':np.any(np.array(rendered[-7][0])!=x),
'ora_zip_crc':zipfile.ZipFile(ora).testzip() is None,
'ora_14_layers':len(ordered)==14,
'no_runtime_release_claim':metrics['production_release']=='blocked_pending_art' and not metrics['approved_sprite'],
'no_spine_claim':metrics['spine_ready'] is False,
}
assert all(checks.values()),checks
metrics['technical_checks']={k:bool(v) for k,v in checks.items()}
(OUT/'CP361_REPORT.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'README.md').write_text('''# CP361 / art production research — NOT RIG / NOT PRODUCTION

This handoff contains FOUR newly authored SVG Bézier/gradient shoulder underlay components at 1290x2694 pixels: hidden shoulder skin, bodice inner fabric, rear silk and rear hair. Source CP348 full figure is STILL an enlarged 215x449 source, so **this is NOT a new high-resolution character**. The four regions were clipped beneath the original opaque arm, retaining exact idle visible pixels. Moving arm mockups use a temporary rotated grouped raster, NOT artist-painted arm-up pose keyframes; no Spine skeleton.

The path geometry is a draft hypothesis of what is behind the original sleeve; it is not recoverable ground-truth art. Review the -2/-7 same-view images for bad fold transitions and cut lines. No acceptable native full-body sprite exists yet. CANON V2.1 unchanged. Full release remains blocked_pending_art.

The package includes an editable 14-layer OpenRaster, four SVG source paths and their native sampled RGBA paint layers. To view just new art, open the SVG or PNG files individually. Never feed the ORA into a production runtime as though CANON art was complete. Verify any edits with side-by-side same-camera rest and raised-arm captures; redo painter-grade shoulder/cloth/hair before animation.
''',encoding='utf-8')
manifest={}
for p in sorted(OUT.iterdir()):
 if p.is_file():manifest[p.name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
# Don't embed huge redundant rendered frames in bundle: only necessary QA/keyframes and original SVG/art masters.
keep=['README.md','CP361_REPORT.json','CP361_SHOULDER_NEW_ART_STUDY_PREVIEW.png','CP361_EDITABLE_14_LAYER_HIGH_CANVAS_ART_STUDY_NOT_RIG.ora',
      'CP361_ANGLE_0_WITH_ART_STUDY_QA.png','CP361_ANGLE_2_WITH_ART_STUDY_QA.png','CP361_ANGLE_7_WITH_ART_STUDY_QA.png','MANIFEST.json','build_cp361.py']
keep+=sorted(p.name for p in OUT.glob('CP361_0*_*.svg'))
keep+=sorted(p.name for p in OUT.glob('CP361_0*_EDITABLE_PAINT_HIGHRES.png'))
package=OUT.parent/'TVK_CP361_Shoulder_Vector_Art_Study_NOT_SPINE.zip'
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in keep:z.write(OUT/name,name)
assert zipfile.ZipFile(package).testzip() is None
print(json.dumps({'report':metrics,'zip':str(package),'zip_sha256':hashlib.sha256(package.read_bytes()).hexdigest(),'file_count':len(keep)},indent=2))
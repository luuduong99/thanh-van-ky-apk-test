from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import hashlib, json, io, zipfile, xml.etree.ElementTree as ET, shutil, textwrap

ROOT=Path('/mnt/data/TVK_LamThien_CP343_Front_Semantic_Region_Study')
for x in ['source','layers','masks','preview','ora','tests','tools']:(ROOT/x).mkdir(parents=True,exist_ok=True)
SRC=Path('/mnt/data/TVK_LamThien_CP342_Front_Alpha_Shadow_Cleanup/source/FRONT_CP342_FLOOR_CLEAN_ALPHA_NOT_RIG.png')
CAN=Path('/mnt/data/TVK_LamThien_CANON_V2_1_20261029/LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
CANSHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
assert hashlib.sha256(CAN.read_bytes()).hexdigest()==CANSHA
src=Image.open(SRC).convert('RGBA'); w,h=src.size;assert (w,h)==(215,449)
source=np.array(src)

def pol(points):
    mask=Image.new('1',(w,h),0); ImageDraw.Draw(mask).polygon(points,fill=1);return np.asarray(mask).astype(bool)

def ell(bounds):
    mask=Image.new('1',(w,h),0);ImageDraw.Draw(mask).ellipse(bounds,fill=1);return np.asarray(mask).astype(bool)

# An editable topological study, not physical mesh segmentation. The exact native
# source RGB is never repainted, and pieces can be recomposed losslessly at rest.
labels=np.full((h,w),-1,dtype=np.int16)
parts=[
 ('01_outer_left_hair_and_silk','outer_left',  '#4f8aca'),
 ('02_outer_right_hair_and_silk','outer_right','#6ca0cc'),
 ('03_left_leg_and_shoe','leg_left','#c28a9a'),
 ('04_right_leg_and_shoe','leg_right','#e0a3a4'),
 ('05_waist_center_fabric','waist','#80bdd3'),
 ('06_left_arm_and_sleeve','arm_left','#9a83c4'),
 ('07_right_arm_and_sleeve','arm_right','#8b6ec9'),
 ('08_bodice_and_necklace','bodice','#c9a452'),
 ('09_head_hair_front_and_ornament','head','#dc9c6a'),
 ('10_small_unassigned_transition','seam_residual','#777777'),
]
# Topological region hints. They were hand-placed while visually inspecting a
# coordinate grid of the *unchanged* 215x449 native source image.
labels[:,:w//2]=0;labels[:,w//2:]=1
# legs and shoes, central clothing and proportions anchored to original crop
for ind,pts in [
 (2,[(76,227),(105,224),(110,275),(109,355),(102,420),(95,441),(80,439),(82,392),(74,370),(73,293)]),
 (3,[(106,222),(137,220),(146,289),(138,365),(132,403),(123,439),(106,441),(105,385),(104,325)]),
 (4,[(65,171),(101,168),(139,168),(154,193),(141,224),(112,270),(107,277),(78,232),(61,200)]),
 (5,[(20,125),(45,115),(74,126),(87,156),(75,184),(52,202),(8,201),(0,191),(8,160)]),
 (6,[(195,124),(170,111),(140,124),(126,158),(139,189),(170,203),(211,199),(214,192),(204,160)]),
 (7,[(76,76),(99,73),(124,74),(143,87),(149,123),(139,164),(131,180),(86,182),(70,159),(70,122)]),
 (8,[(81,0),(121,0),(143,22),(153,51),(140,80),(128,94),(91,94),(69,80),(65,54),(70,23)])
]: labels[pol(pts)]=ind
# residual lane near 2 sleeve/torso junction where downstream artist must manually
# assign occlusion and paint underlayers. Narrow labels used as flags, not bones.
for pts in [[(72,159),(79,160),(82,196),(72,202),(67,178)],[(140,161),(146,166),(148,197),(140,200),(136,180)]]:
    labels[pol(pts)]=9

rgba=source.copy(); alpha=rgba[:,:,3]
# For all nontransparent pixels, assign one source pixel to exactly one layer.
rgba[alpha==0,0:3]=0
outpaths=[]; maskpaths=[]; pixel_counts={}
for k,(filename,human,color) in enumerate(parts):
    bitmap=(labels==k)&(alpha>0)
    part=np.zeros_like(rgba);part[bitmap]=rgba[bitmap]
    output=Image.fromarray(part,'RGBA')
    rel=f'layers/{filename}.png';output.save(ROOT/rel);outpaths.append(rel)
    mask=Image.fromarray((bitmap.astype('uint8')*255),'L');mr=f'masks/{filename}_mask.png';mask.save(ROOT/mr);maskpaths.append(mr)
    pixel_counts[filename]=int(bitmap.sum())

# Reconstruct exact alpha and RGB for all visible (alpha>0) pixels.
recon=np.zeros_like(rgba)
for rel in outpaths:
    a=np.asarray(Image.open(ROOT/rel).convert('RGBA'))
    active=a[:,:,3]>0
    assert not np.any((recon[:,:,3]>0)&active)
    recon[active]=a[active]
assert np.array_equal(recon[:,:,3],source[:,:,3])
assert np.array_equal(recon[source[:,:,3]>0],source[source[:,:,3]>0])
Image.fromarray(recon,'RGBA').save(ROOT/'source/FRONT_CP343_AT_REST_EXACT_RECOMPOSITION.png')
shutil.copy2(SRC,ROOT/'source/FRONT_CP342_SOURCE_LOCKED.png')

# Review on checkerboard: original, recomposition, and anatomical intent map.
scale=2
W,H=440,945
board=Image.new('RGB',(W*3+80,H+90),(246,248,253));d=ImageDraw.Draw(board)
def chess(size):
    im=Image.new('RGBA',size,(245,245,245,255));dr=ImageDraw.Draw(im)
    for y in range(0,size[1],18):
      for x in range(0,size[0],18):
        if (x//18+y//18)%2==0:dr.rectangle((x,y,x+17,y+17),fill=(212,216,225,255))
    return im
base=chess((w,h));orig=Image.alpha_composite(base,src);reco=Image.alpha_composite(base,Image.fromarray(recon,'RGBA'))
for ii,(pic,header) in enumerate([(orig,'CANON V2.1 / CP342 source'),(reco,'CP343 exact rest composite')]):
    board.paste(pic.resize((w*2,h*2),Image.Resampling.NEAREST).convert('RGB'),(W*ii+12,44))
    d.text((W*ii+12,15),header,fill=(19,44,83))
map_img=np.zeros((h,w,3),dtype=np.uint8)+236
for k,(_,_,color) in enumerate(parts):
    col=tuple(int(color[j:j+2],16) for j in (1,3,5))
    mask=(labels==k)&(alpha>0)
    map_img[mask]=col
seg=Image.fromarray(map_img,'RGB')
board.paste(seg.resize((w*2,h*2),Image.Resampling.NEAREST),(W*2+12,44))
d.text((W*2+12,15),'CP343 provisional move-region masks',fill=(19,44,83))
for xx in (W,W*2):d.line((xx,5,xx,930),fill=(185,194,210),width=2)
board.save(ROOT/'preview/CP343_CANON_SOURCE_EXACT_LAYER_MAP_QA.png')

# Pixel QA diagnostic collage; colored parts are not actual painted layers.
legend=Image.new('RGB',(1100,620),'white');ld=ImageDraw.Draw(legend)
ld.text((16,16),'CP343 | Provisional layered pixels (NOT SPINE-READY)',fill='#153254')
ld.text((16,46),'All RGB/alpha pixels recompose exactly at rest; no invisible underpaint.',fill='#385476')
for i,(filename,human,color) in enumerate(parts):
    left=20+(i%2)*545;top=82+(i//2)*102
    ld.rectangle((left,top,left+24,top+24),fill=color)
    ld.text((left+38,top+3),filename,fill='#283b5b')
    ld.text((left+38,top+31),f'{pixel_counts[filename]:,} source pixels | needs manual edges / occlusion',fill='#687891')
legend.save(ROOT/'preview/CP343_LAYER_REGION_LEGEND.png')

# Native ORA. Each layer has a real disjoint rasterized source region and can
# be toggled independently, but it lacks source paint behind the separations.
ora=ROOT/'ora/CP343_FRONT_REGION_LAYERS_EDITABLE_NOT_RIG.ora'
(ora.parent).mkdir(exist_ok=True)
image=ET.Element('image',{'version':'0.0.3','w':str(w),'h':str(h),'name':'CP343 Source Exact Regions - NOT SPINE READY'})
stack=ET.SubElement(image,'stack')
ora_png={}
# top-to-bottom semantic regions; no overlap, order doesn't affect appearance
for idx in reversed(range(len(parts))):
 name=parts[idx][0]; src_path=outpaths[idx];key=f'data/layer{idx:02d}.png'
 ET.SubElement(stack,'layer',{'name':name,'src':key,'x':'0','y':'0','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over'})
 ora_png[key]=(ROOT/src_path).read_bytes()
xml=ET.tostring(image,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(ora,'w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 z.writestr('stack.xml',xml)
 for p,b in ora_png.items():z.writestr(p,b)
 z.write(ROOT/'source/FRONT_CP343_AT_REST_EXACT_RECOMPOSITION.png','mergedimage.png')
 z.write(ROOT/'source/FRONT_CP343_AT_REST_EXACT_RECOMPOSITION.png','Thumbnails/thumbnail.png')
assert zipfile.ZipFile(ora).testzip() is None

manifest={
 'checkpoint':'CP343','date':'2026-10-29',
 'status':'source_exact_provisional_semantic_regions_not_riggable',
 'approved_canon_id':'LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29',
 'approved_source_sha256':CANSHA,
 'native_cutout_size':[w,h],
 'previous_cp342_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
 'region_count':len(parts),
 'region_assignments':[
  {'name':parts[i][0],'description':parts[i][1],'color':parts[i][2],'visible_pixels':pixel_counts[parts[i][0]],'png':outpaths[i],'mask':maskpaths[i],
  'png_sha256':hashlib.sha256((ROOT/outpaths[i]).read_bytes()).hexdigest()}
  for i in range(len(parts))],
 'visible_source_pixels':int(np.count_nonzero(alpha>0)),
 'visible_recomposition_is_pixel_exact':True,
 'underpaint_for_motion_exists':False,
 'semantic_borders_artist_verified':False,
 'high_resolution_repaint_exists':False,
 'riggable_layers_ready':False,'spine_verified':False,'apk_verified':False,
 'android_production_release':'blocked_pending_art',
 'game_sprite_paths_registered':0,
 'ora':'ora/CP343_FRONT_REGION_LAYERS_EDITABLE_NOT_RIG.ora',
 'qa_preview':'preview/CP343_CANON_SOURCE_EXACT_LAYER_MAP_QA.png',
 'notes':['10 editable mutually-exclusive move-region images preserve exact source pixels; masks approximate by hand-placed geometric topology.',
          'Do not animate separated pieces directly. Straight/angled boundaries and missing occluded body fabric/hair require artist redraw, mask refinements and underpaint.',
          'Source native raster is 215x449 and cannot yield true native high-res with resizing.',
          'No change to body proportion, bodice, 5 emotions or integrity 100/70/50/30.']
}
(ROOT/'CP343_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

(ROOT/'README.md').write_text('''# CP343 — Editable Front Move-region Study (NOT RIG READY)\n\nThe exact approved Lâm Thiển CANON V2.1 remains unchanged (SHA256 f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a).\n\nThe 215x449 CP342 Front flat foreground has been split into 10 disjoint, independently editable region PNGs and a 10-layer OpenRaster. Recomposition at rest is pixel-exact (for all visible pixels). These are *approximate source-pixel partitions*, not artist-drawn, joint-ready anatomy or physics parts.\n\nThe contour boundaries are mostly manually placed polygons and will show sharp seams when moved. The mask images can be manually edited in Krita/GIMP; art must be repainted with hidden underpaint/occluded anatomy before motion.\n\nThe preview colour-map illustrates mask groups, not newly painted sprite art. There are no Spine skeletons or Android APK builds. Production sprite release remains blocked.\n\nNext: artist refines one arm/torso joint, repaints underlying shoulder/skin/sleeve and tests small movement for holes; only then can this move beyond static editable masks.\n''')
(ROOT/'ARTIST_TASKS.md').write_text('''# CP344 recommended painter workflow\n\n1. Open `ora/CP343_FRONT_REGION_LAYERS_EDITABLE_NOT_RIG.ora` in Krita; use the CANON V2.1 full sheet and extracted Front as locked references. Avoid treating the 10 coarse masks as final silhouette or bones.\n2. Manually clean edges at left/right arm+sleeve joints; correct occlusion (separate hair from sleeves) with new alpha brushwork. Add **true body/skin/clothing pixels underneath** when those parts rotate.\n3. Repaint at *native larger canvas by drawing*, not upscaling. Match body +17% baked into V2.1, face, the final bodice and white/blue/gold palette. Tweak optional redundant tassels only; preserve signature ribbon/flower assets.\n4. Export a first true multi-part Front master with eyes / mouth separate, then assess 2 small sleeve rotations using the identical background and compare rest pose to CANON.\n5. Validate 5 approved expressions and four integrity states after a single Front physical art pass. 30% dirt/scuff/tear must stay restrained.\n6. Keep `production_release=blocked_pending_art` and sprite_paths empty until explicit user acceptance of actual completed art.\n''')
print('ROOT',ROOT,'parts',pixel_counts,'visible',np.count_nonzero(alpha>0),'ora',ora)
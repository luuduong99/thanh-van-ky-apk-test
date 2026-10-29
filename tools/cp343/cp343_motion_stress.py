from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
R=Path('/mnt/data/TVK_LamThien_CP343_Front_Semantic_Region_Study')
src=Image.open(R/'source/FRONT_CP342_SOURCE_LOCKED.png').convert('RGBA')
parts=sorted((R/'layers').glob('*.png'))
render=Image.new('RGBA',src.size,(0,0,0,0))
for p in parts:
 im=Image.open(p).convert('RGBA')
 if 'left_arm' in p.name:dx,dy=-10,5
 elif 'right_arm' in p.name:dx,dy=10,5
 else:dx,dy=0,0
 layer=Image.new('RGBA',src.size,(0,0,0,0));layer.paste(im,(dx,dy));render=Image.alpha_composite(render,layer)
a=np.array(src)[:,:,3];b=np.array(render)[:,:,3]
hole=(a>127)&(b<25)
excess=(a<25)&(b>127)
# Draw missing underpaint in red, extrusions in yellow; this is a failure diagnostic.
hlight=np.array(render).copy()
hlight[hole]=[240,45,65,255]
hlight[excess]=[238,172,28,255]
colored=Image.fromarray(hlight,'RGBA')
w,h=src.size
canvas=Image.new('RGB',(w*3*2+70,h*2+110),'#f8fafc');draw=ImageDraw.Draw(canvas)
def checker():
 im=Image.new('RGBA',(w,h),'#f8f8f8');dr=ImageDraw.Draw(im)
 for y in range(0,h,14):
  for x in range(0,w,14):
   if (x//14+y//14)%2==0:dr.rectangle((x,y,x+13,y+13),fill='#d8dce6')
 return im
bg=checker()
for i,(image,label) in enumerate([(src,'EXACT source at rest'),(render,'Arm masks moved 10px (not production)'),(colored,'RED = missing paint; YELLOW = overlap/outside')]):
 x=i*(w*2+22)+10
 draw.text((x,16),label,fill='#0e365c')
 canvas.paste(Image.alpha_composite(bg,image).resize((w*2,h*2),Image.Resampling.NEAREST).convert('RGB'),(x,50))
draw.text((10,h*2+65),f'UNDERPAINT GATE FAIL: {hole.sum():,} missing source pixels and {excess.sum():,} new protruding pixels after only moving arm masks.',fill='#9b263b')
canvas.save(R/'preview/CP343_ARTICULATION_UNDERPAINT_FAIL_QA.png')
m=json.loads((R/'CP343_MANIFEST.json').read_text())
m['arm_motion_stress_test']={'offset_left_px':[-10,5],'offset_right_px':[10,5], 'missing_source_pixels':int(hole.sum()),'new_protruding_pixels':int(excess.sum()), 'result':'FAIL_no_hidden_underpaint','diagnostic_preview':'preview/CP343_ARTICULATION_UNDERPAINT_FAIL_QA.png'}
(R/'CP343_MANIFEST.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
print('missing',int(hole.sum()),'outside',int(excess.sum()))
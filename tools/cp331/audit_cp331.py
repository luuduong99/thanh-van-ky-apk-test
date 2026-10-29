#!/usr/bin/env python3
"""Audit CP331 Library-backed ORA files; strict mode refuses unapproved art.

Real pixel audit checks all 5 ORAs, alpha, hidden source, same flat master,
independent crop placements, compositing and pixel invariance outside face ROI.
Does NOT claim generated art matches approved character or is Spine compatible.
"""
import io, hashlib, json, zipfile, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageDraw
from xml.etree import ElementTree as ET

PARTS=('brow_image_left','brow_image_right','eye_image_left','eye_image_right','mouth','blush_image_left','blush_image_right')
IDS=('shy','angry','pain','embarrassed','alluring')
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXPR_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def audit(dir):
 dir=Path(dir);data=json.loads((dir/'manifest.json').read_text())
 errors=[];notes=[];base_hashes=[];frames=[]
 if data.get('canonical_sha256')!=CANON_SHA:errors.append('Canon SHA mismatch')
 if data.get('approved_expression_sha256')!=EXPR_SHA:errors.append('Approved emotion SHA mismatch')
 if data.get('status')!='shared_face_master_technical_trial_unapproved_not_spine_ready':errors.append('Status mismatch')
 if [x['id'] for x in data['results']]!=list(IDS):errors.append('Five expression IDs missing/wrong order')
 if data.get('asset_registration_allowed') or data.get('spine_ready') or data.get('apk_verified'):errors.append('Forbidden production flag')
 if not data.get('flat_master_contains_baked_facial_features'):errors.append('Must declare baked-in face layer limitation')
 if not (dir/'reference'/'FIVE_EMOTIONS_ALREADY_APPROVED.png').is_file() or sha(dir/'reference'/'FIVE_EMOTIONS_ALREADY_APPROVED.png')!=EXPR_SHA:errors.append('Approved image provenance broken')
 for item in data['results']:
  name=item['id'];p=dir/'ora'/f'CP331_{name}_SHARED_FACE_TECH_TRIAL_NOT_GAME_ART.ora'
  if not p.exists():errors.append(f'Missing {p.name}');continue
  if sha(p)!=item['ora_sha256']:errors.append(f'ORA SHA mismatch {name}');continue
  try:
   with zipfile.ZipFile(p) as z:
    if z.testzip():errors.append('ZIP CRC failure '+name)
    if z.read('mimetype')!=b'image/openraster':errors.append('MIME failure '+name)
    root=ET.fromstring(z.read('stack.xml'))
    if [root.attrib.get('w'),root.attrib.get('h')]!=['258','364']:errors.append('Dimensions '+name)
    ls=root.findall('./stack/layer'); imgs=[]
    for x in ls:
     im=Image.open(io.BytesIO(z.read(x.attrib['src']))).convert('RGBA')
     if im.size!=(258,364):errors.append('layer dimensions '+name)
     imgs.append((x.attrib['name'],im,x.attrib['visibility']=='visible'))
    if len(ls)!=10:errors.append('Wrong ORA layer count '+name)
    if set(x[0] for x in imgs[:7])!=set(PARTS):errors.append('Wrong facial parts '+name)
    if any(not x[2] for x in imgs[:8]):errors.append('Visible art unexpectedly hidden '+name)
    if any(x[2] for x in imgs[8:]):errors.append('Guides/placeholder should be hidden '+name)
    if not all(np.count_nonzero(np.array(x[1].getchannel('A')))>200 for x in imgs[:7]):errors.append('Empty face patch '+name)
    base_hashes.append(hashlib.sha256(imgs[7][1].tobytes()).hexdigest())
    merged=Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA')
    full=Image.new('RGBA',(258,364),(0,0,0,0))
    for _,im,vis in reversed(imgs):
     if vis:full=Image.alpha_composite(full,im)
    if ImageChops.difference(merged,full).getbbox():errors.append('ORA composite mismatch '+name)
    preview=Image.open(dir/'preview'/f'{name}_FIXED_FACE_COMPOSITE.png').convert('RGBA')
    if ImageChops.difference(merged,preview).getbbox():errors.append('ORA image preview mismatch '+name)
    frames.append(np.array(merged))
  except Exception as e:errors.append(f'Invalid ORA {name}: {e}')
 if len(set(base_hashes))!=1:errors.append('Each face does NOT use same flat base')
 if len(frames)==5:
  TARGET=list(data['target_region_boxes'].values())
  mask=Image.new('L',(258,364),0);d=ImageDraw.Draw(mask)
  for x0,y0,x1,y1 in TARGET:d.rectangle((x0-1,y0-1,x1+1,y1+1),fill=255)
  outside=np.array(mask)==0
  for i in range(1,len(frames)):
   if not np.array_equal(frames[0][outside],frames[i][outside]):errors.append('Background changed outside facial ROI')
  if all(np.array_equal(frames[0],f) for f in frames[1:]):errors.append('All 5 expressions identical')
 notes.append('This verifies SAME GENERATED FLAT BASE only; no V2 visual identity acceptance')
 notes.append('Eye and mouth are baked into flat base; foreground patches remain NON-SEMANTIC art')
 return errors,notes

def main():
 ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--strict',action='store_true');ap.add_argument('--json-output',type=Path);args=ap.parse_args()
 errors,notes=audit(args.directory)
 if args.strict:errors+=['STRICT ART GATE: CP331 is NOT an artist-approved high-resolution redraw, Spine/Android forbidden.']
 o={'passed':not errors,'errors':errors,'notes':notes,'strict':args.strict}
 print(json.dumps(o,ensure_ascii=False,indent=2))
 if args.json_output:args.json_output.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
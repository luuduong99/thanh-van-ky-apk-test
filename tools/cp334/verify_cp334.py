#!/usr/bin/env python3
"""Validate CP334 flat-candidate art review package (not production art)."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET
import zipfile

IDS = ['shy','angry','pain','embarrassed','alluring']
CANON_SHA = '41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXPRESSION_SHA = 'ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def audit(root):
    root=Path(root)
    m=json.loads((root/'CP334_ART_REVIEW_MANIFEST.json').read_text(encoding='utf-8'))
    problems=[]
    if m.get('checkpoint')!='CP334' or m.get('status')!='VISUAL_CONCEPT_REVIEW_PENDING_ART_ACCEPTANCE': problems.append('Wrong checkpoint or approval status')
    if m.get('canonical_sha256')!=CANON_SHA or sha(root/'source/CANON_V2_ORIGINAL.png')!=CANON_SHA: problems.append('CANON V2 SHA changed')
    if m.get('approved_expression_sha256')!=EXPRESSION_SHA or sha(root/'source/APPROVED_FIVE_EXPRESSION_GUIDE.png')!=EXPRESSION_SHA: problems.append('Approved expression sheet SHA changed')
    full=root/'source/CP334_GENERATED_FLAT_SHEET_NOT_APPROVED.png'
    if m.get('cp334_generated_flat_sheet_sha256')!=sha(full): problems.append('New candidate source changed')
    candidate=Image.open(full).convert('RGB')
    if [x['expression_id'] for x in m.get('candidate_pieces',[])]!=IDS: problems.append('Wrong emotion IDs')
    for item in m.get('candidate_pieces',[]):
        path=root/item['path']
        if not path.exists() or sha(path)!=item['sha256']: problems.append('Candidate crop/hash mismatch '+item['expression_id']);continue
        crop=Image.open(path).convert('RGB')
        expected=candidate.crop(tuple(item['source_box_xyxy']))
        if crop.size!=expected.size or crop.tobytes()!=expected.tobytes():problems.append('Candidate pixels changed '+item['expression_id'])
    ora=root/'CP334_VISUAL_REVIEW_WORKSPACE_NOT_RIG.ora'
    with zipfile.ZipFile(ora) as z:
        if z.testzip() is not None: problems.append('ORA has broken CRC')
        if z.read('mimetype')!=b'image/openraster':problems.append('ORA mimetype bad')
        stack=ET.fromstring(z.read('stack.xml')).find('stack')
        if len(stack.findall('layer'))!=7: problems.append('Review ORA must have 7 flat concept layers only')
        if 'mergedimage.png' not in z.namelist():problems.append('ORA missing composite')
        else:
            im=Image.open(io.BytesIO(z.read('mergedimage.png')))
            if im.size !=(2000,760):problems.append('ORA review canvas wrong size')
    for field in ('new_portrait_style_artist_approved','single_native_face_master_across_five','clean_independent_facial_attachments','clean_underpaint_verified','front_three_quarter_production_art','spine_rig_verified','apk_built_tested'):
        if m['qa_gates'].get(field) is not False:problems.append('Premature production approval: '+field)
    if m['qa_gates'].get('android_sprite_paths_registered')!=0:problems.append('Should not register sprite paths')
    return problems

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args()
    failures=audit(a.root)
    print(json.dumps({'checkpoint':'CP334','pass':not failures,'failures':failures,'production_art_approved':False},indent=2,ensure_ascii=False))
    raise SystemExit(1 if failures else 0)
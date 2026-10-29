#!/usr/bin/env python3
"""CP332: verify transparent semantic art layers in actual ORAs.

The technical pass certifies layer integrity, NOT V2 visual match or rig fitness.
Strict mode deliberately fails for a non-user-approved visual study.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import Counter
import argparse, io, json, hashlib, zipfile
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[1]
BASE=['hair_back','shoulders_costume','neck','ears','face_underpaint','nose_anchor','hair_front','hair_side_locks','flower_gold','choker_jewel']
PARTS=['blush_left','blush_right','eye_white_left','eye_white_right','iris_left','iris_right','eyelashes_left','eyelashes_right','eyelid_left','eyelid_right','brow_left','brow_right','mouth']
EMOTIONS=['shy','angry','pain','embarrassed','alluring']
CANON_SHA='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EXP_SHA='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'


def digest(content):return hashlib.sha256(content).hexdigest()

def inspect_ora(path):
    report={'path':str(path),'passed':False,'issues':[]}
    try:
        with zipfile.ZipFile(path) as arc:
            if arc.testzip() is not None:report['issues'].append('ZIP CRC failed')
            if arc.read('mimetype')!=b'image/openraster':report['issues'].append('MIME is not ORA')
            tree=ET.fromstring(arc.read('stack.xml'))
            if (int(tree.get('w','0')),int(tree.get('h','0'))) != (1024,1024):report['issues'].append('Canvas != 1024x1024')
            nodes=list(tree.find('stack').iter('layer'))
            names=[e.get('name') for e in nodes]
            if len(names)!=len(set(names)):report['issues'].append('Duplicate layer name')
            images={}
            for node in nodes:
                p=node.get('src','')
                if not p.startswith('data/') or not p.endswith('.png') or '..' in p:report['issues'].append('Untrusted entry path');continue
                if node.get('visibility')!='visible':report['issues'].append('Unexpected hidden art layer '+p)
                data=arc.read(p)
                im=Image.open(io.BytesIO(data));im.load()
                if im.mode!='RGBA' or im.size!=(1024,1024):report['issues'].append('Bad RGBA layer '+p)
                if im.getchannel('A').getbbox() is None:report['issues'].append('Empty alpha '+p)
                images[node.get('name')]=im
            composite=Image.new('RGBA',(1024,1024))
            for name in reversed(names):composite=Image.alpha_composite(composite,images[name])
            merged=Image.open(io.BytesIO(arc.read('mergedimage.png'))).convert('RGBA')
            if ImageChops.difference(composite,merged).getbbox() is not None:report['issues'].append('Merged image mismatch')
            report['names']=names;report['layers']=len(names);report['layer_hashes']={n:digest(images[n].tobytes()) for n in names}
            report['base_hashes']={n:report['layer_hashes'][n] for n in names if n.startswith('base_')}
            report['composite_sha256']=digest(merged.tobytes())
    except Exception as exc:report['issues'].append(str(exc))
    report['passed']=len(report['issues'])==0
    return report


def audit(root=ROOT):
    root=Path(root)
    manifest=json.loads((root/'manifest.json').read_text())
    errors=[];reports=[]
    if manifest['canonical_source_sha256']!=CANON_SHA:errors.append('CANON V2 checksum changed')
    if manifest['approved_expression_source_sha256']!=EXP_SHA:errors.append('Approved expression checksum changed')
    if manifest['pixel_sources_cut_from_flat_posters'] is not False:errors.append('Source is not newly drawn independent semantic layers')
    if manifest['base_baked_eyes_brows_mouth'] is not False:errors.append('Clean base should have no baked features')
    if manifest['asset_registration_allowed'] or manifest['spine_rig_complete'] or manifest['apk_verified']:errors.append('False production-ready status')
    baseline=None
    for e in EMOTIONS:
        r=inspect_ora(root/'ora'/f'CP332_{e.upper()}_SEMANTIC_NOT_APPROVED.ora');reports.append(r)
        errors.extend(f'{e}: {s}' for s in r['issues'])
        required=set('base_'+b for b in BASE)|set('expr_'+e+'_'+part for part in PARTS)
        if set(r.get('names',[]))!=required:errors.append(f'{e}: layer names differ from semantic contract')
        if r.get('layers')!=23:errors.append(f'{e}: expected 23 independently stored layers')
        if baseline is None:baseline=r.get('base_hashes',{})
        elif r.get('base_hashes',{})!=baseline:errors.append(f'{e}: master base layer bytes changed across expression')
    base_report=inspect_ora(root/'ora'/'CP332_CLEAN_SEMANTIC_BASE_MASTER_NOT_APPROVED.ora')
    errors.extend(f'master: {s}' for s in base_report['issues'])
    if set(base_report.get('names',[]))!=set('base_'+b for b in BASE):errors.append('Clean master has expression or unexpected layer')
    if base_report.get('base_hashes')!=baseline:errors.append('Master layer image differs from expression scenes')
    if len(set(r.get('composite_sha256') for r in reports))!=5:errors.append('Expressions do not generate five distinct composites')
    # Rig-like displacement probe: the clean face base must remain opaque
    # underneath points previously occupied by separately painted eyes/mouth.
    face_path=root/'source'/'png'/'face_underpaint.png'
    with Image.open(face_path) as face:
        pix=face.getchannel('A')
        for x,y in [(417,503),(607,503),(510,638)]:
            if pix.getpixel((x,y)) < 240:errors.append(f'Skin underpaint is missing at {(x,y)}')
    return {'checkpoint':'CP332','passed':not errors,'errors':errors,'face_ora_count':len(reports),
            'semantic_faceline_layers':len(reports)*len(PARTS),'base_layer_count':len(BASE),
            'actual_oras_checked':reports,'base_ora_checked':base_report,
            'production_art_acceptance':'NOT_APPROVED','spine':'NOT_VERIFIED','apk':'NOT_VERIFIED'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--strict',action='store_true');p.add_argument('--report',type=Path)
    args=p.parse_args();result=audit(args.root)
    if args.report:args.report.write_text(json.dumps(result,indent=2)+'\n')
    print('CP332 semantic art ORA audit:', 'PASS' if result['passed'] else 'FAIL')
    print('6 ORAs, 10 shared master slots, 65 expression slots; ART APPROVAL STILL PENDING')
    for e in result['errors']:print(' -',e)
    if args.strict:
        print('STRICT ART GATE: BLOCKED — no user-approved production face, no Spine or APK.')
    return 0 if result['passed'] and not args.strict else 1

if __name__=='__main__':raise SystemExit(main())
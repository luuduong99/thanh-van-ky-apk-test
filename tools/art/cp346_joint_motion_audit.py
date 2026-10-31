#!/usr/bin/env python3
"""Audit CANON-locked CP343 region motion. This is not a painted underlayer or rig."""
import argparse, io, json, hashlib, zipfile
from pathlib import Path
import numpy as np
from PIL import Image

CANON='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CP343='b61169d5b3fdb04dbbbd38df3ab080b2662e9332fabcc9c6ecaf660691ce9519'
ARMS={'left':('06_left_arm_and_sleeve',(-10,5)),'right':('07_right_arm_and_sleeve',(10,5))}

def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def rgba(data): return Image.open(io.BytesIO(data)).convert('RGBA')
def check(package,canon,out):
    if sha(package)!=CP343 or sha(canon)!=CANON: raise ValueError('Source SHA mismatch: input not approved')
    with zipfile.ZipFile(package) as z:
        if z.testzip(): raise ValueError('Damaged ZIP')
        original=rgba(z.read('source/FRONT_CP342_SOURCE_LOCKED.png'))
        parts=[(p,rgba(z.read(p))) for p in sorted(z.namelist()) if p.startswith('layers/') and p.endswith('.png')]
    if original.size!=(215,449) or len(parts)!=10: raise ValueError('Unexpected source dimensions or layer count')
    idle=Image.new('RGBA',original.size)
    for _,pic in parts: idle=Image.alpha_composite(idle,pic)
    a=np.asarray(original); b=np.asarray(idle)
    if not np.array_equal(a[:,:,3],b[:,:,3]) or not np.array_equal(a[a[:,:,3]>0],b[a[:,:,3]>0]):
        raise ValueError('At-rest image reconstruction is not exact')
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    report={'checkpoint':'CP346','canon_sha256':CANON,'cp343_sha256':CP343,'at_rest_pixel_exact':True,'production_release':'blocked_pending_art','results':{}}
    for case in ('left','right','both'):
        img=Image.new('RGBA',original.size)
        for path,part in parts:
            delta=next((xy for side,(key,xy) in ARMS.items() if (side==case or case=='both') and key in path),(0,0))
            shifted=Image.new('RGBA',original.size)
            shifted.paste(part,delta)
            img=Image.alpha_composite(img,shifted)
        x=np.asarray(img)[:,:,3]; src=a[:,:,3]
        missing=(src>127)&(x<25)
        protrude=(src<25)&(x>127)
        report['results'][case]={'lost':int(missing.sum()),'new':int(protrude.sum()),'gate':'FAIL_missing_underpaint'}
        Image.fromarray(np.uint8(missing)*255,'L').save(out/(case+'_missing_mask.png'))
        Image.fromarray(np.uint8(protrude)*255,'L').save(out/(case+'_new_mask.png'))
    expected={'left':(914,500),'right':(884,598),'both':(1798,1098)}
    for k,(lost,new) in expected.items():
        if (report['results'][k]['lost'],report['results'][k]['new'])!=(lost,new):
            raise ValueError('CP343 locked reference counts not reproduced: '+k)
    (out/'CP346_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cp343-zip',required=True);p.add_argument('--canon',required=True);p.add_argument('--out-dir',required=True)
    args=p.parse_args();print(json.dumps(check(args.cp343_zip,args.canon,args.out_dir),indent=2))

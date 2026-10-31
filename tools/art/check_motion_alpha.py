#!/usr/bin/env python3
"""CP345: structural alpha delta reviewer, not an underpaint quality proof."""
import argparse, json
from PIL import Image
import numpy as np

def inspect(idle_path, moved_path, roi):
    with Image.open(idle_path) as im: a=np.asarray(im.convert('RGBA'))
    with Image.open(moved_path) as im: b=np.asarray(im.convert('RGBA'))
    if a.shape!=b.shape: raise ValueError('different frame dimensions')
    x,y,w,h=roi
    if min(x,y)<0 or min(w,h)<=0 or x+w>a.shape[1] or y+h>a.shape[0]: raise ValueError('invalid ROI')
    old=a[y:y+h,x:x+w,3]>=8; new=b[y:y+h,x:x+w,3]>=8
    lost=int((old & ~new).sum()); gained=int((~old & new).sum())
    return {'roi':roi,'lost_coverage_pixels':lost,'new_coverage_pixels':gained,'decision':'REVIEW_REQUIRED' if lost or gained else 'NO_COVERAGE_CHANGE','warning':'Coverage changes may reflect legitimate silhouette movement; manual art review required.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('idle');p.add_argument('moved');p.add_argument('--region',required=True);p.add_argument('--out');args=p.parse_args()
    try:
        roi=list(map(int,args.region.split(',')))
        if len(roi)!=4:raise ValueError()
    except ValueError:p.error('region must be x,y,w,h')
    s=json.dumps(inspect(args.idle,args.moved,roi),indent=2)
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(s+'\n',encoding='utf-8')
    print(s)
if __name__=='__main__':main()

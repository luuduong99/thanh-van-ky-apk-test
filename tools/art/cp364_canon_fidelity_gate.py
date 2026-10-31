#!/usr/bin/env python3
"""CP364 — source-locked Lâm Thiển Front hair/shoe QA, never art approval.

The check assumes a same-camera, same-layout Front image. A different crop/pose
must be aligned by an artist first. Palette check is an early warning only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
FRONT_BBOX = (13, 172, 230, 630)  # pixel-exact reference in approved sheet
BASE_SIZE = (217, 458)
# Rectangles refer to original Front crop (NOT to CP348's 215×449 cutout).
ROI = {
    'silver_lavender_hair': (83, 12, 135, 57),
    'image_left_blue_toe': (79, 432, 102, 458),
    'image_right_blue_toe': (109, 414, 122, 446),
}


def source_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def front_from_canon(canon_path):
    if source_sha256(canon_path) != CANON_SHA:
        raise ValueError('CANON V2.1 SHA256 mismatch. Refuse candidate checks.')
    with Image.open(canon_path) as img:
        if img.size != (941, 1672):
            raise ValueError('CANON V2.1 dimensions changed')
        return img.convert('RGBA').crop(FRONT_BBOX)


def analyze_candidate(candidate: Image.Image):
    rgba = np.asarray(candidate.convert('RGBA'))
    height, width = rgba.shape[:2]
    if width < 180 or height < 380 or abs(width / height - BASE_SIZE[0] / BASE_SIZE[1]) > 0.035:
        return {
            'technical_status': 'REVIEW_ALIGNMENT',
            'issues': ['Expected aligned Front crop, similar to 217x458 source aspect; this image is not aligned.'],
            'runtime_approved': False, 'visual_qa': 'NOT_PASSED',
            'production_release': 'blocked_pending_art',
        }

    report = {'canvas':[width,height], 'metrics':{}, 'issues':[],
              'runtime_approved':False, 'visual_qa':'NOT_PASSED',
              'production_release':'blocked_pending_art'}
    scale_x = width / BASE_SIZE[0]
    scale_y = height / BASE_SIZE[1]
    for role,(left,top,right,bottom) in ROI.items():
        x1,y1 = round(left*scale_x),round(top*scale_y)
        x2,y2 = round(right*scale_x),round(bottom*scale_y)
        part=rgba[y1:y2,x1:x2]
        opaque=part[:,:,3]>=128
        rgb=part[:,:,:3].astype(np.float32)
        if role=='silver_lavender_hair':
            # A dark-brown replacement must fail even when background is bright.
            bright=(rgb[:,:,0]*0.2126+rgb[:,:,1]*0.7152+rgb[:,:,2]*0.0722)>=125
            accepted=int(np.count_nonzero(opaque & bright))
            total=int(np.count_nonzero(opaque))
            fraction=round(accepted/max(total,1),4)
            report['metrics'][role]={'bright_hair_region_fraction':fraction,
                                      'opaque_pixels':total,'roi_px':[x1,y1,x2,y2]}
            if fraction < 0.42:
                report['issues'].append('Head/hair region is too dark or absent for approved silver-lavender CANON; inspect original hair and identity.')
        else:
            blue=(rgb[:,:,2]>rgb[:,:,0]*1.14)&(rgb[:,:,2]>rgb[:,:,1]*1.09)&(rgb[:,:,2]>90)
            count=int(np.count_nonzero(opaque & blue))
            reference_threshold=max(12, int((x2-x1)*(y2-y1)*0.06))
            report['metrics'][role]={'visible_blue_pixels':count,
                                      'minimum_expected':reference_threshold,
                                      'roi_px':[x1,y1,x2,y2]}
            if count < reference_threshold:
                report['issues'].append(role+' : blue toe appears missing/too weak; check alpha and shoe art against CANON.')
    report['technical_status']='NEEDS_ART_CORRECTION' if report['issues'] else 'REFERENCE_COLOR_GUARDS_CLEAR'
    report['limitations']=[
       'Automatic color checks are not aesthetic approval, nor a guarantee of exact CANON identity.',
       'Requires same-camera, composition-aligned Front at rest; not intended for back/side/3-4 view.',
       'Cannot verify occluded shoulder anatomy, anti-aliasing seams, fabric folds, Spine rig or Android FPS.',
    ]
    return report


def inspect(canon_path,candidate_path):
    front_from_canon(canon_path)
    with Image.open(candidate_path) as im:
        result=analyze_candidate(im)
    result['canon_verified_sha256']=CANON_SHA
    result['candidate_sha256']=source_sha256(candidate_path)
    result['checkpoint']='CP364'
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--canon',required=True)
    p.add_argument('--candidate',required=True)
    p.add_argument('--out')
    args=p.parse_args()
    result=inspect(args.canon,args.candidate)
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.out:
        Path(args.out).write_text(payload,encoding='utf8')
    print(payload,end='')
    return 0 if result['technical_status']=='REFERENCE_COLOR_GUARDS_CLEAR' else 2

if __name__=='__main__':
    raise SystemExit(main())
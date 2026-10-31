#!/usr/bin/env python3
"""CP328 canonical face iris color preflight.

Detect only eye-color identity drift. NOT a face recognizer, quality approval,
layer validity test, or substitute for visual review. The two native source
ROIs were independently inspected on the immutable CANON V2 PNG.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

CANON_SHA = '41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
EMOTION_SHA = 'ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
FACE_BBOX = [1160, 0, 1390, 114]
# ROI coordinates are relative to the 230x114 native face crop.
# WARNING: iris pixels occupy only a subset of the ROIs (also includes skin/lashes).
IRIS_ROIS = {
    'eye_image_left': [69,57,105,88],
    'eye_image_right': [130,30,176,61],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_crop(path: Path) -> Image.Image:
    if sha256(path) != CANON_SHA:
        raise ValueError('CANON V2 checksum mismatch; cannot use image as approved source')
    image = Image.open(path).convert('RGB')
    if image.size != (1672,941):
        raise ValueError('Unexpected CANON V2 image dimensions')
    return image.crop(tuple(FACE_BBOX))


def evaluate_face_crop(image: Image.Image, rois=IRIS_ROIS) -> dict:
    if image.mode != 'RGB':
        image = image.convert('RGB')
    a = np.asarray(image)
    if a.shape[:2] != (114,230):
        raise ValueError('Expected native 230x114 face crop; do not pass 4x upscaled guide')
    hsv = cv2.cvtColor(a,cv2.COLOR_RGB2HSV)
    items = []
    for key,(x0,y0,x1,y1) in rois.items():
        if not (0<=x0<x1<=230 and 0<=y0<y1<=114):
            raise ValueError(f'Invalid eye ROI: {key}')
        p = hsv[y0:y1,x0:x1]
        rgb = a[y0:y1,x0:x1]
        # Golden/amber pigment on original V2 iris: hue 5..27 (OpenCV 0..179).
        # Blue/cyan drift: hue 80..135. Skin also contains amber hue, hence the
        # two small, anchored ROIs plus mandatory artist visual review.
        amber = (p[:,:,0]>=5)&(p[:,:,0]<=27)&(p[:,:,1]>=65)&(p[:,:,2]>=90)
        blue = (p[:,:,0]>=80)&(p[:,:,0]<=135)&(p[:,:,1]>=55)&(p[:,:,2]>=70)
        amber_n=int(amber.sum())
        blue_n=int(blue.sum())
        med_rgb=[int(round(float(x))) for x in np.median(rgb[amber],axis=0)] if amber_n else None
        med_hsv=[int(round(float(x))) for x in np.median(p[amber],axis=0)] if amber_n else None
        passed=amber_n >= 25 and amber_n >= (blue_n * 3 + 1)
        items.append({'eye':key,'roi_xyxy':[x0,y0,x1,y1], 'sample_area_px':int(p.shape[0]*p.shape[1]),
                      'amber_pixels':amber_n,'blue_pixels':blue_n,
                      'amber_median_rgb':med_rgb,'amber_median_hsv_cv':med_hsv,
                      'heuristic_pass':passed})
    return {'status':'heuristic_pass' if all(x['heuristic_pass'] for x in items) else 'heuristic_fail',
            'native_crop_px':[230,114], 'face_source_bbox_xyxy':FACE_BBOX, 'eyes':items,
            'warning':'This is an amber-vs-blue drift guard only, not a full art approval or identity match.'}


def evaluate_candidate_iris_patches(image: Image.Image, patch_rects: dict) -> dict:
    """Optional future high-res art iris audit using ARTIST-ANNOTATED iris-only rectangles.

    Coordinates are in candidate-image pixels, not relative to the 230x114 V2
    reference. Does not apply to closed eyes. Requires explicit manual review.
    """
    arr=np.asarray(image.convert('RGB'))
    h,w=arr.shape[:2]
    if set(patch_rects)!={'left_iris','right_iris'}:
        raise ValueError('Candidate needs exact artist-annotated left_iris/right_iris rectangles')
    hsv=cv2.cvtColor(arr,cv2.COLOR_RGB2HSV)
    audits=[]
    for k,(x0,y0,x1,y1) in patch_rects.items():
        if not all(isinstance(v,int) and not isinstance(v,bool) for v in (x0,y0,x1,y1)) or not (0<=x0<x1<=w and 0<=y0<y1<=h):
            raise ValueError(f'Invalid annotated candidate ROI: {k}')
        p=hsv[y0:y1,x0:x1]
        amber=(p[:,:,0]>=5)&(p[:,:,0]<=27)&(p[:,:,1]>=70)&(p[:,:,2]>=70)
        blue=(p[:,:,0]>=80)&(p[:,:,0]<=135)&(p[:,:,1]>=55)&(p[:,:,2]>=70)
        a=int(amber.sum());b=int(blue.sum());area=p.shape[0]*p.shape[1]
        audits.append({'eye':k,'amber_pixels':a,'blue_pixels':b,'total_pixels':area,
                      'heuristic_pass':a>=max(10,int(area*.2)) and a>b*3})
    return {'status':'heuristic_pass' if all(x['heuristic_pass'] for x in audits) else 'heuristic_fail',
            'eyes':audits,
            'warning':'Artist-selected iris-only ROIs are required. Passing DOES NOT mean production-ready or approved.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('canon_png',type=Path)
    p.add_argument('--out',type=Path)
    p.add_argument('--candidate',type=Path,help='Optional future noncanon artwork to test')
    p.add_argument('--iris-rois',type=Path,help='JSON with artist-annotated iris rectangles in candidate pixels')
    args=p.parse_args()
    try:
        report=evaluate_face_crop(canonical_crop(args.canon_png))
    except (OSError,ValueError) as exc:
        print(json.dumps({'status':'error','error':str(exc)},ensure_ascii=False,indent=2))
        return 2
    if args.candidate or args.iris_rois:
        if not (args.candidate and args.iris_rois):
            print('Both --candidate and --iris-rois are required together')
            return 2
        try:
            rois=json.loads(args.iris_rois.read_text(encoding='utf-8'))
            candidate=Image.open(args.candidate)
            report['candidate']=evaluate_candidate_iris_patches(candidate,rois)
        except (OSError,ValueError,KeyError,TypeError) as exc:
            print(json.dumps({'status':'error','error':str(exc)},ensure_ascii=False))
            return 2
    if args.out:args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['status']=='heuristic_pass' and ('candidate' not in report or report['candidate']['status']=='heuristic_pass') else 1

if __name__=='__main__':raise SystemExit(main())
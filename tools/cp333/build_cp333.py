#!/usr/bin/env python3
"""CP333: deterministic incremental line-art polish on CP332 semantic assets.

A reproducible VECTOR STUDY, not canonical, art-approved or Spine-ready.
No pixels sampled/copied from source reference sheets into the semantic layers.
"""
import os, sys, importlib.util, math
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / 'base_cp332_build.py'
if not SOURCE.exists():
    SOURCE = Path(__file__).resolve().parents[2] / 'TVK_LamThien_CP332_Semantic_Face_Study' / 'source' / 'build_cp332.py'
if not SOURCE.exists():
    SOURCE = Path(__file__).resolve().parents[1] / 'cp332' / 'build_cp332.py'
if not SOURCE.exists():
    SOURCE = Path(__file__).resolve().parents[1] / 'cp332' / 'build_cp332.py'
if not SOURCE.exists():
    raise FileNotFoundError('Requires original CP332 build_cp332.py source; supply alongside CP333 or in tools/cp332.')

OUT = Path(os.environ.get('CP333_OUT', str(Path(__file__).resolve().parents[1])))
os.environ['CP332_OUT'] = str(OUT)
spec = importlib.util.spec_from_file_location('cp332_import_for_cp333',SOURCE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.ROOT = OUT
base.ART = OUT/'source'
base.GOLD = '#d9ad66';base.AMBER='#d58b35'
BASE_ORIGINAL=base.base_art
EXPR_ORIGINAL=base.expression_art


def gold_filaments():
    s=[]
    # Beads, fine leaves, and small pearl arrangements on existing hair pin.
    for x,y,r in [(267,170,4),(280,164,4),(302,166,4),(331,167,5),
                  (271,224,4),(244,263,4),(315,244,3)]:
        s.append(base.circle(x,y,r,'#f2dba7'))
    for j in range(7):
        angle=(j-3)*0.28
        x=273+27*math.sin(angle)
        y=265+48*math.cos(angle)
        s.append(base.path(f'M {x:.1f} {y:.1f} q -6 -10 -2 -19','none','#caa469',2))
    s += [base.path('M 318 187 Q 337 177 362 180 Q 387 182 404 190','none','#f8e4b9',3),
          base.path('M 296 324 Q 305 360 289 395','none','#ffdfa5',3)]
    return ''.join(s)


def hair_shines():
    pieces=[]
    for a in [
        ('M 348 370 C 338 281 400 203 443 188','#fefbff',5),
        ('M 383 352 C 391 279 417 224 462 199','#eeeafd',5),
        ('M 457 382 C 476 310 481 249 484 203','#fefaff',5),
        ('M 577 348 C 590 279 583 235 565 202','#f7f7ff',7),
        ('M 674 366 C 701 271 637 194 607 178','#faf6ff',5),
        ('M 355 456 Q 367 546 346 655','#fdfaff',4),
        ('M 660 439 Q 644 527 671 658','#fefbff',4),
    ]: pieces.append(base.path(a[0],'none',a[1],a[2]))
    pieces.append(base.path('M 398 255 C 435 205 480 179 524 178','none','#a8b3d7',3))
    return ''.join(pieces)


def base_art_refined():
    o=BASE_ORIGINAL()
    # All these are still base semantic layers; no eyelash/eyebrow/mouth shapes baked in.
    o['hair_back']+=base.path('M 261 383 Q 231 604 221 824 M 754 338 Q 788 592 815 856','none','#d8dcfa',5)
    o['face_underpaint']+=(
        base.path('M 388 355 Q 368 560 432 687','none','#fff1e8',6)+
        base.path('M 636 363 Q 657 549 602 674','none','#f1b8bf',6)+
        base.path('M 449 690 Q 512 729 570 688','none','#fce1da',5))
    o['hair_front']+=hair_shines()
    o['hair_side_locks']+=(base.path('M 312 492 Q 309 673 277 824','none','#fdfaff',6)+
       base.path('M 694 500 Q 710 677 729 821','none','#f8f6ff',5))
    o['flower_gold']+=gold_filaments()
    o['choker_jewel']+=(base.path('M 466 812 Q 489 823 512 826','none','#e9ca9b',3)+
        base.circle(512,832,3,'#ffffff'))
    return o


def eye_details(cx,cy,p,side):
    h=p['eye'][2];c=p['eye'][1]
    icy=cy+9+c+p['pupil'][1]
    icx=cx+p['pupil'][0]
    s=[]
    # Subtle iris sunburst, independent from skin and eye whites.
    for k in range(11):
        ang=math.pi*2*k/11
        x1=icx+11*math.sin(ang)
        y1=icy+11*h*math.cos(ang)
        x2=icx+20*math.sin(ang)
        y2=icy+20*h*math.cos(ang)
        s.append(base.path(f'M {x1:.2f} {y1:.2f} L {x2:.2f} {y2:.2f}', 'none','#e7b066',1.6))
    s.append(base.ellipse(icx,icy+10,13,max(4,5*h),'#f5ad52','opacity="0.36"'))
    s.append(base.circle(icx-12,icy-12,4,'#fffdf8'))
    return ''.join(s)


def lash_detail(cx,cy,p,side):
    c=p['eye'][1];s=[]
    for i in range(5):
        # short individual upper lashes on outside edge
        t=i/4
        x=cx+40+i*6
        y=cy-15+c+i*2
        s.append(base.path(f'M {x} {y} q {3+t*3:.2f} -{9+t*4:.2f} {7+t*4:.2f} -{11+t*6:.2f}', 'none','#653e50',3.5))
    # lower lashes use pale cocoa and do not bake skin texture.
    s.append(base.path(f'M {cx-49} {cy+19+c} Q {cx} {cy+38+c} {cx+47} {cy+17+c}', 'none','#b9828c',2.3))
    return ''.join(s)


def refined_mouth(kind):
    lower={
    'shy':'M 501 651 Q 511 654 524 650',
    'angry':'M 491 655 Q 511 649 532 649',
    'pain':'M 492 659 Q 515 673 533 654',
    'embarrassed':'M 499 653 Q 511 658 525 654',
    'alluring':'M 498 663 Q 517 665 534 649',
    }
    return base.path(lower[kind],'none','#e5a0ac',2.5)+base.circle(489,638,2,'#f6bdc2')


def expression_refined(e):
    pieces=EXPR_ORIGINAL(e)
    p=base.PARAMS[e]
    for side,cx in [('left',base.L_EYE[0]),('right',base.R_EYE[0])]:
        cy=base.L_EYE[1]
        pieces['iris_'+side]+=eye_details(cx,cy,p,side)
        pieces['eyelashes_'+side]+=lash_detail(cx,cy,p,side)
        cy0=cy-72+p['brow'][1]
        for step in range(4):
            x0=cx-40+step*23
            y0=cy0-1+step*.7
            pieces['brow_'+side]+=base.path(f'M {x0} {y0} q 8 -6 17 -5','none','#b6a2b4',1.9)
        if e=='embarrassed':
            pieces['blush_'+side]+=base.path(f'M {cx-37} {cy+76} l 15 12 M {cx-15} {cy+78} l 13 12 M {cx+7} {cy+79} l 13 12','none','#ed9aa4',2.4, 'opacity="0.46"')
        elif e=='shy':
            pieces['blush_'+side]+=base.path(f'M {cx-17} {cy+80} l 10 7 M {cx+3} {cy+80} l 10 7','none','#efabb0',1.8,'opacity="0.4"')
    pieces['mouth']+=refined_mouth(e)
    return pieces

base.base_art=base_art_refined
base.expression_art=expression_refined

def main():
    import json
    base.main()
    for f in sorted((OUT/'ora').glob('CP332_*.ora')):
        f.rename(f.with_name(f.name.replace('CP332_', 'CP333_', 1)))
    for f in sorted((OUT/'preview').glob('CP332_*.png')):
        f.rename(f.with_name(f.name.replace('CP332_', 'CP333_', 1)))
    metadata = json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    metadata['checkpoint'] = 'CP333'
    metadata['source_checkpoint'] = 'CP332'
    metadata['status'] = 'refined_vector_facial_detail_prototype_NOT_APPROVED'
    metadata['art_improvements'] = ['hair_fine_shines','gold_ornament_filaments','iris_amber_radial_marks', 'individual_lash_lines','mouth_secondary_contour','brow_hair_strokes']
    metadata['no_same_face_master_pixel_change_between_emotions'] = True
    metadata['artist_visual_match_to_canon_v2'] = 'NOT_APPROVED'
    metadata['face_semantic_layers_artist_approved'] = False
    metadata['provenance'] = 'Generated CP333 via deterministic vector changes to CP332 geometry, NOT from the newly generated infographic'
    for entry in metadata['emotions']:
        entry['ora'] = entry['ora'].replace('CP332_', 'CP333_')
    (OUT/'manifest.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('CP333 refined vector art saved; production art approval remains false.')

if __name__=='__main__':
    main()
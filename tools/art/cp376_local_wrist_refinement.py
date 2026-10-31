#!/usr/bin/env python3
"""CP376: source-locked Lâm Thiển wrist seam and rear ribbon vector art draft.

This is NOT full-body painted art, NOT a functional character rig, and NOT a verified
zero-gap result. Residual fingers from movement must not be blindly filled as underpaint.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, io, json, zipfile, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import cairosvg

BASE=Path(__file__).resolve().parent
MOD=BASE/'cp375_hidden_wrist_art.py'
if not MOD.exists():
    MOD=BASE.parents[1]/'tools'/'art'/'cp375_hidden_wrist_art.py'  # tools/art/cp376... -> tools/art/cp375...
    if not MOD.exists(): MOD=Path(__file__).with_name('cp375_hidden_wrist_art.py')
spec=importlib.util.spec_from_file_location('tvk_cp375_art',MOD)
cp375=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp375)
CANON_SHA=cp375.CANON_SHA
SIZE=cp375.SIZE
SIZE6=cp375.SIZE6
FRONT=cp375.FRONT

NEW_ART={
 '05_wrist_skin_underedge_draft': '''
 <defs><linearGradient id="s376" x1=".15" y1="0" x2=".7" y2="1"><stop stop-color="#fff7ee"/><stop offset=".5" stop-color="#f5d1c7"/><stop offset="1" stop-color="#dca6a4"/></linearGradient></defs>
 <path d="M15.7 181.0 Q22 178.2 29.5 179.4 Q35.5 180.1 36.0 183.7 Q26.4 183.2 17.1 185.5 Q14.6 185 15.7 181.0Z" fill="url(#s376)" stroke="#dbaaaa" stroke-width=".45"/>
 <path d="M17.5 181.5 Q26 179.1 34.7 182.2" fill="none" stroke="#fffcf5" stroke-width="1.05" opacity=".82"/>''',
 '06_inner_cuff_filagree_draft': '''
 <defs><linearGradient id="g376" x1="0" y1="0" x2="1" y2=".2"><stop stop-color="#f5e5ad"/><stop offset=".36" stop-color="#ac7940"/><stop offset=".7" stop-color="#f9e4a5"/><stop offset="1" stop-color="#926334"/></linearGradient></defs>
 <path d="M18.1 181.5 Q24.5 179.4 32.5 181.3 L34.0 183.2 Q28 182 20.4 184.8 L17.7 184.1Z" fill="url(#g376)" stroke="#8b6b44" stroke-width=".36"/>
 <path d="M20.7 183.7 Q27 180.7 31.0 182.4 M23.2 182.6 L24.6 183.4 M27.0 181.8 L28.1 182.7" fill="none" stroke="#fff1be" stroke-width=".46"/>
 <circle cx="29.8" cy="182.05" r=".65" fill="#7fc3e8" stroke="#fce7b3" stroke-width=".26"/>''',
 '07_rear_silk_under_fingers_draft': '''
 <defs><linearGradient id="v376" x1=".1" y1="0" x2=".9" y2="1"><stop stop-color="#f5faff" stop-opacity=".85"/><stop offset=".38" stop-color="#c6d8f5" stop-opacity=".88"/><stop offset=".74" stop-color="#82a9df" stop-opacity=".85"/><stop offset="1" stop-color="#5d8dcd" stop-opacity=".51"/></linearGradient></defs>
 <path d="M34 193 C34.9 199.1 32.3 204.5 27.7 210.3 Q24 214.6 20 218 C22.8 210.3 26.3 204.3 29.7 198.4 Q32.1 195.0 34 193Z" fill="url(#v376)" stroke="#829dd7" stroke-width=".44"/>
 <path d="M32.4 197 Q30 206 24 214" fill="none" stroke="#f7faff" stroke-width="1.15" opacity=".77"/>
 <path d="M33 200 Q29 207 22.6 216" fill="none" stroke="#5b91d8" stroke-width=".58" opacity=".56"/>''',
}

# Regions are a diagnostic of THIS one movement sample; these are NOT semantic alpha gates.
REGION_ROIS={
    'wrist_cuff_seam':(17,178,35,185),
    'rear_ribbon_boundary':(18,196,36,215),
    'finger_silhouette_motion':(7,198,14,215),
}

def svg(name):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE6[0]}" height="{SIZE6[1]}" viewBox="0 0 {SIZE[0]} {SIZE[1]}">{NEW_ART[name]}</svg>'

def validate_source(canon, matte, hand):
    # No file/directory writes until all independent source contracts pass.
    img=cp375.validate_canon(canon)
    orig=np.asarray(img.crop(FRONT))
    mat=Image.open(matte).convert('RGBA')
    arm=Image.open(hand).convert('RGBA')
    if mat.size!=SIZE or arm.size!=SIZE: raise ValueError('Wrong Front crop size')
    if not np.array_equal(np.asarray(mat)[:,:,:3],orig[:,:,:3]):
        raise ValueError('Matte RGB is not exact approved CANON crop')
    return img,mat,arm

def calc_exposed(hand, dx=-6,dy=3):
    orig=np.asarray(hand.getchannel('A'))>128
    shifted=Image.new('RGBA',SIZE)
    shifted.paste(hand,(dx,dy),hand.getchannel('A'))
    moved=np.asarray(shifted.getchannel('A'))>128
    return orig & ~moved, shifted, orig

def diagnostic_clusters(missing):
    n, lab, stats, cent = cv2.connectedComponentsWithStats(missing.astype(np.uint8),8)
    regions=[]
    for i in range(1,n):
        x,y,w,h,area=[int(z) for z in stats[i]]
        mx,my=map(float,cent[i])
        # Soft visually-identified zones. Label as diagnostic hypothesis, not artist-approved anatomy.
        zone=('wrist_cuff_seam' if my<191 else 'finger_silhouette_motion' if mx<15 else 'rear_ribbon_boundary')
        regions.append({'bounds':[x,y,w,h],'pixels':area,'center':[round(mx,2),round(my,2)],'candidate_zone':zone})
    return regions

def compose_masked_underpaint(layers,hand_rest):
    merged=Image.new('RGBA',SIZE6)
    for layer in layers: merged.alpha_composite(layer)
    small=merged.resize(SIZE,Image.Resampling.LANCZOS)
    orig=np.asarray(hand_rest.getchannel('A'))>128
    mask=np.asarray(small.getchannel('A')).copy();mask[~orig]=0
    small.putalpha(Image.fromarray(mask,'L'))
    return small, merged

def make(canon, matte, hand, outdir):
    source,mat,arm=validate_source(canon,matte,hand)
    root=Path(outdir);root.mkdir(parents=True,exist_ok=True)
    for folder in ['svg','layers','qa','ora']: (root/folder).mkdir(exist_ok=True)
    items=[]
    for name in list(cp375.ART)+list(NEW_ART):
        sv=cp375.svg(name) if name in cp375.ART else svg(name)
        ET.fromstring(sv)
        (root/'svg'/f'{name}.svg').write_text(sv,encoding='utf-8')
        im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode('utf8'),output_width=SIZE6[0],output_height=SIZE6[1]))).convert('RGBA')
        if im.getchannel('A').getbbox() is None: raise ValueError('Empty art layer '+name)
        im.save(root/'layers'/f'{name}.png')
        items.append((name,im))
    cp375_under, _=compose_masked_underpaint([v for k,v in items[:4]],arm)
    current_under, full=compose_masked_underpaint([v for k,v in items],arm)
    full.save(root/'CP376_SEVEN_VECTOR_LAYERS_PARTIAL_NOT_APPROVED.png')
    src_exposed,source_shifted,orig=calc_exposed(arm)
    old_alpha=np.asarray(cp375_under.getchannel('A'))>128
    new_alpha=np.asarray(current_under.getchannel('A'))>128
    missing_old=src_exposed&~old_alpha
    missing_new=src_exposed&~new_alpha
    old_cl=diagnostic_clusters(missing_old); new_cl=diagnostic_clusters(missing_new)
    multi_pose_diagnostics={}
    for dx,dy in [(-6,3),(-4,2),(3,-2),(-8,5)]:
        ex,_,_=calc_exposed(arm,dx,dy)
        multi_pose_diagnostics[f'{dx},{dy}']={
            'source_exposed_px':int(ex.sum()),
            'cp375_residual_px':int(np.count_nonzero(ex&~old_alpha)),
            'cp376_residual_px':int(np.count_nonzero(ex&~new_alpha))
        }
    region_counts={}
    for name,(x1,y1,x2,y2) in REGION_ROIS.items():
        zone_old=int(missing_old[y1:y2,x1:x2].sum())
        zone_new=int(missing_new[y1:y2,x1:x2].sum())
        region_counts[name]={'before':zone_old,'after':zone_new}
    # Conservatively classify: disappearing finger tips are not automatically a missing underpaint seam.
    result={'checkpoint':'CP376','source_sha256':CANON_SHA,
       'art_layers_from_cp375':4,'new_drawn_svg_layers':len(NEW_ART),'total_visible_draft_layers':len(items),
       'old_exposed_px':int(src_exposed.sum()), 'cp375_missing_px':int(missing_old.sum()),
       'cp376_missing_px':int(missing_new.sum()),
       'gap_clusters_before':old_cl,'gap_clusters_after':new_cl,'diagnostic_rois':region_counts,
       'multi_offset_diagnostics_not_animation_test':multi_pose_diagnostics,
       'main_pose_dxdy':[-6,3],
       'visual_qa':'NOT_PASSED','sprite_paths':{},'production_release':'blocked_pending_art',
       'native_painted_full_body':False,'full_character_art_complete':False,'full_motion_gap_free':False,
       'spine_ready':False,'apk_ready':False,
       'assumptions':['Gap pixels at moving fingertips are expected silhouette shifts; do NOT flood-fill them as underpaint.',
           'Blue ribbon/cuff seams are candidate art defects requiring visual inspection.',
           'Only one movement offset was evaluated on real source, no mesh/bones/Spine or device tests.',
           'CP376 vector is draft art, not user-approved and not faithful native HD character painting.']}
    # Reassemble technical previews as a source-comparison, never substitute another character.
    raw=np.array(mat)
    eraser=np.asarray(arm.getchannel('A'))>0
    raw[:,:,3][eraser]=0
    background=Image.fromarray(raw,'RGBA')
    before=Image.alpha_composite(Image.alpha_composite(background,cp375_under),source_shifted)
    after=Image.alpha_composite(Image.alpha_composite(background,current_under),source_shifted)
    before.save(root/'qa'/'CP376_BEFORE_MOVEMENT_TECHNICAL.png')
    after.save(root/'qa'/'CP376_AFTER_MOVEMENT_TECHNICAL.png')
    # Grid for precise analysis of 90-pixel clusters, comes from exact CANON with QA marker.
    tagged=source.crop(FRONT).convert('RGBA')
    arr=np.array(tagged)
    arr[missing_old,0:3]=[222,45,50]
    image=Image.fromarray(arr,'RGBA')
    image.crop((0,150,85,229)).resize((425,395),Image.Resampling.NEAREST).save(root/'qa'/'CP376_OLD_90PX_SOURCE_HIGHLIGHT.png')
    arr2=np.asarray(tagged).copy()
    arr2[missing_new,0:3]=[222,45,50]
    Image.fromarray(arr2,'RGBA').crop((0,150,85,229)).resize((425,395),Image.Resampling.NEAREST).save(root/'qa'/'CP376_REMAINING_GAP_SOURCE_HIGHLIGHT.png')
    ora=root/'ora'/'CP376_WRIST_RIBBON_SEVEN_DRAWN_LAYERS_NOT_RIG.ora'
    stackroot=ET.Element('image',{'w':str(SIZE6[0]),'h':str(SIZE6[1]),'name':'CP376 drafts not full-body art','version':'0.0.3'})
    stack=ET.SubElement(stackroot,'stack')
    with zipfile.ZipFile(ora,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for idx,(name,im) in enumerate(reversed(items)):
            bio=io.BytesIO();im.save(bio,format='PNG');internal=f'data/layer_{idx:02d}.png'
            z.writestr(internal,bio.getvalue())
            ET.SubElement(stack,'layer',{'name':'DRAFT__'+name,'src':internal,'visibility':'visible','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        guide=source.crop(FRONT).resize(SIZE6,Image.Resampling.NEAREST)
        bio=io.BytesIO();guide.save(bio,format='PNG')
        z.writestr('data/CANON_REFERENCE_HIDDEN.png',bio.getvalue())
        ET.SubElement(stack,'layer',{'name':'CANON_V2_1_SOURCE_REFERENCE_HIDDEN','src':'data/CANON_REFERENCE_HIDDEN.png','visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('stack.xml',ET.tostring(stackroot,encoding='utf-8',xml_declaration=True))
        bio=io.BytesIO();full.save(bio,format='PNG');z.writestr('mergedimage.png',bio.getvalue())
    assert zipfile.ZipFile(ora).testzip() is None
    result['ora_name']=ora.name
    # Comparison sheet contains only the approved character and source-derived experiments.
    board=Image.new('RGB',(1560,780),'#162a42');draw=ImageDraw.Draw(board)
    fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font=ImageFont.truetype(fontfile,17);bold=ImageFont.truetype(fontfile,25)
    draw.text((24,19),'CP376  |  LAM THIEN — SOURCE-LOCKED WRIST & RIBBON QA',font=bold,fill='#f0f5fd')
    draw.text((24,56),'Exact approved CANON V2.1 / CP375 gap map / CP376 drawn draft / QA markers — NOT APPROVED',font=font,fill='#c7d8eb')
    canon_small=source.copy();canon_small.thumbnail((343,605));board.paste(canon_small.convert('RGB'),(23,112))
    original=source.crop(FRONT).crop((0,150,85,229)).resize((350,330),Image.Resampling.LANCZOS)
    board.paste(original.convert('RGB'),(395,195))
    board.paste(Image.open(root/'qa'/'CP376_OLD_90PX_SOURCE_HIGHLIGHT.png').convert('RGB').resize((350,330)),(790,195))
    board.paste(Image.open(root/'qa'/'CP376_REMAINING_GAP_SOURCE_HIGHLIGHT.png').convert('RGB').resize((350,330)),(1185,195))
    captions=[(24,'01 APPROVED CANON ORIGINAL'),(395,'02 SOURCE WRIST CROP'),(790,'03 CP375 RESIDUAL PIXELS'),(1185,'04 CP376 RESIDUAL PIXELS')]
    for x,label in captions:draw.text((x,560),label,font=ImageFont.truetype(fontfile,14),fill='white')
    draw.text((395,622),f'CP375 residual: {result["cp375_missing_px"]} px    |    CP376 residual: {result["cp376_missing_px"]} px',font=font,fill='#ffdca8')
    draw.text((395,662),'Finger contour shifts are not automatically anatomical holes. Visual approval remains BLOCKED.',font=ImageFont.truetype(fontfile,15),fill='#f0c6bc')
    preview=root/'qa'/'CP376_CANON_GAP_CATEGORIES_UNAPPROVED.png';board.save(preview)
    result['preview_name']=preview.name
    (root/'CP376_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--canon',required=True);p.add_argument('--matte',required=True);p.add_argument('--hand',required=True);p.add_argument('--out',required=True)
    v=p.parse_args();print(json.dumps(make(v.canon,v.matte,v.hand,v.out),ensure_ascii=False,indent=2))
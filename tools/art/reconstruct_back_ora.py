#!/usr/bin/env python3
"""Create an explicitly NON-ORIGINAL, editable ORA study from a flattened Back PNG.

It preserves the supplied standing composite pixel-for-pixel. Masks are hand-drawn
working ROIs, NOT recovered original layer boundaries. The visible parts under
occlusion are approximated with OpenCV inpaint and must be redrawn by an artist.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from xml.etree import ElementTree as ET
from hashlib import sha256
import cv2
import numpy as np
import io, zipfile, json, argparse

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path('/mnt/data/lin_qian_back.png')
# Each grouping is a working partition of visible artwork. Layer order high -> low.
REGIONS=[
 ('hair_jewelry_top', [
     [(53,34),(75,26),(98,41),(103,56),(91,64),(72,60),(50,58)],
     [(48,60),(55,54),(68,61),(66,93),(58,105),(47,88)],
 ]),
 ('hair_front_highlights', [
     [(79,56),(115,53),(135,69),(148,98),(153,126),(159,162),(158,214),(149,241),(147,280),(130,320),(114,335),(89,333),(68,298),(57,245),(60,195),(67,166),(68,118)],
 ]),
 ('hair_outer_strands', [
     [(67,106),(85,143),(87,192),(73,251),(67,305),(60,346),(51,391),(34,445),(22,474),(16,468),(19,422),(31,360),(35,317),(46,263),(49,200)],
     [(111,100),(144,112),(160,145),(166,208),(162,260),(150,299),(135,333),(132,351),(121,349),(132,305),(142,267),(149,211),(148,161)],
 ]),
 ('shoulder_skin_right', [
     [(157,127),(180,140),(191,158),(197,190),(182,205),(171,187),(158,181),(148,153)],
 ]),
 ('shoulder_skin_left', [
     [(43,140),(59,129),(73,148),(71,178),(56,194),(42,180),(40,158)],
 ]),
 ('sleeve_right', [
     [(183,190),(205,184),(206,422),(195,462),(177,419),(174,331),(179,273)],
 ]),
 ('sleeve_left', [
     [(44,182),(60,187),(64,239),(61,312),(47,361),(36,410),(25,481),(13,499),(18,424),(29,332),(32,236)],
 ]),
 ('sash_bow', [
     [(75,298),(103,291),(125,300),(146,297),(174,322),(167,353),(144,355),(139,382),(103,365),(82,344),(67,326)],
 ]),
 ('sash_hanging_panels', [
     [(78,335),(109,358),(130,379),(118,444),(99,522),(80,519),(62,452),(59,387)],
     [(132,365),(164,355),(176,413),(174,494),(157,512),(137,474),(118,442)],
 ]),
]
# 9 foreground masks + backfill = 10 layers. Foreground ORA layer masks overlap
# on purpose: they are editable working groupings, not accurate original cuts.

def draw_masks(size):
    masks=[]
    for name,polygons in REGIONS:
        mask=Image.new('L', size,0)
        d=ImageDraw.Draw(mask)
        for polygon in polygons:d.polygon(polygon,fill=255)
        masks.append((name,mask))
    return masks

def inpaint_underpaint(original_rgb,masks):
    alpha=np.maximum.reduce([np.asarray(mask) for _,mask in masks])
    # 4px extra ensures no ghost pixels exactly at seam when a mask moves.
    dilated=cv2.dilate(alpha,np.ones((7,7),np.uint8),iterations=1)
    # cv2 accepts RGB ndarray for inpaint even though it is normally BGR.
    new=cv2.inpaint(np.array(original_rgb),dilated,3,cv2.INPAINT_TELEA)
    return Image.fromarray(new,'RGB'), Image.fromarray(dilated,'L')

def to_bytes(im):
    out=io.BytesIO(); im.save(out,'PNG');return out.getvalue()

def composite(layers,size):
    out=Image.new('RGBA',size,(0,0,0,0))
    for _,im in reversed(layers):out=Image.alpha_composite(out,im)
    return out

def create(source, out):
    orig=Image.open(source).convert('RGB')
    w,h=orig.size
    masks=draw_masks((w,h))
    under, fill_mask=inpaint_underpaint(orig,masks)
    layers=[]
    for name,mask in masks:
        layer=orig.copy().convert('RGBA');layer.putalpha(mask)
        layers.append((name,layer))
    # Since the working masks overlap, the top image always shows exactly the
    # original pixels, while the lower image is approximate backfilled content.
    # Fill visible pixels outside every mask with original image pixels so the
    # composite is pixel-for-pixel identical to source.
    overall=np.maximum.reduce([np.asarray(mask) for _,mask in masks])
    bg=np.asarray(under).copy()
    unmasked=overall==0
    bg[unmasked]=np.asarray(orig)[unmasked]
    layers.append(('underpaint_estimated_NOT_SOURCE',Image.fromarray(bg,'RGB').convert('RGBA')))
    combined=composite(layers,(w,h)).convert('RGB')
    diff=np.any(np.array(combined)!=np.array(orig),axis=2)
    drift=int(diff.sum())
    if drift:raise RuntimeError(f'Reconstruction must preserve static composite; drift={drift}')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    root=ET.Element('image',{'w':str(w),'h':str(h),'name':'CP317 PROXY Back - NOT CP313 ORIGINAL','version':'0.0.3'})
    st=ET.SubElement(root,'stack',{'name':'visible proxy parts','isolation':'isolate','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over'})
    with zipfile.ZipFile(out,'w') as z:
        # OpenRaster recommends mimetype first, uncompressed.
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        z.writestr('mergedimage.png',to_bytes(combined.convert('RGBA')),compress_type=zipfile.ZIP_DEFLATED)
        z.writestr('data/back_reference_original.png',to_bytes(orig),compress_type=zipfile.ZIP_DEFLATED)
        for i,(name,layer) in enumerate(layers):
            path=f'data/layer_{i:02d}.png'
            z.writestr(path,to_bytes(layer),compress_type=zipfile.ZIP_DEFLATED)
            ET.SubElement(st,'layer',{'name':name,'src':path,'x':'0','y':'0','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over'})
        z.writestr('data/CP317_PROVENANCE.json', json.dumps({
            'type':'PROXY_RECONSTRUCTION_NOT_ORIGINAL',
            'source':'Flattened PNG Back reference',
            'source_sha256':sha256(Path(source).read_bytes()).hexdigest(),
            'CP313_original':False,
            'rig_approved':False,
            'static_composite_drift_pixels':drift,
        },ensure_ascii=False,indent=2))
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    stem=out.with_suffix('')
    (stem.parent/'preview').mkdir(exist_ok=True)
    combined.save(stem.parent/'preview'/'CP317_static_composite.png')
    Image.fromarray(overall,'L').save(stem.parent/'preview'/'CP317_foreground_union_mask.png')
    fill_mask.save(stem.parent/'preview'/'CP317_inpaint_area_mask.png')
    # Make colorized layered QA overlay.
    from PIL import ImageFont
    overlay=orig.copy().convert('RGBA')
    colors=[(233,92,69),(50,160,226),(220,72,179),(213,165,55),(79,214,137),
            (163,105,247),(219,98,94),(49,126,214),(249,165,58)]
    for i,(name,mask) in enumerate(masks):
        tint=Image.new('RGBA',overlay.size,colors[i]+(0,))
        colored=mask.point(lambda a: int(a*0.16))
        tint.putalpha(colored)
        overlay=Image.alpha_composite(overlay,tint)
    overlay.convert('RGB').save(stem.parent/'preview'/'CP317_proxy_mask_overlay.png')
    # Small hair displacements: move ONLY selected hair overlay group, not rig.
    hair=[i for i,(name,_) in enumerate(layers) if name.startswith('hair_')]
    for dx,dy,label in ((5,0,'right_5px'),(-5,0,'left_5px'),(0,5,'down_5px'),(0,-5,'up_5px')):
        moved=[]
        for i,(name,im) in enumerate(layers):
            if i in hair:
                temp=Image.new('RGBA',(w,h));temp.paste(im,(dx,dy));moved.append((name,temp))
            else:moved.append((name,im))
        composite(moved,(w,h)).convert('RGB').save(stem.parent/'preview'/f'CP317_hair_motion_{label}.png')
    report={'checkpoint':'CP317','status':'NON_ORIGINAL_PROXY_FOR_ART_REVIEW',
            'source_file':str(source),'source_sha256':sha256(Path(source).read_bytes()).hexdigest(),
            'canvas':[w,h],'layer_count':len(layers),
            'layer_names_top_to_bottom':[x[0] for x in layers],
            'static_composite_drift_pixels':drift,
            'limitations':['Regions are hand-drawn proxy polygons; not true CP313 cuts',
                           'The hidden shoulder and clothing pixels were approximated using inpaint',
                           'Hair-motion previews are diagnostic, not approved animation',
                           'No +17% geometry adjustment is applied: reference geometry is unchanged'],
            'ready_for_spine_rig':False,'ready_to_replace_CP313':False,
            'source_files_are_not_embedded_as_authentic_CP313':True}
    (stem.parent/'CP317_proxy_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source',nargs='?',default=str(SOURCE))
    parser.add_argument('--out',default=str(ROOT/'CP317_LamThien_Back_10Layer_RECONSTRUCTION_NOT_ORIGINAL.ora'))
    args=parser.parse_args()
    print(json.dumps(create(args.source,args.out),ensure_ascii=False,indent=2))
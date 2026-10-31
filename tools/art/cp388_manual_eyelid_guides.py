#!/usr/bin/env python3
"""CP388 CANON-exact Lâm Thiển face + editable eyelid linework guides.

No automated skin repaint and NO accepted closed-eye asset. All new layers hidden.
Source pixels in mergedimage are exactly the user-approved CANON portrait crop.
"""
from __future__ import annotations
import argparse, hashlib, io, json, shutil, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
BBOX=(25,684,193,881)
SIZE=(168,197)
SCALE=6
# Authored Bézier guides traced over the actual Lâm Thiển eyelids; stroke only,
# NOT a painted skin region or a completed blink frame.
PATHS={
 'left_upper_lash': ('M 34 108 C 42 103, 53 99.5, 64 102.0', (68,32,49,236), 1.15),
 'left_lower_lash': ('M 36 110 C 44 108.3, 54 105.7, 63 103.7', (135,58,78,174), .45),
 'left_crease': ('M 35 102 C 43 98.7, 55 96, 64 99.0', (181,99,101,146), .55),
 'right_upper_lash': ('M 89 88 C 97 82, 110 77, 122 79', (65,31,49,240), 1.20),
 'right_lower_lash': ('M 89 90 C 100 86, 111 80.4, 122 80.5', (138,63,77,174), .50),
 'right_crease': ('M 89 79 C 99 75.8, 112 73, 123 74.0', (172,85,96,149), .56),
}
ROIS={'left': (29,94,69,119),'right':(85,69,130,99)}

def verify_canon(path):
    path=Path(path)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=SHA:
        raise ValueError('CANON_SHA_MISMATCH: exact user-approved file required')
    with Image.open(path) as im:
        if im.size!=(941,1672) or im.mode!='RGBA':
            raise ValueError('CANON_FORMAT_MISMATCH')
        return im.crop(BBOX).copy()

def sample_cubic(p0,p1,p2,p3,n=150):
    return [tuple(sum(((1-t)**3*p0[d],3*(1-t)**2*t*p1[d],3*(1-t)*t*t*p2[d],t**3*p3[d])) for d in range(2)) for t in (i/n for i in range(n+1))]

def parse_and_sample(d):
    s=d.replace(",", " ").split(); assert s[0]=='M' and s[3]=='C' and len(s)==10
    f=list(map(float, [s[1],s[2],s[4],s[5],s[6],s[7],s[8],s[9]]))
    return sample_cubic((f[0],f[1]),(f[2],f[3]),(f[4],f[5]),(f[6],f[7]))

def layer_svg(name, path, rgba, width):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="168" height="197" viewBox="0 0 168 197">'
            f'<path d="{path}" fill="none" stroke="rgb({rgba[0]},{rgba[1]},{rgba[2]})" '
            f'stroke-opacity="{rgba[3]/255:.5f}" stroke-width="{width}" stroke-linecap="round"/>'
            f'</svg>\n')

def draw_layer(path,rgba,width):
    big=Image.new('RGBA',(SIZE[0]*SCALE,SIZE[1]*SCALE),(0,0,0,0))
    draw=ImageDraw.Draw(big)
    points=parse_and_sample(path)
    draw.line([(round(x*SCALE),round(y*SCALE)) for x,y in points],fill=rgba,width=max(1,round(width*SCALE)),joint='curve')
    # use premultiplied alpha sampling to avoid dark halo in native resampling
    arr=np.array(big).astype(np.float32); a=arr[:,:,3:4]/255
    rgb=np.clip(arr[:,:,:3]*a,0,255).astype(np.uint8)
    prem=np.dstack([rgb,arr[:,:,3].astype(np.uint8)])
    im=Image.fromarray(prem,'RGBA').resize(SIZE,Image.Resampling.LANCZOS)
    out=np.asarray(im).copy(); aa=np.maximum(out[:,:,3:4].astype(np.float32)/255,1e-5)
    out[:,:,:3]=np.clip(out[:,:,:3].astype(np.float32)/aa,0,255).astype(np.uint8)
    out[out[:,:,3]==0,:3]=0
    return Image.fromarray(out,'RGBA')

def save_png(im):
    o=io.BytesIO();im.save(o,'PNG');return o.getvalue()

def write_ora(src,layers,dest):
    root=ET.Element('image',w=str(SIZE[0]),h=str(SIZE[1]),name='CP388 • CANON exact + hidden eyelid art guides',version='0.0.3')
    stack=ET.SubElement(root,'stack')
    dest=Path(dest)
    with zipfile.ZipFile(dest,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        all_layers=[('CANON V2.1 EXACT OPEN EYES • VISIBLE',src,True)]+[(name+' • DRAFT hidden',im,False) for name,im in layers.items()]
        all_layers += [('MANUAL PAINT UNDERLAY • EMPTY NOT APPROVED',Image.new('RGBA',SIZE),False)]
        for i,(name,im,visible) in enumerate(all_layers):
            path=f'data/layer_{i:02d}.png';z.writestr(path,save_png(im))
            ET.SubElement(stack,'layer',{'name':name,'src':path,'opacity':'1.0','visibility':'visible' if visible else 'hidden','x':'0','y':'0','composite-op':'svg:src-over'})
        z.writestr('mergedimage.png',save_png(src));z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    with zipfile.ZipFile(dest) as z: assert z.testzip() is None
    return len(all_layers)

def make_board(src,layers,path):
    # Only actual approved Lâm Thiển CANON + exact pixel crop + hand-drawn overlays.
    font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font=ImageFont.truetype(font_path,18) if Path(font_path).exists() else ImageFont.load_default()
    small=ImageFont.truetype(font_path,15) if Path(font_path).exists() else ImageFont.load_default()
    board=Image.new('RGB',(1480,950),(17,35,56));d=ImageDraw.Draw(board)
    d.text((36,20),'THANH VÂN KÝ / CP388 — CANON LÂM THIỂN · EYELID ART GUIDES',font=font,fill=(247,248,251))
    d.text((36,50),'Bản vẽ mí mới vẫn ẨN. Chưa có lớp da khuất hoàn thiện hay hoạt ảnh được duyệt.',font=small,fill=(255,214,168))
    original=src.resize((672,788),Image.Resampling.NEAREST)
    board.paste(original.convert('RGB'),(22,95))
    d.text((32,887),'CANON V2.1 — NGẠI NGÙNG (pixel exact ×4)',font=small,fill='white')
    combined=Image.new('RGBA',SIZE)
    for im in layers.values():combined.alpha_composite(im)
    compare=src.copy();compare.alpha_composite(combined)
    board.paste(compare.resize((672,788),Image.Resampling.NEAREST).convert('RGB'),(780,95))
    d.text((784,887),'ĐƯỜNG MÍ SVG THỬ • OVERLAY CHƯA DUYỆT',font=small,fill=(255,222,176))
    board.save(path)
    return compare

def run(canon,outdir):
    src=verify_canon(canon)  # mandatory before creating any files
    outdir=Path(outdir);(outdir/'layers').mkdir(parents=True,exist_ok=True);(outdir/'qa').mkdir(exist_ok=True)
    shutil.copyfile(canon,outdir/'LAM_THIEN_CANON_V2_1_FINAL_20261029.png')
    src.save(outdir/'CANON_SHY_EXACT.png')
    layers={}
    for name,(path,color,width) in PATHS.items():
        im=draw_layer(path,color,width)
        layers[name]=im
        im.save(outdir/'layers'/f'{name}_NOT_APPROVED.png')
        (outdir/'layers'/f'{name}_NOT_APPROVED.svg').write_text(layer_svg(name,path,color,width),encoding='utf8')
    n=write_ora(src,layers,outdir/'CP388_EDITABLE_EYELID_LINEWORK_ONLY_NOT_RIG.ora')
    make_board(src,layers,outdir/'qa'/'CP388_CANON_AND_MANUAL_EYELID_LINEWORK_DRAFT.png')
    report={'checkpoint':'CP388','source_sha256':SHA,'canvas_native':list(SIZE),
        'linework_paths':list(PATHS),'art_layers':len(layers),'ora_layers':n,
        'source_static_pixel_exact':True,'new_skin_underpaint':'EMPTY/NOT_PAINTED',
        'closed_eye_master_approved':False,'visual_qa':'NOT_PASSED','frames_ready':False,
        'production_release':{'status':'blocked_pending_art','sprite_paths':{},'apk_ready':False,'spine_ready':False},
        'next':'CP389: visually paint/review eye underlay and closed-eye frame; then add independently painted in-between frames'}
    (outdir/'CP388_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    print(json.dumps(run(a.canon,a.out),ensure_ascii=False,indent=2))
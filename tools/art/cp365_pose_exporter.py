#!/usr/bin/env python3
"""TVK CP365: validate and preview genuinely authored ORA arm layers.

A technical motion export is NOT painter-authored final keyframe, Spine rig,
or user acceptance. We fail closed for flat references and empty source layers.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

import numpy as np
from PIL import Image, ImageChops

CANON_SHA = 'f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
REQUIRED = {
    'left_sleeve': '04__FRONT_SLEEVE_LEFT__PAINT',
    'left_arm_skin': '05__LEFT_ARM_SKIN__PAINT',
    'hidden_shoulder_skin': '06__LEFT_SHOULDER_HIDDEN_SKIN__PAINT',
    'bodice_main': '07__BODICE_MAIN__PAINT',
    'hidden_shoulder_bodice': '08__LEFT_SHOULDER_HIDDEN_BODICE__PAINT',
    'back_hair': '12__HAIR_BACK__PAINT',
}
MOVE = (REQUIRED['left_sleeve'], REQUIRED['left_arm_skin'])


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_ora(path):
    with zipfile.ZipFile(path) as z:
        damaged = z.testzip()
        if damaged is not None:
            raise ValueError('ORA CRC failure: ' + damaged)
        root = ET.fromstring(z.read('stack.xml'))
        size = (int(root.attrib['w']), int(root.attrib['h']))
        stack = root.find('stack')
        if stack is None:
            raise ValueError('Missing OpenRaster stack')
        layers=[]
        for node in stack.findall('layer'):
            name=node.get('name','')
            image=Image.open(io.BytesIO(z.read(node.attrib['src']))).convert('RGBA')
            if image.size != size:
                raise ValueError('Layer size mismatch: ' + name)
            if node.get('x','0')!='0' or node.get('y','0')!='0':
                raise ValueError('Layers must share 0,0 origin: ' + name)
            layers.append({'name':name,'image':image,'visible':node.get('visibility','visible')=='visible'})
        if len({layer['name'] for layer in layers}) != len(layers):
            raise ValueError('Duplicate layer names')
        return size,layers


def alpha_pixel_count(img):
    return int(np.count_nonzero(np.asarray(img.getchannel('A')) > 128))


def assess(ora,canon,min_size=(1290,2694)):
    report={'checkpoint':'CP365','source':'artist_layer_master',
            'technical_status':'BLOCKED','production_release':'blocked_pending_art',
            'visual_qa':'NOT_PASSED','spine_ready':False,'runtime_approved':False,
            'errors':[],'roles':{}}
    if sha256(canon) != CANON_SHA:
        report['errors'].append('CANON V2.1 SHA mismatch')
    else:
        report['canon_verified']=True
    try:
        size,layers=read_ora(ora)
        report['canvas']=list(size)
        if size[0]<min_size[0] or size[1]<min_size[1]:
            report['errors'].append('Canvas below native painting intake minimum')
        lookup={l['name']:l for l in layers}
        for role,name in REQUIRED.items():
            layer=lookup.get(name)
            pixels=alpha_pixel_count(layer['image']) if layer else 0
            report['roles'][role]={'name':name,'pixel_count':pixels,
                                   'present':layer is not None,'nonempty':pixels>=max(16,int(size[0]*size[1]*0.0001))}
            if layer is None or not report['roles'][role]['nonempty']:
                report['errors'].append('Unpainted semantic art: '+name)
            elif not layer['visible']:
                report['errors'].append('Mandatory art layer hidden: '+name)
        flat_refs=[l['name'] for l in layers if l['visible'] and
                   ('REFERENCE_ONLY' in l['name'] or 'NOT_PAINT' in l['name'] or
                    'FLAT_REFERENCE' in l['name'])]
        if flat_refs:
            report['errors'].append('Flat guide layers still visible: '+', '.join(flat_refs))
        report['flat_reference_visible']=bool(flat_refs)
        report['layer_count']=len(layers)
        if not report['errors']:
            report['technical_status']='READY_FOR_MOTION_DRAFT'
        return report,size,layers
    except (OSError,ValueError,zipfile.BadZipFile,ET.ParseError,KeyError) as exc:
        report['errors'].append('Invalid layered master: '+str(exc))
        return report,None,None


def composite(layers,size,angle=0,pivot=None):
    """Top-to-bottom OpenRaster stack. Group touching arm layers before rotate."""
    if pivot is None:
        pivot=(size[0]*.325,size[1]*.31)
    lookup={l['name']:l for l in layers}
    if any(name not in lookup for name in MOVE):
        raise ValueError('Missing two arm motion layers')
    if [l['name'] for l in layers].index(MOVE[1]) != [l['name'] for l in layers].index(MOVE[0])+1:
        raise ValueError('Arm skin/sleeve layers must be adjacent for grouped interpolation')
    # Topmost sleeve, lower arm skin. Build one premultiplied RGBA image.
    group=Image.new('RGBA',size)
    group.alpha_composite(lookup[MOVE[1]]['image'])
    group.alpha_composite(lookup[MOVE[0]]['image'])
    if angle:
        group=rotate_premultiplied(group,angle,pivot)
    merged=Image.new('RGBA',size)
    for layer in reversed(layers):
        name=layer['name']
        if name == MOVE[1] or not layer['visible']:
            continue
        merged.alpha_composite(group if name==MOVE[0] else layer['image'])
    return merged


def rotate_premultiplied(image,angle,pivot):
    """Rotation with premultiplied RGB to reduce dark fringes at cutout edges."""
    rgba=np.asarray(image).astype(np.float32)
    alpha=rgba[:,:,3:4]/255.0
    pre=(rgba[:,:,:3]*alpha).clip(0,255).astype('uint8')
    pre_rot=Image.fromarray(pre,'RGB').rotate(angle,Image.Resampling.BICUBIC,center=pivot)
    alpha_rot=image.getchannel('A').rotate(angle,Image.Resampling.BICUBIC,center=pivot)
    a=np.asarray(alpha_rot,dtype=np.float32)/255.0
    rgb=np.asarray(pre_rot,dtype=np.float32)
    out=np.zeros((*a.shape,4),dtype=np.uint8)
    valid=a>1e-5
    out[:,:,:3][valid]=(rgb[valid]/a[valid,None]).clip(0,255).astype(np.uint8)
    out[:,:,3]=np.asarray(alpha_rot)
    return Image.fromarray(out,'RGBA')


def export(ora,canon,directory,angle=-12,pivot=None,min_size=(1290,2694)):
    report,size,layers=assess(ora,canon,min_size=min_size)
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    report['requested_angle_degrees']=angle
    if size and pivot:
        report['requested_pivot_px']=list(pivot)
    if report['technical_status']=='READY_FOR_MOTION_DRAFT':
        rest=composite(layers,size,0,pivot)
        raised=composite(layers,size,angle,pivot)
        if not ImageChops.difference(rest,raised).getbbox():
            report['errors'].append('No motion visible after transform')
            report['technical_status']='BLOCKED'
        else:
            rest.save(directory/'CP365_IDLE_TECHNICAL_DRAFT.png')
            raised.save(directory/'CP365_ARM_RAISE_TECHNICAL_DRAFT.png')
            report['outputs']=['CP365_IDLE_TECHNICAL_DRAFT.png','CP365_ARM_RAISE_TECHNICAL_DRAFT.png']
            report['technique']='grouped bitmap arm rotation; NOT an independently illustrated raised-arm keyframe'
    (directory/'CP365_GATE_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ora',required=True)
    p.add_argument('--canon',required=True)
    p.add_argument('--out',required=True)
    p.add_argument('--angle',type=float,default=-12)
    p.add_argument('--pivot',nargs=2,type=float)
    args=p.parse_args()
    report=export(args.ora,args.canon,args.out,args.angle,tuple(args.pivot) if args.pivot else None)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report['technical_status']=='READY_FOR_MOTION_DRAFT' else 2

if __name__=='__main__':
    raise SystemExit(main())
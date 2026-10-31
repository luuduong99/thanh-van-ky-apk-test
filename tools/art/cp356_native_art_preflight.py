#!/usr/bin/env python3
"""TVK CP356: fail-closed preflight for independently painted front-shoulder art.

The detector checks provenance, ORA structure, alpha content and pose pair.
Structural PASS means READY_FOR_HUMAN_VISUAL_REVIEW, never runtime-approved.
It cannot certify artistic quality, adherence to the approved CANON, or Spine motion.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
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


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def inspect(ora, canon=None, idle=None, raise_frame=None, minimum=(1290,2694)):
    report = {'checkpoint':'CP356','gate':'P0_NATIVE_FRONT_SHOULDER','required_roles':{},
              'study_layers':[],'errors':[], 'warnings':[], 'runtime_approved':False}
    if canon is None:
        report['errors'].append('CANON V2.1 file not supplied, cannot verify provenance')
    elif sha256(canon) != CANON_SHA:
        report['errors'].append('CANON V2.1 SHA256 mismatch')
    else:
        report['canon_sha256_verified'] = True
    try:
        with zipfile.ZipFile(ora) as z:
            broken=z.testzip()
            if broken:
                raise ValueError('Archive CRC failed: '+str(broken))
            root=ET.fromstring(z.read('stack.xml'))
            w,h=int(root.attrib['w']), int(root.attrib['h'])
            report['canvas'] = [w,h]
            if w < minimum[0] or h < minimum[1]:
                report['errors'].append(f'Canvas too small for current Front intake: {w}x{h}')
            layers=root.find('stack').findall('layer')
            report['total_layers']=len(layers)
            names={l.attrib.get('name',''):l for l in layers}
            report['study_layers']=[name for name in names if ('STUDY' in name or 'NOT_APPROVED' in name)]
            for role,name in REQUIRED.items():
                layer=names.get(name)
                if layer is None:
                    report['required_roles'][role]={'name':name,'status':'MISSING'}
                    report['errors'].append('Missing independently painted semantic layer: '+name)
                    continue
                blob=z.read(layer.attrib['src'])
                image=Image.open(io.BytesIO(blob)).convert('RGBA')
                if image.size!=(w,h):
                    report['errors'].append('Wrong canvas for layer '+name)
                alpha=image.getchannel('A')
                bbox=alpha.getbbox()
                visible=int(sum(alpha.histogram()[129:]))
                min_pixels=max(8,int(w*h*0.0001))
                report['required_roles'][role]={'name':name,'status':'NONEMPTY' if bbox else 'EMPTY',
                                               'alpha_bbox':list(bbox) if bbox else None,
                                               'visible_pixels_alpha_gt_128':visible,
                                               'min_visible_pixels':min_pixels}
                if bbox is None:
                    report['errors'].append('No original art pixels in mandatory layer: '+name)
                elif visible < min_pixels:
                    report['errors'].append(f'Semantic layer almost empty / placeholder: {name} ({visible} < {min_pixels})')
            # Reference or QA-only layers must never count toward independent art.
            report['semantic_roles_populated'] = sum(v['status']=='NONEMPTY' for v in report['required_roles'].values())
            report['semantic_roles_required'] = len(REQUIRED)
    except (zipfile.BadZipFile, KeyError, ET.ParseError, ValueError, OSError) as e:
        report['errors'].append('Invalid ORA: '+str(e))
    if idle is None or raise_frame is None:
        report['errors'].append('Two real painted pose exports required: idle and arm_raise')
    else:
        try:
            with Image.open(idle) as im:
                idle_image=im.convert('RGBA')
            with Image.open(raise_frame) as im:
                moved_image=im.convert('RGBA')
            report['pose_canvas'] = list(idle_image.size)
            if idle_image.size != moved_image.size:
                report['errors'].append('Idle/arm_raise canvases mismatch')
            elif idle_image.size[0] < minimum[0] or idle_image.size[1] < minimum[1]:
                report['errors'].append('Pose exports too low resolution')
            elif all(c.getbbox() is None for c in ImageChops.difference(idle_image,moved_image).split()):
                report['errors'].append('Idle and arm_raise have no visible movement')
            else:
                report['pose_images_distinct'] = True
        except (OSError, ValueError) as e:
            report['errors'].append('Pose images invalid: '+str(e))
    report['technical_status']='BLOCKED' if report['errors'] else 'READY_FOR_HUMAN_VISUAL_REVIEW'
    report['visual_qa'] = 'NOT_PASSED'  # Requires reviewed CANON comparison and actual animation; never auto-approve.
    report['production_release'] = 'blocked_pending_art'
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ora',required=True)
    parser.add_argument('--canon')
    parser.add_argument('--idle')
    parser.add_argument('--arm-raise')
    parser.add_argument('--report')
    args=parser.parse_args()
    report=inspect(args.ora,args.canon,args.idle,args.arm_raise)
    data=json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    if args.report:
        Path(args.report).write_text(data,encoding='utf-8')
    print(data,end='')
    raise SystemExit(2 if report['technical_status']=='BLOCKED' else 0)


if __name__=='__main__':main()
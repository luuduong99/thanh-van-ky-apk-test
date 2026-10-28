#!/usr/bin/env python3
"""Read-only OpenRaster QA for Thanh Van Ky; CP315.

Usage:
  python tools/art/audit_ora.py cp313.ora --expect-layers 10 --out cp315_report
  python tools/art/audit_ora.py cp315.ora --baseline cp313_composite.png \
    --allowed-roi 50,140,140,200 --expect-layers 10 --out cp315_compare
  python tools/art/audit_ora.py cp315.ora --motion-layer hair \
    --motion-roi 60,160,120,130 --motion-px 5 --out cp315_motion

Note: no source image is altered. This is a diagnostic, NOT a Spine renderer.
"""
import argparse
from contextlib import contextmanager
import io
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image, ImageChops, ImageDraw, ImageFilter


@contextmanager
def open_ora(path):
    path = Path(path)
    if path.suffix.lower() == '.ora':
        with zipfile.ZipFile(path) as z:
            yield z
        return
    if path.suffix.lower() != '.zip':
        raise ValueError('Expected .ora or .zip containing exactly one .ora')
    with zipfile.ZipFile(path) as z:
        nested = [n for n in z.namelist() if n.lower().endswith('.ora') and not n.startswith('__MACOSX/')]
        if len(nested) != 1:
            raise ValueError(f'Expected one .ora inside ZIP; found {len(nested)}')
        info = z.getinfo(nested[0])
        if info.file_size > 300 * 1024 * 1024:
            raise ValueError('Nested ORA exceeds 300 MB safe limit')
        with zipfile.ZipFile(io.BytesIO(z.read(nested[0]))) as inner:
            yield inner


def parse_roi(value, size):
    try:
        values = [int(v.strip()) for v in value.split(',')]
        if len(values) != 4:
            raise ValueError
        x, y, w, h = values
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x+w > size[0] or y+h > size[1]:
            raise ValueError
        return (x, y, x+w, y+h)
    except ValueError:
        raise ValueError(f'Invalid ROI {value!r}; use x,y,width,height within {size}') from None


def checkerboard(size, tile=16):
    image = Image.new('RGBA', size, '#dedede')
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x//tile + y//tile) % 2 == 0:
                draw.rectangle((x, y, min(x+tile-1,size[0]-1), min(y+tile-1,size[1]-1)), fill='#efefef')
    return image


def pixels(image):
    """Pillow 13+ compatible pixel iterator."""
    return image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()


def count_nonzero(diff):
    # Includes alpha channel changes. Image.getbbox can hide RGB changes when alpha=0;
    # counting the full RGBA tuple avoids that mistake.
    return sum(1 for p in pixels(diff) if any(p))


def roi_mask(size, rois):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    for r in rois:
        draw.rectangle((r[0],r[1],r[2]-1,r[3]-1), fill=255)
    return mask


def render(layers, size, displacements=None):
    displacements = displacements or {}
    composite = Image.new('RGBA', size)
    for layer in reversed(layers):
        if not layer['visible']:
            continue
        x,y = layer['offset']
        dx,dy = displacements.get(layer['index'], (0,0))
        placed = Image.new('RGBA', size)
        placed.paste(layer['image'], (x+dx,y+dy))
        if layer['opacity'] < 1:
            a = placed.getchannel('A').point(lambda v: round(v*layer['opacity']))
            placed.putalpha(a)
        composite = Image.alpha_composite(composite, placed)
    return composite


def extract_layers(ora, errors, warnings):
    root = ET.fromstring(ora.read('stack.xml'))
    w,h = int(root.attrib['w']), int(root.attrib['h'])
    if not (0 < w <= 10000 and 0 < h <= 10000):
        raise ValueError('ORA canvas size outside safe range')
    if root.find('.//stack/stack') is not None:
        warnings.append('Nested stack found: transforms, visibility and blending of parent stacks not simulated')
    nodes = list(root.iter('layer'))
    known = set(ora.namelist())
    layers = []
    for idx,node in enumerate(nodes):
        name = node.attrib.get('name',f'Layer_{idx+1}')
        src = node.attrib.get('src','')
        if not src or src not in known:
            errors.append(f'Missing layer data for {name}: {src}')
            continue
        image = Image.open(io.BytesIO(ora.read(src))).convert('RGBA')
        if image.width > 10000 or image.height > 10000:
            errors.append(f'Layer {name}: dimensions too large')
            continue
        x,y = int(node.attrib.get('x','0')),int(node.attrib.get('y','0'))
        opacity = float(node.attrib.get('opacity','1'))
        if not 0 <= opacity <= 1:
            errors.append(f'Layer {name}: invalid opacity {opacity}')
            continue
        blend = node.attrib.get('composite-op','svg:src-over')
        if blend not in ('svg:src-over','normal'):
            warnings.append(f'{name}: unsupported blend mode {blend}; static render may differ from editor')
        if x < 0 or y < 0 or x+image.width > w or y+image.height > h:
            warnings.append(f'{name}: layer extends outside canvas')
        if image.getchannel('A').getbbox() is None:
            warnings.append(f'{name}: empty alpha')
        layers.append({'index':idx,'name':name,'src':src,'image':image,
                       'offset':(x,y),'opacity':opacity,
                       'visible':node.attrib.get('visibility','visible') != 'hidden',
                       'blend':blend})
    return (w,h),len(nodes),layers


def motion_test(layers, size, reference, selection, roi, px, out, threshold):
    matched = [l for l in layers if l['visible'] and any(s.lower() in l['name'].lower() for s in selection)]
    if not matched:
        raise ValueError(f'No visible layer matched --motion-layer {selection!r}')
    if len(matched) == len([l for l in layers if l['visible']]):
        raise ValueError('Motion selection matches every visible layer; choose actual hair layer names')
    # Pixels completely opaque in a 3x3 neighborhood in rest pose, inside ROI.
    # This avoids treating the normal exterior silhouette as a hole.
    alpha = reference.getchannel('A')
    stable_interior = alpha.filter(ImageFilter.MinFilter(3))
    selected_roi = roi_mask(size,[roi])
    protected = ImageChops.multiply(stable_interior.point(lambda v: 255 if v >= 240 else 0),selected_roi)
    cases=[]
    for axis,step in [('x',-px),('x',px),('y',-px),('y',px)]:
        shift = (step,0) if axis == 'x' else (0,step)
        changed = render(layers,size,{l['index']:shift for l in matched})
        moved_alpha = changed.getchannel('A')
        new_holes = ImageChops.multiply(moved_alpha.point(lambda v: 255 if v <= 15 else 0),protected)
        count = sum(1 for v in pixels(new_holes) if v)
        name=f'motion_{axis}_{step:+d}'
        Image.alpha_composite(checkerboard(size),changed).save(out / (name+'.png'))
        new_holes.save(out / (name+'_new_holes_mask.png'))
        cases.append({'shift_px':list(shift),'new_interior_holes':count})
    return {'selected_layers':[l['name'] for l in matched], 'roi':list(roi),
            'threshold':threshold,'cases':cases,
            'max_new_interior_holes':max(x['new_interior_holes'] for x in cases)}


def run(args):
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    errors,warnings=[],[]
    with open_ora(args.source) as ora:
        size,nlayers,layers=extract_layers(ora,errors,warnings)
        if args.expect_layers is not None and nlayers != args.expect_layers:
            errors.append(f'Expected {args.expect_layers} layers, got {nlayers}')
        if len(layers) != nlayers:
            errors.append(f'Could not read all layers ({len(layers)}/{nlayers})')
        composite=render(layers,size)
        composite.save(out/'composite_rgba.png')
        Image.alpha_composite(checkerboard(size),composite).save(out/'composite_checkered.png')
        if 'mergedimage.png' in ora.namelist():
            merged=Image.open(io.BytesIO(ora.read('mergedimage.png'))).convert('RGBA')
            if merged.size!=size:
                warnings.append('mergedimage.png and ORA canvas size differ')
            else:
                mismatched=count_nonzero(ImageChops.difference(merged,composite))
                if mismatched:
                    warnings.append(f'mergedimage.png mismatch: {mismatched} pixels; inspect blend modes and stack effects')
        basereport=None
        if args.baseline:
            baseline=Image.open(args.baseline).convert('RGBA')
            if baseline.size!=size:
                errors.append('Baseline size mismatch')
            else:
                diff=ImageChops.difference(baseline,composite)
                diff.save(out/'baseline_pixel_diff.png')
                diffmask=Image.new('L',size)
                diffmask.putdata([255 if any(p) else 0 for p in pixels(diff)])
                rois=[parse_roi(s,size) for s in args.allowed_roi]
                allowed=roi_mask(size,rois) if rois else Image.new('L',size,0)
                outside=ImageChops.subtract(diffmask,allowed)
                outside_count=sum(1 for v in pixels(outside) if v)
                inside_count=sum(1 for v in pixels(ImageChops.multiply(diffmask,allowed)) if v)
                total=inside_count+outside_count
                outside.save(out/'outside_allowed_changes_mask.png')
                basereport={'total_changed_pixels':total,'within_allowed_rois':inside_count,
                            'outside_allowed_rois':outside_count,'allowed_rois':[list(r) for r in rois]}
                if outside_count>args.max_outside_changes:
                    errors.append(f'Pixel drift outside allowed ROI: {outside_count} > {args.max_outside_changes}')
        previews=[]
        if args.roi:
            for i,value in enumerate(args.roi):
                box=parse_roi(value,size)
                crop=Image.alpha_composite(checkerboard(size),composite).crop(box)
                crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST).save(out/f'roi_{i+1}_4x.png')
                previews.append(list(box))
        # Create alpha-only contact sheet, layering each PNG onto checkerboard.
        tw=160
        th=max(1,round(tw*size[1]/size[0]))
        cw,ch=240,th+56
        sheet=Image.new('RGB',(cw*2,ch*((len(layers)+1)//2)),'#f7f7f7')
        draw=ImageDraw.Draw(sheet)
        for i,l in enumerate(layers):
            layerimg=Image.new('RGBA',size)
            layerimg.paste(l['image'],l['offset'])
            isolation=Image.alpha_composite(checkerboard(size),layerimg)
            isolation.thumbnail((tw,th))
            px,py=(i%2)*cw,(i//2)*ch
            sheet.paste(isolation.convert('RGB'),(px+8,py+8))
            draw.text((px+8,py+th+12),f'{i+1:02d} '+l['name'][:28],fill='#222222')
        sheet.save(out/'layers_contact_sheet.jpg',quality=90)
        motion=None
        if args.motion_layer:
            if not args.motion_roi:
                errors.append('--motion-roi is required with --motion-layer')
            else:
                motion=motion_test(layers,size,composite,args.motion_layer,
                                   parse_roi(args.motion_roi,size),args.motion_px,out,args.max_holes)
                if motion['max_new_interior_holes']>args.max_holes:
                    errors.append(f'Motion alpha holes: {motion["max_new_interior_holes"]} > {args.max_holes}')
    report={
        'source':str(args.source),'canvas':list(size),'layers_expected':args.expect_layers,
        'layer_count':nlayers,'layers':[{'order_top_first':l['index']+1,'name':l['name'],
            'visible':l['visible'],'size':list(l['image'].size),'offset':list(l['offset']),
            'opacity':l['opacity'],'blend':l['blend'],'source':l['src']} for l in layers],
        'baseline_comparison':basereport,'motion_test':motion,'preview_rois':previews,
        'warnings':warnings,'errors':errors,
        'result': 'FAIL' if errors else ('INSPECTION_READY_WITH_WARNINGS' if warnings else 'INSPECTION_READY')
    }
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'result':report['result'],'layers':nlayers,'warnings':warnings,
                      'errors':errors,'out':str(out)},ensure_ascii=False))
    return 1 if errors else 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',help='10-layer ORA file or ZIP containing exactly one ORA')
    parser.add_argument('--out',default='ora_audit')
    parser.add_argument('--expect-layers',type=int)
    parser.add_argument('--baseline',help='Before-edit RGBA/PNG composite, same canvas as ORA')
    parser.add_argument('--allowed-roi',action='append',default=[],help='ROI where edits are permitted (repeat), x,y,w,h')
    parser.add_argument('--max-outside-changes',type=int,default=0)
    parser.add_argument('--roi',action='append',default=[],help='4x crop for manual inspection (repeat), x,y,w,h')
    parser.add_argument('--motion-layer',action='append',default=[],help='Name substring of HAIR layer(s) to displace')
    parser.add_argument('--motion-roi',help='Seam/interior check ROI, x,y,w,h')
    parser.add_argument('--motion-px',type=int,default=5,help='Shift x,y by +/-px, default 5')
    parser.add_argument('--max-holes',type=int,default=0,help='Allowed new transparent interior pixels in motion ROI')
    args=parser.parse_args()
    try:
        if args.allowed_roi and not args.baseline:
            raise ValueError("--allowed-roi requires --baseline")
        if args.motion_px<1 or args.motion_px>50 or args.max_holes<0 or args.max_outside_changes<0:
            raise ValueError('Invalid threshold/displacement values')
        raise SystemExit(run(args))
    except (OSError,ValueError,KeyError,ET.ParseError,zipfile.BadZipFile) as exc:
        parser.exit(2,f'ORA audit unavailable: {exc}\n')


if __name__ == '__main__':
    main()
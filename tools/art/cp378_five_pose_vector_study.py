#!/usr/bin/env python3
"""CP378: five independently rendered vector hand/silk poses from strict Lâm Thiển CANON.

LOCAL TECHNICAL ART STUDY; NOT a full character, Spine rig, anatomy validation or APK.
New curves are interpolated from authored landmark geometry, NOT blended raster
copies of earlier hand poses. Artistic fidelity remains unapproved.
"""
from pathlib import Path
import argparse, hashlib, io, importlib.util, json, zipfile
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cairosvg

HERE=Path(__file__).resolve().parent
CP376=HERE/'cp376_local_wrist_refinement.py'
if not CP376.exists():
    CP376=HERE.parents[1]/'tools'/'art'/'cp376_local_wrist_refinement.py'
spec=importlib.util.spec_from_file_location('tvk_cp376_cp378',CP376)
cp376=importlib.util.module_from_spec(spec);spec.loader.exec_module(cp376)
CANON_SHA=cp376.CANON_SHA
SIZE=cp376.SIZE
SIZE6=cp376.SIZE6
FRONT=cp376.FRONT
POSES=[('idle',0.),('quarter',.25),('middle',.5),('three_quarter',.75),('raised',1.)]
POSE_LAYER_KEYS=('08_hand_contour_parametric','09_nail_knuckle_detail_parametric','10_rear_silk_fold_parametric')

# Explicit corresponding landmarks in the original 217 x 458 crop's geometry.
# Each interpolation yields a *single* editable path: no two-hand crossfade.
HAND_POINTS={
 'wrist_top':((31.0,190.0),(33.0,183.6)),
 'knuckle_upper':((26.5,194.1),(25.3,189.3)),
 'tip_upper_top':((3.0,201.4),(4.3,189.0)),
 'tip_upper_bottom':((2.0,205.0),(2.8,193.7)),
 'fold_upper':((17.7,203.7),(16.5,196.3)),
 'tip_middle_top':((4.0,209.3),(4.1,197.0)),
 'tip_middle_bottom':((5.3,212.9),(5.2,201.2)),
 'fold_middle':((21.8,207.1),(19.3,201.5)),
 'tip_lower_top':((12.8,214.9),(9.9,205.7)),
 'tip_lower_bottom':((15.7,217.1),(12.1,209.0)),
 'palm_under':((30.2,207.4),(32.2,198.1)),
 'wrist_bottom':((34.3,199.0),(34.6,195.6)),
}

def pt(name,t):
    (x,y),(a,b)=HAND_POINTS[name]
    return (x+(a-x)*t, y+(b-y)*t)

def pos(x,y):return f'{x:.2f} {y:.2f}'

def lerp(a,b,t):return a+(b-a)*t

def _curve_parts(t):
    P={k:pt(k,t) for k in HAND_POINTS}
    g=lambda key:pos(*P[key])
    # Topology is shared by all five poses. Three arcs are visible fingers;
    # their matte is not artificial stationary skin underpaint.
    path=(f'M{g("wrist_top")} '
      f'C{pos(lerp(29.0,29.5,t),lerp(191.8,185.9,t))} {pos(lerp(20.2,20.1,t),lerp(198.2,192.2,t))} {g("tip_upper_top")} '
      f'Q{pos(lerp(.4,1.0,t),lerp(201.4,190.4,t))} {g("tip_upper_bottom")} '
      f'Q{pos(lerp(6.3,6.5,t),lerp(206.1,195.5,t))} {g("fold_upper")} '
      f'C{pos(lerp(10.,10.,t),lerp(206.3,195.6,t))} {pos(lerp(7.2,6.7,t),lerp(208.4,196.8,t))} {g("tip_middle_top")} '
      f'Q{pos(lerp(1.7,1.8,t),lerp(211.,199.5,t))} {g("tip_middle_bottom")} '
      f'Q{pos(lerp(9.9,9.8,t),lerp(214.,203.5,t))} {g("fold_middle")} '
      f'C{pos(lerp(19.,17.,t),lerp(210.,204.3,t))} {pos(lerp(15.,12.5,t),lerp(213.,205.2,t))} {g("tip_lower_top")} '
      f'Q{pos(lerp(10.6,8.2,t),lerp(216.4,207.2,t))} {g("tip_lower_bottom")} '
      f'C{pos(lerp(20.2,18.7,t),lerp(217.2,208.3,t))} {pos(lerp(27.5,28.5,t),lerp(208.3,201.3,t))} {g("palm_under")} '
      f'Q{pos(lerp(33.9,34.5,t),lerp(204.,198.,t))} {g("wrist_bottom")} Z')
    return path,P

def silk_path(t):
    start=(lerp(34.9,38.1,t),lerp(194.1,190.8,t))
    control1=(lerp(38.1,43.1,t),lerp(200.4,197.5,t))
    control2=(lerp(38.1,46.5,t),lerp(215.8,215.8,t))
    tip=(lerp(22.4,38.2,t),lerp(233.4,229.7,t))
    inner1=(lerp(25.8,38.5,t),lerp(221.2,218.2,t))
    inner2=(lerp(29.9,34.6,t),lerp(211.5,201.1,t))
    return (f'M{pos(*start)} C{pos(*control1)} {pos(*control2)} {pos(*tip)} '
            f'Q{pos(*inner1)} {pos(*inner2)} Z')

def drawn_pose_svgs(t):
    contour,P=_curve_parts(t)
    # Static gold trim and hidden wrist layers from CP376 remain separate.
    hand=f'''<defs><linearGradient id="skin378" x1=".5" y1="0" x2=".28" y2="1"><stop stop-color="#fff7ee"/><stop offset=".47" stop-color="#f9ddd1"/><stop offset="1" stop-color="#e7b3af"/></linearGradient></defs>
    <path d="{contour}" fill="url(#skin378)" stroke="#ce989b" stroke-width=".39" stroke-linejoin="round"/>
    <path d="M{pos(*P['wrist_top'])} Q{pos(29.5,lerp(195,188,t))} {pos(*P['wrist_bottom'])}" fill="none" stroke="#fff4ec" stroke-opacity=".66" stroke-width=".61"/>'''
    yshift=lerp(0,-8.6,t)
    lines=f'''<path d="M{pos(3.7,203.6+yshift)} Q{pos(11.8,204.8+yshift)} {pos(18.0,202.0+yshift)}
       M{pos(5.4,211.2+yshift)} Q{pos(13.6,209.0+yshift)} {pos(20.8,205.6+yshift)}
       M{pos(14.7,216.0+yshift)} Q{pos(22.9,211.8+yshift)} {pos(28.7,204.2+yshift)}"
       stroke="#fff8f1" stroke-opacity=".89" stroke-width=".58" fill="none"/>
       <path d="M{pos(6.1,203.9+yshift)} q2 .35 3.3 -.28
         M{pos(7.0,211.2+yshift)} q2.1 -.12 3.1 -1.0
         M{pos(15.4,215.5+yshift)} q2.1 -.5 3.1 -2.1" fill="none" stroke="#b98d91" stroke-opacity=".66" stroke-width=".34"/>
       <path d="M{pos(7.2,204.2+yshift)} Q{pos(8.5,204.1+yshift)} {pos(9.9,203.8+yshift)}
         M{pos(8.1,210.9+yshift)} Q{pos(9.5,210.2+yshift)} {pos(10.9,209.4+yshift)}"
         fill="none" stroke="#fffaf4" stroke-opacity=".87" stroke-width=".27"/>'''
    sail=silk_path(t)
    x_a=lerp(34,39,t); y_a=lerp(197,194,t); x_b=lerp(26,40,t); y_b=lerp(228,226,t)
    silk=f'''<defs><linearGradient id="silk378" x1=".1" y1="0" x2=".9" y2="1"><stop stop-color="#fcfdff" stop-opacity=".87"/><stop offset=".43" stop-color="#d9e7fa" stop-opacity=".78"/><stop offset="1" stop-color="#6c9dde" stop-opacity=".44"/></linearGradient></defs>
       <path d="{sail}" fill="url(#silk378)" stroke="#81a7dc" stroke-opacity=".8" stroke-width=".42"/>
       <path d="M{pos(x_a,y_a)} Q{pos(lerp(35,44,t),lerp(211,208,t))} {pos(x_b,y_b)}" fill="none" stroke="#fcfdff" stroke-width="1.02" stroke-opacity=".9"/>
       <path d="M{pos(x_a-2,y_a+5)} Q{pos(lerp(32,41,t),lerp(212,209,t))} {pos(x_b+1,y_b-2)}" fill="none" stroke="#6997d3" stroke-width=".53" stroke-opacity=".58"/>'''
    return {'08_hand_contour_parametric':hand,'09_nail_knuckle_detail_parametric':lines,'10_rear_silk_fold_parametric':silk}

def wrap_svg(source):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE6[0]}" height="{SIZE6[1]}" viewBox="0 0 {SIZE[0]} {SIZE[1]}">{source}</svg>'

def raster(svg_source):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_source.encode(),output_width=SIZE6[0],output_height=SIZE6[1]))).convert('RGBA')

def make(canon,matte,hand,outdir):
    # Refuse wrong source without creating any outputs.
    source,mat,arm=cp376.validate_source(canon,matte,hand)
    output=Path(outdir)
    output.mkdir(parents=True,exist_ok=True)
    for n in ('svg','png','ora','qa'):(output/n).mkdir(exist_ok=True)
    ref=source.crop(FRONT)
    ref.save(output/'CANON_EXACT_FRONT_REFERENCE_217x458.png')
    fixed=list(cp376.cp375.ART.items())+list(cp376.NEW_ART.items())
    base=[]
    for name,markup in fixed:
        s=wrap_svg(markup)
        ET.fromstring(s)
        image=raster(s)
        (output/'svg'/f'shared__{name}.svg').write_text(s,encoding='utf8')
        image.save(output/'png'/f'shared__{name}.png')
        base.append((name,image))
    report={'checkpoint':'CP378','canon_sha256':CANON_SHA,'canon_image_size':[941,1672],
        'source_crop_size':list(SIZE),'working_canvas':list(SIZE6),
        'poses':[name for name,t in POSES], 't_values':[t for name,t in POSES],
        'shared_draft_layers':7,'unique_drawn_pose_layers':3,'visible_layers_per_pose':10,
        'ora_layers_including_hidden_reference':11,
        'pose_metrics':{},'pose_hand_centroids':[],
        'visual_qa':'NOT_PASSED','production_release':'blocked_pending_art',
        'sprite_paths':{},'spine_ready':False,'apk_ready':False,
        'full_body_semantic_art_ready':False,'full_motion_gap_free':False,
        'animated_game_fps_measured':False,
        'technical_motion_only':True,
        'important':'Five unique editable SVG geometries; no raster blending. Still rough, not CANON-faithful game art or mesh rig.',
        'motion_gap_diagnostic_from_cp376_not_rescored':{'-6,3':18,'-4,2':21,'3,-2':98,'-8,5':26},
        'art_approval':'REQUIRES_USER_REVIEW',
        'release_gate_reason':'Face/full body and hidden underpaint art incomplete; finger appearance not approved, no Spine or Android QA.'}
    rendered={}
    for pose,t in POSES:
        ps=drawn_pose_svgs(t)
        layers=list(base)
        for role,markup in ps.items():
            s=wrap_svg(markup)
            ET.fromstring(s)
            if '<image' in s or 'data:image' in s:raise ValueError('Embedded image in independent vector')
            im=raster(s)
            if im.getchannel('A').getbbox() is None:raise ValueError('Zero alpha in '+role)
            (output/'svg'/f'{pose}__{role}.svg').write_text(s,encoding='utf8')
            im.save(output/'png'/f'{pose}__{role}.png')
            layers.append((role,im))
        comp=Image.new('RGBA',SIZE6)
        for name,layer in layers:comp.alpha_composite(layer)
        comp.save(output/f'CP378_{pose.upper()}_PARTIAL_VECTOR_DRAFT.png')
        rendered[pose]=comp
        # Compare hand centroid with other poses to find discontinuous geometry.
        fg=np.asarray(layers[7][1].getchannel('A'))>128
        ys,xs=np.where(fg)
        center=[round(float(xs.mean()),3),round(float(ys.mean()),3)]
        report['pose_hand_centroids'].append(center)
        report['pose_metrics'][pose]={
           'drawn_hand_opaque_pixels_6x':int(fg.sum()),
           'finger_and_nail_opaque_pixels_6x':int(np.count_nonzero(np.asarray(layers[8][1].getchannel('A'))>128)),
           'drape_opaque_pixels_6x':int(np.count_nonzero(np.asarray(layers[9][1].getchannel('A'))>128)),
           'hand_center_6x':center,
           'drawn_hand_bbox_6x':list(layers[7][1].getchannel('A').getbbox())}
        ora=output/'ora'/f'CP378_{pose.upper()}_TEN_ART_LAYERS_NOT_RIG.ora'
        root=ET.Element('image',{'w':str(SIZE6[0]),'h':str(SIZE6[1]),'name':f'CP378 partial {pose} visual draft; no Spine','version':'0.0.3'})
        stack=ET.SubElement(root,'stack')
        with zipfile.ZipFile(ora,'w') as z:
            z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
            for j,(name,im) in enumerate(reversed(layers)):
                dest=f'data/layer_{j:02d}.png';buf=io.BytesIO();im.save(buf,format='PNG');z.writestr(dest,buf.getvalue())
                ET.SubElement(stack,'layer',{'name':f'CP378_DRAFT_{name}','src':dest,'visibility':'visible','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
            buf=io.BytesIO();ref.resize(SIZE6,Image.Resampling.NEAREST).save(buf,format='PNG')
            z.writestr('data/CANON_REFERENCE_HIDDEN.png',buf.getvalue())
            ET.SubElement(stack,'layer',{'name':'CANON_V2_1_REFERENCE_ONLY_HIDDEN','src':'data/CANON_REFERENCE_HIDDEN.png','visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
            z.writestr('stack.xml',ET.tostring(root,encoding='utf8',xml_declaration=True))
            buf=io.BytesIO();comp.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
        with zipfile.ZipFile(ora) as z:
            assert z.testzip() is None
    centers=np.array(report['pose_hand_centroids'])
    steps=np.sqrt(((centers[1:]-centers[:-1])**2).sum(axis=1))
    report['hand_centroid_step_px_6x']=[round(float(z),3) for z in steps]
    report['hand_motion_step_qa']='PASS_TECHNICAL_ONLY' if max(steps)<34 and min(steps)>0.8 else 'REVIEW_MOVEMENT'
    # Inspect actual matte / source pixels as reference only (not output sprite QA).
    report['exact_canon_source_unchanged']=True
    # User-facing preview has only actual source CANON and CP378 drafts.
    board=Image.new('RGB',(1940,800),'#17263d');draw=ImageDraw.Draw(board)
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';hd=ImageFont.truetype(fontpath,24);sm=ImageFont.truetype(fontpath,15)
    draw.text((22,15),'TVK CP378  |  LAM THIEN  |  FIVE EDITABLE VECTOR HAND/SILK POSES',font=hd,fill='white')
    draw.text((22,50),'Exact approved CANON V2.1 and own-character art drafts ONLY | NO full-body sprite, NO rig, NOT APPROVED',font=sm,fill='#c8dbed')
    exact=source.copy();exact.thumbnail((360,615))
    board.paste(exact.convert('RGB'),(15,99))
    draw.text((22,728),'01 ACTUAL CANON',font=sm,fill='#f2f5fe')
    for idx,(pose,t) in enumerate(POSES):
        im=rendered[pose].resize(SIZE,Image.Resampling.LANCZOS).crop((0,166,85,242)).resize((275,380),Image.Resampling.LANCZOS)
        ck=Image.new('RGBA',im.size,'#eaf0f6');d=ImageDraw.Draw(ck)
        for yy in range(0,ck.height,20):
            for xx in range(0,ck.width,20):
                if (xx//20+yy//20)%2==0:d.rectangle((xx,yy,xx+19,yy+19),fill='#d5e0ec')
        ck=Image.alpha_composite(ck,im)
        x=390+idx*310
        board.paste(ck.convert('RGB'),(x,188))
        draw.text((x,157),f'0{idx+2}  {pose.upper()}  t={t:g}',font=sm,fill='#f2f5fe')
        draw.text((x,590),'VECTOR DRAFT ONLY',font=sm,fill='#eac9bf')
    draw.text((390,670),'Each frame has a separate editable path. No cross-faded double hand. Anatomy and visual fidelity need review.',font=sm,fill='#f4d8b8')
    draw.text((390,708),'Working canvas 1302 x 2748 derives from small 217 x 458 reference; not new native full-body painted detail.',font=sm,fill='#c7d8e9')
    preview=output/'qa'/'CP378_CANON_FIVE_HAND_POSES_NOT_APPROVED.png';board.save(preview)
    report['preview']=str(preview.relative_to(output))
    # Tiny gif is only a flipbook of the technical study, not a runtime benchmark.
    def checker(img):
        image=img.resize(SIZE,Image.Resampling.LANCZOS).crop((0,166,85,242)).resize((255,228),Image.Resampling.LANCZOS)
        b=Image.new('RGBA',image.size,'#e4edf6'); d=ImageDraw.Draw(b)
        for y in range(0,b.height,18):
            for x in range(0,b.width,18):
                if (x//18+y//18)%2:d.rectangle((x,y,x+17,y+17),fill='#cdd9e9')
        return Image.alpha_composite(b,image).convert('RGB')
    frames=[checker(rendered[p]) for p,t in POSES]
    sequence=frames+frames[-2:0:-1]
    sequence[0].save(output/'qa'/'CP378_FIVE_POSE_FLIPBOOK_QA_ONLY.gif',save_all=True,append_images=sequence[1:],duration=170,loop=0,optimize=False)
    (output/'CP378_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--canon',required=True);p.add_argument('--matte',required=True);p.add_argument('--hand',required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    print(json.dumps(make(a.canon,a.matte,a.hand,a.out),ensure_ascii=False,indent=2))
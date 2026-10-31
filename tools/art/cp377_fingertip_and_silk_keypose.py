#!/usr/bin/env python3
"""CP377: CANON-locked independent fingertip and silk pose drawings, DRAFT ONLY.

Two artist-authored vector outlines for fingertip variations and two separate
translucent drape-edge keypose drawings. Maintains source lock and rejects the
idea that all moved fingertip silhouette pixels are missing underpaint.
Not rigged, not a complete hand, not high-resolution full-body production art.
"""
from pathlib import Path
import argparse,hashlib,io,json,zipfile,importlib.util,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageChops
import numpy as np
import cairosvg
CP376_PATH=Path(__file__).with_name('cp376_local_wrist_refinement.py')
_spec=importlib.util.spec_from_file_location('tvk_cp376_for_cp377',CP376_PATH)
cp376=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cp376)

CANON_SHA=cp376.CANON_SHA
FRONT=cp376.FRONT
SIZE=cp376.SIZE
SIZE6=cp376.SIZE6

# Drawn in CANON native crop coordinates; each shape is independently authored.
POSE_ART={
  'idle':{
  '08_fingertip_contour_idle': '''
   <defs><linearGradient id="handRest" x1=".7" y1="0" x2=".2" y2="1"><stop stop-color="#fff1e7"/><stop offset=".42" stop-color="#f8d5cb"/><stop offset="1" stop-color="#e9adae"/></linearGradient></defs>
   <path d="M30.5 189.6 C27.9 193.5 24.2 196.1 20.5 198.1 C15.7 200.4 10.2 201.4 4.0 201.8 Q1.1 202.4 1.2 204.1 Q2.8 205.8 6.1 204.9 L18.0 203.8 C13.6 206.2 8.4 208.1 5.0 209.5 Q2.4 211.1 3.7 212.9 Q5.2 213.8 7.9 212.6 L22.1 207.1 C18.8 209.8 15.3 212.3 12.6 214.6 Q11.4 216.6 13.2 217.5 Q15.2 217.8 17.4 216.0 L29.6 206.9 L32.5 198.6Z" fill="url(#handRest)" stroke="#d59b9f" stroke-width=".45"/>
   <path d="M3.3 203.7 Q8.6 203.9 18.9 202.0 M5.0 211.7 Q14.5 207.5 21.9 204.5 M14.0 216.3 Q23.4 208.1 28.3 205.7" stroke="#fff5ee" stroke-opacity=".83" fill="none" stroke-width=".85"/>
   <path d="M7.4 210.9 Q11 210.5 14.8 208.1 M18.7 213.7 Q23 210 26.3 206.5" stroke="#dbaaa9" stroke-opacity=".63" stroke-width=".45" fill="none"/>''',
  '09_rear_silk_pose_idle': '''
   <defs><linearGradient id="silkRest" x1="0" y1="0" x2=".75" y2="1"><stop stop-color="#f8fbff" stop-opacity=".88"/><stop offset=".45" stop-color="#d7e4f8" stop-opacity=".82"/><stop offset="1" stop-color="#7aa4df" stop-opacity=".48"/></linearGradient></defs>
   <path d="M35.1 194.1 Q36.9 205.1 33.0 215.1 C30.0 224 26.3 228.4 22.0 233.2 Q25.5 220.8 28.6 213.6 Q32.1 203.0 35.1 194.1Z" fill="url(#silkRest)" stroke="#83a8db" stroke-width=".44"/>
   <path d="M34.9 198.7 Q34.4 213.5 25.2 228.9" fill="none" stroke="#f7fbff" stroke-width="1.0" stroke-opacity=".91"/>
   <path d="M33.0 205.8 Q30.5 216.4 25.7 227" fill="none" stroke="#6f99d4" stroke-opacity=".65" stroke-width=".54"/>'''
  },
  'raised':{
  '08_fingertip_contour_raised': '''
   <defs><linearGradient id="handRaised" x1=".65" y1="0" x2=".12" y2="1"><stop stop-color="#fff7ef"/><stop offset=".35" stop-color="#f5d2c6"/><stop offset="1" stop-color="#e8aeb1"/></linearGradient></defs>
   <path d="M32.2 183.8 Q27.4 188.7 23.2 189.8 Q17.7 192 11.5 191.4 L5.4 189.8 Q3.0 189.1 2.2 190.8 Q2.2 192.3 5.3 193.4 L16.7 196.4 C12.1 196.9 8.2 197.0 4.3 196.5 Q1.9 196.8 2.3 199.1 Q3.1 200.7 6.2 200.9 Q12.7 201.6 19.0 201.4 Q14.6 204.2 10.4 205.2 Q8.0 206.0 8.2 207.9 Q9.6 209.2 12.0 208.4 C20.7 206.1 28.2 202.0 33.6 196.9 Z" fill="url(#handRaised)" stroke="#d59f9d" stroke-width=".48"/>
   <path d="M4.1 191.5 Q12.6 195.2 18.4 194.8 M4.4 198.5 Q13 200.0 20 199.0 M10.2 207.2 Q19.7 204.8 27.8 198.9" fill="none" stroke="#fff6ef" stroke-width=".75" stroke-opacity=".86"/>
   <path d="M18.5 195.6 Q23.6 194.2 27.4 192.0 M19.6 201.1 Q25.0 198.2 29.4 195" stroke="#dca9a7" fill="none" stroke-width=".48" stroke-opacity=".65"/>''',
  '09_rear_silk_pose_raised': '''
   <defs><linearGradient id="silkLift" x1=".12" y1="0" x2=".95" y2="1"><stop stop-color="#f7fbff" stop-opacity=".82"/><stop offset=".4" stop-color="#e3efff" stop-opacity=".80"/><stop offset=".74" stop-color="#9fbce8" stop-opacity=".71"/><stop offset="1" stop-color="#538bd5" stop-opacity=".45"/></linearGradient></defs>
   <path d="M38.1 190.7 Q42.6 197.8 43.7 207.5 Q44.3 217.4 38.1 229.8 C39.3 217 36.5 206.2 33.9 199.3 Q34.4 194.3 38.1 190.7Z" fill="url(#silkLift)" stroke="#83a7d8" stroke-width=".5"/>
   <path d="M37.6 193.3 Q43.5 210.7 39 226.6" fill="none" stroke="#ffffff" stroke-width="1.2" stroke-opacity=".84"/>
   <path d="M35.4 198.0 Q39.3 206.5 39.7 217.5" fill="none" stroke="#6596d1" stroke-width=".6" stroke-opacity=".59"/>'''
  }
}

def svg(name,content):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE6[0]}" height="{SIZE6[1]}" viewBox="0 0 {SIZE[0]} {SIZE[1]}">{content}</svg>'

def validate(canon,matte,hand):
    source,mat,arm=cp376.validate_source(canon,matte,hand)
    return source,mat,arm

def checker(im):
    base=Image.new('RGBA',im.size,'#e3eaf2');d=ImageDraw.Draw(base)
    for y in range(0,im.height,18):
        for x in range(0,im.width,18):
            if (x//18+y//18)%2:d.rectangle((x,y,x+17,y+17),fill='#cbd7e6')
    return Image.alpha_composite(base,im).convert('RGB')

def make(canon,matte,hand,out):
    # No filesystem mutations until the private canonical source and both upstream sources are verified.
    master,mat,arm=validate(canon,matte,hand)
    output=Path(out);output.mkdir(parents=True,exist_ok=True)
    for name in ('svg','png','ora','qa'):(output/name).mkdir(exist_ok=True)
    old=list(cp376.cp375.ART.items())+list(cp376.NEW_ART.items())
    rest_pose=master.crop(FRONT)
    report={'checkpoint':'CP377','canon_sha256':CANON_SHA,'source_crop':[217,458],
      'pose_names':list(POSE_ART),'new_independently_drawn_svg_count':4,
      'visible_draft_layers_per_pose':9,'not_same_as_canon':True,'visual_qa':'NOT_PASSED',
      'production_release':'blocked_pending_art','sprite_paths':{},'spine_ready':False,
      'apk_ready':False,'full_motion_gap_free':False,'full_body_semantic_art_complete':False,
      'critical_note':'Alternate fingertip silhouette and rear silk folds are pose art; never fill old fingertip pixels merely to force underpaint gap count to zero.',
      'quality_note':'Vectors are illustrative DRAFT shapes referencing CANON; not artist-approved accurate animated character assets.',
      'pose_metrics':{},'art_files':[]}
    rendered={}
    for pose in ('idle','raised'):
        items=[]
        for name,code in old+list(POSE_ART[pose].items()):
            s=svg(name,code)
            xml=ET.fromstring(s)
            if xml.tag.split('}')[-1]!='svg' or '<image' in s or 'data:image' in s:raise ValueError('Not original vector markup')
            img=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=SIZE6[0],output_height=SIZE6[1]))).convert('RGBA')
            if img.getchannel('A').getbbox() is None:raise ValueError('Empty vector output '+name)
            (output/'svg'/f'{pose}__{name}.svg').write_text(s,encoding='utf8')
            img.save(output/'png'/f'{pose}__{name}.png')
            items.append((name,img))
        composition=Image.new('RGBA',SIZE6)
        for name,img in items:composition.alpha_composite(img)
        composition.save(output/f'CP377_{pose.upper()}_NINE_VECTOR_DRAFT_PARTIAL.png')
        rendered[pose]=composition
        ora=output/'ora'/f'CP377_{pose.upper()}_NINE_DRAWN_LAYERS_DRAFT_NOT_SPINE.ora'
        root=ET.Element('image',{'w':str(SIZE6[0]),'h':str(SIZE6[1]),'name':f'CP377 {pose} draft ONLY','version':'0.0.3'})
        stack=ET.SubElement(root,'stack')
        with zipfile.ZipFile(ora,'w') as z:
            z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
            for i,(name,img) in enumerate(reversed(items)):
                buf=io.BytesIO();img.save(buf,format='PNG');path=f'data/layer_{i:02d}.png'
                z.writestr(path,buf.getvalue())
                ET.SubElement(stack,'layer',{'name':'DRAFT__'+name,'src':path,'visibility':'visible','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
            exact_crop=rest_pose.resize(SIZE6,Image.Resampling.NEAREST)
            buf=io.BytesIO();exact_crop.save(buf,'PNG');z.writestr('data/CANON_REFERENCE_HIDDEN.png',buf.getvalue())
            ET.SubElement(stack,'layer',{'name':'CANON_V2_1_EXACT_CROP_HIDDEN_REFERENCE','src':'data/CANON_REFERENCE_HIDDEN.png','visibility':'hidden','opacity':'1.0','x':'0','y':'0','composite-op':'svg:src-over'})
            z.writestr('stack.xml',ET.tostring(root,encoding='utf8',xml_declaration=True))
            buf=io.BytesIO();composition.save(buf,'PNG');z.writestr('mergedimage.png',buf.getvalue())
        with zipfile.ZipFile(ora) as z:
            if z.testzip() is not None:raise ValueError('ORA ZIP CRC failed')
        report['art_files'].append(str(ora.relative_to(output)))
        # Only the original reference can be measured as such. Pose drawings are still unapproved.
        fingertips=Image.new('RGBA',SIZE6)
        fingertips.alpha_composite(items[-2][1])
        fp_mask=np.asarray(fingertips.getchannel('A'))
        ribbon=np.asarray(items[-1][1].getchannel('A'))
        report['pose_metrics'][pose]={
            'drawn_fingertip_alpha_px_6x':int((fp_mask>128).sum()),
            'drawn_silk_alpha_px_6x':int((ribbon>128).sum()),
            'fingertip_alpha_bbox_6x':list(fingertips.getchannel('A').getbbox()),
            'rear_silk_alpha_bbox_6x':list(items[-1][1].getchannel('A').getbbox()),
            'flat_canon_body_rgb_changed':False}
    a,b=rendered['idle'],rendered['raised']
    report['different_pose_pixels_6x']=int(np.count_nonzero(np.any(np.asarray(a)!=np.asarray(b),axis=2)))
    # Retain CP376 baseline numbers and do not lower them using speculative silhouette painting.
    under6=Image.new('RGBA',SIZE6)
    for name,code in old:
        s=svg(name,code)
        im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=SIZE6[0],output_height=SIZE6[1]))).convert('RGBA')
        under6.alpha_composite(im)
    base_under=under6.resize(SIZE,Image.Resampling.LANCZOS)
    orig=np.asarray(arm.getchannel('A'))>128
    mask=np.asarray(base_under.getchannel('A')).copy();mask[~orig]=0
    under_a=mask>128
    diagnostics={}
    for dx,dy in [(-6,3),(-4,2),(3,-2),(-8,5)]:
        ex,_,_=cp376.calc_exposed(arm,dx,dy)
        diagnostics[f'{dx},{dy}']={'cp376_baseline_uncovered_source_px':int((ex&~under_a).sum()),
          'cp377_silhouette_ignored_for_underpaint':True}
    report['baseline_motion_diagnostics_unchanged']=diagnostics
    # Exact reference and only two local pose drafts from this character.
    board=Image.new('RGB',(1700,900),'#16273b');d=ImageDraw.Draw(board)
    fnt='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';hd=ImageFont.truetype(fnt,28);body=ImageFont.truetype(fnt,16)
    d.text((24,20),'TVK CP377 | LAM THIEN | TWO DRAWN HAND+SILK POSE VARIANTS',font=hd,fill='white')
    d.text((24,62),'CANON V2.1 SOURCE-LOCKED  |  DRAWN SVG DRAFTS, NOT IN-GAME SPRITES',font=body,fill='#cadbec')
    sheet=master.copy();sheet.thumbnail((414,720));board.paste(sheet.convert('RGB'),(20,108))
    ref=rest_pose.crop((0,155,85,238)).resize((345,405),Image.Resampling.LANCZOS)
    board.paste(ref.convert('RGB'),(475,223))
    for pose,x in [('idle',885),('raised',1285)]:
        piece=rendered[pose].resize(SIZE,Image.Resampling.LANCZOS)
        detail=piece.crop((0,155,85,238)).resize((345,405),Image.Resampling.LANCZOS)
        board.paste(checker(detail),(x,223))
    for x,label in [(20,'01 EXACT APPROVED CANON'),(475,'02 EXACT CANON WRIST CROP'),(885,'03 DRAWN IDLE DRAFT'),(1285,'04 DRAWN RAISED DRAFT')]:d.text((x,674),label,font=ImageFont.truetype(fnt,14),fill='#fff')
    d.text((475,746),'Finger contours are intentionally different; rear silk fold changes by pose.',font=body,fill='#f1d4ad')
    d.text((475,782),'CP376 baseline 18px is NOT a target to flood-fill. Visual QA remains NOT PASSED.',font=body,fill='#eac9c9')
    out_image=output/'qa'/'CP377_CANON_TWO_DRAWN_HAND_SILK_POSE_DRAFTS.png';board.save(out_image)
    report['preview']=str(out_image.relative_to(output))
    (output/'CP377_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report

if __name__=='__main__':
    pr=argparse.ArgumentParser();pr.add_argument('--canon',required=True);pr.add_argument('--matte',required=True);pr.add_argument('--hand',required=True);pr.add_argument('--out',required=True)
    x=pr.parse_args();print(json.dumps(make(x.canon,x.matte,x.hand,x.out),ensure_ascii=False,indent=2))
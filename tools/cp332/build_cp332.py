#!/usr/bin/env python3
"""CP332: artist-editable *vector study*, not an approved Lâm Thiển production asset.

Every semantic part is drawn independently into its own transparent RGBA PNG.
No facial expression features are baked into face_underpaint. This is a new
illustration that requires visual comparison/approval against canon V2.
"""
from pathlib import Path
import hashlib, json, zipfile, io, sys, copy, os
from xml.etree import ElementTree as ET
import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(os.environ.get('CP332_OUT',str(Path(__file__).resolve().parents[1])))
ART=ROOT / 'source'
SIZE=1024
EMOTIONS=['shy','angry','pain','embarrassed','alluring']
BASE_SLOTS=['hair_back','shoulders_costume','neck','ears','face_underpaint','nose_anchor','hair_front','hair_side_locks','flower_gold','choker_jewel']
FACE_SLOTS=['blush_left','blush_right','eye_white_left','eye_white_right','iris_left','iris_right','eyelashes_left','eyelashes_right','eyelid_left','eyelid_right','brow_left','brow_right','mouth']
# Portrait uses front-facing x coordinates; cannot be used as back/side geometry.
L_EYE=(417,502);R_EYE=(607,502)
SILVER='#dfdff5'; GOLD='#d9ad66'; AMBER='#d58b35'; NAVY='#182b42'

DEFS='''<defs>
 <linearGradient id="hair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fdfaff"/><stop offset=".35" stop-color="#c4cbef"/><stop offset=".7" stop-color="#b2b4d6"/><stop offset="1" stop-color="#e8e3f5"/></linearGradient>
 <linearGradient id="hairL" x1="0" y1="0" x2="1" y2=".8"><stop offset="0" stop-color="#eff0ff"/><stop offset=".48" stop-color="#a3aace"/><stop offset="1" stop-color="#f5edff"/></linearGradient>
 <linearGradient id="skin" x1="0" y1="0" x2=".87" y2="1"><stop offset="0" stop-color="#ffede6"/><stop offset=".4" stop-color="#ffe2db"/><stop offset=".76" stop-color="#f5c9c9"/><stop offset="1" stop-color="#e9aeb4"/></linearGradient>
 <linearGradient id="cloth" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fcfbff"/><stop offset=".55" stop-color="#c5d6f7"/><stop offset="1" stop-color="#7799c6"/></linearGradient>
 <radialGradient id="iris"><stop offset="0" stop-color="#ffe5a0"/><stop offset=".48" stop-color="#d99439"/><stop offset="1" stop-color="#743a32"/></radialGradient>
 <radialGradient id="blush"><stop offset="0" stop-color="#ff788a" stop-opacity=".48"/><stop offset="1" stop-color="#ff8896" stop-opacity="0"/></radialGradient>
</defs>'''

def svg_art(body):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 1024 1024">{DEFS}{body}</svg>'
def path(d,fill='none',stroke=None,sw=1,extra=''):
    return f'<path d="{d}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else '')+f' {extra}/>'
def ellipse(cx,cy,rx,ry,fill,extra=''):return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'
def circle(cx,cy,r,fill,extra=''):return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {extra}/>'

def flower(x,y,scale=1,rot=0):
    out=f'<g transform="translate({x} {y}) rotate({rot}) scale({scale})">'
    for i in range(5):out+=f'<ellipse cx="0" cy="-17" rx="11" ry="22" fill="#fffaf4" stroke="#e4d8ef" stroke-width="2" transform="rotate({i*72})"/>'
    return out+circle(0,0,9,'#d7a34e')+circle(-3,-3,3,'#fff3b7')+'</g>'

def base_art():
    b={}
    b['hair_back']=(
    path('M 304 245 C 245 285 187 402 177 615 C 170 757 130 899 105 1014 L 908 1014 C 860 839 883 645 826 449 C 797 280 665 135 480 153 C 391 155 344 182 304 245 Z','url(#hairL)','#8f98bd',5)+
    path('M 309 285 C 276 432 271 782 160 1015','none','#fff8ff',19)+
    path('M 692 230 C 774 428 764 854 860 1010','none','#858fbe',14)+
    path('M 235 519 C 264 738 226 875 190 995','none','#b7bce1',9)+
    path('M 782 447 C 796 703 796 832 846 985','none','#fffaff',10))
    b['shoulders_costume']=(
    path('M 273 1022 C 275 906 352 844 433 828 L 599 828 C 680 836 739 889 757 1022 Z','url(#cloth)','#7698c3',5)+
    path('M 316 1018 C 358 911 439 892 503 888 L 519 1024 Z','#fdfaff','#b5c6e9',4)+
    path('M 709 1018 C 663 912 605 891 518 887 L 511 1024 Z','#f8faff','#b5c6e9',4)+
    path('M 368 927 Q 443 894 508 976 Q 570 892 649 924','none','#c49960',7)+
    path('M 347 949 Q 420 937 476 1006 M 673 948 Q 604 938 547 1006','none','#6fa1cc',7))
    b['neck']=(path('M 449 705 L 452 850 Q 510 886 568 852 L 566 705 Z','url(#skin)','#c99598',4)+
                path('M 449 741 Q 457 835 502 862','none','#f7c7c0',14))
    b['ears']=(path('M 342 495 C 301 469 307 562 352 589 L 375 563 Z','url(#skin)','#ca939c',5)+
               path('M 670 507 C 718 465 724 563 682 595 L 658 566 Z','url(#skin)','#ca939c',5)+
               path('M 335 521 Q 356 504 358 559 M 697 524 Q 677 515 679 560','none','#dca5af',4))
    # No eyes, eyebrows, eyelids or mouth on this clean underpaint. Subtle nose is separate.
    b['face_underpaint']=(path('M 370 285 C 414 248 607 248 657 298 C 696 354 685 541 650 635 Q 602 752 513 765 Q 418 748 370 641 C 333 559 331 371 370 285 Z','url(#skin)','#c68f9c',5)+
          path('M 384 373 Q 369 596 441 697','none','#ffebdd',15)+
          path('M 633 371 Q 651 578 586 700','none','#eeaeb7',11))
    b['nose_anchor']=(path('M 506 553 Q 499 580 515 586','none','#d994a1',3)+circle(520,585,4,'#fff6ef'))
    b['hair_front']=(
     path('M 329 364 C 299 235 406 134 523 143 C 670 137 746 233 701 366 C 687 412 654 449 631 462 Q 651 391 615 318 Q 554 394 519 427 L 520 314 Q 458 423 411 450 Q 433 351 433 329 Q 376 410 342 456 Z','url(#hair)','#969cba',5)+
     path('M 353 374 Q 411 236 503 189 M 480 232 Q 469 313 429 392 M 542 187 Q 550 290 521 377 M 620 246 Q 663 336 645 414','none','#fffaff',12)+
     path('M 405 238 C 466 168 587 151 646 226','none','#c2badf',7))
    b['hair_side_locks']=(
     path('M 350 403 C 309 526 316 777 257 942 Q 304 867 347 692 C 365 578 365 470 365 415 Z','url(#hairL)','#a2a4c9',4)+
     path('M 674 400 C 719 549 709 772 752 955 Q 685 847 657 667 C 637 544 651 455 663 415 Z','url(#hairL)','#a2a4c9',4)+
     path('M 336 466 Q 320 699 276 894 M 688 452 Q 698 716 738 895','none','#f9f6ff',9)+
     path('M 364 520 Q 337 682 306 810','none','#bdc2e6',6))
    b['flower_gold']=(flower(282,254,1.2,-13)+flower(303,201,.75,12)+flower(249,307,.52,-15)+
     path('M 280 189 Q 354 145 433 178','none','#cfa563',8)+
     path('M 286 324 C 278 369 265 411 273 462','none','#d3a95e',5)+
     path('M 277 453 l -9 24 l 17 -6 Z','#78a9d7','#c79c56',3)+
     circle(354,161,8,'#f4d898')+circle(380,168,5,'#e4ba75'))
    b['choker_jewel']=(path('M 442 792 Q 512 824 578 791 L 570 818 Q 511 849 448 818 Z','#c5d7ed','#b38a5b',5)+
       path('M 461 806 Q 512 832 555 807','none','#d6b472',5)+
       path('M 513 809 l 16 23 l -16 32 l -16 -32 Z','#68a9d6','#b7884f',5)+
       circle(513,828,6,'#efffff'))
    return b

# Every expression only has semantic feature elements: no background skin/hair crops.
PARAMS={
'shy': {'brow':(-7,3),'eye':(0,9,1.0),'pupil':(4,5),'eyelid':2,'mouth':'shy','blush':.38},
'angry':{'brow':(14,-9),'eye':(0,-1,0.82),'pupil':(0,0),'eyelid':13,'mouth':'angry','blush':.12},
'pain':{'brow':(-16,-3),'eye':(0,13,0.60),'pupil':(0,6),'eyelid':20,'mouth':'pain','blush':.15},
'embarrassed':{'brow':(-11,5),'eye':(0,15,.62),'pupil':(5,7),'eyelid':15,'mouth':'embarrassed','blush':.64},
'alluring':{'brow':(1,-3),'eye':(0,10,.72),'pupil':(-4,2),'eyelid':18,'mouth':'alluring','blush':.20},
}

def expression_art(e):
    p=PARAMS[e];parts={}
    for side,cx in [('left',L_EYE[0]),('right',R_EYE[0])]:
        cy=L_EYE[1];edge=-1 if side=='left' else 1
        x,c=p['eye'][0],p['eye'][1];height=round(40*p['eye'][2])
        # Separate parts drawn on transparent SVG; iris is amber by policy.
        parts[f'eye_white_{side}']=path(f'M {cx-65} {cy+c} Q {cx} {cy-29+c} {cx+66} {cy+c} Q {cx} {cy+height+c} {cx-65} {cy+c} Z','#fff8f3','#bc8793',2)
        icx=cx+p['pupil'][0];icy=cy+9+c+p['pupil'][1]
        parts[f'iris_{side}']=(ellipse(icx,icy,24,28*p['eye'][2],'url(#iris)','#') if False else ellipse(icx,icy,22, max(12,25*p['eye'][2]),'url(#iris)')+
            ellipse(icx+1,icy,9,max(9,16*p['eye'][2]),'#593e48')+circle(icx-9,icy-11,7,'#fff9e8')+circle(icx+8,icy+5,3,'#fff1d1'))
        parts[f'eyelashes_{side}']=(path(f'M {cx-68} {cy+2+c} Q {cx-20} {cy-35+c} {cx+65} {cy-3+c}','none','#633a4b',9)+
             path(f'M {cx+50} {cy-11+c} l 17 -14 M {cx+58} {cy-6+c} l 15 -8','none','#633a4b',6))
        # Lid is an independent skin-tinted stroke, not pasted face pixels.
        lidY=cy-22+p['eyelid']+c
        parts[f'eyelid_{side}']=path(f'M {cx-62} {lidY} Q {cx} {lidY-17} {cx+65} {lidY-3}','none','#df9eaa',5)
        eyebrowY=cy-72+p['brow'][1]
        innerShift=p['brow'][0] *(1 if side=='left' else -1)
        parts[f'brow_{side}']=path(f'M {cx-58} {eyebrowY+7} Q {cx-15} {eyebrowY-15+innerShift} {cx+49} {eyebrowY+1}','none','#9188a4',9)
        # Blush is a transparent color gradient and never includes source skin.
        op=p['blush'];parts[f'blush_{side}']=ellipse(cx,cy+77,71,29,'url(#blush)',f'opacity="{op*1.7:.2f}"')
    mouths={
      'shy':path('M 490 640 Q 512 631 532 642 Q 511 654 493 642 Z','#b96f79','#a15b6a',3)+path('M 497 640 Q 515 644 530 640','none','#ffd2cc',3),
      'angry':path('M 482 643 Q 510 638 540 640','none','#854957',6)+path('M 490 643 Q 513 650 534 641','none','#e3a6ae',3),
      'pain':path('M 485 639 Q 500 616 522 622 Q 541 625 539 653 Q 510 669 489 649 Z','#b75e6b','#924e5a',4)+path('M 495 640 Q 519 629 534 641','none','#fff4ef',6),
      'embarrassed':path('M 497 643 Q 511 638 526 642 Q 516 647 503 643','none','#ae636e',5),
      'alluring':path('M 483 637 Q 516 652 539 631 Q 525 655 504 654 Q 491 651 483 637 Z','#c1757e','#a65e65',3)+path('M 501 646 Q 517 649 531 640','none','#fff4ec',3),
    }
    parts['mouth']=mouths[e]
    return parts

def render_svg(code):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_art(code).encode(),output_width=SIZE,output_height=SIZE))).convert('RGBA')

def sha(bytes_data):return hashlib.sha256(bytes_data).hexdigest()

def save_png(im,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    im.save(path,optimize=True)
    return sha(path.read_bytes())

def stack_xml(layer_entries):
    root=ET.Element('image',{'w':str(SIZE),'h':str(SIZE),'name':'CP332 Lâm Thiển semantic face R&D / NOT APPROVED'})
    stack=ET.SubElement(root,'stack')
    for entry in reversed(layer_entries):
        ET.SubElement(stack,'layer',{'name':entry['name'],'src':'data/'+entry['name']+'.png',
            'x':'0','y':'0','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over'})
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)

def create_ora(layers,path):
    comp=Image.new('RGBA',(SIZE,SIZE))
    for layer in layers:comp=Image.alpha_composite(comp,layer['image'])
    output=io.BytesIO();comp.save(output,format='PNG')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        z.writestr('stack.xml',stack_xml(layers))
        z.writestr('mergedimage.png',output.getvalue())
        for layer in layers:
            p=io.BytesIO();layer['image'].save(p,format='PNG')
            z.writestr('data/'+layer['name']+'.png',p.getvalue())
    return comp

def open_svg_export(part,svg,path):
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(svg_art(svg),encoding='utf-8')

def main():
    for sub in ('ora','preview','reference','source'): (ROOT/sub).mkdir(parents=True,exist_ok=True)
    base=base_art(); base_layers=[];parts_hash={};spec={}
    for k in BASE_SLOTS:
        svg=base[k];im=render_svg(svg);open_svg_export(k,svg,ART/'svg'/(k+'.svg'))
        h=save_png(im,ART/'png'/(k+'.png'));parts_hash['base/'+k]=h
        base_layers.append({'name':'base_'+k,'image':im})
    clean_base=create_ora(base_layers,ROOT/'ora'/'CP332_CLEAN_SEMANTIC_BASE_MASTER_NOT_APPROVED.ora')
    save_png(clean_base,ROOT/'preview'/'CP332_CLEAN_MASTER_NO_EYES_MOUTH.png')
    images={};all_expr=[]
    for emotion in EMOTIONS:
        pieces=expression_art(emotion);layers=[layer for layer in base_layers if layer['name'] not in ('base_hair_front','base_hair_side_locks','base_flower_gold')];slotdata={}
        for k in FACE_SLOTS:
            fragment=pieces[k];image=render_svg(fragment)
            p=ART/'png'/emotion/(k+'.png');h=save_png(image,p)
            svgpath=ART/'svg'/emotion/(k+'.svg');open_svg_export(k,fragment,svgpath)
            parts_hash[emotion+'/'+k]=h
            slotdata[k]={'alpha_nonzero_px':sum(i>0 for i in image.getchannel('A').get_flattened_data()),'sha256':h}
            layers.append({'name':'expr_'+emotion+'_'+k,'image':image})
        # Hair locks and floral ornaments must occlude the face attachments,
        # rather than letting lashes/brows draw on top of a hair fringe.
        layers.extend([layer for layer in base_layers if layer['name'] in ('base_hair_front','base_hair_side_locks','base_flower_gold')])
        comp=create_ora(layers,ROOT/'ora'/('CP332_'+emotion.upper()+'_SEMANTIC_NOT_APPROVED.ora'))
        cpath=ROOT/'preview'/('CP332_'+emotion.upper()+'_COMPOSITE.png');save_png(comp,cpath)
        images[emotion]=comp;all_expr.append({'id':emotion,'slots':slotdata,'ora':(ROOT/'ora'/('CP332_'+emotion.upper()+'_SEMANTIC_NOT_APPROVED.ora')).name,'sha256_merged':sha(cpath.read_bytes())})
    # transparency / master integrity demonstration at three scales
    bg=Image.new('RGBA',(SIZE,SIZE),(234,239,249,255))
    contact=Image.new('RGB',(5*400+60, 660),(15,32,52));draw=ImageDraw.Draw(contact)
    labels={'shy':'01 · NGAI NGUNG / SHY','angry':'02 · TUC GIAN / ANGRY','pain':'03 · DAU DON / PAIN','embarrassed':'04 · XAU HO / EMBARRASSED','alluring':'05 · QUYEN RU / ALLURING'}
    for i,e in enumerate(EMOTIONS):
        im=Image.alpha_composite(bg,images[e]).convert('RGB').resize((365,365),Image.Resampling.LANCZOS)
        contact.paste(im,(25+i*400,78))
        draw.text((25+i*400,36),labels[e],fill=(248,226,187))
        sm=Image.alpha_composite(bg,images[e]).convert('RGB').resize((132,132),Image.Resampling.LANCZOS)
        contact.paste(sm,(140+i*400,470));draw.text((25+i*400,462),'132px dialogue QA',fill=(176,204,225))
    contact.save(ROOT/'preview'/'CP332_SEMANTIC_FACE_FIVE_STATES_REVIEW.png',quality=94)
    sourcecanon=Path(os.environ.get('CP332_CANON','/mnt/data/TVK_LamThien_CANON_BodyCostume_V2_20261028.png'))
    src=Image.open(sourcecanon);native=src.crop((1160,0,1390,114));native.save(ROOT/'reference'/'CANON_V2_FACE_NATIVE_230x114.png')
    approved_path=Path(os.environ.get('CP332_EXPRESSIONS','/mnt/data/a_clean_anime_character_expression_reference_sheet.png'))
    exp=Image.open(approved_path);exp.save(ROOT/'reference'/'APPROVED_FIVE_EXPRESSION_SHEET.png')
    manifest={'checkpoint':'CP332','date':'2026-10-29','status':'hand_drawn_vector_semantic_face_study_not_user_approved_not_spine_ready',
    'canonical_visual_id':'LT_CANON_BODY_REF_2026-10-28_V2','canonical_source_sha256':sha(sourcecanon.read_bytes()),
    'approved_expression_profile_id':'LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED','approved_expression_source_sha256':sha(approved_path.read_bytes()),
    'source_type':'new_vector_paths_without_automated_cutouts_or_baked_face_expressions','vector_native_canvas':[SIZE,SIZE],
    'note':'New illustration is vector-rendered at output size, not upscaled from canon. Style/identity requires user visual review; production NOT approved.',
    'master_source_image_native':[230,114],'base_layer_names':BASE_SLOTS,'semantic_expression_layers':FACE_SLOTS,
    'base_slots_count':len(BASE_SLOTS),'expression_slots_each':len(FACE_SLOTS),'total_independent_emotion_slots':len(EMOTIONS)*len(FACE_SLOTS),
    'shared_base_hashes':{k:parts_hash['base/'+k] for k in BASE_SLOTS},'emotions':all_expr,'pixel_sources_cut_from_flat_posters':False,
    'base_baked_eyes_brows_mouth':False,'underpaint_source':'newly_drafted_vector_skin_underpaint_not_artist_approved',
    'iris_color_reference':'amber_not_blue','requires_artist_visual_approval':True,'asset_registration_allowed':False,
    'production_face_master_approved':False,'production_face_sprites_approved':False,'spine_rig_complete':False,'apk_verified':False,
    'sample_ui_sizes':[132,64],'side_three_quarter_completed':False,'wardrobe_damage_pose_integration_complete':False}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'base_layers':len(BASE_SLOTS),'face_layers':len(FACE_SLOTS)*len(EMOTIONS),'source_sha':manifest['canonical_source_sha256'],'approved_expression_sha':manifest['approved_expression_source_sha256'],'status':manifest['status']}))

if __name__=='__main__':main()
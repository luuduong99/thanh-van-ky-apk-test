#!/usr/bin/env python3
"""CP330 prototype: lossless per-expression facial patch decomposition.

Source is a newly generated *unapproved* flat reference board. The process
separates 7 painted regions into RGBA layers, creates an approximate underpaint
and preserves the source composite byte-for-byte at native resolution. It does
NOT redraw V2 high-resolution art, does not share one painted master across
emotions and is NEVER a game/Spine asset.
"""
import io, json, zipfile, hashlib
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
import cv2, numpy as np

OUT = Path(__file__).resolve().parents[1]
SOURCE = OUT / 'reference' / 'CP330_UNAPPROVED_GENERATED_SOURCE_SHEET.png'
CANON_HASH='41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711'
APPROVED_HASH='ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7'
CANON_ID='LT_CANON_BODY_REF_2026-10-28_V2'
EXP_ID='LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED'
NAMES=['shy','angry','pain','embarrassed','alluring']
VI=['Ngại ngùng','Tức giận','Đau đớn','Xấu hổ','Quyến rũ']
CROPS=[(11,90,271,460),(281,90,538,460),(546,90,803,460),(811,90,1067,460),(1074,90,1325,460)]
# Bboxes are hand annotated in *native candidate crop pixels* with loose masks;
# these are NOT facial landmarks from canon, and not artist-approved rig anchors.
BOXES={
 'shy':{'brow_image_left':(63,124,110,145),'brow_image_right':(132,105,182,130),'eye_image_left':(61,141,114,177),'eye_image_right':(130,119,189,156),'mouth':(112,183,147,211),'blush_image_left':(68,170,116,200),'blush_image_right':(151,148,198,187)},
 'angry':{'brow_image_left':(68,120,120,143),'brow_image_right':(145,111,197,136),'eye_image_left':(66,136,120,168),'eye_image_right':(143,132,203,165),'mouth':(122,186,155,211),'blush_image_left':(68,159,114,192),'blush_image_right':(172,155,214,192)},
 'pain':{'brow_image_left':(67,135,124,162),'brow_image_right':(144,114,197,140),'eye_image_left':(61,151,125,182),'eye_image_right':(143,124,201,161),'mouth':(106,180,168,214),'blush_image_left':(71,174,122,210),'blush_image_right':(155,156,210,194)},
 'embarrassed':{'brow_image_left':(62,132,116,152),'brow_image_right':(132,125,191,150),'eye_image_left':(59,148,117,186),'eye_image_right':(132,141,191,178),'mouth':(109,199,144,229),'blush_image_left':(66,176,118,217),'blush_image_right':(147,166,206,210)},
 'alluring':{'brow_image_left':(61,136,113,157),'brow_image_right':(131,117,191,143),'eye_image_left':(62,153,120,190),'eye_image_right':(135,133,202,170),'mouth':(125,188,165,219),'blush_image_left':(71,178,123,220),'blush_image_right':(153,161,205,204)},
}
PARTS=['brow_image_left','brow_image_right','eye_image_left','eye_image_right','mouth','blush_image_left','blush_image_right']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pngbytes(im):
    buf=io.BytesIO();im.save(buf,format='PNG',compress_level=6);return buf.getvalue()

def create_masks(size, boxes):
    # Mutually exclusive elliptical ROIs: 7 real source regions become independent
    # nonempty RGBA layers. Underpaint is filled below them in the master.
    occupied=Image.new('L',size,0)
    masks={}
    for name in PARTS:
        m=Image.new('L',size,0);d=ImageDraw.Draw(m)
        b=boxes[name];d.ellipse(b,fill=255)
        # Avoid ambiguous pixels under overlapping ROIs: priority to earlier layer.
        masks[name]=ImageChops.subtract(m,occupied)
        occupied=ImageChops.lighter(occupied,m)
    return masks,occupied

def rgba_from_mask(rgb, mask):
    out=rgb.convert('RGBA');out.putalpha(mask);return out

def make_ora(path, size, ordered_layers, composite):
    root=Element('image',{'w':str(size[0]),'h':str(size[1]),'name':path.stem,'version':'0.0.3'})
    stack=SubElement(root,'stack')
    with zipfile.ZipFile(path,'w') as z:
        def add(filename, payload, compress_type=zipfile.ZIP_DEFLATED):
            info=zipfile.ZipInfo(filename, date_time=(2026,10,29,0,0,0))
            info.compress_type=compress_type
            info.create_system=3
            info.external_attr=(0o100644 << 16)
            z.writestr(info,payload)
        add('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for i,(name,im,visible) in enumerate(ordered_layers):
            loc=f'data/layer_{i:02}.png'
            SubElement(stack,'layer',{'name':name,'src':loc,'opacity':'1.0','visibility':'visible' if visible else 'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
            add(loc,pngbytes(im))
        add('stack.xml',tostring(root,encoding='utf-8'))
        add('mergedimage.png',pngbytes(composite))
        add('Thumbnails/thumbnail.png',pngbytes(composite.copy().resize((min(256,size[0]),int(size[1]*min(256,size[0])/size[0])))))

def compose(bottom_to_top,size):
    canvas=Image.new('RGBA',size,(0,0,0,0))
    for im in bottom_to_top:canvas=Image.alpha_composite(canvas,im)
    return canvas

def build():
    for folder in ['ora','preview','candidates']:(OUT/folder).mkdir(parents=True,exist_ok=True)
    source=Image.open(SOURCE).convert('RGB')
    results=[]
    for name,bbox in zip(NAMES,CROPS):
        portrait=source.crop(bbox)
        W,H=portrait.size
        masks,union=create_masks(portrait.size,BOXES[name])
        for part in PARTS:
            if not masks[part].getbbox():raise RuntimeError(f'empty layer {name}/{part}')
        # Inpaint the source behind the movable facial regions. This is auto
        # filled approximate skin/hair, NOT final artist-drawn underpaint.
        mask_array=np.asarray(union,dtype=np.uint8)
        inpaint=np.array(portrait)
        inpaint=cv2.inpaint(cv2.cvtColor(inpaint,cv2.COLOR_RGB2BGR),mask_array,7,cv2.INPAINT_TELEA)
        inpaint=Image.fromarray(cv2.cvtColor(inpaint,cv2.COLOR_BGR2RGB))
        underpaint=inpaint.convert('RGBA')
        base=portrait.convert('RGBA')
        # Base is genuinely cleared where the seven individual layers are
        # painted; previous CP325 just pasted patches on top of a flat image.
        inverse=ImageChops.invert(union)
        base.putalpha(inverse)
        parts={n:rgba_from_mask(portrait,masks[n]) for n in PARTS}
        comp=compose([underpaint,base]+[parts[p] for p in PARTS[::-1]],portrait.size)
        # Compositing is exact: each original pixel is found in either base or
        # exactly one foreground part, never duplicated in both.
        diff=ImageChops.difference(comp.convert('RGB'),portrait)
        if diff.getbbox():raise RuntimeError('Pixel composite mismatch for '+name)
        # Underpaint + shifted eyes does not leave transparent alpha holes;
        # this says nothing about artist-level texture fidelity.
        shifted=Image.new('RGBA',portrait.size,(0,0,0,0))
        shifted.alpha_composite(underpaint);shifted.alpha_composite(base)
        for part in PARTS[::-1]:
            im=parts[part]
            offset=(4,-3) if part.startswith('eye_') or part=='mouth' else (0,0)
            blank=Image.new('RGBA',portrait.size,(0,0,0,0))
            blank.paste(im,offset)
            shifted.alpha_composite(blank)
        if shifted.getchannel('A').getextrema() != (255,255):raise RuntimeError('holes in shifted sample')
        ora=OUT/'ora'/f'CP330_{name}_PAINTED_REGION_TRIAL_NOT_GAME_ART.ora'
        ordered_layers=[(part,parts[part],True) for part in PARTS] + [('face_base_cutout',base,True),('automatic_underpaint_REQUIRES_ARTIST_REVIEW',underpaint,True),('GUIDE_UNAPPROVED_CP330_SOURCE_REFERENCE_ONLY',portrait.convert('RGBA'),False)]
        make_ora(ora,portrait.size,ordered_layers,comp)
        cand=OUT/'candidates'/f'{name}_NATIVE_UNAPPROVED.png';portrait.save(cand)
        comp.save(OUT/'preview'/f'CP330_{name}_COMPOSITE_NATIVE.png')
        shifted.save(OUT/'preview'/f'CP330_{name}_MOVEMENT_TEST.png')
        results.append({'expression_id':name,'source_crop_xyxy':bbox,'native_dimensions_px':[W,H], 'candidate_sha256':sha(cand),'ora_sha256':sha(ora),'independent_alpha_layers':7,'underpaint':'cv2_telea_auto_not_approved','base_has_cutouts':True,'default_composite_pixel_exact':True,'shift_test_no_alpha_holes':True,'face_shared_across_emotions':False,'qa':'tech_valid_art_unapproved','region_bounds':BOXES[name]})
    manifest={'checkpoint':'CP330','date':'2026-10-29','status':'candidate_flat_art_decomposed_technical_only_NOT_CANON','canonical_visual_id':CANON_ID,'canonical_sha256':CANON_HASH,'approved_expression_profile':EXP_ID,'approved_expression_sha256':APPROVED_HASH,'source_unapproved_generated_sheet_sha256':sha(SOURCE),'source_generated_sheet_px':list(source.size),'source_warning':'New AI art has not been approved and includes spurious final/Spine-ready labels. All such claims are false; images are R&D only.', 'production_asset_allowed':False,'same_canonical_face_master':False,'new_artist_redraw_complete':False,'spine_ready':False,'apk_ready':False,'art_preview_needs_review':True,'total_candidate_portraits':5,'total_independent_facial_painted_region_layers':35,'total_ora_files':5,'source_native_resolution_only':True,'results':results}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    create_contact(manifest)
    return manifest

def font(sz=20):
    p='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(p,sz)

def create_contact(manifest):
    # High-density review contact panel; copies native pixels, explicitly not
    # fabricated high-resolution production art.
    W,H=1560,1130
    board=Image.new('RGB',(W,H),'#0d1d31');d=ImageDraw.Draw(board)
    d.text((30,18),'TVK / LAM THIEN — CP330 PAINTED REGIONS (DRAFT ONLY)',font=font(30),fill='#f8e9cb')
    d.text((30,58),'CANON V2 and five original expressions remain APPROVED. These five NEW redraw candidates are NOT approved.',font=font(15),fill='#c8d7e5')
    for i,name in enumerate(NAMES):
        x=20+i*310
        im=Image.open(OUT/'candidates'/f'{name}_NATIVE_UNAPPROVED.png').convert('RGB')
        p=im.resize((int(im.width*.96),int(im.height*.96)),Image.Resampling.LANCZOS)
        board.paste(p,(x+22,112))
        d.text((x+20,92),f'{i+1}. {name}',font=font(20),fill='#e5d7b6')
        q=Image.open(OUT/'preview'/f'CP330_{name}_MOVEMENT_TEST.png').convert('RGB')
        q=q.resize((int(q.width*.87),int(q.height*.87)),Image.Resampling.LANCZOS)
        board.paste(q,(x+22,530))
        d.text((x+20,506),'Shifted eye/mouth QA',font=font(15),fill='#8ed2c6')
        d.text((x+18,872),f'Native: {im.width}x{im.height}px',font=font(14),fill='#d2e0ef')
        d.text((x+18,898),'7 RGBA patches; base cutouts',font=font(13),fill='#d2e0ef')
        d.text((x+18,924),'Auto underpaint: NOT approved',font=font(13),fill='#f4b89d')
    d.rectangle((18,968,W-18,1110),fill='#142d46',outline='#507a97',width=2)
    d.text((36,988),'NOT a shared face master; NOT high-resolution source; NOT Spine art; NOT a game asset.',font=font(20),fill='#f4b89d')
    d.text((36,1026),'Technical result: five editable ORAs, nonempty alpha layers, byte-exact composite, no alpha holes in shifted sample.',font=font(15),fill='#d2e0ef')
    d.text((36,1056),'Next: artist redraw matching LT_CANON_BODY_REF_2026-10-28_V2 + approved emotion direction, then independent art review.',font=font(14),fill='#d2e0ef')
    board.save(OUT/'preview'/'CP330_FIVE_FACE_REGION_QA_NOT_APPROVED.png')

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--source',type=Path,default=SOURCE,help='UNAPPROVED CP330 reference board PNG, not CANON V2')
 p.add_argument('--out',type=Path,default=OUT,help='Working output directory')
 a=p.parse_args()
 SOURCE=a.source;OUT=a.out
 if not SOURCE.is_file():p.error('Source PNG missing; use --source for local Library-backed file')
 m=build();print(json.dumps({'n':len(m['results']),'sha':m['source_unapproved_generated_sheet_sha256']},indent=2))
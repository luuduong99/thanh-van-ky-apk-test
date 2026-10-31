#!/usr/bin/env python3
"""CP340: source-locked CANON V2.1 reference crops and one experimental alpha cutout.
No semantic art layers or new image design are claimed. Requires Pillow, numpy, OpenCV.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np, cv2, hashlib, json, io, zipfile, xml.etree.ElementTree as ET

SHA='f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a'
CANON='LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29'
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'reference'/'CANON_V2_1_EXACT_ORIGINAL.png'
BBOX={
 'view_front':(13,177,228,626),
 'view_side':(232,177,365,626),
 'view_back':(364,177,562,626),
 'view_three_quarter_front':(544,177,753,626),
 'view_three_quarter_back':(741,177,913,626),
 'emotion_shy':(19,671,190,921),
 'emotion_angry':(198,671,369,921),
 'emotion_pain':(378,671,546,921),
 'emotion_embarrassed':(555,671,732,921),
 'emotion_alluring':(733,671,913,921),
 'damage_100':(16,1186,239,1388),
 'damage_70':(244,1186,461,1388),
 'damage_50':(466,1186,680,1388),
 'damage_30':(685,1186,914,1388),
}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(n=20):
 for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']:
  try:return ImageFont.truetype(p,n)
  except OSError:pass
 return ImageFont.load_default()

def make_ora(path,front,matted):
    # 2 real raster layers (one visible alpha trial and a hidden exact reference)
    w,h=front.size
    root=ET.Element('image',{'version':'0.0.3','w':str(w),'h':str(h),'name':'CP340_REFERENCE_MATTE_NOT_PRODUCTION'})
    stack=ET.SubElement(root,'stack')
    ET.SubElement(stack,'layer',{'name':'FRONT_GRABCUT_ALPHA_TRIAL_NOT_RIGGED','src':'data/layer0.png','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
    ET.SubElement(stack,'layer',{'name':'ORIGINAL_FLAT_CROP_REFERENCE_ONLY','src':'data/layer1.png','opacity':'1.0','visibility':'hidden','composite-op':'svg:src-over','x':'0','y':'0'})
    def png(im):
     buf=io.BytesIO();im.save(buf,format='PNG');return buf.getvalue()
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
     z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
     z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
     z.writestr('data/layer0.png',png(matted))
     z.writestr('data/layer1.png',png(front))
     z.writestr('mergedimage.png',png(matted))
     z.writestr('Thumbnails/thumbnail.png',png(matted.copy().resize((min(256,w),round(min(256,w)*h/w)))))

def cutout(img):
    rgb=np.array(img.convert('RGB'))
    h,w=rgb.shape[:2]
    if (w,h)!=(215,449):raise ValueError('This mask is tailored to the exact approved native front crop; never use for other models')
    mask=np.full((h,w),cv2.GC_PR_BGD,np.uint8)
    mask[:10,:]=cv2.GC_BGD;mask[-3:,:]=cv2.GC_BGD
    mask[:,:8]=cv2.GC_BGD;mask[:,-7:]=cv2.GC_BGD
    possible=[[(78,7),(143,7),(168,60),(168,124),(139,186),(154,260),(138,434),(91,437),(69,275),(65,190),(48,135),(56,75)],
              [(38,138),(96,144),(85,265),(45,333),(23,430),(10,434),(16,290)],
              [(135,126),(187,150),(207,300),(202,438),(171,438),(143,350),(128,280)]]
    for v in possible:cv2.fillPoly(mask,[np.array(v,np.int32)],cv2.GC_PR_FGD)
    certain=[[(102,25),(123,26),(131,63),(120,91),(95,86),(90,56)],
             [(94,92),(143,95),(157,144),(133,198),(95,201),(76,144)],
             [(97,198),(132,200),(133,300),(119,419),(102,420),(86,307)]]
    for v in certain:cv2.fillPoly(mask,[np.array(v,np.int32)],cv2.GC_FGD)
    cv2.setRNGSeed(0)
    bg=np.zeros((1,65),np.float64);fg=bg.copy()
    cv2.grabCut(rgb[:,:,::-1].copy(),mask,None,bg,fg,8,cv2.GC_INIT_WITH_MASK)
    alpha=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype(np.uint8)
    alpha=cv2.morphologyEx(alpha,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    alpha=cv2.GaussianBlur(alpha,(3,3),.5)
    return Image.fromarray(np.dstack([rgb,alpha]),'RGBA')

def checker(im):
    arr=np.array(im.convert('RGBA'));h,w=arr.shape[:2]
    tile=(np.indices((h,w)).sum(axis=0)//12)%2
    bg=np.where(tile[...,None],np.array([202,202,205]),np.array([249,249,249])).astype('float32')
    al=arr[:,:,3:4].astype('float32')/255
    return Image.fromarray(np.uint8(np.clip(bg*(1-al)+arr[:,:,:3].astype('float32')*al,0,255)))

def contact(crops,matted):
    canvas=Image.new('RGB',(1510,1300),'#F8FBFF');d=ImageDraw.Draw(canvas)
    d.text((34,24),'CP340  |  LAM THIEN CANON V2.1   -   SOURCE-EXACT ART INTAKE',font=font(27),fill='#173254')
    d.text((34,63),'Exact approved pixels: no redesign, no AI upscale. Experimental alpha is NOT a production sprite.',font=font(17),fill='#37516a')
    items=[('FRONT',crops['view_front']),('SIDE',crops['view_side']),('BACK',crops['view_back']),('3/4 FRONT',crops['view_three_quarter_front']),('3/4 BACK',crops['view_three_quarter_back'])]
    X=[28,329,630,931,1232]
    for i,(label,im) in enumerate(items):
     x=X[i];tw=230;th=430
     scale=min(tw/im.width,th/im.height)
     img=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.NEAREST)
     d.rounded_rectangle((x,105,x+251,599),radius=10,fill='#EFF5FC',outline='#B3C9DC',width=2)
     canvas.paste(img,(x+(251-img.width)//2,132))
     d.text((x+12,112),label,font=font(18),fill='#173254')
     d.text((x+12,575),f'native {im.width}x{im.height}',font=font(13),fill='#617487')
    # Five expressions row
    emos=['shy','angry','pain','embarrassed','alluring']
    d.text((34,625),'FIVE EXPRESSION REFERENCES - original pixels (not standalone animation layers)',font=font(21),fill='#173254')
    for i,id in enumerate(emos):
     x=25+i*301;img=crops['emotion_'+id]
     # no resample, crop as is
     canvas.paste(img,(x+60,682))
     d.text((x+61,948),id.upper(),font=font(18),fill='#17436d')
    d.text((34,995),'Damage is governed by the final V2.1 sheet: 100 / 70 / 50 / 30. Keep 30% restrained.',font=font(18),fill='#17436d')
    # alpha trial at bottom
    s=checker(matted);s.thumbnail((135,220),Image.Resampling.NEAREST)
    canvas.paste(s,(35,1045))
    d.text((195,1080),'First alpha cutout: FRONT only, native 215x449',font=font(20),fill='#173254')
    d.text((195,1120),'Real RGBA matte, but hair/fabric edges are not artist-clean.',font=font(17),fill='#7e3d30')
    d.text((195,1151),'Source flat image contains baked facial and clothing details; not a rig layer.',font=font(17),fill='#7e3d30')
    d.text((195,1190),'Art direction QA: 3/4-front looks nearly frontal; redraw distinct perspective if required.',font=font(17),fill='#7e3d30')
    d.text((195,1223),'DO NOT register these crops in Android sprite_paths. Release remains blocked.',font=font(17),fill='#7e3d30')
    return canvas

def main():
    if sha(SOURCE)!=SHA:raise ValueError('CANON V2.1 source SHA mismatch, refusing to generate')
    src=Image.open(SOURCE).convert('RGBA')
    if src.size!=(941,1672):raise ValueError('Bad source size')
    crops={}; rec=[]
    for id,box in BBOX.items():
        crop=src.crop(box);out=BASE/'extracted'/f'{id}_NATIVE_REFERENCE.png';crop.save(out)
        crops[id]=crop
        rec.append({'id':id,'source_box_xyxy':list(box),'size_px':list(crop.size),'sha256':sha(out),'exact_source_pixels':True})
    front=crops['view_front'];matted=cutout(front)
    mpath=BASE/'extracted'/'view_front_EXPERIMENTAL_GRABCUT_ALPHA_NOT_RIG.png';matted.save(mpath)
    make_ora(BASE/'ora'/'CP340_FRONT_TRIAL_REFERENCE_AND_MASK_NOT_RIG.ora',front,matted)
    contact(crops,matted).save(BASE/'preview'/'CP340_CANON_V21_VIEWS_EMOTIONS_AND_ALPHA_QA.png')
    # bigger side by side
    s=Image.new('RGB',(950,1050),'#F6F9FD');d=ImageDraw.Draw(s)
    ori=front.convert('RGB').resize((430,898),Image.Resampling.NEAREST)
    pre=checker(matted).resize((430,898),Image.Resampling.NEAREST)
    s.paste(ori,(30,78));s.paste(pre,(485,78))
    d.text((30,25),'ORIGINAL FRONT CROPPED FROM CANON V2.1',font=font(17),fill='#173254')
    d.text((485,25),'EXPERIMENTAL ALPHA - NOT RIG/PRODUCTION',font=font(17),fill='#173254')
    d.text((30,1000),'Native 215x449; preview pixel-doubled. SAME artwork, ONLY alpha changed.',font=font(17),fill='#173254')
    s.save(BASE/'preview'/'CP340_FRONT_ALPHA_SIDE_BY_SIDE.png')
    manifest={'checkpoint':'CP340','source_id':CANON,'source_sha256':SHA,'source_file':'reference/CANON_V2_1_EXACT_ORIGINAL.png',
      'original_pixel_size':[941,1672],'source_preserved':True,'reference_crops':rec,
      'first_alpha_trial':{'path':str(mpath.relative_to(BASE)),'sha256':sha(mpath),'native_size':[215,449],
        'composite_type':'GrabCut from original front pixels, non-semantic single flattened foreground',
        'source_rgb_pixels_unchanged':True,'approved':False,'hair_edges_need_redraw':True,'cloth_underdrawing_absent':True},
      'ora_path':'ora/CP340_FRONT_TRIAL_REFERENCE_AND_MASK_NOT_RIG.ora',
      'ora_sha256':sha(BASE/'ora'/'CP340_FRONT_TRIAL_REFERENCE_AND_MASK_NOT_RIG.ora'),
      'production':{'real_artist_native_highres_layers_complete':False,'clean_underpaint_done':False,'facial_attachments_independent':False,'spine_ready':False,'android_apk_verified':False,'sprite_paths_registered':0},
      'source_view_observations':['Front and 3/4 Front in this board are close in facial orientation; artist needs explicit true 3/4 perspective at production redraw',
       'damage 30% must not be exaggerated beyond approved visual reference','original full-body view cells have very low native resolution compared with rig quality'],
      'status':'P0_VISUAL_SOURCE_AUDIT_COMPLETE_P1_ONE_EXPERIMENTAL_FLAT_ALPHA_CUTOUT_NOT_PRODUCTION'}
    (BASE/'CP340_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Created',len(rec),'source-exact crops, one front matte and OpenRaster technical review')

if __name__=='__main__':main()
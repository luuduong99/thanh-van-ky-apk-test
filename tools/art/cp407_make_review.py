#!/usr/bin/env python3
"""Create CP407 15-pose animated comparison from approved-source-only DRAFT art.
This does NOT release actual production sprite or claim painter QA.
"""
import argparse, json, hashlib
from pathlib import Path
import numpy as np, cv2
from PIL import Image
import cp401_occlusion_blink as cp
import cp407_source_lash_transfer as transfer

PROGRESS=[0,.14,.28,.42,.56,.72,.86,1,.86,.72,.56,.42,.28,.14,0]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def build(root,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    open_native,closed_native=transfer.source(root)
    source_4x=np.asarray(open_native.resize(transfer.DISPLAY,Image.Resampling.LANCZOS))
    closed,layer=transfer.new_candidate(open_native,closed_native,.75)
    closed_rgba=np.asarray(closed)
    mask=transfer.roi_mask()
    def frame(p):
        if p==0:return Image.fromarray(source_4x,'RGBA')
        if p==1:return closed.copy()
        a=np.asarray(cp.eyelid_position(open_native,closed_native,p).resize(transfer.DISPLAY,Image.Resampling.LANCZOS)).copy()
        if p>.74:
            q=np.clip((p-.74)/.26,0,1);q=q*q*(3-2*q)
            a[mask,:3]=np.rint(a[mask,:3]*(1-q)+closed_rgba[mask,:3]*q).astype(np.uint8)
        a[~mask]=source_4x[~mask]
        a[:,:,3]=source_4x[:,:,3]
        return Image.fromarray(a,'RGBA')
    images=[frame(p) for p in PROGRESS]
    atlas=Image.new('RGBA',(transfer.DISPLAY[0]*15,transfer.DISPLAY[1]))
    for i,img in enumerate(images):atlas.alpha_composite(img,(i*transfer.DISPLAY[0],0))
    atlas.save(out/'CP407_ATLAS_15_4X_TRANSFER_DRAFT.png')
    gif=[img.resize((336,394),Image.Resampling.LANCZOS) for img in images]
    gif[0].save(out/'CP407_BLINK_DRAFT.gif',save_all=True,append_images=gif[1:],duration=[160,45,45,45,45,45,60,160,60,45,45,45,45,45,160],loop=0,optimize=False)
    video=out/'CP407_BLINK_COMPARISON_30FPS_DRAFT.mp4'
    vw=transfer.DISPLAY[0]*2;vh=transfer.DISPLAY[1]
    writer=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*'mp4v'),30,(vw,vh))
    if not writer.isOpened():raise ValueError('video codec unavailable')
    for i in range(72):
        p=cp.frame_progress(i/72)
        img=frame(p)
        side=np.concatenate([source_4x[:,:,:3],np.asarray(img)[:,:,:3]],axis=1)
        writer.write(cv2.cvtColor(side,cv2.COLOR_RGB2BGR))
    writer.release()
    for img in images:
        a=np.asarray(img)
        assert np.array_equal(a[~mask],source_4x[~mask])
        assert np.array_equal(a[:,:,3],source_4x[:,:,3])
    assert np.array_equal(np.asarray(images[0]),source_4x)
    assert np.array_equal(np.asarray(images[-1]),source_4x)
    assert np.array_equal(np.asarray(images[7]),closed_rgba)
    report={'checkpoint':'CP407','role':'SOURCE-LOCKED REVIEW ONLY / NOT APPROVED', 'frame_count':15,'video_frame_count':72,'fps':30,'frame_size':[672,788], 'atlas_size':list(atlas.size),'original_canon_hash':cp.CANON_SHA,'closed_candidate':sha(out/'CP407_CANON_LASH_TRANSFER_075_DRAFT.png'),'atlas_sha256':sha(out/'CP407_ATLAS_15_4X_TRANSFER_DRAFT.png'),'outside_eye_pixels_changed':0, 'user_approval':False,'production_art_approval':False,'apk_integrated':False,'source_face_is_native_hd':False,'notes':'Source texture warping improves contrast but still has pigment clumps; not a final artist-approved eyelid.'}
    (out/'CP407_BLINK_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    return report
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--root',default=str(Path(__file__).parent));a.add_argument('--out',default=str(Path(__file__).parent/'outputs'));x=a.parse_args();print(json.dumps(build(x.root,x.out),ensure_ascii=False,indent=2))
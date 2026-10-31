#!/usr/bin/env python3
"""CP354: limited local mesh motion probe; QA only, not rig or painter-grade art."""
import argparse, hashlib, io, json, zipfile
import cv2
import numpy as np
from PIL import Image

LOCKED_ZIP = "f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497"
LOCKED_CANON = "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"

def ease(x):
    t=np.clip(x,0,1)
    return t*t*(3-2*t)

def warp(source_rgba, amount=1.0):
    """Amount 0 returns pixel-exact 4x reference; 1 moves left palm ~3.8x2.2 source px."""
    original=source_rgba.convert("RGBA").resize((860,1796),Image.Resampling.NEAREST)
    if amount == 0: return original
    rgba=np.asarray(original,dtype=np.float32)/255.0
    yy,xx=np.mgrid[:1796,:860].astype("float32")
    sx,sy=xx/4,yy/4
    u=np.clip((sy-128)/68,0,1)
    center=71-57*u
    sigma=14+2*u
    influence=(ease(u)**1.6)*np.exp(-0.5*np.abs((sx-center)/sigma)**3)
    influence*=1-ease((sy-194)/30)
    mx=(xx+3.8*float(amount)*influence*4).astype("float32")
    my=(yy+2.2*float(amount)*influence*4).astype("float32")
    premul=rgba[:,:,:3]*rgba[:,:,3,None]
    pa=cv2.remap(premul,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    a=cv2.remap(rgba[:,:,3],mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    rgb=np.zeros_like(pa)
    mask=a>1e-5
    rgb[mask]=np.clip(pa[mask]/a[mask,None],0,1)
    result=np.dstack((rgb,a))
    return Image.fromarray(np.uint8(np.clip(result*255+0.5,0,255)),"RGBA")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cp348-zip",required=True)
    p.add_argument("--canon",required=True)
    p.add_argument("--amount",type=float,default=1.0)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    assert 0<=args.amount<=1
    def sha(path):return hashlib.sha256(open(path,"rb").read()).hexdigest()
    assert sha(args.cp348_zip)==LOCKED_ZIP and sha(args.canon)==LOCKED_CANON
    with zipfile.ZipFile(args.cp348_zip) as z:
        assert z.testzip() is None
        src=Image.open(io.BytesIO(z.read("FRONT_CP348_TEN_LAYER_RECON_QA_ONLY.png"))).convert("RGBA")
    result=warp(src,args.amount)
    result.save(args.output)
    print(json.dumps({"status":"QA_ONLY","canvas":[860,1796],"amount":args.amount,
      "painter_grade":False,"spine_ready":False,"release":"blocked_pending_art"}))
if __name__=="__main__":main()

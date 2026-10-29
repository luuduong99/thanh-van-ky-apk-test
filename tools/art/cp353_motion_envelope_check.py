#!/usr/bin/env python3
"""CP353: reproduce real CP348 arm-pivot alpha changes (QA only, not rig)."""
import argparse, hashlib, io, json, zipfile
from pathlib import Path
import numpy as np
from PIL import Image

SOURCE_SHA="f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497"
ANGLES=(0,-0.25,-0.5,-0.75,-1,-1.5,-2,-3,-5)
S=6

def audit(path):
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==SOURCE_SHA, "Wrong approved QA source archive"
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        names=sorted(n for n in z.namelist() if n.startswith("layers/") and n.endswith(".png"))
        assert len(names)==10 and names[5].endswith("06_left_arm_and_sleeve.png")
        layers=[Image.open(io.BytesIO(z.read(n))).convert("RGBA").resize((1290,2694),Image.Resampling.NEAREST) for n in names]
        src=np.asarray(Image.open(io.BytesIO(z.read("FRONT_CP348_TEN_LAYER_RECON_QA_ONLY.png"))).convert("RGBA"))
    out=[]
    for angle in ANGLES:
        base=Image.new("RGBA",(1290,2694))
        for i,pic in enumerate(layers):
            if i==5 and angle:
                pic=pic.rotate(angle,Image.Resampling.BICUBIC,center=(70*S,132*S))
            base.alpha_composite(pic)
        q=np.asarray(base)[3::6,3::6]
        assert np.array_equal(q[400:449],src[400:449]), "Feet changed"
        if angle==0: assert np.array_equal(q,src), "At-rest drift"
        lost=int(((src[:,:,3]>127)&(q[:,:,3]<25)).sum())
        added=int(((src[:,:,3]<25)&(q[:,:,3]>127)).sum())
        out.append(dict(degrees=angle,lost=lost,new=added))
    return {"type":"low_res_motion_QA_not_approved_art","pivot_source_px":[70,132],"source_size":[215,449],
        "results":out,"release":"blocked_pending_art"}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("cp348_zip")
    a=p.parse_args()
    print(json.dumps(audit(a.cp348_zip),indent=2))

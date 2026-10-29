#!/usr/bin/env python3
"""CP359: verify source-pixel-exact arm split. Not native art / rig acceptance."""
import argparse
import io
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image

def png(raw):
    return np.asarray(Image.open(io.BytesIO(raw)).convert("RGBA"))

def audit(cp348_zip, cp359_ora):
    with zipfile.ZipFile(cp348_zip) as z:
        if z.testzip() is not None:
            raise ValueError("CP348 source ZIP corruption")
        source = png(z.read("FRONT_CP348_TEN_LAYER_RECON_QA_ONLY.png"))
        arm = png(z.read("layers/06_left_arm_and_sleeve.png"))
    with zipfile.ZipFile(cp359_ora) as z:
        if z.testzip() is not None:
            raise ValueError("CP359 ORA ZIP corruption")
        root = ET.fromstring(z.read("stack.xml"))
        layers = root.find("stack").findall("layer")
        if len(layers) != 17:
            raise ValueError("CP359 must contain exactly 17 raster layers")
        entries = [(layer.get("name"), png(z.read(layer.get("src")))) for layer in layers]
        recovered = png(z.read("mergedimage.png"))
    parts = [im.astype("int32") for name,im in entries
             if name.startswith("CP359_0") and name.endswith("_SOURCE_NOT_PAINT")]
    holes = [im for name,im in entries if "HIDDEN" in name and name.endswith("_EMPTY_NOT_PAINT")]
    if len(parts) != 6 or not all(np.any(a[:,:,3] > 0) for a in parts):
        raise ValueError("Expected six nonempty source-only arm parts")
    if len(holes) != 2 or any(np.any(a[:,:,3] != 0) for a in holes):
        raise ValueError("Hidden native underpaint slots must remain truthfully empty")
    if not np.array_equal(np.sum(parts,axis=0),arm.astype("int32")):
        raise ValueError("Arm pixel ownership is not source-exact")
    if not np.array_equal(recovered[:,:,3],source[:,:,3]):
        raise ValueError("Source alpha drift")
    if not np.array_equal(recovered[source[:,:,3]>0],source[source[:,:,3]>0]):
        raise ValueError("Source visible-color drift")
    return {"structural_qa":"PASS","arm_source_parts":6,"ORA_layers":17,
            "native_painted_hidden_layers":0,"runtime_approved":False,
            "production_release":"blocked_pending_art"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cp348-zip",type=Path,required=True)
    p.add_argument("--cp359-ora",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(audit(args.cp348_zip,args.cp359_ora),indent=2))

if __name__=="__main__":
    main()

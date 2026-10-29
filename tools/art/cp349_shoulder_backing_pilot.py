#!/usr/bin/env python3
"""CP349: reproduce a LOW-RES arm backing alpha pilot. Not production art/rig."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

CANON_SHA = "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
CP348_SHA = "f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497"

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_png(data):
    return np.asarray(Image.open(io.BytesIO(data)).convert("RGBA")).copy()

def composite(layers, backing=None, arm_shift=(0, 0)):
    base = Image.new("RGBA", (215, 449))
    if backing is not None:
        base.alpha_composite(Image.fromarray(backing, "RGBA"))
    for i, pix in enumerate(layers):
        layer = Image.fromarray(pix, "RGBA")
        if i == 5 and arm_shift != (0, 0):
            shifted = Image.new("RGBA", layer.size)
            shifted.paste(layer, arm_shift)
            layer = shifted
        base.alpha_composite(layer)
    return np.asarray(base)

def run(cp348_zip, canon, outdir):
    if sha(cp348_zip) != CP348_SHA or sha(canon) != CANON_SHA:
        raise RuntimeError("Locked CANON V2.1 or CP348 SHA mismatch")
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(cp348_zip) as z:
        if z.testzip() is not None:
            raise RuntimeError("Corrupt CP348 archive")
        names = sorted(p for p in z.namelist() if p.startswith("layers/") and p.endswith(".png"))
        layers = [load_png(z.read(p)) for p in names]
        reference = load_png(z.read("FRONT_CP348_TEN_LAYER_RECON_QA_ONLY.png"))
    assert len(layers) == 10 and reference.shape == (449, 215, 4)
    arm = layers[5]
    yy, xx = np.mgrid[0:449, 0:215]
    visible = (arm[:, :, 3] == 255) & (xx >= 54) & (xx < 71) & (yy >= 122) & (yy < 188)
    backing = np.zeros_like(reference)
    ys, xs = np.where(visible)
    for y, x in zip(ys, xs):
        choices = np.flatnonzero(reference[max(0,y-2):min(449,y+3),70:95,3].max(axis=0)>128)
        sx = 70 + int(choices[np.argmin(np.abs((70+choices)-(73+(x-54)*0.23)))]) if len(choices) else 76
        backing[y, x, :3] = reference[y, sx, :3]
        backing[y, x, 3] = 255
    for c in range(3):
        rgb = backing[:, :, c].astype(np.float32)
        weight = visible.astype(np.float32)
        avg = gaussian_filter(rgb, 1.1) / np.maximum(1e-6, gaussian_filter(weight, 1.1))
        backing[:, :, c][visible] = np.uint8(np.clip(0.5*rgb[visible]+0.5*avg[visible],0,255))
    rest = composite(layers, backing)
    assert np.array_equal(rest, reference), "At-rest CANON-derived pixels changed"
    before = composite(layers, arm_shift=(-10, 5))
    after = composite(layers, backing, arm_shift=(-10, 5))
    lost = lambda frame: (reference[:,:,3] > 127) & (frame[:,:,3] < 25)
    a, b = int(lost(before).sum()), int(lost(after).sum())
    assert (a,b) == (914,263), "Unexpected diagnostic baseline"
    report = {
        "checkpoint":"CP349","source":"real CP348 ten-region sprites 215x449",
        "rest_exact_rgba":True, "backing_opaque_pixels":int(visible.sum()),
        "left_arm_shift_xy":[-10,5],"uncovered_before":a,"uncovered_after":b,
        "regained_coverage":a-b,"visual_qa":"FAIL_visible_vertical_smear",
        "semantic_high_resolution_art":False,"rig_ready":False,
        "production_release":"blocked_pending_art",
        "explanation":"Lost alpha coverage is not proof of anatomy. Backing RGB is sampled and stretched; fails visual review."
    }
    Image.fromarray(backing,"RGBA").save(outdir/"CP349_BACKING_EXPERIMENT_NOT_ART.png")
    Image.fromarray(after,"RGBA").save(outdir/"CP349_MOVED_EXPERIMENT_NOT_RIG.png")
    (outdir/"CP349_REPRODUCTION.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))
    return report

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--cp348-zip",required=True)
    p.add_argument("--canon",required=True)
    p.add_argument("--out-dir",required=True)
    a=p.parse_args()
    run(a.cp348_zip,a.canon,a.out_dir)

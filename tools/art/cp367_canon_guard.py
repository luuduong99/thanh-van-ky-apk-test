#!/usr/bin/env python3
"""CP367: Lâm Thiển CANON V2.1-only Front/toe regression guard.

Source provenance + blue shoe checks only. NOT painter acceptance, Spine or APK.
The optional candidate must be aligned to exact source Front (217x458).
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

CANON_SHA = "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
CANON_SIZE = (941, 1672)
FRONT_BBOX = (13, 172, 230, 630)
FRONT_SIZE = (217, 458)
TOES = {
    "image_left_toe": (79, 432, 102, 458),
    "image_right_toe": (109, 414, 122, 446),
}

def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def get_reference(path):
    if file_sha256(path) != CANON_SHA:
        raise ValueError("CANON_SHA_MISMATCH: use exact user-approved reference only")
    with Image.open(path) as img:
        if img.size != CANON_SIZE or img.mode != "RGBA":
            raise ValueError("CANON_FORMAT_MISMATCH")
        return img.crop(FRONT_BBOX).copy()

def blue_mask(part):
    rgb = part[:, :, :3].astype(np.float32)
    return ((rgb[:, :, 2] > rgb[:, :, 0] * 1.14)
            & (rgb[:, :, 2] > rgb[:, :, 1] * 1.09)
            & (rgb[:, :, 2] > 90))

def evaluate(canon, candidate=None):
    ref = np.asarray(get_reference(canon))
    report = {
        "checkpoint": "CP367", "canon_sha256": CANON_SHA,
        "source_verified": True,
        "technical_status": "REFERENCE_CHECK_ONLY",
        "toe_results": {}, "visual_qa": "NOT_PASSED",
        "rig_or_spine_ready": False, "apk_approved": False,
        "production_release": "blocked_pending_art",
        "limitations": [
            "Same-camera aligned Front reference only, not aesthetic approval",
            "Motion underpaint, clothing, alpha draw-order, other views, Android not tested"
        ],
    }
    if candidate is None:
        target = ref
    else:
        with Image.open(candidate) as img:
            if img.size != FRONT_SIZE:
                report["technical_status"] = "REVIEW_ALIGNMENT"
                report["candidate_canvas"] = list(img.size)
                report["issues"] = ["Expected exact 217x458 Front alignment; no inferred scaling"]
                return report
            target = np.asarray(img.convert("RGBA"))
        report["candidate_sha256"] = file_sha256(candidate)

    issues = []
    for name, (x1, y1, x2, y2) in TOES.items():
        src_part = ref[y1:y2, x1:x2]
        out_part = target[y1:y2, x1:x2]
        source_blue = blue_mask(src_part) & (src_part[:, :, 3] >= 128)
        visible_blue = blue_mask(out_part) & (out_part[:, :, 3] >= 128)
        source_count = int(np.count_nonzero(source_blue))
        covered = int(np.count_nonzero(source_blue & visible_blue))
        fraction = covered / max(1, source_count)
        passed = (source_count >= 20 and fraction >= 0.75)
        report["toe_results"][name] = {
            "roi": [x1, y1, x2, y2],
            "reference_blue_pixels": source_count,
            "matched_visible_blue_pixels": covered,
            "coverage_ratio": round(fraction, 4), "pass": passed
        }
        if not passed:
            issues.append(f"{name}: missing blue toe / alpha / color / alignment")
    report["issues"] = issues
    report["technical_status"] = ("TOE_REGRESSION_FOUND" if issues
                                   else "SOURCE_TOE_COLOR_COVERAGE_OK")
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--canon", required=True)
    parser.add_argument("--candidate")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = evaluate(args.canon, args.candidate)
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"technical_status": result["technical_status"],
                      "toe_results": result["toe_results"]}, ensure_ascii=False))
    return 0 if result["technical_status"] == "SOURCE_TOE_COLOR_COVERAGE_OK" else 2

if __name__ == "__main__":
    raise SystemExit(main())

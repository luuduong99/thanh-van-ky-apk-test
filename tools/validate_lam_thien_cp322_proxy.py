#!/usr/bin/env python3
"""QA for CP322 draft alpha sprites. Cannot approve a design or a rig.

No third-party dependencies; supports PNG 8-bit RGBA non-interlaced, filters 0–4.
Returns alpha pixel occupancy based on decoded IDAT, not an inferred filename.
"""
import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path

SIGNATURE = bytes([137, 80, 78, 71, 13, 10, 26, 10])
VIEWS = {"front", "side", "back", "front_3q", "back_3q"}
CANON = "LT_CANON_BODY_REF_2026-10-28_V2"
CANON_SHA = "41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711"


def png_alpha_coverage(path):
    raw = Path(path).read_bytes()
    if raw[:8] != SIGNATURE:
        raise ValueError("Invalid PNG signature")
    offset = 8
    width = height = None
    compressed = bytearray()
    seen_end = False
    while offset + 12 <= len(raw):
        n = struct.unpack_from(">I", raw, offset)[0]
        kind = raw[offset + 4:offset + 8]
        next_offset = offset + 12 + n
        if next_offset > len(raw):
            raise ValueError("Truncated PNG chunk")
        chunk = raw[offset + 8:offset + 8 + n]
        stored_crc = struct.unpack_from(">I", raw, offset + 8 + n)[0]
        if (zlib.crc32(kind + chunk) & 0xFFFFFFFF) != stored_crc:
            raise ValueError("CRC mismatch")
        if kind == b"IHDR":
            if width is not None or n != 13:
                raise ValueError("Duplicate or malformed IHDR")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", chunk)
            if (depth, color, compression, filtering, interlace) != (8, 6, 0, 0, 0):
                raise ValueError("RGBA 8-bit non-interlaced PNG required")
            if width <= 0 or height <= 0 or width * height > 30_000_000:
                raise ValueError("Invalid or unreasonably large PNG")
        elif kind == b"IDAT":
            compressed.extend(chunk)
        elif kind == b"IEND":
            seen_end = True
            break
        offset = next_offset
    if not seen_end or width is None or not compressed:
        raise ValueError("Missing required PNG chunks")
    data = zlib.decompress(compressed)
    rowlength = width * 4
    if len(data) != height * (rowlength + 1):
        raise ValueError("Unexpected decoded PNG size")
    previous = bytearray(rowlength)
    num_opaque = 0
    pos = 0
    for _ in range(height):
        filtering = data[pos]
        pos += 1
        row = bytearray(data[pos:pos + rowlength])
        pos += rowlength
        if filtering not in range(5):
            raise ValueError("Unsupported PNG scanline filter")
        for i in range(rowlength):
            a = row[i - 4] if i >= 4 else 0
            b = previous[i]
            c = previous[i - 4] if i >= 4 else 0
            if filtering == 1:
                row[i] = (row[i] + a) & 255
            elif filtering == 2:
                row[i] = (row[i] + b) & 255
            elif filtering == 3:
                row[i] = (row[i] + ((a + b) // 2)) & 255
            elif filtering == 4:
                p = a + b - c
                da, db, dc = abs(p - a), abs(p - b), abs(p - c)
                paeth = a if da <= db and da <= dc else (b if db <= dc else c)
                row[i] = (row[i] + paeth) & 255
        num_opaque += sum(v > 16 for v in row[3::4])
        previous = row
    return width, height, num_opaque


def audit(folder, strict=False):
    folder = Path(folder)
    errors = []
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("visual_approval") != "NOT_APPROVED" or manifest.get("new_visual_is_not_canon") is not True:
        errors.append("Candidate must remain explicitly NOT_APPROVED")
    if manifest.get("canonical_reference_id") != CANON or manifest.get("canonical_reference_sha256") != CANON_SHA:
        errors.append("Approved canon V2 identity or SHA changed")
    rows = manifest.get("files", [])
    if {r.get("view_id") for r in rows} != VIEWS or len(rows) != 5:
        errors.append("Exactly five draft view IDs required")
    for r in rows:
        basename = r.get("file", "")
        file = folder / basename
        if not basename.endswith("_draft_RGBA_PROXY.png") or file.name != basename or not file.is_file():
            errors.append("Bad proxy filename or missing file: " + basename)
            continue
        if hashlib.sha256(file.read_bytes()).hexdigest() != r.get("sha256"):
            errors.append("SHA mismatch: " + basename)
        try:
            width, height, alpha_pixels = png_alpha_coverage(file)
            if [width, height] != r.get("native_px"):
                errors.append("Native dimension mismatch: " + basename)
            if alpha_pixels != r.get("alpha_occupied_pixels"):
                errors.append("Alpha occupancy mismatch: " + basename)
            if not (0 < alpha_pixels < width * height):
                errors.append("Proxy should include both opaque and transparent pixels: " + basename)
            if abs(alpha_pixels * 100 / (width * height) - r.get("alpha_coverage_pct", -1)) > 0.02:
                errors.append("Alpha percentage mismatch: " + basename)
        except (OSError, ValueError, zlib.error) as exc:
            errors.append("Unreadable RGBA proxy " + basename + ": " + str(exc))
    if strict:
        errors.append("CP322 candidate is NOT APPROVED; never pass the production gate")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    errors = audit(args.folder, args.strict)
    print(json.dumps({"passed": not errors, "production_ready": False, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
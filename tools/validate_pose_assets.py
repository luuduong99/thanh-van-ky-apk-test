#!/usr/bin/env python3
"""Validate TVK pose images and touch-zone registrations before building Android.

Only checks file existence, dimensions, ids and coordinate ranges. Does not
certify artwork, anatomy, interactive usability or Spine/Live2D rig playback.
"""
from __future__ import annotations
import json
import struct
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
CATALOGUE = ASSETS / "character_interactions.json"


def fail(message: str):
    raise SystemExit("TVK pose validation failed: " + message)


def asset_path(value: str) -> Path:
    if not value or not value.startswith("characters/"):
        fail("Unexpected pose art path: " + repr(value))
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "\\" in value:
        fail("Unsafe pose path: " + value)
    return ASSETS.joinpath(*p.parts)


def png_dimensions(path: Path) -> tuple[int, int]:
    if not path.is_file():
        fail("Missing image: " + str(path.relative_to(ROOT)))
    with path.open("rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        fail("Not a PNG: " + str(path.relative_to(ROOT)))
    width, height = struct.unpack(">II", header[16:24])
    if min(width, height) < 96:
        fail("Image too small: " + str(path.relative_to(ROOT)))
    return width, height


def main():
    data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    if data.get("version", 0) < 6:
        fail("Outdated pose manifest")
    characters = data.get("characters", [])
    found = set()
    count = 0
    for ch in characters:
        cid = ch["id"]
        if cid in found:
            fail("Repeated character " + cid)
        found.add(cid)
        poses = ch.get("poses", [])
        pose_ids = set()
        for pose in poses:
            pid = pose["id"]
            if pid in pose_ids:
                fail("Duplicate pose " + cid + "/" + pid)
            pose_ids.add(pid)
            img_path = asset_path(pose["image"])
            dims = png_dimensions(img_path)
            count += 1
            print(f"OK {cid}/{pid}: {img_path.relative_to(ROOT)}, {dims[0]}x{dims[1]}")
        if not {"front", "back", "bed_kneel_forward", "bed_recline"}.issubset(pose_ids):
            fail("Missing required pose for " + cid)

        zone_count = {}
        for zone in ch.get("touchZones", []):
            pid = zone["pose"]
            if pid not in pose_ids:
                fail("Orphan touch pose " + cid + "/" + pid)
            zone_count[pid] = zone_count.get(pid, 0) + 1
            if not isinstance(zone.get("requiresConsent"), bool):
                fail("Invalid consent flag on " + cid + "/" + zone.get("id", ""))
            for region in zone.get("regions", []):
                values = [region.get(k) for k in ("x1", "y1", "x2", "y2")]
                if any(not isinstance(v, (int, float)) or not (0 <= v <= 1) for v in values):
                    fail("Invalid touch bounds for " + cid + "/" + zone.get("id", ""))
                if not (values[0] < values[2] and values[1] < values[3]):
                    fail("Inverted touch rectangle for " + cid + "/" + zone.get("id", ""))
        for required in ("bed_kneel_forward", "bed_recline"):
            if zone_count.get(required, 0) < 4:
                fail(f"Missing calibrated regions in {cid}/{required}")
        outfits = {o["id"]: o for o in ch.get("wardrobeStates", [])}
        if "default" not in outfits:
            fail("No default outfit for " + cid)
        for pose in poses:
            path = outfits["default"].get("images", {}).get(pose["id"])
            if path != pose["image"]:
                fail("Default outfit doesn't match current pose for " + cid + "/" + pose["id"])
    if not {"to_nguyet_ly", "lin_qian"}.issubset(found):
        fail("Expected two opening heroines")
    print(f"Validated {count} PNG pose assets across {len(found)} characters.")


if __name__ == "__main__":
    main()

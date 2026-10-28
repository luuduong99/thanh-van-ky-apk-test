#!/usr/bin/env python3
"""CP320: verify approved sources and audit full-body view/pose calibration.

This validator never creates art, guesses coordinates, or marks rig readiness.
Default checks the manifest contract; --strict also gates art readiness.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs/art/LAM_THIEN_CP320_VIEW_CALIBRATION.json"
REQUIRED_VIEWS = {"front", "back", "side", "front_three_quarter", "back_three_quarter", "back_turn"}
REQUIRED_POSES = {"bed_side_lying", "bed_sit", "chair_sit", "wall_lean", "bed_recline", "bed_kneel_forward"}
REQUIRED_LEVELS = [100, 70, 50, 30]
EXPECTED_LANDMARKS = ["head_top", "chin", "shoulder_center", "waist_center", "hip_center", "knee_center", "ankle_center"]


def verify_png(path, expected_sha=None, expected_dimensions=None):
    """Check actual PNG bytes, dimensions and optional approved checksum."""
    path = Path(path)
    if not path.is_file():
        return [f"Missing PNG: {path}"]
    raw = path.read_bytes()
    errors = []
    if len(raw) < 24 or raw[:8] != b"\\x89PNG\\r\\n\\x1a\\n" or raw[12:16] != b"IHDR":
        return [f"Not a valid PNG header: {path}"]
    width, height = struct.unpack(">II", raw[16:24])
    if expected_dimensions and [width, height] != list(expected_dimensions):
        errors.append(f"Wrong dimensions: {path} ({width}x{height})")
    if expected_sha and hashlib.sha256(raw).hexdigest() != expected_sha:
        errors.append(f"SHA256 mismatch (source must not be changed): {path}")
    return errors


def validate_manifest(data, strict=False):
    errors, pending = [], []
    if data.get("schema_version") != 1 or data.get("character_id") != "lin_qian":
        errors.append("Expected CP320 manifest schema 1 for lin_qian")
    canon = data.get("canon", {})
    if canon.get("reference_id") != "LT_CANON_BODY_REF_2026-10-28_V2":
        errors.append("Wrong canon model; must use approved V2")
    if canon.get("historical_plus_17_already_included") is not True:
        errors.append("Do not apply +17% again to V2")
    if data.get("approved_damage", {}).get("levels") != REQUIRED_LEVELS:
        errors.append("Damage levels must match approved 100/70/50/30")
    landmarks = data.get("coordinate_system", {}).get("landmark_names")
    if landmarks != EXPECTED_LANDMARKS:
        errors.append("Incorrect or reordered rig landmarks")

    def check_records(key, required):
        records = data.get(key, [])
        ids = [r.get("id") for r in records]
        if len(set(ids)) != len(ids) or not required.issubset(ids):
            errors.append(f"{key}: missing/duplicate entries")
        for r in records:
            rid = r.get("id", "<unknown>")
            pts = r.get("landmarks_normalized")
            if pts is None:
                pending.append(f"{key}/{rid}: landmark measurements not supplied")
            elif not isinstance(pts, dict) or set(pts) != set(EXPECTED_LANDMARKS):
                errors.append(f"{key}/{rid}: must have exactly seven named landmark coordinates")
            else:
                for name, xy in pts.items():
                    if (not isinstance(xy, list) or len(xy) != 2
                        or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 1 for v in xy)):
                        errors.append(f"{key}/{rid}/{name}: expected normalized [x,y] values in [0,1]")
            art = r.get("asset_path")
            layered = r.get("layered_asset_path")
            if not art or not layered:
                pending.append(f"{key}/{rid}: source or layered art missing")
            elif art == layered:
                errors.append(f"{key}/{rid}: flattened source cannot count as layered art")
            if r.get("review_status") != "approved":
                pending.append(f"{key}/{rid}: preview not approved")
    check_records("views", REQUIRED_VIEWS)
    check_records("additional_poses", REQUIRED_POSES)
    layer = data.get("layer_contract", {})
    if len(set(layer.get("required", []))) != len(layer.get("required", [])) or len(layer.get("required", [])) < 12:
        errors.append("Layer contract incomplete")
    if layer.get("status") != "verified":
        pending.append("Actual layered PNG/ORA and alpha/seam QA not verified")
    if strict and pending:
        errors.extend(pending)
    return errors, pending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--canon", type=Path, help="Exact V2 PNG bytes, if locally available")
    parser.add_argument("--damage", type=Path, help="Exact approved four-level PNG")
    parser.add_argument("--strict", action="store_true", help="Require completed art and review (expected to fail before production)")
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors, pending = validate_manifest(data, strict=args.strict)
    if args.canon:
        c = data["canon"]
        errors += verify_png(args.canon, c["sha256"], [c["width"], c["height"]])
    if args.damage:
        errors += verify_png(args.damage, data["approved_damage"]["sha256"], [1672, 941])
    print(json.dumps({"checkpoint": "CP320", "passed": not errors, "errors": errors, "pending_count": len(pending), "pending": pending}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

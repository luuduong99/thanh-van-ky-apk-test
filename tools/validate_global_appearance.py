#!/usr/bin/env python3
"""Validate the shared outfit/damage/pose contract for every TVK character.

This validates declarations and missing-asset behavior only; it never claims art,
Spine animation or an APK build is complete.
"""
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "app/src/main/assets/character_interactions.json"
ASSETS = ROOT / "app/src/main/assets"
INTEGRITY = ("100", "70", "50", "30")
REQUIRED_PLANNED = {
    "side", "front_three_quarter", "back_three_quarter", "back_turn",
    "bed_side_lying", "bed_sit", "chair_sit", "wall_lean"
}


def check_path(value):
    if not isinstance(value, str) or not value.startswith("characters/"):
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and ".." not in p.parts and "\\" not in value and p.suffix == ".png"


def validate(data, assets_root=ASSETS):
    errors = []
    sys = data.get("appearanceSystem", {})
    if sys.get("scope") != "all_current_and_future_characters":
        errors.append("Appearance system must be global")
    if sys.get("poseChangePolicy") != "preserve_wardrobe_and_integrity_for_all_levels":
        errors.append("All wardrobe levels must survive pose changes")
    if sys.get("missingArtPolicy") != "show_missing_asset_without_reverting_to_default":
        errors.append("Missing art may not fallback to default")
    if sys.get("integrityLevels") != [100, 70, 50, 30]:
        errors.append("Integrity levels must be 100/70/50/30")
    if set(sys.get("stateKeys", [])) != {"wardrobe", "integrity", "pose", "expression", "action"}:
        errors.append("Appearance state keys incomplete")
    ids = set()
    for ch in data.get("characters", []):
        cid = ch.get("id", "")
        if cid in ids or not re.fullmatch("[a-z0-9_]{1,64}", cid):
            errors.append("Duplicate or invalid character ID: " + cid)
        ids.add(cid)
        poses = ch.get("poses", [])
        active = {p.get("id") for p in poses}
        if None in active or len(active) != len(poses):
            errors.append(cid + ": active pose ids missing/duplicated")
        planned = ch.get("plannedPoses", [])
        planned_ids = {p.get("id") for p in planned}
        if (active & planned_ids) or len(planned_ids) != len(planned) or not REQUIRED_PLANNED.issubset(active | planned_ids):
            errors.append(cid + ": planned pose matrix incomplete or overlapping")
        for p in planned:
            if p.get("status") != "asset_required" or not check_path(p.get("artworkPath")):
                errors.append(cid + ": invalid planned pose metadata")
        wardrobes = ch.get("wardrobeStates", [])
        states = {w.get("id") for w in wardrobes}
        if len(states) != len(wardrobes) or not {"default", "outer_removed", "private_fantasy"}.issubset(states):
            errors.append(cid + ": missing or duplicate wardrobe states")
        for w in wardrobes:
            wid = w.get("id", "")
            if w.get("appearancePersistence") != "character_scoped_all_poses":
                errors.append(cid + "/" + wid + ": wardrobe not persistent")
            for p in poses:
                name = w.get("images", {}).get(p.get("id", ""))
                if not check_path(name):
                    errors.append(cid + "/" + wid + ": invalid base image for " + str(p.get("id")))
                if wid == "default" and name != p.get("image"):
                    errors.append(cid + ": default art disagrees with pose")
            damage = w.get("integrityImages", {})
            if not all(key in damage for key in INTEGRITY[1:]):
                errors.append(cid + "/" + wid + ": missing damage level registration")
            for level in INTEGRITY[1:]:
                for p in poses:
                    name = damage.get(level, {}).get(p.get("id", ""))
                    if not check_path(name):
                        errors.append(cid + "/" + wid + ": invalid damage art for " + level + "/" + str(p.get("id")))
                    elif assets_root and (assets_root / name).is_file() and w.get("status") == "asset_required":
                        # A file could have been added; status must still be reviewed manually.
                        pass
    if not ids:
        errors.append("No characters registered")
    return errors


def main():
    errors = validate(json.loads(CATALOGUE.read_text(encoding="utf-8")))
    if errors:
        print("GLOBAL APPEARANCE INVALID:\n" + "\n".join("- " + e for e in errors))
        raise SystemExit(1)
    print("GLOBAL APPEARANCE VALID: all characters have persistent wardrobe/damage/pose contracts; artwork readiness is separate")


if __name__ == "__main__":
    main()

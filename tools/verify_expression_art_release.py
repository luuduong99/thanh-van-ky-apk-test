#!/usr/bin/env python3
"""Fail closed for unapproved face sprites before an Android game release.

CP335: source artwork approval and actual game-asset approval are different.
The current Lâm Thiển reference is user-approved, but the five independent
production facial sprites are NOT. Until those assets exist and have an
art-review manifest, no sprite path may be registered in Android.

This script validates a synthetic release in tests, but passing tests on fake
fixtures says nothing about the visual quality of real art. Human art review is
still mandatory; strict file checks do not replace artist QA or Android APK QA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from PIL import Image

SHA = re.compile(r"[0-9a-f]{64}\Z")
ID = re.compile(r"[a-z0-9_]{1,64}\Z")
REL = re.compile(r"characters/[a-z0-9_]{1,64}/[A-Za-z0-9_./-]+\.png\Z")
APPROVAL_FIELDS = ("artist_qa_passed", "runtime_qa_passed")
CANON_ID = "LT_CANON_BODY_REF_2026-10-28_V2"
EXPRESSION_ID = "LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED"
EXPECTED = ("shy", "angry", "pain", "embarrassed", "alluring")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def flatten_sprites(mapping: object, character: str) -> tuple[dict[str, str], list[str]]:
    """Get expression|wardrobe|integrity|pose -> file; reject malformed keys."""
    result: dict[str, str] = {}
    errors: list[str] = []
    if not isinstance(mapping, dict):
        return {}, [f"{character}: sprite_paths must be a JSON object"]
    for expression, wardrobes in mapping.items():
        if not ID.fullmatch(expression) or not isinstance(wardrobes, dict):
            errors.append(f"{character}: malformed expression key {expression!r}")
            continue
        for wardrobe, steps in wardrobes.items():
            if not ID.fullmatch(wardrobe) or not isinstance(steps, dict):
                errors.append(f"{character}: invalid wardrobe for {expression}")
                continue
            for integrity, poses in steps.items():
                if integrity not in ("100", "70", "50", "30") or not isinstance(poses, dict):
                    errors.append(f"{character}: unsupported integrity {integrity!r}")
                    continue
                for pose, path in poses.items():
                    key = "|".join((expression, wardrobe, integrity, pose))
                    if not ID.fullmatch(pose) or not isinstance(path, str):
                        errors.append(f"{character}: invalid pose/path in {key}")
                    else:
                        result[key] = path
    return result, errors


def _safe_asset_path(path: str, character_id: str) -> bool:
    return (bool(REL.fullmatch(path)) and ".." not in path and "\\" not in path
            and path.startswith(f"characters/{character_id}/"))


def validate(root: Path, *, profile_file: Path | None = None) -> list[str]:
    root = root.resolve()
    asset_base = (root / "app/src/main/assets").resolve()
    profile_file = profile_file or asset_base / "character_expression_profiles.json"
    errors: list[str] = []
    profile = json.loads(profile_file.read_text(encoding="utf-8"))
    if profile.get("schema_version") != 1:
        errors.append("invalid character_expression_profiles schema_version")
    for character in profile.get("characters", []):
        name = character.get("id", "")
        if not isinstance(name, str) or not ID.fullmatch(name):
            errors.append("invalid character id")
            continue
        paths, parse_errors = flatten_sprites(character.get("sprite_paths", {}), name)
        errors.extend(parse_errors)
        release = character.get("production_release")
        status = release.get("status") if isinstance(release, dict) else None
        if status != "approved_for_runtime":
            # Critical: any orphan sprite paths, even if they do not exist yet,
            # represent unsafe release of art not individually accepted.
            if paths:
                errors.append(f"{name}: sprite_paths exist without production approval")
            if isinstance(release, dict) and status != "blocked_pending_art":
                errors.append(f"{name}: invalid pending release status {status!r}")
            continue

        if character.get("approval_status") != "explicit_user_approved_expression_preview":
            errors.append(f"{name}: expression direction is not approved")
        if not paths:
            errors.append(f"{name}: production release has no sprite paths")
        if name == "lin_qian":
            if character.get("canonical_body_visual_id") != CANON_ID:
                errors.append("lin_qian: wrong body canon")
            if character.get("approved_profile_id") != EXPRESSION_ID:
                errors.append("lin_qian: wrong expression reference")
            ids = tuple(e.get("id") for e in character.get("approved_expressions", []))
            if ids != EXPECTED:
                errors.append("lin_qian: five expression IDs differ from approved order")
        for field in APPROVAL_FIELDS:
            if release.get(field) is not True:
                errors.append(f"{name}: {field} must be true for released art")
        if not release.get("user_asset_approval_id"):
            errors.append(f"{name}: missing explicit user art acceptance ID")
        if (release.get("canonical_body_visual_id") != character.get("canonical_body_visual_id")
            or release.get("canonical_body_sha256") != character.get("canonical_body_sha256")
            or release.get("approved_expression_profile_id") != character.get("approved_profile_id")
            or release.get("approved_expression_sha256") != character.get("expression_preview_sha256")):
            errors.append(f"{name}: production release source references differ")
        manifest_path = release.get("sprite_manifest_path")
        manifest_digest = release.get("sprite_manifest_sha256")
        if not isinstance(manifest_path, str) or not manifest_path.startswith(f"characters/{name}/") \
                or ".." in manifest_path or not manifest_path.endswith(".json"):
            errors.append(f"{name}: unsafe or missing sprite manifest path")
        else:
            full = (asset_base / manifest_path).resolve()
            if not full.is_relative_to(asset_base) or not full.is_file():
                errors.append(f"{name}: sprite manifest file missing")
            elif not isinstance(manifest_digest, str) or not SHA.fullmatch(manifest_digest) \
                    or sha256_file(full) != manifest_digest:
                errors.append(f"{name}: manifest SHA256 mismatch")
            else:
                art_manifest = json.loads(full.read_text(encoding="utf-8"))
                if art_manifest.get("status") != "artist_and_user_accepted":
                    errors.append(f"{name}: art manifest is not accepted")
                if art_manifest.get("canonical_body_visual_id") != character.get("canonical_body_visual_id"):
                    errors.append(f"{name}: art manifest wrong canon")
        allowed_hashes = release.get("approved_sprite_hashes")
        if not isinstance(allowed_hashes, dict):
            errors.append(f"{name}: no per-file SHA256 approval map")
            allowed_hashes = {}
        if set(paths.values()) != set(allowed_hashes):
            errors.append(f"{name}: approved sprite list differs from actual declared paths")
        if len(paths) != len(set(paths.values())):
            errors.append(f"{name}: one PNG reused for multiple face/outfit/pose states")
        for key, path in paths.items():
            if not _safe_asset_path(path, name):
                errors.append(f"{name}: unsafe sprite path {key}")
                continue
            full = (asset_base / path).resolve()
            if not full.is_relative_to(asset_base) or not full.is_file():
                errors.append(f"{name}: missing sprite file {path}")
                continue
            expected = allowed_hashes.get(path)
            if not isinstance(expected, str) or not SHA.fullmatch(expected) or sha256_file(full) != expected:
                errors.append(f"{name}: SHA256 mismatch {path}")
                continue
            with Image.open(full) as im:
                if im.format != "PNG" or im.mode != "RGBA":
                    errors.append(f"{name}: sprite must be RGBA PNG {path}")
                    continue
                if min(im.size) < 512:
                    errors.append(f"{name}: sprite has insufficient native pixels {path}")
                extrema = im.getchannel("A").getextrema()
                if extrema is None or extrema[1] == 0 or extrema[0] == 255:
                    errors.append(f"{name}: sprite must have meaningful alpha {path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = validate(args.repo)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        print("CP335 FACE ASSET RELEASE: BLOCKED")
        for error in errors:
            print(" -", error)
        return 1
    print("CP335 FACE ASSET RELEASE: VALID (pending art is safely withheld)")
    print("This does not establish visual fidelity, Spine rig success, or APK testing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
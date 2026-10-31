#!/usr/bin/env python3
"""Validate approved character art reference and production status separation."""
import argparse
import json
import re
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[2] / "docs/art/LAM_THIEN_DESIGN_REGISTRY.json"


def validate(data):
    errors = []
    approved = data.get("latest_user_approved_design") or {}
    candidate = data.get("latest_pending_preview")
    impl = data.get("implementation") or {}
    if not approved.get("id") or not approved.get("approved_on"):
        errors.append("Missing confirmed current design id/date")
    if not approved.get("required_traits"):
        errors.append("Missing required visual traits")
    if not approved.get("visual_reference_location"):
        errors.append("Missing verified approved visual source URL")
    checksum = approved.get("visual_reference_sha256", "")
    if not re.fullmatch(r"[0-9a-f]{64}", checksum):
        errors.append("Missing or invalid approved image SHA-256")
    dims = approved.get("visual_reference_dimensions")
    if not isinstance(dims, list) or len(dims) != 2 or any(not isinstance(x, int) or x <= 0 for x in dims):
        errors.append("Missing or invalid approved reference dimensions")
    if candidate is not None:
        if not isinstance(candidate, dict) or candidate.get("approval_status") not in ("pending", "approved", "rejected"):
            errors.append("Invalid candidate approval status")
        elif candidate.get("approval_status") == "pending" and candidate.get("id") == impl.get("design_reference_id"):
            errors.append("Pending preview cannot become production design reference")
    referenced = impl.get("design_reference_id")
    if referenced and referenced != approved.get("id"):
        errors.append("Production design reference must point at latest approved design")
    if referenced and any(s in referenced.lower() for s in ("proxy", "cp317", "deprecated", "reconstruction")):
        errors.append("Deprecated source cannot become production reference")
    if any(impl.get(k) is True for k in ("sprite_layers_complete", "spine_rig_complete", "physics_approved", "apk_integrated")):
        if not referenced:
            errors.append("Production milestone claimed without approved design reference")
        if not approved.get("visual_reference_location"):
            errors.append("Production milestone claimed before approved visual asset is available")
    if impl.get("apk_integrated") and not impl.get("spine_rig_complete"):
        errors.append("Cannot claim APK integration without rig complete")
    if impl.get("physics_approved") and not impl.get("spine_rig_complete"):
        errors.append("Cannot claim physics approved without rig complete")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", nargs="?", type=Path, default=DEFAULT)
    args = parser.parse_args()
    errors = validate(json.loads(args.registry.read_text(encoding="utf8")))
    if errors:
        print("DESIGN REGISTRY INVALID:\n" + "\n".join("- " + e for e in errors))
        return 1
    print("DESIGN REGISTRY VALID: current approved visual reference and implementation stages are separate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

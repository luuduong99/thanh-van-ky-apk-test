#!/usr/bin/env python3
"""Verify Lam Thien's approved expressions stay distinct from her body canon.

This checks approval metadata (not graphic pixels or completion of sprites/rig/APK).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "docs" / "art"
CANON_ID = "LT_CANON_BODY_REF_2026-10-28_V2"
ACTIVE_CANON_ID = "LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29"
ACTIVE_CANON_SHA = "f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a"
EXPRESSION_ID = "LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED"
EXPRESSION_SHA = "ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7"
CANON_SHA = "41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711"
EMOTIONS = ("shy", "angry", "pain", "embarrassed", "alluring")
FILES = {
    "approved": "LAM_THIEN_FIVE_EXPRESSIONS_APPROVED_2026_10_29.json",
    "registry": "LAM_THIEN_DESIGN_REGISTRY.json",
    "model": "LAM_THIEN_MODEL_CARD_V2.json",
    "global": "GLOBAL_CHARACTER_EXPRESSION_STANDARD_2026_10_29.json",
}


def load_contracts(root=ART):
    return {key: json.loads((Path(root) / name).read_text(encoding="utf-8"))
            for key, name in FILES.items()}


def validate(approved, registry, model, global_standard):
    errors = []
    eids = [e.get("id") for e in approved.get("approved_expressions", [])]
    gids = global_standard.get("emotion_ids", [])
    if eids != list(EMOTIONS) or gids != list(EMOTIONS) or len(set(eids)) != 5:
        errors.append("All five approved emotions must be present in stable order and unique")
    if (approved.get("expression_profile_id") != EXPRESSION_ID or
        approved.get("approval_status") != "explicit_user_approved_expression_preview"):
        errors.append("Lam Thien expression approval is missing or replaced by an unapproved review")
    if approved.get("canonical_body_visual_id") != CANON_ID:
        errors.append("The expression guide cannot replace the approved body V2")
    source = approved.get("source", {})
    if source.get("sha256") != EXPRESSION_SHA:
        errors.append("Wrong approved 5-expression preview SHA256")
    if "Approved References/Lam_Thien_Expressions_20261029" not in source.get("library_path", ""):
        errors.append("Approved expression art must point to its archived approved reference")
    if source.get("source_kind") != "flat_approved_expression_reference_not_layered_asset":
        errors.append("An approved concept is not a production sprite")
    base = next((x for x in registry.get("archived_approved_designs", []) if x.get("id") == "LT_CANON_BODY_REF_2026-10-28_V2"), {})
    active = registry.get("latest_user_approved_design", {})
    if (active.get("id") != ACTIVE_CANON_ID or active.get("visual_reference_sha256") != ACTIVE_CANON_SHA):
        errors.append("The latest approved character model V2.1 must remain the active body canon")
    profile = registry.get("approved_expression_profile", {})
    if base.get("id") != CANON_ID or base.get("visual_reference_sha256") != CANON_SHA:
        errors.append("The historical character model V2 archive must be preserved")
    if (profile.get("id") != EXPRESSION_ID or
        profile.get("source_sha256") != EXPRESSION_SHA or
        profile.get("expression_ids") != list(EMOTIONS)):
        errors.append("Design registry expression approval does not match the approved spec")
    if (model.get("canonical_visual_id") != CANON_ID or
        model.get("source", {}).get("sha256") != CANON_SHA or
        model.get("approved_expression_profile_id") != EXPRESSION_ID or
        model.get("approved_expression_reference_sha256") != EXPRESSION_SHA):
        errors.append("Model card V2 disagrees with the approved expression profile")
    if (global_standard.get("approval_status") != "approved_global_expression_direction" or
        global_standard.get("per_character_requirements", {}).get("requires_individual_preview_approval") is not True or
        global_standard.get("per_character_requirements", {}).get("no_copying_lam_thien_face_or_body") is not True):
        errors.append("Global standard must require individualized facial art and separate review")
    examples = global_standard.get("examples", {})
    if (examples.get("lin_qian", {}).get("approved_expression_profile") != EXPRESSION_ID or
        examples.get("to_nguyet_ly", {}).get("approved_expression_profile") is not None):
        errors.append("Do not accidentally pre-approve another character's expression art")
    if (approved.get("art_qa", {}).get("approved_visual_direction") is not True or
        approved.get("source", {}).get("mode") != "RGB"):
        errors.append("Approved expression preview metadata inconsistent")
    return errors


def main():
    try:
        data = load_contracts()
        errors = validate(data["approved"], data["registry"], data["model"], data["global"])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        print("EXPRESSION APPROVAL CONTRACT FAILED:")
        for error in errors:
            print(" - " + error)
        raise SystemExit(1)
    print("EXPRESSION APPROVAL CONTRACT OK — 5 approved Lam Thien expressions, body V2 unchanged.")
    print("This does NOT certify layered sprites, Spine animation, other characters, or APK.")


if __name__ == "__main__":
    main()

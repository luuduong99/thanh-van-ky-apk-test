# CP368 — Lâm Thiển: CANON-locked localized left-sleeve refinement (2026-10-29)

**Status:** 6 SVG/PNG layers refined and tested; **VISUAL QA NOT PASSED**, not independent full-body game art, no Spine rig or APK release.

## Source of truth / image policy
- Exact approved CANON V2.1 uploaded by user: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Precise Front crop `(13,172,230,630)` (217×458); SVG workspace 1302×2748 from this geometry. Workspace scale is not native source detail enhancement.
- Preview only uses the actual character's user-approved CANON crop, older CP366 derived study and **CP368 DRAFT explicitly labeled NOT APPROVED**. Never display unrelated character art to represent CANON.

## Actual new art and QA
- Rebuilt **six independent edited SVG art layers**: rear silver/lavender hair, hidden bodice cloth, hidden shoulder skin, arm/hand, translucent sleeve silk, gold shoulder/wrist ornaments. Feathered drape folds, thinner flowing strands, more organic gold filigree.
- Real `CP368_REFINED_SIX_LAYER_SLEEVE_DRAFT_NOT_SPINE.ora` with six visible editable raster layers and one **hidden** CANON reference. Transparent merge PNG and technical 0/-8/-15 degree motion samples.
- Technical shoulder overlap pixels at 0/-8/-15/+8 degrees: **20,416 / 19,199 / 18,105 / 21,708**. Nonzero overlap is **not proof** of gap-free rigging/skin underpaint or accurate artist-painted keyframes.
- Exact source SHA gate and wrong-source rejection, valid SVG independent parts, ORA ZIP CRC/layer visibility, preview and blocked release status. **6/6 local regression tests PASS** with private CANON and ORA. GitHub test runner without private art will skip art-dependent checks, not falsely claim a passed visual check.
- Handoff archive: `TVK_CP368_LamThien_RefinedSleeve_NOT_APPROVED.zip`, **25 entries**, SHA256 `2a8ab1c8a5b22eac5a265ebfe07bcde592de501c9b98014aaa6c957f618009b8`. ORA SHA256 `0f9841ec802e77712c7819d1aad60d1465cb18103045ef07dc0314cf6091bb53`. Stored in Library `/Thanh Van Ky/Development/CP368_Refined_Sleeve_Study/`.
- Reproducible code: `tools/art/cp368_refine_sleeve.py`; tests: `tests/art/test_cp368_refine_sleeve.py` (requires `cp366_build_vector_sleeve.py` and Pillow/NumPy/CairoSVG).

## Remaining acceptance blockers
- **Visual mismatch** remains in silk folds, underpaint, ornaments and hair compared to painting in approved CANON. No artist approval; don't replace CANON with this study.
- Right sleeve, head/face, full bodice/body, legs and **both blue shoe tips** have not been repainted as production semantically separated sprites.
- No true painter-authored raised arm keyframe. Group rotate is only a QA sample. No trustworthy FPS/device result.
- Keep `production_release.status=blocked_pending_art`, `sprite_paths={}`, `rig_ready=false`, `apk_ready=false`.

## CP369 next
1. Refine visible parts/underpaint by hand to match **the exact user-approved CANON V2.1** and compare at a consistent camera.
2. Extend genuine high-resolution painted semantic body/front layers (face, arm right, bodice, legs/shoes and underpaint), while retaining shoe blue toe colors and +17% proportions.
3. Draw rest and arm-raised keyframes with actual garment fold changes; review visually with user **before** Spine, combat runtime, and Android APK.

# TVK CP373 — Lâm Thiển / Full-body Front source-region guide

**Date:** 2026-10-30. **Status: technical SOURCE GUIDE only — NOT APPROVED ART, NOT RIG OR APK.**

## CANON authority and strict image rule

- The only authoritative source is the exact user-approved `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, **941×1672 RGBA**, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- New pictures show ONLY this source sheet, pixel-exact crops of the same sheet and clearly labeled source-derived technical previews. Never use different characters, internet images, old references, or unapproved drafts as CANON.
- +17% proportions and all character details are preserved as *reference*. The cropped Front is only **217×458 native source pixels**, not 4K artwork. Enlargements used for inspection DO NOT add new details.

## What was actually produced

- Actual Front source crop `BBOX=(13,172,230,630)`, RGB preserved without repainting.
- Draft alpha matte of complete visible Front using GrabCut plus blue/lavender edge recovery. **This matte is imperfect**: pale ribbon edges and remaining floor shadow require human refinement. Do not import it into the game or claim alpha clean.
- 19 independently editable **source-pixel region** PNGs, 19 grayscale masks, one editable foreground mask, one ORA with 19 visible source-region layers and **one hidden CANON Front reference**. These are approximate routing polygons, *not* true anatomical/silk/skin/occluded painted layers.
- Recomposition of 19 layers is pixel-exact to the *working experimental matte* at rest, not pixel-equal to the opaque background of the original CANON.
- Preview includes only exact CANON, Front source crop, matte QA and color-coded region study.
- Proof of both blue shoe-tip regions: image-left 163/163 pixel retention, image-right 146/146; this checks reference pixels only, not runtime rendering.
- Motion gap diagnostic: shifting one hand `(-6,+3)` yields **204 uncovered alpha pixels** because no hidden anatomy/underpaint was painted. This is an explicit **FAIL for rig readiness**.
- **10/10 local tests PASS** for CANON authentication, source extraction and color preservation, matte/region reassembly, ORA CRC/stack, shoe-tip preservation, expected missing underpaint and a release gate that stays blocked. Passing these tests is NOT visual art approval.

## Files

- `cp373_fullbody_source_guide.py` — deterministic generation, Python 3 with Pillow, NumPy, OpenCV.
- `test_cp373_fullbody_source_guide.py` — unit tests; source-dependent tests skip without private CANON bytes.
- `OUTPUT/source/FRONT_EXACT_CROP_WITH_BACKGROUND.png` — true unscaled source reference.
- `OUTPUT/source/FRONT_MATTE_DRAFT_NOT_ART.png` — experimental transparent full body.
- `OUTPUT/masks/` — editable source region masks, `OUTPUT/layers/` — source-pixel layer PNGs.
- `OUTPUT/ora/CP373_FRONT_19_SOURCE_REGION_GUIDES_NOT_RIG.ora` — editable OpenRaster reference study.
- `OUTPUT/qa/CP373_CANON_FRONT_MATTE_19REGION_COMPARISON.png` — CANON-only comparison.
- `OUTPUT/CP373_REPORT.json`, `OUTPUT/SOURCE_ROLE_MANIFEST.json`, `CP373_TEST_LOG.txt`.

## Release blockers / CP374 next

1. Manual correction of pale edges and removal of the floor shadow from matte; user approves preview before replacing references.
2. **Independent artist-created high resolution whole-body art**, rather than simply upscaling/splitting the original 217×458 crop. The visual styling must match user-approved CANON V2.1 exactly.
3. Explicit hidden body/skin, cloth and hair underpaint under moving sections, draw-order and alpha proof against multiple hand/cloth poses.
4. Body, face/expression, arms, lower garment, both legs and **two blue shoe toes** as actual painted semantic layers; later create 5 expressions and four clothing-integrity states 100/70/50/30.
5. Only after production art acceptance: implement/test 2D rig/Spine or equivalent, integrate into Android gameplay, build and test APK.

**Mandatory flags:** `visual_qa=NOT_PASSED`, `production_release=blocked_pending_art`, `sprite_paths={}`, `native_painted_full_body=false`, `rig_spine_ready=false`, `apk_ready=false`.
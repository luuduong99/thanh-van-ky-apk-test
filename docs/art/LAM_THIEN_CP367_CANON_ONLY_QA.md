# CP367 — CANON-only source and shoe-tip regression QA (2026-10-29)

**CANON reference:** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. This is the exact user-approved Lâm Thiển image, unchanged. Not a new art design.

## Actual completed work
- Source-locked audit of Front crop `(13,172,230,630)` (217×458).
- Blue shoe toe image-left: **163/163 source blue pixels visible**, image-right: **146/146 visible**. These are reference pixels, not evidence of runtime sprite rendering.
- Regression test: deliberately transparentizing left or right blue toe triggers `TOE_REGRESSION_FOUND`; misaligned 215×449 candidate triggers `REVIEW_ALIGNMENT` instead of a false PASS. Wrong CANON SHA is rejected.
- **6/6 local tests PASS** on exact uploaded CANON; technical QA image contains only the exact source sheet and crops/nearest-neighbor enlargements from it. The local handoff ZIP is `TVK_CP367_CANON_QA_HANDOFF.zip`, SHA256 `91890dff146043ee727150e23a1fbf8a5921426f966b8c48f54d9b857f63c867`.
- Local script `cp367_canon_guard.py`, tests `test_cp367_canon_guard.py`, report JSON and CANON-only preview are in the handoff bundle.

## Binding image policy (user decision)
For **all characters** and **all subsequent visual previews**, only show the newest **user-approved character-specific CANON** image or precisely labeled crops derived from that actual CANON. **Never silently substitute an unrelated generated/image-search character image, old deprecated character version, or technical proxy.** If a new pose/sprite is being drafted from CANON, show it *alongside the actual CANON*, explicitly marked **UNAPPROVED DRAFT** until accepted; do not misrepresent a draft as the canon itself. If actual reference is unavailable, state so rather than showing another character.

## Art and release status
CP366's six partial SVG sleeve studies exist and are editable, but their visual quality is **NOT_PASSED**; the remaining full-body/hidden shoulder, accurate sleeve/hair fabric, actual painted raised-arm keyframe, spine rig and game APK remain unverified. CP367 is a **provenance and regression test**, not new independent full-body art or a pose completion. `production_release.status=blocked_pending_art` and `sprite_paths={}` remain mandatory.

## CP368 next work
1. Refine six independent CP366 painted fragments to match CANON shoulder/skin/sleeve, gold trims, silver hair and occlusion edges, then test actual hidden underpaint at small rotation.
2. Finish semantic high-resolution Front (head/face/body/other arm/legs/shoes) with its own truly painted pixels; do not treat a magnified crop as genuine native painting.
3. Show a same-view two-pose painter-authored comparison alongside the exact CANON and obtain approval; only then proceed to Spine/runtime and verified Android APK build.
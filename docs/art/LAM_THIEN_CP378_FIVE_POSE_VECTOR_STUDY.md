# Thanh Vân Ký — CP378: Lâm Thiển, five vector hand/silk pose study

**Date:** 2026-10-30. **Status: technical DRAFT / ART NOT APPROVED / not a Spine rig or Android APK.**

## Approved authority

- Exactly approved user CANON V2.1: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941 × 1672 RGBA, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- All reference visuals come from this exact file; the only other images are derived *drafts of Lâm Thiển* with NOT APPROVED labels. No unrelated illustration is used.
- Body +17%, hair/face, white-blue-gold clothing, five approved expressions, and four damage stages remain as-is in reference, **not created as actual animated full-body attachments**. Both approved blue shoe toes in CANON are untouched.

## Actual work

- Builds on CP376's **seven existing draft wrist/underpaint layers** but does not alter those shared SVGs.
- Adds **three separate original, editable SVG geometry layers for each of five positions:** (1) hand+three finger contours, (2) finger/nail/knuckle line details, (3) transparent rear silk with pose-dependent folds. Positions use one consistent landmark topology at `t=0, .25, .5, .75, 1`.
- Creates **five OpenRaster files**, each with 10 visible art layers and one hidden *exact CANON* reference, plus five transparent composite PNGs. 7 shared SVG files + 15 per-pose SVGs, with matching 22 PNGs.
- One-frame flipbook GIF is a **technical visual study**, not a game animation/verified FPS measurement. No raster crossfade between two complete fingers is used; every pose has one hand contour path with its own geometry.
- All work is mapped on 1302 × 2748 vector canvas from the small **217 × 458** reference crop. It must **not** be described as an independently fully redrawn high-definition full-body character.

## Verified technical QA

- **12/12 local unit tests PASS** using exact approved CANON plus CP374 matte/hand input. Test checks include SHA/crop, wrong-source rejection before output creation, five unique editable hand paths, intermediate alpha/centroid metrics, valid 5× OpenRaster stack and ZIP CRC, CANON reference hidden, GIF and preview existence, release still blocked.
- Simulated public GitHub CI without private files: **4 PASS, 8 SKIP**; skipped source-dependent tests are not art passes.
- Hand alpha-centroid distances for each adjacent 6× canvas frame: **12.076 / 12.120 / 12.220 / 12.333 px**. This indicates even movement of the *modelled region centroid* only; it does not establish that the animation looks natural, clothing obeys physics, or the hand anatomy is correct.
- CP376 residual diagnostic maintained unchanged as baseline: (-6,+3) 18px, (-4,+2) 21px, (+3,-2) 98px, (-8,+5) 26px. **These are not new CP378 motion-gap scores.** The hand silhouette change must not be 'fixed' by flood filling underpaint.

## Production blockers

- **VISUAL QA = NOT_PASSED**. Small vector hand/silk art does not closely reproduce the detailed approved CANON. Intermediate geometry is mathematically smooth but remains schematic.
- No independent production-grade high-res semantic Front full-body master; no real occluded anatomy and full-body draw order. Character face/eyes/mouth/expressions, armor/skirts, right arm, legs, and blue shoe tips are not ready as production sprites.
- No Spine/2D rig with mesh/physics, no Android runtime integration, no measured game FPS, no APK made/tested.
- Preserve `production_release.status=blocked_pending_art`, `sprite_paths={}` and do NOT import any CP378 output into Android assets.

## CP379 next — return focus to full body

1. Use approved CANON as the only authoritative reference, clean up remaining alpha/ground shadow and inspect lower dress/toes before any production art.
2. **Build an independent native painted full-body Front source** with separate face/hair/body/bodice/left/right arm/long skirt/legs/blue shoes, plus occluded anatomy. Do not describe masks from the 217×458 PNG as high-res repainting.
3. Use CP378 five-frame pose study as a temporary motion topology guide only; artist should draw real hand/silk key poses matching CANON and preview with the exact original.
4. Gate Spine/rig and APK until layer-native art is approved and verified on device.
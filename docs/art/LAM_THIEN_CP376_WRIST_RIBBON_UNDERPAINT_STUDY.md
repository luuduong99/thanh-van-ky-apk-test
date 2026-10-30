# Thanh Vân Ký — CP376 | Lâm Thiển wrist & rear-ribbon underpaint study

**Date:** 2026-10-30. **Status: technical 7-layer SVG/ORA DRAFT; art QA NOT PASSED, NO Spine/APK release.**

## CANON authority
- Only user-approved `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` is the reference.
- Preserve face, hair, white/blue/gold costume, body proportions (+17% already in the approved art), and **both blue shoe toes**.
- Image QA is composed **only** of the original CANON, its pixel-exact Front crop, and clearly labeled local technical drafts. No character replacement or unrelated image.

## Actual work
- Based on four independent CP375 source-locked SVG paths, **created three new, independently editable vector path layers** for (1) skin behind wrist edge, (2) inner gold cuff ornament, and (3) blue-white silk extending behind the moving hand.
- Exports seven per-layer SVG and independent transparent PNGs, plus an OpenRaster `.ora` with **7 visible new/draft art layers + 1 hidden exact CANON guide**. The vector canvas is 1302×2748 pixels using a coordinate grid derived from a **217×458 source crop**, not a rebuilt high-resolution painted full-body master.
- No source CANON, original matte or original hand image was modified. No raster pixels were copied from the CANON into these visible vector layers.

## Source-locked alpha QA (NOT visual acceptance)

| Hand shift in 217×458 crop | CP375 uncovered px | CP376 uncovered px |
|---|---:|---:|
| (-6,+3) | 90 | **18** |
| (-4,+2) | 68 | **21** |
| (+3,-2) | 121 | **98** |
| (-8,+5) | 113 | **26** |

For main shift (-6,+3): 204 original source-hand pixels became unoccupied after translation. CP375 drawing overlapped 114 of them; CP376 drawing overlapped another 72, leaving 18.

**Residual 18 pixel diagnostic groups:** 0 at likely wrist cuff seam (35 before), 3 at possible rear ribbon edge (40 before), **15 at moving fingertips** (15 before). Fingertips are a silhouette-pose difference, not evidence that stationary underpaint should be painted across the moving fingers. Do **not** use a zero-pixel score as an automated production gate. The ROI labels are technical hypotheses, require artist inspection.

The new art reduces source-alpha uncovered pixels but does NOT guarantee correct anatomy, convincing translucent silk, physical motion, rig stability, or no holes in other moves. There is still visible mismatch against the detailed CANON sheet.

## Verified checks and deliverables
- **11/11 local `unittest` tests PASS**, covering source hash/size, independent Bézier SVG content, invalid source preflight, four offset diagnostics, preservation of both blue shoe toes in upstream source, seven unique layer PNGs, ORA CRC/8 layers/hidden guide, fingertip restraint, and mandatory release blocking.
- Private CANON/matte/hand files are intentionally not part of the GitHub source repository. CI without them should **PASS 4 static tests / SKIP 7 real-asset tests**, not claim full 11 PASS.
- `cp376_local_wrist_refinement.py` builds reproducibly from CP375 source script and the exact CANON/matte/hand bytes; `test_cp376_local_wrist_refinement.py` validates the results.
- `OUTPUT/qa/CP376_CANON_GAP_CATEGORIES_UNAPPROVED.png` is a CANON-only comparison. `OUTPUT/ora/CP376_WRIST_RIBBON_SEVEN_DRAWN_LAYERS_NOT_RIG.ora` is editable in Krita.

## Remaining blockers / CP377
1. **Visual QA NOT PASSED.** The 3 new SVGs are coarse approximations of silk/skin/gold and differ from source painting. No independent high-resolution full-body art has been completed.
2. Remaining fingertip silhouette and rear ribbon appearance require artist-drawn **real alternate hand pose**, not blanket underpaint to reach 0 missing pixels. Test more pose offsets, partial transparency/draw order, and compare with exact CANON.
3. Finish full-body Front semantic art (face, front/back hair, bodice, both arms, translucent drapes, dress, legs and two blue shoe tips), including occluded anatomy. Then 5 expressions and approved 100/70/50/30 clothing integrity references.
4. Keep `visual_qa=NOT_PASSED`, `production_release=blocked_pending_art`, `sprite_paths={}`, `full_motion_gap_free=false`, `spine_ready=false`, `apk_ready=false` until explicit review and real APK/device testing.

**This checkpoint is a small verifiable art/alpha experiment, not proof that Lâm Thiển is animation-ready.**

## Package check
- Source and resulting `.ora` are part of the local ZIP; exact CANON PNG is included for traceability (not to be replaced by a generated reference).
- A separate `CP376_PUBLIC_MODE_TEST_LOG.txt` verifies test behavior with **4 static PASS / 7 source-dependent SKIP** when no private art is present.
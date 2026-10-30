# Thanh Vân Ký — CP375: Native-authored hidden-wrist study (not approved)

**Date:** 2026-10-30  
**Character:** Lâm Thiển / exact user-approved CANON V2.1  
**Status:** Technical art study completed; aesthetic approval **NOT PASSED**, Spine/Android release **BLOCKED**.

## Unchanged source of truth

- File: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, size 941×1672, RGBA.
- SHA256: `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Front crop: exact source rectangle `(13,172,230,630)` = 217×458 source pixels.
- Character model +17%, face/hair, white-blue-gold clothing, both blue shoe tips, expressions and four approved clothing-integrity milestones are **not modified**.
- Preview shows only the exact approved CANON, an exact crop, and CP375 draft pieces derived for **this character**. No substitute image.

## Actual new artwork and tests

- Four newly authored, independent Bézier/vector SVG paths and gradients: `01_hidden_silk_back`, `02_hidden_upper_sleeve_lining`, `03_hidden_forearm_skin`, `04_hidden_gold_inner_cuff`. Every file contains real drawn shapes, not a bitmap image embedded in SVG.
- Each SVG is natively rasterized at 1302×2748 into RGBA, and a 5-layer OpenRaster file is created (four visible art studies + one hidden CANON guide); **the 6× canvas does not turn original 217×458 CANON detail into native HD**.
- One constrained diagnostic for the former CP373 hand source layer shifted (-6,+3) checks local alpha exposure. Uncovered source pixels **204** before; newly drawn alpha overlaps **114**, leaving **90** uncovered. These counts describe alpha coverage, **not** approved anatomy, seamless motion, or artist-quality redrawing.
- Technical preview has CANON + exact crop + underpainting study + moved source test, labeled UNAPPROVED.
- **9/9 unit tests PASS** locally using real approved CANON + CP374 matte + source hand. Tests cover input checksum, wrong-source blocking, valid authored SVG paths, four independent nonempty artworks, ORA CRC/layers, two blue toes retained (163/163, 146/146), honest remaining seam and blocked APK/Spine status.

## Remaining issues / gates

- Art visually does not match the approved CANON's fine rendering and geometry. Underpainting is schematic and artificially clipped to the old visible hand source region for this one diagnostic. It cannot be used directly as a correctly rigged skeleton or game sprite.
- Partial CP374 floor shadow and pale silk matte remain unresolved. The rest of the 19 CP374 Front regions are still source-pixel routing guides, **not** newly painted full-body semantic art.
- Hand/arm and rest of body need **truly authored high-resolution complete artwork** with hidden skin, cloth and back hair; then independently drawn poses and tests of motion / draw order / all 5 expressions / 4 damage integrity levels.
- `visual_qa=NOT_PASSED`, `production_release=blocked_pending_art`, `sprite_paths={}`, `spine_ready=false`, `apk_ready=false` remain mandatory. No APK build was run for CP375.

## Contents and reproducibility

- `cp375_hidden_wrist_art.py` — reproducible rendering from exact CANON.
- `test_cp375_hidden_wrist_art.py` — nine technical tests (source-required tests skip on CI lacking private art).
- `OUTPUT/svg/` — four independent native SVG paths.
- `OUTPUT/layers/` — four RGBA layer PNGs at 1302×2748.
- `OUTPUT/CP375_FOUR_AUTHORED_HIDDEN_WRIST_LAYERS_NOT_RIG.ora` — edited layered study.
- `OUTPUT/qa/CP375_CANON_V2_1_PARTIAL_PAINT_COMPARISON_NOT_APPROVED.png` — comparison with true CANON.
- `OUTPUT/CP375_REPORT.json`, `CP375_TEST_LOG.txt`.
- `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, `CP374_PARTIAL_FLOOR_REMOVAL_NOT_ART.png`, and `14_left_hand_source.png` — exact source inputs used for reproducibility; never treat the latter as completed painted anatomy.

## CP376 start point

1. Repaint the **entire left arm/shoulder and sleeve** at native art quality, not just hidden wrist fragments. Maintain the exact CANON design, proportions, gold ornament, skin tones and hair overlaps.
2. Provide two clean manually authored poses; remove the remaining 90-pixel exposed source gap and run moving-geometry/draw-order QA, without cheating by copying/restoring already-visible arm pixels into an allegedly hidden paint layer.
3. Move to head/face, bodice/garment, right arm, legs/two blue shoes and all remaining Front semantic layers. Show *real CANON versus DRAFT* for approval before opening the Spine/Android release gate.
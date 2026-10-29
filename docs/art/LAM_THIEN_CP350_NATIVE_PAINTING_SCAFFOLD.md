# CP350 — Lâm Thiển CANON V2.1 native painting scaffold (not finished art)

Date: 2026-10-29. **Actual editable 17-layer OpenRaster template created, valid ZIP/CRC and layer validation PASS; art painting NOT DONE.**

## Why this is needed
CP349 low-res sampled-color shoulder backing reduced uncovered alpha counts 914 -> 263 but **failed visual QA** due to a vertical smear. More polygon auto-filling cannot replace real semantic redraw. Pivot/underpaint must be painted on its own editable canvas; approved reference may only be used to guide new art.

## New files and QA
- `CP350_NATIVE_PAINTING_SCAFFOLD_NOT_ART_NOT_RIG.ora`: valid OpenRaster, 1290×2694 canvas, **15 named transparent painter layers** for skin, face, hair, bodice, left/right shoulders and sleeves, ribbons, legs/blue shoes, and **2 guide layers**. Source CP348 raster is **nearest-neighbor scaled 6× as a faded guide only**. All genuine paint layers are still EMPTY.
- `CP350_PAINTING_SCAFFOLD_QA.png`: source close-up and annotated region, showing the image-left shoulder source ROI `x=54..71, y=122..188`, approximate image-left shoulder pivot `(70,132)` in 215×449 coordinates (**only a provisional visual hint, NOT a rig coordinate signoff**).
- `CP350_MANIFEST.json`, `README_CP350.md`, `cp350_build.py` portable builder (requires Pillow, NumPy). Open ORA in Krita to paint new native layers.
- OpenRaster checks on actual produced archive PASS: 17 raster layer entries, 15 with `__PAINT` names, merged image size 1290×2694, no CRC errors, manifest contains locked source hashes.
- Package `TVK_CP350_Native_Painting_Scaffold_NOT_ART_NOT_RIG.zip`, SHA256 `13327791e4254b451543022f83abad66aaee05c23ef2066d930319dadb24c941` (5 files), stored at Library `/Thanh Van Ky/Development/CP350_Editable_Front_Painting_Scaffold/`.

## CANON and release constraints
- Immutable CANON V2.1 user-approved image SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Guide comes from CP348 source 215×449, SHA256 `9033f86dca6ce69d96b8926c7abe92431f1bb7e585560637872070e1a0934814`. **Upscaling an image as reference creates no new art detail; this scaffold is not a high-resolution native redraw.**
- Body +17%, face, bodice, white/blue/gold outfit, hair, two visible blue shoe toes, 5 expressions, and damage states 100/70/50/30 are locked to CANON.
- No new underpaint has been painted; no rigid/animated joint solved; no visual QA on real painted two-pose motion; no Spine and no Android QA.
- Retain `production_release.status=blocked_pending_art`, `sprite_paths={}`. Do not claim completed art or production-ready rig.

## CP351 next material action
Paint the **first real image-left shoulder junction**, using the editable empty layers and CANON references: hidden skin, hidden bodice, separate sleeve, back hair occlusion. Render idle and a modest arm raise, compare to CANON at rest. Visual QA must PASS with no smear/holes. Do not progress to other angles/expressions until this genuine native art milestone is passed.
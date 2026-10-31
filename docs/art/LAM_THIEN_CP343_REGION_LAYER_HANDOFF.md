# CP343 — Lâm Thiển: Front editable region layers, EXACT rest-image reconstruction (2026-10-29)

**Approved base:** `LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29` — PNG 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. This source, its +17% body proportion, the precise bodice/coverage, hairstyle, accessories and the 5 core expressions and damage 100/70/50/30 are **unchanged**.

## Real new assets

- Took **exact existing CP342 215×449 RGBA Front** and hand-defined **10 nonoverlapping editable raster pixel regions** with separately saved PNG and binary masks. Groups: outer left/right hair+silk, left/right leg+shoe, center waist fabric, left/right arm+sleeve, bodice+necklace, head+hair ornament, narrow ambiguous seam regions.
- Created an actual **OpenRaster with 10 independent visible raster layers**, `CP343_FRONT_REGION_LAYERS_EDITABLE_NOT_RIG.ora`. Pixel assignment is **lossless at rest**, so recomposition matches the source alpha and the original RGBA of every pixel where alpha>0. Source RGB/body/bodice were **not repainted or changed**.
- Created colour-coded boundary QA `CP343_CANON_SOURCE_EXACT_LAYER_MAP_QA.png` and a region legend; built an explicit **articulation stress test**: shifted the two arm/sleeve regions ±10px / +5px. **1,798 original visible pixels became transparent holes**, plus **1,098 new protruding pixels** (see `CP343_ARTICULATION_UNDERPAINT_FAIL_QA.png`). This **fails the underpaint/motion gate** and is valuable evidence of where to draw hidden skin/hair/garment.
- Actual binary PNG, mask, OpenRaster ZIP/CRC and underpaint fail-stress QA: **12/12 local tests PASS**. This checks reproducibility and correct FAIL status, **not animation quality**.
- Package `TVK_LamThien_CP343_Source_Exact_Region_Layers_NOT_SPINE_READY.zip`: 34 files, ZIP CRC PASS, SHA256 `b61169d5b3fdb04dbbbd38df3ab080b2662e9332fabcc9c6ecaf660691ce9519`.
- Saved to ChatGPT Library Development `/Thanh Van Ky/Development/CP343_Canon_V2_1_Front_Region_Layers/`; includes `.ora`, all 10 source-group PNGs, masks, builder, reproducible stress test, image QA and file integrity manifest.

## Unfinished and BLOCKED

**These ten layers are approximate polygon-based partitions of ONE 215×449 flattened source.** Borders are intentionally provisional. Their parts are **not independently redrawn anatomical layers**, do not have painted hidden regions behind moving arms/hair, and are **not riggable**. Source resolution is too low for a high-quality native production master. A successful source-pixel composite is **not** evidence of physics, draw order, rig or Spine compatibility.

`app/src/main/assets/character_expression_profiles.json`: `production_release.status=blocked_pending_art`, `sprite_paths={}` unchanged. **No Spine/APK builds or new production sprite files.**

## CP344 — next useful production milestone

1. Open the ORA in Krita. Focus **only on left arm-to-shoulder and adjoining bodice** first: manually redraw the seam and inpaint real hidden skin/clothing pixels, matching V2.1 at rest. Do not change figure/bodice design or coverage.
2. Redraw hair/sleeve occlusion at that joint so the arm can rotate a few degrees and produce no transparent holes. Export separate proper shoulder/arm/cloth semantic alpha layers.
3. Build a two-frame movement QA (rest + small arm lift). At-rest composite must remain faithful to the full original approved character; movement must have no holes and no design drift. Also test the right shoulder after the left one is sound.
4. Continue native high-res line/shading redraw, then five facial attachments and four damage stages; retain restrained 30% wear. Ask user to accept *completed sprite art*, not to reapprove the V2.1 design.
5. Only after approval, integrate CP335 sprite hash release gate and actual Android/Spine build.

**Checkpoint status:** P0 CANON source lock COMPLETE; CP343 editable source segmentation COMPLETE; **P1 riggable layered painter art NOT DONE**; Spine and APK NOT DONE.

[Layer manifest](LAM_THIEN_CP343_REGION_LAYER_MANIFEST.json) · [Current plan](LAM_THIEN_PLAN_AFTER_CANON_V2_1.md).

# Thanh Vân Ký — CP380: Lâm Thiển full-body detail study (2026-10-30)

**Status:** editable full-body vector *DRAFT* produced; **Visual QA NOT PASSED**, not a production game sprite, not a Spine rig or an Android APK.

## Approved reference and fidelity policy
- Approved character reference is exactly `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- The source Front figure in that sheet is **only 217×458 native source pixels**. CP379/CP380 use 1302×2748 vector canvas but this does **not** magically turn the low-res source into painter-grade native HD art.
- User's CANON-only image policy is mandatory: no unrelated image, no alternate character/old design, draft always labeled and compared against approved CANON.
- The +17% approved proportions, silver/lavender hair, white/blue/gold outfit, accessories and both blue shoe tips remain source reference invariants, not independently artist-approved in the draft vector.

## Actual editable art work
- **Preserved 21/21 CP379 original full-body color-blocking layers** as original PNG **and SVG** bytes, including their ordering, without recomposing/re-encoding the individual original files.
- **8 independently authored new SVG layer drawings**, with PNG alpha counterparts: left/right separated hair shine strands, forehead fringe details, eyelash/iris/cheek strokes, white flower/ribbon ornaments, bodice white-blue fabric fold lines, neck/waist gold filigree and gems, silk/drape edge stitching.
- New OpenRaster `CP380_29_ART_LAYERS_DETAIL_STUDY_NOT_APPROVED.ora` has **29 visible art layers and 1 hidden exact-source CANON guide**. ZIP CRC and merged image re-composition are verified.
- `CP380_CANON_CP379_CP380_DETAIL_COMPARE_NOT_APPROVED.png` shows only the exact user-approved CANON sheet, CP379/CP380 drawing drafts and a pixel-exact CANON detail crop. No substituted reference.
- CP379→CP380 composite: **152,505 pixels with RGBA differences** across the 1302×2748 study canvas. This quantifies added artwork, **not beauty, similarity or motion**.

## Tests / limits
- **12/12 local tests PASS** with private CANON and CP379 art available, including source SHA, exact source PNG copy, original 21 PNG/SVG bytes, eight nonempty independent SVG/RGBA layers, 30-layer ORA CRC, mergedimage exactness, preview, wrong-source rejection before writes, explicit release BLOCK.
- Public source-only test simulation: **4 PASS / 8 SKIP** because private source assets are absent. An actual green CI workflow only checks public contracts, not the 8 asset tests.
- **Visual QA NOT PASSED**: full-body silhouette, eyes/face likeness, flower positions, bodice shape, silk folds and jewel density still differ substantially from approved CANON; rendered previews must not be used as game assets. No actual occluded anatomy drawn/validated, no five facial expression sprites or 100/70/50/30 clothing states, no Spine/physics, no frame timing/FPS, and no Android APK produced.
- **Required flags:** `production_release.status=blocked_pending_art`, `sprite_paths={}`, `native_painted_full_body=false`, `rig_ready=false`, `apk_ready=false`.

## CP381 next (substantive art quality milestone)
1. Stop relying on decorative vector tracing as evidence of CANON fidelity. **Artist-grade native painted head/face and bodice** are now the blocking prerequisite. Match approved CANON face/eye spacing, head and hair silhouette and gold ornaments; produce full-size layered art independently (not blurred magnification of 217×458 crop).
2. Establish full-body semantic painter layers and physically plausible hidden skin/cloth/hair underpaint; test small movement and draw-order for each joint, especially wrist/shoulder and ribbons.
3. Provide side-by-side actual CANON vs painter-authored layer composites for explicit visual acceptance, then implement 5 expressions and the 4 preapproved clothing states, secondary views, rig/Spine, and verified Android APK.
4. Carry over all existing automated checks and **never switch production status** until the actual visuals and runtime have passed.
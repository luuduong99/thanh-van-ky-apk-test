# Thanh Vân Ký CP377 — Lâm Thiển | Independent fingertip + silk pose draft (2026-10-30)

**STATUS: technical draw study, visual QA NOT PASSED. No native full-body artist-grade art, no rig, Spine or APK.**

## Canon authority
- Exactly user-approved `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- All previews show only this exact image, a pixel-exact crop or clearly marked CP377 draft derived from this same character. Never show unrelated generated characters.
- Keep the locked +17% proportions, white/blue/gold costume, silver hair, face and both blue shoe toes. The actual CANON is unchanged.

## Verified actual work
1. Retained 7 editable CP376 wrist/sleeve SVG layers unchanged. Created 4 **new independently authored SVG paths**: `idle fingertips`, `raised fingertips`, `idle rear silk fold`, `raised rear silk fold`. Neither pose is a raster translation or rotate of the other; the finger outline and fabric drape geometry differ.
2. Two `.ora` files (`CP377_IDLE_NINE_DRAWN_LAYERS_DRAFT_NOT_SPINE.ora`, `CP377_RAISED_NINE_DRAWN_LAYERS_DRAFT_NOT_SPINE.ora`): each **9 visible vector-derived art PNG layers + 1 exact-CANON guide hidden**, canvas 1302×2748 based on 217×458 source crop. Includes editable SVGs for every layer, 2 flattened partial previews and CANON-only side-by-side QA image.
3. 36,705 source-canvas RGBA pixels differ between the 2 composited partial poses. This establishes independent geometry, not a faithful full-body keyframe or smooth game animation.
4. The CP376 alpha diagnostics for original moving source are intentionally left **unchanged**, because old fingertip pixels disappearing during a pose is not the same as missing hidden anatomy: (-6,+3)=18, (-4,+2)=21, (+3,-2)=98, (-8,+5)=26 source pixels. No artificial zero-gap claim.
5. `10/10 local unittest PASS` with actual private CANON and CP374 hand/matte assets. GitHub-layout **4 PASS / 6 SKIP** simulation without private images. ORA ZIP CRC verified; source hash verified; RGB unchanged; both blue shoe regions of source matte 163/163 and 146/146 unchanged.

## Important limitations
- **Visual QA NOT PASSED.** These are modest locally drawn vector sketches, still noticeably simpler than approved CANON painting; fine fingers, nails, silk transparency and attachment angle are artist-review tasks.
- The two drawings depict *only hand contour and silk underlayer variations*, not two completed independent full-body frames. No intermediate motion frames, mesh physics, skeleton, Sprite runtime, device FPS, or APK.
- The remaining CP376 source-pose residuals are diagnostics, not production clearance. `production_release.status=blocked_pending_art`, `sprite_paths={}`, `spine_ready=false`, `apk_ready=false`.

## Next: CP378
- Prioritize a real artist-reviewed hand+forearm master and wrist attachment geometry which seamlessly matches exact CANON; perform multi-pose hand anatomical draw-order review and avoid flood-filling moving finger boundaries.
- Finish high-resolution native semantic full-body layers (head/face, hair front/back, bodice/skin, both arms, skirt/drapes, legs and two blue shoes), clean underpaint and floor shadow, then create five expressions and 100/70/50/30 overlays. User preview and acceptance must come before real rig/Spine/Android build.

**Reproduction:** Python3 Pillow NumPy CairoSVG OpenCV. Run `cp377_fingertip_and_silk_keypose.py --canon ... --matte ... --hand ... --out OUTPUT`; run `python -m unittest -v test_cp377_fingertip_and_silk_keypose.py` in directory with actual sources.
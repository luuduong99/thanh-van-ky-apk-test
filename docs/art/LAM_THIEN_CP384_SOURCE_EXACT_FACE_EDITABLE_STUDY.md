# Thanh Vân Ký — CP384 | Lâm Thiển canonical portrait, reversible eye/mouth source layers

**2026-10-30. Status: source-accurate STATIC face construction PASS; Blink/underpaint VISUAL QA NOT_PASSED. NOT RIG / NOT APK.**

## CANON source
- Only user-approved `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, exact SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Chosen original expression: `Ngại ngùng` / `01_shy_Ngai_ngung`, exact native crop in original sheet `[25,684,193,881]` = 168×197. Its small native resolution is not improved by enlarging previews. The portrait is still part of an infographic with opaque background — **not a clean transparent game sprite**.
- User requirement: show **only the right character's approved CANON** (or crops), and never treat vector technical studies as production art. The expression's approved *source* is different from the quality acceptance of animation/paint.

## Actual output
- Three editable source-exact visible layers: two independent eye regions and mouth region. The source region is split with non-overlapping binary masks, all original source RGB/A preserved in the cutouts.
- One visible `technical_inpaint_underpaint_NOT_APPROVED` composite base, derived from the source by local CV inpainting inside eye/mouth regions only. It is NOT artist-made skin/eyelids/hair and NOT visual-acceptance ready.
- Two **hidden** experimental blink-eyelid paint layers, one hidden native CANON reference; **7-layer ORA** in Krita. Static `mergedimage.png` recomposes pixel-for-pixel exactly to source CANON crop, not just visually similar.
- Separate `CP384_BLINK_TECHNICAL_DRAFT_NOT_APPROVED.png` demonstrates why automatic skin infill remains flawed: blurred/smeared eye edges. This is **not** acceptable game animation or an approved expression, and is not included in production assets.
- QA contact sheet compares only actual CANON source, exact editable static reconstruction, technical inpaint, and **rejected** technical blink draft. No other character/stock image.

## QA
- `10/10` local unittest PASS with private CANON. Includes source SHA lock, invalid source rejected before any output, exact static recomposition, mask non-overlap, preservation of all original pixels outside editable ROIs, ORA ZIP integrity/visibility and release blocking.
- Public-only simulation without private CANON: `3 PASS / 7 SKIP`. Do not interpret public CI as confirmation of rendered art.
- Targeted native artwork still missing: actual repaint of closed lids with correct lashes/eyebrows/hair, face/hair occlusion, mouth expression frames, clean transparent silhouette, resolution-appropriate master, full-body motion, Spine/physics, APK/device validation.

## Next: CP385
1. Hand-paint **one correctly matched closed-eye/shy expression** using CANON original's lashes, hair strands and blush; compare in-place to CANON before accepting. This technical inpaint output is a guide only, not publishable art.
2. Clean background matte and provide proper hair/skin occlusion under eyelids/mouth without visual holes; verify masks and compositing both at native and displayed scale.
3. Extend only after approval to other four expressions and full-body layered animation. Keep `visual_qa=NOT_PASSED`, `production_release.status=blocked_pending_art`, `sprite_paths={}`, `spine_ready=false`, `apk_ready=false`.

Code: `tools/art/cp384_exact_face_eye_master.py`. Tests: `tests/art/test_cp384_exact_face_eye_master.py`. Private output bundle in Library CP384. No production app assets are touched.
# Thanh Vân Ký — CP369 | Separate shoulder/wrist gold + local underpaint QA

Date: 2026-10-29. Character: **Lâm Thiển**. Stage: **LOCAL ART TECHNICAL DRAFT — NOT APPROVED**.

## Immutable authority
- Exact user-approved source: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Precise Front reference `(13,172,230,630)` → 217×458. 1302×2748 SVG workspace is authored against this small reference crop, **not** proof of native 4K detail.
- Keep +17% body design, face, hair, white/blue/gold costume, **both blue shoe tips**, expressions and clothing integrity levels 100/70/50/30. Only CANON/crops from CANON are visual reference. CP368/CP369 are clearly labeled **UNAPPROVED DRAFT**.

## Actual CP369 implementation
- Created **seven independent editable SVG and transparent RGBA layers**: lavender rear hair, occluded bodice material, occluded shoulder skin, arm+hand, draping sleeve, moving wrist gold and **static shoulder gold**. CP368 incorrectly combined shoulder and wrist gold into one motion layer.
- Added hand-authored vector geometry beneath the left arm: small skin patches at newly exposed shoulder seam and extra white/blue bodice underpaint. These are **not** nearest-neighbor alpha dilations or a pixel crop pretending to be fully painted new art.
- Composite idle and technical rotations at **−8°, −15°, +8°**. Only arm/sleeve/wrist move; shoulder jewelry and underpaint are anchored. This is a rigid bitmap rotation study, **not painter-drawn secondary keyframes, Spine rig or true smooth game animation**.
- **Local revealed-joint audit (source coordinate ROI x=54..83, y=124..170):** at −8°, 3,192 previously covered arm pixels became exposed; at −15° 5,905; at +8° 789. All were backed in this **limited ROI** by edited body/skin alpha. Negative control stripping both occluded layers fails, so this particular test is meaningful. **No claim of whole-character hole-free motion**, occlusion correctness, cloth physics or visual approval.
- Exported OpenRaster with seven visible editable layers and one hidden exact-CANON guide; tested ZIP CRC, source SHA, canvas, independent gold source, motion comparison and release gate. **8/8 local tests PASS**, with missing-source asset checks skipped in CI if private art is not mounted.

## Files
- `cp369_split_gold_and_underpaint.py` and `test_cp369_split_gold_and_underpaint.py` are reproducible technical art and QA code. Dependencies: Python 3, Pillow, NumPy, CairoSVG, and the adjacent CP366 + CP368 art source modules.
- `OUTPUT/CP369_SEVEN_LAYER_SEPARATED_SHOULDER_WRIST_NOT_SPINE.ora` is editable artwork study; not full character source.
- `OUTPUT/CP369_CANON_V2_1_CP368_CP369_SIDE_BY_SIDE_UNAPPROVED.png` places the true CANON next to earlier/new clearly labeled drafts and technical pose; **no unrelated character image**.
- `OUTPUT/CP369_QA_REPORT.json` records measured local motion, not claims of completed animation.

## Known issues — MUST remain blocked
- Current SVG styling remains simplified relative to the approved CANON painting: sleeve folds, hair, jewelry, color/material blending and hand silhouette require artistic redraw and validation.
- Only one partial left arm is available. No full-body semantic master, true second raised-arm keyframe, right arm, face expressions, outfits/damage variants or finished blue-toe shoe sprites.
- No finished Spine/2D rig, Android APK integration or device FPS measurement from this asset.
- **Visual QA = NOT_PASSED; production_release = blocked_pending_art; sprite_paths = {}.** Do not replace approved CANON with CP369 draft.

## CP370 next actionable scope
1. Visual manual refinement of CP369 shoulder/hair/silk proportions directly against pixel-exact CANON, then user art preview approval (not assumed).
2. Extend genuinely drawn independent body layers beyond left arm (right arm, face/eyes, full torso/legs/shoes) with hidden-underpaint and clear occlusion order; preserve both blue shoe toes.
3. Create proper **painted idle + raised-arm keyframes** of the *same* character (not a rotated bitmap) and verify both still match CANON. Only after approval may Spine/game integration and an APK test be considered.
# CP348 — Lâm Thiển | Refine blue shoe toe and propagate to ten editable CP343 layers

Date: 2026-10-29. **QA work completed. Native high-resolution art, motion underpaint, Spine and Android APK NOT complete.**

## Source-provenance lock
- User-approved CANON V2.1 PNG 941×1672 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; it remains **unmodified**.
- CP343 ten-region source ZIP SHA256 `b61169d5b3fdb04dbbbd38df3ab080b2662e9332fabcc9c6ecaf660691ce9519`.
- Original CP342 215×449 crop SHA256 `d1f8ab09f517d484d93c7356270338c040c399b9a715c30624c6cefd2d635890`.
- CP347 QA candidate SHA256 `986a1ad9d68568f280cf8f562a98661d0a8bc17dc156a013a485b4bcc5b6ef6f`.
- None of the old locked files were replaced.

## Verified repair
- Identified excess pale blue-gray floor pixels at edge of image-left shoe in CP347. Created a tighter *experimental* alpha polygon at ROI x=[84,116), y=[432,449) only, anti-aliased at 8×.
- Alpha altered on **349 pixels**, versus 416 pixels in CP347, and **243 new pixels cross alpha>128**. Blue shoe pixel visibility within ROI increased from 14 to 119 according to fixed RGB threshold, compared with 153 in CP347 wider matte. Reduced extraneous matte while leaving the original visible region intact. This is not a guarantee of perfect final shoe contour.
- **RGB unchanged over entire canvas**, no alpha modification outside foot ROI, no pre-existing alpha erased, opposite shoe unchanged.
- Integrated corrected alpha/RGB pixels into CP343's **ten disjoint editable region PNGs** and wrote a valid **10-layer OpenRaster** `CP348_TEN_REGION_TOE_FIXED_NOT_RIG.ora`. Original visible pixels retain their original ownership. Newly recovered pixels are assigned provisionally to image-left shoe group `03_left_leg_and_shoe`. This is a provisional source region, **not a painter-drawn independent limb**.
- ORA and layer recomposition match repaired flat input **for all alpha pixels and all RGB pixels where alpha>0**. Hidden RGB for fully transparent pixels is not promised identical.
- Created foot close-up / full-front before-after previews and a zip with 20 files containing reproducible Python patch, 29 automated actual-source tests and integrity manifest.
- **29/29 local QA assertions PASS**: SHA/source locks, alpha-only ROI, opposite shoe, no overlap, recomposition, ORA CRC/mergedimage and confirmation that shoulder movement still has defects.
- 20-entry package: `TVK_LamThien_CP348_Foot_Toe_10_Layer_QA_NOT_RIG.zip`, SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`, ZIP CRC PASS.
- Stored in Library `/Thanh Van Ky/Development/CP348_Shoe_Toe_Ten_Layer_Recovery_QA/` with two comparison PNG files. Use **CP348** rather than CP343 as the next **QA-only source of the shoe visibility**; do not overwrite CANON V2.1.

## QA vs production
- This derives from a **215×449 low-res flat crop**. The feet can still contain a little painted-in original floor/shadow. Avoid upscaling and claiming a crisp final sprite.
- **CP346 shoulder gaps remain**: counts were 914/500 left, 884/598 right, 1798/1098 both before this foot patch. CP348 motion regression testing still observes substantial missing coverage; no real shoulder underpaint has been painted.
- Body proportions (+17% already baked in), face, hair, bodice, white/blue/gold costume, four damage stages and five expressions are unchanged.
- No user-approved native high-resolution layered art, rig/Spine animation or FPS/device test. Production flags `production_release.status=blocked_pending_art`, `sprite_paths={}` remain unchanged.

## CP349 prioritized next action
1. Obtain or paint **actual native high-resolution Front semantic layers**, first tackle image-left shoulder/arm-to-bodice hidden skin/cloth/hair (not more source-region polygon tweaks).
2. Render idle plus slightly lifted arm with genuine hidden layers, inspect source-canon silhouette against V2.1. Keep toe visibility in QA after movement.
3. Repeat on opposite shoulder and face attachments; only after art acceptance run rig/Android performance tests.
4. Do not claim work complete based on QA mockups or PNG posters.

## Reproduction
Open the QA ZIP from Library. Its root includes `cp348_integrate_toe_refinement.py`, `test_cp348_real_assets.py`, repaired PNG, the 10 region PNGs, the ORA and exact SHA manifest. It requires Python, NumPy and Pillow, and the original three locked inputs as documented in README.
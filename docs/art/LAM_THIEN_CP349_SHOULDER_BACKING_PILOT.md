# CP349 — Lâm Thiển: experimental left shoulder underpaint; visual QA FAIL

Date: 2026-10-29. Source is actual CP348 ten-region raster image, **not generated demo art**.

## Source integrity
- CANON V2.1 approved image: SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- CP348 QA ten-layer ZIP: SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`.
- 215×449 source with ten coarse segmented layers, all original color/body/attire unchanged. Left arm source is layer `06_left_arm_and_sleeve`, a raster region containing some hair/sleeve; it is not a semantic bone attachment.

## Executed compositor pilot
- Created `CP349_EXPERIMENTAL_LEFT_SHOULDER_UNDERPAINT_NOT_ART.png`: 950 opaque backing pixels within ROI `(54,122)..(71,188)`, with RGB copied/interpolated from nearby visible source colors. The backing layer is composited **behind** the region layers, not painted from true anatomical underlayer.
- At-rest composite vs CP348: exact RGBA match **PASS**.
- Move only image-left arm (-10, +5) pixels:
  - Previous uncovered coverage pixels: **914**.
  - After pilot backing: **263**.
  - Regained: **651** (71.2% of prior uncovered coverage).
- Visual inspection: backing creates a vertical **unnatural smeared strip** on the bodice/underarm. **Visual QA FAIL.**
- A technical GIF `CP349_MOTION_EXPERIMENT_NOT_RIG.gif` demonstrates the defect; it is NOT a gameplay animation.
- Archived QA package ZIP `TVK_CP349_Shoulder_Underpaint_Pilot_NOT_RIG.zip`, SHA256 `18815b317d3cda7a7a87d25d3afa45812110081072445d8b67096687bd12fa4a`, seven entries, ZIP CRC PASS.
- Saved to Library `/Thanh Van Ky/Development/CP349_Shoulder_Underpaint_Compositing_Pilot/` with QA PNG and GIF. Reproduction code: `tools/art/cp349_shoulder_backing_pilot.py`.

## Gate and next steps
- **Do not integrate CP349 art/animation** into the game. The percentage change is only a coverage measurement and does not prove a correct anatomical joint.
- Need a true **native high-resolution, artist-painted** shoulder/arm, bodice underpaint, separate sleeve/hair with hidden pixels. At minimum, draw two poses idle + gentle arm-lift; examine both pixel/visual QA against original CANON V2.1.
- CP350 target: replace strip with painted hidden fabric/skin, refine shoulder pivot and sleeve overlap, then inspect remaining 263px missing areas; if native art is unavailable, no amount of alpha coverage metrics may substitute.
- CANON V2.1 shape (+17%), face, bodice, white-blue-gold costume, expression and four damage states are immutable.
- Release stays `production_release.status=blocked_pending_art`, `sprite_paths={}`. No Spine or Android device QA has occurred.

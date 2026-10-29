# CP354 — Lâm Thiển: small-motion local mesh deformation pilot (NOT production art)

Date: 2026-10-29. **Actual source QA complete, 12/12 automated checks pass; visual/art acceptance not granted.**

## Purpose and actual work

CP352's procedural painted underlayers exposed long peach/blue bands and failed visual inspection. CP353 independently rotated a crudely grouped sleeve layer at small angles, still creating alpha gaps. For CP354 we evaluated an **alternative technique for subtle idle animation only**: deforming the **whole CP348 215×449 image locally** using a smooth image-space displacement near the image-left sleeve, anchoring the shoulder to avoid the hard line introduced by rotating a cut-out region.

- Locked user-approved CANON V2.1 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` unchanged.
- Locked CP348 blue-shoe-restored region ZIP SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497` unchanged.
- Experiment uses fourfold **nearest-neighbor enlargement only for sampling** (860×1796 output), **not new high-resolution drawing**. Dense optical inverse warp, with falloff around shoulder/arm, ~3.8 source pixels lateral and 2.2 pixels vertical distal maximum motion. Premultiplied-alpha resampling reduces halos.
- The face, right side and both feet including the **two blue shoe toes** remain bitwise unchanged at all five tested positions. Idle image is pixel-exact to 4× CP348 nearest-neighbor.
- The 25-frame GIF is an offline rendered 0→100→0% cosine easing loop, not measured Android FPS or Spine animation.

## Measured coverage changes

| Warp amount | Lost-visible source pixels | Newly visible pixels | Lost pixels in shoulder seam ROI |
| --- | ---: | ---: | ---: |
| 0% | 0 | 0 | 0 |
| 25% | 0 | 2 | 0 |
| 50% | 12 | 23 | 0 |
| 75% | 22 | 39 | 0 |
| 100% | 36 | 67 | 0 |

These are **coverage changes**, not automatically valid/invalid anatomy. This movement's amplitude is not equivalent to CP346's -10,+5 whole-arm translation or CP353's angles, so these figures **must not be used to assert a superior same-motion comparison**. Continuous warping can still visibly deform textures and fabric and does not recreate hidden body geometry.

## Actual deliverables

- `CP354_SHOULDER_MESH_SIDE_BY_SIDE_QA.png`: actual five-position detailed seam view.
- `CP354_FULL_FIGURE_MESH_COMPARISON.png`: full-figure idle vs maximum motion.
- `CP354_LOCAL_MESH_MOTION_QA_ONLY.gif`: 25 frames source-locked.
- `CP354_IDLE_REF.png`, `CP354_MESH_POSE_FULL.png`: RGBA outputs.
- `build_cp354_mesh_motion.py` plus `test_cp354_real_source.py`, metrics, README and integrity manifest.
- **12/12 real-source test guards PASS**: source hashes, canvas, idle, unchanged face/feet/opposite side, nonzero arm movement, 100% lost coverage <100, no detected lost coverage in shoulder seam ROI, 25 GIF frames, previews, release gate.
- Bundle `TVK_CP354_MESH_MOTION_QA_ONLY.zip` has **11 files**, SHA256 `709170f2e8e8577ea9f8f7d3674142c243f0677fda1a91aea7cc5aadc7b359e4`, CRC PASS.
- Library folder: `/Thanh Van Ky/Development/CP354_Local_Mesh_Motion_Probe/`. Small core reference implementation: [mesh probe](../../tools/art/cp354_mesh_deform_probe.py).

## Release gate

**This is a modest motion-prototype alternative, not the CP354 painter-grade Native Art milestone.** No actual new semantic high-res skin/bodice/sleeve/hair layers, large-amplitude gesture or combat rig, Spine export or Android performance verification. Keep `production_release.status=blocked_pending_art` and `sprite_paths={}`; no APK art release. CANON V2.1 (+17%, face, hairstyle, bodice, white/blue/gold costume, toe shapes, five expressions and four damage stages) remains unchanged.

## Next actual visual-art task

Use CP351 editable ORA as an underpainting workspace, **create actual independent high-resolution arm/sleeve/body/hair art** including hidden skin/cloth under the shoulder, show user/artist side-by-side CANON vs idle and an active raised-arm pose. Mesh warp may later be a controlled *idle-only* technique, but cannot substitute for dynamic combat actions with real articulation. Do not repeat further color-fill tricks as if they were native redraw.
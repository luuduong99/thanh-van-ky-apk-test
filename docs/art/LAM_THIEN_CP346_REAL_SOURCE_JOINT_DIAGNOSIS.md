# CP346 — Lâm Thiển: real-source two-shoulder motion diagnosis

Date: 2026-10-29. **Source-level diagnostic complete; painter-quality joint underpaint NOT DONE.**

## Provenance and approval
- CANON V2.1 final approved `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` 941×1672, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- CP343 region-layer archive SHA256 `b61169d5b3fdb04dbbbd38df3ab080b2662e9332fabcc9c6ecaf660691ce9519`.
- Both files retrieved from existing user Library; SHA verification PASS. Original CANON image is unmodified.
- Used genuine CP343 source and all 10 editable raster region layers (215×449), not fabricated synthetic test images. Pixel-exact at-rest RGBA recomposition PASS.
- Motion is diagnostic translation only: image-left arm (-10,+5) px; image-right arm (+10,+5) px.

## Measured source coverage changes (NOT repaired)
| Motion | Original visible pixels no longer covered | New visible pixels outside original |
| --- | ---: | ---: |
| Image-left arm only | 914 | 500 |
| Image-right arm only | 884 | 598 |
| Both arms | 1798 | 1098 |

- Both-arm counts independently reproduce CP343 baseline: 1798/1098.
- Motion masks and visual QA image built from real source. One mask `underpaint_priority_mask_NOT_PAINT.png` unions source regions that reveal blank coverage during test. It is a guidance layer only; no skin/hair/cloth has been painted beneath the joint.
- 5 local actual-source QA assertions PASS: locked source hashes; ZIP + at-rest recomposition; per-arm counts; mask union; production-release block flags.

## Reproduce
```bash
python tools/art/cp346_joint_motion_audit.py --cp343-zip /path/to/CP343.zip --canon /path/to/CANON.png --out-dir /tmp/cp346
```
Requires Python, NumPy and Pillow. The tool fails on wrong source hash and unexpected baseline. Source archives are in user Library under `/Thanh Van Ky/Development/CP343_Canon_V2_1_Front_Region_Layers/` and `/Thanh Van Ky/Approved References/Lam_Thien_CANON_V2_1_FINAL_20261029/`.

## CP347 actual art deliverable gate
1. Obtain/repaint high-resolution Front in genuine semantic editable layers, not CP343 masks enlarged. Paint hidden skin, bodice fabric, hair and sleeve under image-left shoulder first; maintain CANON V2.1 exactly (+17% included, bodice, face, colors).
2. Deliver separate native alpha PNGs + layered ORA with underpaint, shoulder pivot and correct overlap; rest/raised-arm composite before/after side-by-side.
3. Repeat for opposite shoulder, measure real joint-frame alpha and visually inspect the new seam. No release based solely on pixel-delta reduction.
4. Only then implement rig/smooth interpolation, five expressions, damage stages, Android APK FPS measurement.

`production_release.status=blocked_pending_art`, `sprite_paths={}`; no art/Spine/APK acceptance.

## Archived QA package for continuing CP347
- User Library: `/Thanh Van Ky/Development/CP346_Real_Source_Shoulder_QA/`.
- ZIP: `TVK_LamThien_CP346_Real_Asset_Joint_QA_NOT_RIG.zip` — SHA256 `04ad01e18aa924327b817b0ae7fb539a77eadf162a4eb64b5e98f6429af27729`, 17 files, archive CRC PASS.
- Preview: `CP346_REAL_ASSET_JOINT_QA.png`, side-by-side source / left / right / both translation with missing/new alpha highlights.
- Package includes full QA preview generator, re-run CLI, 5 actual-source local tests, masks, JSON metrics, and SHA manifest. Art layer paint is **still absent**; a passed QA test is not a passed rig.

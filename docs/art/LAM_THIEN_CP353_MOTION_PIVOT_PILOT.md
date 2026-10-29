# CP353 — Lâm Thiển: small-angle shoulder pivot diagnostic, NOT a native redraw

Date: 2026-10-29. **Motion QA pilot complete; CP353's requested painter-quality native redraw is still incomplete.**

## Decision and provenance

- CANON V2.1 final approved image unchanged (SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`).
- CP348 ten-region toe-repaired source unchanged (archive SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`; 215×449 original).
- CP352 three gradient material studies were **visual QA FAIL** due to a conspicuous skin/blue vertical band. This CP353 **does not claim to repair those studies**; instead it measures a different, less aggressive motion: rotate image-left arm around provisional pivot at (70,132) in source pixels. Reference is upsampled sixfold for motion compositing; the 6× raster remains low-res source, not native high-res painted art.

## Actual measured diagnostics

| Angle | Lost coverage | New coverage |
| --- | ---: | ---: |
| 0° | 0 | 0 |
| -0.25° | 0 | 0 |
| -0.5° | 27 | 8 |
| -0.75° | 55 | 16 |
| -1° | 80 | 21 |
| -1.5° | 121 | 45 |
| -2° | 157 | 77 |
| -3° | 251 | 147 |
| -5° | 414 | 251 |

CP346's previous **-10,+5-pixel whole-arm translation** exposed 914 lost pixels. **Rotation is a smaller, qualitatively different movement**, therefore the lower counts are *not* evidence of solved underpaint or a superior equivalent-amplitude animation.

- Measured on the real CP348 ten-layer source; SHA checks PASS, source ZIP CRC PASS, arm-only transform PASS, pixel-exact idle reproduction PASS, both blue shoe toes unchanged throughout PASS.
- 25-frame cosine-eased `CP353_GENTLE_PIVOT_MOTION_QA_ONLY.gif` generated from real pixels, up to 2°. It is *not* a Spine animation, APK capture or measured 60fps performance.
- `CP353_PIVOT_ROTATION_COMPARISON_QA.png` shows the seam at idle, old translation, and -1/-2/-5-degree rotations; `CP353_FULL_FIGURE_REST_VS_PIVOT.png` preserves complete figure for visual comparison.
- QA bundle `TVK_LamThien_CP353_Gentle_Pivot_Motion_QA_NOT_RIG.zip` has 7 files including a portable builder, metrics and SHA manifest; SHA256 `b6243c48171f991a868677b0977eab65884fe3447089484becf48dda4d9dbd47`, ZIP integrity PASS.
- Library: `/Thanh Van Ky/Development/CP353_Gentle_Pivot_Motion_QA/`; code to reproduce alpha metric from genuine CP348 asset: [pivot audit](../../tools/art/cp353_motion_envelope_check.py).

## Mandatory art gate remains

**No high-resolution independently painted skin/bodice/hair underlay, no semantic arm/sleeve separation, no approved idle + arm-lift, no real Spine skeleton, no verified Android APK**. Use CP351 editor scaffold for future painting. Keep `production_release.status=blocked_pending_art` and `sprite_paths={}` unchanged; don't mistake a smooth small-angle GIF for finished game motion.

Next: artist/native redraw the image-left shoulder with separate hidden skin, bodice, sleeve and back hair, then compare physically plausible motion frames against CANON V2.1, preserve both blue toes. Only after visual approval can more ambitious movements and rig/Android QA be considered.

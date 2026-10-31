# CP352 — First non-empty semantic shoulder underlay studies (NOT APPROVED)

Date: 2026-10-29. **Material pilot complete; visual QA FAIL. Do not ship or replace CP351.**

## Actual work performed
- Opened existing CP351 21-layer OpenRaster, not a simulated document, with locked inputs: CANON V2.1 SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, CP348 10-region ZIP SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`, CP351 ORA SHA256 `511c495302057daad9f8538a84cc74fe60ca90f84ef400b7ffbcbd38d230ab79`.
- Kept 21 layers (4 hidden QA guides, 15 editable paint layers, 1 additional existing guide and the flat reference). Populated **three previously empty painted raster layers** at 1290×2694 using manually directed curved shapes and color gradients: `06__LEFT_SHOULDER_HIDDEN_SKIN__PAINT`, `08__LEFT_SHOULDER_HIDDEN_BODICE__PAINT`, `12__HAIR_BACK__PAINT`. **12 paint layers remain blank.**
- These were only **hand-directed experimental material/color studies**, not artist-redrawn original high-resolution body parts. Their alphas are limited to the hidden, originally opaque arm region; the CP348 flat reference is stacked above the experimental underlays.
- Rendered genuine source-aligned **rest and arm-translation (-10,+5)** comparison. At rest the downsampled result is pixel-for-pixel equal to CP348; both shoe toes are unchanged. The ORA `mergedimage.png` remains byte-identical to CP351.
- Alpha-coverage lost when moving the image-left sleeve/arm: **914 source pixels baseline → 366 with CP352 pilot**. This is a simple alpha-coverage measure, not proof of correct anatomical shading. Note CP349 had **263** with a different source-color backing and also failed visually; CP352 is **not** an improvement on that metric.
- **Visual QA FAIL**: the raised-arm image shows a conspicuous long peach/blue color band. Do not use this art for runtime, do not interpret as successful native painting.
- OpenRaster 21-layer check PASS, 3 nonempty / 12 blank painter layer check PASS, ZIP CRC PASS, reference CANON hash check PASS, idle image unchanged PASS, toe regression guard PASS. **No Spine or APK test performed.**

## Files and reproducibility
- ORA `CP352_SHOULDER_3_PAINT_LAYERS_REST_LOCKED_NOT_RIG.ora`, SHA256 `5616029023f0a9e5c6e719eefed806e9fc629190a8d6d4a554b341ef1b87238a`.
- QA preview `CP352_LEFT_SHOULDER_TWO_POSE_QA.png` shows rest, arm-shift without backing, and shift with three material studies.
- Full ZIP `TVK_CP352_SHOULDER_THREE_PAINT_LAYERS_EXPERIMENT_NOT_RIG.zip`, SHA256 `a5755fbd5adee753cea17725418e39d5af47ec4abb44c5b003a940baa6325b31`, with `build_cp352.py`, manifest, preview, two frames and ORA. Python builder uses Pillow, NumPy, SciPy; source locations in script reference a working-directory layout and must be adapted to reproduce outside the work session.
- User Library path: `/Thanh Van Ky/Development/CP352_Shoulder_Three_Layer_Paint_Study_FAIL_QA/`.

## Art/production gates and next
- **CANON V2.1 stays untouched**: +17% proportions, face, hair, white/blue/gold costume/bodice, blue toes, expressions and damage 100/70/50/30. No approved changes.
- `production_release.status=blocked_pending_art`, `sprite_paths={}`; no rig, no motion acceptance, no APK.
- **CP353:** painter redraft on three layers: replace artificial vertical bands with continuous anatomy and cloth folds; separate the arm/sleeve silhouette from hair and bodice with real underpaint; compare to approved full figure in idle and raised-arm views, inspect seam at native zoom. Fix visual QA first (not just coverage count). A 215×449 flat source cannot provide true artist-grade hidden-detail reconstruction by sampling. If no original high-res separate source exists, commission/create artist-level redrawing of the Front with layer underpaint before any claim of final animation.

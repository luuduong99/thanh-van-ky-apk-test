# CP355 — Lâm Thiển: editable vector-authored shoulder underlay study, VISUAL QA FAIL

Date: 2026-10-29. **Actual editable material study completed, but ART NOT ACCEPTED, SPINE/APK BLOCKED.**

## Source-of-truth locks
- User-approved CANON V2.1 `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Shoe-corrected CP348 ten-layer QA archive, SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`.
- CP351 21-layer guide ORA is the base for edited layered format, not a high-resolution approved native art asset.
- **Immutable design:** +17% body proportions already baked into CANON, identity, face, silver hair, white flower, white/blue/gold bodice, both blue shoe toes, five expressions, costume integrity 100/70/50/30.

## Completed material experiment
1. Inspected actual shoulder source close-up (original CP348 figure 215×449). Group `06_left_arm_and_sleeve` remains an approximate polygon with portions of sleeve/fabric/hair, not a clean articulated anatomical layer.
2. Created **three new independently authored SVG Bézier and gradient illustration studies**: `CP355_SKIN_UNDERLAY_EDITABLE.svg`, `CP355_BODICE_UNDERLAY_EDITABLE.svg`, `CP355_HAIR_UNDERLAY_EDITABLE.svg`. Rasterized at 1290×2694 into 3 actual separate RGBA PNG layers. These are manually directed local drawings, **not** missing real source anatomy recovered from pixels.
3. Clipped new study layers to originally fully opaque arm pixels; at rest the composited RGBA stays **exactly equal** to unmodified CP348 source.
4. Inserted them, **all hidden by default**, into the existing real CP351 ORA: `CP355_24_LAYER_EDITABLE_VECTOR_UNDERLAY_STUDY_NOT_RIG.ora` (24 total layers); old merged image byte-identical to CP351. Original 15 CP350 artist slots are preserved.
5. Tested image-left arm rotation around tentative pivot (70,132) in 215×449 source coordinates. **15/15 binary tests PASS** including exact idle image, original ORA merged image, nonempty SVG-raster layers, unchanged feet/blue shoe toes, integrity and release lock.

## Measured lost coverage on same-motion comparisons
| Angle | CP348 arm rotation without patch | With CP355 three art-study layers |
| --- | ---: | ---: |
| -1° | 80 px | 45 px |
| -2° | 157 px | 88 px |
| -3° | 251 px | 149 px |
| -4° | 329 px | 195 px |

These are **coverage-only** metrics. New pixels outside silhouette are not evidence of quality. They do not prove correct anatomy, fabric folds, face/costume fidelity, rig usability or animation smoothness.

## Visual result and release
- A peach/blue seam and local unnatural cut line remain at -2°/-4°; the approved CANON's real hidden anatomy is unavailable in the 215×449 flattened figure. **Visual QA = FAIL.**
- Although the SVG geometry is scalable, the overall enlarged raster is a source-derived prototype, **NOT native high-res artist-grade artwork**. Neither 3 SVG studies nor the 24-layer ORA is an approved production sprite.
- No Spine skeleton, full-body semantic painting, attack animation, hardware APK performance test or user approval of new art has occurred.
- Keep `app/src/main/assets/character_expression_profiles.json`: `production_release.status=blocked_pending_art`, `sprite_paths={}`.

## Files and integrity
- `CP355_24_LAYER_EDITABLE_VECTOR_UNDERLAY_STUDY_NOT_RIG.ora` SHA256 `249763becc26523eba0ae20a0fffdf0f672d5524b79189336bfb017ae0eb9fae`.
- `TVK_LamThien_CP355_Three_SVG_Underlays_VISUAL_FAIL_NOT_RIG.zip`: **17 files**, SHA256 `010d66432940e039edd1248a6789d7246048b07a42f85543e618bbc7872d7136`, ZIP CRC PASS. Contains 3 SVG, 3 painted PNG layers, ORA, before/after, motion GIF, metrics, test results, source and README.
- User Library `/Thanh Van Ky/Development/CP355_Editable_Vector_Underlay_Visual_QA_FAIL/`. Original reference files stay unchanged.

## CP356 next honest production direction
Do not iterate alpha/mesh masks and call them finished art. The real **production bottleneck is authored, independent high-resolution character illustration** that redraws left shoulder, sleeve, bodice and hair with extended underlay behind moving elements. Work from the locked CANON V2.1 to produce a complete Front redraw in semantic layers; compare approved full-body silhouette at idle, plus actual raised-arm/turn poses. Require artist visual acceptance before releasing a sprite; then rig and test on real Android hardware. If this source is unavailable, clearly label any procedural study as provisional.
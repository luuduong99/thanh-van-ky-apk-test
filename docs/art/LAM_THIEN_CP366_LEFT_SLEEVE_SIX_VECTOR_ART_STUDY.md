# CP366 — Lâm Thiển: six newly authored left-sleeve SVG art studies, NOT game-ready

Date: 2026-10-29. **New independently editable vector geometry produced and structural QA passed; Visual QA NOT PASSED, no production art acceptance.**

## Source-of-truth and actual scope
- Approved Lâm Thiển CANON V2.1 remains unchanged, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, sheet 941×1672.
- Source crop rectangle `(13,172,230,630)` → 217×458 Front. 1302×2748 working canvas is exactly 6× aligned to this crop.
- This pass **did not recover a lost layered original, finish full-body painting, or generate a correct fully painted arm-raise keyframe.** Unlike CP365's empty scaffold, however, CP366 has actual nonempty newly authored SVG paths and rendered editable raster layers for one side of the character.
- These parts are hand-authored Bézier/gradient **design studies**, not source-extracted masks or approved artist-grade painted parts. No existing CANON or older asset is overwritten.

## Actual new deliverables
- Six editable vector source files, each with newly drawn paths, gradients, folds or strokes:
  1. `01_rear_hair_lavender.svg` — behind-arm lavender hair strokes.
  2. `02_hidden_bodice_cloth.svg` — occluded blue-white bodice fabric.
  3. `03_hidden_shoulder_skin.svg` — skin/color under the arm.
  4. `04_arm_skin_and_hand.svg` — left upper arm, forearm and hand.
  5. `05_translucent_front_sleeve.svg` — translucent front sleeve with folds.
  6. `06_gold_shoulder_cuff_trim.svg` — gold fittings/cuff.
- Every SVG has a 1302×2748 native-scale RGBA PNG counterpart, plus transparent merged preview.
- `CP366_PARTIAL_SIX_LAYER_SLEEVE_ART_STUDY_NOT_SPINE.ora` is **7-layer OpenRaster**, six visible study layers plus a **hidden** *low-res nearest-neighbor CANON crop used as a reference only*. Each is editable independently. The combined art remains partial, lacks the full body and has non-final surface detail.
- `CP366_SLEEVE_ART_STUDY_SIDE_BY_SIDE.png`: approved CANON exact crop vs new partial vector art vs 45% alignment overlay. **Art visually differs from approved painting**, especially the folds, shoulder trimming and hair overlap.
- `CP366_VECTOR_ARM_TECHNICAL_POSE_QA.png`: isolated *same-view* 0°/-8°/-15° group-rotated arm technical images. Hair/bodice/shoulder underpaint remains fixed behind. The -15° pose does not contain new painter-authored raised-arm folds/anatomy.
- `CP366_VECTOR_ARM_MOTION_QA_ONLY.gif`: 25-frame small-amplitude technical test, **NOT real Spine/rig animation or Android performance measurement**.
- `tools/art/cp366_build_vector_sleeve.py` rebuilds the 6 SVG/PNG art layers/ORA from exact CANON SHA; `tests/art/test_cp366_native_sleeve_study.py`: **5/5 local structural tests PASS** on source lock, actual vector paths, output image alpha, ORA layers/hidden guide and blocked release status. The ORA asset-only test skips in public GitHub CI without private Library artwork.
- Archive `TVK_CP366_Six_Authored_Sleeve_Layers_NOT_GAME_READY.zip` **23 entries**, SHA256 `4952e29a86759b2bab38d62416c74ee66c594b4ff67449b8c9f5adfd1f528295`, CRC PASS. ORA SHA256 `7bddf869a1d0ad73cd705c3f073958db7d51d6b713f9560eac66b4e4ebf7ac90`.
- Persistent Library: `/Thanh Van Ky/Development/CP366_Six_Vector_Sleeve_Art_Study/`.

## Visual QA and release conditions
- **Visual QA = NOT_PASSED.** The current vector folds are more schematic than CANON V2.1; silk, hair and ornaments need substantial refinement and alignment before any approval. This is deliberately a localized arm/sleeve handoff for continued real art work, **not 6 complete mandatory full-body art roles**. The source Front and both blue shoe toes remain reference-only, not newly painted within this ORA.
- CANON (+17% baked-in proportions, silver-lavender hair, white flower, approved face, white/blue/gold costume, both blue shoe toes, five expressions, 100/70/50/30 damage thresholds) remains immutable.
- `app/src/main/assets/character_expression_profiles.json` still has `production_release.status=blocked_pending_art` and `sprite_paths={}`. **No CP366 sprite imported or APK built.** Passing structural tests does not approve art, joints or FPS.

## CP367 specific next work
1. Improve and align the **six actual SVG art pieces** to approved CANON fabric folds, gold filigree and back-hair intersections; ensure occluded skin/cloth extends as needed for movement without rectangular smears.
2. Finish and repaint remaining character semantic parts at native resolution, never by upscaling the 215×449 crop. Maintain head/face, complete bodice, other arm, legs and both blue shoe toes.
3. Create **artist-painted same-angle rest/raised-arm** poses and visual contact sheets. Have user/artist review and accept; only then enable Spine/rig and test target Android runtime FPS. The CP365 technical exporter should be a QA aid, not a substitute for manual keyframes.

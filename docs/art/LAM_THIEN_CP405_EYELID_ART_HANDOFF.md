# Thanh Vân Ký — CP405: Lâm Thiển eyelid paint source-locked review

**Checkpoint date:** 2026-10-30. **TECHNICAL CANDIDATE COMPLETED; VISUAL ART NOT APPROVED.**

## Source (single source of truth)

- Approved `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Exactly cropped `Ngại ngùng` face `(25,684,193,881)` => 168×197 native pixels; LEFT ROI `(29,93,71,124)`, RIGHT ROI `(83,70,129,110)`.
- Historical +17% body scaling is ALREADY integrated into approved art; never add another 17%.

## Substantial work in CP405

1. Created a source-only **editable painting pass** using separate layers for the skin plane, warm upper crease, variable-opacity lash roots, 19 independent tapered lash tips per eye, and inner eye corner. All art is rasterized with 16× subpixel sampling back to the exact CANON-native 168×197 region. These are **programmatic artist-directed strokes, NOT professionally painted hi-resolution source art**.
2. Added a source-lash transfer study: samples eyelash pigment from the **same** approved CANON and locally warps it onto the closed contour; never uses an external face.
3. Compared the approved CANON / CP402 baseline / CP405 new paint and the separate source-lash transfer candidate. **Neither CP405 variant is clearly better** at native size; both remain DRAFT, **do not replace CP402 baseline**.
4. Produced editable `CP405_EYE_ART_8_LAYER_NOT_APPROVED.ora` with the original CANON **sole visible** and all CP405 candidate layers hidden. `mergedimage.png` is the exact unmodified CANON face.
5. Produced 15-slot atlas (2520×197), 72-frame 30 FPS MP4, GIF, reviews and manifest. Source SHA verified. Exactly **0 pixel changed outside both eye ROI**; **1,809** face pixels changed inside. Original RGBA alpha is unchanged. No permission to package in APK.
6. **20/20 local technical tests PASS** including source validation, ROI, alpha, ORA, tamper/release guard, deterministic source-only reconstruction. GitHub public CI has only the static subset, and private-source cases must SKIP.

## Explicitly rejected false artwork

An unrelated automatically generated infographic with **black-haired** female incorrectly asserts "CP405 hoàn thành", real-phone testing and APK integration. **Reject, do not display or use as Lâm Thiển art or a true progress report**. The only valid screenshots are composited pixel-for-pixel from the approved source named above. No off-canon art becomes CANON from passing code tests.

## Remaining completion blocker (not a CI problem)

- Eyelashes/eyelids are still **too thin, flat, and mechanical**, especially in the eye with the sparse dark outline. The approved CANON consists of a design *sheet*, not an original high-resolution facial layer master; the relevant cropped face is only 168×197.
- A real higher-resolution independently redrawn eyelid/skin/lash asset is required for painter-grade appearance. Import only once its identity and visual quality are compared with CANON and **explicitly approved by the user**.
- Rebuild the closed-eye source keyframe, then artist-paint intermediate shapes, rerun smooth blink QA, and finally validate **on a real Android phone**. Existing CP403 Android debug viewer can test legacy CP402 atlas; it has NOT been updated to accept CP405 automatically and should remain so.
- No physical phone test, production rig, Spine or release-quality APK test has been completed. Do not invent an ETA or imply progress by repeating source-preservation tests.

## Release gate

`closed_eye_user_approved=false`; `blink_user_approved=false`; `spine_ready=false`; `apk_tested_on_device=false`; `production_sprite_paths={}`; `release=blocked_pending_painter_and_user_approval`.

## Regenerate from private source

```bash
PYTHONPATH=tools/art python tools/art/cp405_eyelid_paint.py \
  --canon /private/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
  --prev /private/CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png \
  --out /private/CP405_OUTPUT
TVK_CP405_CANON=/private/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
TVK_CP405_PREVIOUS=/private/CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png \
PYTHONPATH=tools/art python -m unittest discover -s tests/art -p test_cp405_eyelid_paint.py -v
```
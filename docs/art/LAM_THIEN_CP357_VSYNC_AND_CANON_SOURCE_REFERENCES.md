# CP357 — Android VSYNC motion, verified APK, CANON V2.1 pose references

Date: 2026-10-29. **Android prototype frame scheduling improved and built; native art remains BLOCKED.**

## Code applied (not just proposed)
- `app/src/main/java/vn/thanhvanky/prototype/TVKCharacterMotionView.kt` now schedules continuous drawing using **`postInvalidateOnAnimation()`** rather than the fixed `postInvalidateDelayed(40L)` (~25 scheduled frame attempts per second). The view is instantiated by `CharacterInteractionActivity.kt` for interactive character portraits.
- Android redraw now follows display VSYNC; this makes 60/90/120 Hz pacing *possible* on supported screens, but **does not prove measured FPS or eliminate dropped frames**. Heavy GPU/CPU art can still stutter, and this remains a bitmap-mesh prototype, not rig/Spine.
- Regression test `tests/art/test_cp357_android_motion_vsync.py` asserts VSYNC scheduling, removal of 40ms delay, retained animation toggle and non-Spine disclaimer.
- CI confirmed **Art QA success**, run [40883917665](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40883917665), and **Android APK build success**, run [40883917655](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40883917655), both at commit `0ae981f5b09d56610550202f8d7d4233f7ca1fe4`.
- Artifact ID `12901233190`, artifact name `thanh-van-ky-debug-apk` extracted from GitHub. ZIP CRC and APK ZIP structure verified locally. Debug APK bytes **8,789,756**, SHA256 **`b7fbcc93aca6bf773b04328cb235e01492317f3cd125fc684fd19cf6fe79eb03`**. Archive of official Actions artifact SHA256 `7203476ccfbfca9c67bbbce9d631a9e6fca32c17bba763ff8deaa6051b9732dd`.
- **No Android device run, FPS capture, visual comparison of game layout or final art QA was performed.** This is a DEBUG build, not a visually approved Lâm Thiển release. Production release gate remains `blocked_pending_art`; do not claim it contains approved V2.1 production sprites.

## Art reference kit (real approved image crop, no counterfeit high-res)
- Original user-approved CANON V2.1 full sheet SHA256 **`f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`**, 941×1672, untouched.
- Added four **pixel-exact original-sheet** PNG crops, audited pixel-for-pixel against CANON:
  - `FRONT` sheet bbox (13,172)–(230,630), **217×458**.
  - `THREE_QUARTER_FRONT_RAISED_HAND` bbox (550,172)–(758,630), **208×458**.
  - `FRONT_SHOULDER` bbox (30,267)–(204,395), **174×128**.
  - `THREE_QUARTER_SHOULDER` bbox (561,263)–(740,408), **179×145**.
- `CP357_CANON_VIEW_CROSS_REFERENCE_QA.png`: a compact anatomical/style reference board, showing standing Front and 3/4 pose with hand raised and detailed shoulders.
- **These are different angles**, not idle and raised-arm frames of an identical camera view. Do **not** crossfade or treat them as a completed animation pair; do **not** upscale to call high-res newly painted art. The existing painted semantic art slots remain 0/6 populated per actual CP356 audit.
- Reference ZIP `TVK_CP357_CANON_SOURCE_REFERENCE_AND_VSYNC_NOT_ART.zip`, 8 entries, CRC PASS, SHA256 **`517d1358f2499aa351d375a989a6a0f829cdd434fcb210bcca46804237992a82`**. The original full CANON file is NOT modified or duplicated inside this small crop kit.
- Archived APK, reference ZIP and QA board at **`/Thanh Van Ky/Development/CP357_Android_VSYNC_Canon_References/`**.

## Remaining mandatory art work (CP358)
Native painter/artist must actually paint the six separately movable and overlapped shoulder sections on a high-resolution canvas:
1. Front sleeve left;
2. left arm skin;
3. hidden shoulder skin;
4. main bodice/cloth;
5. hidden shoulder bodice/cloth;
6. hair back.

Then export **same-view** idle and raised-arm PNG frame pairs (with the **same canvas, pivot and camera**), review against CANON V2.1 including +17% proportions, silver hair, white/blue/gold costume, facial identity and **both blue shoe toes**, and only after human visual QA accept a true rig/Sprite/Spine set. The game must not silently replace missing art with wrong outfits or damage states (100,70,50,30).

Current: `production_release.status=blocked_pending_art`, `sprite_paths={}`. No approved high-resolution painted semantic sprite, no Spine motion acceptance, no measured phone FPS. Debug APK is for testing application logic and VSYNC frame scheduling only.
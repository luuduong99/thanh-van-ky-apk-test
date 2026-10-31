# CP358 — Android motion debug telemetry and honest legacy-art disclosure

Date: 2026-10-29. Status: **code implemented, CI validation in progress at initial documentation; native left-shoulder art NOT completed.**

## Objective and what was actually changed

The original CP358 production priority remains to create six genuinely painted, high-resolution semantic art layers for Lâm Thiển's left shoulder/arm (sleeve, arm skin, hidden shoulder skin, bodice, hidden bodice, rear hair), plus two *same-angle* idle and raised-arm exports. The existing CP355/Cp356 24-layer ORA had **0/6** production-painted roles and no valid animated pose pair. None of the mask, inpaint, vector-study or mesh-warp passes is sufficient. **The current CP358 does not solve this art bottleneck.**

The existing Android debug prototype can nevertheless be improved and measured without claiming art is done:

1. `TVKCharacterMotionView.kt`: record **debug-only canvas callback cadence** over approximately 2-second windows. Logs to `TVKMotion`: `canvas_draw_fps`, count of draw-to-draw intervals over 33 ms, and explicit suffix `debug_only_not_display_fps`. Logging only for a debuggable application while animation is running and the view is shown. Keep CP357 `postInvalidateOnAnimation()` VSYNC scheduling. Frame callback cadence is not GPU presentation FPS and is not a phone benchmark by itself.
2. `CharacterExpressionCatalog.kt`: add `hasRuntimeArtApproval(catalogue, characterId)`, requiring the established strict `approvedSpriteRelease` gate and nonempty registered sprite paths; do **not** mark a flat visual reference or placeholder as runtime-approved.
3. `CharacterInteractionActivity.kt`: when selected character is `lin_qian` and there is no runtime-approved sprite release, clearly show **“ẢNH TEST / LEGACY”** and describe the existing bitmap-mesh as a demo, not CANON V2.1 art or a Spine rig. This avoids user confusing existing `characters/lin_qian.png` debug placeholder with the approved CANON.
4. `tests/art/test_cp358_android_art_safety.py`: five repository tests for telemetry guard, debug-only gate, VSYNC regression, placeholder label and blocked `sprite_paths`.

## Approved source and explicit rejection of drifting visual

- CANON V2.1 remains unchanged, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. Do not reapply +17%; keep identity, silver hair, flower, white/blue/gold costume/bodice, both blue shoe toes, five expressions and damage at 100/70/50/30.
- Available Library/Drive and project files were checked for a reusable genuine native high-resolution separated master; no verified master with six independent painted hidden regions was found during this pass. This does **not** establish that no such master exists anywhere.
- A newly generated *illustrative* CP358 infographic showed **dark hair** inconsistent with CANON and falsely claimed approved art/test completion. It was **REJECTED immediately** and deliberately NOT archived to the project, NOT added to sprites and NOT approved. All progress claims must come from actual GitHub and inspected bytes.

## Device verification (future manual step; not yet performed)

When installing a new debug build on an Android test phone:
```sh
adb logcat -c
adb logcat -s TVKMotion:D
adb shell dumpsys gfxinfo vn.thanhvanky.prototype framestats
```
Use logcat draw cadence to detect long intervals; compare to actual device frame presentation/jank/performance with Android profiling. Do not claim steady 60fps without measurements. When an approved sprite exists, repeat with its actual final high-resolution textures.

## Release gate and exact next art task
- `production_release.status=blocked_pending_art`; `sprite_paths={}`. The debug APK still has existing placeholder assets; the on-screen warning explicitly discloses this.
- **CP359:** create painter-quality new native left shoulder semantic art: separate sleeve, arm skin, hidden shoulder skin, bodice, hidden bodice and rear hair, with actual occluded texture, folds and shading. Export two real keyframes at *identical view, canvas, and pivot*. Run CP356 technical preflight and manual Visual QA against CANON V2.1 before activating a production sprite. When and only when that passes, proceed to full-body rigging, then phone FPS measurement and APK art release.

## GitHub references
- Android view: `app/src/main/java/vn/thanhvanky/prototype/TVKCharacterMotionView.kt`.
- UI label: `app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt`.
- Approval resolver: `app/src/main/java/vn/thanhvanky/prototype/CharacterExpressionCatalog.kt`.
- Tests: `tests/art/test_cp358_android_art_safety.py`.


## CP358 verified APK artifact — 2026-10-29

- [TVK Art QA run 40885894376](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40885894376): **completed/success** at commit `0bf214017c577e7a9be977cbea6a9282283ea214`.
- [Android build run 40885894352](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40885894352): **completed/success** at same code/test commit.
- Actual downloaded GitHub artifact ID `12903065909` ZIP SHA256 `e56ae711c5ce8e0ec2d4460f8627730e030e1c0b46934111d9a18191e82109dd`, artifact CRC pass. Extracted APK `TVK_CP358_Debug.apk`: **8,790,897 bytes**, SHA256 `c172ee04c3882ffa6254902fe3a3fc86d3e22285bd884db6c3c0ffd7897f2869`, APK ZIP CRC pass, 27 entries. Validated compiled `classes3.dex` contains `TVKMotion`, `canvas_draw_fps`, and `ẢNH TEST / LEGACY` strings.
- Stored APK and `TVK_CP358_Debug_Readme.md` in Library folder `/Thanh Van Ky/Development/CP358_Debug_Motion_Cadence_And_Art_Gate/`.
- **This debug APK has NOT been run on physical hardware and has no measured presentation FPS**. The visual CANON V2.1 painted sprite gate remains `blocked_pending_art` and paths empty.

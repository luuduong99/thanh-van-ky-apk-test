# TVK CP419 — Lâm Thiển: cùng pose cho blink + 5 kênh idle (DEBUG)

**Date:** 2026-10-30  
**Status:** TECHNICAL DEBUG; **art review PENDING; production rig not ready**.

## Change delivered

- Before CP419, CP410 moved **208×443 standing** while blinking a **different pose face** in a separate inset; CP417/CP418 blinked the **correct standing pose** but did not deform the body simultaneously. CP419 now uses **the exact same standing source atlas frame** for whole-body mesh and blink at every instant.
- CANON locked: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; crop `(16,180,224,623)` 208×443.
- CP417 five-frame atlas 1040×443, SHA256 `cb6cbe03cb1b9ccd3201e4a6bb6ba0e9cc3225111c4f78d441d7d9d7296d05cb`; frame 0 exactly the same source standing crop and all other changes confined to two eye ROI.
- In `TVKCP417SamePoseBlinkActivity`, a single monotonic `elapsedSeconds()` drives (a) the CP417 2.4s eyelid timing **and** (b) CP410's 20×36 body mesh using five wave channels (breath/head/arms/hair/silk). Each of the five slices is decoded from the **same-pose** CP417 atlas. Toggle CP419 combined mode; retain the CP418 5-frame scrubber and source comparison. Debug-only via `FLAG_DEBUGGABLE`; raw-byte SHA verification of user-selected CANON and atlas; private pixels are never committed or embedded in APK.
- Added dedicated menu button `CP419 | Idle + mắt (DEBUG)` that preselects combined mode after valid image selection.

## What this means and does not mean

**Meaningful integration:** a real Android view can draw the full-body image and blink as a single moving picture rather than two unrelated panes. This aligns source pose and time, and can be debugged on-device.

**Limitations:** this is **single flattened bitmap mesh deformation**, not Spine/Live2D, a painted layered head/hair/neck, or a guarantee of naturally independent hair physics. Source is only 208×443; zooming/display scaling doesn't create HD detail. No artist-quality closed-eye master was added. The source CANON itself remains unchanged. The GIF preview made via OpenCV approximates Android mesh, **not evidence of the device rendering or FPS**.

## QA and release gate

- Public source tests check SHA-pinned loaders, same-pose sprite slices, single timebase for blink+motion, Android Canvas mesh, debug-only UI, unchanged production gate. Private tests verify exact source/atlas hashes, original frame 0, no changes outside eyes.
- Run locally with the exact source: `TVK_CP419_CANON=/path/to/CANON.png TVK_CP419_ATLAS=/path/to/ATLAS.png python -m unittest discover -s tests/art -p 'test_cp419_same_pose_sync.py' -v`.
- `visual_approval=PENDING_USER`; `production_release.status=blocked_pending_art`; `sprite_paths={}`, `spine_ready=false`, `device_tested=false`.

## Next CP420

Prioritize actual high-resolution same-pose face/neck/hair hand-painted master and user visual approval. Do not mislabel new technical animation work as solving the missing art. If no artist master exists, CP420 should focus on obtaining/painting one rather than another mask-only benchmark.
## Verified CI, APK, offline review pack

- [CP419 public test run 41084788314](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41084788314) **SUCCESS: 10 tests discovered, 7 PASS / 3 SKIP** because GitHub public checkout lacks private CANON and atlas. The three image-dependent checks were independently executed with the exact local inputs and PASS.
- [Android build run 41084788184](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41084788184) **SUCCESS**, downloaded artifact ID `12990748098`. APK `TVK_CP419_Android_Debug_Preview.apk`: **8,827,665 bytes**, SHA-256 `0ab6e9b95c5aec405e98a9d581d3244f1e8385976103375c5fae1a28561b0b28`.
- Inspected APK ZIP CRC, DEX includes the CP419 UI flag and mesh function; no CANON/atlas private file in packaged APK assets.
- Private review package `TVK_CP419_Android_SamePose_Sync_Review_Pack.zip`: **18,921,525 bytes**, SHA256 `debf44c213fa7f1c74334c0fdfb0cfc91fa0a4ca62b80deab96dbf5c2b6581fb`, includes APK, CANON, atlas, simulation GIF, MP4, 6-frame image, manifest and instructions. Stored in Library `/Thanh Van Ky/Development/CP419_SamePose_CombinedIdle_Blink_Debug/`.
- Still **NOT validated on a physical Android device**; debug body animation, not artist-approved original rig.

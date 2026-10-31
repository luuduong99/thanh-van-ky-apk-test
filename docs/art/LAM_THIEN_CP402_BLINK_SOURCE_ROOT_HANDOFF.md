# TVK — CP402 / Lâm Thiển, source-root eyelid study + Android debug preview

**2026-10-30 • DRAFT / NOT ART APPROVED / NOT IN PRODUCTION**

## Provenance

- Exact source: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` RGBA 941×1672, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Pixel-exact portrait crop `(25,684,193,881)` 168×197. Only eye ROIs (LEFT 29,93,71,124; RIGHT 83,70,129,110) may be edited; no external source faces or garments.
- Original approved Lâm Thiển CANON, body +17% and outfit locked; new black/silver-hair costume references are not active for Lâm Thiển.

## What CP402 actually does

- Two variants of the **closed-eye study**: `source-root` uses dark source upper-eyelash root colors per x and tapered anti-aliased lashes over original-CANON skin inpainting; `soft-root` is the gentler candidate.
- **Do not claim painter-grade improvement**: at native 168×197 source resolution the retouch remains limited, and any enlargement is resampling; final painter refinement and user approval are still missing.
- Atlas: `CP402_ATLAS_ROOT_DRAFT_15.png` 2520×197 (15 poses, 168×197 each), SHA256 `645738fa932a354e3142e2474eb35011491b091d06451a08c4443e6650529c97`.
- 72-frame source-locked blink sequence, 2.4 seconds / 30 FPS, review-only GIF and MP4. The Python proof checks every frame remains identical to CANON **outside both eyes**, and alpha remains unchanged.
- CP401 source curve lookups were memoized for speed without changing rendered pixels (old vs optimized hashes compared for 5 representative blink poses).
- Android **debug-only** preview component can open the exact pinned CP402 atlas using Android's system file picker, SHA256 and dimensions gate, plus an explicit DRAFT label. It **never auto-registers draft art** and refuses to run in non-debuggable builds. No APK runtime claim without full Gradle build/real Android test.
- Public repository must contain scripts, Kotlin preview, tests, docs, **not the private CANON bitmap or draft atlas**. The exact files are backed up separately in the Library/ZIP.

## Verification

- **19/19 local tests PASS**, 4 static + 10 source-dependent + 5 preview safety tests. In public CI without private source, **9 static PASS / 10 SKIP** expected. Source-dependent SKIP is not approval.
- GitHub debug build and source guards must be checked separately; a successful build proves compilation, not animation quality.

## Remaining gates — CP403, not yet completed

1. Real artist retouch for both eyes and eyelashes to match native CANON linework, compare at native & zoom, receive user's explicit art approval.
2. Review timing / intermediate frames in moving preview; avoid ghosted pupils and jumping skin seams.
3. Only after art sign-off create approved sprite manifest with per-file hashes and wire it to the real Lâm Thiển interaction view; run on actual Android device.

**Never confuse an algorithmically-generated blink proof, technical CI PASS, or debug preview with finished Lâm Thiển artwork in game.**
## Verified GitHub build (2026-10-30)

- [CP402 source preflight](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41035609945): **SUCCESS**; GitHub CI verified **9 PASS / 10 SKIP** without the private CANON bitmap (expected and not art acceptance).
- [Android debug APK build](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41035603978): **SUCCESS** at commit `95e27a85e96119dc02b89c312a5099cf43a60788`; archive artifact ID `12968380860` contains `app-debug.apk`. This proves compilation only; no physical-device rendering benchmark was performed.
- Debug-only review workflow: download/import `CP402_ATLAS_ROOT_DRAFT_15.png` to the Android phone; install the compiled debug APK; open Lâm Thiển interaction screen -> `CP402 | Xem thử chớp mắt (DRAFT)` -> select the atlas using Android file picker. Exact PNG SHA-256 and 2520×197 size are required. Wrong files are rejected. The app contains no CP402 atlas as a built-in production asset.
- Both the real debug APK and its GitHub artifact ZIP were backed up in Library at `/Thanh Van Ky/Development/CP402_SourceRoot_Blink_DebugReview_20261030/`.
- **Status remains:** user visual approval for eyelid/eyelash master = PENDING; Android physical-device testing = NOT VERIFIED; production sprite and full Lâm Thiển runtime blink = BLOCKED.

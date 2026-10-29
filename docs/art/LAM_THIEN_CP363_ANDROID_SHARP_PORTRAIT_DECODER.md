# CP363 — Native-resolution Android portrait decoding (measured source-resolution fix)

Date: 2026-10-29. **Android decoding policy implemented and CI PASS. High-resolution painted art NOT completed.**

## Why this matters
`app/src/main/java/vn/thanhvanky/prototype/CharacterInteractionActivity.kt` previously hardcoded `BitmapFactory.Options.inSampleSize = 2` in **both** the full-picture branch and `leftThird` crop branch. This halves both source dimensions even when the original is very small, destroying details before canvas rendering.

For the **actual CP348 215×449 Lâm Thiển QA sprite**, the forced-downsampled approximation contains ~108×225 pixels before the view scales it back up; after this fix the decoder can retain **all 215×449 source pixels**. For the approved reference sheet 941×1672, the new policy also chooses sample 1. Neither effect invents painted detail or turns a low-res crop into final art.

## Actual code change
- Added `portraitSampleSize(width,height)` selecting a *power-of-two* sample factor, using max side **4096 px** and total decoded area **8,000,000 pixels**, or up to about **32 MB ARGB_8888 image data** per bitmap (not a hard upper bound on total process memory).
- For ordinary image loads, read dimensions with `BitmapFactory.Options.inJustDecodeBounds = true` then reopen the asset and decode pixels at the selected sample factor.
- For `BitmapRegionDecoder` `leftThird` crop, compute factor from the **cropped region dimensions**, not the entire image; retain precise region selection.
- Use `Bitmap.Config.ARGB_8888` and `inScaled=false` for predictable source dimensions and image quality. Both old fixed `inSampleSize=2` code paths removed.
- Release gate/legacy placeholder policy is unchanged: no unapproved Lâm Thiển production artwork. `production_release.status=blocked_pending_art`, `sprite_paths={}`.

## Verified QA
- Added `tests/art/test_cp363_sharp_portrait_decode.py`: source-contract regression tests + numerical policy examples (small images sample=1; huge images bounded to powers of two, full/cropped branch checks, release guard preserved).
- [TVK Art QA 40896372149](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40896372149) **completed/success** at commit `0054be929eb6279dc13317b468009fc3d4427592`.
- [Build Android APK 40896371601](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40896371601) **completed/success** at the same commit.
- Downloaded actual GitHub artifact ID **12908140067**, `thanh-van-ky-debug-apk`. Artifact ZIP SHA256 `ebc1561b4b92e002f8727c14a16497581ae31af63cffeda728c555efa319409e`, CRC PASS. Extracted debug APK **8,792,059 bytes** SHA256 **`430d2be42c5f0c42340fe173e29145338db00a83dec5709a26c1422f68446039`**, ZIP CRC PASS, 27 members.
- Inspected APK `assets/character_expression_profiles.json`: correct active V2.1 ID, `blocked_pending_art`, empty `sprite_paths`.
- `CP363_SOURCE_RESOLUTION_BEFORE_AFTER_QA.png`: **offline simulation using genuine CP348 toe-repaired sprite**, comparing image downsampling to ~108×225 then displaying at 295×616 versus preserving original 215×449 then displaying at same size. **Not a screenshot of Android playback or device-level measured result.**
- APK `TVK_CP363_Debug.apk` available as session artifact and archived with preview to Library `/Thanh Van Ky/Development/CP363_Sharp_Portrait_Decoding/`.

## Limits / next milestone CP364
The fix affects **pixel decoding only**, not the actual quality of painted character parts, alpha edges, animation rigging, high-quality filter choice or stable device FPS. Low-res CP348 remains an unapproved study. CP361's four vector underlays failed manual Visual QA on raised-arm rotation.

The user-approved CANON V2.1 sheet (SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`) and fixed +17% proportions, face, costume, silver hair, accessories and two blue shoe toes remain unchanged.

**CP364**: obtain/create full artist-quality *independently painted native-resolution* Front semantic layers, especially hidden shoulder/arm sleeve/bodice/rear hair. Render genuine same-view idle and raised-arm keyframes; manual visual approval, then rig and device FPS profiling. Do not mistake successful Android build, offline preview or source-decoder sharpness for completed final art.

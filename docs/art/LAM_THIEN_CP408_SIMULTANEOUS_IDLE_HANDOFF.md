# Thanh Vân Ký — CP408 / Lâm Thiển simultaneous whole-body idle (debug prototype)

**Date:** 2026-10-30  
**Status:** TECHNICAL PREVIEW ONLY — 14/14 local test PASS; **NOT ART/ANIMATION APPROVED**.  
**Goal:** Coordinate multiple independent motion channels and demonstrate them on the *same* source-locked standing-body view before the actual skeleton/texture layers are ready.

## Source-of-truth

- **Only** `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941×1672 RGBA); SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- The sheet is not a production sprite. CP408 extracts its **front standing reference** rectangle `(16,180,224,623)` → **208×443 pixels**. This is still only a sheet crop, not true high-resolution original artwork.
- The exact unchanged extracted crop is `OUTPUT/CP408_CANON_FRONT_UNCHANGED_CROP.png`; hash and dimensions are pinned in `OUTPUT/CP408_MANIFEST.json`.
- Body proportion +17% already baked into CANON. Never apply twice. Never substitute a different female portrait when showing the approved Lâm Thiển.

## Actual technical work

- Prototype **five independent phase tracks** active at once: torso breath (3.8 s), head tilt/shift (6.2 s), arms/shoulder sway (5.3 s), loose hair delay (5.7 s), silk/hem sway (4.5 s).
- The body demo is intentionally **one softly deformed bitmap mesh**, NOT segmented parts, actual head-bone rotation, shoulder/hand keyframes, cloth physics, elastic chest art, or a complete Spine/Live2D rig. A one-layer portrait cannot authentically articulate occluded body parts.
- Uses same CANON crop on both sides of a 30 FPS, 5 s comparison movie; generated frames show the subtle collective deformation. Original image remains untouched; no other source art.
- The **eye-blink timing slot is reserved but the eyelid art is NOT present**. CP402/CP407 eyelid drafts are not approved and their face coordinates do not align with the tiny standing-body face. A preliminary auto-painted eye overlay produced obvious stripes and was **rejected**, NOT included in these results.
- **Debug Android viewer only**, launched from Lâm Thiển interaction page, guarded by `FLAG_DEBUGGABLE`, `android:exported=false`, and an Android document picker. Requires the original 941×1672 CANON, verifies *raw file SHA-256 before decode*, rejects wrong/oversized images. Never silently falls back to legacy `lin_qian.png` or bundles the private fullbody image into APK assets. Five controls can toggle channels individually; pause/resume provided.

## Tests and gates

- **14/14 local tests PASS:** 7 public static source/guard checks, 7 exact-private-image checks, including per-channel nonzero deformation, combined-motion difference from each single channel, source hash, pixel-exact extract and output manifest.
- In public GitHub CI without the private image, the expected result is **7 PASS + 7 SKIP**, *not* 14/14. Build/CI status to be recorded after GitHub Actions runs.
- `source_art_approved=true` only applies to *the unchanged CANON sheet*, **not** the animated body artwork.
- `painted_closed_eye_master=false`, `rigged_character_ready=false`, `physical_android_device_tested=false`, `production_sprite_paths={}`.

## Next actual production tasks

1. Recover or paint **high-resolution, fully separable** front figure: head + hair underpaint, face/eyelids, neck, shoulders/arms/hands, torso, waist/hip, legs, silk front/back, jewelry. Preserve the user-approved CANON silhouette and details. Artwork needs to be *re-drawn properly*, not just enlarged.
2. Finish Lâm Thiển closed-eye keyframe and make visually correct blink frames at native render resolution; obtain explicit art approval.
3. Replace debug bitmap mesh with proper bones/deformation zones, layer compositing, depth ordering, occlusion fills and local motion constraints. Support additive breath/head/hand/hair/silk/blink tracks independently and in parallel.
4. Test on Android *physical* device, review compositing, clipping, aliasing, draw cadence and release gate.

**DO NOT** count this as finished whole-body animation or merge debug-only assets into production.

## Verified CI and Android artifact (same checkpoint)

- CP408 public CI: [Run 41055678227](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41055678227) **SUCCESS** (7 public PASS, 7 private-source SKIP); on exact local source **14/14 PASS**.
- CANON manifest CI: **SUCCESS** at the CP408 checkpoint; original pixel SHA unchanged.
- Android debug: [Run 41055670232](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/41055670232) **SUCCESS**, artifact ID `12977125558` (APK `8,806,596` bytes, SHA256 `3790b839e8225057df267325f5216289c536a67a17f9389d54e514a1bfd8aafb`).
- Android APK DEX includes `TVKCombinedIdlePreviewActivity` and `TVKCombinedIdleMotionView`; no private CANON or CP408 preview imagery is embedded in APK assets. Debug viewer requires the original CANON selected by user. **Physical device testing NOT performed**.
- Portable test pack `TVK_CP408_Android_And_Canon_Review.zip` contains exact source CANON, compiled APK, draft video and instructions. Keep it private; do not commit CANON artwork to GitHub.
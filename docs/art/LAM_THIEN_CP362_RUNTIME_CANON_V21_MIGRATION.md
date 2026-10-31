# CP362 — Lâm Thiển runtime CANON V2.1 migration and fail-closed sprite gate

Date: 2026-10-29. **Actual runtime metadata/code correctness fix completed; native painter art NOT completed.**

## What inspection found
- Source-of-truth `docs/art/LAM_THIEN_DESIGN_REGISTRY.json` correctly names latest user-approved `LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29`, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` (941×1672, flat reference, not a rig).
- However `app/src/main/assets/character_expression_profiles.json` still used previous **V2** ID `LT_CANON_BODY_REF_2026-10-28_V2` and SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711` in `canonical_body_visual_id`/`canonical_body_sha256` **and also in `production_release`**. It contained a nested V2.1 reference but consciously retained those legacy release-gate fields. That archival choice creates a future release footgun: an accepted image could be checked against the *wrong* body source if metadata changed without a separate gate.
- The five approved expression **style/direction** references independently remain approved, even though their historical `canonical_body_visual_id` in the expression design document is V2. We do not mutate that historical source; face art must be redrawn to the active V2.1 identity before game use.

## Concrete source changes
1. `app/src/main/assets/character_expression_profiles.json`: migrate both runtime body fields and both production release body fields to **active V2.1 ID/SHA**. Preserve the old pair only in `archived_body_release_metadata`. Update misleading character notes. `production_release.status` remains `blocked_pending_art`; `sprite_paths={}`, `artist_qa_passed=false`, `runtime_qa_passed=false`.
2. `CharacterExpressionCatalog.kt`: `approvedSpriteRelease` refuses Lâm Thiển art unless nested active-reference, character runtime body, and production release body **all match exactly the locked V2.1 ID and SHA**. This is a defensive contract check. It does not approve artwork and does not change any other character's body reference.
3. Update `tests/art/test_cp324_expression_runtime.py`: assert runtime references against **latest active V2.1 registry** instead of the old archived V2 model card, while keeping historical expression direction independent.
4. Add `tests/art/test_cp362_runtime_canon_v21.py` with five tests covering active canon, release contract, historical metadata, blocked art, separate facial direction.

## Art status and original CP362 goal
The CP361 real editable ORA and original CANON were reopened. The four new shapes cover small hidden shoulder studies, but the rest of the 1290×2694 canvas still scales the **215×449 raster**, not an independently painted high-res figure. Visual art remained FAIL in CP361. No fully authored, same-camera idle/arm-raise source, six complete painter-authored parts, Spine rig or physical Android performance recording was obtained in this turn. **The native high-resolution painter-art milestone is NOT DONE.** We deliberately didn't use a new freely generated lookalike as an approved Lâm Thiển source: character facial identity, silver-lavender hair, white/blue/gold costume, body proportion +17% already integrated, both blue shoe toes, five expressions and damage levels 100/70/50/30 remain locked.

## Acceptance gate
- Runtime contract correct != actual production sprites exist. `production_release.status=blocked_pending_art` and `sprite_paths={}` remain untouched.
- For CP363: author an artist-quality high-resolution independent front figure including hidden layers beneath shoulders, upper arm/sleeve, bodice and rear hair; export **same-camera/same-canvas/same-pivot idle and deliberate arm-raise frames**; compare against active V2.1 portrait and two shoe toes; manual visual approval required before importing rig/Spine and testing on Android.
- CI results, once obtained, must be appended separately; do not mark as pass before observing workflow conclusions.


## Additional CP362 runtime leak fixed

A second, distinct fallback risk was found in `CharacterInteractionActivity.kt`: even when expression sprite resolution refused unapproved art, the **neutral pose** could still use `CharacterAppearanceState.resolveArt(...).path` and display a legacy placeholder bitmap, merely labelled `ẢNH TEST / LEGACY`. CP362 now uses `safeHeroineImage` for both normal and bed portrait layouts:

- **Debuggable APK:** may show existing legacy illustration for development, with explicit banner.
- **Non-debuggable/release APK:** if `lin_qian` has no approved runtime sprite release, passes empty asset path and renders the no-image placeholder instead. It must NOT silently display a wrong V2 model.
- Other characters unaffected; all established expression/pose/damage fallback protections remain in place.
- `tests/art/test_cp362_runtime_canon_v21.py` now also checks both portrait branches and this release-build guard. This is source/metadata-level regression; **physical device screenshots and measured FPS remain untested**.

This ensures the active V2.1 body reference is enforced at *both* sprite-release metadata and actual portrait display paths. It does not create any approved artwork.


## Verified CI and APK artifact

- [TVK Art QA run 40893899956](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40893899956) **completed/success** at `c7a0a31080ad91a0cd6ea679f080a54377ac67b3`; tests were updated for the new `hasApprovedLamThienSprite` variable and V2/V2.1 historical distinction.
- [Android APK build run 40893908748](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40893908748) **completed/success** at code commit `911cd9f22921cce07f24b95b0bfea2db704464c4`.
- GitHub artifact ID `12905118427`, name `thanh-van-ky-debug-apk`: downloaded artifact ZIP CRC PASS and extracted `TVK_CP362_Debug.apk` CRC PASS, 27 entries, **8,791,461 bytes**, SHA256 `2ee780ed142fb60d1f2cea720fdebd5ec9a033980290a12f6ea21f0f5115dce0`.
- Inspected actual packaged `assets/character_expression_profiles.json`: active V2.1 ID/SHA correct, release stays `blocked_pending_art` and sprite paths empty. Compiled DEX contains V2.1 SHA, `ẢNH TEST / LEGACY`, and safe portrait path.
- User Library: `/Thanh Van Ky/Development/CP362_Runtime_CANON_V2_1_Migration/` with verified APK and release notes. No physical device installation or measured 60 FPS.


## CP362 final fail-closed partial-release safeguard (supersedes earlier debug APK)

- Further inspected the neutral-pose fallback: even if a single expression sprite eventually gained release approval, old neutral or unrelated pose artwork from `resolveArt` must **never** appear in a release build. `CharacterInteractionActivity.kt` now uses `expressionArt.orEmpty()` for **all nondebug Lâm Thiển** displays, and `heroineImage` only for tagged debugging. This is intentionally restrictive until a separately approved neutral-state sprite resolver exists.
- `tests/art/test_cp362_runtime_canon_v21.py` checks this safe selection across both normal and bed portraits; CP358's earlier legacy-banner regression test was updated for the factored `hasApprovedLamThienSprite` variable.
- **Final verified CI:** [Art QA 40894537812](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40894537812) **SUCCESS** and [Android build 40894537829](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40894537829) **SUCCESS**, at `45369552696610a62322846f54ac7586aa9495e4`.
- **Superseding final debug APK:** GitHub artifact `12906906193`, `TVK_CP362_Debug_Final.apk`, **8,791,463 bytes**, SHA256 `09c0ed2599b8ccd1aeed348a748100deb80ad65d6c06da62556774127596f26a`, ZIP CRC PASS. Inspected packaged assets: V2.1 ID and hash, `blocked_pending_art`, `sprite_paths={}`; DEX retains V2.1 contract and legacy-debug banner. Uploaded as `TVK_CP362_Debug.apk` into the CP362 Library folder, overwriting the previous CP362 draft debug APK; final notes also saved.
- **Still not production art:** Native high-resolution Lâm Thiển shoulder paint and Spine rig not approved. No device performance measurement.

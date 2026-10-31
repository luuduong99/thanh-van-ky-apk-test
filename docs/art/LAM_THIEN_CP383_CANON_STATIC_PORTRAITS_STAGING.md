# Thanh Vân Ký — CP383: Approved CANON portrait still-image staging (2026-10-30)

**Scope:** Lâm Thiển source-accurate *static* dialogue portraits and proof-of-display. **Not an artist-painted new face, not a new animation, not imported into Android, and not approved for release.**

## Exact identity authority

- Source: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` — 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- The five portrait crops are taken from the **same exact approved CANON** at `[22,681,196,884]`, `[203,681,377,884]`, `[382,681,556,884]`, `[561,681,737,884]` and `[744,681,918,884]`. Original 174×203 px (four) and 176×203 px (one).
- No images searched from the web, no images of different characters, no CP379/CP380 vector art substituted in character UI.

## New deliverables

1. `OUTPUT/portraits/*_CANON_EXACT.png` — five source pixel-exact full expression crops, not redrawn.
2. `OUTPUT/portraits/*_INNER_CROP_SOURCE_ONLY.png` — five direct inner pixel crops that omit a 3px border from all sides for a framed UI; no RGB edits or upscaling in source files.
3. `OUTPUT/PORTRAIT_ATLAS_EXACT_SOURCE_ONLY.png` — 984×235 RGBA atlas with five source pixel-exact crops separated by 16px transparent padding; `OUTPUT/CP383_SOURCE_PORTRAIT_MANIFEST.json` contains atlas positions, original CANON bounding boxes, source pixel sizes and blocked status.
4. `OUTPUT/qa/CP383_CANON_ONLY_PORTRAIT_PREVIEW.png` and `OUTPUT/qa/CP383_LANDSCAPE_DIALOGUE_CANON_STATIC_PREVIEW.png` — two **illustrative static** preview boards. The only character illustrations in them are derived from the exact approved CANON. The dark UI frame/background is not a screenshot of a running APK.
5. Generator `cp383_canon_portrait_staging.py`, tests, source-absent/public static test log and local test log. Source CANON copied byte-for-byte in OUTPUT.

## Validation

- **9/9 local tests PASS** with exact CANON bytes; every extracted portrait, inner crop and atlas rectangle equals the corresponding exact source pixel region.
- Invalid CANON hash fails *before* output-directory creation.
- Reproduced GitHub-public/source-absent test mode: **3 PASS / 6 SKIP**; source-art CI cannot certify portrait pixels if private source absent.
- In a dialogue UI, a framed source crop can preserve the approved face's identity. But source images include their original sheet background and **have no semantic hair/skin/eye/mouth rig separation**.

## Explicit production gate

- `visual_qa`: `SOURCE_FIDELITY_PASSED_ART_REBUILD_PENDING` means **identity provenance has passed only**. It is **not** a claim that new art looks good or has been approved.
- `production_release`: `blocked_pending_art`; `sprite_paths`: `{}`; `rig_or_spine_ready`: `false`; `apk_ready`: `false`.
- Nothing was copied into `app/src/main/assets` or wired into running gameplay. This is an isolated staging package, not an APK build.
- A 174/176×203 source image will not magically become painter-grade HD by display resizing, and a static panel portrait does not resolve blinking, mouth animation, sleeves or battle sprites.

## CP384 actual next work

Create an **independently painted, high-detail face master** based only on the five higher-information approved expression crops, preserving facial identity, silver hair, ornamental flowers and blue/gold details. Separately paint semantic eye/brow/eyelid, lips, skin underpaint, bangs and accessory layers. Compare next to CANON and obtain visual acceptance before expanding to expressions and full-body Spine/Android. Do not use low-fidelity vector substitutes in user-facing game art.
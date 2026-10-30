# Thanh Vân Ký — CP391: CANON-only eyelid painting study (2026-10-30)

**Status: ART DRAFT / VISUAL QA NOT PASSED / NO APK.**

## Source lock

- Approved character: **Lâm Thiển**, **CANON V2.1**, **+17%** body ratio. Do not substitute artwork from other characters or unverified generated illustrations.
- Exact source image: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941×1672 RGBA), SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Original expression crop: `Ngại ngùng` at `(25,684,193,881)`, **168×197 original pixels**. Enlarged displays do not add detail.
- Base draft: CP390 closed-eye source-derived **NOT APPROVED** image; its art quality has not been certified.

## Actual new work

- Create 6 independent, alpha-transparent painted **native-resolution** overlays for eyes (left/right): eyelid shadow, crease, tapered lash shapes.
- Preserve exact CANON pixels at the **open-eye** frame and as the only visible layer in the ORA.
- Create 9-layer ORA: visible CANON; hidden historical CP390, 6 new hidden art layers, hidden CP391 closed-eye composite. All images in comparison are exact CANON and derivative CP390/CP391 on the **same person**.
- Candidate differs from CP390 in **1,113 pixels**; differs from CANON only in eye-region ROIs. This count is **not an aesthetic quality score**.
- Both canvas and painted overlays stay at native 168×197 resolution. These layers are *not* rig-quality master assets or an APK.
- A separate illustrative infographic generation was **excluded** because it redrew the character and contained unverified claims about test results. Never use it as CP391 reference, validation evidence or in-game art.

## Verified QA

- **10/10 local tests PASS** on exact private source and CP390 base.
- **3 PASS / 7 SKIP** in simulated public repository checkout without private source images. GitHub Actions can only verify the static contracts unless private test assets are deliberately and safely mounted.
- Original CANON byte-exact, hash locked; wrong source rejected **before writing files**.
- New art is confined to ROIs LEFT `(31,94,70,124)` and RIGHT `(84,70,130,107)`. **0 pixels** changed outside those ROIs.
- ORA 9 layers, 1 visible, mergedimage matches CANON exactly; ZIP CRC validates.
- `visual_qa=NOT_PASSED`, `production_release.status=blocked_pending_art`, `sprite_paths={}`. No change to Android assets.

## Artistic issues / next CP392

- The additional lash taper, crease and shadow are **a draft**; eyelid interior skin is still too simplified compared with CANON.
- The closed-eye sprite requires proper painted skin / eye shading and hair overlap, plus real visual approval before building blink in-between frames.
- Keep asset staging separate from `app/src/main/assets`, and never replace the approved source without explicit approval.
- After visual acceptance: build independent eye poses, inspect on-device at real output scale, then move to full-body animation/Spine and APK integration.

**Code:** `cp391_eyelid_paint_pass.py` 
**Test:** `test_cp391_eyelid_paint_pass.py` 
**Preview:** `OUTPUT/qa/CP391_CANON_CP390_CP391_ACTUAL_SOURCE_COMPARE.png`
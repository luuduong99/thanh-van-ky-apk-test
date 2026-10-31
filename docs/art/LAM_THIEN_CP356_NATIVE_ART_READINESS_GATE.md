# CP356 — Native art intake gate (actual CP355 source audited, release blocked)

Date: 2026-10-29. **Technical QA tooling completed; new native high-resolution painted art NOT completed.**

## Why CP356 did not accept CP355 as native art

The **actual** CP355 OpenRaster `CP355_24_LAYER_EDITABLE_VECTOR_UNDERLAY_STUDY_NOT_RIG.ora` was reopened and its raster-layer alpha inspected, not judged by filename alone. This confirmed:
- CANON V2.1 reference PNG SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`: verified, unmodified.
- CP355 ORA: valid canvas **1290×2694**, **24** layers.
- All **15 production painter layers in the CP350/CP351 template are still empty**. In particular **0/6 mandatory left shoulder/front roles** contain painted pixels: sleeve, left arm skin, hidden shoulder skin, bodice main, hidden shoulder bodice, back hair.
- CP355 also includes **three real but unapproved hidden experimental vector study layers**, NOT a finished semantic body/arm painting. Those do not count toward the six required roles.
- No separately drawn high-resolution `idle` and `arm_raise` pose exports were submitted for true-motion QA.
- Hence actual-source preflight **BLOCKED**, process exit code **2**, release remains `blocked_pending_art`. This is a *correct rejection*, not a failed unit test.

## New functioning code and real outputs

- [CP356 native-art preflight](../../tools/art/cp356_native_art_preflight.py) (`tools/art/cp356_native_art_preflight.py`) validates reference SHA, ORA integrity, canvas resolution, six required independently named raster layers, missing/empty/one-pixel placeholder content and two distinct full-resolution pose exports. It generates JSON with exact failure reasons.
- [Unit tests](../../tests/art/test_cp356_native_art_preflight.py) provide **6/6 local PASS** on synthetic fixtures. Tests run via existing `.github/workflows/art-qa.yml` path matching tools/art/** and tests/art/**. **Passing validator tests never approves production art.**
- Actual-source report: `CP356_REAL_CP355_PREFLIGHT.json`, `technical_status: BLOCKED`, `semantic_roles_populated: 0/6`, 3 study layers and missing pose pair.
- Image `CP356_LAYER_READINESS_QA.png`: locked CANON sheet alongside CP355 ORA composite and six red empty mandatory-layer indicators.
- Bundle `TVK_LamThien_CP356_Art_Readiness_GATE_NOT_ART.zip`: preflight script, unit tests, actual-source JSON, QA image, manifest and instructions. SHA256 `a17b66735cbafd13680dbb6c9f014fb10e3543e4bf1b1ce57e682ab584bf1910`; ZIP CRC PASS.
- Library destination `/Thanh Van Ky/Development/CP356_Native_Art_Readiness_Gate/`.

## Mandatory manual QA after structural intake

Even when a *future* real art ORA has six nonempty roles plus high-resolution idle/arm_raise images, preflight will return at best `READY_FOR_HUMAN_VISUAL_REVIEW` with `visual_qa=NOT_PASSED` and `runtime_approved=false`. An artist/user must then compare against the full CANON V2.1 for silhouette, +17% proportions, facial identity, white–blue–gold costume/bodice, silver hair, adornments, both blue shoe toes, expression set and damage thresholds 100/70/50/30. Motion QA must inspect folds, sleeve overlaps and hidden anatomy without smears or alpha holes. Android frame pacing and FPS must be **measured** before a runtime release.

**No new approved sprite or Spine rig was created at CP356. No APK was built or declared production-ready.**
Do not update `app/src/main/assets/character_expression_profiles.json` `sprite_paths={}` or `production_release.status=blocked_pending_art` based on this checkpoint.

## CP357 precise next action

Produce the genuine native painted left-arm/shoulder asset rather than another low-resolution mask/mesh trial. On separate semantic layers paint **left sleeve, upper arm and hidden skin, main bodice and hidden cloth, back hair** using the user-approved CANON V2.1. Create actual idle + raised-arm native-resolution composite exports. Run `python tools/art/cp356_native_art_preflight.py --ora <file.ora> --canon <canon.png> --idle <idle.png> --arm-raise <raised.png>`; then have art visually reviewed. Only afterward rig and test APK.

## CP356 CI reconciliation — 2026-10-29

The **six new CP356 tests all passed** in the earlier failed global Art QA workflow. That workflow's failure was due to two pre-existing CairoSVG imports without installed dependency and three legacy V2-era registry/validator assertions incompatible with the already-approved V2.1 active reference. We added the CairoSVG Python dependency in `.github/workflows/art-qa.yml`, synchronized `docs/art/LAM_THIEN_DESIGN_REGISTRY.json` active fields to immutable V2.1 (historical V2 preserved in archive), and made `tools/validate_lam_thien_expression_approval.py` verify the active V2.1 hash while continuing to protect the old V2 archive. These were **metadata/tooling repairs only**, not new art approval.

Latest [Art QA workflow run](https://github.com/luuduong99/thanh-van-ky-apk-test/actions/runs/40881142488) **completed SUCCESS** on `0ad726bda97954ebd0959d93d3cac5304112fe4d`. The CP356 actual-asset preflight remains **BLOCKED** for 0/6 painted shoulder layers and no approved pose pair; CI green does not mean character sprite ready.

# CP351 — QA-guided 21-layer OpenRaster for Lâm Thiển shoulder repaint

Date: 2026-10-29. **EDITOR SCAFFOLD COMPLETE, REAL PAINTED ART NOT COMPLETE.**

## Reusable verified inputs
- CANON V2.1 user-approved: SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- CP348 source cutout 215×449, repaired blue shoe toes: ZIP SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`.
- CP350 artist scaffold archive: SHA256 `13327791e4254b451543022f83abad66aaee05c23ef2066d930319dadb24c941`; canvas 1290×2694. Uses upscaled CP348 reference as a guide, NOT native high-res artwork.
- CP349 experimental backing reduced image-left arm lost coverage 914→263 px but was visually rejected: unnatural vertical seam. Additional CP350-style Navier–Stokes inpaint trial showed **the same 263 px remaining**, a different smear and still visual QA FAIL. Procedural texture fill is not painted hidden anatomy.

## Actual CP351 deliverable
The **real CP350 OpenRaster** was loaded and augmented (no reference image regeneration) to create `CP351_CANON_V2_1_JOINT_QA_GUIDED_21_LAYER_NOT_ART.ora`.

- Existing **17 raster layers preserved**: 15 originally empty named artist-paint layers, one shoulder guide and one low-resolution reference.
- Added **four real RGBA guide layers, all hidden by default**, resulting in **21-layer ORA**:
  - `18__GUIDE_QA_LOST_COVERAGE_914_HIDE` red missing-alpha map after image-left arm shift (-10,+5).
  - `19__GUIDE_QA_REMAINING_GAPS_263_HIDE` amber map of unresolved alpha after CP349 procedural backing.
  - `20__GUIDE_BOTH_BLUE_SHOES_CHECK_HIDE` toe alpha/color review rectangle, to catch recurrence of CP347 toe-mask error.
  - `21__GUIDE_APPROX_SHOULDER_PIVOT_HIDE` green guide at (70,132) on the **215×449 low-res cutout** (scaled to native scaffold), approximate only—not an approved rig pivot.
- ZIP CRC, 21-layer XML, 4 hidden guide layers, 15 **still entirely transparent** paint layers and merged image **bitwise identical to the CP350 original** all PASS.
- Preview `CP351_ORA_GUIDES_SHOULDER_QA.png` displays actual reference, 914-px alpha delta and 263-px residual, no fabricated art.
- ORA SHA256 `511c495302057daad9f8538a84cc74fe60ca90f84ef400b7ffbcbd38d230ab79`.
- Source+code+ORA+preview+manifest ZIP SHA256 `49e0f43927e4490194edb14ce80753ddf5db309a1eb251bedb09dcca5717a2ef`.
- Archived to Library `/Thanh Van Ky/Development/CP351_Shoulder_QA_Guided_ORA/`.

## Strict release status
**Production art NOT DONE.** The 15 paint layers are still empty; this artifact is an improved editable handoff with QA overlays. No genuine independently drawn hidden skin, bodice, sleeve, or back hair; no acceptable two-pose motion, Spine rig, or APK measurement. `production_release.status=blocked_pending_art`, `sprite_paths={}`.

## CP352 next
Open `CP351_CANON_V2_1_JOINT_QA_GUIDED_21_LAYER_NOT_ART.ora` in Krita; on the actual blank semantic paint layers, paint shoulder/upper arm skin underlay, inner bodice/cloth, and hair overlap matching CANON V2.1 (head, figure +17%, costume, and both blue shoe toes unchanged). Show the user's approved reference alongside idle plus small arm-lift renders. Validate natural shading, no rectangular smear, no clipping or alpha hole in motion. **Only visual QA PASS with actual native art** can unblock rigging.
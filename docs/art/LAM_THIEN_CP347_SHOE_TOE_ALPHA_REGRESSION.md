# CP347 — Lâm Thiển: blue shoe toe hidden by alpha mask (user-reported regression)

Date: 2026-10-29. Status: **BUG CONFIRMED; isolated alpha restoration QA PASS; painter-quality art / rig / APK NOT READY**.

## Finding
- User observed that the **front foot on image-left** appeared only with gold ornament while the opposite shoe retained a blue toe in CP346 visual QA.
- Cross-check the **approved CANON V2.1** poster SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`: **both shoe toes are blue** in the approved Front.
- The blue pixels are still present in **RGB** of the 215×449 crop but wrongly **zeroed by its alpha mask**. Source `FRONT_CP341_REFINED_SINGLE_FOREGROUND_NOT_RIG.png` already exhibits the missing toe; CP342's floor-shadow alpha cleanup carried the error to CP343/CP346. **Not caused by shoulder motion QA or an intended asymmetrical costume.**
- A production APK using these CP343/CP346 pixels directly would render the toe missing. The production sprite gate is presently **blocked**, and no tested Android build with this sprite exists.

## Experimental restoration (NOT production)
- Input `FRONT_CP342_FLOOR_CLEAN_ALPHA_NOT_RIG.png` SHA256 `d1f8ab09f517d484d93c7356270338c040c399b9a715c30624c6cefd2d635890`.
- Apply an anti-aliased **restricted alpha mask only** to left/front shoe toe ROI, `x=84..115, y=433..448`, preserving every **RGB pixel exactly**.
- QA facts: **416 pixel alpha values** changed; **299 pixels** newly pass alpha>128. Source and output keep 215×449. All alpha outside the ROI (including opposite shoe) unchanged. Deterministic reproduction byte-for-byte PASS; ZIP CRC PASS.
- User-visible visual proof: `TVK_CP347_Shoe_Toe_Alpha_Before_After_QA.png` shows **CANON / CP342 mask bug / corrected candidate**. Candidate visibly recovers blue toe with the existing source pixels.
- QA ZIP: `TVK_CP347_Shoe_Alpha_Recovery_QA_ONLY.zip` stored at Library `/Thanh Van Ky/Development/CP347_Shoe_Toe_Alpha_Recovery_QA/` with PNG preview, alpha-only candidate, standalone deterministic patch script and hash manifest.

## Follow-up gates
1. **Review candidate foot close-up against original CANON V2.1** for alignment, silhouette, soft edge/halo, and shadow removal. This QA cutout is a low-res *proof of recoverability*, not a high-res native sprite.
2. In actual high-resolution Front redraw, **both blue toes must be present** in rest pose. Add a bilateral shoe visibility QA test for every animation/damage state; do not hide silhouette by applying a global floor-removal mask.
3. Repair semantic 2D layers/underpaint on shoulder/arm as separately required by CP346; after rig creation verify shoes and ankles stay attached, draw order correct, no truncation on Android.
4. Retain `production_release.status=blocked_pending_art`, `sprite_paths={}` until artist QA, animation and APK tests pass.

**Canon body and costume +17%, hair, bodice, five expressions and four damage levels remain unchanged.** This is a **repair of erroneous transparency**, not a redesign.
# Thanh Vân Ký — CP393 Lâm Thiển closed-eyelid study (2026-10-30)

## Status: DRAFT / VISUAL QA NOT PASSED / NO GAME RELEASE

This checkpoint does **not** claim to have completed painter-quality closed eyelids, final animation, a Spine rig, or a tested Android APK. The eye-open character stays exactly identical to the user-approved CANON.

## Source and identity

- Approved source: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, RGBA 941×1672.
- SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a` (exact bytes preserved in archive).
- Working expression: `Ngại ngùng`, pixel-exact source crop `(25,684,193,881)` at native **168×197**.
- Only real source Lâm Thiển pixels and manually keyed curves/sampled skin from *the same approved portrait* are used. The separately liked illustrative style image for Tô Nguyệt Ly is not used here.

## What was actually created

- Two independently adjustable candidate composites: **full closed draft** and **soft closed draft**. The original CP392 near-closed candidate is included as a comparison but not promoted.
- Six new RGBA art layers, independent for both eyes: left/right `SKIN` (masked CANON cheek sampled underpainting), `SHADOW` (blurred crease and lash-root shadows), and `LASH` (anti-aliased hand-keyed strokes).
- `CP393_CANON_AND_6_EDITABLE_EYELID_PAINT_LAYERS_NOT_APPROVED.ora` has **9 layers**: approved original visible, six art study layers hidden, two candidate composites hidden. Its `mergedimage.png` matches the approved 168×197 crop pixel-exactly.
- Both candidates preserve RGB/alpha **outside the eye regions**; `CP393_REPORT.json` records `0` changed pixels outside the mask. Within the two eye regions 1659 pixels (full) and 1143 pixels (soft) differ from the open-eye source. These are technical bounds, **not similarity or aesthetic scores**.
- A side-by-side review image is produced exclusively from original CANON, original CP392, and CP393 derivatives. Native 168×197 source is not made sharper by scaling up.

## Review — why not approved

- CP393 replaces visible iris/eye-white areas in a more complete way than CP392, but the lower-lid transition can still look flat, the lash shapes are somewhat stiff, and skin shading is not yet a true hand-painted hidden-skin master.
- Some eyebrow/hairline overlap may need hand correction. The closed-eye image must be approved visually against the actual source at both native and magnified sizes.
- No automatic import to `app/src/main/assets`. Release metadata remains `blocked_pending_art`, `sprite_paths={}`.

## Verification

`python -m unittest -v test_cp393_closed_eye_master_study.py`

- Exact private CANON available: **10/10 PASS** (4 public/static + 6 source-dependent).
- Public GitHub checkout without private sources: **4 PASS / 6 SKIP**. CI green is not visual approval.
- Wrong source SHA fails before an output directory is created. ORA ZIP CRC, 9-layer visibility, pixel-exact merged image, source crop equality and outside-eye mask are checked.

## CP394 next

Stop creating more automatically sampled cheek patches. Produce a manually painted, higher-fidelity closed-eye master for ONE expression, with approved eyelid/skin/lashes and proper underpaint; review next to exact Lâm Thiển CANON. After user approval, paint actual intermediate blink keyframes, then proceed to the remaining four expressions, full-body art, rig, and Android build.
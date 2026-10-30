# Thanh Vân Ký — CP381 | Lâm Thiển CANON identity fidelity and painting handoff

**Date:** 2026-10-30. **Status: reference and editable workspace delivered; actual new painted art NOT produced.**

## Authoritative image policy

- **ONLY** the exact user-approved `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941 × 1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`) and clearly labeled Lâm Thiển drafts derived from it may appear in previews.
- The CANON retains +17% body proportions, approved white/blue/gold outfit and accessories, five expressions, four clothing-integrity levels, and both blue shoe tips. None is being replaced or silently redesigned.
- The exact Front crop remains **217 × 458 native pixels**. The 1302 × 2748 canvas is a **pixel-enlarged painting reference grid**, not a native high-detail painting.

## Actual CP381 work

1. Reopened real CP380 source (`29` editable draft art layers) and exact CANON. Compared source-aligned small Front against the rejected full-body draft; no scoring threshold has been treated as sufficient for visual approval.
2. Prepared **3 registered identity work areas**, in original 217 × 458 Front coordinates: face `(84,39,139,92)`, hair/headpieces `(65,7,157,119)`, neck/bodice/waist `(67,90,153,204)`.
3. Extracted **5 larger exact-pixel facial-expression reference crops from the same CANON sheet**, plus **8 exact-pixel accessory detail crops** (eye, flower, ear, collar, bodice jewel, back bow, tassel and ornament). These source crops are more useful as a painting model than the tiny Full-Front face and are *not generated artwork*.
4. Built `CP381_FACE_HAIR_BODICE_PAINTING_WORKSPACE_NOT_ART.ora`, with **8 total layers**: three intentionally **EMPTY** editable painting layers, three hidden region markers, one hidden rejected CP380 draft and the enlarged exact CANON Front guide visible at bottom. Combined image is the CANON guide; do not mistake this editable scaffold for art creation.
5. Made two QA boards: `CP381_CANON_FACE_HAIR_BODICE_REVIEW.png` (CANON crop vs unapproved CP380 at exact registered coordinates), `CP381_EXACT_CANON_EXPRESSION_AND_ACCESSORY_REFERENCES.png` (ONLY CANON direct crops, never a substitute character).
6. Source-locked script refuses wrong CANON bytes and malformed CP380 draft **before writing any output**. 9/9 local tests PASS; test on public source-only layout 3 PASS / 6 SKIP as private art isn't stored on GitHub.

## Technical comparison, NOT artistic acceptance scores

| Region | RGB absolute error average, 0–255 | Single-scale structural similarity |
|---|---:|---:|
| Face | 44.04 | 0.0397 |
| Hair + headpieces | 38.57 | 0.1459 |
| Neck, bodice, waist | 50.00 | 0.0849 |

These values compare images registered by Front coordinates; they also capture sheet-resolution limitations and background differences. They **are not a calibrated likeness metric** and should not become automatic painting thresholds. Visual reviewer must check proportions, eye shape, lips, bangs, flower/tassels, cut and folds of clothing, gold filigree, skin shading and source-consistent character identity.

## Mandatory release status

- `visual_qa=NOT_PASSED`
- `production_release.status=blocked_pending_art`
- `sprite_paths={}`
- `painting_layers_have_artist_pixels=false`, `native_fullbody_painting_complete=false`, `rig_ready=false`, `apk_ready=false`
- CP380 remains an unapproved color-blocking draft. No actual new high-resolution art, Spine skeleton or APK was produced in CP381.

## CP382: highest-value next production task

**Artist-painted Face identity FIRST**, using the 5 exact CANON expression crops and 8 exact accessory references as authority, keeping the initial Front face contour and face-to-body scale. Deliver a newly hand-painted face/eye/brow/lips and bangs/jewelry overlay on real semantic layers, not a copied-and-enlarged CANON face. Include an actual portrait close-up compare (CANON vs new draft) and obtain user acceptance before changing the game; then paint hair and bodice with appropriate hidden edges. Do not count empty painting layers or a green CI build as art approved.
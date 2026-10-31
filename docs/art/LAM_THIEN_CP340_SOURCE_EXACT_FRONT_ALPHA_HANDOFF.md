# CP340 — Lâm Thiển CANON V2.1 | Exact-source extraction and Front alpha R&D

**Date:** 2026-10-29  
**Active user-approved visual:** `LT_CANON_V2_1_FINAL_USER_APPROVED_2026_10_29`.  
**Immutable original SHA256:** `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. Image **941×1672 RGBA, 9:16**.

## Verified actual progress

1. Verified original PNG bytes against the approved hash, not old CP337/CP338/CP339.
2. Cut **14 native pixel-exact references**, no new model design and no invented high-resolution pixels: 5 angles, 5 facial expressions, and 4 damage levels. Source bbox and PNG hashes in [manifest](LAM_THIEN_CP340_ALPHA_TRIAL_MANIFEST.json).
3. Made a **real native 215×449 Front foreground RGBA trial**, by applying an OpenCV GrabCut-derived alpha mask to the exact source crop. Color/RGB pixels are **unchanged from the source**. It is only one flattened raster foreground, **NOT a clean Spine-ready sprite**. Light hair, sheer sleeves and drapes remain problematic, need redraw/mask refinement.
4. Created **2-layer editable OpenRaster**: `FRONT_GRABCUT_ALPHA_TRIAL_NOT_RIGGED` visible; `ORIGINAL_FLAT_CROP_REFERENCE_ONLY` hidden. No semantic separation of face, eyes, hair, garment or limb underpainting exists. Do not treat OpenRaster layer-count as completed game assets.
5. Generated side-by-side and full QA previews; four garment-damage reference crops remain **exactly** those approved at stages 100/70/50/30. Do not enhance or exaggerate scuffs, dirt, tears, or chest/outfit coverage at 30%.
6. Local **9/9 actual binary tests PASS**, checking original SHA, 14 exact source pixels, native sizes, Front RGBA pixel fidelity & real alpha, OpenRaster ZIP/CRC/stack/composite, and production-blocking flags.
7. Source-aligned reference package ZIP `TVK_LamThien_CP340_Canon_V21_Front_Alpha_Trial_NOT_SPINE_READY.zip` SHA256 `51cafc14800032712eeed7f0d1ff47edf6f486659ac38c28279298a1be0cb535`, 26 entries, ZIP CRC PASS. Backup in ChatGPT Library `/Thanh Van Ky/Development/CP340_Canon_V2_1_Front_Alpha_Trial/`, with `.ora`, experimental alpha PNG and preview separately indexed.

## Visual QA conclusions

- The approved sheet is **one flat infographic**, not 4K/Spine output; source Front view is **215×449 native**. Resizing it does not produce detailed new line art.
- Front and 3/4 Front **faces are close to frontal** in the sheet. A true production 3/4 head must be redrawn with correct perspective *without changing any defining face, body, bodice or costume design*.
- The image-derived alpha contains **imperfect cutout edges**, source-baked face/outfit, and no hidden underpaint. This is useful for tracing alignment only.
- Five expression crops and four damage crops are **still flat reference cells**, not independently animated attachments or damage overlays.
- `app/src/main/assets/character_expression_profiles.json` keeps `production_release.status=blocked_pending_art`, `sprite_paths={}`. **Never release or replace canon with this trial**.

## Next work that actually unlocks the game

1. Art redraw a **native high-detail Front** anchored to the exact 215×449 source crop and full approved sheet (no redesign, +17% already integrated); cleanly separate body, hair/back/front, skin/face underpaint, bodice, sleeves, ribbons and signature accessories.
2. Test only **one pose and one view** first: joint rotations, transparent alpha, hair/cloth occlusion, draw order and comparison with canonical full-body silhouette.
3. Produce five expression attachments on a *single artist-painted face master*, preserve amber irises and approved emotion styling, QA at 256/132/64px.
4. Apply 70/50/30 overlays from approved reference **without exaggerating damage or changing body/coverage**. Then replicate across the other angles and poses.
5. Request visual acceptance of **painted sprite art**, not reference reapproval. Once approved, unlock CP335 asset SHA release, rig Spine, Android build and on-device QA.

**Milestone status:** P0 source visual audit + native crops COMPLETE; P1 experimental single flat alpha trial only; **P1 real semantic art NOT COMPLETE; P2 Spine and P3 APK NOT COMPLETE**.

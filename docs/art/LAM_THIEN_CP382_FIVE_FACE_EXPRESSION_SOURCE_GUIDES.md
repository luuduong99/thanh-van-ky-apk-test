# Thanh Vân Ký — CP382 | Lâm Thiển, five exact CANON portrait decomposition guides

Date: 2026-10-30. **SOURCE/SEMANTIC GUIDE only; 5 actual newly painted faces NOT complete.**

## Authority & provenance

- Only the user-approved CANON V2.1 `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941 × 1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Five exact expression crops from this very PNG, not web illustrations or another character:
  - `01_shy_Ngai_ngung.png`: (22,681,196,884), 174×203
  - `02_angry_Tuc_gian.png`: (203,681,377,884), 174×203
  - `03_pain_Dau_don.png`: (382,681,556,884), 174×203
  - `04_embarrassed_Xau_ho.png`: (561,681,737,884), 176×203
  - `05_charming_Quyen_ru.png`: (744,681,918,884), 174×203
- Every crop is verified **pixel-for-pixel against SHA-verified approved source** before writing any output. The packaged CANON is copied byte-for-byte, not re-encoded.

## Newly delivered

1. Five editable `.ora` files with **9 visible source-region guide layers** each (source pixels assigned to exclusive approximate areas), **3 hidden individually authored vector line studies** (brows, eye contour, mouth), and **1 hidden exact CANON reference**. 13 layers per ORA. Each source layer is transparent outside its rough mask; raster layer merge at rest is pixel-exact to corresponding CANON expression crop.
2. Forty-five RGBA source-region PNGs and fifteen vector SVG/PNG trial line-work layers. Eye/mouth/bang masks are *rough routing polygons*, **not true semantic separation or artist-painted skin/hair underpaint**. The visible source masks include opaque panel background pixels and are **not game-ready transparent face sprites**.
3. One CANON-only visual QA board, JSON manifest, deterministic Python generator, unittest with negative-source tests and local logs.

## Actual verification and limits

- **11/11 local `unittest` PASS**, including wrong-CANON rejection before output, tampered crop rejection, 5 pixel-exact source recompositions, nonoverlap and nonempty regions, ZIP CRC and layer counts, hidden line-studies, refusal to approve production.
- Public CI without private CANON and 5 crops should run **3 static PASS and 8 private-art SKIP** (not eleven art PASS). No visual or rig approval is implied.
- The newly authored 15 small vector traces are deliberately **hidden and unapproved**; they are not equivalent to a fully painted master face. Source expression art is approximately 174×203 pixels, **not independently painted HD**.
- Identity locked: +17% proportions and approved face/hair/outfit, five expressions, four clothing states and blue shoe tips remain exclusively in the user-approved CANON. This checkpoint only works on portrait crops, not shoes or clothing.

## Release gate

`visual_qa=NOT_PASSED`, `release_status=blocked_pending_art`, `sprite_paths={}`, `native_face_master_complete=false`, `art_approved=false`, `spine_ready=false`, `apk_ready=false`.

## CP383 / actual next painting

Paint one *real* native-resolution semantic face master (skin/ears/eyes/brows/mouth/forehead/bangs/hairpiece) using the higher-information CANON expression closeups; use the source-routing ORA as a protected guide **not as final anatomy**. Show new face side by side with the precise approved CANON, seek user visual approval, then extend to 4 other expressions. After face approval continue hair, bodice and hidden underpaint; only after full-body approval proceed to rig/Spine and Android APK.

Command:

```bash
python cp382_face_semantic_intake.py --canon inputs/LAM_THIEN_CANON_V2_1_FINAL_20261029.png --refs inputs/expression_refs --out OUTPUT
python -m unittest test_cp382_face_semantic_intake -v
```
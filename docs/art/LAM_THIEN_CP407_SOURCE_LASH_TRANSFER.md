# Thanh Vân Ký — CP407 / Lâm Thiển source-lash warp experiment

**Date:** 2026-10-30  
**Status:** Technical study completed. **ART NOT APPROVED; no runtime sprite or APK import.**

## Authoritative source

- Exact user-chosen `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941x1672 RGBA; SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`).
- Exact face crop `x=25..193,y=684..881` (168x197), not an independent HD art source.
- Previous CP402 root SHA-256 `0391ba0cb906bf5334f176ac28a508cad4afa700fe6cb7c2deb52affaf1ac5f6`.

## Concrete art investigation

- CP406 used new vector-style lines at 4× display size, but they were too uniform.
- CP407 transports a narrow strip of **real pigmentation from the CANON open upper lashes** to the CP402 closed lash curve by a geometric warp. Color/opacity are derived from the skin/lash contrast of the *same* exact source. Two different transfer weights (`0.75`, `1.15`) allow aesthetic comparison without substituting another character.
- Exact original CANON is retained outside the two existing eye ROIs in every generated frame. Source alpha preserved; no AI-generated substitute face.
- Display-only output at `672x788` is **NOT newly recovered high-resolution original art**. The real face source is only `168x197`.
- Two candidate still PNGs, a 4-way source-comparison board, an editable OpenRaster (6 layers; **ONLY exact CANON display source is visible**), a 15-pose atlas, looping GIF and 72-frame/30fps MP4.
- **15/15 unit tests passed locally** with exact CANON and CP402 source, including rejection of tampered source, unchanged outside-eye pixels/alpha, correct atlas, and source-only ORA merged layer.

## Visual QA decision

- Source-root detail is more varied and higher contrast than CP406's nearly uniform line. At enlarged scale, **dark pigment still clumps in a few locations and eyelid/skin shading is imperfect**. Thus neither CP407 version is qualified as production art. `0.75` is used only for comparison animation; the CP402/CP406 studies are not overwritten.
- Do not release based solely on test PASS or screenshot appearance. Do not change character identity, facial shape, hair/costume, +17% model body reference, or approved CANON.
- Do not use the earlier generated CP405 image of a different dark-haired character claiming “complete”. It is not Lâm Thiển and has no production status.

## True completion blockers

1. An artist-grade painted closed-eyelid frame that remains faithful to exact approved character image, with professionally tapered eyelashes and coherent local skin shading; ideally start with actual larger layered source if available, but **do not replace CANON**.
2. Explicit visual acceptance at native / enlarged resolution against exact CANON; then final closed keyframe and intermediate-frame checking.
3. Real Android playback/quality testing using approved assets, and production-art manifest/gating update. Debug APK/atlas preflight is NOT production integration.

## Usage

Run from the archive's project root:

```bash
python cp407_source_lash_transfer.py --root . --out outputs
python cp407_make_review.py --root . --out outputs
PYTHONPATH=. python -m unittest -v test_cp407_source_lash_transfer.py
```

**Release:** `visual_qa=NOT_APPROVED`, `sprite_paths={}`, `apk_integrated=false`.
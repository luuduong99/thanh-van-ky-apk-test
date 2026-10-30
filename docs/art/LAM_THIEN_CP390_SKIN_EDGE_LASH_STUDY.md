# Thanh Vân Ký — CP390 handoff (2026-10-30)

**Character:** Lâm Thiển. **Result:** technical skin-edge/eyelash trial; **VISUAL QA NOT PASSED**. No game runtime, rig, Spine or APK work was performed.

## Source is locked

- Approved source: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` — SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`; 941×1672 RGBA.
- Native 168×197 portrait cut: `(25,684,193,881)` (expression “Ngại ngùng”). Same Lâm Thiển source only. **Do not use the Tô Nguyệt Ly style reference to replace Lâm Thiển.**
- Exact CANON source bytes retained in the archive. The visible ORA layer and `mergedimage.png` remain pixel-exact source.

## Actual changes

1. Take CP389's two hand-painted/gradient eye skin underlay rasters. Sample valid source skin pixels at the feathered boundary of each underlay inside the same approved CANON, and apply a bounded RGB correction to reduce color mismatch. A subtle cheek micro-texture residual is sampled *from the very same CANON* (no external character image).
2. Create four **independent new RGBA raster layers**: `LEFT_SKIN`, `RIGHT_SKIN`, `LEFT_LASH`, `RIGHT_LASH`. The latter pair adds small eyelash taps to the older CP389 closed-eye line.
3. Save `CP390_TEN_LAYER_FACE_DRAFT_NOT_APPROVED.ora` with 10 layers: exactly one CANON original visible; four historical CP389 parts hidden; four new CP390 parts hidden; one CP390 closed-eye composite hidden. Source, CP389, CP390 before/after PNGs are provided.
4. Eye editing is strictly restricted to native portrait coordinates `LEFT [31,94,70,124)` and `RIGHT [84,70,130,107)`. The rest of the CANON character remains unaffected.

## Technical QA (not an aesthetic score)

| Measurement | CP389 | CP390 | Interpretation |
|---|---:|---:|---|
| Left eye skin feather-edge RGB MAE to open-eye CANON | 14.9951 | 13.5437 | ~9.7% lower |
| Right eye skin feather-edge RGB MAE to open-eye CANON | 11.4506 | 10.3900 | ~9.3% lower |
| Changed pixels **outside** eye ROIs | — | **0** | source protected |
| Native portrait source | 168×197 | 168×197 | **not HD** |
| ORA layers | 6 | **10** | technical layers, not a rig |
| Local tests with private exact CANON & CP389 source | 9/9 PASS | 9/9 PASS | source / structure QA only |
| Public runner without private source | — | 3 PASS / 6 SKIP | does not test real artwork |

**Warning:** The edge metric compares the DRAFT closed-eye composite with an **open-eye** reference on feathered boundary pixels. No approved closed-eye ground truth exists. Improving this metric does **not** prove a better blink or a correct eyelid/anatomy. CP390 still has visibly simplified skin shadows and eyelash strokes; **visual QA fails**.

## Release gate

- `visual_qa=NOT_PASSED`
- `production_release.status=blocked_pending_art`
- `sprite_paths={}`
- `spine_ready=false`; `apk_ready=false`
- No asset is copied into Android production `app/src/main/assets`.

## Next work — CP391

Create an artist-quality independent closed eyelid and under-skin plate with soft natural shadowing and exactly aligned lashes on CANON V2.1, review side-by-side at **native 168×197** and zoom 4×. Obtain explicit user art approval before creating in-between blink frames or integrating with engine. If artist-quality reconstruction cannot yet be achieved, retain the original CANON face as the only approved art.
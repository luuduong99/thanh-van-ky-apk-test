# Thanh Vân Ký — CP404 Lâm Thiển / actual eye paint study (30/10/2026)

**Checkpoint:** CP404. **Technical work completed, visual art NOT APPROVED.**

## Exact input / never swap characters

- Source `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, RGBA `941×1672`.
- Face crop `(25,684,193,881)` exactly `168×197`. Eye ROIs left `(29,93,71,124)` and right `(83,70,129,110)` relative to crop.
- Previous CP402 Root DRAFT (`CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png`) SHA-256 `0391ba0cb906bf5334f176ac28a508cad4afa700fe6cb7c2deb52affaf1ac5f6`.

## Real work in CP404

- Two new **source-locked** draft retouches: `FEATHER` and `DEFINED`, via source-only inpainting underdrawn eyelid, soft lower-lid skin shading, muted crease, warm pigment with varied opacity, and tiny tapered eyelash tips. A third `BALANCED` draft blends old CP402 Root with new Defined 68:32 inside eye ROIs, to preserve visible root line while softening its mechanical edge.
- `CP404_EYE_EDITABLE_8_LAYER_NOT_APPROVED.ora`: 8 layers, **only exact original CANON visible**, proposed art and semantic paint layers hidden. `mergedimage.png` equals exact 168×197 CANON. The master remains untouched.
- Edited exact source full-body comparison: `CP404_FULL_CANON_BODY_EYES_DRAFT_NOT_APPROVED.png`, source pixels unchanged except the two eye ROIs at local face position. 1,943 full-body pixels changed; image is **DRAFT**, NOT the new CANON.
- 15-slot draft atlas (2520×197); 72-frame, 2.4s, 30 FPS MP4; GIF/APNG; comparison image with exact original and CP402 Root.
- 15/15 local unit tests PASS: source lock, source privacy, ROI and alpha guard, deterministic paint, 8-layer ORA hidden/visible QA, reject changed CANON, verify geometric frames.

## Honest art QA

**Technical QA ≠ artistic signoff.** Visual inspection found the soft study faded lash contours too much; defined still appears mechanically drawn. **None should be promoted over CP402 Root automatically.** Due to the face source being only 168×197, pixel-level patching does not yield the artist-quality original high-resolution closed-eye sprite the game needs. Next action is *painting of true eyelid artwork using a high-resolution semantically layered face master, or careful 168×197 native painterly redraw*, preserving CANON character identity. Then show the new closed-eye keyframe and loop at native size and in full body and get user's visual acceptance before Android import.

## Release gate

- `visual_qa=NOT_APPROVED`, `production_sprite_paths={}`, `spine_ready=false`, `apk_blink_approved=false`, `physical_device_tested=false`.
- Never package CP404 canvas, atlas, MP4 or PNG as a production character asset. The Android debug viewer built in CP403 remains **test only** and SHA-pinned to CP402 atlas; CP404's atlas SHA is different and **must not be passed as though it were CP402**.
- Use the latest approved Lâm Thiển CANON V2.1, **NOT** a black-hair outfit reference or image generated from a different model.

## Files

- Source PNG, CP402 previous crop, `cp401_occlusion_blink.py`, CP404 script, unittest, all outputs and manifest in private chat ZIP `TVK_CP404_LamThien_Eyelid_Art_Study_NOT_APPROVED.zip` and Library backup. GitHub contains scripts, test and docs only; no private CANON bitmap.

## Rerun (private source outside repo)

```bash
PYTHONPATH=tools/art python tools/art/cp404_artistic_eyelid.py \
 --canon /path/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
 --prev /path/CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png --out /path/cp404_outputs
TVK_CP404_CANON=/path/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
TVK_CP404_PREV=/path/CP402_CLOSED_ROOT_CANDIDATE_NOT_APPROVED.png \
PYTHONPATH=tools/art python -m unittest discover -s tests/art -p 'test_cp404_artistic_eyelid.py' -v
```
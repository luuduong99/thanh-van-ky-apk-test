# Thanh Vân Ký — CP403 Lâm Thiển / blink visual inspection

**Date:** 2026-10-30  
**Scope:** Verify the exact CP402 CANON-based 15-frame eye atlas and improve **debug-only** Android visual inspection.  
**Status:** Technical improvements & QA, **NOT artist-approved / NOT a production blink**.

## Immutable approved source / inputs

- Approved CANON V2.1: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Exact portrait crop: `(25,684,193,881)` → 168×197 RGBA.
- CP402 atlas reference: `CP402_ATLAS_ROOT_DRAFT_15.png`, 2520×197 RGBA, SHA-256 `645738fa932a354e3142e2474eb35011491b091d06451a08c4443e6650529c97`.
- Allowed source-space ROIs: LEFT `(29,93,71,124)`, RIGHT `(83,70,129,110)`.
- Only the approved Lâm Thiển source. Neither a different AI portrait nor the newer outfit reference is substituted.

## Verified local CP403 work

1. **Atlas review**: 15 slots; 8 unique visual states (open and close mirrored); first/last frames pixel-exact CANON; source alpha identical in every frame; outside both eye ROIs **0 changed pixels**. Pixel-diff outside eyes = PASS, not aesthetic acceptance.
2. **Review sheet** `CP403_15_POSE_REVIEW_NOT_APPROVED.png`, 5×3 grid using raw atlas frames, pixel-accurate nearest-neighbor enlarged view. No character art pixels revised in CP403.
3. **Android source viewer improved**: source-open and DRAFT-blink **simultaneously** from the same verified atlas; start/stop, frame-by-frame stepping, pixel-sharp or filtered comparison; auto pause when activity backgrounds; SHA/size/8MiB validations preserved; debug-only, nonexported, no art added to production assets.
4. **19/19 local tests PASS** (10 public/static, 9 private source-dependent) using exact canonical image and source hash. Public CI can only cover static checks; source-dependent tests intentionally SKIP when the private artwork is not available. The **expected CI result is 10 PASS / 9 SKIP**, pending verification.
5. Other known blockers remain: closed-eye design still has a thin/computer-generated lash line, no separately painted high-resolution underpaint/mesh, no user aesthetic approval, no validation on the physical Xiaomi device, and no official sprite in the runtime manifest.

## Acceptance gate / next tasks

- **CP404 / art:** redraw/paint real closed-eye master (both lids and underpaint) in character's CANON style; show native + zoom; obtain explicit visual approval. Do not claim nearest-neighbor enlargement is new HD source art.
- **CP405 / runtime:** only after approved eye artwork, rebuild intermediate frame meshes/atlas, lock new SHA, run artifact QA and Android device test; add official runtime sprite mapping only after acceptance.
- Production status: `blocked_pending_painted_eye_art_and_device_qa`; `sprite_paths={}`; `apk_blink_approved=false`.

## Rebuild checks

```bash
export TVK_CP403_CANON=/path/to/LAM_THIEN_CANON_V2_1_FINAL_20261029.png
export TVK_CP403_ATLAS=/path/to/CP402_ATLAS_ROOT_DRAFT_15.png
PYTHONPATH=tools/art python -m unittest discover -s tests/art -p 'test_cp403_review_qa.py' -v
python tools/art/cp403_review_qa.py --canon "$TVK_CP403_CANON" --atlas "$TVK_CP403_ATLAS" --output cp403_review
```

**Do not add any CP402/CP403 DRAFT bitmap to `app/src/main/assets` or mark sprite files production-approved.**
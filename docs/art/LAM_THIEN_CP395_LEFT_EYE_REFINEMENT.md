# Thanh Vân Ký — CP395 / Lâm Thiển LEFT eye contour local refinement

**2026-10-30 — TECHNICAL DRAFT ONLY — NOT APPROVED**

## Canon & provenance
- Final character reference: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Portrait: Ngại ngùng source crop `(25,684,193,881)` at **168×197 native pixels**, pixel exact.
- Prior CP394 closed-eye draft SHA256 `d3774068b0d9464a7c3c640b0f21289a812493765259365a3ee481cc8af326d9`.
- No substituted character, unrelated reference, AI image reinterpretation or upscaled art is used as source.

## Actual work
- Audited iris-gray/eyelash band visible around LEFT eye in CP394. Partial source-eyelash retention in CP394 also preserved some eye interior dark pixels.
- Two independently editable variations: **TIGHT** (narrow source-lash band / stronger occlusion), **SOFT** (wider band / gentler occlusion).
- Four new alpha PNG technical overlays: 2 × (skin local, lash local), all based on the same exact CANON portrait and CP394 base. The RIGHT eye and all other face parts remain untouched vs CP394.
- `CP395_CANON_LEFT_EYE_9_LAYER_DRAFT_NOT_APPROVED.ora`: 9 layers, one CANON portrait visible, CP394 previous draft and all CP395 variants hidden. ORA CRC checks passed; merged image exact CANON.
- Board `qa/CP395_CANON_CP394_CP395_SOURCE_EXACT_COMPARE.png` and closeup `qa/CP395_LEFT_EYE_NATIVE_ZOOM_COMPARE.png` use source-only characters.

## QA — not aesthetic scoring
- **11/11 local unit tests PASS**, including exact source SHA lock, exact CP394 prior lock, four nonempty technical overlays, two separate variants, tamper rejection before output creation, ORA CRC/9 layers/visible source and eye-only mutations.
- CP395 vs prior CP394: TIGHT **133** pixels changed; SOFT **151** pixels changed. **0** pixels modified outside the LEFT-eye ROI `(29,93,71,124)` for both. No changes outside both eye ROIs relative to original CANON.
- On public GitHub without private source assets, expected **4 PASS / 7 SKIP**. Do not interpret skipped art tests as visual acceptance.

## Honest release assessment
- **Visual QA: NOT_PASSED**. The resulting differences are minor; source native resolution is only 168×197. Neither variant is objectively validated as prettier or painter-grade. Closed eyelid/underpaint/lash edges still require high-quality hand-painted redraw, proper anatomy and user's approval.
- `production_release.status=blocked_pending_art`, `sprite_paths={}`, Spine and APK readiness false. Nothing from CP395 imported into Android game assets.
- Do **not** repeat tiny automated eye patches indefinitely and call the character complete. CP396 should begin from an artist-grade source painting of a properly closed left eye, preserving CANON identity, with a native-size preview and zoom, and obtain visual approval before animation work.

## Rebuild

```bash
PYTHONPATH=tools/art python tools/art/cp395_left_eye_contour_refinement.py \
  --canon /path/to/LAM_THIEN_CANON_V2_1_FINAL_20261029.png \
  --cp394 /path/to/CP394_CLOSED_EYE_SOURCE_LASH_STUDY_NOT_APPROVED.png \
  --out /path/to/output
PYTHONPATH=tools/art python -m unittest discover -s tests/art -p 'test_cp395_left_eye_contour_refinement.py' -v
```

The ZIP also contains `dependencies/cp394_source_lash_underpaint.py` so a local copy can be rebuilt with `PYTHONPATH=dependencies:.` from its extracted root. The canonical GitHub repository uses `tools/art/` instead.
# Thanh Vân Ký — CP389 Lâm Thiển closed-eye manually authored draft

**Checkpoint date:** 2026-10-30. **Status:** LOCAL SOURCE QA PASS, **VISUAL QA NOT_PASSED**, no approval for animation, Spine or Android APK.

## Exact source and artist identity

- Only reference is user-approved **Lâm Thiển CANON V2.1**, native 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Source portrait **Ngại ngùng** is crop `(25,684,193,881)`, exactly 168×197 native. The CANON image is copied byte-for-byte; no web image, generated substitute or Tô Nguyệt Ly sample was used.
- The static **open-eye portrait is unchanged**, and the ORA opens with that exact image visible.

## Actual new work

- CP388 had six hidden closed-eye linework guide layers but **no underpaint**. CP389 adds four independent 168×197 transparent RGBA raster layers, manually specified in code coordinates and color stops rather than using automatic inpaint:
  1. `LEFT_UNDERLAY_DRAFT.png` — left skin/eyelid shadow underpaint
  2. `RIGHT_UNDERLAY_DRAFT.png` — right underpaint
  3. `LEFT_CLOSED_EYELID_DRAFT.png` — linework, crease, lash accents
  4. `RIGHT_CLOSED_EYELID_DRAFT.png` — linework, crease, lash accents
- Draft closed-eye composite changes **1,680 native pixels**; 709 in left audited eye ROI and 971 in right audited eye ROI; **0 changed pixels outside** the two allowed local eye ROIs `(31,94,69,122)` and `(85,70,130,105)`. This proves spatial containment, **not** artist quality.
- New **6-layer OpenRaster** includes one pixel-exact visible CANON, four individually editable hidden draft layers, and one hidden composite preview. Its mergedimage is the unchanged CANON image.
- QA comparison shows only the actual CANON user reference and our explicitly labeled closed-eye draft of the same character. The zoom is nearest-neighbor for inspection, *not* new HD detail.

## Honest visual limitations

- Closed-eye skin has flattened color and lash geometry is not yet as polished as the official CANON. **No closed-eye image has been approved by the user**.
- CP389 is a handcrafted *procedural painting study* (curves/skin gradients). It is not artist-painted production master. Closed-eye candidate uses newly painted overlay while the underlying face stays exact source.
- No approved eyelid rig, no 25/50/75%-closed frames, no frame-timing/physics, no device FPS and no Android APK build from this work.
- Keep: `visual_qa=NOT_PASSED`, `production_release.status=blocked_pending_art`, `sprite_paths={}`, `spine_ready=false`, `apk_ready=false`.

## Tests and reproducibility

- `cp389_closed_eye_study.py --canon PATH --out PATH`: verifies exact source SHA and format **before creating output folders**, then renders four editable layers, ORA, QA board and JSON report.
- `test_cp389_closed_eye_study.py`: **9/9 local PASS** with the real source (including reject modified CANON, source copy SHA, source image exact, change confined to eye region, nonempty new layers, ORA CRC/visible count/merged exact, blocked release).
- Public-source-only simulation: **3 PASS / 6 SKIP** when private CANON is absent. Never describe a public CI pass as the complete 9-source-test result.

## CP390 next

1. Manually repaint the eyelid/skin with original watercolor/cel-shaded texture, exact crease, tapered lashes and blush: the current underpaint is too flat.
2. Send **actual source CANON beside the CP390 closed-eye DRAFT** at native and 4× before any claim of quality approval.
3. After the user approves a closed-eye master, design artist-drawn intermediate frames and then test in-engine; continue other expressions/full-body, not the other way around.

**Do not register any of these drafts as runtime art.**
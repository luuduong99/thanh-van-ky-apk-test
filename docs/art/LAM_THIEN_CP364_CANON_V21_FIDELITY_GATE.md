# CP364 — Lâm Thiển CANON V2.1 visual-fidelity preflight (ART STILL BLOCKED)

Date: 2026-10-29. **New source-locked reference QA and code implemented, not new native illustrated art.**

## What was done

1. Reopened the **actual user-approved CANON V2.1** PNG from persistent Library at `/Thanh Van Ky/Approved References/Lam_Thien_CANON_V2_1_FINAL_20261029/LAM_THIEN_CANON_V2_1_FINAL_20261029.png`. Exact SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, size 941×1672. Never altered the approved master.
2. Extracted exact Front reference `CP364_CANON_V21_FRONT_PIXEL_EXACT.png` (217×458, source rectangle [13,172,230,630]). This is **pixel-identical to the source rectangle, not a newly painted high-resolution character**.
3. Made `CP364_CANON_EXACT_VISUAL_REFERENCE.png` board (1536×900) from exact reference crops: entire Front, silver-lavender hair/head and **both original blue shoe toes**. Zoom is display-only, does not restore imaginary texture details.
4. Attempted an illustrative new full-body raised-arm preview but **rejected it immediately**: it changed CANON hair to dark brown, drifted wardrobe/face, and invented apparent PASS/completion claims. **The rejected preview was NOT saved to GitHub, persistent Library, or an APK**. Do not infer 2 fully painted poses exist.
5. Implemented [CP364 canonical-fidelity checker](../../tools/art/cp364_canon_fidelity_gate.py) that requires exact locked CANON SHA before checking a candidate. It checks aligned Front crop aspect, **light silver-lavender top hair region**, and **two non-overlapping blue-toe ROIs separately**. On source Front: hair-region brightness fraction **0.8722**; image-left toe **163 visible blue pixels** (guard minimum 35); image-right toe **146** (minimum 24). The output `REFERENCE_COLOR_GUARDS_CLEAR` is **only a preliminary pixel-color preflight**, NEVER visual/art release approval.
6. [Six new regression tests](../../tests/art/test_cp364_canon_fidelity_gate.py) (synthetic fixtures, **6/6 local PASS**) cover good-color reference that still cannot auto-approve; dark-brown hair; missing each blue toe separately; invalid camera/aspect; source identity metadata. The actual approved Front was separately checked with exact SHA and non-overlapping toe ROIs.

## Implementation and limitations

- All image tests expect a **same-camera, composition-aligned Front at rest**. New pose, side/3-4/back view, different rig-canvas framing, or changed character alignment requires deliberate ROI mapping and manual inspection first. Do not treat an ROI false positive as art approval.
- Color/alpha statistics cannot certify detailed face likeness, layered anatomy behind the shoulder, fabric folds and seams, expressions, damage 100/70/50/30, or Spine animation. Image quality and Android FPS are **not** measured.
- Locked design: **+17% already baked in**, silver-lavender hair and white flower, white/blue/gold bodice, approved facial identity, two visible blue shoe toes, five expressions, four garment integrity thresholds. No change to the CANON master.
- Status remains `production_release.status=blocked_pending_art`, `sprite_paths={}`. No new sprite imported and no production APK art approved.

## Deliverables

- ZIP `TVK_CP364_CANON_V21_Reference_Color_Gate_NOT_ART.zip`, **8 entries**, SHA256 `4828cfc2c49bc5d98abd02fc4265fe03371d1b9a767c283794fa31d80c310e56`, ZIP CRC PASS.
- Includes reproducible checker, six tests, image-board builder, exact Front crop, actual-source JSON metrics, board PNG, manifest and README.
- Archived to Library: `/Thanh Van Ky/Development/CP364_CANON_V21_Fidelity_Gate/`.
- Repo code in `tools/art/cp364_canon_fidelity_gate.py` and `tests/art/test_cp364_canon_fidelity_gate.py`.

## Next production work: CP365

**Actual full native art is still missing**, not because of CI or decoder code. Create six individually illustrated **high-resolution** semantic Front roles from user-approved CANON V2.1: left sleeve, left arm skin, hidden shoulder skin, main bodice, hidden shoulder fabric, back hair (and later secondary silk/ribbons). Draw occluded geometry behind the movable elements, maintain recognizable face, silhouette and both shoe toes. Export **genuinely independently painted same-view idle/arm_raise images**, plus an editable layered master. Run CP356 structural preflight and this CP364 color guard, then have human visual QA and direct user approval before rigging/Spine and on-device performance tests. Do not repeat enlarged 215×449 source as an approved native sprite.

# Thanh Vân Ký — CP385, Lâm Thiển CANON-exact static master + eyelid shape study

Date: 2026-10-30. **Technical source study; VISUAL QA NOT PASSED, production BLOCKED.**

## Reference
- Exact user-approved CANON V2.1 `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Portrait: “Ngại ngùng” face exact original pixel crop `(25,684,193,881)` = 168×197. **No unrelated character imagery used.**

## What is actually implemented
- Improved CP384's mask design using two localized, hand-defined eye polygons and one mouth region. **This changes (and in places expands) eye selection** so original lashes are covered; it does not universally shrink the masked area.
- Source-exact separate left-eye/right-eye/mouth cutouts, inpainted skin **technical** underlay, independently drawn experimental closed eyelid strokes. 7-layer ORA with 3 hidden layers (2 draft eyelids + exact CANON reference), CRC PASS.
- Five test frames: CANON open → 55% technical transition → unapproved closed → 55% transition → CANON open. The open endpoints and static compositing reconstruct pixel-for-pixel exact CANON; every change in the underlay occurs only within selected masks.
- Technical underpaint changes 1,722 source pixels from the CANON image, versus 1,660 for the prior CP384 base. **These are affected-pixel counts, not visual quality scores and do not prove the new art is better.**
- A same-character source-only review panel and technical flipbook GIF are supplied. Drawing new eye lids on top of inpaint is **not** equivalent to artist-painted native animation.

## Checks and limitations
- 10/10 local tests PASS on exact private CANON and CP384 underlay; GitHub source-only public simulation yields **3 PASS / 7 SKIP** (private art tests absent). Static source bytes preserve SHA, ORA 7-layer CRC, no output on wrong CANON SHA.
- **Artist QA NOT_PASSED**: residual skin smoothing and eye contour issues remain; portrait still includes original design-sheet background and is only 168×197. 55% transitional frames rely on technical source opacity adjustments; they have not been artist-approved or evaluated in Spine, Unity or an Android APK. Do not call them smooth motion or approved production sprites.
- Release flags: `visual_qa=NOT_PASSED`, `production_release=blocked_pending_art`, `sprite_paths={}`, `spine_ready=false`, `apk_ready=false`.

## Source and handoff
- `cp385_blink_shape_study.py`, `test_cp385_blink_shape_study.py`, `OUTPUT/CP385_REPORT.json`, `OUTPUT/CP385_SHY_SOURCE_AND_BLINK_DRAFT_NOT_RIG.ora`, `OUTPUT/qa/CP385_CANON_VS_BLINK_DRAFT.png`, `OUTPUT/qa/CP385_FIVE_FRAME_TECH_BLINK.gif`, five source/technical frame PNGs, and user-approved original CANON file.
- Code intended for `tools/art/cp385_blink_shape_study.py`, `tests/art/test_cp385_blink_shape_study.py`; private reference art intentionally not committed into GitHub.

## CP386 next
1. Replace inpaint with painter-authored eyelid/skin underlay that truly matches CANON eye anatomy; check closed-eye portrait at native zoom with no smear and no hairline/eyebrow damage.
2. Obtain user visual acceptance for a **single** closed-eye master; then create true intermediate blink keyframes with preserved detail and check timing/draw-order in Android.
3. Prepare correctly transparent portraits, genuine semantic hair/face layers, and continue 4 remaining expression masters, full-body animation, 100/70/50/30 costume states. Keep existing CANON unchanged.
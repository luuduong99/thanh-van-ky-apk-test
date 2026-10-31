# Thanh Vân Ký — CP397 / Lâm Thiển: source-locked closed-eye DRAFT

**Ngày:** 2026-10-30  
**Trạng thái:** Two-eyes closed-eye technical paint study completed **as DRAFT only**; **VISUAL QA NOT PASSED**, user approval pending. Not an HD animation keyframe, released sprite, rig or APK.

## Approved source, no substitution

- Exactly `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, **941×1672 RGBA**, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Exact expression crop `(25,684,193,881)` → **168×197 native pixels**.
- No generated alternative character / source swap. Original CANON remains the one visible ORA layer and the `mergedimage.png` output. Draft is explicitly labeled `NOT APPROVED` and not imported into Android.

## What was actually produced

- Closed-eye experiment based on CANON pixels only: local skin reconstruction, eyelid shadow, crease, and eyeliner/eyelash paths, **4 independently editable RGBA layers for each eye**.
- `CP397_CANON_LOCKED_EYE_DRAFT_11_LAYER_NOT_APPROVED.ora` — 11 layers, one original source visible, all draft layers hidden.
- `CP397_CANON_VS_CLOSED_EYE_DRAFT_COMPARE.png` — original CANON alongside eye-only draft; `CP397_BOTH_EYES_NATIVE_ZOOM_COMPARE.png` — left/right zoom.
- `CP397_CLOSED_EYE_PAINT_STUDY_DRAFT_NOT_APPROVED.png` — facial crop at 168×197 pixels, **not a painter-approved HD master**.
- Source and all outputs bundled in chat attachment `TVK_CP397_LamThien_CanonClosedEye_DRAFT_NOT_APPROVED.zip`; archive includes the exact approved source PNG, script, tests, 11-layer ORA, reports, PNG previews, and manifest. **Private source art is not assumed available on public GitHub**.

## Verified local tests and limits

- **12/12 unit tests PASS locally** on private approved CANON.
- **1710** face pixels changed inside two eye regions; **0** changed outside.
- Source-space ROIs: left `(29,93,71,124)`; right `(83,70,129,110)`.
- Verified original SHA, exact source crop, 8 nonempty RGBA layers, alpha boundaries, curve geometry, ORA integrity/CRC, sole visible source, merged exact source, tamper rejection, and release guard.
- **Aesthetic FAIL / BLOCKED:** the eye skin and lash contours still look too flat/artificial when enlarged. Technical PASS is **not visual acceptance**.
- Don't claim generated "CP397 finished" infographic is a valid CANON asset; it depicts the wrong person and was rejected. Only the source-locked CP397 preview and approved CANON may be used.

## CP398 task / acceptance gate

1. Refine full eyelid skin painting and fine lashes for BOTH closed eyes, prioritizing the left under-eye edge; maintain same character and style as canonical crop.
2. Keep eye-only changes, or explicitly review expanded ROI before changing other facial pixels.
3. Show native 168×197 and enlarged comparison against original. **Obtain visual approval from user** before constructing blink in-betweens, rigging, physics, or Android sprite import.
4. Preserve CANON V2.1 master, +17% body reference and strict CANON-only policy.

```json
{
  "checkpoint": "CP397",
  "closed_eye_draft_created": true,
  "native_art_painter_approved": false,
  "visual_qa": "NOT_PASSED",
  "production_release": {
    "status": "blocked_pending_visual_art_approval",
    "sprite_paths": {},
    "spine_ready": false,
    "apk_ready": false
  }
}
```

Full rebuild command and dependencies are contained in the CP397 ZIP `CP397_HANDOFF.md`. No art edits were made to `app/src/main/assets`.

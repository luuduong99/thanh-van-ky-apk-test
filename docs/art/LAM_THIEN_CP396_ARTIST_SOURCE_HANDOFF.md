# Thanh Vân Ký — CP396 Lâm Thiển / CANON-locked artist source handoff

**Date:** 2026-10-30  
**Status:** **ARTIST HANDOFF PREPARED — EYE ART NOT YET DRAWN — VISUAL QA NOT PASSED**  
**No Spine, animation, HD sprite or APK milestone.**

## Provenance / approved source

- Exact approved source: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, size **941 × 1672 RGBA**, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- Original `Ngại ngùng` portrait is an *unchanged* crop `(25,684,193,881)`, **168 × 197** native pixels.
- All preview character pixels derive solely from the source file. No substitute character, older artwork, AI-generated replacement or reinterpretation was used.
- Only the approved source image is a master. The CP394/CP395 eye variants are *unapproved technical studies*.

## Actual CP396 work verified locally

- Produced original pixel-exact face crop.
- Created **native** `CP396_NATIVE_10_LAYER_ARTIST_WORKMASTER_NOT_APPROVED.ora` with 1 exact CANON visible layer, 8 separate *empty* artist-paint layers (4 each for LEFT and RIGHT), and 1 hidden eye ROI guide.
- Created **x4** `CP396_X4_10_LAYER_ARTIST_WORKSPACE_NOT_APPROVED.ora`, 672 × 788 pixels; source is **nearest-neighbor viewing proxy only**, NOT an HD art master or a native hand-painted sprite.
- Created `CP396_SOURCE_VS_ROI_MAP_NOT_ART.png`: image on each side uses the exact same CANON expression; right side adds *annotation outlines only*. No character art has been repainted in the guide.
- Eye-only QA ROIs: LEFT `(29,93,71,124)`; RIGHT `(83,70,129,110)` in native portrait coordinates.
- **8/8 local tests PASS**: SHA lock, native pixel-exact crop, each ORA 10 layers with one visible exact source, eight actually transparent paint targets, ROI geometry, fail-fast rejection of tampered source.
- Local zip `TVK_CP396_LamThien_CANON_Artist_Handoff_NOT_APPROVED.zip` includes the exact approved CANON copy, two ORA files, source-only board, manifest, README, regeneration script and tests. Zip shared in the CP396 chat as an artifact; **do not assume GitHub hosts the private-source binary**.

## Art task remains blocked: CP397

1. Paint *new painter-quality* fully closed eyelid, especially the LEFT eye; iris/eye-white must not show. Preserve eyelash style, underpainted skin, eyelid crease, lashes, and subtle shadows. Keep the character's CANON face identity intact.
2. Treat eye-only masks as QA constraints. If real art requires widening them, propose and review the change — no silent face changes.
3. Compare native 168×197 and zoom. Do not judge aesthetic acceptance using pixel-diff PASS alone.
4. Submit the **actual painted keyframe** for visual approval before blink in-betweens / rig / any Android art import.
5. Never repeat tiny automated eyelid patches while claiming full art completion.

## Release gate

```json
{
  "checkpoint": "CP396",
  "closed_eye_keyframe_painted": false,
  "visual_qa": "NOT_PASSED",
  "production_release": {
    "status": "blocked_pending_art",
    "sprite_paths": {},
    "spine_ready": false,
    "apk_ready": false
  }
}
```

**Keep CANON-only policy active across all TVK characters.** Tô Nguyệt Ly reference remains DRAFT until separately approved.
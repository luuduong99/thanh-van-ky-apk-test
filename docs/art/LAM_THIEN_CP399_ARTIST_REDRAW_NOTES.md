# CP399: art-redraw notes for CP400 (Lâm Thiển CANON V2.1)

**DO NOT RELEASE**; below is paint-over guidance, not an approved image.

- Preserve exact face silhouette, eyes' spacing, visible brow, eyelashes shape language, mouth, blush, hair, flower and accessories from CANON. Source crop 168×197 only.
- Eye LEFT ROI `(29,93,71,124)`: remove flat horizontal gray line and feather at corners. Under-eye pink skin must match source texture and light. Retain fine, natural lash distribution rather than repeated vector strokes.
- Eye RIGHT ROI `(83,70,129,110)`: taper upper lid and outer-lash tip; prevent an abrupt hard horizontal ending. Preserve original brow highlight and adjacent hair.
- Close both eyes completely; iris / sclera should not leak through.
- If art correction needs to touch outside ROI, submit explicit new masks and side-by-side pixel diff for approval first.
- For future 2D rig: create genuinely painted layers (skin/eye-line/lash/crease/underpaint) on higher-resolution native original *if supplied*, not simply x4 or x8 enlarged pixels.
- Compare at **native 168×197** and zoom. Photograph-like blur or pixel-difference PASS is not enough.
- Store final user's approval reference and exact hashes before adding to `app/src/main/assets`. Never silently swap model/face.

Current two candidates are only draft input; do **not** select Natural/Soft as a final production keyframe without aesthetic approval.
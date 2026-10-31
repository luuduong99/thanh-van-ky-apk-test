# Thanh Vân Ký — CP388: Lâm Thiển exact-CANON eyelid linework guides

**Status:** technical linework draft, **VISUAL QA NOT PASSED**, not an accepted closed-eye portrait, not Spine, and not an Android APK.

## Canon is unchanged

- Exact user-approved Lâm Thiển V2.1 source file, `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, 941×1672 RGBA, SHA-256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- The **Ngại ngùng** face crop is `(25,684,193,881)`, exactly **168×197 native pixels**. The display at 4× zoom is only an enlarged reference; it creates no new detail.
- The image selected as a style reference for Tô Nguyệt Ly remains separate and was **not** used as a Lâm Thiển reference.

## What was actually produced

1. **Six manually authored Bézier eyelid-line guides**, each exported both as editable SVG and transparent PNG: left/right upper lash, left/right lower lash, left/right crease. SVG paths and pixel alpha are independent and limited to small eye regions. They are not completed closed-eye eyelids or hidden skin.
2. An **8-layer OpenRaster**: one visible exact-source CANON face, six new **hidden** linework draft layers, and one **empty** hidden painting-underlay layer. The merged image remains 100% source-identical.
3. A side-by-side QA image showing the exact CANON and a *linework overlay* on the same source. It does **not** claim to show a finished blink frame.
4. Reproducible tool, unit tests, reports, and a zipped handoff that includes the original source PNG byte-for-byte.

## QA

- **8/8 local unit tests PASS** with the exact CANON source: source SHA lock and wrong-source rejection before writes; all six SVG curves parse; PNG alpha remains in respective eye ROIs; source bytes preserved; ORA ZIP/visible layer count/merged image exact; release remains blocked.
- In an isolated public CI copy without the private CANON source: **3 PASS / 5 SKIP**. Static tests passing do not imply the private art was tested in GitHub.
- Underpaint layer is **intentionally EMPTY**. This explicitly prevents passing technical inpainting or flat skin patches off as artist-painted detail.

## Remaining blockers / CP389

- Paint actual *closed-eye* eyelids and realistic skin underlay, with correct original iris occlusion, highlights, lash taper, crease, blush, and hair overlaps. Original open-eye face must remain pixel-exact.
- Review the result next to the original CANON at native size and 4×; **the user must approve the visual design** before intermediate blink poses are created and integrated.
- Create independent 25/50/75% frames only after artist-quality open/closed master exists; then verify underpaint at different poses and test in the engine.
- Do not import draft SVG/PNG/ORA into `app/src/main/assets` or mark `sprite_paths` nonempty before approval.

**Release gate:** `visual_qa=NOT_PASSED`; `production_release.status=blocked_pending_art`; `sprite_paths={}`; `spine_ready=false`; `apk_ready=false`.
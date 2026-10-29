# CP344 — Lâm Thiển CANON V2.1: native art and 2D motion quality gate

Date: 2026-10-29. Status: PLANNED / NOT IMPLEMENTED. Previous checkpoint: CP343 region masks passed static composite checks, but moving an arm exposed 1,798 missing pixels and 1,098 protruding pixels; underpaint gate FAIL.

## Source of truth
- CANON V2.1 user approved image `LAM_THIEN_CANON_V2_1_FINAL_20261029.png`, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, 941×1672.
- Keep +17% body proportions, distinctive face, silver/lavender hair, white flower, white/blue/gold clothing, bodice construction, five expressions and damage 100/70/50/30 exactly as approved.
- CP343 215×449 region layers are for analysis and not quality-approved game sprites. Do not upscale a low-resolution crop and claim native high-res asset.

## First executable art unit: front shoulder–arm seam
1. Paint a native-resolution Front figure in separated semantic layers with complete hidden regions: upper arm/shoulder skin, sleeve fabric, underlying bodice, back hair overlap, arm and relevant ribbons. No gaps at joints.
2. Deliver real named transparent PNG layers and ORA (or a layered editable master). Each part must have a safe padded canvas and consistent origin/pivot.
3. Render idle pose plus two keyframes of one gentle arm lift; compare each against CANON V2.1 for silhouette, costume, facial recognition, colors, coverage.
4. Test alpha holes, unexpected clipping, layer draw order and visual deformation at the shoulder, sleeve, neckline and hair overlap. Record before/after full figure and zoomed QA.
5. Only after one arm passes proceed to opposite arm, five expression attachments and all damage variations; then side/back/3-4 views.

## Android visual and motion targets (targets, not measured results)
- Prioritize crisp source art, correct aspect ratio, alpha premultiplication and sampling; high-res source and mipmap/filter settings depend on scale and renderer.
- Aim for steady 60 FPS on target phone; measure device frame time, memory and frame pacing. 30 FPS fallback may be necessary on slower hardware; never promise an untested rate.
- For game render, smooth interpolated 2D bone animation plus secondary hair/sleeve/ribbon motion; avoid hard cutout drift, texture swimming, alpha seams and excessive blur.
- Respect previously approved combat layout (all allies and enemies on one screen), portrait/dialogue UI, and animation on active combat turns and threshold-triggered damage.
- Need actual APK capture with idle, expression swap, arm motion and combat action; test on Android and document measured FPS before claiming quality passed.

## Release gate
- Current `production_release.status=blocked_pending_art`, `sprite_paths={}`.
- CP344 cannot pass until layered art, real underpaint, composited previews, motion test and device test exist. A checklist alone is not evidence of execution.

Next: construct/obtain editable high-resolution Front original art and complete one arm joint; run visual QA with CANON side-by-side.
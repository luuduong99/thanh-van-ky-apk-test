# Thanh Vân Ký — CP392: Source-retained eyelash occlusion study

**Date:** 2026-10-30  
**Identity:** Lâm Thiển CANON V2.1, exact 941×1672 RGBA, SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`  
**Source portrait:** CANON sheet crop `(25,684,193,881)` 168×197 px — *Ngại ngùng*.  
**Previous draft:** CP391 SHA256 `24787edd37449346d0c6a97bc6a3cd06e2f4bfc8a093d21acbf6cb435d32acac`.

## Scope completed

Previous CP391 repainting of both eyelids caused a flat skin region and changed the original eyelash shape. CP392 instead **preserves the source eye/lash contour** and tests narrow, hand-aligned eye-occlusion masks, sampling underlying color from the **same CANON portrait** at a source-local cheek offset (+13 px). It creates two non-final variants: `gentle` (partial) and `near_closed` (more occluded; not a true fully closed eye). Each variant has independent LEFT and RIGHT source-sampled patch PNGs (4 total).

The ORA contains **8 layers**: only the original open-eye CANON is visible; the CP391 historical draft, 4 patch layers and 2 variant composites are **hidden**. The ORA merged image is pixel-exact to the source portrait. Each draft modifies **only** within the previous approved technical eye ROI; original CANON data is copied byte-for-byte and never overwritten.

## Tests (actual measurements)

- **11/11 local unittest PASS** with private CANON/CP391. Public-source-only simulation: **4 PASS / 7 SKIP** because the exact art is private. These are technical, not aesthetic tests.
- `gentle` changes **814 pixels** versus the original portrait; `near_closed` changes **1,087 pixels**; the two variants differ at **748 pixels**.
- Changed pixels **outside eye ROIs = 0** in both variants.
- Wrong source SHA rejected before output. ORA CRC PASS and exactly one visible CANON source layer.

## Honest visual QA

**NOT PASSED.** The `gentle` version looks like a narrower version of the same original eyes. `near_closed` still retains portions of the old open-eye lash contour and may show remnants of the old iris; it does NOT include complete painter-drawn eyelids/underpainting for full closure. The source has native resolution 168×197 px and enlarging it is not HD art creation. There is no rig, Spine validation, Android runtime, new APK, FPS test or artist approval.

`production_release.status=blocked_pending_art`, `sprite_paths={}`, `spine_ready=false`, `apk_ready=false`. Do not import CP392 candidates into `app/src/main/assets`.

## Next: CP393

Make a **new genuine closed-eye painter-quality overlay**, including skin, lid fold, lashes and concealed anatomy, using this correct Lâm Thiển CANON and CP392 masks as editable guides. Review at native size and 4×, request user visual acceptance, and only then create intermediate blink frames. Do not use a newly generated unrelated portrait as CANON. Keep Tô Nguyệt Ly's aesthetic reference separate.
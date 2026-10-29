# CP361 — Lâm Thiển: editable four-part shoulder underpainting study, Visual QA FAIL

Date: 2026-10-29. **Source-locked material illustration study completed, not native full-body art, not Spine or APK ready.**

## Source and design locks
- Approved CANON V2.1 941×1672 PNG: SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. File unchanged.
- CP348 toe-fixed 10-region raster: archive SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`; actual full-figure cutout **215×449**.
- Locks: no new +17% body adjustment (already present), approved face/silver-lavender hair/white flower/white-blue-gold bodice/two blue shoe toes, 5 expressions and damage levels 100/70/50/30.
- CP360 previously made two tiny experimental Bézier regions but could not produce artist-quality motion. CP361 is a larger, **still provisional**, multi-material art study and deliberately does not claim the complete six production-painted shoulder roles.

## Work produced from actual assets
- Four distinct **new SVG drawings** with custom Bézier paths, gradients and highlights/shadows at a 1290×2694 *rasterization canvas*. These are editable vector source paths, not upscaled old skin or cloth pixels:
  - `01_hidden_shoulder_skin`
  - `02_hidden_bodice_inner_fabric`
  - `03_rear_silk_underarm`
  - `04_rear_hair_overlap`
- Four individual full-resolution PNGs of authored color strokes; also four clipped QA parts placed only beneath pixels where original low-res arm alpha is fully opaque.
- One **14-layer OpenRaster** `CP361_EDITABLE_14_LAYER_HIGH_CANVAS_ART_STUDY_NOT_RIG.ora` at 1290×2694: 10 *sixfold nearest-neighbor enlarged* original CP348 layers plus 4 clipped authored patch layers. **The other 10 original source parts are still low-res and are not native high-resolution redraws.** The ORA is for editability and compositing experiments only; the four original SVGs are the editable painter source.
- Idle image reproduces approved visible CP348 RGB and alpha **exactly at enlarged source pixels**; both blue toes are unchanged. CANON sheet was not modified.
- Matching camera/canvas temporary grouped-arm rotations at 0°, -2°, -4°, -7° with/without new art. These are raster transforms, **not artist-painted same-view raised-arm keyframes**, and not Spine.

## Quantitative seam-area diagnostics (6× raster pixels)
The ROI is a manually selected shoulder/upper-body area x=[42..84],y=[119..191] in the 215×449 source view, mapped to 6× for the analysis. Lost source coverage is not necessarily an anatomical hole (moving hand/sleeve leaves vacated source pixels). Metrics from CP361 rendered images:
| Angle | Lost coverage before | Lost coverage with art | Newly revealed patch pixels |
| --- | ---: | ---: | ---: |
| 0° | 0 | 0 | 0 |
| -2° | 2039 | 430 | 1596 |
| -4° | 4278 | 540 | 3712 |
| -7° | 7673 | 581 | 7066 |

**Do not compare these 6× counts directly with prior CP359/360 native-215px measurements** or treat fewer lost pixels as visual correctness.

## Real QA status and files
- The technical checks in the builder: **12/12 PASS** (CANON and CP348 SHA locks, four nonempty new authored paints, clipping, pixel-exact rest, consistent mockup canvases, ORA zip integrity / 14 layers, and explicit release block).
- **Manual visual review: FAIL / NOT ACCEPTED**. `CP361_SHOULDER_NEW_ART_STUDY_PREVIEW.png` reveals stiff blue/silk fill and unnatural edges around the body/arm at larger rotation; the full 215×449 source's existing silhouette cut lines remain. The work does not reconstruct complete anatomy, shoulder/sleeve details or back-hair geometry.
- ORA SHA256 `e58b8e34c1c07b6859064cad87fa92c45a90613d6bd66fc2b8e439deff284e9ce` (check actual file if changing sources).
- Deliverable `TVK_CP361_Shoulder_Vector_Art_Study_NOT_SPINE.zip` **17 files**, CRC PASS, SHA256 `224d694c7a01f5e66b6c12c3a68c6b82f9115103bbaafa78a7909c5732c935c8`.
- Library: `/Thanh Van Ky/Development/CP361_Four_Vector_Underlays_ArtStudy_VISUAL_FAIL/`.
- Source code: [CP361 builder](../../tools/art/cp361_four_shoulder_underlay_study.py), tested with locked original input files, receives `--canon`, `--cp348-zip`, `--out`; [CP361 code safety tests](../../tests/art/test_cp361_vector_study_safety.py).
- `production_release.status=blocked_pending_art`, `sprite_paths={}`. **No APK build or device FPS test was undertaken during this art-only checkpoint.**

## CP362 — next real art milestone
Author independently painted **full-resolution** left arm skin, front/inner sleeve, body/bodice, hidden shoulder anatomy and cloth, and back hair with enough occluded continuation for lifted-arm motion. Existing CP361 vector components can be used only as initial color/position studies. Replace source-derived low-resolution 10-part base with an actual native high-resolution multi-layer full figure. Export a genuine same-angle (same viewpoint/pivot/canvas) idle + deliberate raised-arm pose pair. Review facial identity, proportions, two blue shoe toes, cloth folds and silhouette against CANON V2.1 before rig/Spine, then measure Android frame pacing on device. Never mark a temporary raster transform as a finished painter-authored pose.

# CP360 — Lâm Thiển: two local original vector-underpaint studies + seam-aware motion QA

Date: 2026-10-29. **Technical source QA passes, new painted sketches are NOT artist-approved native character art.** Do not ship.

## Source
- Exact user-approved CANON V2.1 final reference (unchanged), SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`.
- CP348 toe-corrected 10 region archive, SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`.
- CP359 editable six-way source split, still **215×449** source pixels, is a disjoint material segmentation and **not** painted native production art.

## New work and verified behavior
- **Two new separately editable, original Bézier/gradient study layers** at **1290×2694 render resolution**:
  - `CP360_HIDDEN_SKIN_PAINT_STUDY.svg`: softly shaded tiny hidden shoulder/upper-arm region.
  - `CP360_HIDDEN_BODICE_PAINT_STUDY.svg`: small blue-white inner bodice/cloth fold study.
  They were hand-directed based on approved reference and rendered to transparent 6x RGBA. This is only local newly authored underpaint, **not a complete genuine high-res character**, not recovered hidden pixels from the original.
- Downsampled, strictly clipped to the fully opaque original CP348 arm area to guarantee **pixel-exact idle alpha and visible RGB**, still preserving both approved blue shoe toes.
- New `CP360_LEFT_SHOULDER_PAINT_STUDY_19_LAYER_NOT_RIG.ora`: **19 layers**, consisting of the original nine other CP348 source groups, six CP359 arm material layers, two **actual local paint studies** and two **still-EMPTY full native underpaint slots**. The ORA is a 215×449 **low-res editable research file**, despite the original vector study renders at 1290×2694.
- Exported same-view, same-canvas `0/-1/-2/-4°` composite QA poses before/after tiny underpaint, and full contact sheet `CP360_SHOULDER_PAINT_SAME_VIEW_QA.png`. These are **mathematical group rotations**, not realistic hand-lift keyframes or Spine rigging.
- Discovered a useful error in earlier metric interpretations: pixels vacated by the **moving hand and silhouette** are often expected; not all pixels missing from rest-frame alpha indicate true underpaint holes. We now report manually selected shoulder seam, bodice-adjacent seam and free-hand ROI separately.
- **Important render fix:** When the six CP359 source categories are rotated individually, independent interpolation causes visible discontinuities; CP360 composites them as **one temporary arm group first** and transforms once for the QA pose. At -2°, individual vs grouped images differ at **1,362 RGBA pixel positions** (this is a rendering-method difference, not an error count). Keep source layers separate for future authoring, do not individually rotate arbitrary segmentation masks before proper reillustration.

## Same-motion source-coverage measurements (small, not approval)
All numbers derived from original CP348 source at **215×449**, rotating the same grouped arm around **provisional pivot (70,132)**:
| Rotation | Lost coverage before | Lost coverage after | Shoulder-seam coverage before→after | Body-seam coverage before→after | Hand-margin coverage before→after |
|---|---:|---:|---:|---:|---:|
| 0° | 0 | 0 | 0→0 | 0→0 | 0→0 |
| -1° | 30 | 30 | 0→0 | 13→13 | 12→12 |
| -2° | 133 | 117 | 3→0 | 47→34 | 52→52 |
| -4° | 307 | 265 | 18→0 | 105→81 | 98→98 |

The seam ROIs are *hand-selected for diagnosis*; missing coverage in a region is not a verified hole without reviewing occlusion geometry. The hand-margin changes, for instance, are plausibly expected silhouette motion. Reduced counts do **not** establish anatomical correctness or fabric continuity. The same pose still has visible visual defects at other edges. **Artist Visual QA: NOT PASSED.**

## Verification, files and provenance
- Local actual-source checks **12/12 PASS**, including exact SHA source locks, correct ORA CRC/19-layer count, exact idle composite, both new paint sketches nonempty, **two full native slots empty**, matching pose dimensions, no production release.
- Core builder: `tools/art/cp360_local_underpaint_study.py`, CLI inputs `--cp348-zip`, `--cp359-zip`, `--canon`, `--out`.
- Synthetic CI tests: `tests/art/test_cp360_motion_semantics.py`; tests prove motion-metric safety and source gates but never certify real art.
- QA bundle `TVK_CP360_Local_Shoulder_Paint_Study_VISUAL_NOT_APPROVED.zip`: **25 files**, ZIP SHA256 `58f782dbc06cb051a7009f1ab4e84fba3c38563904458464fb3b87a256e9fc84`; ZIP CRC PASS. Contains SVG sources, 6x native samples of local patches, 19-layer low-res ORA, 0/-1/-2/-4° images, JSON ROI statistics, README and builder.
- ORA SHA256 `80b0c583e342ad40d62e429a2bd2fb05158bce5ac7139d3e3f70308d474d0ee4`.
- Library path: `/Thanh Van Ky/Development/CP360_Local_Native_Vector_Underpaint_Study/`. No approved source overwritten.

## Honest production gate and CP361
- Only **two tiny new local vector sketches**, not **six complete high-resolution independently painted shoulder/arm/bodice/hair source parts**.
- Full-body native art, hidden anatomy, realistic sleeve folds, reliable camera-consistent pose pair, independent rig/skeleton and physical Android FPS remain unverified or absent.
- `production_release.status=blocked_pending_art`, `sprite_paths={}` remain unchanged. Do **not** register this test ORA into APK or claim motion/painter approval.
- **CP361:** replace source-derived shoulder material cuts with genuinely painter-authored high-res semantic layers, including complete hidden skin/cloth/hair **well beyond the current tiny local patches**. Require same-view idle/arm-raise composite and artist/user acceptance before using in Spine/Android. Continue checking both blue toes and CANON V2.1 body proportions (+17% already applied), face, silver hair, white-blue-gold bodice, expressions and damage stages.

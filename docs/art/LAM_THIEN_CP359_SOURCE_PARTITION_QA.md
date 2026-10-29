# CP359 — Lâm Thiển: source-exact left-arm texture partition (NOT painter-grade art)

Date: 2026-10-29. Completed: a reproducible source-to-editable-layer restructuring experiment. **Native art, hidden underpaint, rig and Android visual QA remain incomplete.**

## Source lock
- User-approved CANON V2.1 PNG SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`, left untouched. +17% ratio already included. White/blue/gold bodice, silver hair, ornaments, face and two blue shoe toes unchanged.
- Source CP348 10-region archive SHA256 `f7cd164a509f6cb93b48c0fb6987dd9b008d58f4e11d625f5a4c1c30173f1497`. Its **215×449** source is low-resolution. The original `06_left_arm_and_sleeve.png` had skin, sleeve, gold trim and silk mixed in a single patch.

## Work actually produced
- Split the actual `06_left_arm_and_sleeve.png` into **six independent and nonempty, mutually exclusive RGBA textures** with pixel ownership preserved:
  1. `CP359_01_ARM_SKIN_SOURCE_NOT_PAINT` (1,022 occupied pixels)
  2. `CP359_02_GOLD_TRIM_SOURCE_NOT_PAINT` (182)
  3. `CP359_03_BACK_SILK_SOURCE_NOT_PAINT` (1,478)
  4. `CP359_04_INNER_SLEEVE_SOURCE_NOT_PAINT` (497)
  5. `CP359_05_LOWER_SILK_SOURCE_NOT_PAINT` (734)
  6. `CP359_06_SLEEVE_REMAINDER_SOURCE_NOT_PAINT` (356)
- **These are class-partitioned source pixels, not new artwork or verified perfect anatomical semantic masks.** They may need manual refinement for articulated use.
- Created a **valid 17-layer OpenRaster** `CP359_ARM_SEMANTIC_SOURCE_PARTITION_NOT_RIG.ora`: nine unchanged CP348 source groups, six new subdivisions replacing one grouped arm and **two distinct EMPTY hidden-underpaint layers** (for future skin/cloth painting). At rest, alpha and visible RGBA values match the CP348 original **pixel-for-pixel**.
- Rotating the original arm group -2° around provisional (70,132) at **native low-res grid** still yields 133 missing-coverage and 62 new-coverage pixels. The earlier CP353 -2° count of 157 px was made with 6× resampling and is **not directly comparable**. This test proves missing underpaint remains; it does not certify a correct articulated pose.
- Created `CP359_SOURCE_PARTITION_QA.png`: source/rest, partition/rest, diagnostic pivot pose, six individual visible material categories. **Visual QA not approved for animation.**
- **9/9 local actual-source structural/reproducibility checks PASS**, including canonical hash, ZIP CRC, each layer, exact material pixel ownership, visible comp, blank hidden layers and hard release block. The PASS applies **only to technical structural QA**, not artistic fidelity.
- Deliverable ZIP `TVK_CP359_Source_Exact_Arm_Six_Part_ORA_NOT_PAINT.zip` (14 files) SHA256 `f1412e354973812054035982473192cd409b1a1e914ca6ace0e32265a46b07d1`. ORA SHA256 `1eeacef8ae8503afbd6f5d4c33d18144baf0344121a96a33a0f2baae0c291ad0`. Archived to Library `/Thanh Van Ky/Development/CP359_Source_Exact_Left_Arm_Partition_QA/`.
- Full generation and actual-source test scripts `build_cp359.py` / `test_cp359.py` reside inside the ZIP. Repo checker `tools/art/cp359_pixel_ownership_check.py` verifies already-exported ORA against original CP348 ZIP.

## Explicit limits / what's next CP360
- Source is **215×449**. No high-res reillustration was obtained or completed; **0 genuinely painted hidden native layers**, **0 same-view high-res art pose pair**, no Spine rig/Android art acceptance.
- The six components are *source-pixel categories*, **not** the six mandatory painter roles of CP356. **Do not set those painter slots to filled**. The permanent gate remains `production_release.status=blocked_pending_art` and `sprite_paths={}`.
- **CP360 action:** use CP359 editable source split *only as a mask/alignment guide* to actually paint new high-resolution shoulder skin, sleeve folds, bodice underlap and hair overlap, then export same-camera, same-pivot idle and arm-raise images. Evaluate against CANON V2.1 with human review; do not use artificial interpolation or generated drifting identity. Only after artist-grade art passes can rig and measured Android APK tests start.

# Lâm Thiển — CP333: refine SVG semantic face layers (2026-10-29)

**Checkpoint:** CP333 technical layer polish COMPLETE; **production art NOT APPROVED, Spine NOT VERIFIED, APK NOT BUILT**.

## Approved references — NEVER replace

- **CANON V2 / body–face–costume:** `LT_CANON_BODY_REF_2026-10-28_V2`, SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`; the canonical face has **warm amber eyes**, long silver hair, white–pale-blue outfit, restrained gold decoration. The character-specific +17% change is already in V2.
- **Five expression reference:** `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`, `shy / angry / pain / embarrassed / alluring`. This reference controls emotion, **not new facial identity**.
- Four garment integrity thresholds `100/70/50/30`, outfit and pose state rules remain unchanged. Do not copy Lam Thien face/body to other characters.

## Actual files created in CP333

1. Using existing CP332 **semantic SVG geometry**, added a few more hand-authored *vector path details* for hair shine, gold floral filaments, amber iris marks, eyelashes, brow strands and finer mouth contours. No poster pixels were copied to the semantic layers.
2. Regenerated **one OpenRaster base master** (10 editable RGBA layers) and **five emotion ORAs**, each with the **same 10 base layers plus 13 RGBA facial parts** (65 independently stored expression layers in all). All six ORAs have actual nonempty art.
3. Preserved full opaque base facial skin under the eye and lip coordinates, and the hair draw-order above the face. Five expressions produce distinct composites. **Current 1024×1024 canvas is VECTOR R&D, not evidence of CANON V2 fidelity.**
4. Created CP333 comparison review as a local image in the Library backup: `preview/CP333_BEFORE_AFTER_ART_QA_NOT_APPROVED.png`, plus `CP333_CANON_REFERENCE_GATE.png` and `CP333_DIALOGUE_SIZES_QA.png`. These previews clearly label the assets **NOT APPROVED**.
5. Saved repeatable authoring code `tools/cp333/build_cp333.py`, QA script `tools/cp333/validate_cp333.py`, contract `tests/art/test_cp333_source_contract.py`, and machine-readable [manifest](LAM_THIEN_CP333_ART_HANDOFF_MANIFEST.json).

## Binary QA results (local, actual files)

- **13/13 local unittest PASS**, including six ORA ZIP/CRC/stack and merged RGBA pixels, 65 nonempty alpha attachments, identical base hashes across all five emotions, warm amber and no blue eye drift, source SHA unchanged, and actual source-vs-refinement byte changes on PNG layers.
- `validate_cp333.py` technical audit: **PASS**. **Production `--strict` deliberately returns exit code 1**, because artist approval, full 3/4 head, Spine and APK are missing.
- A separate source-only contract (locally **9/9 PASS**) verifies the SVG edits and immutable reference metadata. GitHub CI does not contain Library ORA binaries; only source/metadata and synthetic renders are tested.
- **No new sprite_path entries** in Android; no game art is registered from CP333.

## Files and provenance

- Local package: `TVK_LamThien_CP333_Refined_Vector_Study_NOT_APPROVED.zip` (**179 entries**; ZIP CRC PASS), SHA-256 `1f8aa806758332194e258f941530b18b54e00991c877c3397a274d7c134517ad`.
- Persistent Library Development: `/Thanh Van Ky/Development/CP333_Refined_Vector_Study/TVK_LamThien_CP333_Refined_Vector_Study_NOT_APPROVED.zip`.
- Asset compare: `/Thanh Van Ky/Development/CP333_Refined_Vector_Study/CP333_BEFORE_AFTER_ART_QA_NOT_APPROVED.png`.
- `CP333_ART_HANDOFF_MANIFEST.json` stores SHA-256 for the six ORAs and guard flags; `CP333_FILE_CHECKSUMS.json` in ZIP has per-file hashes. Source included in the package; replay requires approved source files with exact hashes.
- Latest infographic generated in this phase may say “Production Ready”; **this phrase is only drawn text in an image**, and does not establish actual sprite quality, layers or Spine readiness.

## Visual QA and honest blockers

**Technical detail was added, but the result still looks flatter, more icon-like, with different facial geometry and hair ornament proportions than the richly shaded anime CANON V2.** This is not approved as the final Lâm Thiển face. Current four body/wardrobe damage stages are not connected to the CP333 face art. No Front 3/4 or side semantic face master exists.

## CP334 — required next meaningful milestone

1. Prioritize **high-fidelity redraw by artist/image-editing** against official CANON V2, rather than another low-value crop/atlas iteration. Retain one consistent face, amber eyes, silver hair, floral ornaments and outfit identity.
2. Produce visibly polished layers for `hair_front/back`, `face_underpaint`, eyes/iris/lashes, eyelids/brows, mouth and blush. Repair underpaint and occlusion where mesh moves. Preserve semantic separate SVG/ORA structure from CP332/333.
3. Make a genuine Front and 3/4 art pair in matching pose/proportions; QA 256px/132px/64px on five expressions, check facial silhouette, brows, gaze, blush and mouth. Keep eyes amber in each open-eye state.
4. **Send finished art preview for asset acceptance** (the user already approved CANON V2 and five emotional directions; do not ask them to approve those choices again).
5. Only after accepted art, link assets in Android, import actual Spine project, check animation/blend/occlusion, build/test APK and update P0/P1/P2 acceptance flags with evidence.

**CP333 does not close P0-02, P0-03, P1-03 or P2.**

# CP365 — Lâm Thiển: same-view layered pose export, native art still missing

Date: 2026-10-29. **Actual tool implementation and real-ORA source audit completed; production art NOT completed.**

## Original request and present blocker
The production goal is still a true high-resolution *independently painted* character Front, including both left sleeve and arm, hidden shoulder skin, main and hidden bodice cloth, and back hair. The previous CP350 1290×2694 ORA is only an editable scaffold: **all six mandatory paint layers remain empty** and the 17th flat CP348 low-resolution reference remains visible. Existing CP361 source-derived material studies failed visual review. Merely enlarging, recoloring or rotating the 215×449 reference is not compliant with CANON V2.1 art acceptance.

## Work completed and executed
- Implemented [`tools/art/cp365_pose_exporter.py`](../../tools/art/cp365_pose_exporter.py): loads a valid OpenRaster, requires exact SHA256 of approved CANON reference, checks six semantic roles for substantial alpha pixels, prevents visible flat-reference layers being counted as newly painted art and retains `production_release=blocked_pending_art`.
- For *new genuinely painted* inputs, renderer creates same-canvas `CP365_IDLE_TECHNICAL_DRAFT.png` / `CP365_ARM_RAISE_TECHNICAL_DRAFT.png` with a **single grouped arm+front-sleeve transform**, while actual hidden skin, fabric and hair remain independent and stationary. It uses premultiplied RGB rotation to reduce black edge halos. This is a **technical motion draft**; a grouped bitmap transform is not a painter-authored raised-arm pose, Spine or runtime approval. Pivot and angle are provisional.
- Missing source/underpaint/flat-reference issues cause exit code **2 and no two-pose PNGs**; an artist must fill layers first.
- Ran on actual CP350 ORA and the user-approved CANON image SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`. Genuine-source report: **BLOCKED (6/6 required layers empty, reference only)**. No images were faked.
- Added [`tests/art/test_cp365_pose_exporter.py`](../../tests/art/test_cp365_pose_exporter.py): **6/6 local PASS**, including actual existing master must fail, synthetic painted layers produce two same-view frames, invisible underpaint triggers block, flat-reference triggers block, wrong CANON triggers block, idle is deterministic. On GitHub CI, the asset-only test is skipped if the original private Library binaries aren't present; the other synthetic tests remain runnable.
- Actual shared source ORA SHA256 `402c9f2de2f9124c423ed8ed3d54f1b6feb22ee74304b355e43e5cb94e60114d`; no modification to the CANON image or the source ORA.
- Bundle `TVK_CP365_Layered_Pose_Exporter_NOT_ART.zip`, SHA256 `2149be68e8b86bf83319e2f0cd938db9ac070808667aeebb9009b9c21eb4f7b9`, ZIP CRC PASS. Contains source script, 6-test suite, README, original CP350 ORA (unmodified) and actual-source JSON failure report. Stored in Library `/Thanh Van Ky/Development/CP365_Same_View_Art_Pose_Exporter/`.

## Release gate
- CANON V2.1 unchanged: +17% proportions already integrated, face, silver-lavender hair, white flower, white-blue-gold outfit, both blue shoe toes, five expressions, four damage levels 100/70/50/30.
- **No high-resolution six-role independent painting completed; no user-approved raised-arm painter frame; no Spine rig or real Android FPS measurement.** Do not update `sprite_paths={}` or `production_release.status=blocked_pending_art`.
- A passed structural intake or a generated *technical draft* never implies Visual QA acceptance.

## CP366 concrete next milestone
Produce the **first genuine artist-grade underpainting** directly on the semantic ORA layers, ideally starting with image-left sleeve/upper arm and hidden shoulder fabric; keep original CANON as reference, not visible as production texture. Complete all six semantic roles and export a same-view true idle and raised-arm **artist-authored** pose pair, then compare silhouette, seams, face, two blue shoes and materials. Use this CP365 renderer only for interim grouped-arm motion QA, and run CP356 preflight, CP364 hair/shoe check, and manual Visual QA. Move to rig/Android only after accepted art exists.

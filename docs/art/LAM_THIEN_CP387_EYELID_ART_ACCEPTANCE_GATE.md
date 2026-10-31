# Thanh Vân Ký — CP387: CANON Lâm Thiển eyelid occlusion audit and paint gate

**Date:** 2026-10-30. **ART VISUAL QA NOT PASSED.** No production sprite, rig, Spine, or Android APK.

## Source of truth
- The only approved Lâm Thiển image: `LAM_THIEN_CANON_V2_1_FINAL_20261029.png` (941×1672 RGBA; SHA256 `f43046d13861a2b23b2e99094040be139831de4af929c9299e7e275a3eaf910a`). This ZIP preserves exact source bytes.
- The reference for eyes is the original **Ngại ngùng** portrait crop `(25,684,193,881)`, 168×197 native pixels. Do not substitute any other portrait. The separate user-selected Tô Nguyệt Ly style moodboard is not used here.

## Actual completed work, not an art approval
1. Reviewed CP386 eye masks, current closed-eye geometry and artifacts.
2. Ran three **rejected** options against this exact source: OpenCV TELEA inpaint, Navier–Stokes inpaint, and local cheek-color donor reconstruction. All three differ only **inside** the two eye polygons; changed pixels are TELEA 1,390, NS 1,389, cheek donor 1,390, and **zero outside**. These numbers are containment checks, **not similarity/beauty scores**.
3. Created a reversible OpenRaster `.ora` with **7 layers**, exactly one visible: the exact approved static portrait. Hidden layers: CP386 prior trial, all three rejected CP387 repair candidates, and two eye review-mask overlays. Its merged image is pixel-exact to the approved crop.
4. Created a comparison sheet using *only* the exact Lâm Thiển CANON and her own CP386/CP387 derivative studies. No alternate character images.
5. Added reproducible Python tool/tests. **9/9 local tests pass**, including a bad-CANON-hash test, ZIP CRC, source-exact merged image, containment, and blocked release. With no private CANON in a public CI runner, **3 PASS / 6 SKIP**. This does not constitute art acceptance.

## Visual verdict
**REJECTED / NOT_PASSED.** TELEA/NS can wash out eyelid shadows or leave mismatched dark edges; cheek donor introduces flat/pink skin regions and conflicts with hair/eyebrow occlusions. None paints authentic closed eyelids, inner/outer corners, eyelashes, subtle skin crease, cheek blush, or genuine hidden facial anatomy. Do not promote any candidate to CANON, game sprite, or accepted blink frame.

## Specific CP388 painting tasks
- Paint both closed lids **by hand from the same CANON** with separate upper fold, lashes and lower-lid reflected-light strokes. Keep original face/hair/jewelry outside the edit zone completely untouched.
- Reconstruct true behind-eye skin as part of the illustration, not generic algorithmic skin patches. Maintain correct inner/outer eye corners, tapered lashes, upper lid shadow, blush falloff, hair strands that cross the face.
- Review open/closed eyes at native 168×197 and 4× nearest zoom; avoid jagged/flat pink cut-outs and ensure no lingering iris pixels. If image still lacks authentic detail, work from the exact larger facial expression panel in CANON rather than upscaling the 168px crop.
- Submit one **CANON vs painter-drawn closed-eye** approval preview. Only after explicit acceptance create individually drawn 25/50/75% blink frames, test motion timing and painterly edge continuity, separate transparent face/hair semantic layers, then integrate animation.
- Continue the approved +17% silhouette, five expressions, four garment damage states, blue shoe tips and all previously confirmed design constraints; do not copy the Tô Nguyệt Ly style reference into Lâm Thiển art.

## Release gate
`production_release.status=blocked_pending_art`, `sprite_paths={}`, `visual_qa=NOT_PASSED`, `spine_ready=false`, `apk_ready=false`.

## Repro
`python tools/art/cp387_occlusion_and_artist_gate.py --canon <approved-canon> --prior <CP386-frame-03> --out <outdir>`

Do not describe this checkpoint as completed blink animation. It is an evidence-backed diagnosis that all automated eyelid repairs remain unsuitable for art production.
# CP338 — Lâm Thiển | CANON body lock + optional fringe simplification (2026-10-29)

## Decision confirmed by user

**May omit some excess nonfunctional tassels, narrow dangling decorations or redundant tiny fabric fringe if high-fidelity drawing/rigging becomes difficult.** This is optional and conditional; NOT blanket permission to replace CANON V2 or redesign the garment.

**Locked:** Full V2 character identity, body silhouette, the already-integrated +17% proportion, eye colour (warm amber), silver hairstyle, white flower signature accessory, face shape, primary white/light-blue/gold colour and costume coverage, main neckline, braiding/closures/main flowing sleeves and ribbons, four damage states (100/70/50/30) and five approved emotions (shy/angry/pain/embarrassed/alluring).

**Permissible micro-trim:** A few *secondary* loose fringe tips/tassels that are visually redundant, have no important costume fastening function and do not define silhouette. Never remove anchoring closures, the long characteristic ribbons or head ornaments. If removing an item changes the costume's silhouette, neck/chest coverage, signature ornament hierarchy or visible style, this must be **REVISE** not an automatic pass. Design changes cannot compound from view to view.

**Acceptance:** Art candidate is reviewed in a full enough body/costume context, beside original CANON V2. Outcome: `PASS`, `PASS_WITH_MINOR_NOTES`, or `REVISE`. A work-in-progress can qualify for small approved-looking deviations but sprite assets are not production accepted by default.

## Actual files delivered this checkpoint

- Verified original pixel source CANON V2 SHA-256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711` and approved expression sheet SHA-256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`.
- Exported **22 native-resolution, unchanged reference pieces**: 4 wardrobe, 4 integrity states, 4 poses, 4 viewing angles, 1 closeup and 5 emotional references. Explicit category IDs, source boxes/native sizes, SHA-256 and labels live in [CP338 manifest](LAM_THIEN_CP338_CANON_TRIM_MANIFEST.json).
- Files are cropped/duplicated at native resolution, **not redrawn or rigged**. Captured visual index `CP338_CANON_CROPS_VISUAL_QA.png` only for reference. This checkpoint **does not actually remove any tassels from CANON V2**; trims are an option for later art only.
- Binary QA: all 22 exported PNG hashes and sizes verified; direct comparison of 17 CANON pieces with original crop pixels **PASS**. 5 emotion reference PNGs reused from approved CP324 sources. Both approved original source PNGs independently match recorded SHA values.
- Local package `TVK_LamThien_CP338_Canon_Reference_And_Trim_Policy.zip`; Library Development backup at `/Thanh Van Ky/Development/CP338_Canon_Costume_Trim/`. The reference art does NOT belong in the game's production asset registry.

## Next actual implementation step

1. Use full CANON V2 body/costume image directly, not the rejected CP337 Front/3/4 generation. Plan and draw genuine face/wardrobe parts in a stable editing source. Minor tassel trimming may be applied only to non-signature decorations, leaving all structural clothing untouched.
2. Before trying another AI edit or drawing new angle, compare the candidate silhouette, neckline, coverage, signature sleeves, headpiece and face against source side-by-side. Reject changes to any locked identity feature.
3. Separate five emotional parts from the same face-master for each real angle, then verify clean underpaint/true alpha and compositing. This is NOT achieved by crops.
4. After artist/user art acceptance, run CP335 art release gate to register sprites; only then test Spine/animation and Android APK.

## Status

- Canon + emotions: **approved and unchanged**.
- Optional tassel simplification policy: **approved as a limited production tolerance**.
- 22 pixel-preserved reference images: **created and verified**.
- Native high-resolution layered art, independent facial attachments, animation/Spine and APK: **NOT DONE**.
- CP337 rejected candidate pair stays rejected. CP335 sprite release still **blocked_pending_art**.

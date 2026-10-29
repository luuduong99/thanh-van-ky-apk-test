# CP337 — Lâm Thiển | Production portrait art execution checkpoint (2026-10-29)

## Approved and immutable
- Body/face/outfit reference: `LT_CANON_BODY_REF_2026-10-28_V2`, SHA256 `41d42c4bdb36f5d34c8ec4104627be3bab32e888c9f3d98ec86c9703838a9711`. Warm amber eyes, silver hair, white flowers, restrained gold, white/pale-blue clothes, +17% already applied.
- Five expressions: `LT_EXPRESSIONS_FIVE_2026_10_29_APPROVED`, SHA256 `ef1a3b9ba125d202a90d85bf04707edc50cbbcd0b5133055312ee143741cd4d7`: shy, angry, pain, embarrassed, alluring. Facial emotion only; never overrides V2 identity.
- Clothing damage 100/70/50/30 unchanged.

## Actual CP337 step
- Reviewed original V2 PNG and CP336 binary source package locally. Front-labeled native face 145x151, 3/4-labeled 143x151, closeup 230x114: not sufficient native layered production artwork.
- Rechecked connected Drive CANON V2 folder `1zOzVn1bvx2IhgozwWlXRgm8u7bKSnBt8`: original PNG, flat-image ZIP, README, MODEL_CARD; no source ORA/PSD/KRA found. Filename searches found no ORA/PSD/KRA across accessible Drive; this is not proof of nonexistence elsewhere.
- Initiated a NEW standalone candidate FRONT portrait using V2 as source, without infographic or misleading 'Production Ready' labels, Runway task id `880ac92b-bf38-48ae-bd33-e7fde597efd8`. At documentation time task was **PENDING**: no finished image delivered, no observed visual comparison or approval; this is not evidence of art completion. Next output must be inspected against V2 before use. This external image task is not an automated follow-up delivery.
- Existing CP336 validator and CP335 release gate remain authoritative. No new sprite_path or production approval should be applied.

## CP337 status and next actions
1. **FRONT preview:** retrieve/inspect actual candidate if completed; compare anatomical face, amber eyes, silver hair, white floral headpiece, ornament gold moderation, V2 dress; mark any differences. This is a **concept/reference-only** step, not layer art.
2. **True 3/4 preview:** prepare matching alternate head viewpoint without changing face shape, not just another pose crop; inspect side by side at 256/132/64 px.
3. **Production art redraw remains blocked:** requires native high-resolution editable source with transparent semantic parts and clean underlying skin/hair. Face base must have no baked eye or mouth; need stable base per angle, 5 emotion states, independent eyebrow, iris, eye white, lash, lid, mouth and blush. Do not claim 138 QA fixture PNGs represent art.
4. **Validation:** CP336 head-layer validator + CP328 iris colour gate; compare true source checksums; artist visual review and explicit user approval of finished asset separately from already approved canonical concept.
5. **Integration:** only after 4 passes, use CP335 release manifest and Android sprite paths, test Spine/renderer, Android build and device APK. Those remain NOT DONE.

**Current checkpoint:** planning/source verification and a standalone FRONT preview generation request; CP337 production art, 3/4 production master, Spine, Android APK **NOT COMPLETE**.

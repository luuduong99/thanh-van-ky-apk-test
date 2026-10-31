# TVK-02 / WORLD-001 — Map, dialogue and quest logic extraction

**Date:** 2026-10-31. **Branch:** tvk/world-story. **Source commit:** 669123f8db9397c18207a4dbef645a9dbb8a8a39. **Draft PR:** https://github.com/luuduong99/thanh-van-ky-apk-test/pull/3. **Status:** READY_FOR_REVIEW; not merged, not Android-device-verified.

## Audited baseline

- MainActivity.kt currently owns a 390 × 780 Canvas map, four location hit rectangles, six Chapter I dialogue lines and their typewriter, two choice buttons, and tvk_chapter_1 SharedPreferences (complete/choice).
- The existing complete preference means **the opening choice was made**, not that all Chapter I quests/combat are finished. Preserve the legacy flag for migration; UI must not label the full chapter completed because of it.
- docs/CHAPTER_01_IMPLEMENTATION.md and docs/STORY_BIBLE.md document later investigation, NPC feedback and a combat step, but those are not yet implemented as a complete playable loop.
- docs/team/STATIC_FIRST_SCENE_MODE.md supersedes historical body-touch demonstrations. World map markers and dialogue taps stay enabled; body touch reactions must not return via this module.

## New production-neutral Kotlin classes

| File | Responsibility |
|---|---|
| TVKWorldMap.kt | Four existing map hit regions, destination messages, locked secret, pure select(x, y) |
| TVKDialogueEngine.kt | Six original lines with stable IDs/speakers, typewriter typeNext, two-step tap, final-choice gate |
| TVKQuestEngine.kt | Validates the two existing choices; derives objectives and companion; restores legacy save keys |
| tests/world/World001ContractTest.kt | Deterministic Kotlin/JVM contract checks; no Android dependency |

No CANON artwork, animation, wardrobe, character-touch behavior, battle UI, shared source or Android manifests are modified.

## TVK-04 integration contract (proposal, not applied)

1. In MainActivity.kt, keep Canvas rendering/UI coordinates intact but replace hard-coded map hit rectangles with TVKWorldMap.select(x, y); only navigate when destination != null.
2. Map storyIndex/storyVisible to TVKDialogueEngine.Progress; call typeNext for typing; on normal dialogue tap use tap; show two independent choices only when choicesVisible returns true.
3. At choice tap call TVKQuestEngine.choose(progress, "forest" / "sect"); reject null. Persist introChoiceMade to old SharedPreferences complete and choice to choice, then show destinationMessage and current objective.
4. At Activity creation call TVKQuestEngine.restore(storyPrefs.getBoolean("complete", false), storyPrefs.getString("choice", null)) to reject inconsistent legacy state. Keep wardrobe / pose / integrity untouched.
5. WORLD-002 can add NPC-specific quest feedback, investigation progression, story milestones and combat hooks with separate approval. This patch does not claim to implement later steps.

## Test command

    kotlinc app/src/main/java/vn/thanhvanky/prototype/TVKWorldMap.kt app/src/main/java/vn/thanhvanky/prototype/TVKDialogueEngine.kt app/src/main/java/vn/thanhvanky/prototype/TVKQuestEngine.kt tests/world/World001ContractTest.kt -include-runtime -d /tmp/tvk-world-001-tests.jar
    java -cp /tmp/tvk-world-001-tests.jar vn.thanhvanky.prototype.World001ContractTest

**Review gates:** Kotlin/JVM contract run locally (18 PASS / 0 FAIL). TVK-04 then checks integration diffs, Android build and device behavior. Standalone contract tests do not demonstrate an Android build or full Chapter I.

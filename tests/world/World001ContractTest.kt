package vn.thanhvanky.prototype

/** Runs on a plain Kotlin/JVM compiler, without Android or third-party dependencies. */
object World001ContractTest {
    @JvmStatic fun main(args: Array<String>) {
        var passed = 0
        fun checkCase(name: String, test: () -> Unit) {
            test()
            passed++
            println("PASS $name")
        }
        val dialogue = TVKDialogueEngine
        val quest = TVKQuestEngine
        val initial = TVKDialogueEngine.Progress()

        checkCase("six known dialogue lines") { check(dialogue.lines.size == 6) }
        checkCase("stable unique dialogue IDs") { check(dialogue.lines.map { it.id }.distinct().size == 6) }
        checkCase("original wording stays intact") {
            check(dialogue.lines[1].textVi.startsWith("Tô Nguyệt Ly: Huynh về rồi!"))
            check(dialogue.lines[5].textVi == "Tô Nguyệt Ly: Chúng ta nên làm gì trước khi trời tối?")
        }
        checkCase("typewriter increments by two") { check(dialogue.typeNext(initial).visibleChars == 2) }
        checkCase("tap reveals before advancing") {
            val revealed = dialogue.tap(initial)
            check(revealed.lineIndex == 0 && revealed.visibleChars == dialogue.lines[0].textVi.length)
            check(dialogue.tap(revealed) == TVKDialogueEngine.Progress(1, 0))
        }
        checkCase("typing clamps to line length") {
            check(dialogue.typeNext(initial, 99999).visibleChars == dialogue.lines[0].textVi.length)
        }
        checkCase("negative typewriter step rejected") {
            check(runCatching { dialogue.typeNext(initial, -1) }.isFailure)
        }
        checkCase("premature choice rejected") { check(quest.choose(initial, quest.FOREST) == null) }
        val lastIncomplete = TVKDialogueEngine.Progress(5, 1)
        val lastFull = dialogue.tap(lastIncomplete)
        checkCase("choice shown only after last line revealed") {
            check(!dialogue.choicesVisible(lastIncomplete) && dialogue.choicesVisible(lastFull))
        }
        checkCase("last dialogue tap does not skip choice") { check(dialogue.tap(lastFull) == lastFull) }
        checkCase("forest branch objective and companion") {
            val state = requireNotNull(quest.choose(lastFull, quest.FOREST))
            check(state.introChoiceMade)
            check(quest.objective(state)?.id == "investigate_forest")
            check(quest.objective(state)?.destinationId == "forest")
            check(quest.companionIds(state) == listOf("to_nguyet_ly"))
        }
        checkCase("sect branch objective and companion") {
            val state = requireNotNull(quest.choose(lastFull, quest.SECT))
            check(quest.objective(state)?.label == "Hỏi chấp sự về dị tượng")
            check(quest.companionIds(state).size == 1)
        }
        checkCase("invalid choice blocked") { check(quest.choose(lastFull, "secret") == null) }
        checkCase("legacy save keys compatible") {
            check(quest.PREFS_NAME == "tvk_chapter_1" && quest.KEY_COMPLETE == "complete" && quest.KEY_CHOICE == "choice")
            check(quest.restore(true, quest.FOREST).choice == quest.FOREST)
            check(quest.restore(false, quest.FOREST).choice == null)
            check(quest.restore(true, "invalid") == TVKQuestEngine.SavedState())
        }
        checkCase("map has four unique points") {
            check(TVKWorldMap.locations.map { it.id }.toSet().size == 4)
        }
        checkCase("map selection matches current source") {
            check(TVKWorldMap.select(192f, 310f).destination == "sect")
            check(TVKWorldMap.select(92f, 475f).destination == "town")
            check(TVKWorldMap.select(285f, 525f).destination == "forest")
        }
        checkCase("secret remains locked") {
            val result = TVKWorldMap.select(282f, 215f)
            check(result.locked && result.destination == null)
        }
        checkCase("empty map tap has no navigation") {
            check(TVKWorldMap.select(5f, 5f).destination == null)
        }
        println("WORLD-001: $passed PASS, 0 FAIL")
    }
}
